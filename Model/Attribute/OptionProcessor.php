<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Attribute;

use Aichouchm\AttributeImport\Model\Csv\Validator as CsvValidator;
use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Eav\Api\Data\AttributeInterface;
use Magento\Framework\App\ResourceConnection;

/**
 * Persists attribute option groups to the database.
 *
 * WHY DIRECT DB WRITES INSTEAD OF $attribute->setOption() + repository->save():
 *   The Magento API approach is correct for 1-20 options but becomes very slow
 *   at scale: for each option the attribute model builds an entire options array
 *   in memory, then the resource model iterates it with individual INSERT calls.
 *   For 500 options × 3 stores = 1500 label rows, that's 1500 separate INSERTs.
 *
 *   This processor batches the DB work:
 *     1. Insert all new option rows individually (needed for lastInsertId())
 *     2. Batch-insert ALL labels with a single insertMultiple() call
 *     3. Batch-insert ALL swatches with a single insertOnDuplicate() call
 *
 *   Result: (n_new_options) + 1 + 1 = O(n) → O(1) queries as n grows.
 *
 * SWATCH COLUMN IN eav_attribute_option_swatch:
 *   type = 1 → hex colour (#RRGGBB)
 *   type = 2 → image URL
 *   type = 0 → text swatch label
 *
 * DEFAULT VALUE:
 *   Written to eav_attribute.default_value as the raw option_id integer.
 */
class OptionProcessor
{
    // Column indices in a data row (admin-store row)
    private const COL_ATTR_CODE  = 0;
    private const COL_STORE      = 1;
    private const COL_VALUE      = 2;
    private const COL_SWATCH     = 3; // only when swatchType !== NONE
    // sort_order and is_default shift by 1 when there's a swatch column

    public function __construct(
        private readonly ResourceConnection $resourceConnection,
        private readonly StoreResolver      $storeResolver
    ) {}

    /**
     * Processes a list of option groups and writes them to the database.
     *
     * An option group is an associative array:
     *   [
     *     'admin'  => string[],   // the admin-store CSV row
     *     'stores' => string[][],  // zero or more store-view rows
     *   ]
     *
     * @param  array[]          $groups        Pre-grouped option data
     * @param  array            $existingOptions [value => option_id] for store_id=0
     * @param  int              $swatchType    CsvValidator::SWATCH_* constant
     * @param  AttributeInterface $attribute
     * @return array{imported: int, skipped: int, skippedValues: string[]}
     */
    public function processGroups(
        array $groups,
        array $existingOptions,
        int $swatchType,
        AttributeInterface $attribute
    ): array {
        $newOptions   = [];   // keyed by a temporary string key
        $labelRows    = [];
        $swatchRows   = [];
        $defaultKey   = null;
        $skipped      = [];

        [$sortOrderCol, $isDefaultCol] = $this->dataColumnOffsets($swatchType);

        foreach ($groups as $group) {
            $adminRow = $group['admin'];
            $value    = $adminRow[self::COL_VALUE];

            // Skip duplicates (already in DB) — log the skip in the caller
            if (array_key_exists($value, $existingOptions)) {
                $skipped[] = $value;
                continue;
            }

            $key = 'new_' . count($newOptions);

            $newOptions[$key] = [
                'attribute_id' => $attribute->getAttributeId(),
                'sort_order'   => (int) ($adminRow[$sortOrderCol] ?? 0),
            ];

            // Track which key is the default
            if (($adminRow[$isDefaultCol] ?? '0') === '1') {
                $defaultKey = $key;
            }

            // Admin store label (store_id = 0)
            $labelRows[] = ['key' => $key, 'store_id' => 0, 'value' => $value];

            // Swatch for admin store
            if ($swatchType !== CsvValidator::SWATCH_NONE) {
                $swatchVal = $adminRow[self::COL_SWATCH] ?? '';
                $swatchRows[] = [
                    'key'      => $key,
                    'store_id' => 0,
                    'type'     => $this->detectSwatchType($swatchVal),
                    'value'    => $swatchVal,
                ];
            }

            // Store-view labels (and text swatch per store if applicable)
            foreach ($group['stores'] as $storeRow) {
                $storeCode = $storeRow[self::COL_STORE];
                $storeId   = $this->storeResolver->getStoreId($storeCode);
                $labelRows[] = ['key' => $key, 'store_id' => $storeId, 'value' => $storeRow[self::COL_VALUE]];

                // Text swatches can have per-store labels
                if ($swatchType === CsvValidator::SWATCH_TEXT) {
                    $swatchRows[] = [
                        'key'      => $key,
                        'store_id' => $storeId,
                        'type'     => 0,
                        'value'    => $storeRow[self::COL_SWATCH] ?? $storeRow[self::COL_VALUE],
                    ];
                }
            }
        }

        if (!empty($newOptions)) {
            $this->bulkSave($newOptions, $labelRows, $swatchRows, $defaultKey, $attribute);
        }

        return [
            'imported'      => count($newOptions),
            'skipped'       => count($skipped),
            'skippedValues' => $skipped,
        ];
    }

