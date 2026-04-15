<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Csv;

use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Catalog\Model\Product;
use Magento\Catalog\Model\ResourceModel\Eav\AttributeFactory;

class Validator
{
    public const SWATCH_NONE   = -1;
    public const SWATCH_VISUAL =  1;

    private const SWATCH_COL_NAMES = ['hex_code'];

    public function __construct(
        private readonly StoreResolver    $storeResolver,
        private readonly AttributeFactory $attributeFactory
    ) {}

    public function getSwatchType(string $attributeCode): int
    {
        $attribute  = $this->attributeFactory->create()->loadByCode(Product::ENTITY, $attributeCode);
        $additional = json_decode($attribute->getAdditionalData() ?? '{}', true);

        return match ($additional['swatch_input_type'] ?? null) {
            'visual' => self::SWATCH_VISUAL,
            default  => self::SWATCH_NONE,
        };
    }

    /**
     * @param string[] $headerRow
     * @return string[]
     */
    public function validateHeaders(array $headerRow, int $swatchType): array
    {
        $expected = $this->expectedHeaders($swatchType);
        $errors   = [];

        $expectedCount = count($expected);
        $actualCount   = count($headerRow);

        if ($actualCount !== $expectedCount) {
            return [
                (string) __('Invalid column count: expected %1, got %2. Expected columns: %3',
                    $expectedCount, $actualCount, implode(', ', $expected))
            ];
        }

        foreach ($headerRow as $i => $cell) {
            $cell = strtolower(trim($cell));
            $exp  = $expected[$i];

            if (is_array($exp)) {
                if (!in_array($cell, $exp, true)) {
                    $errors[] = (string) __('Column %1: expected one of "%2", got "%3"',
                        $i + 1, implode('", "', $exp), $cell);
                }
            } elseif ($cell !== $exp) {
                $errors[] = (string) __('Column %1: expected "%2", got "%3"', $i + 1, $exp, $cell);
            }
        }

        return $errors;
    }

    /**
     * @param  array[] $rows Data rows (header excluded)
     * @return string[]
     */
    public function validateRows(array $rows, string $attributeCode, int $swatchType): array
    {
        $errors          = [];
        $adminValues     = [];
        $optionStores    = [];
        $defaultSelected = false;
        $expectAdminNext = true;

        [$sortOrderCol, $isDefaultCol] = $this->dataColumnOffsets($swatchType);

        foreach ($rows as $index => $row) {
            $rowNum    = $index + 2;
            $storeCode = trim($row[1] ?? '');
            $isAdmin   = $this->isAdminStoreCode($storeCode);

            foreach ([0 => 'attribute_code', 1 => 'store_view', 2 => 'value'] as $col => $name) {
                if (($row[$col] ?? '') === '') {
                    $errors[] = (string) __('Row %1: "%2" is required and cannot be empty.', $rowNum, $name);
                }
            }

            if (($row[0] ?? '') !== $attributeCode) {
                $errors[] = (string) __('Row %1: attribute_code "%2" does not match selected attribute "%3".',
                    $rowNum, $row[0] ?? '', $attributeCode);
            }

            if ($isAdmin) {
                $optionStores    = [];
                $expectAdminNext = false;
                $value           = $row[2] ?? '';

                if (in_array($value, $adminValues, true)) {
                    $errors[] = (string) __('Row %1: Duplicate option value "%2" within the CSV (admin store).',
                        $rowNum, $value);
                }
                $adminValues[] = $value;

                if (!is_numeric($row[$sortOrderCol] ?? '')) {
                    $errors[] = (string) __('Row %1: sort_order must be a number, got "%2".',
                        $rowNum, $row[$sortOrderCol] ?? '');
                }

                $isDefaultVal = $row[$isDefaultCol] ?? '';
                if (!in_array($isDefaultVal, ['0', '1'], true)) {
                    $errors[] = (string) __('Row %1: is_default must be 0 or 1, got "%2".', $rowNum, $isDefaultVal);
                }

                if ($isDefaultVal === '1') {
                    if ($defaultSelected) {
                        $errors[] = (string) __('Row %1: is_default=1 is already set for another option.', $rowNum);
                    }
                    $defaultSelected = true;
                }

                if ($swatchType === self::SWATCH_VISUAL) {
                    $swatchVal = $row[3] ?? '';
                    if (!$this->isValidSwatchValue($swatchVal)) {
                        $errors[] = (string) __('Row %1: swatch value "%2" is not a valid hex color or image URL.',
                            $rowNum, $swatchVal);
                    }
                }
            } else {
                if ($expectAdminNext) {
                    $errors[] = (string) __('Row %1: First row must have store_view "admin" or "default". Got "%2".',
                        $rowNum, $storeCode);
                    $expectAdminNext = false;
                }

                if (!$this->storeResolver->isValidStoreCode($storeCode)) {
                    $errors[] = (string) __('Row %1: Store view "%2" does not exist in Magento.', $rowNum, $storeCode);
                }

                $normalised = strtolower($storeCode);
                if (in_array($normalised, $optionStores, true)) {
                    $errors[] = (string) __('Row %1: Store view "%2" appears more than once for the same option.',
                        $rowNum, $storeCode);
                }
                $optionStores[] = $normalised;
            }
        }

        return $errors;
    }

    private function isAdminStoreCode(string $code): bool
    {
        return in_array(strtolower($code), ['admin', 'default'], true);
    }

    private function dataColumnOffsets(int $swatchType): array
    {
        return $swatchType !== self::SWATCH_NONE ? [4, 5] : [3, 4];
    }

    private function expectedHeaders(int $swatchType): array
    {
        $base = ['attribute_code', 'store_view', 'value'];
        if ($swatchType !== self::SWATCH_NONE) {
            return array_merge($base, [self::SWATCH_COL_NAMES, 'sort_order', 'is_default']);
        }
        return array_merge($base, ['sort_order', 'is_default']);
    }

    private function isValidSwatchValue(string $value): bool
    {
        return (bool) preg_match('/^#[A-Fa-f0-9]{6}$/', trim($value));
    }
}
