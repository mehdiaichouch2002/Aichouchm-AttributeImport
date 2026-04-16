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
        return $this->toRelativePath($this->getUrl('attributeimport/import/preview'));
    }

    /**
     * @return string
     */
    public function getProcessUrl(): string
    {
        return $this->toRelativePath($this->getUrl('attributeimport/import/process'));
    }

    /**
     * @param string $url
     * @return string
     */
    private function toRelativePath(string $url): string
    {
        $parts = parse_url($url);
        $path  = $parts['path'] ?? '/';
        return empty($parts['query']) ? $path : $path . '?' . $parts['query'];
    }
}
