---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-03-template-system-contract-standardization.md -->

# Template System Contract Standardization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Standardize the Stage 99 template system contract and frontmatter rules so `support/` owns rules, `templates/` owns copyable forms, and validators enforce the boundary.

**Architecture:** This plan implements the contract-first design in `docs/03.specs/template-system-contract-standardization/spec.md`. It updates support contracts first, then copyable templates, then validator enforcement, then direct fallout surfaces and generated indexes. Broad target-document rewrites stay out of scope unless they are direct fallout from a changed template or validator rule.

**Tech Stack:** Markdown, Bash, Python snippets embedded in `scripts/validation/check-repo-contracts.sh`, Git, repo-local validation scripts.

---

## Overview

This plan turns the approved Stage 99 contract-standardization spec into
bite-sized implementation tasks. Each task has a clear commit boundary and
verification gate.

## Context

The repository already separates copyable templates under
`docs/99.templates/templates/` from non-copyable support rules under
`docs/99.templates/support/`. The next step is to tighten the contract:
frontmatter must be role-specific, README files must stay as indexes, support
documents must own durable rules, and validators must catch legacy path,
metadata, and target-contract drift.

The plan intentionally avoids runtime changes. Known infra image/version drift
is recorded as an out-of-scope gap when full repo contracts are run.

## Goals & In-Scope

- **Goals**:
  - Make Stage 99 support documents the single rule surface for template
    contracts, frontmatter, lifecycle, governance, and selection.
  - Normalize copyable template source metadata and target guidance.
  - Add validator coverage for legacy frontmatter keys, README/support boundary
    drift, machine-readable template frontmatter, and template target mapping.
  - Update only direct fallout in governance/provider/index surfaces.
- **In Scope**:
  - `docs/99.templates/support/**`
  - `docs/99.templates/templates/**`
  - `scripts/validation/check-repo-contracts.sh`
  - direct references in `docs/00.agent-governance/**`, `.claude/**`,
    `.codex/**`, `docs/03.specs/**`, `docs/04.execution/**`, and
    `docs/90.references/llm-wiki/llm-wiki-index.md`
  - progress evidence in `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not rewrite all existing target documents into the newest template body
    shape.
  - Do not add new top-level docs stages or compatibility shims.
  - Do not resolve infra image/version drift.
- **Out of Scope**:
  - Docker Compose runtime changes
  - secret values, credentials, tokens, or private keys
  - remote GitHub settings
  - deployment behavior
  - non-direct corpus-wide prose rewriting

## File Structure

| File or Directory | Responsibility in This Plan |
| --- | --- |
| `docs/99.templates/support/template-contract.md` | Canonical template-source shape, placeholder rules, target inheritance, and README/support boundary. |
| `docs/99.templates/support/frontmatter-contract.md` | Type-specific frontmatter key/value contract and legacy-key removal rules. |
| `docs/99.templates/support/template-governance.md` | Protected surface, commit boundary, review, validation, and rollback rules. |
| `docs/99.templates/support/template-selection.md` | Target path to canonical template mapping. |
| `docs/99.templates/support/lifecycle-status.md` | Lifecycle values and allowed surfaces. |
| `docs/99.templates/support/external-source-rationale.md` | External source rationale and local interpretation. |
| `docs/99.templates/support/README.md` | Support document index only. |
| `docs/99.templates/templates/**` | Copyable template artifacts only. |
| `docs/99.templates/README.md` | Stage 99 catalog and routing entrypoint only. |
| `scripts/validation/check-repo-contracts.sh` | Enforces Stage 99 template, frontmatter, target path, and legacy drift contracts. |
| `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md` | Execution evidence for the implementation run. |
| `docs/90.references/llm-wiki/llm-wiki-index.md` | Generated tracked path index refreshed after doc additions, moves, or deletions. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target Spec Criteria | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create execution evidence and freeze the Stage 99 inventory baseline. | `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md` | VAL-TPL-003 | Inventory commands captured; task evidence has protected surface boundaries. |
| PLN-002 | Consolidate Stage 99 support contracts. | `docs/99.templates/support/*.md`, `docs/99.templates/README.md` | VAL-TPL-001 | Support docs own durable rules; README remains catalog/routing only. |
| PLN-003 | Normalize copyable template metadata and target contracts. | `docs/99.templates/templates/**/*.template.*`, template category READMEs | VAL-TPL-001 | Template sources use allowed metadata and target guidance. |
| PLN-004 | Enforce contract and legacy drift in validators. | `scripts/validation/check-repo-contracts.sh` | VAL-TPL-004 | Repo contract catches template/frontmatter/target drift and stale legacy patterns. |
| PLN-005 | Apply direct fallout and regenerate derived indexes. | direct references, provider surfaces, LLM Wiki index | VAL-TPL-003 | No provider drift, stale path drift, or generated index drift. |
| PLN-006 | Close evidence, run final validation, and commit. | progress log, task evidence, staged changes | VAL-TPL-004 | Required checks pass or report only known infra drift. |

## Implementation Tasks

### Task 1: Create Execution Evidence and Inventory Baseline

**Files:**

- Create: `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`
- Modify: `docs/04.execution/tasks/README.md`
- Read: `docs/99.templates/support/template-contract.md`
- Read: `docs/99.templates/support/frontmatter-contract.md`
- Read: `docs/03.specs/template-system-contract-standardization/spec.md`

 **Step 1: Create the task evidence file from the task template**

Create `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md` with this initial content:

```markdown
---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md -->

