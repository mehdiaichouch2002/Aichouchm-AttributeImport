<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Api;

interface ImportServiceInterface
{
    /**
     * Validate a CSV file without writing to the database.
     *
     * @return array{is_valid: bool, errors: string[], rows: array}
     */
    public function validate(string $filePath, string $attributeCode): array;

    /**
     * Import attribute options from a CSV file.
     * Options that already exist in the database are skipped (not overwritten).
     *
     * @return array{success: bool, messages: string[], imported: int, skipped: int}
     */
    public function import(string $filePath, string $attributeCode): array;
}
