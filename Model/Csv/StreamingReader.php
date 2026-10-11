<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Csv;

use Generator;
use Magento\Framework\Exception\FileSystemException;
use Magento\Framework\Exception\LocalizedException;
use Magento\Framework\Filesystem\Driver\File as FileDriver;

/**
 * Streams a CSV file row by row (header first), trimming every cell.
 */
class StreamingReader
{
    /**
     * Maximum number of data rows (header excluded)
     */
    public const MAX_ROWS = 10000;

    private const UTF8_BOM = "\xEF\xBB\xBF";

    /**
     * @param FileDriver $fileDriver
     * @param string $delimiter
     * @param string $enclosure
     * @param string $escape
     */
    public function __construct(
        private readonly FileDriver $fileDriver,
        private readonly string $delimiter = ',',
        private readonly string $enclosure = '"',
        private readonly string $escape = '\\'
    ) {
    }

    /**
     * Yield each non-empty row; the key is the zero-based line index (0 = header).
     *
     * @param string $filePath
     * @return Generator<int,string[]>
     * @throws FileSystemException
     * @throws LocalizedException
     */
    public function read(string $filePath): Generator
    {
        $handle = $this->fileDriver->fileOpen($filePath, 'r');

        try {
            $index = 0;
            while (($row = $this->fileDriver->fileGetCsv(
                $handle,
                0,
                $this->delimiter,
                $this->enclosure,
                $this->escape
            )) !== false) {
                if ($row === [null]) {
                    continue;
                }
                if ($index > self::MAX_ROWS) {
                    throw new LocalizedException(
                        __('The CSV file exceeds the maximum of %1 data rows.', self::MAX_ROWS)
                    );
                }
                if ($index === 0 && isset($row[0]) && str_starts_with($row[0], self::UTF8_BOM)) {
                    $row[0] = substr($row[0], strlen(self::UTF8_BOM));
                }

                yield $index++ => array_map(static fn ($cell): string => trim((string) $cell), $row);
            }
        } finally {
            $this->fileDriver->fileClose($handle);
        }
    }
}
