<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Import\Source;

use Aichouchm\AttributeImport\Model\Attribute\AttributeGuard;
use Magento\Catalog\Model\Product;
use Magento\Eav\Api\AttributeRepositoryInterface;
use Magento\Framework\Api\SearchCriteriaBuilder;
use Magento\Framework\Data\OptionSourceInterface;

/**
 * Attribute selector options: user-defined select/multiselect product attributes.
 */
class Attributes implements OptionSourceInterface
{
    /**
     * @var array<int,array{value:string,label:mixed}>|null
     */
    private ?array $options = null;

    /**
     * @param AttributeRepositoryInterface $attributeRepository
     * @param SearchCriteriaBuilder $searchCriteriaBuilder
     */
    public function __construct(
        private readonly AttributeRepositoryInterface $attributeRepository,
        private readonly SearchCriteriaBuilder $searchCriteriaBuilder
    ) {
    }

    /**
     * Build the option list once per request.
     *
     * @return array<int,array{value:string,label:mixed}>
     */
    public function toOptionArray(): array
    {
        if ($this->options !== null) {
            return $this->options;
        }

        $this->options = [['value' => '', 'label' => __('-- Please Select --')]];

        $searchCriteria = $this->searchCriteriaBuilder
            ->addFilter('frontend_input', AttributeGuard::ALLOWED_FRONTEND_INPUTS, 'in')
            ->addFilter('is_user_defined', 1)
            ->create();

        $items = $this->attributeRepository->getList(Product::ENTITY, $searchCriteria)->getItems();

        foreach ($items as $attribute) {
            $this->options[] = [
                'value' => $attribute->getAttributeCode(),
                'label' => sprintf(
                    '%s [%s]',
                    $attribute->getDefaultFrontendLabel() ?? $attribute->getAttributeCode(),
                    $attribute->getAttributeCode()
                ),
            ];
        }

        return $this->options;
    }
}
