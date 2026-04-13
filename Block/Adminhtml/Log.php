<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml;

use Magento\Backend\Block\Template;
use Magento\Framework\App\Filesystem\DirectoryList;
use Magento\Framework\Filesystem;

/**
 * Renders the last N lines of the attribute import log file.
 *
 * The log file path is injected via di.xml so it can be overridden without
 * touching the class. Default: var/log/attribute_import.log.
 */
class Log extends Template
{
    private const DEFAULT_LINES = 200;

    public function __construct(
        Template\Context             $context,
        private readonly Filesystem  $filesystem,
        private readonly string      $logFile = '/var/log/attribute_import.log',
        array $data = []
    ) {
        parent::__construct($context, $data);
    }

    /**
     * Returns the last $limit lines from the log file, newest first.
     *
     * @return string[]
     */
    public function getLogLines(int $limit = self::DEFAULT_LINES): array
    {
        try {
            $varDir  = $this->filesystem->getDirectoryRead(DirectoryList::VAR_DIR);
            // Strip leading slash and var/ prefix since we're already in VAR_DIR
            $relPath = ltrim(str_replace('/var/', '', $this->logFile), '/');

            if (!$varDir->isExist($relPath)) {
                return [];
            }

            $content = $varDir->readFile($relPath);
            $lines   = array_reverse(array_filter(explode("\n", $content)));

            return array_slice($lines, 0, $limit);
        } catch (\Throwable) {
            return [];
        }
    }

    public function getLogUrl(): string
    {
        return $this->getUrl('attributeimport/import/log');
    }

    public function getImportUrl(): string
    {
        return $this->getUrl('attributeimport/import/index');
    }
}
