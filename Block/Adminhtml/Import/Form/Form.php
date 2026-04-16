<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import\Form;

use Aichouchm\AttributeImport\Model\Import\Source\Attributes;
use Magento\Backend\Block\Template\Context;
use Magento\Backend\Block\Widget\Form\Generic;
use Magento\Framework\Data\FormFactory;
use Magento\Framework\Registry;

/**
 * Class Form
 */
class Form extends Generic
{
    /**
     * Source file field name
     */
    public const FIELD_NAME_SOURCE_FILE = 'import_file';

    /**
     * @param Context $context
     * @param Registry $registry
     * @param FormFactory $formFactory
     * @param Attributes $sourceAttributes
     * @param array $data
     */
    public function __construct(
        Context                     $context,
        Registry                    $registry,
        FormFactory                 $formFactory,
        private readonly Attributes $sourceAttributes,
        array $data = []
    ) {
        parent::__construct($context, $registry, $formFactory, $data);
    }

    /**
     * @return $this
     */
    protected function _prepareForm(): static
    {
        /** @var \Magento\Framework\Data\Form $form */
        $form = $this->_formFactory->create([
            'data' => [
                'id'      => 'attribute-import-form',
                'method'  => 'post',
                'enctype' => 'multipart/form-data',
            ],
        ]);

        $fieldset = $form->addFieldset('base_fieldset', [
            'legend' => __('Import Settings'),
            'class'  => 'fieldset-wide',
        ]);

        $fieldset->addField('attribute_code', 'select', [
            'name'     => 'attribute_code',
            'label'    => __('Select Attribute'),
            'title'    => __('Select Attribute'),
            'required' => true,
            'values'   => $this->sourceAttributes->toOptionArray(),
            'onchange' => 'attributeImport.onAttributeChange();',
            'note'     => __('Only user-defined select/multiselect attributes are listed.'),
        ]);

        $fieldset->addField(self::FIELD_NAME_SOURCE_FILE, 'file', [
            'id'       => 'import_file',
            'name'     => self::FIELD_NAME_SOURCE_FILE,
            'label'    => __('CSV File'),
            'title'    => __('CSV File'),
            'required' => true,
            'class'    => 'input-file',
            'onchange' => 'attributeImport.onFileChange();',
            'note'     => __('Accepted format: CSV with columns attribute_code, store_view, value, [swatch,] sort_order, is_default'),
        ]);

        $form->setUseContainer(true);
        $this->setForm($form);

        return parent::_prepareForm();
    }
}
