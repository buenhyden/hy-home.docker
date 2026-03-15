# Documentation Maintenance Runbook

- **Tier**: L1 (Local Dev)
- **layer:** ops

**Overview (KR):** 리포지토리의 문서 품질과 구조를 일관되게 유지하기 위한 운영 절차입니다.

## Context

Maintaining a flat documentation taxonomy requires manual checks and automated validation during the refactor phase.

## Procedures

### 1. Audit Entry Points

- Verify `AGENTS.md` points to the correctly pluralized paths.
- Ensure `gateway.md` triggers are up to date.

### 2. Metadata Check

- Run the following command to find files missing `layer` metadata:

  ```bash
  find docs -name "*.md" -exec grep -L "layer:" {} +
  ```

## Verification

- `[VAL-RBK-001]` No files missing `layer:` metadata.
- `[VAL-RBK-002]` All links in `README.md` are pluralized.
