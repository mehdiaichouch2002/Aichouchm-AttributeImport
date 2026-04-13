<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import;

use Magento\Backend\Block\Template;

/**
 * Preview block rendered server-side and returned as HTML via AJAX.
 */
class Preview extends Template
{
    /**
     * Formats a CSV column header (e.g. "sort_order" → "Sort Order").
     */
    public function formatHeader(string $value): string
    {
        return ucwords(str_replace('_', ' ', strtolower($value)));
    }
}
