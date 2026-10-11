<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Service;

use Magento\Framework\Exception\LocalizedException;
use Magento\Store\Model\Store;
use Magento\Store\Model\StoreManagerInterface;

/**
 * Maps CSV store_view codes to store IDs ("default"/"admin" = global label, store 0).
 */
class StoreResolver
{
    public const ADMIN_STORE_CODES = ['admin', 'default'];

    /**
     * @var array<string,int>|null Lower-cased store code => store ID
     */
    private ?array $storeIds = null;

    /**
     * @param StoreManagerInterface $storeManager
     */
    public function __construct(
        private readonly StoreManagerInterface $storeManager
    ) {
    }

    /**
     * Whether the code designates the global (admin) label.
     *
     * @param string $storeCode
     * @return bool
     */
    public function isAdminStoreCode(string $storeCode): bool
    {
        return in_array(strtolower($storeCode), self::ADMIN_STORE_CODES, true);
    }

    /**
     * Whether the code is the admin alias or an existing store view.
     *
     * @param string $storeCode
     * @return bool
     */
    public function isValidStoreCode(string $storeCode): bool
    {
        return $this->isAdminStoreCode($storeCode)
            || array_key_exists(strtolower($storeCode), $this->getStoreIds());
    }

    /**
     * Resolve a store code to its ID.
     *
     * @param string $storeCode
     * @return int
     * @throws LocalizedException
     */
    public function getStoreId(string $storeCode): int
    {
        if ($this->isAdminStoreCode($storeCode)) {
            return Store::DEFAULT_STORE_ID;
        }

        $storeIds = $this->getStoreIds();
        $code     = strtolower($storeCode);

        if (!array_key_exists($code, $storeIds)) {
            throw new LocalizedException(__('Store view "%1" does not exist in Magento.', $storeCode));
        }

        return $storeIds[$code];
    }

    /**
     * Store views are loaded once per request.
     *
     * @return array<string,int>
     */
    private function getStoreIds(): array
    {
        if ($this->storeIds === null) {
            $this->storeIds = [];
            foreach ($this->storeManager->getStores() as $store) {
                $this->storeIds[strtolower((string) $store->getCode())] = (int) $store->getId();
            }
        }

        return $this->storeIds;
    }
}
