<?php
/**
 * Copyright © Mehdi Aichouch. All rights reserved.
 * See LICENSE for license details.
 */
declare(strict_types=1);

namespace Aichouchm\AttributeImport\Model;

use Aichouchm\AttributeImport\Api\ImportServiceInterface;
use Aichouchm\AttributeImport\Model\Attribute\AttributeGuard;
use Aichouchm\AttributeImport\Model\Attribute\OptionProcessor;
use Aichouchm\AttributeImport\Model\Csv\StreamingReader;
use Aichouchm\AttributeImport\Model\Csv\Validator as CsvValidator;
use Aichouchm\AttributeImport\Service\StoreResolver;
use Magento\Framework\App\Cache\Manager as CacheManager;
use Magento\Framework\App\ResourceConnection;
use Magento\Framework\Exception\LocalizedException;
use Magento\Store\Model\Store;
use Psr\Log\LoggerInterface;
use Throwable;

/**
 * Validates and imports attribute options from a CSV file.
 */
class ImportService implements ImportServiceInterface
{
    /**
     * Cache types refreshed after a successful import
     */
    private const CACHE_TYPES = ['eav', 'full_page', 'block_html'];

    /**
     * @param StreamingReader $streamingReader
     * @param CsvValidator $csvValidator
     * @param OptionProcessor $optionProcessor
     * @param AttributeGuard $attributeGuard
     * @param StoreResolver $storeResolver
     * @param ResourceConnection $resourceConnection
     * @param CacheManager $cacheManager
     * @param LoggerInterface $logger
     */
    public function __construct(
        private readonly StreamingReader $streamingReader,
        private readonly CsvValidator $csvValidator,
        private readonly OptionProcessor $optionProcessor,
        private readonly AttributeGuard $attributeGuard,
        private readonly StoreResolver $storeResolver,
        private readonly ResourceConnection $resourceConnection,
        private readonly CacheManager $cacheManager,
        private readonly LoggerInterface $logger
    ) {
    }

    /**
     * @inheritdoc
     */
    public function validate(string $filePath, string $attributeCode): array
    {
        try {
            $attribute  = $this->attributeGuard->getImportableAttribute($attributeCode);
            $swatchType = $this->csvValidator->getSwatchType($attribute);
            $rows       = iterator_to_array($this->streamingReader->read($filePath), false);

            $headerErrors = $this->csvValidator->validateHeaders($rows[0] ?? []);
            if ($headerErrors !== []) {
                return $this->invalid($headerErrors);
            }

            $errors = $this->csvValidator->validateRows(array_slice($rows, 1), $attributeCode, $swatchType);

            return [
                'is_valid'    => $errors === [],
                'errors'      => $errors,
                'rows'        => $rows,
                'swatch_type' => $swatchType,
            ];
        } catch (LocalizedException $e) {
            return $this->invalid([$e->getMessage()]);
        } catch (Throwable $e) {
            $this->logger->error(sprintf('Validation failed unexpectedly: %s', $e));
            return $this->invalid([(string) __('The file could not be read. See attribute_import.log for details.')]);
        }
    }

    /**
     * @inheritdoc
     */
    public function import(string $filePath, string $attributeCode): array
    {
        $this->logger->info(sprintf('Import started — attribute: %s', $attributeCode));

        $validation = $this->validate($filePath, $attributeCode);
        if (!$validation['is_valid']) {
            foreach ($validation['errors'] as $error) {
                $this->logger->error(sprintf('Validation error: %s', $error));
            }
            return $this->result(false, $validation['errors']);
        }

        try {
            $attribute = $this->attributeGuard->getImportableAttribute($attributeCode);
            $result    = $this->optionProcessor->processGroups(
                $this->groupRowsByOption($validation['rows']),
                $this->loadExistingOptions((int) $attribute->getAttributeId()),
                $validation['swatch_type'],
                $attribute
            );
        } catch (LocalizedException $e) {
            $this->logger->error(sprintf('Import failed: %s', $e->getMessage()));
            return $this->result(false, [$e->getMessage()]);
        } catch (Throwable $e) {
            $this->logger->error(sprintf('Import failed unexpectedly: %s', $e));
            return $this->result(false, [(string) __('An unexpected error occurred. Please check the import log.')]);
        }

        foreach ($result['skippedValues'] as $value) {
            $this->logger->warning(sprintf('Skipped: "%s" already exists for attribute "%s".', $value, $attributeCode));
        }

        if ($result['imported'] > 0) {
            $this->cacheManager->clean(self::CACHE_TYPES);
        }

        $summary = (string) __(
            'Import complete. Imported: %1, Skipped (already exist): %2',
            $result['imported'],
            $result['skipped']
        );
        $this->logger->info($summary);

        return $this->result(true, [$summary], $result['imported'], $result['skipped']);
    }

    /**
     * Split rows into option groups: an admin row followed by its translations.
     *
     * @param array<int,string[]> $rows Header included
     * @return array<int,array{admin:string[],stores:array<int,string[]>}>
     */
    private function groupRowsByOption(array $rows): array
    {
        $groups  = [];
        $current = null;

        foreach (array_slice($rows, 1) as $row) {
            if ($this->storeResolver->isAdminStoreCode($row[CsvValidator::COL_STORE_VIEW])) {
                if ($current !== null) {
                    $groups[] = $current;
                }
                $current = ['admin' => $row, 'stores' => []];
            } elseif ($current !== null) {
                $current['stores'][] = $row;
            }
        }

        if ($current !== null) {
            $groups[] = $current;
        }

        return $groups;
    }

    /**
     * Admin labels of the attribute's existing options, lower-cased.
     *
     * @param int $attributeId
     * @return array<string,int>
     */
    private function loadExistingOptions(int $attributeId): array
    {
        $connection = $this->resourceConnection->getConnection();
        $select     = $connection->select()
            ->from(
                ['v' => $this->resourceConnection->getTableName('eav_attribute_option_value')],
                ['value', 'option_id']
            )
            ->join(
                ['o' => $this->resourceConnection->getTableName('eav_attribute_option')],
                'v.option_id = o.option_id',
                []
            )
            ->where('o.attribute_id = ?', $attributeId)
            ->where('v.store_id = ?', Store::DEFAULT_STORE_ID);

        $existing = [];
        foreach ($connection->fetchPairs($select) as $value => $optionId) {
            $existing[mb_strtolower((string) $value, 'UTF-8')] = (int) $optionId;
        }

        return $existing;
    }

    /**
     * Validation result for a file that cannot be imported.
     *
     * @param string[] $errors
     * @return array{is_valid:false,errors:string[],rows:array<int,string[]>,swatch_type:int}
     */
    private function invalid(array $errors): array
    {
        return ['is_valid' => false, 'errors' => $errors, 'rows' => [], 'swatch_type' => CsvValidator::SWATCH_NONE];
    }

    /**
     * Import result payload returned to the controller.
     *
     * @param bool $success
     * @param string[] $messages
     * @param int $imported
     * @param int $skipped
     * @return array{success:bool,messages:string[],imported:int,skipped:int}
     */
    private function result(bool $success, array $messages, int $imported = 0, int $skipped = 0): array
    {
        return ['success' => $success, 'messages' => $messages, 'imported' => $imported, 'skipped' => $skipped];
    }
}
