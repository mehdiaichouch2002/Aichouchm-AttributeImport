<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Api;

/**
 * Interface ImportServiceInterface
 */
interface ImportServiceInterface
{
    /**
     * @param string $filePath
     * @param string $attributeCode
     * @return array
     */
    public function validate(string $filePath, string $attributeCode): array;

    /**
     * @param string $filePath
     * @param string $attributeCode
     * @return array
     */
    public function import(string $filePath, string $attributeCode): array;
}
