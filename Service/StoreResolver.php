<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Service;

use Magento\Framework\Exception\NoSuchEntityException;
use Magento\Store\Model\StoreManagerInterface;

/**
 * Resolves a store_view column value from the CSV to a Magento store_id integer.
 *
 * WHY A DEDICATED SERVICE (not a Helper):
 *   Helpers in Magento are a legacy pattern. A plain service class with
 *   constructor injection is testable, focused, and follows PSR principles.
 *
 * STORE CODE CONVENTION:
 *   Both "admin" and "default" (case-insensitive) resolve to store_id=0,
 *   which is Magento's "admin" store — the global, store-agnostic label.
 *
 *   WHY map "default" to 0?
 *   The spec CSV uses "default" to mean the base/global value. Magento's
 *   native import/export tool uses "admin" for the same concept. Supporting
 *   both spellings prevents confusing validation errors for users following
 *   the spec format.
 */
class StoreResolver
{
    public function __construct(
        private readonly StoreManagerInterface $storeManager
    ) {}

    /**
     * Resolves a CSV store_view value to a numeric Magento store_id.
     *
     * @throws NoSuchEntityException If the store code doesn't exist
     */
    public function getStoreId(string $storeCode): int
    {
        if (in_array(strtolower($storeCode), ['admin', 'default', '0'], true)) {
            return 0;
        }
        return (int) $this->storeManager->getStore($storeCode)->getId();
    }

    /**
     * Returns all store codes known to Magento (excluding admin store).
     * Used by the Validator to verify that store codes in the CSV exist.
     */
    public function getAllStoreCodes(): array
    {
        $codes = [];
        foreach ($this->storeManager->getStores() as $store) {
            $codes[] = $store->getCode();
        }
        return $codes;
    }

    /**
     * Returns true when the store code exists in Magento or is a reserved alias.
     */
    public function isValidStoreCode(string $storeCode): bool
    {
        if (in_array(strtolower($storeCode), ['admin', 'default', '0'], true)) {
            return true;
        }
        return in_array($storeCode, $this->getAllStoreCodes(), true);
    }
}
