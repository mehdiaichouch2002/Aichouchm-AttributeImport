<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Test\Unit\Model\Csv;

use Aichouchm\AttributeImport\Model\Csv\Validator;
use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Catalog\Model\ResourceModel\Eav\Attribute;
use Magento\Catalog\Model\ResourceModel\Eav\AttributeFactory;
use PHPUnit\Framework\MockObject\MockObject;
use PHPUnit\Framework\TestCase;

class ValidatorTest extends TestCase
{
    private Validator $validator;
    /** @var StoreResolver&MockObject */
    private StoreResolver $storeResolver;

    protected function setUp(): void
    {
        $this->storeResolver = $this->createMock(StoreResolver::class);
        $this->storeResolver->method('isValidStoreCode')->willReturn(true);
        $this->storeResolver->method('getAllStoreCodes')->willReturn(['default', 'fr', 'en']);

        $attributeModel = $this->createMock(Attribute::class);
        $attributeModel->method('getAdditionalData')->willReturn(null);

        $attributeFactory = $this->createMock(AttributeFactory::class);
        $attributeFactory->method('create')->willReturn($attributeModel);

        $this->validator = new Validator($this->storeResolver, $attributeFactory);
    }

    // ── Header validation ─────────────────────────────────────────────────────

    public function testValidHeadersNoSwatchPass(): void
    {
        $errors = $this->validator->validateHeaders(
            ['attribute_code', 'store_view', 'value', 'sort_order', 'is_default'],
            Validator::SWATCH_NONE
        );
        $this->assertEmpty($errors);
    }

    public function testValidHeadersWithSwatchPass(): void
    {
        $errors = $this->validator->validateHeaders(
            ['attribute_code', 'store_view', 'value', 'hex_code', 'sort_order', 'is_default'],
            Validator::SWATCH_VISUAL
        );
        $this->assertEmpty($errors);
    }

    public function testWrongColumnCountReturnsError(): void
    {
        $errors = $this->validator->validateHeaders(
            ['attribute_code', 'store_view', 'value'],
            Validator::SWATCH_NONE
        );
        $this->assertNotEmpty($errors);
        $this->assertStringContainsString('column count', $errors[0]);
    }

    public function testWrongHeaderNameReturnsError(): void
    {
        $errors = $this->validator->validateHeaders(
            ['attribute_code', 'store', 'value', 'sort_order', 'is_default'],
            Validator::SWATCH_NONE
        );
        $this->assertNotEmpty($errors);
    }

    // ── Row validation ────────────────────────────────────────────────────────

    public function testValidRowsPass(): void
    {
        $rows = [
            ['color', 'admin', 'Red', '1', '1'],
            ['color', 'fr',    'Rouge', '1', '1'],
            ['color', 'admin', 'Blue', '2', '0'],
        ];
        $errors = $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
        $this->assertEmpty($errors);
    }

    public function testMissingValueReturnsError(): void
    {
        $rows   = [['color', 'admin', '', '1', '1']];
        $errors = $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
        $this->assertNotEmpty($errors);
    }

    public function testWrongAttributeCodeReturnsError(): void
    {
        $rows   = [['size', 'admin', 'Red', '1', '1']];
        $errors = $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
        $this->assertNotEmpty($errors);
        $this->assertStringContainsString('attribute_code', $errors[0]);
    }

    public function testNonNumericSortOrderReturnsError(): void
    {
        $rows   = [['color', 'admin', 'Red', 'abc', '1']];
        $errors = $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
        $this->assertNotEmpty($errors);
        $this->assertStringContainsString('sort_order', $errors[0]);
    }

    public function testDuplicateAdminValueReturnsError(): void
    {
        $rows = [
            ['color', 'admin', 'Red', '1', '1'],
            ['color', 'admin', 'Red', '2', '0'],
        ];
        $errors = $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
        $this->assertNotEmpty($errors);
        $this->assertStringContainsString('Duplicate', $errors[0]);
    }

    public function testMultipleDefaultsReturnsError(): void
    {
        $rows = [
            ['color', 'admin', 'Red', '1', '1'],
            ['color', 'admin', 'Blue', '2', '1'],
        ];
        $errors = $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
        $this->assertNotEmpty($errors);
        $this->assertStringContainsString('is_default', $errors[0]);
    }

    public function testDuplicateStoreInGroupReturnsError(): void
    {
        $rows = [
            ['color', 'admin', 'Red', '1', '1'],
            ['color', 'fr',    'Rouge', '1', '1'],
            ['color', 'fr',    'Rouge duplicate', '1', '1'],
        ];
        $errors = $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
        $this->assertNotEmpty($errors);
        $this->assertStringContainsString('Store view', $errors[0]);
    }

    public function testValidatorIsStateless(): void
    {
        // Running validation twice should give the same result, not accumulated errors
        $rows = [['color', 'admin', 'Red', '1', '1']];
        $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
        $errors = $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
        $this->assertEmpty($errors);
    }

    public function testDefaultStoreCodeAcceptedAsAdmin(): void
    {
        // 'default' must be accepted as an alias for the admin store
        $rows = [
            ['color', 'default', 'Red', '1', '1'],
            ['color', 'fr',      'Rouge', '1', '1'],
        ];
        $errors = $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
        $this->assertEmpty($errors);
    }
}
