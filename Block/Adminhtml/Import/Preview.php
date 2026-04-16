<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import;

use Magento\Backend\Block\Template;

/**
 * Class Preview
 */
class Preview extends Template
{
    /**
     * @param string $value
     * @return string
     */
    public function formatHeader(string $value): string
    {
        return ucwords(str_replace('_', ' ', strtolower($value)));
    }
}
