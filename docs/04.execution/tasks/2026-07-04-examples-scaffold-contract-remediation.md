---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-07-04-examples-scaffold-contract-remediation.md -->

# Task: Examples Scaffold Contract Remediation

## Overview

This task records the approved follow-up for `WDC-GAP-017`. It brings the
copyable example scaffold documents under `examples/sample-web-service/` back
in line with the current README and service scaffold contracts without changing
runtime behavior.

## Inputs

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/document-contracts/gap-register.md)
- **README Template**: [README template](../../99.templates/templates/common/readme.template.md)
- **Service Template**: [Service scaffold template](../../99.templates/templates/spec-contracts/service.template.md)

## Working Rules

- Keep changes limited to example scaffold documentation and traceability
  evidence.
- Do not change `Dockerfile`, `docker-compose.yml`, `.env.example`,
  `nginx.conf`, static site files, or runtime behavior.
- Do not inspect or write secret values, credentials, tokens, private keys, raw
  logs, shell history, or `.env` values.
- Preserve the example as a copyable scaffold rather than converting it into a
  production service spec.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `examples/sample-web-service/README.md`; `examples/sample-web-service/service.md` | User continuation for the next follow-up and PLN-WDC-RM-003 examples approval gate | Example scaffold documentation profile and template links | The README had a scaffold-specific profile with no top lifecycle frontmatter, and both files linked to removed flat `docs/99.templates/service.template.md`. | The README now follows the common README profile while preserving scaffold-specific sections; both files carry `status: active` frontmatter and link to `docs/99.templates/templates/spec-contracts/service.template.md`. | `git revert` the examples scaffold remediation commit | No secret values, credentials, tokens, private keys, raw logs, shell history, `.env` values, runtime config changes, Compose changes, Dockerfile changes, nginx config changes, or static site changes |
| `docs/90.references/audits/document-contracts/gap-register.md`; `docs/90.references/audits/document-contracts/frontmatter-routing-profile.md`; `docs/04.execution/tasks/README.md`; `docs/00.agent-governance/memory/progress.md` | Documentation traceability requirements | Closure evidence for `WDC-GAP-017` | `WDC-GAP-017` was deferred as an examples/scaffold decision and the frontmatter routing profile listed examples as deferred. | The example scaffold decision is recorded as closed, while provider and infra follow-up rows remain separate. | `git revert` the examples scaffold remediation commit | Same redaction boundary as above |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Review current README, service, and template contracts for the sample scaffold. | doc | N/A | PLN-WDC-RM-003 | Template and audit source reads | Codex | Done |
| T-002 | Normalize example scaffold frontmatter, README profile, and service-template links. | doc | N/A | PLN-WDC-RM-003 | Example docs diff and stale-template search | Codex | Done |
| T-003 | Update gap register and frontmatter routing evidence for `WDC-GAP-017`. | doc | N/A | PLN-WDC-RM-008 follow-up | Register/profile references | Codex | Done |
| T-004 | Regenerate indexes and run documentation validation. | doc | N/A | VAL-WDC-RM-001 through VAL-WDC-RM-008 | Verification Summary | Codex | Done |

## Verification Summary

- **Test Commands**:
  - `rg -n 'docs/99\.templates/(readme|service)\.template' examples`
  - `git diff --check`
  - `bash scripts/knowledge/generate-llm-wiki-index.sh --check`
  - `bash scripts/operations/sync-provider-surfaces.sh --check`
  - `bash scripts/validation/check-doc-traceability.sh`
  - `bash scripts/validation/check-doc-implementation-alignment.sh`
  - `bash -n scripts/validation/check-repo-contracts.sh`
  - `bash scripts/validation/check-repo-contracts.sh`
- **Eval Commands**: N/A for documentation-only remediation.
- **Logs / Evidence Location**: This task document and the source
  `gap-register.md`.
- **Results**:
  - PASS: stale flat README/service template path scan returned no matches
    under `examples`.
  - PASS: generated `docs/90.references/llm-wiki/llm-wiki-index.md` with
    1129 paths.
  - PASS: provider surfaces have no drift.
  - PASS: doc traceability reports `failures=0`.
  - PASS: doc implementation alignment reports `failures=0`,
    `stage_docs_total=549`, and `removed_template_mentions_total=0`.
  - PASS: repo-contract shell syntax is valid.
  - Expected FAIL: full repo contracts report `failures=2`, confined to the
    known out-of-scope Keycloak hardening image mismatch and tech-stack
    expected-image drift. The changed document template gate reports
    `changed_template_docs_total=5`, `normalized_changed_template_docs_total=5`,
    and `legacy_changed_template_docs_skipped=0`.
- **Manual Checks**: Confirmed the diff does not change example runtime files,
  Compose declarations, Dockerfile content, nginx config, static site content,
  secret material, provider surfaces, remote GitHub state, or infra drift.
  Full repository contracts are expected to keep failing only on the existing
  out-of-scope infra drift until a separate infra task is approved.

## Related Documents

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/document-contracts/gap-register.md)
- **Frontmatter Routing Profile**: [Frontmatter routing profile](../../90.references/audits/document-contracts/frontmatter-routing-profile.md)
- **Example README**: [sample-web-service README](../../../examples/sample-web-service/README.md)
- **Example Service Scaffold**: [sample-web-service service scaffold](../../../examples/sample-web-service/service.md)
