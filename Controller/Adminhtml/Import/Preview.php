<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Controller\Adminhtml\Import;

use Aichouchm\AttributeImport\Api\ImportServiceInterface;
use Aichouchm\AttributeImport\Block\Adminhtml\Import\Preview as PreviewBlock;
use Exception;
use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\App\Action\HttpPostActionInterface;
use Magento\Framework\Controller\Result\Json;
use Magento\Framework\Controller\Result\JsonFactory;
use Magento\Framework\View\LayoutFactory;

class Preview extends Action implements HttpPostActionInterface
{
    public const ADMIN_RESOURCE = 'Aichouchm_AttributeImport::import_attributes';

    public function __construct(
        Context                              $context,
        private readonly JsonFactory         $resultJsonFactory,
        private readonly ImportServiceInterface $importService,
        private readonly LayoutFactory       $layoutFactory
    ) {
        parent::__construct($context);
    }

    public function execute(): Json
    {
        $result = $this->resultJsonFactory->create();

        try {
            $this->assertValidRequest();

            $attributeCode = $this->getRequest()->getParam('attribute_code');
            $filePath      = $this->getUploadedFilePath();

            $validation = $this->importService->validate($filePath, $attributeCode);
            $html       = $this->renderPreviewBlock($validation['rows'], $validation['errors']);

            return $result->setData([
                'success'  => true,
                'data'     => $html,
                'is_valid' => $validation['is_valid'],
            ]);
        } catch (Exception $e) {
            return $result->setData([
                'success' => false,
                'message' => $e->getMessage(),
            ]);
        }
    }

    private function assertValidRequest(): void
    {
        $files = $this->getRequest()->getFiles()->toArray();

        if (empty($files['import_file']['tmp_name'])) {
            throw new Exception((string) __('Please upload a CSV file.'));
        }
        if (strtolower(pathinfo($files['import_file']['name'], PATHINFO_EXTENSION)) !== 'csv') {
            throw new Exception((string) __('Only CSV files are allowed.'));
        }
        if (empty($this->getRequest()->getParam('attribute_code'))) {
            throw new Exception((string) __('Please select an attribute.'));
        }
    }

    private function getUploadedFilePath(): string
    {
        $files    = $this->getRequest()->getFiles()->toArray();
        $filePath = $files['import_file']['tmp_name'] ?? '';

        if (!is_readable($filePath)) {
            throw new Exception((string) __('Cannot read the uploaded file.'));
        }
        return $filePath;
    }

    private function renderPreviewBlock(array $rows, array $errors): string
    {
        return $this->layoutFactory->create()
            ->createBlock(PreviewBlock::class)
            ->setTemplate('Aichouchm_AttributeImport::import/preview.phtml')
            ->setData(compact('rows', 'errors'))
            ->toHtml();
    }
}
