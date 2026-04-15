<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Attribute;

use Aichouchm\AttributeImport\Model\Csv\Validator as CsvValidator;
use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Eav\Api\Data\AttributeInterface;
use Magento\Framework\App\ResourceConnection;

class OptionProcessor
{
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

        $sortOrderCol = $swatchType !== CsvValidator::SWATCH_NONE
            ? CsvValidator::COL_SORT_ORDER_SWATCH
            : CsvValidator::COL_SORT_ORDER_PLAIN;

        $isDefaultCol = $swatchType !== CsvValidator::SWATCH_NONE
            ? CsvValidator::COL_IS_DEFAULT_SWATCH
            : CsvValidator::COL_IS_DEFAULT_PLAIN;

        foreach ($groups as $group) {
            $adminRow = $group['admin'];
            $value    = $adminRow[CsvValidator::COL_VALUE];

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
                $swatchRows[] = [
                    'key'      => $key,
                    'store_id' => 0,
                    'type'     => 1,
                    'value'    => $adminRow[CsvValidator::COL_SWATCH] ?? '',
                ];
            }

            foreach ($group['stores'] as $storeRow) {
                $storeId     = $this->storeResolver->getStoreId($storeRow[CsvValidator::COL_STORE_VIEW]);
                $labelRows[] = ['key' => $key, 'store_id' => $storeId, 'value' => $storeRow[CsvValidator::COL_VALUE]];
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

}
