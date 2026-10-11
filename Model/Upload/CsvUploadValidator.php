<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Upload;

use finfo;
use Magento\Framework\App\RequestInterface;
use Magento\Framework\Exception\LocalizedException;
use Magento\Framework\Filesystem\Io\File as IoFile;

/**
 * Validates the uploaded CSV (presence, upload status, extension, size, content type).
 */
class CsvUploadValidator
{
    public const FIELD_NAME = 'import_file';

    public const MAX_FILE_SIZE = 10485760; // 10 MB

    private const ALLOWED_MIME_TYPES = ['text/plain', 'text/csv', 'application/csv'];

    /**
     * @param IoFile $ioFile
     */
    public function __construct(
        private readonly IoFile $ioFile
    ) {
    }

    /**
     * Return the temporary path of a valid uploaded CSV.
     *
     * @param RequestInterface $request
     * @return string
     * @throws LocalizedException
     */
    public function getValidatedPath(RequestInterface $request): string
    {
        $file = $request->getFiles(self::FIELD_NAME);

        if (!is_array($file) || empty($file['tmp_name']) || ($file['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) {
            throw new LocalizedException(__('Please upload a CSV file.'));
        }

        $pathInfo  = $this->ioFile->getPathInfo((string) ($file['name'] ?? ''));
        $extension = strtolower((string) ($pathInfo['extension'] ?? ''));
        if ($extension !== 'csv') {
            throw new LocalizedException(__('Only CSV files are allowed.'));
        }

        $size = (int) ($file['size'] ?? 0);
        if ($size <= 0 || $size > self::MAX_FILE_SIZE) {
            throw new LocalizedException(__('The file is empty or exceeds the 10 MB limit.'));
        }

        $mimeType = (new finfo(FILEINFO_MIME_TYPE))->file((string) $file['tmp_name']);
        if (!in_array($mimeType, self::ALLOWED_MIME_TYPES, true)) {
            throw new LocalizedException(__('Invalid file type. Only CSV files are accepted.'));
        }

        return (string) $file['tmp_name'];
    }
}
