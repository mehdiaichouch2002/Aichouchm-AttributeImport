<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Csv;

use Generator;
use RuntimeException;

/**
 * Class StreamingReader
 */
class StreamingReader
{
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

        // Strip UTF-8 BOM so Excel-exported files work without header validation failures
        $bom = fread($handle, 3);
        if ($bom !== "\xEF\xBB\xBF") {
            rewind($handle);
        }

        try {
            $lineNumber = 0;
            while (($row = fgetcsv($handle, 0, $this->delimiter, $this->enclosure, $this->escape)) !== false) {
                yield $lineNumber => array_map('trim', $row);
                $lineNumber++;
            }
        } finally {
            fclose($handle);
        }
    }

    /**
     * @param string $filePath
     * @return array
     */
    public function readHeader(string $filePath): array
    {
        foreach ($this->read($filePath) as $row) {
            return $row;
        }
        return [];
    }
}
