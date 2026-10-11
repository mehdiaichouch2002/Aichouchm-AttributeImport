<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Test\Unit\Model\Csv;

use Aichouchm\AttributeImport\Model\Csv\StreamingReader;
use Magento\Framework\Exception\LocalizedException;
use Magento\Framework\Filesystem\Driver\File;
use PHPUnit\Framework\TestCase;

class StreamingReaderTest extends TestCase
{
    /**
     * @var string
     */
    private string $file;

    protected function setUp(): void
    {
        $this->file = (string) tempnam(sys_get_temp_dir(), 'csv');
    }

    protected function tearDown(): void
    {
        if (is_file($this->file)) {
            unlink($this->file);
        }
    }

    /**
     * @param string $content
     * @return array<int,string[]>
     */
    private function read(string $content): array
    {
        file_put_contents($this->file, $content);

        return iterator_to_array((new StreamingReader(new File()))->read($this->file), false);
    }

    public function testRowsAreTrimmedAndBlankLinesSkipped(): void
    {
        $rows = $this->read("a, b ,c\n\n 1 ,2, 3 \n");

        $this->assertSame([['a', 'b', 'c'], ['1', '2', '3']], $rows);
    }

    public function testUtf8BomIsStrippedFromTheHeader(): void
    {
        $rows = $this->read("\xEF\xBB\xBFattribute_code,value\ncolor,Red\n");

        $this->assertSame('attribute_code', $rows[0][0]);
    }

    public function testQuotedCellsKeepCommasAndAccents(): void
    {
        $rows = $this->read("value\n\"Pêche, claire\"\n");

        $this->assertSame('Pêche, claire', $rows[1][0]);
    }

    public function testRowLimitIsEnforced(): void
    {
        $this->expectException(LocalizedException::class);

        $this->read("header\n" . str_repeat("x\n", StreamingReader::MAX_ROWS + 1));
    }

    public function testExactlyMaxRowsIsAccepted(): void
    {
        $rows = $this->read("header\n" . str_repeat("x\n", StreamingReader::MAX_ROWS));

        $this->assertCount(StreamingReader::MAX_ROWS + 1, $rows);
    }
}
