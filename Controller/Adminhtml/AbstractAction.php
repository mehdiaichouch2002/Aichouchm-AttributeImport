<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Controller\Adminhtml;

use Magento\Backend\App\Action;

/**
 * Shared ACL resource for every Import Attributes admin action.
 */
abstract class AbstractAction extends Action
{
    public const ADMIN_RESOURCE = 'Aichouchm_AttributeImport::import_attributes';
}
