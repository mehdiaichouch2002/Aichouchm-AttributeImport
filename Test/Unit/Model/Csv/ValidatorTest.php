<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Test\Unit\Model\Csv;

use Aichouchm\AttributeImport\Model\Csv\Validator;
use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Eav\Model\Entity\Attribute\AbstractAttribute;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\MockObject\Stub;
use PHPUnit\Framework\TestCase;

class ValidatorTest extends TestCase
{
    private const ADMIN_CODES = ['admin', 'default'];
    private const STORE_CODES = ['admin', 'default', 'fr', 'en'];

    /**
     * @var Validator
     */
    private Validator $validator;

    protected function setUp(): void
    {
        /** @var StoreResolver&Stub $storeResolver */
        $storeResolver = $this->createStub(StoreResolver::class);
        $storeResolver->method('isAdminStoreCode')->willReturnCallback(
            static fn (string $code): bool => in_array(strtolower($code), self::ADMIN_CODES, true)
        );
        $storeResolver->method('isValidStoreCode')->willReturnCallback(
            static fn (string $code): bool => in_array(strtolower($code), self::STORE_CODES, true)
        );

        $this->validator = new Validator($storeResolver);
    }

    /**
     * @param array<int,string[]> $rows
     * @param int $swatchType
     * @return string[]
     */
    private function validate(array $rows, int $swatchType = Validator::SWATCH_NONE): array
    {
        return $this->validator->validateRows($rows, 'color', $swatchType);
    }

    public function testValidVisualSwatchFilePasses(): void
    {
        $this->assertSame([], $this->validate([
            ['color', 'default', 'Red', '#FF0000', '1', '1'],
            ['color', 'fr', 'Rouge', '#FF0000', '1', '1'],
            ['color', 'default', 'Blue', '#0000FF', '2', '0'],
        ], Validator::SWATCH_VISUAL));
    }

    public function testHeadersMustMatchExactly(): void
    {
        $this->assertSame([], $this->validator->validateHeaders(Validator::EXPECTED_HEADERS));
        $this->assertNotEmpty($this->validator->validateHeaders(['attribute_code', 'store_view']));
        $this->assertNotEmpty($this->validator->validateHeaders(
            ['attribute_code', 'store', 'value', 'hex_code', 'sort_order', 'is_default']
        ));
    }

    /**
     * @param string[] $row
     * @param string $expectedFragment
     */
    #[DataProvider('invalidRowProvider')]
    public function testInvalidAdminRowIsRejected(array $row, string $expectedFragment): void
    {
        $errors = $this->validate([$row], Validator::SWATCH_VISUAL);

        $this->assertNotEmpty($errors);
        $this->assertStringContainsString($expectedFragment, implode(' | ', $errors));
    }

    /**
     * @return array<string,array{0:string[],1:string}>
     */
    public static function invalidRowProvider(): array
    {
        return [
            'non-numeric sort order' => [['color', 'default', 'Red', '#FF0000', 'abc', '0'], 'must be a number'],
            'negative sort order'    => [['color', 'default', 'Red', '#FF0000', '-1', '0'], '0 or greater'],
            'decimal sort order'     => [['color', 'default', 'Red', '#FF0000', '1.5', '0'], 'whole number'],
            'bad is_default'         => [['color', 'default', 'Red', '#FF0000', '1', '2'], 'is_default must be 0 or 1'],
            'bad hex'                => [['color', 'default', 'Red', 'red', '1', '0'], 'not a valid hex colour'],
            'missing hex'            => [['color', 'default', 'Red', '', '1', '0'], 'hex_code is required'],
            'html in value'          => [['color', 'default', '<b>Red</b>', '#FF0000', '1', '0'], 'HTML tags'],
            'newline in value'       => [
                ['color', 'default', "Red\nINFO: forged", '#FF0000', '1', '0'],
                'control characters',
            ],
            'wrong attribute code'   => [['size', 'default', 'Red', '#FF0000', '1', '0'], 'does not match'],
            'too few columns'        => [['color', 'default', 'Red'], 'expected 6 columns'],
        ];
    }

    public function testDuplicateAdminValuesAreCaseInsensitive(): void
    {
        $errors = $this->validate([
            ['color', 'default', 'Red', '', '1', '0'],
            ['color', 'default', 'RED', '', '2', '0'],
        ]);

        $this->assertCount(1, $errors);
        $this->assertStringContainsString('Duplicate option value "RED"', $errors[0]);
    }

    public function testOnlyOneDefaultOptionIsAllowed(): void
    {
        $errors = $this->validate([
            ['color', 'default', 'Red', '', '1', '1'],
            ['color', 'default', 'Blue', '', '2', '1'],
        ]);

        $this->assertCount(1, $errors);
        $this->assertStringContainsString('already set for another option', $errors[0]);
    }

    public function testStoreRowRules(): void
    {
        $errors = $this->validate([
            ['color', 'fr', 'Rouge', '', '1', '0'],
            ['color', 'default', 'Red', '', '1', '0'],
            ['color', 'de', 'Rot', '', '1', '0'],
            ['color', 'fr', 'Rouge', '', '1', '0'],
            ['color', 'fr', 'Rouge encore', '', '1', '0'],
        ]);

        $joined = implode(' | ', $errors);
        $this->assertStringContainsString('appears before any admin', $joined);
        $this->assertStringContainsString('"de" does not exist', $joined);
        $this->assertStringContainsString('appears more than once', $joined);
    }

    public function testPlainSelectIgnoresHexColumn(): void
    {
        $this->assertSame([], $this->validate([['color', 'default', 'Small', 'anything', '1', '0']]));
    }

    /**
     * @param string|null $additionalData
     * @param int $expected
     */
    #[DataProvider('swatchTypeProvider')]
    public function testSwatchTypeIsReadFromAdditionalData(?string $additionalData, int $expected): void
    {
        $attribute = $this->createStub(AbstractAttribute::class);
        $attribute->method('getData')->willReturn($additionalData);

        $this->assertSame($expected, $this->validator->getSwatchType($attribute));
    }

    /**
     * @return array<string,array{0:string|null,1:int}>
     */
    public static function swatchTypeProvider(): array
    {
        return [
            'visual'       => ['{"swatch_input_type":"visual"}', Validator::SWATCH_VISUAL],
            'text'         => ['{"swatch_input_type":"text"}', Validator::SWATCH_TEXT],
            'plain select' => [null, Validator::SWATCH_NONE],
            'invalid json' => ['{not json', Validator::SWATCH_NONE],
        ];
    }
}
