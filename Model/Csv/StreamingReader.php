<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model\Csv;

use Generator;
use RuntimeException;

/**
 * Streams a CSV file one row at a time via fgetcsv.
 *
 * WHY NOT Magento\Framework\File\Csv::getData():
 *   getData() calls file() internally, which loads the ENTIRE file into a PHP
 *   array before returning it. A 50 MB CSV with 50k rows → 50 MB in RAM just
 *   for reading. With a 256 M PHP memory limit, three concurrent admin imports
 *   could OOM the process.
 *
 *   This reader is a PHP Generator: it yields one array per row and never
 *   holds more than one row in memory at a time. Memory stays constant at
 *   O(1) regardless of file size.
 *
 * UTF-8 BOM:
 *   Excel always prepends a 3-byte BOM (\xEF\xBB\xBF) when saving as "CSV UTF-8".
 *   Without stripping it, the first column header becomes "\xEF\xBB\xBFattribute_code"
 *   which fails header validation. The reader detects and skips the BOM automatically.
 */
class StreamingReader
{
    public function __construct(
        private readonly string $delimiter = ',',
        private readonly string $enclosure = '"',
        private readonly string $escape    = '\\'
    ) {}

    /**
     * Opens the file and yields one row array per line.
     *
     * Line numbers are 0-based (line 0 = header row).
     *
     * @return Generator<int, string[]>
     * @throws RuntimeException When the file cannot be opened
     */
    public function read(string $filePath): Generator
    {
        $handle = @fopen($filePath, 'r');
        if ($handle === false) {
            throw new RuntimeException(
                (string) __('Cannot open CSV file: %1', $filePath)
            );
        }

        // Strip UTF-8 BOM silently so Excel-exported files work out of the box
        $bom = fread($handle, 3);
        if ($bom !== "\xEF\xBB\xBF") {
            rewind($handle);
        }

        try {
            $lineNumber = 0;
            while (($row = fgetcsv($handle, 0, $this->delimiter, $this->enclosure, $this->escape)) !== false) {
                // Trim whitespace from each cell; fgetcsv can leave leading spaces
                yield $lineNumber => array_map('trim', $row);
                $lineNumber++;
            }
        } finally {
            // Guaranteed close even if the caller abandons the generator mid-stream
            fclose($handle);
        }
    }

    /**
     * Reads only the header row without streaming the rest of the file.
     * Useful for a quick header-only validation pass.
     */
    public function readHeader(string $filePath): array
    {
        foreach ($this->read($filePath) as $row) {
            return $row;
        }
        return [];
    }
}
