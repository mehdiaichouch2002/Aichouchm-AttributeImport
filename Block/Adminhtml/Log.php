<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml;

use Magento\Backend\Block\Template;
use Magento\Framework\App\Filesystem\DirectoryList;
use Magento\Framework\Filesystem;

class Log extends Template
{
    private const LOG_FILE      = 'log/attribute_import.log';
    private const DEFAULT_LINES = 200;

    public function __construct(
        Template\Context             $context,
        private readonly Filesystem  $filesystem,
        array $data = []
    ) {
        parent::__construct($context, $data);
    }

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

    public function getLogUrl(): string
    {
        return $this->getUrl('attributeimport/import/log');
    }

    public function getImportUrl(): string
    {
        return $this->getUrl('attributeimport/import/index');
    }
}
