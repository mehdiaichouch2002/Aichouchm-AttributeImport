<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Csv;

use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Catalog\Model\Product;
use Magento\Catalog\Model\ResourceModel\Eav\AttributeFactory;

/**
 * Stateless CSV validator: every method returns its result rather than storing
 * errors on the instance.
 *
 * WHY STATELESS:
 *   The reference module stores errors in a private $messageErrors array on the
 *   instance. Because Magento's DI container creates singletons by default, a
 *   second validation call in the same request would accumulate errors from the
 *   first call. Making every method return its findings avoids this entirely and
 *   makes the class trivially unit-testable.
 *
 * COLUMN LAYOUT:
 *   Plain select (5 columns):
 *     attribute_code | store_view | value | sort_order | is_default
 *
 *   Visual or text swatch (6 columns):
 *     attribute_code | store_view | value | swatch | sort_order | is_default
 *     (The spec names the 4th column "hex_code"; both names are accepted.)
 *
 * SWATCH TYPE CONSTANTS (match eav_attribute_option_swatch.type):
 *   SWATCH_NONE  (-1) → plain select, no swatch column
 *   SWATCH_TEXT  ( 0) → text swatch (styled label)
 *   SWATCH_VISUAL( 1) → visual swatch (hex colour or image URL)
 */
class Validator
{
    public const SWATCH_NONE   = -1;
    public const SWATCH_TEXT   =  0;
    public const SWATCH_VISUAL =  1;

    // Accepted names for the swatch column (position 3)
    private const SWATCH_COL_NAMES = ['swatch', 'hex_code', 'swatch_value', 'color'];

    public function __construct(
        private readonly StoreResolver    $storeResolver,
        private readonly AttributeFactory $attributeFactory
    ) {}

    // ── Public API ────────────────────────────────────────────────────────────

    /**
     * Detect the swatch type for a given attribute code.
     * Returns one of the SWATCH_* class constants.
     */
    public function getSwatchType(string $attributeCode): int
    {
        $attribute  = $this->attributeFactory->create()->loadByCode(Product::ENTITY, $attributeCode);
        $additional = json_decode($attribute->getAdditionalData() ?? '{}', true);

        return match ($additional['swatch_input_type'] ?? null) {
            'visual' => self::SWATCH_VISUAL,
            'text'   => self::SWATCH_TEXT,
            default  => self::SWATCH_NONE,
        };
    }

    /**
     * Validate the header row.
     * Returns an empty array on success, or error strings on failure.
     *
     * @param  string[] $headerRow Raw header cells from the CSV
     * @param  int      $swatchType One of the SWATCH_* constants
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

            // The swatch column accepts several aliases
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
     * Validate all data rows (header excluded — pass array_slice($rows, 1)).
     *
     * Validates:
     *  - Attribute code consistency
     *  - Required fields (attribute_code, store_view, value)
     *  - First row of each option group must be an admin/default store row
     *  - No duplicate admin values within the CSV
     *  - No duplicate store codes within the same option group
     *  - Store codes exist in Magento
     *  - sort_order is numeric (admin rows only)
     *  - is_default is 0 or 1 (admin rows only)
     *  - At most one is_default=1 across all options
     *
     * Returns empty array on success, error strings on failure.
     *
     * @param  array[]  $rows        Data rows (no header)
     * @param  string   $attributeCode
     * @param  int      $swatchType  One of the SWATCH_* constants
     * @return string[]
     */
    public function validateRows(array $rows, string $attributeCode, int $swatchType): array
    {
        $errors           = [];
        $adminValues      = [];    // admin-store values seen so far (duplicate detection)
        $optionStores     = [];    // store codes for the current option group
        $defaultSelected  = false;
        $expectAdminNext  = true;  // the very first row must be an admin row

        [$sortOrderCol, $isDefaultCol] = $this->dataColumnOffsets($swatchType);

        foreach ($rows as $index => $row) {
            $rowNum    = $index + 2;  // human-readable: +1 for 1-based, +1 for header
            $storeCode = trim($row[1] ?? '');
            $isAdmin   = $this->isAdminStoreCode($storeCode);

            // ── Required-field checks (all rows) ───────────────────────────
            foreach ([0 => 'attribute_code', 1 => 'store_view', 2 => 'value'] as $col => $name) {
                if (($row[$col] ?? '') === '') {
                    $errors[] = (string) __('Row %1: "%2" is required and cannot be empty.', $rowNum, $name);
                }
            }

            // ── Attribute code consistency ──────────────────────────────────
            if (($row[0] ?? '') !== $attributeCode) {
                $errors[] = (string) __('Row %1: attribute_code "%2" does not match selected attribute "%3".',
                    $rowNum, $row[0] ?? '', $attributeCode);
            }

            // ── Admin row rules ─────────────────────────────────────────────
            if ($isAdmin) {
                // Start of a new option group
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
                        $errors[] = (string) __('Row %1: is_default=1 is already set for another option. Only one option may be the default.', $rowNum);
                    }
                    $defaultSelected = true;
                }

                // Visual swatch: validate hex/URL format
                if ($swatchType === self::SWATCH_VISUAL) {
                    $swatchVal = $row[3] ?? '';
                    if (!$this->isValidSwatchValue($swatchVal)) {
                        $errors[] = (string) __('Row %1: swatch value "%2" is neither a valid hex color (#RRGGBB) nor an image URL.',
                            $rowNum, $swatchVal);
                    }
                }
            } else {
                // ── Non-admin store row ─────────────────────────────────────
                if ($expectAdminNext) {
                    $errors[] = (string) __('Row %1: First row must have store_view "admin" or "default". Got "%2".',
                        $rowNum, $storeCode);
                    $expectAdminNext = false; // report only once
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

    // ── Private helpers ───────────────────────────────────────────────────────

    /**
     * True when the store code string represents the admin/global store (store_id=0).
     */
    private function isAdminStoreCode(string $code): bool
    {
        return in_array(strtolower($code), ['admin', 'default', '0'], true);
    }

    /**
     * Returns [sortOrderColumnIndex, isDefaultColumnIndex] for the given swatch type.
     */
    private function dataColumnOffsets(int $swatchType): array
    {
        return $swatchType !== self::SWATCH_NONE
            ? [4, 5]  // swatch col at 3, sort_order at 4, is_default at 5
            : [3, 4]; // no swatch col, sort_order at 3, is_default at 4
    }

    /**
     * Returns the expected header array.
     * Arrays at a position mean "accept any of these names" (case-insensitive).
     */
    private function expectedHeaders(int $swatchType): array
    {
        $base = ['attribute_code', 'store_view', 'value'];
        if ($swatchType !== self::SWATCH_NONE) {
            return array_merge($base, [self::SWATCH_COL_NAMES, 'sort_order', 'is_default']);
        }
        return array_merge($base, ['sort_order', 'is_default']);
    }

    /**
     * Returns true for valid visual swatch values: hex colours or image URLs.
     */
    private function isValidSwatchValue(string $value): bool
    {
        $value = trim($value);

        // Hex colour
        if (preg_match('/^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$/', $value)) {
            return true;
        }

        // Image URL (absolute or root-relative)
        if (preg_match('/^(https?:\/\/|\/\/|\/|\.\/).*\.(jpg|jpeg|png|gif|svg|webp)$/i', $value)) {
            return true;
        }

        return false;
    }
}
