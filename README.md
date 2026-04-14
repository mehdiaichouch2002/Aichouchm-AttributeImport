# Aichouchm_AttributeImport

**Magento 2 module for bulk importing product attribute options from CSV files via the Admin Panel.**

---

## Overview

Magento 2 has no native way to bulk-import attribute options (the selectable values of a `select` or `multiselect` attribute, such as colors, sizes, or materials). The only built-in approach is clicking "Add Option" dozens of times in the admin UI — one row at a time.

This module adds a dedicated page under **Stores → Attributes → Import Attributes** that lets an admin:

1. Select an attribute (e.g. `color`)
2. Upload a CSV file containing all desired option values, their translations per store view, and (optionally) swatch data
3. Preview and validate the file before committing
4. Import with one click — new options are created, duplicates are logged and skipped
5. Review the import log directly in the admin panel

---

## Requirements

| Dependency | Version |
|---|---|
| PHP | ≥ 8.1 |
| Magento Open Source / Adobe Commerce | 2.4.x |
| `magento/module-swatches` | bundled with Magento |

---

## Installation

### Via Composer (recommended)

Ensure your Magento project's `composer.json` has:

```json
"minimum-stability": "dev",
"prefer-stable": true
```

Then:

```bash
composer require aichouchm/magento2-module-attribute-import
bin/magento module:enable Aichouchm_AttributeImport
bin/magento setup:upgrade
bin/magento cache:flush
```

### Via Composer path repository (local development)

Add to the root `composer.json` of your Magento project:

```json
"repositories": [
    { "type": "path", "url": "../Aichouchm-AttributeImport" }
]
```

Then:

```bash
composer require aichouchm/magento2-module-attribute-import
bin/magento module:enable Aichouchm_AttributeImport
bin/magento setup:upgrade
bin/magento cache:flush
```

### If you use the Robo dev environment

```bash
robo composer require aichouchm/magento2-module-attribute-import
robo magento module:enable Aichouchm_AttributeImport
robo magento setup:upgrade
robo magento cache:flush
```

---

## Admin Panel Location

**Stores → Attributes → Import Attributes**

A secondary link to the import log is accessible from the same page.

---

## CSV Format

### Plain `select` attribute (no swatch)

```
attribute_code,store_view,value,sort_order,is_default
size,default,Small,1,1
size,fr,Petite,1,1
size,en,Small,1,1
size,default,Medium,2,0
size,fr,Moyenne,2,0
size,en,Medium,2,0
```

### Visual swatch attribute (hex colour or image URL)

```
attribute_code,store_view,value,swatch,sort_order,is_default
color,default,Red,#FF0000,1,1
color,fr,Rouge,#FF0000,1,1
color,en,Red,#FF0000,1,1
color,default,Blue,#0000FF,2,0
color,fr,Bleu,#0000FF,2,0
color,en,Blue,#0000FF,2,0
```

> The `swatch` column also accepts the alias `hex_code` (as shown in the spec).  
> For image swatches, provide an absolute or root-relative URL (e.g. `/media/swatch/red.jpg`).

### Text swatch attribute

Same 6-column layout as visual swatch. The `swatch` value is a styled label string.

---

## Column Reference

| Column | Required | Description |
|---|---|---|
| `attribute_code` | Yes | Must match the attribute you selected in the form. Every row must have the same value. |
| `store_view` | Yes | `default` or `admin` = global label (store\_id=0). Any other value must be a valid Magento store code (e.g. `fr`, `en`). |
| `value` | Yes | The option label for this store view. |
| `swatch` / `hex_code` | Yes (swatch attrs only) | Hex colour (`#RRGGBB`) or image URL. Ignored for text swatches (use the `value` column instead). |
| `sort_order` | Yes (admin row only) | Integer. Controls the display order of the option in dropdowns. |
| `is_default` | Yes (admin row only) | `1` = this option is the default selected value. Only one option may have `is_default=1`. |

---

## Row Grouping Rules

Each option is defined as a **group** of rows:

