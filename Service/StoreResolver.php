<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Service;

use Magento\Framework\Exception\NoSuchEntityException;
use Magento\Store\Model\StoreManagerInterface;

class StoreResolver
{
    public function __construct(
        private readonly StoreManagerInterface $storeManager
    ) {}

    /**
     * @throws NoSuchEntityException
     */
    public function getStoreId(string $storeCode): int
    {
        if (in_array(strtolower($storeCode), ['admin', 'default', '0'], true)) {
            return 0;
        }
        return (int) $this->storeManager->getStore($storeCode)->getId();
    }

    public function getAllStoreCodes(): array
    {
        $codes = [];
        foreach ($this->storeManager->getStores() as $store) {
            $codes[] = $store->getCode();
        }
        return $codes;
    }

    public function isValidStoreCode(string $storeCode): bool
    {
        if (in_array(strtolower($storeCode), ['admin', 'default', '0'], true)) {
            return true;
        }
        return in_array($storeCode, $this->getAllStoreCodes(), true);
    }
}
