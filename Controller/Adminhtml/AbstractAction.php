<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Controller\Adminhtml;

use Exception;
use finfo;
use Magento\Backend\App\Action;

/**
 * Base admin controller
 */
abstract class AbstractAction extends Action
{
    /**
     * Authorization resource
     */
    public const ADMIN_RESOURCE = 'Aichouchm_AttributeImport::import_attributes';

    private const MAX_FILE_SIZE  = 10485760; // 10 MB
    private const ALLOWED_MIMES  = ['text/plain', 'text/csv'];

    /**
     * @return void
     * @throws Exception
     */
    protected function assertValidRequest(): void
    {
        $files = $this->getRequest()->getFiles()->toArray();

        if (empty($files['import_file']['tmp_name'])) {
            throw new Exception((string) __('Please upload a CSV file.'));
        }
        if (strtolower(pathinfo($files['import_file']['name'], PATHINFO_EXTENSION)) !== 'csv') {
            throw new Exception((string) __('Only CSV files are allowed.'));
        }

        $tmpPath  = $files['import_file']['tmp_name'];
        $realSize = filesize($tmpPath);

        if ($realSize === false || $realSize > self::MAX_FILE_SIZE) {
            throw new Exception((string) __('File size exceeds the 10 MB limit.'));
        }

        $mimeType = (new finfo(FILEINFO_MIME_TYPE))->file($tmpPath);
        if (!in_array($mimeType, self::ALLOWED_MIMES, true)) {
            throw new Exception((string) __('Invalid file type. Only CSV files are accepted.'));
        }

        if (empty($this->getRequest()->getParam('attribute_code'))) {
            throw new Exception((string) __('Please select an attribute.'));
        }
    }

    /**
     * @return string
     * @throws Exception
     */
    protected function getUploadedFilePath(): string
    {
        $files    = $this->getRequest()->getFiles()->toArray();
        $filePath = $files['import_file']['tmp_name'] ?? '';

        if (!is_readable($filePath)) {
            throw new Exception((string) __('Cannot read the uploaded file.'));
        }
        return $filePath;
    }
}
