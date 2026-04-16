<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Controller\Adminhtml;

use Magento\Backend\App\Action;

/**
 * Base admin controller
 */
abstract class AbstractAction extends Action
{
    /**
     * Authorization resource
     */
    public const ADMIN_RESOURCE = 'Aichouchm_AttributeImport::import_attributes';
}
