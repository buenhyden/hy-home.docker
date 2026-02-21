---
trigger: model_decision
glob: ["**/*.{json,po,mo,xliff}"]
description: "Localization (i18n/l10n) Pillar: Enforces translation keys, ICU message formats, and world-ready UI standards."
---

# Localization Pillar

- **Role**: Localization Engineer
- **Purpose**: Ensure products are world-ready (internationalization) and accurately translated (localization).
- **Activates When**: Adding UI text, formatting dates, or implementing multi-region support.

**Trigger**: model_decision — Apply during UI development and content internationalization.

## 1. Standards

### Principles

- **[REQ-LOC-01] Key-Based Translation**
  - UI text MUST utilize translation keys instead of raw, hardcoded strings.
- **[REQ-LOC-02] Contextual Extraction**
  - Translation keys MUST be descriptive and include semantic context for translators.
- **[REQ-LOC-03] Regional Formatting**
  - Dates, currencies, and numbers MUST be formatted using locale-aware libraries (e.g., `Intl` API).

### Supported Formats

| Industry Standard | File Extension | Recommendation |
| --- | --- | --- |
| JSON i18next | `.json` | Common for Web |
| Gettext | `.po` / `.mo` | Common for Systems/Python |
| XLIFF | `.xliff` | Universal Exchange |

### Must

- **[REQ-LOC-04] ICU Message Format**
  - Use ICU formats for complex strings involving plurals, genders, or variable injection.
- **[REQ-LOC-05] RTL Support Readiness**
  - UI layouts MUST be designed with Right-to-Left (RTL) compatibility in mind.
- **[REQ-LOC-06] Dynamic Key Auditing**
  - All dynamically generated keys MUST be documented to ensure successful extraction by scanners.

### Must Not

- **[BAN-LOC-01] UI Hardcoding**
  - End-user facing strings MUST NOT be hardcoded in the primary source code.
- **[BAN-LOC-02] Brute-Force Concatenation**
  - Sentences MUST NOT be constructed by concatenating isolated translation keys (breaks linguistic flow).

### Failure Handling

- **Stop Condition**: Stop the build if missing translation keys are detected for required languages.

## 2. Procedures

- **[PROC-LOC-01] Extraction Workflow**
  - IF adding new UI components THEN MUST run the localization scanner to extract new keys.
- **[PROC-LOC-02] Sync Synchronization**
  - Maintain a weekly sync between the source repository and the Translation Management System (TMS).

## 3. Examples

### ICU Plurals (Good)

```json
{
  "cart_items": "{count, plural, =0 {No items} one {1 item} other {# items}}"
}
```

## 4. Validation Criteria

- **[VAL-LOC-01] Key Coverage**
  - [ ] 100% of UI strings are associated with a key in the primary localization file.
- **[VAL-LOC-02] Formatting Accuracy**
  - [ ] Currencies display correct symbols and decimal separators for at least 3 target regions.
- **[VAL-LOC-03] Layout Integrity**
  - [ ] UI remains stable when switched to high-expansion languages (e.g., German).
