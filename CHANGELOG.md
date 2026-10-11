# Changelog

## 1.1.0

### Security
- Server-side attribute allow-list: the posted `attribute_code` must be a user-defined
  `select`/`multiselect` product attribute. Previously only the dropdown filtered it, so a
  crafted request could write options into system attributes such as `status`.
- Unexpected errors are no longer returned to the browser (they could expose file paths or
  SQL errors); they are logged and replaced by a generic message.
- Option values containing HTML tags or line breaks/control characters are rejected. Line
  breaks could be used to forge entries in `attribute_import.log`.
- Admin UI moved to a RequireJS component with no inline event handlers (CSP-friendly);
  URLs are passed as JSON instead of being interpolated into JavaScript.
- Index and Log controllers accept GET only; the Import button is truly disabled until the
  file passes validation, and both actions are locked while a request runs (no double import).

### Fixed
- Text swatch attributes (e.g. `size`) now get a swatch value for every store label.
- Existing options are matched case-insensitively, like the database collation, so `red`
  no longer creates a near-duplicate of `Red`.
- CSV files saved by Excel with a UTF-8 BOM are accepted.
- Blank lines in the CSV no longer trigger a `trim(null)` deprecation.
- Row limit off-by-one; `sort_order` must now be a whole number.

### Changed
- The log viewer reads only the last 256 KB of the log instead of the whole file.
- Upload checks moved to `Model\Upload\CsvUploadValidator`; attribute rules to
  `Model\Attribute\AttributeGuard`.
- `StreamingReader` uses Magento's filesystem driver instead of `@fopen`.
- Templates use `$escaper`; inline styles moved to `styles.css`.
- Attribute source implements `OptionSourceInterface` (replaces deprecated `ArrayInterface`).
- Code passes the Magento2 coding standard with no errors or warnings (was 1 error, 158 warnings).

### Added
- Unit tests for the validator, CSV reader and attribute guard (PHPUnit 10–12).

## 1.0.0

- Logger writes only to `var/log/attribute_import.log`.
- README install command fixed for Packagist.
