<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Controller\Adminhtml\Import;

use Aichouchm\AttributeImport\Api\ImportServiceInterface;
use Aichouchm\AttributeImport\Block\Adminhtml\Import\Preview as PreviewBlock;
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
 * "Check Data": validate the uploaded CSV and return the preview table.
 */
class Preview extends AbstractAction implements HttpPostActionInterface
{
    /**
     * @param Context $context
     * @param JsonFactory $resultJsonFactory
     * @param ImportServiceInterface $importService
     * @param CsvUploadValidator $uploadValidator
     * @param LoggerInterface $logger
     */
    public function __construct(
        Context $context,
        private readonly JsonFactory $resultJsonFactory,
        private readonly ImportServiceInterface $importService,
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
            $filePath   = $this->uploadValidator->getValidatedPath($this->getRequest());
            $validation = $this->importService->validate(
                $filePath,
                (string) $this->getRequest()->getParam('attribute_code', '')
            );

            return $result->setData([
                'success'  => true,
                'data'     => $this->renderPreview($validation['rows'], $validation['errors']),
                'is_valid' => $validation['is_valid'],
            ]);
        } catch (LocalizedException $e) {
            return $result->setData(['success' => false, 'message' => $e->getMessage()]);
        } catch (Throwable $e) {
            $this->logger->error(sprintf('Preview failed unexpectedly: %s', $e));
            return $result->setData([
                'success' => false,
                'message' => (string) __('An unexpected error occurred. See attribute_import.log for details.'),
            ]);
        }
    }

    /**
     * Render the preview table HTML.
     *
     * @param array<int,string[]> $rows
     * @param string[] $errors
     * @return string
     */
    private function renderPreview(array $rows, array $errors): string
    {
        return $this->_view->getLayout()
            ->createBlock(PreviewBlock::class)
            ->setTemplate('Aichouchm_AttributeImport::import/preview.phtml')
            ->setData(['rows' => $rows, 'errors' => $errors])
            ->toHtml();
    }
}
