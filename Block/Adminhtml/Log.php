<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml;

use Magento\Backend\Block\Template;
use Magento\Framework\App\Filesystem\DirectoryList;
use Magento\Framework\Filesystem;
use Psr\Log\LoggerInterface;
use Throwable;

/**
 * Shows the newest entries of var/log/attribute_import.log.
 */
class Log extends Template
{
    private const LOG_FILE = 'log/attribute_import.log';

    private const DEFAULT_LINES = 300;

    /**
     * Only the end of the file is read, so a large log never exhausts memory.
     */
    private const MAX_BYTES = 262144; // 256 KB

    private const LEVEL_CLASSES = [
        '.ERROR'   => 'log-line-error',
        '.WARNING' => 'log-line-warning',
        '.INFO'    => 'log-line-info',
    ];

    /**
     * @param Template\Context $context
     * @param Filesystem $filesystem
     * @param LoggerInterface $logger
     * @param array $data
     */
    public function __construct(
        Template\Context $context,
        private readonly Filesystem $filesystem,
        private readonly LoggerInterface $logger,
        array $data = []
    ) {
        parent::__construct($context, $data);
    }

    /**
     * Newest log lines first.
     *
     * @param int $limit
     * @return string[]
     */
    public function getLogLines(int $limit = self::DEFAULT_LINES): array
    {
        try {
            $varDir = $this->filesystem->getDirectoryRead(DirectoryList::VAR_DIR);
            if (!$varDir->isFile(self::LOG_FILE)) {
                return [];
            }

            $size   = (int) ($varDir->stat(self::LOG_FILE)['size'] ?? 0);
            $offset = max(0, $size - self::MAX_BYTES);

            $file = $varDir->openFile(self::LOG_FILE);
            try {
                $file->seek($offset);
                $content = (string) $file->read(self::MAX_BYTES);
            } finally {
                $file->close();
            }

            $lines = explode("\n", $content);
            if ($offset > 0) {
                array_shift($lines); // first line is cut mid-way
            }
            $lines = array_values(array_filter(array_map('trim', $lines), static fn (string $l): bool => $l !== ''));

            return array_slice(array_reverse($lines), 0, $limit);
        } catch (Throwable $e) {
            $this->logger->warning(sprintf('Attribute import log could not be read: %s', $e->getMessage()));
            return [];
        }
    }

    /**
     * CSS class for a log line based on its level.
     *
     * @param string $line
     * @return string
     */
    public function getLineClass(string $line): string
    {
        foreach (self::LEVEL_CLASSES as $needle => $class) {
            if (str_contains($line, $needle)) {
                return $class;
            }
        }

        return 'log-line';
    }

    /**
     * URL of the import page ("Back to Import").
     *
     * @return string
     */
    public function getImportUrl(): string
    {
        return $this->getUrl('attributeimport/import/index');
    }
}
