<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Attribute;

use Aichouchm\AttributeImport\Model\Csv\Validator as CsvValidator;
use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Eav\Model\Entity\Attribute\AbstractAttribute;
use Magento\Framework\App\ResourceConnection;
use Magento\Framework\Exception\LocalizedException;
use Magento\Store\Model\Store;
use Throwable;

/**
 * Writes new options, their store labels and swatches in a single transaction.
 */
class OptionProcessor
{
    /**
     * @param ResourceConnection $resourceConnection
     * @param StoreResolver $storeResolver
     */
    public function __construct(
        private readonly ResourceConnection $resourceConnection,
        private readonly StoreResolver $storeResolver
    ) {
    }

    /**
     * Create every option group whose admin label does not exist yet.
     *
     * @param array<int,array{admin:string[],stores:array<int,string[]>}> $groups
     * @param array<string,int> $existingOptions Lower-cased admin label => option ID
     * @param int $swatchType One of CsvValidator::SWATCH_*
     * @param AbstractAttribute $attribute
     * @return array{imported:int,skipped:int,skippedValues:string[]}
     * @throws LocalizedException
     * @throws Throwable
     */
    public function processGroups(
        array $groups,
        array $existingOptions,
        int $swatchType,
        AbstractAttribute $attribute
    ): array {
        $attributeId = (int) $attribute->getAttributeId();
        $newOptions  = [];
        $labelRows   = [];
        $swatchRows  = [];
        $defaultKey  = null;
        $skipped     = [];

        foreach ($groups as $group) {
            $adminRow   = $group['admin'];
            $value      = $adminRow[CsvValidator::COL_VALUE];
            $normalised = mb_strtolower($value, 'UTF-8');

            if (isset($existingOptions[$normalised])) {
                $skipped[] = $value;
                continue;
            }
            // Guards against the same label appearing twice in one file.
            $existingOptions[$normalised] = 0;

            $key = count($newOptions);
            $newOptions[$key] = [
                'attribute_id' => $attributeId,
                'sort_order'   => (int) $adminRow[CsvValidator::COL_SORT_ORDER],
            ];

            if ($adminRow[CsvValidator::COL_IS_DEFAULT] === '1') {
                $defaultKey = $key;
            }

            $labels = [Store::DEFAULT_STORE_ID => $value];
            foreach ($group['stores'] as $storeRow) {
                $storeId          = $this->storeResolver->getStoreId($storeRow[CsvValidator::COL_STORE_VIEW]);
                $labels[$storeId] = $storeRow[CsvValidator::COL_VALUE];
            }

            foreach ($labels as $storeId => $label) {
                $labelRows[] = ['key' => $key, 'store_id' => $storeId, 'value' => $label];

                if ($swatchType === CsvValidator::SWATCH_TEXT) {
                    $swatchRows[] = ['key' => $key, 'store_id' => $storeId, 'type' => 0, 'value' => $label];
                }
            }

            if ($swatchType === CsvValidator::SWATCH_VISUAL) {
                $swatchRows[] = [
                    'key'      => $key,
                    'store_id' => Store::DEFAULT_STORE_ID,
                    'type'     => 1,
                    'value'    => $adminRow[CsvValidator::COL_SWATCH],
                ];
            }
        }

        if ($newOptions !== []) {
            $this->bulkSave($attributeId, $newOptions, $labelRows, $swatchRows, $defaultKey);
        }

        return [
            'imported'      => count($newOptions),
            'skipped'       => count($skipped),
            'skippedValues' => $skipped,
        ];
    }

    /**
     * Insert options one by one (to capture IDs), then labels and swatches in bulk.
     *
     * @param int $attributeId
     * @param array<int,array{attribute_id:int,sort_order:int}> $newOptions
     * @param array<int,array{key:int,store_id:int,value:string}> $labelRows
     * @param array<int,array{key:int,store_id:int,type:int,value:string}> $swatchRows
     * @param int|null $defaultKey
     * @return void
     * @throws Throwable
     */
    private function bulkSave(
        int $attributeId,
        array $newOptions,
        array $labelRows,
        array $swatchRows,
        ?int $defaultKey
    ): void {
        $connection = $this->resourceConnection->getConnection();

        $connection->beginTransaction();
        try {
            $optionIds = [];
            foreach ($newOptions as $key => $optionData) {
                $connection->insert($this->resourceConnection->getTableName('eav_attribute_option'), $optionData);
                $optionIds[$key] = (int) $connection->lastInsertId();
            }

            $connection->insertOnDuplicate(
                $this->resourceConnection->getTableName('eav_attribute_option_value'),
                array_map(
                    static fn (array $row): array => [
                        'option_id' => $optionIds[$row['key']],
                        'store_id'  => $row['store_id'],
                        'value'     => $row['value'],
                    ],
                    $labelRows
                ),
                ['value']
            );

            if ($swatchRows !== []) {
                $connection->insertOnDuplicate(
                    $this->resourceConnection->getTableName('eav_attribute_option_swatch'),
                    array_map(
                        static fn (array $row): array => [
                            'option_id' => $optionIds[$row['key']],
                            'store_id'  => $row['store_id'],
                            'type'      => $row['type'],
                            'value'     => $row['value'],
                        ],
                        $swatchRows
                    ),
                    ['type', 'value']
                );
            }

            if ($defaultKey !== null) {
                $connection->update(
                    $this->resourceConnection->getTableName('eav_attribute'),
                    ['default_value' => (string) $optionIds[$defaultKey]],
                    ['attribute_id = ?' => $attributeId]
                );
            }

            $connection->commit();
        } catch (Throwable $e) {
            $connection->rollBack();
            throw $e;
        }
    }
}
