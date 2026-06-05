---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-06-03-governance-surgical-reverification.md -->

# Task: Governance Surgical Re-Verification + Tech-Stack Drift Closure

## Overview

This document is the execution and verification audit trail for surgical
reverification of shared governance and the Claude harness, plus closure and
recurrence-prevention automation for Dependabot-driven tech-stack version drift
found during that work. This is cross-cutting governance work, so it references
governance documents instead of a parent Spec
(`documentation-protocol.md` §8.5).

## Inputs

- **Parent Plan**: [Governance Surgical Re-Verification Plan](../plans/2026-06-03-governance-surgical-reverification.md)
- **Governance Scope**: [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)

## Working Rules

- This is documentation/verification/script work, and every task leaves verification evidence.
- Do not store raw logs, secret values, or shell history.
- Do not bulk-edit read-only stage documents; record gaps in governance memory.
- Do not bypass security/CI governance contracts; when conflicts arise, decide direction through user approval.

## Approved Surface Evidence

| Surface             | Approval Source                        | Target                                          | Before Evidence                                    | After Evidence                                              | Rollback / Recovery        | Redaction Boundary         |
| ------------------- | -------------------------------------- | ----------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------- | -------------------------- | -------------------------- |
| Infra registry data | User approval for "versions.json sync" | `infra/tech-stack.versions.json` | 9 component tags stale (mismatch with Dependabot bumps) | Matches compose declarations, `check-repo-contracts.sh failures=0` | `git revert` / rerun `sync` | No secrets, image tags only |
| CI workflow | User approval for "read-only drift gate" | `.github/workflows/tech-stack-version-sync.yml` | None | `contents: read` drift gate (auto-commit not adopted) | Delete workflow file | No secrets |
| Contract validator | Script registration required (usage contract) | `scripts/validation/check-repo-contracts.sh` | New script absent from `expected_implementations` | New script registered, `failures=0` | Remove registration line | None |

## Task Table

| Task ID | Description                              | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence                                                                                                    | Owner | Status |
| ------- | ---------------------------------------- | ---- | --------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------ | ----- | ------ |
| T-001   | Rerun governance-scope QA/CI gates | ops | N/A (cross-cutting) | PLN-001 | repo-contracts/traceability/impl-alignment/compose/hardening/quickwin/template-security/wiki all `failures=0`/PASS | hy | Done |
| T-002   | Reverify model freshness on the web + cross-check repository | doc | N/A | PLN-002 | Claude `opus-4.8`/`sonnet-4.6` current; `gemini-3.5-pro` not GA; `.claude/agents` 1 opus + 14 sonnet; 0 stale models | hy | Done |
| T-003   | Synchronize tech-stack drift | impl | N/A | PLN-003 | `infra/tech-stack.versions.json` 9 tags match compose; `check-repo-contracts.sh failures=0` | hy | Done |
| T-004   | Record Gemini tier memory reverification | doc | N/A | PLN-004 | Added 2026-06-03 reverification section to `memory/2026-05-31-gemini-model-tier-review.md` | hy | Done |
| T-005   | Write tech-stack sync script | impl | N/A | PLN-006 | `scripts/operations/sync-tech-stack-versions.sh` (`--check`/`--dry-run`/write); injected-drift detect/fix positive test passed | hy | Done |
| T-006   | Register script governance | impl | N/A | PLN-006 | `check-repo-contracts.sh` allowlist + 3 `scripts/README.md` table registrations; usage contract PASS | hy | Done |
| T-007   | Add read-only CI drift gate | impl | N/A | PLN-007 | `.github/workflows/tech-stack-version-sync.yml` runs `sync --check` with `contents: read`; workflow security contract PASS | hy | Done |
| T-008   | Write trace evidence | doc | N/A | PLN-005 | Updated plan, task, two README indexes, and progress row | hy | Done |

## Suggested Types

- `impl`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-001 Rerun governance gates
- [x] T-002 Reverify web models

### Phase 2

- [x] T-003 Synchronize drift
- [x] T-004 Record Gemini tier memory
- [x] T-005 Write sync script
- [x] T-006 Register script governance
- [x] T-007 Add read-only CI drift gate
- [x] T-008 Write trace evidence

## Verification Summary

- **Test Commands**: `bash scripts/operations/sync-tech-stack-versions.sh --check` -> in sync; injected-drift positive test (detect rc=1 -> write fix -> reverify in sync).
- **Eval Commands**: `bash scripts/validation/check-repo-contracts.sh` -> `failures=0`; `check-doc-traceability.sh` -> `failures=0` (`catalog_pairs_total=46`); `check-doc-implementation-alignment.sh` -> `failures=0`; `validate-docker-compose.sh`/`check-all-hardening.sh`/quickwin/template-security -> PASS; LLM Wiki freshness PASS; `git diff --check` -> no results.
- **Logs / Evidence Location**: This document's Task Table and the latest row in `docs/00.agent-governance/memory/progress.md`.

### Deviation Notes

- The original request assumed a greenfield 3-phase governance build, but governance was already mature and consistent, so user approval limited scope to "surgical reverification + gap closure + recurrence-prevention automation."
- Gemini tier inversion was recorded only as a memory decision item with no policy change because `gemini-3.5-pro` was not GA.
- The root cause of tech-stack drift was Dependabot automatic bumps. Based on user choice, this was implemented as a **read-only drift gate + one-command sync script** instead of CI **auto-commit**. Reason: repository security governance hard-prohibits workflow `contents: write` (`check-repo-contracts.sh` GitHub workflow security contracts). The security contract was not bypassed.

## Related Documents

- **Parent Plan**: [Governance Surgical Re-Verification Plan](../plans/2026-06-03-governance-surgical-reverification.md)
- **Governance (Model Policy SSOT)**: [subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Gemini Model Tier Review (memory)**: [2026-05-31-gemini-model-tier-review.md](../../00.agent-governance/memory/2026-05-31-gemini-model-tier-review.md)
- **Progress Log**: [progress.md](../../00.agent-governance/memory/progress.md)
