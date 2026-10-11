<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import\Form;

use Aichouchm\AttributeImport\Model\Import\Source\Attributes;
use Aichouchm\AttributeImport\Model\Upload\CsvUploadValidator;
use Magento\Backend\Block\Template\Context;
use Magento\Backend\Block\Widget\Form\Generic;
use Magento\Framework\Data\Form as DataForm;
use Magento\Framework\Data\FormFactory;
use Magento\Framework\Exception\LocalizedException;
use Magento\Framework\Registry;

/**
 * Import settings form: attribute selector and CSV upload.
 */
class Form extends Generic
{
    public const FIELD_NAME_SOURCE_FILE = CsvUploadValidator::FIELD_NAME;

    /**
     * @param Context $context
     * @param Registry $registry
     * @param FormFactory $formFactory
     * @param Attributes $sourceAttributes
     * @param array $data
     */
    public function __construct(
        Context $context,
        Registry $registry,
        FormFactory $formFactory,
        private readonly Attributes $sourceAttributes,
        array $data = []
    ) {
        parent::__construct($context, $registry, $formFactory, $data);
    }

    /**
     * Build the form; change handlers are bound by the JS component, not inline.
     *
     * @return $this
     * @throws LocalizedException
     */
    protected function _prepareForm(): static
    {
        /** @var DataForm $form */
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
            'note'     => __('Only user-defined select/multiselect attributes are listed.'),
        ]);

        $fieldset->addField(self::FIELD_NAME_SOURCE_FILE, 'file', [
            'name'     => self::FIELD_NAME_SOURCE_FILE,
            'label'    => __('CSV File'),
            'title'    => __('CSV File'),
            'required' => true,
            'class'    => 'input-file',
            'note'     => __('Columns: attribute_code, store_view, value, hex_code, sort_order, is_default'),
        ]);

        $form->setUseContainer(true);
        $this->setForm($form);

        return parent::_prepareForm();
    }
}
