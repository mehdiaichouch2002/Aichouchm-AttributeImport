<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import;

use Magento\Backend\Block\Widget\Form\Container;

/**
 * Page container with the Check Data / View Log / Import buttons.
 *
 * Buttons carry no inline handlers (CSP); Aichouchm_AttributeImport/js/attribute-import binds them.
 */
class Form extends Container
{
    /**
     * @var string
     */
    protected $_mode = 'form';

    /**
     * @inheritdoc
     */
    protected function _construct(): void
    {
        $this->_objectId   = 'import_ids';
        $this->_blockGroup = 'Aichouchm_AttributeImport';
        $this->_controller = 'adminhtml_import';

        parent::_construct();

        $this->buttonList->remove('back');
        $this->buttonList->remove('reset');
        $this->buttonList->remove('save');

        $this->buttonList->add('check-data-button', [
            'label' => __('Check Data'),
            'id'    => 'check-data-button',
            'class' => 'action-default',
        ], 0, 10);

        $this->buttonList->add('view-log-button', [
            'label' => __('View Log'),
            'id'    => 'view-log-button',
            'class' => 'action-default',
        ], 0, 20);

        $this->buttonList->add('import-button', [
            'label'    => __('Import'),
            'id'       => 'import-button',
            'class'    => 'primary',
            'disabled' => true,
        ], 0, 30);
    }
}
