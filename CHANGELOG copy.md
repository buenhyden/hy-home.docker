# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-02-20

### Added

- Prototype/Fast-Track mode rules and workflow (`workflow-fast-prototype.md`) for rapid scripting and validation.
- Automated directory pruning step in project initialization (`workflow-project-init.md`).
- GitHub Actions workflows for security scanning (`security-scan.yml`) and application verification (`verify-application.yml`).
- Explicit runbook creation instructions in `OPERATIONS.md`.
- New API specification template (`api-spec-template.md`).

### Changed

- Standardized documentation and template paths across all AI rules and workflows.
- Reorganized `templates/` into specific subdirectories (e.g., `product/`, `architecture/`, `engineering/`) for better isolation.
- Refined workspace architecture rules to enforce strict directory separation (`web/`, `app/`, `server/`).
- Added framework agnosticism guardrails to `llms.txt`.
