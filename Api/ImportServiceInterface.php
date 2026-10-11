<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Api;

/**
 * Validate and import product attribute options from a CSV file.
 *
 * @api
 */
interface ImportServiceInterface
{
    /**
     * Validate the file without writing anything.
     *
     * @param string $filePath
     * @param string $attributeCode
     * @return array{is_valid:bool,errors:string[],rows:array<int,string[]>,swatch_type:int}
     */
    public function validate(string $filePath, string $attributeCode): array;

    /**
     * Validate, then create the options that do not exist yet.
     *
     * @param string $filePath
     * @param string $attributeCode
     * @return array{success:bool,messages:string[],imported:int,skipped:int}
     */
    public function import(string $filePath, string $attributeCode): array;
}
