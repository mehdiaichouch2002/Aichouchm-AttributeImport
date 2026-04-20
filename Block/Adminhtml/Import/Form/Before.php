<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import\Form;

use Magento\Backend\Block\Template;

/**
 * Class Before
 */
class Before extends Template
{
    /**
     * @return string
     */
    public function getPreviewUrl(): string
    {
        return $this->getUrl('attributeimport/import/preview');
    }

    /**
     * @return string
     */
    public function getProcessUrl(): string
    {
        return $this->getUrl('attributeimport/import/process');
    }
}
