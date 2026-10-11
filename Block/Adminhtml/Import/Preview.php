<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import;

use Magento\Backend\Block\Template;

/**
 * Validation preview table (rendered by the Preview controller).
 */
class Preview extends Template
{
    /**
     * Turn a CSV header such as "hex_code" into "Hex Code".
     *
     * @param string $value
     * @return string
     */
    public function formatHeader(string $value): string
    {
        return ucwords(str_replace('_', ' ', strtolower($value)));
    }
}
