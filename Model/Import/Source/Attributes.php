<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Import\Source;

use Magento\Eav\Api\AttributeRepositoryInterface;
use Magento\Framework\Api\SearchCriteriaBuilder;
use Magento\Framework\Option\ArrayInterface;

/**
 * Source model for the attribute selector dropdown on the import form.
 *
 * Lists only user-defined select/multiselect attributes — system attributes
 * like "status", "visibility", "tax_class_id" are excluded because modifying
 * their options can break core Magento functionality.
 *
 * WHY NOT return system attributes:
 *   System attributes (is_user_defined = 0) are configured by core code. Their
 *   option_ids are hardcoded in installers. Importing new values could cause
 *   mismatches between DB values and the expected constants in PHP.
 */
class Attributes implements ArrayInterface
{
    private ?array $options = null;

    public function __construct(
        private readonly AttributeRepositoryInterface $attributeRepository,
        private readonly SearchCriteriaBuilder        $searchCriteriaBuilder
    ) {}

    /**
     * {@inheritdoc}
     */
    public function toOptionArray(): array
    {
        if ($this->options !== null) {
            return $this->options;
        }

        $this->options = [['value' => '', 'label' => __('-- Please Select --')]];

        $searchCriteria = $this->searchCriteriaBuilder->create();
        $items          = $this->attributeRepository
            ->getList('catalog_product', $searchCriteria)
            ->getItems();

        foreach ($items as $attribute) {
            if (
                $attribute->getIsUserDefined()
                && in_array($attribute->getFrontendInput(), ['select', 'multiselect'], true)
            ) {
                $this->options[] = [
                    'value' => $attribute->getAttributeCode(),
                    'label' => sprintf(
                        '%s [%s]',
                        $attribute->getDefaultFrontendLabel() ?? $attribute->getAttributeCode(),
                        $attribute->getAttributeCode()
                    ),
                ];
            }
        }

        return $this->options;
    }
}
