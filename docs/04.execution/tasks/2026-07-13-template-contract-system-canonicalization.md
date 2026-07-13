---
status: active
artifact_id: task:2026-07-13-template-contract-system-canonicalization
artifact_type: task
parent_ids:
  - plan:2026-07-13-template-contract-system-canonicalization
---

<!-- Target: docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md -->

# Template Contract System Canonicalization Execution Task

## Overview

This Task is the durable execution and review ledger for Spec 130 and its
implementation Plan. It covers Stage 99 registry, support, and copyable forms;
direct Stage 00 and validator fallout; preservation-oriented migration of the
typed baseline; generated evidence; and bounded routing for later corpus
waves.

The work runs serially in the isolated
`codex/template-contract-system-canonicalization` branch. Each of the seven
implementation units receives a fresh implementer, a separate specification
review, and a separate quality review before its logical commit.

## Inputs

- **Approved Spec**:
  [Spec 130](../../03.specs/130-template-contract-system-canonicalization/spec.md)
- **Active Plan**:
  [Implementation Plan](../plans/2026-07-13-template-contract-system-canonicalization.md)
- **Parent foundation**:
  [Spec 129](../../03.specs/129-document-contract-canonicalization/spec.md)
- **Canonical audit**:
  [2026-07-05 implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Machine registry**:
  [document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- **Current contracts**:
  [Stage 99 support](../../99.templates/support/README.md)
- **User approvals**:
  destructive Stage 99 contract and governance changes, protected-surface
  fallout, logical commits, staged direct-consumer migration, and
  Subagent-Driven execution were explicitly approved in this task.

## Working Rules

- Follow Spec 130 and the active Plan exactly.
- Run Tasks T-TCS-001 through T-TCS-007 serially.
- Use a fresh implementation agent for each task.
- Run specification review before quality review.
- Resolve all Critical and Important findings before task commit.
- Record Minor findings and their disposition.
- Preserve completed and superseded evidence bodies.
- Do not infer review dates, parents, approvals, incidents, postmortems,
  releases, tests, or runtime truth.
- Keep one machine registry and one canonical owner per rule or form.
- Do not run `pre-commit run --all-files` directly.
- Use the controlled wrapper only from a clean committed worktree after the
  whole-branch review.
- Run `graphify update .` after code changes when available and treat the
  report as advisory.

## Approved Surface Evidence

| Surface | Approval and boundary | Allowed action | Forbidden action | Evidence |
| --- | --- | --- | --- | --- |
| `docs/99.templates/` | Explicit user scope and destructive-change approval | Reorganize contracts, registry, catalogs, and forms; add Audit; delete duplicate forms | Create a second registry or leave two canonical owners | Spec 130 and Plan |
| Stage 00 documentation | Direct governance and reference fallout approved | Update authoring, stage, checklist, Memory, and Progress routes | Add provider-local policy or runtime state | Per-task diff and reviews |
| `scripts/validation/` and `tests/validation/` | Validator implementation required by Spec | TDD changes to metadata and repository gates | Add an unrelated checker or expose raw bodies in diagnostics | RED/GREEN output |
| Typed baseline | Preservation-oriented direct migration approved | Remove template residue and normalize semantically equivalent headings | Rewrite historical commands, counts, verdicts, or decisions | Task 7 disposition |
| Canonical generated evidence | Generator-only update approved | Run named owner scripts and commit deterministic outputs | Hand-edit generated bodies | Generator output and check mode |
| `.github/workflows/ci-quality.yml` | Conditional only | Modify only if a RED integration test proves named routing is missing | Change remote settings or broaden CI without a failing contract | RED test and separate review |
| Runtime and external state | Not in scope | Read tracked documentation required for evidence | Mutate Compose, containers, secrets, deployment, remote GitHub, or global provider state | Whole-branch scope review |

## Task Table

| ID | Deliverable | Dependency | Status | Implementation role | Required review |
| --- | --- | --- | --- | --- | --- |
| T-TCS-001 | Registry and support contract canonicalization | Spec and Plan | In Review | fresh implementer | spec then quality |
| T-TCS-002 | Common, README, and Governance forms | T-TCS-001 | Queued | fresh implementer | spec then quality |
| T-TCS-003 | Stage 01-03 and Spec-child forms | T-TCS-001 | Queued | fresh implementer | spec then quality |
| T-TCS-004 | Stage 04 Plan and Task system | T-TCS-001 through 003 | Queued | fresh implementer | spec then quality |
| T-TCS-005 | Stage 05 Operations forms | T-TCS-001 | Queued | fresh implementer | spec then quality |
| T-TCS-006 | Executable template and target validation | T-TCS-001 through 005 | Queued | fresh implementer | spec then quality |
| T-TCS-007 | Direct consumers, generated evidence, and wave routing | T-TCS-001 through 006 | Queued | fresh implementer | spec then quality |

## T-TCS-001 Implementation Evidence

- Replaced the flat typed-template mapping with 23 exact roles that own unique
  sources, target profiles, target globs, and non-overlapping heading envelopes.
- Added deterministic role matching and fail-closed classification, including
  exact Spec-child paths, README profile delegation, Memory/Progress
  specificity, and generated inventory exclusion.
- Added exact-key, known-profile, safe-path/glob, unique-source, heading, and
  repository source-existence validation. Typed sources retain target-profile
  placeholder checks; README, governance, and Archive keep their distinct
  source/target metadata boundaries.
- Reconciled the ten named human support owners and verified the external
  rationale against official or primary sources on 2026-07-13 without claiming
  that local roles or metadata are international standards.
- Controller-approved dependency correction: Task 1 created the minimal Audit
  source needed by repository-contract existence checks. Its Target and
  target-relative comments are a temporary legacy-shell compatibility exception;
  Task 2 owns final form-only normalization and Task 6 owns removal of the old
  shell requirement.
- Adding the tracked Audit path caused ordinary generated freshness fallout.
  The LLM Wiki index, coverage snapshot, and metadata inventory were refreshed
  only through their canonical generators; Task 7 still owns the final
  branch-wide refresh and disposition.

## Review Evidence

| Task | Spec review | Quality review | Findings | Disposition |
| --- | --- | --- | --- | --- |
| T-TCS-001 | Not run — implementation complete and awaiting independent review | Not run — implementation complete and awaiting independent review | No independent findings recorded | In Review; implementer self-review complete |
| T-TCS-002 | Not run — dependency is queued | Not run — dependency is queued | None recorded | Await T-TCS-001 |
| T-TCS-003 | Not run — dependency is queued | Not run — dependency is queued | None recorded | Await T-TCS-001 |
| T-TCS-004 | Not run — dependencies are queued | Not run — dependencies are queued | None recorded | Await T-TCS-001 through 003 |
| T-TCS-005 | Not run — dependency is queued | Not run — dependency is queued | None recorded | Await T-TCS-001 |
| T-TCS-006 | Not run — dependencies are queued | Not run — dependencies are queued | None recorded | Await T-TCS-001 through 005 |
| T-TCS-007 | Not run — dependencies are queued | Not run — dependencies are queued | None recorded | Await T-TCS-001 through 006 |
| Whole branch | Not run — implementation has not completed | Not run — implementation has not completed | None recorded | Await T-TCS-007 |

## Verification Summary

### Planning baseline

| Command | Result | Meaning |
| --- | --- | --- |
| Metadata changed-mode for Spec and Plan | Pass, zero violations | Typed identity, parent, and lifecycle transition are valid |
| Repository contract check | Pass | Current repository contracts remain green before implementation |
| Document traceability check | Pass | Current Stage 04/05 catalogs remain synchronized |
| Documentation implementation alignment | Pass | Current docs and tracked implementation agree within the existing gate |
| LLM Wiki index and coverage check | Pass after generator refresh | Generated knowledge evidence includes the active Plan |
| `git diff --check` | Pass | No whitespace error in the planning commit |

### Required implementation checks

- Focused RED and GREEN tests named by each Plan task.
- Full `tests.validation.test_document_metadata` suite.
- Metadata `check-contracts`, `check-changed`, and applicable active reporting.
- Repository contracts, document traceability, and implementation alignment.
- YAML and machine-template fixture validation.
- Reference searches after every deletion.
- LLM Wiki and metadata inventory generator and check modes.
- Graphify refresh and advisory report corroboration after code changes.
- Final whole-branch specification and quality review.
- Controlled all-files pre-commit wrapper from a clean commit.

### T-TCS-001 RED and GREEN

| Phase | Command | Result |
| --- | --- | --- |
| RED | `python3 -m unittest tests.validation.test_document_metadata.ProfileSchemaTests tests.validation.test_document_metadata.TemplateRoleInferenceTests -v` | Expected failure: 10 tests ran with 26 errors because `template_roles` and `classify_template_role()` did not exist. |
| GREEN | Same focused command | Pass: 10/10. |
| Regression | `python3 -m unittest tests.validation.test_document_metadata -v` | Pass: 109/109. |
| Metadata contracts | `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | Pass: zero violations. |
| Repository contracts | `bash scripts/validation/check-repo-contracts.sh` | Pass: `failures=0`. |
| Generated freshness | Canonical LLM Wiki index/coverage generators and metadata inventory report mode | Pass: 1,298 index paths, 1,297 safe coverage paths, and 903 metadata records / 2,033 advisory findings. |
| Graph refresh | `graphify update .` | Pass: refreshed to 23,053 nodes / 24,116 edges / 1,540 communities; outputs restored after evidence capture to keep this logical commit scoped, and conclusions were corroborated against tracked source, Stage 00, Spec 130, and this Plan/Task. |
| Diff hygiene | `git diff --check` and Python compilation | Pass. |

## Controlled Agent Pre-commit Evidence

The final wrapper has not run because implementation and whole-branch review
have not completed.

| Field | Current value |
| --- | --- |
| Planned entrypoint | `scripts/validation/run-agent-precommit-all-files.sh` |
| Direct pre-commit invocation | Prohibited |
| Planned prefixes | `docs/`, `scripts/validation/`, `tests/validation/` |
| Preconditions | Clean committed worktree; all task reviews and full validation pass |
| Hook result | Not run |
| Snapshot result | Not run |
| Unexpected paths | Not observed because the wrapper has not run |

## Commit Ledger

| Commit | Logical unit | Validation |
| --- | --- | --- |
| `ff26fd6b` | Approved Spec 130 and generated design evidence | Metadata, repository contracts, traceability, generated freshness, diff |
| `10fe2f9d` | Active Stage 04 Plan and generated planning evidence | Metadata changed-mode, repository contracts, traceability, alignment, generated freshness, diff |

Implementation and review-fix commits will be appended after each task closes.

## Migration Wave Routing

| Wave | Scope | Entry gate | Exit evidence | This branch |
| --- | ---: | --- | --- | --- |
| A | 89 active PRD, ARD, ADR, Spec, and Plan documents | New approved Spec and Plan; parent graph established | Chain-level metadata, body, link, review, and validation evidence | Route only |
| B | 66 Guides, 64 Policies, and 61 Runbooks | New approved Spec and Plan; real review evidence available | Domain-level review, operations links, metadata, and validation evidence | Route only |
| C | 229 completed and one superseded document | New approved preservation Plan | Minimum metadata and link repair with unchanged historical body evidence | Route only |
| D | Five Archive tombstones | Proven origin, reason, date, and replacement | Complete provenance and link validation | Route only |
| E | Six generated documents | Canonical generator identified | Generator output and check mode agree | Route only |

## Deferred and Blocked Items

- Waves A through E are intentionally deferred to independent approved Specs
  and Plans.
- Corpus-wide blocking is deferred until all approved migration waves finish.
- Runtime Compose, infrastructure, security, and deployment remediation stays
  in Specs 124 through 127.
- Remote GitHub enforcement remains outside this branch.
- No implementation blocker is present at Task initialization.

## Related Documents

- [Spec 130](../../03.specs/130-template-contract-system-canonicalization/spec.md)
- [Implementation Plan](../plans/2026-07-13-template-contract-system-canonicalization.md)
- [Stage 99 template system](../../99.templates/README.md)
- [Template support](../../99.templates/support/README.md)
- [Metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Progress log](../../00.agent-governance/memory/progress.md)
