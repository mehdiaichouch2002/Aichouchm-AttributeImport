<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Service;

use Magento\Store\Model\StoreManagerInterface;

/**
 * Class StoreResolver
 */
class StoreResolver
{
    /**
     * @var string[]
     */
    private array $storeCodes = [];

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
     * @return string[]
     */
    public function getAllStoreCodes(): array
    {
        if (!empty($this->storeCodes)) {
            return $this->storeCodes;
        }
        foreach ($this->storeManager->getStores() as $store) {
            $this->storeCodes[] = $store->getCode();
        }
        return $this->storeCodes;
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
