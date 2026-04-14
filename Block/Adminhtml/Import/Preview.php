<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import;

use Magento\Backend\Block\Template;

class Preview extends Template
{
    public function formatHeader(string $value): string
    {
        return ucwords(str_replace('_', ' ', strtolower($value)));
    }
}
