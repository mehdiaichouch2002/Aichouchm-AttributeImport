<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Controller\Adminhtml\Import;

use Aichouchm\AttributeImport\Api\ImportServiceInterface;
use Aichouchm\AttributeImport\Controller\Adminhtml\AbstractAction;
use Exception;
use Magento\Backend\App\Action\Context;
use Magento\Framework\App\Action\HttpPostActionInterface;
use Magento\Framework\Controller\Result\Json;
use Magento\Framework\Controller\Result\JsonFactory;
use Psr\Log\LoggerInterface;

/**
 * Controller Class Process
 */
class Process extends AbstractAction implements HttpPostActionInterface
{
    /**
     * @param Context $context
     * @param ImportServiceInterface $importService
     * @param JsonFactory $resultJsonFactory
     * @param LoggerInterface $logger
     */
    public function __construct(
        Context                                 $context,
        private readonly ImportServiceInterface $importService,
        private readonly JsonFactory            $resultJsonFactory,
        private readonly LoggerInterface        $logger
    ) {
        parent::__construct($context);
    }

    /**
     * @return Json
     */
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
            $this->logger->error(sprintf('Controller error: %s', $e->getMessage()));
            return $result->setData([
                'success'  => false,
                'messages' => [(string) __('An unexpected error occurred. See attribute_import.log for details.')],
                'imported' => 0,
                'skipped'  => 0,
            ]);
        }
    }
}
