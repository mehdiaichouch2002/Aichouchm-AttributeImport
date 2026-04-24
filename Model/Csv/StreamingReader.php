<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Csv;

use Generator;
use OverflowException;
use RuntimeException;

/**
 * Class StreamingReader
 */
class StreamingReader
{
    private const MAX_ROWS = 10000;

    /**
     * @param string $delimiter
     * @param string $enclosure
     * @param string $escape
     */
    public function __construct(
        private readonly string $delimiter = ',',
        private readonly string $enclosure = '"',
        private readonly string $escape    = '\\'
    ) {}

    /**
     * @param string $filePath
     * @return Generator
     */
    public function read(string $filePath): Generator
    {
        $handle = @fopen($filePath, 'r');
        if ($handle === false) {
            throw new RuntimeException(
                (string) __('Cannot open CSV file: %1', $filePath)
            );
        }

        try {
            $lineNumber = 0;
            while (($row = fgetcsv($handle, 0, $this->delimiter, $this->enclosure, $this->escape)) !== false) {
                if ($lineNumber > self::MAX_ROWS) {
                    throw new OverflowException(
                        (string) __('CSV exceeds the maximum allowed %1 rows.', self::MAX_ROWS)
                    );
                }
                yield $lineNumber => array_map('trim', $row);
                $lineNumber++;
            }
        } finally {
            fclose($handle);
        }
    }
}
