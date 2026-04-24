<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Csv;

use Aichouchm\AttributeImport\Service\StoreResolver;
use JsonException;
use Magento\Catalog\Model\Product;
use Magento\Eav\Model\Config as EavConfig;

/**
 * Class Validator
 */
class Validator
{
    /**
     * Non-swatch attribute (no swatch column in CSV)
     */
    public const SWATCH_NONE   = -1;

    /**
     * Visual swatch attribute (hex colour or image URL)
     */
    public const SWATCH_VISUAL =  1;

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

    /**
     * @var string[]
     */
    private const EXPECTED_HEADERS = ['attribute_code', 'store_view', 'value', 'hex_code', 'sort_order', 'is_default'];

    /**
     * @param StoreResolver $storeResolver
     * @param EavConfig $eavConfig
     */
    public function __construct(
        private readonly StoreResolver $storeResolver,
        private readonly EavConfig     $eavConfig
    ) {}

    /**
     * @param string $attributeCode
     * @return int
     * @throws JsonException
     */
    public function getSwatchType(string $attributeCode): int
    {
        $attribute  = $this->eavConfig->getAttribute(Product::ENTITY, $attributeCode);
        $additional = json_decode($attribute->getAdditionalData() ?? '{}', true, 512, JSON_THROW_ON_ERROR);

        return match ($additional['swatch_input_type'] ?? null) {
            'visual' => self::SWATCH_VISUAL,
            default  => self::SWATCH_NONE,
        };
    }

    /**
     * @param array $headerRow
     * @return array|string[]
     */
    public function validateHeaders(array $headerRow): array
    {
        $expectedCount = count(self::EXPECTED_HEADERS);
        $actualCount   = count($headerRow);

        if ($actualCount !== $expectedCount) {
            return [
                (string) __('Invalid column count: expected %1, got %2. Expected columns: %3',
                    $expectedCount, $actualCount, implode(', ', self::EXPECTED_HEADERS))
            ];
        }

        $errors = [];
        foreach ($headerRow as $i => $cell) {
            if (strtolower(trim($cell)) !== self::EXPECTED_HEADERS[$i]) {
                $errors[] = (string) __('Column %1: expected "%2", got "%3"',
                    $i + 1, self::EXPECTED_HEADERS[$i], $cell);
            }
        }

        return $errors;
    }

    /**
     * @param array $rows
     * @param string $attributeCode
     * @param int $swatchType
     * @return array
     */
    public function validateRows(array $rows, string $attributeCode, int $swatchType): array
    {
        $errors          = [];
        $adminValues     = [];
        $optionStores    = [];
        $defaultSelected = false;
        $hasAdminRow     = false;

        foreach ($rows as $index => $row) {
            $rowNum    = $index + 2;
            $storeCode = trim($row[self::COL_STORE_VIEW] ?? '');
            $isAdmin   = $this->isAdminStoreCode($storeCode);

            foreach ([
                self::COL_STORE_VIEW => 'store_view',
                self::COL_VALUE      => 'value',
            ] as $col => $name) {
                if (($row[$col] ?? '') === '') {
                    $errors[] = (string) __('Row %1: "%2" is required and cannot be empty.', $rowNum, $name);
                }
            }

            if (mb_strlen($row[self::COL_VALUE] ?? '', 'UTF-8') > 255) {
                $errors[] = (string) __('Row %1: value exceeds the 255 character limit.', $rowNum);
            }

            if (($row[self::COL_ATTRIBUTE_CODE] ?? '') !== $attributeCode) {
                $errors[] = (string) __('Row %1: attribute_code "%2" does not match selected attribute "%3".',
                    $rowNum, $row[self::COL_ATTRIBUTE_CODE] ?? '', $attributeCode);
            }

            if ($isAdmin) {
                $hasAdminRow     = true;
                $optionStores    = [];
                $value           = $row[self::COL_VALUE] ?? '';

                if (in_array($value, $adminValues, true)) {
                    $errors[] = (string) __('Row %1: Duplicate option value "%2" within the CSV (admin store).',
                        $rowNum, $value);
                }
                $adminValues[] = $value;

                $sortOrderVal = $row[self::COL_SORT_ORDER] ?? '';
                if (!is_numeric($sortOrderVal)) {
                    $errors[] = (string) __('Row %1: sort_order must be a number, got "%2".',
                        $rowNum, $sortOrderVal);
                } elseif ((int) $sortOrderVal < 0) {
                    $errors[] = (string) __('Row %1: sort_order must be 0 or greater, got "%2".',
                        $rowNum, $sortOrderVal);
                }

                $isDefaultVal = $row[self::COL_IS_DEFAULT] ?? '';
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
                    $swatchVal = $row[self::COL_SWATCH] ?? '';
                    if ($swatchVal === '') {
                        $errors[] = (string) __('Row %1: hex_code is required for visual swatch attributes.', $rowNum);
                    } elseif (!$this->isValidSwatchValue($swatchVal)) {
                        $errors[] = (string) __('Row %1: hex_code "%2" is not a valid hex colour (expected #RRGGBB).',
                            $rowNum, $swatchVal);
                    }
                }
            } else {
                if (!$hasAdminRow) {
                    $errors[] = (string) __('Row %1: store view row "%2" appears before any admin (default) row.',
                        $rowNum, $storeCode);
                }

                if ($storeCode !== '' && !$this->storeResolver->isValidStoreCode($storeCode)) {
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

    /**
     * @param string $code
     * @return bool
     */
    private function isAdminStoreCode(string $code): bool
    {
        return in_array(strtolower($code), StoreResolver::ADMIN_STORE_CODES, true);
    }

    /**
     * @param string $value
     * @return bool
     */
    private function isValidSwatchValue(string $value): bool
    {
        return (bool) preg_match('/^#[A-Fa-f0-9]{6}$/', trim($value));
    }
}