# Task: Template System Contract Standardization

## Overview

This task records execution evidence for the Stage 99 template-system contract
standardization implementation. The work updates support contracts, copyable
templates, validator rules, direct fallout references, provider mirrors, and
generated indexes according to the approved spec.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/99.templates/**` | User-approved A+B scope and approved spec | Support contracts and copyable templates | Inventory captured before edits | Updated contracts and templates | `git revert` this task's commits | No secret values, credentials, tokens, private keys, raw logs, or `.env` values |
| `scripts/validation/check-repo-contracts.sh` | User-approved protected-surface change | Template/frontmatter validator rules | Existing validator sections inspected | New checks added or confirmed | `git revert` validator commit | No secret values, credentials, tokens, private keys, raw logs, or `.env` values |
| Provider surfaces | Template rules affect agent behavior | `.claude/**`, `.codex/**` | Provider sync check | Provider sync no drift | `bash scripts/operations/sync-provider-surfaces.sh --write` then revert if needed | No credentials or local-only settings |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Capture Stage 99 inventory baseline. | docs | Template System Contract Standardization Spec / Data Modeling | PLN-001 | Inventory command output summarized below | Codex | Active |
| T-002 | Consolidate support contracts. | docs | Template System Contract Standardization Spec / Core Design | PLN-002 | Support docs diff and repo contract | Codex | Planned |
| T-003 | Normalize copyable templates. | docs | Template System Contract Standardization Spec / Interfaces | PLN-003 | Template scan and repo contract | Codex | Planned |
| T-004 | Update validator enforcement. | script | Template System Contract Standardization Spec / Validator Interfaces | PLN-004 | `bash -n` and repo contract | Codex | Planned |
| T-005 | Apply direct fallout and regenerate indexes. | docs | Template System Contract Standardization Spec / Tools | PLN-005 | Provider sync and LLM Wiki freshness | Codex | Planned |
| T-006 | Close verification evidence. | docs | Template System Contract Standardization Spec / Success Criteria | PLN-006 | Validation matrix complete | Codex | Planned |

## Inventory Baseline

- Template source files: Not run at evidence-file creation time; Task 1 Step 2 replaces this with the exact count and any notable path groups.
- Support documents: Not run at evidence-file creation time; Task 1 Step 2 replaces this with the exact count and support document list summary.
- Legacy frontmatter key hits: Not run at evidence-file creation time; Task 1 Step 3 replaces this with either `none` or a concise gap list.

## Validation Results

| Command | Result |
| --- | --- |
| `git diff --check` | Pending |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Pending |
| `bash scripts/operations/sync-provider-surfaces.sh --check` | Pending |
| `bash scripts/validation/check-doc-traceability.sh` | Pending |
| `bash scripts/validation/check-doc-implementation-alignment.sh` | Pending |
| `bash scripts/validation/check-repo-contracts.sh` | Pending |

## Verification Summary

- **Test Commands**: Listed in `## Validation Results`.
- **Eval Commands**: N/A for documentation contract standardization.
- **Manual Checks**: Verify support docs own rules and README files remain indexes.

## Related Documents

- **Spec**: [../../03.specs/template-system-contract-standardization/spec.md](../../03.specs/template-system-contract-standardization/spec.md)
- **Plan**: [../plans/2026-07-03-template-system-contract-standardization.md](../plans/2026-07-03-template-system-contract-standardization.md)
- **Template contract**: [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- **Frontmatter contract**: [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
```

 **Step 2: Capture Stage 99 inventory counts**

Run:

```bash
find docs/99.templates/templates -type f | sort
find docs/99.templates/support -maxdepth 1 -type f | sort
```

Expected: output lists only canonical template/support files under the existing
Stage 99 folders.

 **Step 3: Capture legacy metadata scan**

Run:

```bash
rg -n '^(type|owner|updated|links|document_type|template_type):' docs/99.templates docs/01.requirements docs/02.architecture docs/03.specs docs/04.execution docs/05.operations docs/90.references
```

Expected: either no matches or matches that are explicitly documented as gaps in
the task evidence.

 **Step 4: Update the task evidence baseline**

Edit `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`:

- Replace the three initial `Not run at evidence-file creation time...` lines
  under `## Inventory Baseline` with concise counts and any legacy metadata
  hits.
- Keep command details summarized; do not paste raw long logs.

 **Step 5: Add the task to the tasks README index**

Modify `docs/04.execution/tasks/README.md` by adding one bullet or table entry
for `2026-07-03-template-system-contract-standardization.md` near the other
2026-07-03 or template-system entries.

 **Step 6: Run Task 1 verification**

Run:

```bash
git diff --check
bash scripts/validation/check-doc-traceability.sh
```

Expected:

- `git diff --check` exits 0.
- Traceability check exits 0 with `failures=0`.

 **Step 7: Commit Task 1**

Run:

```bash
git add docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md docs/04.execution/tasks/README.md
git commit -m "docs(execution): Add template contract standardization evidence"
```

Expected: commit succeeds.

### Task 2: Consolidate Support Contracts

**Files:**

- Modify: `docs/99.templates/support/template-contract.md`
- Modify: `docs/99.templates/support/frontmatter-contract.md`
- Modify: `docs/99.templates/support/template-governance.md`
- Modify: `docs/99.templates/support/template-selection.md`
- Modify: `docs/99.templates/support/lifecycle-status.md`
- Modify: `docs/99.templates/support/external-source-rationale.md`
- Modify: `docs/99.templates/support/README.md`
- Modify: `docs/99.templates/README.md`
- Modify: `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`

 **Step 1: Add support ownership language to `template-contract.md`**

Ensure `docs/99.templates/support/template-contract.md` contains these rules,
using existing section headings when possible:

```markdown
- Template forms and template rules are separate surfaces.
- Copyable forms live under `docs/99.templates/templates/`.
- Non-copyable rules live under `docs/99.templates/support/`.
- README files are indexes and routing surfaces; durable rules belong in support documents.
- Target documents inherit from exactly one primary template role.
```

 **Step 2: Expand `frontmatter-contract.md` with a role matrix**

Ensure `docs/99.templates/support/frontmatter-contract.md` contains a table with
these exact surface families:

```markdown
| Surface | Required Keys | Disallowed Duplicate-Purpose Keys |
| --- | --- | --- |
| Markdown template source | `status: draft` | `type`, `owner`, `updated`, `links`, `document_type`, `template_type` |
| Machine-readable template source | none; use comments | YAML frontmatter fences, `type`, `owner`, `updated`, `links` |
| Stage 99 support document | `layer: agentic` | `status`, `type`, `owner`, `updated`, `links` |
| Target stage document | path-derived role plus lifecycle `status` | `type`, `document_type`, `template_type` |
| Generated tracked document | generator-owned metadata such as `generated_by` | human-authored lifecycle keys unless the generator owns them |
```

 **Step 3: Add protected-surface commit rules to `template-governance.md`**

Ensure `docs/99.templates/support/template-governance.md` says:

```markdown
- Keep support-contract edits, template-source edits, validator edits, direct fallout edits, and generated-index refreshes in separate commits where practical.
- Record existing unrelated validation failures as gaps.
- Use `git mv` for path moves.
- Run provider sync checks when agent-facing surfaces change.
```

 **Step 4: Confirm `template-selection.md` maps every canonical role**

Check that `docs/99.templates/support/template-selection.md` includes target
rows for:

- PRD, ARD, ADR, Spec, Plan, Task
- Guide, Policy, Runbook, Incident packet incident file, Incident packet
  `postmortem.md`
- Reference, Archive, README
- Memory, Progress, Harness task contract
- API spec, Agent design, Data model, Service, Tests, OpenAPI, GraphQL,
  Protobuf

If a role is missing, add an exact row with the existing canonical template path.

 **Step 5: Keep `docs/99.templates/README.md` as a catalog**

Edit `docs/99.templates/README.md` only if it contains durable rules that now
belong in support. Keep it limited to overview, audience, scope, catalog,
structure, how-to-work, and related documents.

 **Step 6: Update task evidence for Task 2**

In `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`,
mark `T-002` as `Done` and add a concise note that support contracts now own
the durable rules.

 **Step 7: Run Task 2 verification**

Run:

```bash
git diff --check
rg -n 'README.*must|README.*required|README.*forbidden' docs/99.templates/README.md docs/99.templates/templates/*/README.md
```

Expected:

- `git diff --check` exits 0.
- The `rg` command returns no README-only durable contract rules that should
  live in support. A README may link to support rules.

 **Step 8: Commit Task 2**

Run:

```bash
git add docs/99.templates/support docs/99.templates/README.md docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md
git commit -m "docs(templates): Consolidate support contracts"
```

Expected: commit succeeds.

### Task 3: Normalize Copyable Templates

**Files:**

- Modify: `docs/99.templates/templates/sdlc/*.template.md`
- Modify: `docs/99.templates/templates/spec-contracts/*.template.*`
- Modify: `docs/99.templates/templates/operations/*.template.md`
- Modify: `docs/99.templates/templates/governance/*.template.md`
- Modify: `docs/99.templates/templates/common/*.template.md`
- Modify: `docs/99.templates/templates/**/README.md`
- Modify: `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`

 **Step 1: Verify Markdown template frontmatter**

Run:

```bash
for f in docs/99.templates/templates/**/*.template.md; do sed -n '1,3p' "$f"; done
```

Expected: every printed block is exactly:

```markdown
---
status: draft
---
```

 **Step 2: Remove duplicate-purpose metadata from Markdown templates**

Run:

```bash
rg -n '^(type|owner|updated|links|document_type|template_type):' docs/99.templates/templates
```

Expected: no matches. If matches exist, remove those keys from template
frontmatter or body metadata examples and rely on target sections such as
`## Related Documents`.

 **Step 3: Verify machine-readable templates do not use YAML frontmatter**

