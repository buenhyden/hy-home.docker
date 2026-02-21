---
trigger: always_on
glob: ["**/*.{txt,csv,log}", "**/.env.example"]
description: "Special Miscellaneous Standards: Enforces readability and secret prevention for non-code assets like logs and environment templates."
---

# Special Miscellaneous Standard

- **Role**: General Engineering Generalist
- **Purpose**: Define standards for miscellaneous file types not covered by specific technical domains, ensuring baseline quality and security.
- **Activates When**: Creating or editing plain text files, CSV datasets, logs, or environment variable examples.

**Trigger**: always_on — Apply during the maintenance of miscellaneous project assets.

## 1. Standards

### Principles

- **[REQ-MISC-01] Structural Clarity**
  - Even non-code assets MUST be readable, consistently formatted, and logically structured to ensure discoverability.
- **[REQ-MISC-02] Leak Prevention**
  - Miscellaneous assets MUST NOT contain PII, credentials, or internal implementation secrets.

### Asset Baseline

| File Type | Requirement ID | Critical Requirement |
| --- | --- | --- |
| .env.example | [REQ-MISC-03] | Mandatory for all env-driven projects |
| .csv | [REQ-MISC-04] | UTF-8 encoding with standard headers |
| .log | [REQ-MISC-05] | Rotation-aware and PII-redacted |

### Must

- **[REQ-MISC-06] Empty Env Templates**
  - `.env.example` files MUST include all required keys but NO real values. Use dummy placeholders (e.g., `YOUR_API_KEY`).
- **[REQ-MISC-07] Log Anonymization**
  - Production log files MUST NOT contain unmasked personally identifiable information (PII) or authentication tokens.
- **[REQ-MISC-08] Explicit Key Documentation**
  - Environment variable keys in `.env.example` SHOULD include comments explaining their purpose and source.

### Must Not

- **[BAN-MISC-01] Binary Blobs in Main**
  - Avoid committing large binary files to the main repository; utilize Git LFS or external artifact storage.
- **[BAN-MISC-02] Placeholder Values in Main**
  - Do NOT commit `.env.example` files that contain "dummy" values that are actually valid test credentials.

### Failure Handling

- **Stop Condition**: Stop commit if a `.txt` or `.log` file is identified to contain clear-text credentials.

## 2. Procedures

- **[PROC-MISC-01] Env Sync Workflow**
  - IF adding a new secret key to the application THEN MUST update the `.env.example` template in the same PR.
- **[PROC-MISC-02] Encoding Audit**
  - Verify that all text-based data files utilize UTF-8 encoding to prevent cross-platform character corruption.

## 3. Examples

### Secure .env.example (Good)

```bash
# Database connection for development
DB_USER=test_user
DB_PASS= # Set your password
```

## 4. Validation Criteria

- **[VAL-MISC-01] Secret Cleanliness**
  - [ ] Automated scans verify zero real secrets in the `.env.example` file.
- **[VAL-MISC-02] Format Adherence**
  - [ ] CSV and logs pass standard parsing checks without encoding errors.
- **[VAL-MISC-03] Key Sufficiency**
  - [ ] Every key required by the application is represented in the `.env.example` file.
