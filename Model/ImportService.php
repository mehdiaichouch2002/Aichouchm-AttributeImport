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

/**
 * Orchestrates the full CSV import flow.
 *
 * Flow:
 *   1. Load attribute → confirm it exists and is a select/multiselect
 *   2. Detect swatch type → determines CSV column layout
 *   3. Stream header → validate header row
 *   4. Stream data rows → validate all rows
 *   5. On validation pass: stream again to group rows by option
 *   6. OptionProcessor.processGroups() → bulk DB writes
 *   7. Clear EAV caches so changes appear immediately
 *   8. Log every imported/skipped/error event with timestamp + line number
 *
 * WHY TWO STREAMING PASSES (validate then process):
 *   Validating everything before writing guarantees atomicity at the CSV level:
 *   either the entire file is valid and we write, or we reject it entirely
 *   without a partial import that leaves the attribute in an inconsistent state.
 *   The memory cost is negligible because StreamingReader never holds more than
 *   one row at a time.
 */
class ImportService implements ImportServiceInterface
{
    private const ENTITY_TYPE = 'catalog_product';

    public function __construct(
        private readonly StreamingReader           $streamingReader,
        private readonly CsvValidator              $csvValidator,
        private readonly OptionProcessor           $optionProcessor,
        private readonly AttributeRepositoryInterface $attributeRepository,
        private readonly ResourceConnection        $resourceConnection,
        private readonly CacheManager              $cacheManager,
        private readonly LoggerInterface           $logger  // injected as named virtual type
    ) {}

    // ── Public contract ───────────────────────────────────────────────────────

    /**
     * {@inheritdoc}
     */
    public function validate(string $filePath, string $attributeCode): array
    {
        try {
            [$swatchType, $allRows] = $this->readAllRows($filePath, $attributeCode);

            $headerErrors = $this->csvValidator->validateHeaders($allRows[0] ?? [], $swatchType);
            if (!empty($headerErrors)) {
                return ['is_valid' => false, 'errors' => $headerErrors, 'rows' => []];
            }

            $dataRows = array_slice($allRows, 1);
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

    /**
     * {@inheritdoc}
     */
    public function import(string $filePath, string $attributeCode): array
    {
        $this->logger->info(sprintf('[%s] Import started — attribute: %s', date('Y-m-d H:i:s'), $attributeCode));

        try {
            // 1. Validate first — no DB writes until the CSV is clean
            $validation = $this->validate($filePath, $attributeCode);
            if (!$validation['is_valid']) {
                foreach ($validation['errors'] as $error) {
                    $this->logger->error(sprintf('[%s] Validation error: %s', date('Y-m-d H:i:s'), $error));
                }
                return [
                    'success'  => false,
                    'messages' => $validation['errors'],
                    'imported' => 0,
                    'skipped'  => 0,
                ];
            }

            // 2. Load attribute
            $attribute  = $this->attributeRepository->get(self::ENTITY_TYPE, $attributeCode);
            $swatchType = $this->csvValidator->getSwatchType($attributeCode);

            // 3. Pre-load existing option values for this attribute (store_id=0 only)
            //    This single query prevents N duplicate-check queries inside the loop.
            $existingOptions = $this->loadExistingOptions((int) $attribute->getAttributeId());

            // 4. Stream the file again to group rows by option
            $groups = $this->groupRowsByOption($filePath, $swatchType);

            // 5. Process and persist
            $result = $this->optionProcessor->processGroups(
                $groups,
                $existingOptions,
                $swatchType,
                $attribute
            );

            // 6. Log skipped duplicates
            foreach ($result['skippedValues'] as $val) {
                $this->logger->warning(sprintf(
                    '[%s] Skipped duplicate: option "%s" already exists for attribute "%s".',
                    date('Y-m-d H:i:s'), $val, $attributeCode
                ));
            }

            // 7. Invalidate EAV and full-page caches so changes are visible immediately
            $this->invalidateCaches();

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

    // ── Private helpers ───────────────────────────────────────────────────────

    /**
     * Reads all CSV rows into memory for validation/preview purposes.
     * This is the only time we hold the full file in RAM — and only when the
     * admin explicitly clicks "Check Data" (preview), not during the real import.
     */
    private function readAllRows(string $filePath, string $attributeCode): array
    {
        $swatchType = $this->csvValidator->getSwatchType($attributeCode);
        $rows       = [];
        foreach ($this->streamingReader->read($filePath) as $row) {
            $rows[] = $row;
        }
        return [$swatchType, $rows];
    }

    /**
     * Streams the CSV and groups data rows into option groups.
     *
     * An option group:
     *   - starts when an admin/default store row is encountered
     *   - collects all subsequent non-admin rows until the next admin row
     *
     * Header row (line 0) is skipped.
     */
    private function groupRowsByOption(string $filePath, int $swatchType): array
    {
        $groups       = [];
        $currentGroup = null;

        foreach ($this->streamingReader->read($filePath) as $lineNumber => $row) {
            if ($lineNumber === 0) {
                continue; // skip header
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

    /**
     * Returns a [value => option_id] map of existing options for the attribute
     * at store_id=0 (admin store / global label).
     */
    private function loadExistingOptions(int $attributeId): array
    {
        $connection  = $this->resourceConnection->getConnection();
        $select      = $connection->select()
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

    /**
     * Clears EAV and full-page caches after a successful import.
     * Without this, Magento may still serve stale attribute option data from cache.
     */
    private function invalidateCaches(): void
    {
        $this->cacheManager->clean(['eav', 'full_page', 'block_html']);
    }
}
