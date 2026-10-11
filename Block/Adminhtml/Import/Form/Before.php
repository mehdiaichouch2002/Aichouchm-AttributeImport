<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Block\Adminhtml\Import\Form;

use Magento\Backend\Block\Template;
use Magento\Framework\Serialize\Serializer\Json;

/**
 * Preview/notification containers and the JS component configuration.
 */
class Before extends Template
{
    /**
     * @param Template\Context $context
     * @param Json $json
     * @param array $data
     */
    public function __construct(
        Template\Context $context,
        private readonly Json $json,
        array $data = []
    ) {
        parent::__construct($context, $data);
    }

    /**
     * JSON configuration for Aichouchm_AttributeImport/js/attribute-import.
     *
     * @return string
     */
    public function getJsConfig(): string
    {
        return (string) $this->json->serialize([
            'Aichouchm_AttributeImport/js/attribute-import' => [
                'previewUrl' => $this->getUrl('attributeimport/import/preview'),
                'processUrl' => $this->getUrl('attributeimport/import/process'),
                'logUrl'     => $this->getUrl('attributeimport/import/log'),
            ],
        ]);
    }
}
