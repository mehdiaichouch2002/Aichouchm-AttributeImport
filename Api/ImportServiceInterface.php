<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Api;

/**
 * Service contract for attribute option CSV import.
 *
 * Having an interface here enables:
 *  - Swapping implementations via di.xml preference (e.g. async version)
 *  - Mocking in tests without touching the real DB
 *  - Clear public API that doesn't expose internals
 */
interface ImportServiceInterface
{
    /**
     * Validate a CSV file without writing anything to the database.
     *
     * Returns:
     *   is_valid (bool)   — true when no blocking errors exist
     *   errors   (string[]) — list of human-readable error messages
     *   rows     (array)  — raw CSV rows (including header) for the preview table
     *
     * @param string $filePath Absolute path to the uploaded CSV file
     * @param string $attributeCode Target attribute code (e.g. "color")
     * @return array{is_valid: bool, errors: string[], rows: array}
     */
    public function validate(string $filePath, string $attributeCode): array;

    /**
     * Import attribute options from a CSV file.
     *
     * Skips (with a log warning) any option whose admin-store value already
     * exists in the database — it does NOT update existing options.
     *
     * Returns:
     *   success  (bool)
     *   messages (string[]) — one message per imported/skipped/error event
     *   imported (int)      — count of newly created options
     *   skipped  (int)      — count of options that already existed
     *
     * @param string $filePath Absolute path to the uploaded CSV file
     * @param string $attributeCode Target attribute code (e.g. "color")
     * @return array{success: bool, messages: string[], imported: int, skipped: int}
     */
    public function import(string $filePath, string $attributeCode): array;
}
