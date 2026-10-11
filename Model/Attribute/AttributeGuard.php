<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Attribute;

use Magento\Catalog\Model\Product;
use Magento\Eav\Model\Config as EavConfig;
use Magento\Eav\Model\Entity\Attribute\AbstractAttribute;
use Magento\Framework\Exception\LocalizedException;

/**
 * Single source of truth for which product attributes may receive imported options.
 *
 * The admin dropdown only lists allowed attributes, but the attribute code arrives
 * in a POST parameter, so every request must be re-checked on the server.
 */
class AttributeGuard
{
    /**
     * Frontend input types that own a list of options
     */
    public const ALLOWED_FRONTEND_INPUTS = ['select', 'multiselect'];

    /**
     * @param EavConfig $eavConfig
     */
    public function __construct(
        private readonly EavConfig $eavConfig
    ) {
    }

    /**
     * Load the attribute and assert options may be imported into it.
     *
     * @param string $attributeCode
     * @return AbstractAttribute
     * @throws LocalizedException
     */
    public function getImportableAttribute(string $attributeCode): AbstractAttribute
    {
        $attribute = $attributeCode === ''
            ? null
            : $this->eavConfig->getAttribute(Product::ENTITY, $attributeCode);

        if ($attribute === null || !$attribute->getAttributeId()) {
            throw new LocalizedException(__('Attribute "%1" does not exist.', $attributeCode));
        }

        if (!$this->isImportable($attribute)) {
            throw new LocalizedException(
                __('Attribute "%1" is not a user-defined select or multiselect attribute.', $attributeCode)
            );
        }

        return $attribute;
    }

    /**
     * Whether the attribute is a user-defined option attribute.
     *
     * @param AbstractAttribute $attribute
     * @return bool
     */
    public function isImportable(AbstractAttribute $attribute): bool
    {
        return (bool) $attribute->getIsUserDefined()
            && in_array($attribute->getFrontendInput(), self::ALLOWED_FRONTEND_INPUTS, true);
    }
}
