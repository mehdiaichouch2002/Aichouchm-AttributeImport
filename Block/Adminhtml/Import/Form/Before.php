<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import\Form;

use Magento\Backend\Block\Template;

/**
 * Provides AJAX endpoint URLs to the JavaScript layer.
 *
 * WHY EXPOSE URLS VIA A BLOCK:
 *   Hardcoding admin URLs in .js files breaks when the admin path changes
 *   (e.g. /admin → /secure_admin). The block resolves routes dynamically via
 *   the URL model, so the JS always uses the correct current admin URL.
 */
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