    // ── Private persistence helpers ───────────────────────────────────────────

    private function bulkSave(
        array $newOptions,
        array $labelRows,
        array $swatchRows,
        ?string $defaultKey,
        AttributeInterface $attribute
    ): void {
        $connection  = $this->resourceConnection->getConnection();
        $optionTable = $this->resourceConnection->getTableName('eav_attribute_option');
        $valueTable  = $this->resourceConnection->getTableName('eav_attribute_option_value');
        $swatchTable = $this->resourceConnection->getTableName('eav_attribute_option_swatch');

        // 1. Insert options one-by-one to collect lastInsertId per row.
        //    WHY NOT insertMultiple: we need the auto-incremented option_id for
        //    each row to build the labels and swatch arrays.
        $keyToOptionId = [];
        foreach ($newOptions as $key => $optionData) {
            $connection->insert($optionTable, $optionData);
            $keyToOptionId[$key] = (int) $connection->lastInsertId();
        }

        // 2. Batch-insert all labels in ONE query.
        if (!empty($labelRows)) {
            $rows = [];
            foreach ($labelRows as $lr) {
                $rows[] = [
                    'option_id' => $keyToOptionId[$lr['key']],
                    'store_id'  => $lr['store_id'],
                    'value'     => $lr['value'],
                ];
            }
            $connection->insertMultiple($valueTable, $rows);
        }

        // 3. Set default value on the attribute row.
        if ($defaultKey !== null && isset($keyToOptionId[$defaultKey])) {
            $connection->update(
                $this->resourceConnection->getTableName('eav_attribute'),
                ['default_value' => (string) $keyToOptionId[$defaultKey]],
                ['attribute_id = ?' => $attribute->getAttributeId()]
            );
        }

        // 4. Batch-insert/update all swatches in ONE query.
        if (!empty($swatchRows)) {
            $rows = [];
            foreach ($swatchRows as $sr) {
                $rows[] = [
                    'option_id' => $keyToOptionId[$sr['key']],
                    'store_id'  => $sr['store_id'],
                    'type'      => $sr['type'],
                    'value'     => $sr['value'],
                ];
            }
            $connection->insertOnDuplicate($swatchTable, $rows, ['type', 'value']);
        }
    }

    /**
     * Detects the eav_attribute_option_swatch.type value from a swatch string.
     *   1 → hex colour
     *   2 → image URL
     *   0 → text (fallback)
     */
    private function detectSwatchType(string $value): int
    {
        $value = trim($value);
        if (preg_match('/^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$/', $value)) {
            return 1;
        }
        if (preg_match('/^(https?:\/\/|\/\/|\/|\.\/).*\.(jpg|jpeg|png|gif|svg|webp)$/i', $value)) {
            return 2;
        }
        return 0;
    }

    /**
     * Returns [sortOrderColumnIndex, isDefaultColumnIndex].
     */
    private function dataColumnOffsets(int $swatchType): array
    {
        return $swatchType !== CsvValidator::SWATCH_NONE ? [4, 5] : [3, 4];
    }
}
