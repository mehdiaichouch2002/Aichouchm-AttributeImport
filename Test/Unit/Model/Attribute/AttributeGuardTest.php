<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Test\Unit\Model\Attribute;

use Aichouchm\AttributeImport\Model\Attribute\AttributeGuard;
use Magento\Eav\Model\Config as EavConfig;
use Magento\Eav\Model\Entity\Attribute\AbstractAttribute;
use Magento\Framework\Exception\LocalizedException;
use PHPUnit\Framework\TestCase;

class AttributeGuardTest extends TestCase
{
    /**
     * @param int|null $id
     * @param bool $userDefined
     * @param string $input
     * @return AttributeGuard
     */
    private function guardFor(?int $id, bool $userDefined, string $input): AttributeGuard
    {
        $attribute = $this->createStub(AbstractAttribute::class);
        $attribute->method('getAttributeId')->willReturn($id);
        $attribute->method('getIsUserDefined')->willReturn($userDefined);
        $attribute->method('getFrontendInput')->willReturn($input);

        $eavConfig = $this->createStub(EavConfig::class);
        $eavConfig->method('getAttribute')->willReturn($attribute);

        return new AttributeGuard($eavConfig);
    }

    public function testUserDefinedSelectIsAllowed(): void
    {
        $attribute = $this->guardFor(93, true, 'select')->getImportableAttribute('color');

        $this->assertSame(93, $attribute->getAttributeId());
    }

    public function testSystemAttributeIsRejected(): void
    {
        $this->expectException(LocalizedException::class);
        $this->expectExceptionMessage('not a user-defined select or multiselect');

        $this->guardFor(97, false, 'select')->getImportableAttribute('status');
    }

    public function testTextAttributeIsRejected(): void
    {
        $this->expectException(LocalizedException::class);

        $this->guardFor(73, true, 'text')->getImportableAttribute('custom_text');
    }

    public function testUnknownAttributeIsRejected(): void
    {
        $this->expectException(LocalizedException::class);
        $this->expectExceptionMessage('does not exist');

        $this->guardFor(null, true, 'select')->getImportableAttribute('nope');
    }

    public function testEmptyCodeIsRejected(): void
    {
        $this->expectException(LocalizedException::class);

        $this->guardFor(93, true, 'select')->getImportableAttribute('');
    }
}
