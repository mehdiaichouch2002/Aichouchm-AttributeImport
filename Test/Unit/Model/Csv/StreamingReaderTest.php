<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Test\Unit\Model\Csv;

use Aichouchm\AttributeImport\Model\Csv\StreamingReader;
use PHPUnit\Framework\TestCase;
use RuntimeException;

class StreamingReaderTest extends TestCase
{
    private StreamingReader $reader;

    protected function setUp(): void
    {
        $this->reader = new StreamingReader();
    }

    public function testReadYieldsAllRows(): void
    {
        $csv = $this->writeTempCsv([
            'attribute_code,store_view,value,sort_order,is_default',
            'color,admin,Red,1,1',
            'color,fr,Rouge,1,1',
        ]);

        $rows = iterator_to_array($this->reader->read($csv));
        unlink($csv);

        $this->assertCount(3, $rows);
        $this->assertSame(['attribute_code', 'store_view', 'value', 'sort_order', 'is_default'], $rows[0]);
        $this->assertSame(['color', 'admin', 'Red', '1', '1'], $rows[1]);
        $this->assertSame(['color', 'fr', 'Rouge', '1', '1'], $rows[2]);
    }

    public function testReadStripsUtf8Bom(): void
    {
        $csv = $this->writeTempCsv(["\xEF\xBB\xBFattribute_code,store_view,value,sort_order,is_default"]);

        $rows = iterator_to_array($this->reader->read($csv));
        unlink($csv);

        $this->assertSame('attribute_code', $rows[0][0]);
    }

    public function testReadTrimsWhitespace(): void
    {
        $csv = $this->writeTempCsv(['  color  ,  admin  ,  Red  ,  1  ,  1  ']);

        $rows = iterator_to_array($this->reader->read($csv));
        unlink($csv);

        $this->assertSame(['color', 'admin', 'Red', '1', '1'], $rows[0]);
    }

    public function testReadThrowsOnMissingFile(): void
    {
        $this->expectException(RuntimeException::class);
        iterator_to_array($this->reader->read('/nonexistent/path/file.csv'));
    }

    public function testReadHeaderReturnsOnlyFirstRow(): void
    {
        $csv = $this->writeTempCsv([
            'attribute_code,store_view,value,sort_order,is_default',
            'color,admin,Red,1,1',
        ]);

        $header = $this->reader->readHeader($csv);
        unlink($csv);

        $this->assertSame(['attribute_code', 'store_view', 'value', 'sort_order', 'is_default'], $header);
    }

    public function testReadEmptyFileYieldsNoRows(): void
    {
        $csv  = tempnam(sys_get_temp_dir(), 'csv');
        file_put_contents($csv, '');

        $rows = iterator_to_array($this->reader->read($csv));
        unlink($csv);

        $this->assertEmpty($rows);
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private function writeTempCsv(array $lines): string
    {
        $path = tempnam(sys_get_temp_dir(), 'csv');
        file_put_contents($path, implode("\n", $lines));
        return $path;
    }
}
