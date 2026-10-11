<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Controller\Adminhtml\Import;

use Aichouchm\AttributeImport\Api\ImportServiceInterface;
use Aichouchm\AttributeImport\Controller\Adminhtml\AbstractAction;
use Aichouchm\AttributeImport\Model\Upload\CsvUploadValidator;
use Magento\Backend\App\Action\Context;
use Magento\Framework\App\Action\HttpPostActionInterface;
use Magento\Framework\Controller\Result\Json;
use Magento\Framework\Controller\Result\JsonFactory;
use Magento\Framework\Exception\LocalizedException;
use Psr\Log\LoggerInterface;
use Throwable;

/**
 * "Import": validate again, then create the new options.
 */
class Process extends AbstractAction implements HttpPostActionInterface
{
    /**
     * @param Context $context
     * @param ImportServiceInterface $importService
     * @param JsonFactory $resultJsonFactory
     * @param CsvUploadValidator $uploadValidator
     * @param LoggerInterface $logger
     */
    public function __construct(
        Context $context,
        private readonly ImportServiceInterface $importService,
        private readonly JsonFactory $resultJsonFactory,
        private readonly CsvUploadValidator $uploadValidator,
        private readonly LoggerInterface $logger
    ) {
        parent::__construct($context);
    }

    /**
     * @inheritdoc
     */
    public function execute(): Json
    {
        $result = $this->resultJsonFactory->create();

        try {
            $filePath = $this->uploadValidator->getValidatedPath($this->getRequest());

            return $result->setData($this->importService->import(
                $filePath,
                (string) $this->getRequest()->getParam('attribute_code', '')
            ));
        } catch (LocalizedException $e) {
            return $result->setData($this->failure($e->getMessage()));
        } catch (Throwable $e) {
            $this->logger->error(sprintf('Import request failed unexpectedly: %s', $e));
            return $result->setData(
                $this->failure((string) __('An unexpected error occurred. See attribute_import.log for details.'))
            );
        }
    }

    /**
     * Failure payload in the same shape as a successful import result.
     *
     * @param string $message
     * @return array{success:false,messages:string[],imported:int,skipped:int}
     */
    private function failure(string $message): array
    {
        return ['success' => false, 'messages' => [$message], 'imported' => 0, 'skipped' => 0];
    }
}
