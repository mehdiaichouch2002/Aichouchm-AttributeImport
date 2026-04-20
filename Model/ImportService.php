<?php
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model;

use Aichouchm\AttributeImport\Api\ImportServiceInterface;
use Aichouchm\AttributeImport\Model\Attribute\OptionProcessor;
use Aichouchm\AttributeImport\Model\Csv\StreamingReader;
use Aichouchm\AttributeImport\Model\Csv\Validator as CsvValidator;
use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Eav\Model\Config as EavConfig;
use Magento\Framework\App\Cache\Manager as CacheManager;
use Magento\Framework\App\ResourceConnection;
use Psr\Log\LoggerInterface;
use Throwable;

/**
 * Class ImportService
 */
class ImportService implements ImportServiceInterface
{
    /**
     * EAV entity type for catalog products
     */
    private const ENTITY_TYPE = 'catalog_product';

    /**
     * @param StreamingReader $streamingReader
     * @param CsvValidator $csvValidator
     * @param OptionProcessor $optionProcessor
     * @param EavConfig $eavConfig
     * @param ResourceConnection $resourceConnection
     * @param CacheManager $cacheManager
     * @param LoggerInterface $logger
     */
    public function __construct(
        private readonly StreamingReader  $streamingReader,
        private readonly CsvValidator     $csvValidator,
        private readonly OptionProcessor  $optionProcessor,
        private readonly EavConfig        $eavConfig,
        private readonly ResourceConnection $resourceConnection,
        private readonly CacheManager     $cacheManager,
        private readonly LoggerInterface  $logger
    ) {}

    /**
     * @param string $filePath
     * @param string $attributeCode
     * @return array
     */
    public function validate(string $filePath, string $attributeCode): array
    {
        try {
            [$swatchType, $allRows] = $this->readAllRows($filePath, $attributeCode);

            $headerErrors = $this->csvValidator->validateHeaders($allRows[0] ?? []);
            if (!empty($headerErrors)) {
                return ['is_valid' => false, 'errors' => $headerErrors, 'rows' => [], 'swatch_type' => $swatchType];
            }

            $dataRows  = array_slice($allRows, 1);
            $rowErrors = $this->csvValidator->validateRows($dataRows, $attributeCode, $swatchType);

            return [
                'is_valid'   => empty($rowErrors),
                'errors'     => $rowErrors,
                'rows'       => $allRows,
                'swatch_type' => $swatchType,
            ];
        } catch (Throwable $e) {
            return ['is_valid' => false, 'errors' => [$e->getMessage()], 'rows' => [], 'swatch_type' => CsvValidator::SWATCH_NONE];
        }
    }

    /**
     * @param string $filePath
     * @param string $attributeCode
     * @return array
     */
    public function import(string $filePath, string $attributeCode): array
    {
        $this->logger->info(sprintf('Import started — attribute: %s', $attributeCode));

        try {
            $validation = $this->validate($filePath, $attributeCode);
            if (!$validation['is_valid']) {
                foreach ($validation['errors'] as $error) {
                    $this->logger->error(sprintf('Validation error: %s', $error));
                }
                return ['success' => false, 'messages' => $validation['errors'], 'imported' => 0, 'skipped' => 0];
            }

            $attribute       = $this->eavConfig->getAttribute(self::ENTITY_TYPE, $attributeCode);
            $swatchType      = $validation['swatch_type'];
            $existingOptions = $this->loadExistingOptions((int) $attribute->getAttributeId());
            $groups          = $this->groupRowsByOption($validation['rows']);

            $result = $this->optionProcessor->processGroups($groups, $existingOptions, $swatchType, $attribute);

            foreach ($result['skippedValues'] as $val) {
                $this->logger->warning(sprintf('Skipped: "%s" already exists for attribute "%s".', $val, $attributeCode));
            }

            $this->cacheManager->clean(['eav', 'full_page', 'block_html']);

            $summary = (string) __(
                'Import complete. Imported: %1, Skipped (already exist): %2',
                $result['imported'],
                $result['skipped']
            );
            $this->logger->info($summary);

            return [
                'success'  => true,
                'messages' => [$summary],
                'imported' => $result['imported'],
                'skipped'  => $result['skipped'],
            ];
        } catch (Throwable $e) {
            $this->logger->error(sprintf('Unexpected error: %s', $e->getMessage()));
            return [
                'success'  => false,
                'messages' => [(string) __('An unexpected error occurred. Please check the import log.')],
                'imported' => 0,
                'skipped'  => 0,
            ];
        }
    }

    /**
     * @param string $filePath
     * @param string $attributeCode
     * @return array
     */
    private function readAllRows(string $filePath, string $attributeCode): array
    {
        return [
            $this->csvValidator->getSwatchType($attributeCode),
            iterator_to_array($this->streamingReader->read($filePath), false),
        ];
    }

    /**
     * @param array $rows
     * @return array
     */
    private function groupRowsByOption(array $rows): array
    {
        $groups       = [];
        $currentGroup = null;

        foreach (array_slice($rows, 1) as $row) {
            $storeCode = strtolower(trim($row[CsvValidator::COL_STORE_VIEW] ?? ''));
            $isAdmin   = in_array($storeCode, StoreResolver::ADMIN_STORE_CODES, true);

            if ($isAdmin) {
                if ($currentGroup !== null) {
                    $groups[] = $currentGroup;
                }
                $currentGroup = ['admin' => $row, 'stores' => []];
            } elseif ($currentGroup !== null) {
                $currentGroup['stores'][] = $row;
            }
        }

        if ($currentGroup !== null) {
            $groups[] = $currentGroup;
        }

        return $groups;
    }

    /**
     * @param int $attributeId
     * @return array
     */
    private function loadExistingOptions(int $attributeId): array
    {
        $connection = $this->resourceConnection->getConnection();
        $select     = $connection->select()
            ->from(
                ['v' => $this->resourceConnection->getTableName('eav_attribute_option_value')],
                ['value', 'v.option_id']
            )
            ->join(
                ['o' => $this->resourceConnection->getTableName('eav_attribute_option')],
                'v.option_id = o.option_id',
                []
            )
            ->where('o.attribute_id = ?', $attributeId)
            ->where('v.store_id = ?', 0);

        $result = [];
        foreach ($connection->fetchAll($select) as $row) {
            $result[$row['value']] = (int) $row['option_id'];
        }
        return $result;
    }
}
