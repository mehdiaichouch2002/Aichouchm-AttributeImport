<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import;

use Magento\Backend\Block\Widget\Form\Container;

/**
 * Class Form
 */
class Form extends Container
{
    /**
     * @var string
     */
    protected $_mode = 'form';

    /**
     * @return void
     */
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

        $this->buttonList->add(
            'view-log-button',
            [
                'label'   => __('View Log'),
                'type'    => 'button',
                'class'   => 'action-default',
                'onclick' => 'setLocation(\'' . $this->getUrl('attributeimport/import/log') . '\')',
            ]
        );

        $this->_objectId   = 'import_ids';
        $this->_blockGroup = 'Aichouchm_AttributeImport';
        $this->_controller = 'adminhtml_import';
    }
}
