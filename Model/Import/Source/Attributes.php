<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Import\Source;

use Magento\Eav\Api\AttributeRepositoryInterface;
use Magento\Framework\Api\SearchCriteriaBuilder;
use Magento\Framework\Option\ArrayInterface;

/**
 * Class Attributes
 */
class Attributes implements ArrayInterface
{
    /**
     * @var array|null
     */
    private ?array $options = null;

    /**
     * @param AttributeRepositoryInterface $attributeRepository
     * @param SearchCriteriaBuilder $searchCriteriaBuilder
     */
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
