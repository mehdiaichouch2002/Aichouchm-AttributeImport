<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Service;

use Magento\Framework\Exception\NoSuchEntityException;
use Magento\Store\Model\StoreManagerInterface;

/**
 * Class StoreResolver
 */
class StoreResolver
{
    /**
     * @param StoreManagerInterface $storeManager
     */
    public function __construct(
        private readonly StoreManagerInterface $storeManager
    ) {}

    /**
     * @param string $storeCode
     * @return int
     */
    public function getStoreId(string $storeCode): int
    {
        if (in_array(strtolower($storeCode), ['admin', 'default'], true)) {
            return 0;
        }
        return (int) $this->storeManager->getStore($storeCode)->getId();
    }

    /**
     * @return array
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
     * @param string $storeCode
     * @return bool
     */
    public function isValidStoreCode(string $storeCode): bool
    {
        if (in_array(strtolower($storeCode), ['admin', 'default'], true)) {
            return true;
        }
        return in_array($storeCode, $this->getAllStoreCodes(), true);
    }
}
