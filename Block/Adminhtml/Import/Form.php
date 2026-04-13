<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import;

use Magento\Backend\Block\Widget\Form\Container;

/**
 * Container block for the import form.
 *
 * Manages the toolbar buttons: removes the default Back/Reset buttons
 * and replaces Save with Import (disabled until "Check Data" passes).
 * A secondary "Check Data" button triggers the AJAX preview flow.
 */
class Form extends Container
{
    protected $_mode = 'form';

    protected function _construct(): void
    {
        parent::_construct();

        $this->buttonList->remove('back');
        $this->buttonList->remove('reset');

        $this->buttonList->update('save', 'label', __('Import'));
        $this->buttonList->update('save', 'id', 'import-button');
        $this->buttonList->update('save', 'class', 'primary disabled');
        $this->buttonList->update('save', 'onclick', 'attributeImport.submit()');

        $this->buttonList->add(
            'check-data-button',
            [
                'label'   => __('Check Data'),
                'type'    => 'button',
                'id'      => 'check-data-button',
                'class'   => 'action-default',
                'onclick' => 'attributeImport.checkData();',
            ]
        );

        $this->_objectId  = 'import_ids';
        $this->_blockGroup = 'Aichouchm_AttributeImport';
        $this->_controller = 'adminhtml_import';
    }
}
