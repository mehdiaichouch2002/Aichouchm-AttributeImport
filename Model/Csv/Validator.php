<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Csv;

use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Eav\Model\Entity\Attribute\AbstractAttribute;

/**
 * Stateless CSV validation: returns a list of human-readable errors, never writes.
 */
class Validator
{
    /**
     * Plain select/multiselect: no swatch data
     */
    public const SWATCH_NONE = -1;

    /**
     * Text swatch: eav_attribute_option_swatch.type = 0, value = label per store
     */
    public const SWATCH_TEXT = 0;

    /**
     * Visual swatch: eav_attribute_option_swatch.type = 1, value = #RRGGBB
     */
    public const SWATCH_VISUAL = 1;

    /**
     * Unified 6-column CSV format:
     * attribute_code | store_view | value | hex_code | sort_order | is_default
     */
    public const COL_ATTRIBUTE_CODE = 0;
    public const COL_STORE_VIEW     = 1;
    public const COL_VALUE          = 2;
    public const COL_SWATCH         = 3;
    public const COL_SORT_ORDER     = 4;
    public const COL_IS_DEFAULT     = 5;

    public const EXPECTED_HEADERS = ['attribute_code', 'store_view', 'value', 'hex_code', 'sort_order', 'is_default'];

    private const MAX_VALUE_LENGTH = 255;

    /**
     * @param StoreResolver $storeResolver
     */
    public function __construct(
        private readonly StoreResolver $storeResolver
    ) {
    }

    /**
     * Resolve the swatch type from the attribute's additional_data.
     *
     * @param AbstractAttribute $attribute
     * @return int One of the SWATCH_* constants
     */
    public function getSwatchType(AbstractAttribute $attribute): int
    {
        $additional = json_decode((string) $attribute->getData('additional_data'), true);

        return match (is_array($additional) ? ($additional['swatch_input_type'] ?? null) : null) {
            'visual' => self::SWATCH_VISUAL,
            'text'   => self::SWATCH_TEXT,
            default  => self::SWATCH_NONE,
        };
    }

    /**
     * Validate the header row.
     *
     * @param string[] $headerRow
     * @return string[]
     */
    public function validateHeaders(array $headerRow): array
    {
        $expectedCount = count(self::EXPECTED_HEADERS);

        if (count($headerRow) !== $expectedCount) {
            return [
                (string) __(
                    'Invalid column count: expected %1, got %2. Expected columns: %3',
                    $expectedCount,
                    count($headerRow),
                    implode(', ', self::EXPECTED_HEADERS)
                ),
            ];
        }

        $errors = [];
        foreach ($headerRow as $i => $cell) {
            if (strtolower($cell) !== self::EXPECTED_HEADERS[$i]) {
                $errors[] = (string) __(
                    'Column %1: expected "%2", got "%3"',
                    $i + 1,
                    self::EXPECTED_HEADERS[$i],
                    $cell
                );
            }
        }

        return $errors;
    }

    /**
     * Validate data rows (header excluded).
     *
     * @param array<int,string[]> $rows
     * @param string $attributeCode
     * @param int $swatchType
     * @return string[]
     */
    public function validateRows(array $rows, string $attributeCode, int $swatchType): array
    {
        $errors          = [];
        $adminValues     = [];
        $optionStores    = [];
        $defaultSelected = false;
        $hasAdminRow     = false;
        $columnCount     = count(self::EXPECTED_HEADERS);

        foreach (array_values($rows) as $index => $row) {
            $rowNum = $index + 2;

            if (count($row) !== $columnCount) {
                $errors[] = (string) __('Row %1: expected %2 columns, got %3.', $rowNum, $columnCount, count($row));
                continue;
            }

            $storeCode = $row[self::COL_STORE_VIEW];
            $value     = $row[self::COL_VALUE];
            $isAdmin   = $this->storeResolver->isAdminStoreCode($storeCode);

            array_push($errors, ...$this->validateValue($rowNum, $storeCode, $value));

            if ($row[self::COL_ATTRIBUTE_CODE] !== $attributeCode) {
                $errors[] = (string) __(
                    'Row %1: attribute_code "%2" does not match selected attribute "%3".',
                    $rowNum,
                    $row[self::COL_ATTRIBUTE_CODE],
                    $attributeCode
                );
            }

            if (!$isAdmin) {
                array_push($errors, ...$this->validateStoreRow($rowNum, $storeCode, $hasAdminRow, $optionStores));
                $optionStores[] = strtolower($storeCode);
                continue;
            }

            $hasAdminRow  = true;
            $optionStores = [];

            $normalised = mb_strtolower($value, 'UTF-8');
            if ($value !== '' && isset($adminValues[$normalised])) {
                $errors[] = (string) __(
                    'Row %1: Duplicate option value "%2" within the CSV (admin store).',
                    $rowNum,
                    $value
                );
            }
            $adminValues[$normalised] = true;

            array_push($errors, ...$this->validateAdminRow($rowNum, $row, $swatchType, $defaultSelected));
        }

        return $errors;
    }

