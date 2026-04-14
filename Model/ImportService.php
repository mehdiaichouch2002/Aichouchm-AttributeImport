<?php

declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model;

use Aichouchm\AttributeImport\Api\ImportServiceInterface;
use Aichouchm\AttributeImport\Model\Attribute\OptionProcessor;
use Aichouchm\AttributeImport\Model\Csv\StreamingReader;
use Aichouchm\AttributeImport\Model\Csv\Validator as CsvValidator;
use Magento\Eav\Api\AttributeRepositoryInterface;
use Magento\Framework\App\Cache\Manager as CacheManager;
use Magento\Framework\App\ResourceConnection;
use Psr\Log\LoggerInterface;
use Throwable;

class ImportService implements ImportServiceInterface
{
    private const ENTITY_TYPE = 'catalog_product';

    public function __construct(
        private readonly StreamingReader              $streamingReader,
        private readonly CsvValidator                $csvValidator,
        private readonly OptionProcessor             $optionProcessor,
        private readonly AttributeRepositoryInterface $attributeRepository,
        private readonly ResourceConnection          $resourceConnection,
        private readonly CacheManager                $cacheManager,
        private readonly LoggerInterface             $logger
    ) {}

    public function validate(string $filePath, string $attributeCode): array
    {
        try {
            [$swatchType, $allRows] = $this->readAllRows($filePath, $attributeCode);

            $headerErrors = $this->csvValidator->validateHeaders($allRows[0] ?? [], $swatchType);
            if (!empty($headerErrors)) {
                return ['is_valid' => false, 'errors' => $headerErrors, 'rows' => []];
            }

            $dataRows  = array_slice($allRows, 1);
            $rowErrors = $this->csvValidator->validateRows($dataRows, $attributeCode, $swatchType);

            return [
                'is_valid' => empty($rowErrors),
                'errors'   => $rowErrors,
                'rows'     => $allRows,
            ];
        } catch (Throwable $e) {
            return ['is_valid' => false, 'errors' => [$e->getMessage()], 'rows' => []];
        }
    }

    public function import(string $filePath, string $attributeCode): array
    {
        $this->logger->info(sprintf('[%s] Import started — attribute: %s', date('Y-m-d H:i:s'), $attributeCode));

        try {
            $validation = $this->validate($filePath, $attributeCode);
            if (!$validation['is_valid']) {
                foreach ($validation['errors'] as $error) {
                    $this->logger->error(sprintf('[%s] Validation error: %s', date('Y-m-d H:i:s'), $error));
                }
                return ['success' => false, 'messages' => $validation['errors'], 'imported' => 0, 'skipped' => 0];
            }

            $attribute       = $this->attributeRepository->get(self::ENTITY_TYPE, $attributeCode);
            $swatchType      = $this->csvValidator->getSwatchType($attributeCode);
            $existingOptions = $this->loadExistingOptions((int) $attribute->getAttributeId());
            $groups          = $this->groupRowsByOption($filePath, $swatchType);

            $result = $this->optionProcessor->processGroups($groups, $existingOptions, $swatchType, $attribute);

            foreach ($result['skippedValues'] as $val) {
                $this->logger->warning(sprintf(
                    '[%s] Skipped: "%s" already exists for attribute "%s".',
                    date('Y-m-d H:i:s'), $val, $attributeCode
                ));
            }

            $this->cacheManager->clean(['eav', 'full_page', 'block_html']);

            $summary = (string) __(
                'Import complete. Imported: %1, Skipped (already exist): %2',
                $result['imported'],
                $result['skipped']
            );
            $this->logger->info(sprintf('[%s] %s', date('Y-m-d H:i:s'), $summary));

            return [
                'success'  => true,
                'messages' => [$summary],
                'imported' => $result['imported'],
                'skipped'  => $result['skipped'],
            ];
        } catch (Throwable $e) {
            $this->logger->error(sprintf('[%s] Unexpected error: %s', date('Y-m-d H:i:s'), $e->getMessage()));
            return [
                'success'  => false,
                'messages' => [(string) __('An unexpected error occurred. Please check the import log.')],
                'imported' => 0,
                'skipped'  => 0,
            ];
        }
    }

    private function readAllRows(string $filePath, string $attributeCode): array
    {
        $swatchType = $this->csvValidator->getSwatchType($attributeCode);
        $rows       = [];
        foreach ($this->streamingReader->read($filePath) as $row) {
            $rows[] = $row;
        }
        return [$swatchType, $rows];
    }

    private function groupRowsByOption(string $filePath, int $swatchType): array
    {
        $groups       = [];
        $currentGroup = null;

        foreach ($this->streamingReader->read($filePath) as $lineNumber => $row) {
            if ($lineNumber === 0) {
                continue;
            }

            $storeCode = strtolower(trim($row[1] ?? ''));
            $isAdmin   = in_array($storeCode, ['admin', 'default', '0'], true);

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