Run:

```bash
for f in docs/99.templates/templates/spec-contracts/*.template.yaml docs/99.templates/templates/spec-contracts/*.template.graphql docs/99.templates/templates/spec-contracts/*.template.proto; do sed -n '1,5p' "$f"; done
```

Expected: no output block begins with `---`.

 **Step 4: Confirm target guidance exists in every template**

Run:

```bash
rg -L 'Target:' docs/99.templates/templates
rg -L 'Target-relative|Cross-links:' docs/99.templates/templates
```

Expected: no missing-template files are printed. Markdown templates use
`Target-relative`; machine-readable templates use `Cross-links:`.

 **Step 5: Normalize category README wording**

For each file below, ensure the README describes only category purpose, template
list, target rules summary, and related documents:

```text
docs/99.templates/templates/README.md
docs/99.templates/templates/sdlc/README.md
docs/99.templates/templates/spec-contracts/README.md
docs/99.templates/templates/operations/README.md
docs/99.templates/templates/governance/README.md
docs/99.templates/templates/common/README.md
```

Move any durable contract rule to the matching `support/` document and leave a
link from the README.

 **Step 6: Update task evidence for Task 3**

In `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`,
mark `T-003` as `Done` and summarize the template frontmatter scan result.

 **Step 7: Run Task 3 verification**

