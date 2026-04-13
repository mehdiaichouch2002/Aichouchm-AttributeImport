<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Controller\Adminhtml\Import;

use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\View\Result\Page;
use Magento\Framework\View\Result\PageFactory;

class Index extends Action
{
    public const ADMIN_RESOURCE = 'Aichouchm_AttributeImport::import_attributes';

    public function __construct(
        Context                          $context,
        private readonly PageFactory     $resultPageFactory
    ) {
        parent::__construct($context);
    }

    public function execute(): Page
    {
        $resultPage = $this->resultPageFactory->create();
        $resultPage->setActiveMenu('Aichouchm_AttributeImport::import_attributes');
        $resultPage->getConfig()->getTitle()->prepend(__('Import Attribute Options'));
        return $resultPage;
    }
}
