<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml;

use Magento\Backend\Block\Template;
use Magento\Framework\App\Filesystem\DirectoryList;
use Magento\Framework\Filesystem;

/**
 * Class Log
 */
class Log extends Template
{
    /**
     * Path to the log file relative to var/
     */
    private const LOG_FILE = 'log/attribute_import.log';

    /**
     * Default number of log lines to display
     */
    private const DEFAULT_LINES = 200;

    /**
     * @param Template\Context $context
     * @param Filesystem $filesystem
     * @param array $data
     */
    public function __construct(
        Template\Context            $context,
        private readonly Filesystem $filesystem,
        array $data = []
    ) {
        parent::__construct($context, $data);
    }

    /**
     * @param int $limit
     * @return array
     */
    public function getLogLines(int $limit = self::DEFAULT_LINES): array
    {
        try {
            $varDir = $this->filesystem->getDirectoryRead(DirectoryList::VAR_DIR);

            if (!$varDir->isExist(self::LOG_FILE)) {
                return [];
            }

            $content = $varDir->readFile(self::LOG_FILE);
            $lines   = array_reverse(array_filter(explode("\n", $content)));

            return array_slice($lines, 0, $limit);
        } catch (\Throwable) {
            return [];
        }
    }

    /**
     * @return string
     */
    public function getLogUrl(): string
    {
        return $this->getUrl('attributeimport/import/log');
    }

    /**
     * @return string
     */
    public function getImportUrl(): string
    {
        return $this->getUrl('attributeimport/import/index');
    }
}