Run:

```bash
git diff --check
bash scripts/validation/check-repo-contracts.sh
```

Expected:

- `git diff --check` exits 0.
- Repo contract has no template-source failures. Existing infra image/version
  drift may remain and must be recorded as out-of-scope.

 **Step 8: Commit Task 3**

Run:

```bash
git add docs/99.templates/templates docs/99.templates/support docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md
git commit -m "docs(templates): Normalize template source metadata"
```

Expected: commit succeeds.

### Task 4: Enforce Template and Frontmatter Contracts

**Files:**

- Modify: `scripts/validation/check-repo-contracts.sh`
- Modify: `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`

 **Step 1: Add or update the Stage 99 template contract validator section**

In `scripts/validation/check-repo-contracts.sh`, ensure the template validation
logic enforces these exact checks:

```text
1. Required canonical template files exist.
2. Template files do not exist outside `docs/99.templates/templates/`.
3. Markdown template sources start with `---`, `status: draft`, `---`.
4. Markdown template sources contain `Target:`, target-relative guidance, and `## Related Documents`.
5. Machine-readable template sources contain `Target:` and `Cross-links:`.
6. Machine-readable template sources do not contain Markdown `## Related Documents`.
7. Template and support docs do not use legacy duplicate-purpose frontmatter keys.
8. Stage 99 README files do not contain durable rules that belong in support.
```

 **Step 2: Add a legacy frontmatter key scan**

Add a Python or shell check that fails when any Stage 99 template/support source
uses these keys outside the allowed support examples:

```text
type
owner
updated
links
document_type
template_type
```

The check must allow these words in explanatory prose, but not as YAML
frontmatter keys at the start of a line.

 **Step 3: Add a machine-readable frontmatter check**

Ensure non-Markdown templates under `docs/99.templates/templates` fail when the
first non-empty line is `---`.

 **Step 4: Add README/support boundary check**

Add a targeted check that scans Stage 99 README files for durable rule markers
such as:

```text
Forbidden
Required keys
Allowed keys
MUST
MUST NOT
```

The check should fail only when the README is asserting a durable rule without a
nearby link to a support document. Keep this check limited to
`docs/99.templates/**/*.md`.

 **Step 5: Run syntax verification**

Run:

```bash
bash -n scripts/validation/check-repo-contracts.sh
```

Expected: command exits 0.

 **Step 6: Update task evidence for Task 4**

In `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`,
mark `T-004` as `Done` and add the validator sections updated.

 **Step 7: Run Task 4 verification**

Run:

```bash
git diff --check
bash scripts/validation/check-repo-contracts.sh
```

Expected:

- `git diff --check` exits 0.
- Repo contract has no Stage 99 template/frontmatter failures. Existing infra
  image/version drift may remain and must be recorded as out-of-scope.

 **Step 8: Commit Task 4**

Run:

```bash
git add scripts/validation/check-repo-contracts.sh docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md
git commit -m "test(templates): Enforce template metadata contract"
```

Expected: commit succeeds.

### Task 5: Apply Direct Fallout and Regenerate Indexes

**Files:**

- Modify if needed: `docs/00.agent-governance/rules/documentation-protocol.md`
- Modify if needed: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Modify if needed: `.claude/**`
- Modify if needed: `.codex/**`
- Modify: `docs/90.references/llm-wiki/llm-wiki-index.md`
- Modify: `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`

 **Step 1: Search for stale template paths and legacy key examples**

Run:

```bash
rg -n 'docs/99\.templates/(?!templates/|support/)|\.template\.md|type:|owner:|updated:|links:|document_type:|template_type:' docs .claude .codex scripts README.md
```

Expected: results are either canonical nested template paths, support contract
examples, or direct fallout that must be updated in this task.

 **Step 2: Update direct fallout references**

For every direct fallout reference found in Step 1:

- update stale template paths to canonical `docs/99.templates/templates/...`
  paths
- update stale support paths to canonical `docs/99.templates/support/...` paths
- remove legacy frontmatter examples when they are not part of support-contract
  explanation
- leave unrelated target-document body drift as a gap in the task evidence

 **Step 3: Sync provider surfaces when `.claude` changed**

Run:

```bash
bash scripts/operations/sync-provider-surfaces.sh --check
```

Expected: `sync-provider-surfaces: no drift`.

If the command reports drift caused by intentional `.claude` changes, run:

```bash
bash scripts/operations/sync-provider-surfaces.sh --write
```

Then rerun the `--check` command. Expected final output:
`sync-provider-surfaces: no drift`.

 **Step 4: Refresh the LLM Wiki index**

Run:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
```

Expected:

- generator reports the path count
- freshness check reports `PASS: generated LLM Wiki index is fresh`

 **Step 5: Update task evidence for Task 5**

In `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`,
mark `T-005` as `Done` and summarize:

- stale path scan result
- provider sync result
- LLM Wiki path count
- any out-of-scope target-document body gaps

 **Step 6: Run Task 5 verification**

Run:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
```

Expected: every command exits 0.

 **Step 7: Commit Task 5**

Run:

```bash
git add docs .claude .codex
git commit -m "docs(templates): Apply template contract fallout"
```

Expected: commit succeeds.

### Task 6: Final Verification and Evidence Closure

**Files:**

- Modify: `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`
- Modify: `docs/00.agent-governance/memory/progress.md`

 **Step 1: Run final verification bundle**

Run:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected:

- all commands except full repo contract exit 0
- full repo contract has no Stage 99, template, frontmatter, provider, link, or
  LLM Wiki failures
- full repo contract may still fail on existing infra image/version drift

 **Step 2: Try Graphify refresh**

Run:

```bash
graphify update .
```

Expected:

- if `graphify` exists, the command completes
- if `graphify` is unavailable, record `graphify update . skipped because graphify is unavailable in PATH`

 **Step 3: Close task evidence**

Edit `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md`:

- set frontmatter `status: completed`
- mark `T-006` as `Done`
- update every pending validation result with `PASS`, `PASS with known infra drift`, or `Skipped with reason`
- record the final commit list

 **Step 4: Update progress memory**

Add or update the top row in `docs/00.agent-governance/memory/progress.md`:

```markdown
| 2026-07-03 | Template contract standardization implementation | Done | Implemented the Stage 99 support/template/frontmatter contract standardization plan with validator and direct fallout updates. | N/A | Checks PASS: `git diff --check`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check`; `bash scripts/operations/sync-provider-surfaces.sh --check`; `bash scripts/validation/check-doc-traceability.sh`; `bash scripts/validation/check-doc-implementation-alignment.sh`. Full `check-repo-contracts.sh` has no template-system failures and still reports existing infra image/version drift. |
```

 **Step 5: Commit Task 6**

Run:

```bash
git add docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md docs/00.agent-governance/memory/progress.md
git commit -m "docs(templates): Close template contract standardization evidence"
```

Expected: commit succeeds.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Formatting | Staged markdown has no whitespace errors. | `git diff --check` | exit 0 |
| VAL-PLN-002 | LLM Wiki | Generated index is fresh. | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS freshness message |
| VAL-PLN-003 | Provider | Provider mirrors are synchronized. | `bash scripts/operations/sync-provider-surfaces.sh --check` | `sync-provider-surfaces: no drift` |
| VAL-PLN-004 | Traceability | Execution and operation docs remain linked. | `bash scripts/validation/check-doc-traceability.sh` | `failures=0` |
| VAL-PLN-005 | Implementation alignment | Active docs still align with tracked implementation surfaces. | `bash scripts/validation/check-doc-implementation-alignment.sh` | `failures=0` |
| VAL-PLN-006 | Repo contract | Template and frontmatter contract checks pass. | `bash scripts/validation/check-repo-contracts.sh` | no Stage 99/template/frontmatter failures; existing infra drift may remain |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Validator catches broad historical drift outside Stage 99 | High | Scope new checks to Stage 99 or changed direct fallout unless the spec explicitly requires broader enforcement. |
| README files regain durable rules | Medium | Move durable rules into support docs and leave README links to support. |
| Machine-readable templates accidentally gain YAML frontmatter | Medium | Add validator check for non-Markdown template frontmatter fences. |
| Provider mirrors drift after `.claude` edits | Medium | Run provider sync check and write sync when needed. |
| Full repo contract fails on known infra drift | Low | Record infra image/version drift as an out-of-scope gap and avoid runtime edits. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Run all validation commands in `## Verification Plan`.
- **Sandbox / Canary Rollout**: N/A for documentation contract changes.
- **Human Approval Gate**: User approval required before executing this plan.
- **Rollback Trigger**: Any Stage 99 validator failure that cannot be fixed
  without broad target-document rewrites.
- **Prompt / Model Promotion Criteria**: N/A; no model behavior is promoted.

## Completion Criteria

 Support contracts define the canonical Stage 99 rule surface.
 Copyable templates comply with frontmatter and target-contract rules.
 Validator enforces the Stage 99 contract without broad false positives.
 Direct fallout references are updated.
 LLM Wiki index is fresh.
 Provider surfaces report no drift.
 Execution task evidence is completed.
 Progress memory is updated.

## Related Documents

- **Spec**: [../../03.specs/template-system-contract-standardization/spec.md](../../03.specs/template-system-contract-standardization/spec.md)
- **Prior Template System Spec**: [../../03.specs/template-system-reorganization/spec.md](../../03.specs/template-system-reorganization/spec.md)
- **Planned Task Evidence**: `docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md` will be created by Task 1.
- **Template catalog**: [../../99.templates/README.md](../../99.templates/README.md)
- **Template contract**: [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- **Frontmatter contract**: [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Template governance**: [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
- **Template selection guide**: [../../99.templates/support/template-selection.md](../../99.templates/support/template-selection.md)
- **Documentation protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
