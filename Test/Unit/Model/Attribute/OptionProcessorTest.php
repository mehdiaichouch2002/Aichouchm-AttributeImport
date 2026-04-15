<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Test\Unit\Model\Attribute;

use Aichouchm\AttributeImport\Model\Attribute\OptionProcessor;
use Aichouchm\AttributeImport\Model\Csv\Validator;
use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Eav\Api\Data\AttributeInterface;
use Magento\Framework\App\ResourceConnection;
use Magento\Framework\DB\Adapter\AdapterInterface;
use PHPUnit\Framework\MockObject\MockObject;
use PHPUnit\Framework\TestCase;

class OptionProcessorTest extends TestCase
{
    /** @var ResourceConnection&MockObject */
    private ResourceConnection $resourceConnection;
    /** @var AdapterInterface&MockObject */
    private AdapterInterface $connection;
    /** @var StoreResolver&MockObject */
    private StoreResolver $storeResolver;
    /** @var AttributeInterface&MockObject */
    private AttributeInterface $attribute;

    private OptionProcessor $processor;

    protected function setUp(): void
    {
        $this->connection = $this->createMock(AdapterInterface::class);
        $this->connection->method('lastInsertId')->willReturnOnConsecutiveCalls(100, 101, 102);
        $this->connection->method('getTableName')->willReturnArgument(0);

        $this->resourceConnection = $this->createMock(ResourceConnection::class);
        $this->resourceConnection->method('getConnection')->willReturn($this->connection);
        $this->resourceConnection->method('getTableName')->willReturnArgument(0);

        $this->storeResolver = $this->createMock(StoreResolver::class);
        $this->storeResolver->method('getStoreId')->willReturnMap([
            ['admin',   0],
            ['default', 0],
            ['fr',      2],
            ['en',      3],
        ]);

        $this->attribute = $this->createMock(AttributeInterface::class);
        $this->attribute->method('getAttributeId')->willReturn(42);

        $this->processor = new OptionProcessor($this->resourceConnection, $this->storeResolver);
    }

    public function testNewOptionsAreInserted(): void
    {
        $this->connection->expects($this->once())
            ->method('insert')
            ->with(
                'eav_attribute_option',
                $this->arrayHasKey('attribute_id')
            );

        $this->connection->expects($this->once())
            ->method('insertMultiple');

        $groups = [
            [
                'admin'  => ['color', 'admin', 'Red', '', '1', '1'],
                'stores' => [['color', 'fr', 'Rouge', '', '1', '1']],
            ],
        ];

        $result = $this->processor->processGroups($groups, [], Validator::SWATCH_NONE, $this->attribute);

        $this->assertSame(1, $result['imported']);
        $this->assertSame(0, $result['skipped']);
    }

    public function testExistingOptionsAreSkipped(): void
    {
        $this->connection->expects($this->never())->method('insert');

        $groups = [
            [
                'admin'  => ['color', 'admin', 'Red', '', '1', '1'],
                'stores' => [],
            ],
        ];

        // 'Red' already exists in the DB
        $result = $this->processor->processGroups(
            $groups,
            ['Red' => 100],
            Validator::SWATCH_NONE,
            $this->attribute
        );

        $this->assertSame(0, $result['imported']);
        $this->assertSame(1, $result['skipped']);
        $this->assertSame(['Red'], $result['skippedValues']);
    }

    public function testMultipleGroupsMixedSkipAndImport(): void
    {
        $this->connection->method('insert')->willReturn(1);

        $groups = [
            [
                'admin'  => ['color', 'admin', 'Red',  '', '1', '1'],
                'stores' => [],
            ],
            [
                'admin'  => ['color', 'admin', 'Blue', '', '2', '0'],
                'stores' => [],
            ],
        ];

        // 'Red' exists, 'Blue' does not
        $result = $this->processor->processGroups(
            $groups,
            ['Red' => 100],
            Validator::SWATCH_NONE,
            $this->attribute
        );

        $this->assertSame(1, $result['imported']);
        $this->assertSame(1, $result['skipped']);
    }

    public function testSwatchDataIsPersistedForVisualSwatch(): void
    {
        $this->connection->method('insert')->willReturn(1);

        $this->connection->expects($this->once())
            ->method('insertOnDuplicate');

        $groups = [
            [
                'admin'  => ['color', 'admin', 'Red', '#FF0000', '1', '1'],
                'stores' => [],
            ],
        ];

        $this->processor->processGroups($groups, [], Validator::SWATCH_VISUAL, $this->attribute);
    }

    public function testEmptyGroupsReturnZeroCounts(): void
    {
        $result = $this->processor->processGroups([], [], Validator::SWATCH_NONE, $this->attribute);

        $this->assertSame(0, $result['imported']);
        $this->assertSame(0, $result['skipped']);
    }
}
