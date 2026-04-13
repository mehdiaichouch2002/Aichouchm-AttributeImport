<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Controller\Adminhtml\Import;

use Aichouchm\AttributeImport\Api\ImportServiceInterface;
use Exception;
use Magento\Backend\App\Action;
use Magento\Backend\App\Action\Context;
use Magento\Framework\App\Action\HttpPostActionInterface;
use Magento\Framework\Controller\Result\Json;
use Magento\Framework\Controller\Result\JsonFactory;
use Psr\Log\LoggerInterface;

/**
 * AJAX endpoint: execute the actual import and return a result summary.
 *
 * The "Import" button is disabled in the UI until "Check Data" passes, so by
 * the time this controller is called the CSV has already been validated.
 * The service re-validates internally before writing — defence in depth.
 */
class Process extends Action implements HttpPostActionInterface
{
    public const ADMIN_RESOURCE = 'Aichouchm_AttributeImport::import_attributes';

    public function __construct(
        Context                              $context,
        private readonly ImportServiceInterface $importService,
        private readonly JsonFactory         $resultJsonFactory,
        private readonly LoggerInterface     $logger  // injected as named virtual type via di.xml
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

            $importResult = $this->importService->import($filePath, $attributeCode);

            return $result->setData([
                'success'  => $importResult['success'],
                'messages' => $importResult['messages'],
                'imported' => $importResult['imported'],
                'skipped'  => $importResult['skipped'],
            ]);
        } catch (Exception $e) {
            $this->logger->error(sprintf('[%s] Controller error: %s', date('Y-m-d H:i:s'), $e->getMessage()));
            return $result->setData([
                'success'  => false,
                'messages' => [(string) __('An unexpected error occurred. See attribute_import.log for details.')],
                'imported' => 0,
                'skipped'  => 0,
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
}
