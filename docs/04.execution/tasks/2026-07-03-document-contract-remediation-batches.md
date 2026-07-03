---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md -->

# Task: Document Contract Remediation Batches

## Overview

This task records execution evidence for the document-contract remediation
batches that follow the completed workspace document contract audit pack. The
first work unit creates this evidence file, confirms the current
`WDC-GAP-*` baseline, and preserves protected boundaries before any target
corpus remediation begins.

## Inputs

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/document-contracts/gap-register.md)
- **Audit Pack Task**: [Workspace document contract audit pack task](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Template Contract**: [Template contract](../../99.templates/support/template-contract.md)
- **Frontmatter Contract**: [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- **Stage Authoring Matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Working Rules

- Execute one remediation batch at a time.
- Do not apply target corpus fixes without the matching batch approval.
- Keep provider, workflow, validator, secret-handling, infra, and target-stage
  edits in separate logical commits.
- Treat Stage 00 governance and Stage 99 template contracts as the source of
  truth; provider files are adapters, not owners.
- Do not inspect secret values, credentials, tokens, certificates, private
  keys, raw logs, shell history, or `.env` values.
- Keep existing infra image/version drift out of documentation batches unless
  an infra-specific task is approved.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` | Approved remediation batch plan and user continuation | Execution evidence | File absent | Task evidence records baseline and future batch status | `git revert` this task-evidence commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `docs/04.execution/tasks/README.md` | Task-stage routing contract | Task index | Remediation batch task not listed | Active task linked in structure and related documents | `git revert` this task-evidence commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `projects/README.md`; `projects/storybook/README.md`; `projects/storybook/nextjs/README.md` | PLN-WDC-RM-003 and user continuation for the next approved batch | Project README profile and template-link cleanup | Project READMEs used `Related References`, removed flat README template links, and `projects/README.md` still named obsolete operations-stage paths. | Project READMEs use `Related Documents`, canonical common README template links, and current Stage 03/04/05 taxonomy wording. | `git revert` the T-003 README batch commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `secrets/README.md` | PLN-WDC-RM-003 secret README approval with redaction boundary | Secret README profile and template-link cleanup | Secret README used `Related References`, duplicated the operations README link, and linked a removed flat README template path. | Secret README uses `Related Documents`, one operations README link, and the canonical common README template link. | `git revert` the T-003 README batch commit | Read only `secrets/README.md`; do not inspect secret value files, credentials, tokens, private keys, certificates, raw logs, shell history, or `.env` values |
| `tests/README.md` | PLN-WDC-RM-003 and user continuation for the next approved batch | Tests README profile cleanup | Tests README used `Related References`. | Tests README uses `Related Documents`. | `git revert` the T-003 README batch commit | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| Future protected surfaces | Parent plan approval gates | Provider, workflow, validator, secret-handling, infra, and target-stage changes | No remediation applied in T-001 | Future tasks must record per-batch evidence before edits | Revert the specific future batch commit | Redaction boundary must be restated in each future batch before touching protected surfaces |

## Task Table

| Task ID | Description | Type | Parent Plan / Phase | Source Gaps | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create task evidence and confirm current gap-register baseline. | doc | PLN-WDC-RM-001 | All rows | Baseline counts and validation matrix | Codex | Done |
| T-002 | Fix active governance and provider adapter drift. | doc | PLN-WDC-RM-002 | WDC-GAP-001, WDC-GAP-002, WDC-GAP-022 | Provider sync and repo contracts | Codex | Done |
| T-003 | Normalize README profiles by surface. | doc | PLN-WDC-RM-003 | WDC-GAP-003, WDC-GAP-004, WDC-GAP-005, WDC-GAP-017, WDC-GAP-019 | README/template drift checks | Codex | Done |
| T-004 | Normalize target-stage frontmatter and section profiles. | doc | PLN-WDC-RM-004 | WDC-GAP-006, WDC-GAP-007, WDC-GAP-008, WDC-GAP-009, WDC-GAP-016 | Inventory rerun and profile exceptions | Codex | Planned |
| T-005 | Decide CI/CD, QA, parser, and Graphify enforcement. | doc/script | PLN-WDC-RM-005 | WDC-GAP-010, WDC-GAP-011, WDC-GAP-018 | Protected-surface checks | Codex | Planned |
| T-006 | Preserve or reclassify historical evidence rows. | doc | PLN-WDC-RM-006 | WDC-GAP-012, WDC-GAP-013, WDC-GAP-014, WDC-GAP-015 | Historical evidence review | Codex | Planned |
| T-007 | Execute infra drift only as a separate infra task if approved. | ops | PLN-WDC-RM-007 | WDC-GAP-020, WDC-GAP-021 | Infra-only validation | Codex | Deferred |
| T-008 | Close batch evidence, update register dispositions, regenerate indexes, and commit. | doc | PLN-WDC-RM-008 | All touched rows | Final validation matrix and commit trail | Codex | Planned |

## Baseline Snapshot

| Measure | Command | Result |
| --- | --- | ---: |
| Total `WDC-GAP-*` rows | `rg '^\| WDC-GAP-[0-9]{3} ' docs/90.references/audits/document-contracts/gap-register.md \| wc -l` | 30 |
| `direct-fix` rows | Row count filtered by disposition `direct-fix`. | 0 |
| `batch-fix` rows | Row count filtered by disposition `batch-fix`. | 11 |
| `historical-evidence` rows | Row count filtered by disposition `historical-evidence`. | 4 |
| `out-of-scope-gap` rows | Row count filtered by disposition `out-of-scope-gap`. | 7 |
| `no-action` rows | Row count filtered by disposition `no-action`. | 8 |

## Batch Status

| Batch | Source Rows | Current Status | Boundary |
| --- | --- | --- | --- |
| Governance and provider adapter drift | WDC-GAP-001, WDC-GAP-002, WDC-GAP-022 | Local adapter drift done; remote evidence deferred | WDC-GAP-001 and WDC-GAP-002 were remediated by making Gemini, Claude, and generated Codex adapter text defer to Stage 00 owners. WDC-GAP-022 still requires separate remote GitHub re-verification approval. |
| README profile normalization | WDC-GAP-003, WDC-GAP-004, WDC-GAP-005, WDC-GAP-017, WDC-GAP-019 | Approved surfaces done; examples deferred | Projects, secrets, and tests README surfaces were remediated. `secrets/README.md` was handled as metadata-only documentation and no secret value files were inspected. WDC-GAP-017 remains deferred because `examples/**` needs a separate examples/scaffold contract decision. |
| Target-stage frontmatter and section profiles | WDC-GAP-006, WDC-GAP-007, WDC-GAP-008, WDC-GAP-009, WDC-GAP-016 | Planned | Requires stage/profile decisions before corpus edits. |
| CI/CD, QA, parser, and Graphify decisions | WDC-GAP-010, WDC-GAP-011, WDC-GAP-018 | Planned | Requires protected workflow, script, validator, or pre-commit approval before edits. |
| Historical evidence preservation or reclassification | WDC-GAP-012, WDC-GAP-013, WDC-GAP-014, WDC-GAP-015 | Planned | Preserve old truth unless active-consumption conflict is proven. |
| Infra drift follow-up | WDC-GAP-020, WDC-GAP-021 | Deferred | Requires separate infra task and runtime-change approval if Compose changes. |

## Validation Results

| Scope | Command | Result |
| --- | --- | --- |
| Gap baseline | Baseline `rg ... \| wc -l` commands listed in `## Baseline Snapshot` | PASS: register still has 30 rows with disposition distribution `0/11/4/7/8`. |
| Task path pre-check | `test -f docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md` before creation | PASS: command exited non-zero before creation, confirming the evidence file was new. |
| Target corpus boundary | Manual diff review | PASS: T-001 creates task evidence and task index only; no target corpus remediation is applied. |
| LLM Wiki regeneration | `bash scripts/knowledge/generate-llm-wiki-index.sh` | PASS: generated `docs/90.references/llm-wiki/llm-wiki-index.md` with 1125 paths after the T-003 README batch evidence update. |
| Whitespace | `git diff --check` | PASS: no whitespace errors. |
| LLM Wiki freshness | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS: generated LLM Wiki index is fresh. |
| Provider surfaces | `bash scripts/operations/sync-provider-surfaces.sh --check` | PASS: `sync-provider-surfaces: no drift`. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` | PASS: `failures=0`. |
| Implementation alignment | `bash scripts/validation/check-doc-implementation-alignment.sh` | PASS: `failures=0`. |
| Repo contract syntax | `bash -n scripts/validation/check-repo-contracts.sh` | PASS: shell syntax is valid. |
| Full repo contract | `bash scripts/validation/check-repo-contracts.sh` | Expected FAIL: `failures=2`; no task, plan, reference, provider, LLM Wiki, Stage 99, or document-contract remediation failures. Failures remain confined to known out-of-scope infra drift: the Keycloak hardening image mismatch and `infra/tech-stack.versions.json` expected-image drift. |
| Adapter wording drift | `rg -n 'gemini-3\.1-pro\|gemini-3\.5-flash\|DOCS 3 RULES\|R1\)\|R2\)\|R3\)\|docs/99\.templates/(readme\|service)\.template\|updated:' GEMINI.md .agents/rules/workspace.md .agents/workflows/documentation.md .claude/agents/doc-writer.md .claude/skills/ops-runbook-agent/skill.md .codex/skills/ops-runbook-agent/skill.md` | PASS: no matches in the remediated adapter surfaces. |
| Provider mirror generation | `bash scripts/operations/sync-provider-surfaces.sh --write` | PASS: regenerated generated Codex/Gemini provider surfaces after the Claude ops-runbook skill edit. |
| Provider mirror freshness | `bash scripts/operations/sync-provider-surfaces.sh --check` | PASS: `sync-provider-surfaces: no drift`. |
| README approved surfaces | `rg -n 'Related References\|docs/99\.templates/(readme\|service)\.template\|docs/0[7]\.operations\|docs/1[0]' projects/README.md projects/storybook/README.md projects/storybook/nextjs/README.md secrets/README.md tests/README.md` | PASS: no stale section, removed template, or legacy stage-pattern matches in approved T-003 surfaces. |
| README examples boundary | `rg -n 'docs/99\.templates/(readme\|service)\.template\|Related References' projects secrets tests examples` | EXPECTED SCOPED RESIDUAL: matches remain only under `examples/sample-web-service/**`, which is WDC-GAP-017 and remains deferred. |

## Remediation Evidence

### T-002 Governance and Provider Adapter Drift

- WDC-GAP-001: updated `.agents/rules/workspace.md` and
  `.agents/workflows/documentation.md` so Gemini/Antigravity native surfaces
  defer model policy, workflow policy, artifact routing, and template rules to
  Stage 00 and Stage 99 owners instead of restating those rules.
- WDC-GAP-002: updated `.claude/agents/doc-writer.md` and
  `.claude/skills/ops-runbook-agent/skill.md` so runtime prompts link to the
  documentation protocol, docs scope, stage authoring matrix, and mapped
  operations templates instead of owning DOCS 3 or operations section profiles.
- Generated Codex mirror: refreshed
  `.codex/skills/ops-runbook-agent/skill.md` from the Claude skill through
  `scripts/operations/sync-provider-surfaces.sh --write`.
- Root shim alignment: updated `GEMINI.md` so model selection points to
  `docs/00.agent-governance/subagent-protocol.md` rather than repeating model
  values.
- WDC-GAP-022: remote branch-protection evidence remains deferred. No `gh api`
  remote verification or remote setting mutation was performed in this batch.

### T-003 README Profile Normalization

- WDC-GAP-003: updated project README surfaces to use `## Related Documents`
  and canonical `docs/99.templates/templates/common/readme.template.md`
  links. `projects/README.md` also no longer repeats obsolete operations-stage
  path literals.
- WDC-GAP-004: updated `secrets/README.md` to use the README profile's
  `## Related Documents` heading, removed a duplicate operations README link,
  and replaced the removed flat README template link. No secret value files
  were opened.
- WDC-GAP-005: updated `tests/README.md` to use `## Related Documents`.
- WDC-GAP-017: examples remain deferred; `examples/sample-web-service/**`
  still contains the removed flat service-template references until an
  examples/scaffold contract decision is approved.
- WDC-GAP-019: the stale operations-stage literal in `projects/README.md` was
  remediated after project README scope approval in this batch.

## Verification Summary

- **Test Commands**: Listed in `## Validation Results`.
- **Eval Commands**: N/A for documentation task evidence.
- **Logs / Evidence Location**: This task document and the source
  `gap-register.md`.
- **Manual Checks**: Confirmed T-003 changes stayed limited to approved
  project, secrets, and tests README surfaces; no provider, workflow,
  validator, secret value, runtime, or infra surfaces were changed.

## Related Documents

- **Parent Plan**: [Document contract remediation batch plan](../plans/2026-07-03-document-contract-remediation-batches.md)
- **Source Register**: [Document contract gap register](../../90.references/audits/document-contracts/gap-register.md)
- **Audit Pack Task**: [Workspace document contract audit pack task](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Audit Pack Plan**: [Workspace document contract audit pack plan](../plans/2026-07-03-workspace-document-contract-audit-pack.md)
- **Audit Pack Spec**: [Workspace document contract audit pack spec](../../03.specs/workspace-document-contract-audit-pack/spec.md)