    /**
     * Checks shared by every row: required cells, length and safe characters.
     *
     * @param int $rowNum
     * @param string $storeCode
     * @param string $value
     * @return string[]
     */
    private function validateValue(int $rowNum, string $storeCode, string $value): array
    {
        $errors = [];

        if ($storeCode === '') {
            $errors[] = (string) __('Row %1: "%2" is required and cannot be empty.', $rowNum, 'store_view');
        }
        if ($value === '') {
            $errors[] = (string) __('Row %1: "%2" is required and cannot be empty.', $rowNum, 'value');
            return $errors;
        }
        if (mb_strlen($value, 'UTF-8') > self::MAX_VALUE_LENGTH) {
            $errors[] = (string) __('Row %1: value exceeds the %2 character limit.', $rowNum, self::MAX_VALUE_LENGTH);
        }
        if (preg_match('/[\x00-\x1F\x7F]/u', $value) === 1) {
            $errors[] = (string) __('Row %1: value contains line breaks or control characters.', $rowNum);
        }
        if (preg_match('/<[^>]*>/', $value) === 1) {
            $errors[] = (string) __('Row %1: value must not contain HTML tags.', $rowNum);
        }

        return $errors;
    }

    /**
     * Checks for the admin (default) row that opens an option group.
     *
     * @param int $rowNum
     * @param string[] $row
     * @param int $swatchType
     * @param bool $defaultSelected Updated when this row is the default option
     * @return string[]
     */
    private function validateAdminRow(int $rowNum, array $row, int $swatchType, bool &$defaultSelected): array
    {
        $errors = [];

        $sortOrder = $row[self::COL_SORT_ORDER];
        if (!is_numeric($sortOrder)) {
            $errors[] = (string) __('Row %1: sort_order must be a number, got "%2".', $rowNum, $sortOrder);
        } elseif ((float) $sortOrder < 0) {
            $errors[] = (string) __('Row %1: sort_order must be 0 or greater, got "%2".', $rowNum, $sortOrder);
        } elseif (!ctype_digit($sortOrder)) {
            $errors[] = (string) __('Row %1: sort_order must be a whole number, got "%2".', $rowNum, $sortOrder);
        }

        $isDefault = $row[self::COL_IS_DEFAULT];
        if (!in_array($isDefault, ['0', '1'], true)) {
            $errors[] = (string) __('Row %1: is_default must be 0 or 1, got "%2".', $rowNum, $isDefault);
        } elseif ($isDefault === '1') {
            if ($defaultSelected) {
                $errors[] = (string) __('Row %1: is_default=1 is already set for another option.', $rowNum);
            }
            $defaultSelected = true;
        }

        if ($swatchType === self::SWATCH_VISUAL) {
            $hex = $row[self::COL_SWATCH];
            if ($hex === '') {
                $errors[] = (string) __('Row %1: hex_code is required for visual swatch attributes.', $rowNum);
            } elseif (preg_match('/^#[A-Fa-f0-9]{6}$/', $hex) !== 1) {
                $errors[] = (string) __(
                    'Row %1: hex_code "%2" is not a valid hex colour (expected #RRGGBB).',
                    $rowNum,
                    $hex
                );
            }
        }

        return $errors;
    }

    /**
     * Checks for a translation row (non-admin store view).
     *
     * @param int $rowNum
     * @param string $storeCode
     * @param bool $hasAdminRow
     * @param string[] $optionStores Store codes already used by the current option
     * @return string[]
     */
    private function validateStoreRow(int $rowNum, string $storeCode, bool $hasAdminRow, array $optionStores): array
    {
        $errors = [];

        if (!$hasAdminRow) {
            $errors[] = (string) __(
                'Row %1: store view row "%2" appears before any admin (default) row.',
                $rowNum,
                $storeCode
            );
        }
        if ($storeCode !== '' && !$this->storeResolver->isValidStoreCode($storeCode)) {
            $errors[] = (string) __('Row %1: Store view "%2" does not exist in Magento.', $rowNum, $storeCode);
        }
        if (in_array(strtolower($storeCode), $optionStores, true)) {
            $errors[] = (string) __(
                'Row %1: Store view "%2" appears more than once for the same option.',
                $rowNum,
                $storeCode
            );
        }

        return $errors;
    }
}
