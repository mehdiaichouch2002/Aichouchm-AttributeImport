<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Attribute;

use Aichouchm\AttributeImport\Model\Csv\Validator as CsvValidator;
use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Eav\Api\Data\AttributeInterface;
use Magento\Framework\App\ResourceConnection;

class OptionProcessor
{
    private const COL_STORE  = 1;
    private const COL_VALUE  = 2;
    private const COL_SWATCH = 3;

    public function __construct(
        private readonly ResourceConnection $resourceConnection,
        private readonly StoreResolver      $storeResolver
    ) {}

    /**
     * @param  array[]           $groups         [{admin: row, stores: [row…]}, …]
     * @param  array             $existingOptions [value => option_id] at store_id=0
     * @param  int               $swatchType      CsvValidator::SWATCH_* constant
     * @return array{imported: int, skipped: int, skippedValues: string[]}
     */
    public function processGroups(
        array $groups,
        array $existingOptions,
        int $swatchType,
        AttributeInterface $attribute
    ): array {
        $newOptions = [];
        $labelRows  = [];
        $swatchRows = [];
        $defaultKey = null;
        $skipped    = [];

        [$sortOrderCol, $isDefaultCol] = $this->dataColumnOffsets($swatchType);

        foreach ($groups as $group) {
            $adminRow = $group['admin'];
            $value    = $adminRow[self::COL_VALUE];

            if (array_key_exists($value, $existingOptions)) {
                $skipped[] = $value;
                continue;
            }

            $key = 'new_' . count($newOptions);

            $newOptions[$key] = [
                'attribute_id' => $attribute->getAttributeId(),
                'sort_order'   => (int) ($adminRow[$sortOrderCol] ?? 0),
            ];

            if (($adminRow[$isDefaultCol] ?? '0') === '1') {
                $defaultKey = $key;
            }

            $labelRows[] = ['key' => $key, 'store_id' => 0, 'value' => $value];

            if ($swatchType !== CsvValidator::SWATCH_NONE) {
                $swatchVal    = $adminRow[self::COL_SWATCH] ?? '';
                $swatchRows[] = [
                    'key'      => $key,
                    'store_id' => 0,
                    'type'     => $this->detectSwatchType($swatchVal),
                    'value'    => $swatchVal,
                ];
            }

            foreach ($group['stores'] as $storeRow) {
                $storeId     = $this->storeResolver->getStoreId($storeRow[self::COL_STORE]);
                $labelRows[] = ['key' => $key, 'store_id' => $storeId, 'value' => $storeRow[self::COL_VALUE]];

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

        // Insert one row at a time to capture each lastInsertId before batching labels/swatches
        $keyToOptionId = [];
        foreach ($newOptions as $key => $optionData) {
            $connection->insert($optionTable, $optionData);
            $keyToOptionId[$key] = (int) $connection->lastInsertId();
        }

        if (!empty($labelRows)) {
            $rows = [];
            foreach ($labelRows as $lr) {
                $rows[] = ['option_id' => $keyToOptionId[$lr['key']], 'store_id' => $lr['store_id'], 'value' => $lr['value']];
            }
            $connection->insertMultiple($valueTable, $rows);
        }

        if ($defaultKey !== null && isset($keyToOptionId[$defaultKey])) {
            $connection->update(
                $this->resourceConnection->getTableName('eav_attribute'),
                ['default_value' => (string) $keyToOptionId[$defaultKey]],
                ['attribute_id = ?' => $attribute->getAttributeId()]
            );
        }

        if (!empty($swatchRows)) {
            $rows = [];
            foreach ($swatchRows as $sr) {
                $rows[] = ['option_id' => $keyToOptionId[$sr['key']], 'store_id' => $sr['store_id'], 'type' => $sr['type'], 'value' => $sr['value']];
            }
            $connection->insertOnDuplicate($swatchTable, $rows, ['type', 'value']);
        }
    }

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

    private function dataColumnOffsets(int $swatchType): array
    {
        return $swatchType !== CsvValidator::SWATCH_NONE ? [4, 5] : [3, 4];
    }
}