- The **first row** of a group has `store_view = default` (or `admin`) — this is the global (admin-store) label.
- Subsequent rows have other store view codes — these are translations.
- A new group begins at the next `default`/`admin` row.

```
color,default,Red,#FF0000,1,1   ← start of group 1 (sort_order and is_default set here)
color,fr,Rouge,#FF0000,1,1      ← translation for "fr" store
color,en,Red,#FF0000,1,1        ← translation for "en" store
color,default,Blue,#0000FF,2,0  ← start of group 2
color,fr,Bleu,#0000FF,2,0
color,en,Blue,#0000FF,2,0
```

---

## Validation Rules

The **Check Data** button validates the file before any data is written:

| Rule | Severity |
|---|---|
| Column count must match expected layout | Error — blocks import |
| Column names must match expected names | Error — blocks import |
| `attribute_code` must match selected attribute on every row | Error — blocks import |
| `store_view`, `value` must not be empty | Error — blocks import |
| First row of each option group must be a `default`/`admin` store row | Error — blocks import |
| `sort_order` must be a number | Error — blocks import |
| `is_default` must be `0` or `1` | Error — blocks import |
| Only one option may have `is_default=1` | Error — blocks import |
| No duplicate values within the same `default`/`admin` store in the CSV | Error — blocks import |
| No duplicate store codes within the same option group | Error — blocks import |
| Non-existent store codes | Error — blocks import |
| Option value already exists in the database | Warning — logs and skips |

---

## Duplicate Handling

If an option value already exists in the database for the selected attribute, the module **skips it silently** (logs a warning) instead of overwriting it. This is intentional — it protects options that have been manually adjusted by an admin.

Skipped values appear in the import result message and in the log file.

---

## Logging

Every import action is logged to:

```
var/log/attribute_import.log
```

Each entry includes a timestamp, log level, and a message. Entries are visible from **Stores → Attributes → Import Attributes → View Log** without needing server access.

Log levels used:

| Level | When |
|---|---|
| INFO | Import started, import completed with summary |
| WARNING | Option skipped because it already exists |
| ERROR | Validation failure, unexpected exception |

---

## Architecture Summary

```
CSV upload
    │
    ▼
StreamingReader        ← fgetcsv generator — O(1) memory per row
    │
    ▼
Validator              ← stateless, returns error list — no DB writes
    │
    ▼  (only if valid)
ImportService          ← groups rows by option, pre-loads existing options once
    │
    ▼
OptionProcessor        ← bulk DB writes: insertMultiple for labels, insertOnDuplicate for swatches
    │
    ▼
CacheManager           ← clears eav + full_page caches
    │
    ▼
Logger                 ← writes to var/log/attribute_import.log
```

---

## Running Unit Tests

Tests are written for PHPUnit 10 and require no Magento bootstrap — they use mocks only.

```bash
# From within the Magento project (where vendor/phpunit/phpunit is installed):
docker compose exec maintenance bash -c \
  "cd /var/www/html && vendor/bin/phpunit app/code/Aichouchm/AttributeImport/Test/Unit"

# Or directly if phpunit is in PATH:
phpunit --testdox Test/Unit
```

---

## ACL / Permissions

The module registers one ACL resource:

```
Magento_Backend::stores
  └── Magento_Backend::stores_attributes
        └── Aichouchm_AttributeImport::import_attributes   ← "Import Attributes"
```

Assign this resource to any admin role that needs access to the import page.

---

## Supported Attribute Types

| Frontend Input | Supported |
|---|---|
| `select` | Yes |
| `multiselect` | Yes |
| `swatch_visual` | Yes (hex + image URL) |
| `swatch_text` | Yes |
| `boolean`, `date`, `text`, etc. | No — these have no options |

System attributes (`is_user_defined = false`) are excluded from the attribute selector to prevent accidental modification of core Magento configuration.

---

## Compatibility

- Tested with Magento 2.4.6 and 2.4.7
- Compatible with Varnish full-page caching (module clears `eav` and `full_page` cache tags after import)
- Compatible with Redis page cache

---

## License

MIT — see [LICENSE](LICENSE) file.
