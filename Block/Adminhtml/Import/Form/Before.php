<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import\Form;

use Magento\Backend\Block\Template;

class Before extends Template
{
    public function getPreviewUrl(): string
    {
        return $this->getUrl('attributeimport/import/preview');
    }

    public function getProcessUrl(): string
    {
        return $this->getUrl('attributeimport/import/process');
    }
}
