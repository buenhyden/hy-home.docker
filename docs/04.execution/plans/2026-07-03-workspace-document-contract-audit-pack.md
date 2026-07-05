---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md -->

# Workspace Document Contract Audit Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a contract-first audit pack that inventories workspace document profiles, compares them with repo-local contracts, maps CI/CD and QA automation coverage, and records actionable gaps without rewriting the corpus.

**Architecture:** The plan executes the approved spec in `docs/03.specs/102-workspace-document-contract-audit-pack/spec.md` as an audit-only pass. It creates execution evidence under `docs/04.execution/tasks/`, durable audit reports under `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/`, and a batch proposal that later implementation plans can execute with separate commits.

**Tech Stack:** Markdown, YAML frontmatter inspection, `git ls-files`, `rg`, Bash validation scripts, GitHub Actions YAML inspection, repo-local documentation validators.

---

## Overview

This plan turns the approved workspace document contract audit pack spec into
bite-sized execution tasks. The implementation creates audit evidence and
reports only. It does not normalize target documents, change Docker Compose
runtime behavior, read secret values, or modify remote systems.

The plan deliberately separates:

- **Execution evidence** in `docs/04.execution/tasks/`.
- **Reusable audit reports** in `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/`.
- **Future implementation batches** described as gaps, not executed in this
  audit pack.

## Context

The repository already has Stage 00 governance, Stage 99 template contracts,
repo-local validators, provider-surface sync, and LLM Wiki indexing. The next
safe step is to measure how root shims, provider files, GitHub workflows,
official docs stages, infra/project/script/secret/test docs, archives, and
examples conform to those contracts.

The approved spec requires classification before edits. Active policy,
historical evidence, generated references, and out-of-scope runtime drift must
not be treated as the same kind of gap.

## Goals & In-Scope

- **Goals**:
  - Create an execution task record for the audit pack.
  - Create the `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/` audit-report
    bundle.
  - Inventory document roles, surfaces, README profiles, frontmatter keys,
    sections, stale template guidance, CI/CD rules, QA gates, and automation
    coverage.
  - Classify gaps as `direct-fix`, `batch-fix`, `historical-evidence`,
    `out-of-scope-gap`, or `no-action`.
  - Produce a future implementation batch proposal without applying the fixes.
- **In Scope**:
  - `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
  - `docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md`
  - `docs/90.references/audits/README.md`
  - `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/**`
  - `docs/90.references/README.md` when it needs a new audit category link
  - `docs/90.references/llm-wiki/llm-wiki-index.md`
  - `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not rewrite the target corpus in this plan.
  - Do not delete legacy documents.
  - Do not add new validators unless audit evidence proves the gap and a later
    implementation plan approves validator work.
  - Do not resolve existing infra image/version drift.
- **Out of Scope**:
  - Docker Compose runtime changes.
  - Secret values, credentials, tokens, certificates, private keys, shell
    history, raw logs, and `.env` values.
  - Remote GitHub settings and branch protection changes.
  - Provider runtime configuration changes.
  - Bulk edits to historical Stage 04 evidence.
  - Formatting-only target document rewrites.

## File Structure

| File or Directory | Responsibility in This Plan |
| --- | --- |
| `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md` | Execution evidence, task checklist, validation results, and commit trail for the audit pack run. |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md` | Index for the durable document-contract audit reports. |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-inventory.md` | Counts and examples of top-frontmatter keys by surface and document role. |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/section-profile-inventory.md` | Required, optional, duplicate, and forbidden heading patterns by document role. |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/readme-profile-inventory.md` | README profile comparison for root, docs, governance, infra, scripts, secrets, projects, tests, examples, and archive surfaces. |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/contract-governance-map.md` | Stage 00, Stage 99, root shim, provider, script, and workflow governance comparison. |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/template-application-gaps.md` | Active stale template guidance, old template paths, unresolved template tokens, and historical-evidence classifications. |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md` | CI/CD, QA, validation, provider sync, LLM Wiki, hardening, and local QA coverage matrix. |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md` | Final disposition table and future implementation batch proposal. |
| `docs/90.references/audits/README.md` | Audit category index updated to route to `document-contracts/`. |
| `docs/90.references/README.md` | Reference-stage index updated when the new audit bundle is not already discoverable. |
| `docs/90.references/llm-wiki/llm-wiki-index.md` | Generated tracked path index refreshed after new audit files are added. |
| `docs/00.agent-governance/memory/progress.md` | Final work log entry for the audit-pack execution. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target Spec Criteria | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create task evidence and audit bundle skeleton. | Task evidence, audit README files, audit indexes | VAL-WDC-001, VAL-WDC-002 | Task evidence exists, audit bundle is linked, `git diff --check` passes. |
| PLN-002 | Capture document role, frontmatter, section, and README profile inventories. | `frontmatter-inventory.md`, `section-profile-inventory.md`, `readme-profile-inventory.md` | VAL-WDC-002, VAL-WDC-003 | Inventories cite commands, scopes, counts, and known limitations. |
| PLN-003 | Compare governance, contracts, templates, root shims, and provider surfaces. | `contract-governance-map.md`, `template-application-gaps.md` | VAL-WDC-003, VAL-WDC-004 | Gaps are classified without editing target corpus files. |
| PLN-004 | Map CI/CD, QA, and automation coverage. | `automation-coverage-map.md` | VAL-WDC-005 | Workflows and validators are mapped with enforce/report/gap status. |
| PLN-005 | Build the gap register and future implementation batch proposal. | `gap-register.md`, task evidence | VAL-WDC-004, VAL-WDC-006 | Every gap has disposition, evidence, and next-action owner. |
| PLN-006 | Close evidence, regenerate indexes, validate, and commit. | progress log, LLM Wiki index, task evidence | VAL-WDC-001 through VAL-WDC-006 | Required checks pass or fail only on known infra drift. |

## Implementation Tasks

### Task 1: Create Task Evidence and Audit Bundle Skeleton

**Files:**

- Create: `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
- Create: `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md`
- Modify: `docs/90.references/audits/README.md`
- Modify: `docs/90.references/README.md` when the audit bundle is not listed
- Read: `docs/03.specs/102-workspace-document-contract-audit-pack/spec.md`
- Read: `docs/90.references/audits/README.md`

- [ ] **Step 1: Create the task evidence file**

Create `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md` with this initial content:

```markdown
---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md -->

# Task: Workspace Document Contract Audit Pack

## Overview

This task records execution evidence for the workspace document contract audit
pack. The work creates durable audit reports for document profiles,
frontmatter, sections, README profiles, governance contracts, CI/CD, QA,
automation coverage, and future implementation gaps.

## Inputs

- Parent Spec: `docs/03.specs/102-workspace-document-contract-audit-pack/spec.md`
- Parent Plan: `docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md`
- Template Contract: `docs/99.templates/support/template-contract.md`
- Frontmatter Contract: `docs/99.templates/support/frontmatter-contract.md`
- Stage Authoring Matrix: `docs/00.agent-governance/rules/stage-authoring-matrix.md`

## Working Rules

- Audit first; do not normalize target documents in this task.
- Inspect tracked paths, Markdown structure, workflow YAML, and validator output.
- Do not read or print secret values from `secrets/**`.
- Classify historical evidence separately from active guidance drift.
- Record existing infra image/version drift as out of scope.
- Keep execution evidence here and stable audit reports in `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/`.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md` | Approved Stage 03 spec and user approval | Execution evidence | File absent | Task evidence records audit execution | `git revert` audit-pack commits | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/**` | Approved Stage 03 spec and user approval | Durable audit reports | Bundle absent | Audit reports created and indexed | `git revert` audit-pack commits | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |
| `docs/90.references/audits/README.md` | Approved Stage 03 spec and user approval | Audit category routing | Document-contract bundle not listed | Bundle linked | `git revert` audit-pack commits | No secret values, credentials, tokens, private keys, raw logs, shell history, or `.env` values |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create task evidence and audit bundle skeleton. | docs | Workspace Document Contract Audit Pack Spec / Data Modeling | PLN-001 | Audit skeleton and links | Codex | Active |
| T-002 | Capture document profile inventories. | docs | Workspace Document Contract Audit Pack Spec / Core Design | PLN-002 | Inventory reports with commands and counts | Codex | Planned |
| T-003 | Compare governance, contracts, templates, root shims, and provider surfaces. | docs | Workspace Document Contract Audit Pack Spec / Contracts | PLN-003 | Contract map and template-application gap report | Codex | Planned |
| T-004 | Map CI/CD, QA, and automation coverage. | docs | Workspace Document Contract Audit Pack Spec / Tool Contract | PLN-004 | Automation coverage map | Codex | Planned |
| T-005 | Build final gap register and implementation batch proposal. | docs | Workspace Document Contract Audit Pack Spec / Gap Disposition Rules | PLN-005 | Gap register with dispositions | Codex | Planned |
| T-006 | Close evidence, regenerate indexes, validate, and commit. | docs | Workspace Document Contract Audit Pack Spec / Verification | PLN-006 | Validation matrix and commit trail | Codex | Planned |

## Inventory Baseline

- Baseline tracked Markdown count: Not run yet; Task 2 records the exact count.
- Baseline README count: Not run yet; Task 2 records the exact count.
- Baseline workflow count: Not run yet; Task 4 records the exact count.
- Existing out-of-scope drift: Known infra hardening and tech-stack expected-image drift remain out of scope.

## Validation Results

| Command | Result |
| --- | --- |
| `git diff --check` | Pending |
| `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Pending |
| `bash scripts/operations/sync-provider-surfaces.sh --check` | Pending |
| `bash scripts/validation/check-doc-traceability.sh` | Pending |
| `bash scripts/validation/check-doc-implementation-alignment.sh` | Pending |
| `bash -n scripts/validation/check-repo-contracts.sh` | Pending |
| `bash scripts/validation/check-repo-contracts.sh` | Pending |

## Verification Summary

- Test Commands: Listed in `## Validation Results`.
- Eval Commands: N/A for documentation audit reports.
- Manual Checks: Confirm audit reports classify gaps without editing target documents.

## Commit Trail

- Pending.

## Related Documents

- Spec: `docs/03.specs/102-workspace-document-contract-audit-pack/spec.md`
- Plan: `docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md`
- Audit bundle: `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md`
```

- [ ] **Step 2: Create the audit bundle README**

Create `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md` with this
content:

```markdown
---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md -->

# Document Contract Audit References

> durable audit reports for workspace document contracts and automation coverage

## Overview

This folder stores reusable audit reports for repository documentation
contracts. It supports active execution evidence in
`docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
without replacing that task evidence.

## Audience

This README is for:

- Documentation Specialists
- Agentic Workflow Specialists
- QA Engineers
- Repository Maintainers

## Scope

### In Scope

- Frontmatter, section, and README profile inventories.
- Governance, template, root shim, provider, workflow, and validator comparison.
- CI/CD, QA, and automation coverage mapping.
- Gap disposition records and future implementation batch proposals.

### Out of Scope

- Runtime configuration changes.
- Secret values, credentials, tokens, certificates, private keys, shell history, raw logs, and `.env` values.
- Active task evidence that belongs in `docs/04.execution/tasks/`.
- Historical evidence rewriting.

## Structure

- `README.md`
- `frontmatter-inventory.md`
- `section-profile-inventory.md`
- `readme-profile-inventory.md`
- `contract-governance-map.md`
- `template-application-gaps.md`
- `automation-coverage-map.md`
- `gap-register.md`

## Current References

- Frontmatter inventory: `frontmatter-inventory.md`
- Section profile inventory: `section-profile-inventory.md`
- README profile inventory: `readme-profile-inventory.md`
- Contract governance map: `contract-governance-map.md`
- Template application gaps: `template-application-gaps.md`
- Automation coverage map: `automation-coverage-map.md`
- Gap register: `gap-register.md`

## How to Work in This Area

1. Keep reports source-attributed with command or file evidence.
2. Classify gaps before proposing edits.
3. Record out-of-scope infra, runtime, secret, remote, and historical-evidence gaps without patching them.
4. Update this README when audit report files are added, renamed, or removed.
5. Refresh the LLM Wiki index after changing tracked report files.

## Related Documents

- Audit references: `docs/90.references/audits/README.md`
- Workspace document contract audit pack spec: `docs/03.specs/102-workspace-document-contract-audit-pack/spec.md`
- Workspace document contract audit pack plan: `docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md`
- Workspace document contract audit pack task: `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
- Template contract: `docs/99.templates/support/template-contract.md`
- Frontmatter contract: `docs/99.templates/support/frontmatter-contract.md`
```

- [ ] **Step 3: Update audit indexes**

Modify `docs/90.references/audits/README.md`:

- In `## Structure`, add `document-contracts/ # Workspace document contract audit reports`.
- In `## Current References`, replace "No non-README audit references are
  currently tracked in this category." with a bullet linking to
  `Document contract audit references: ./document-contracts/README.md`.

Modify `docs/90.references/README.md` only if `audits/` does not already explain
that audit reports live there. Add one routing line to the existing reference
category list; do not add a new section.

- [ ] **Step 4: Run Task 1 verification**

Run:

```bash
git diff --check
bash scripts/validation/check-doc-traceability.sh
```

Expected:

- `git diff --check` exits 0.
- Traceability exits 0 with `failures=0`.

- [ ] **Step 5: Commit Task 1**

Run:

```bash
git add docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md docs/90.references/audits/README.md docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md docs/90.references/README.md
git commit -m "docs(audits): Add document contract audit pack evidence"
```

Expected: commit succeeds. If `docs/90.references/README.md` was not changed,
remove it from `git add`.

### Task 2: Capture Document Profile Inventories

**Files:**

- Create: `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-inventory.md`
- Create: `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/section-profile-inventory.md`
- Create: `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/readme-profile-inventory.md`
- Modify: `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
- Read: `docs/99.templates/support/frontmatter-contract.md`
- Read: `docs/99.templates/support/template-selection.md`

- [ ] **Step 1: Capture tracked Markdown and README counts**

Run:

```bash
git ls-files '*.md' | wc -l
git ls-files '*README.md' | wc -l
git ls-files '*.md' | rg -n '(^|/)README\.md$'
```

Expected:

- The first two commands print numeric counts.
- The README path list contains root, docs, infra, projects, tests, examples,
  archive, and stage README surfaces when those files are tracked.

- [ ] **Step 2: Capture top-frontmatter key distribution**

Run:

```bash
python3 - <<'PY'
from collections import Counter, defaultdict
from pathlib import Path
import subprocess

paths = subprocess.check_output(["git", "ls-files", "*.md"], text=True).splitlines()
key_counts = Counter()
examples = defaultdict(list)
for path in paths:
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        key_counts["(none)"] += 1
        if len(examples["(none)"]) < 5:
            examples["(none)"].append(path)
        continue
    end = text.find("\n---\n", 4)
    if end == -1:
        key_counts["(unterminated)"] += 1
        examples["(unterminated)"].append(path)
        continue
    keys = []
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "-")):
            keys.append(line.split(":", 1)[0].strip())
    if not keys:
        key_counts["(empty)"] += 1
        if len(examples["(empty)"]) < 5:
            examples["(empty)"].append(path)
    for key in keys:
        key_counts[key] += 1
        if len(examples[key]) < 5:
            examples[key].append(path)

for key, count in sorted(key_counts.items(), key=lambda item: (-item[1], item[0])):
    print(f"{key}\t{count}\t{', '.join(examples[key])}")
PY
```

Expected: output is tab-separated key, count, and example paths. Record the top
keys, unexpected duplicate-purpose keys, and example paths in
`frontmatter-inventory.md`.

- [ ] **Step 3: Capture heading distribution by surface**

Run:

```bash
python3 - <<'PY'
from collections import Counter, defaultdict
from pathlib import Path
import subprocess

paths = subprocess.check_output(["git", "ls-files", "*.md"], text=True).splitlines()
surface_counts = defaultdict(Counter)
examples = defaultdict(lambda: defaultdict(list))

def surface(path):
    if path in {"AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md"}:
        return "root"
    if path.startswith((".agents/", ".claude/", ".codex/")):
        return "provider"
    if path.startswith(".github/"):
        return "github"
    if path.startswith("docs/"):
        parts = path.split("/")
        return "/".join(parts[:2]) if len(parts) > 1 else "docs"
    return path.split("/", 1)[0] if "/" in path else "other"

for path in paths:
    text = Path(path).read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            title = line[level:].strip()
            if title:
                key = f"H{level}: {title}"
                group = surface(path)
                surface_counts[group][key] += 1
                if len(examples[group][key]) < 3:
                    examples[group][key].append(path)

for group in sorted(surface_counts):
    print(f"## {group}")
    for key, count in surface_counts[group].most_common(25):
        print(f"{count}\t{key}\t{', '.join(examples[group][key])}")
PY
```

Expected: output groups common headings by surface. Record repeated headings,
required profile sections, and suspicious duplicate sections in
`section-profile-inventory.md`.

- [ ] **Step 4: Capture README profile examples**

Run:

```bash
git ls-files '*README.md' | while read -r path; do
  printf '%s\t' "$path"
  rg -n '^## (Overview|Audience|Scope|Structure|How to Work in This Area|Related Documents|Current References|Documentation Standards|Plan Contract)' "$path" | sed 's/:.*//' | wc -l
done
```

Expected: each README path prints with a numeric count of expected profile
headings. Use the output to identify root README, docs-stage README, governance
README, infra folder README, infra service README, scripts README, secrets
README, projects README, tests README, examples README, and archive README
profiles.

- [ ] **Step 5: Write inventory reports**

Create the three inventory files with these shared sections:

- top frontmatter `status: active`
- target comment pointing to the exact report path
- H1 matching the report name
- `## Overview`
- `## Scope`
- `## Method`
- `## Findings`
- `## Gaps For Register`
- `## Related Documents`

Each `## Method` table must quote the command used in this task and describe
the measured purpose. Each `## Findings` and `## Gaps For Register` table must
use measured evidence from Steps 1 through 4 and one of these dispositions:
`direct-fix`, `batch-fix`, `historical-evidence`, `out-of-scope-gap`, or
`no-action`. Do not save illustrative rows.

- [ ] **Step 6: Update task evidence**

In `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`:

- Mark `T-002` as `Done`.
- Replace the "Not run yet" baseline lines for tracked Markdown and README
  counts with measured counts.
- Add a concise implementation note naming the three report files.

- [ ] **Step 7: Run Task 2 verification**

Run:

```bash
rg -n 'sample row|example row|measured gap|measured finding|exact command from this task|illustrative row' docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-inventory.md docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/section-profile-inventory.md docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/readme-profile-inventory.md
git diff --check
bash scripts/validation/check-doc-traceability.sh
```

Expected:

- The `rg` command finds no remaining template markers.
- `git diff --check` exits 0.
- Traceability exits 0 with `failures=0`.

- [ ] **Step 8: Commit Task 2**

Run:

```bash
git add docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-inventory.md docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/section-profile-inventory.md docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/readme-profile-inventory.md docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md
git commit -m "docs(audits): Inventory workspace document profiles"
```

Expected: commit succeeds.

### Task 3: Compare Governance, Contracts, Templates, Root Shims, and Provider Surfaces

**Files:**

- Create: `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/contract-governance-map.md`
- Create: `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/template-application-gaps.md`
- Modify: `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
- Read: `AGENTS.md`
- Read: `CLAUDE.md`
- Read: `GEMINI.md`
- Read: `README.md`
- Read: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Read: `docs/99.templates/support/template-contract.md`
- Read: `docs/99.templates/support/frontmatter-contract.md`
- Read: `docs/99.templates/support/template-governance.md`
- Read: `docs/99.templates/support/template-selection.md`

- [ ] **Step 1: Scan active governance and provider surfaces**

Run:

```bash
rg -n 'docs/99\.templates/(readme|service|runbook|incident|postmortem|plan|task|spec|adr|prd|ard)\.template|type:|owner:|updated:|document_type:|template_type:' AGENTS.md CLAUDE.md GEMINI.md README.md .agents .claude .codex docs/00.agent-governance docs/99.templates
```

Expected: output may include valid support text, historical notes, or actionable
active guidance drift. Classify each actionable match in
`template-application-gaps.md`; do not edit the matched files in this task.

- [ ] **Step 2: Scan target surfaces for active stale template guidance**

Run:

```bash
rg -n --pcre2 'docs/99\.templates/(?!templates/|support/)|Use templates from docs/99\.templates|Read the matching template from docs/99\.templates|load the mapped template from docs/99\.templates' AGENTS.md CLAUDE.md GEMINI.md README.md docs archive examples infra projects scripts secrets tests .agents .claude .codex .github
```

Expected: output is classified as active guidance drift, broad catalog
reference, historical evidence, generated artifact, or out-of-scope gap. Record
the classification in `template-application-gaps.md`.

- [ ] **Step 3: Compare contract ownership surfaces**

Run:

```bash
rg -n 'frontmatter|template|README|governance|contract|policy|rule|validation|validator|CI|QA|Formatting|formatting|SDLC' docs/00.agent-governance docs/99.templates AGENTS.md CLAUDE.md GEMINI.md README.md .github scripts
```

Expected: output identifies the current rule owners and possible duplicate
rule surfaces. Summarize ownership in `contract-governance-map.md`; do not move
rules in this task.

- [ ] **Step 4: Write the governance map and template gap reports**

Create `contract-governance-map.md` with:

- `## Overview`
- `## Scope`
- `## Method`
- `## Contract Owners`
- `## Potential Conflicts`
- `## Rule Duplication Candidates`
- `## Gaps For Register`
- `## Related Documents`

Create `template-application-gaps.md` with:

- `## Overview`
- `## Scope`
- `## Method`
- `## Active Guidance Drift`
- `## Broad References With No Action`
- `## Historical Evidence`
- `## Out-of-Scope Gaps`
- `## Gaps For Register`
- `## Related Documents`

Use measured path and line evidence from Steps 1 through 3. Every gap row must
include a disposition from the approved set.

- [ ] **Step 5: Update task evidence**

In `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`:

- Mark `T-003` as `Done`.
- Add an implementation note naming `contract-governance-map.md` and
  `template-application-gaps.md`.
- Record whether `DESIGN.md` was absent or present.

- [ ] **Step 6: Run Task 3 verification**

Run:

```bash
test -e DESIGN.md && printf 'DESIGN.md present\n' || printf 'DESIGN.md absent\n'
rg -n 'sample row|example row|measured gap|measured finding|illustrative row' docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/contract-governance-map.md docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/template-application-gaps.md
git diff --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-implementation-alignment.sh
```

Expected:

- The `test` command prints either `DESIGN.md present` or `DESIGN.md absent`.
- The `rg` command finds no remaining template markers.
- Diff whitespace, provider sync, and implementation alignment checks pass.

- [ ] **Step 7: Commit Task 3**

Run:

```bash
git add docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/contract-governance-map.md docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/template-application-gaps.md docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md
git commit -m "docs(audits): Compare document governance contracts"
```

Expected: commit succeeds.

### Task 4: Map CI/CD, QA, and Automation Coverage

**Files:**

- Create: `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md`
- Modify: `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
- Read: `.github/workflows/**`
- Read: `scripts/README.md`
- Read: `scripts/validation/check-repo-contracts.sh`
- Read: `scripts/validation/check-doc-traceability.sh`
- Read: `scripts/validation/check-doc-implementation-alignment.sh`
- Read: `scripts/operations/sync-provider-surfaces.sh`
- Read: `scripts/knowledge/generate-llm-wiki-index.sh`

- [ ] **Step 1: Inventory GitHub workflows**

Run:

```bash
git ls-files '.github/workflows/*.yml' '.github/workflows/*.yaml'
rg -n '^(name:|on:|permissions:|jobs:)|uses:|pull-requests:|contents:|id-token:|persist-credentials|actions/checkout|secrets\.' .github/workflows
```

Expected: workflow files and security-relevant lines are listed. Record
workflow names, trigger scope, permissions, action pinning status, and credential
handling in `automation-coverage-map.md`.

- [ ] **Step 2: Inventory repo-local validation and QA scripts**

Run:

```bash
git ls-files 'scripts/**/*.sh' 'scripts/*.sh' | rg '(validation|operations|knowledge|quality|test|lint|format|security|audit)'
rg -n 'check-|validate|lint|format|test|audit|security|provider|llm-wiki|hardening|traceability|alignment' scripts README.md AGENTS.md docs/00.agent-governance docs/04.execution/plans/README.md
```

Expected: validation and QA entrypoints are listed. Record whether each check is
CI-enforced, local-only, report-only, or currently unguarded.

- [ ] **Step 3: Run current validation entrypoints**

Run:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash -n scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected:

- All checks pass except full repo contract may fail only on known out-of-scope
  infra drift.
- If a new failure appears in document, provider, LLM Wiki, Stage 99, or audit
  surfaces, fix the audit report or task evidence before continuing.

- [ ] **Step 4: Write `automation-coverage-map.md`**

Create `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md`
with:

- `## Overview`
- `## Scope`
- `## Method`
- `## CI/CD Workflow Coverage`
- `## QA And Validation Coverage`
- `## Formatting Coverage`
- `## Security And Supply-Chain Signals`
- `## Unguarded Rules`
- `## Gaps For Register`
- `## Related Documents`

Each coverage row must include:

- path or command
- owner surface
- current status: `enforced`, `report-only`, `local-only`, `manual`, or
  `unguarded`
- evidence
- proposed next action

- [ ] **Step 5: Update task evidence**

In `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`:

- Mark `T-004` as `Done`.
- Replace the "workflow count" baseline line with the measured count.
- Add a validation note for full repo contract behavior.

- [ ] **Step 6: Run Task 4 verification**

Run:

```bash
rg -n 'sample row|example row|measured gap|measured finding|illustrative row' docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
```

Expected:

- The `rg` command finds no remaining template markers.
- LLM Wiki freshness may fail until Task 6 regenerates the index; if it fails
  only because new audit files are not indexed yet, record that in task
  evidence and continue.
- Other checks pass.

- [ ] **Step 7: Commit Task 4**

Run:

```bash
git add docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md
git commit -m "docs(audits): Map documentation automation coverage"
```

Expected: commit succeeds.

### Task 5: Build Gap Register and Future Implementation Batch Proposal

**Files:**

- Create: `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md`
- Modify: `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
- Read: all reports under `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/`

- [ ] **Step 1: Extract gap rows from audit reports**

Run:

```bash
rg -n 'direct-fix|batch-fix|historical-evidence|out-of-scope-gap|no-action' docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack
```

Expected: output lists gap classifications from all report files. Every gap
candidate should have one of the approved dispositions.

- [ ] **Step 2: Write `gap-register.md`**

Create `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md` with:

- `## Overview`
- `## Scope`
- `## Method`
- `## Gap Summary`
- `## Direct-Fix Candidates`
- `## Batch-Fix Candidates`
- `## Historical Evidence`
- `## Out-of-Scope Gaps`
- `## No-Action Items`
- `## Future Implementation Batches`
- `## Related Documents`

Use this table shape in each gap section:

```markdown
| ID | Surface | Gap | Evidence | Disposition | Next Action |
| --- | --- | --- | --- | --- | --- |
| WDC-GAP-001 | `repo-relative/path.md` | Measured gap summary | `path:line` or command evidence | `direct-fix` | Include in the next approved document-contract remediation plan. |
```

Assign sequential IDs as `WDC-GAP-001`, `WDC-GAP-002`, and so on. Do not leave
example rows in the saved file.

- [ ] **Step 3: Add future implementation batches**

In `## Future Implementation Batches`, define batches that can be executed as
separate plans. Use this order unless measured evidence proves a different
dependency:

1. Active governance and provider drift fixes.
2. README profile normalization by surface.
3. Target-stage frontmatter and section normalization.
4. CI/CD and QA validator enhancement.
5. Historical evidence archive or tombstone cleanup.
6. Out-of-scope infra drift follow-up.

Each batch must include affected surfaces, required approvals, validation
commands, and commit boundary guidance.

- [ ] **Step 4: Update task evidence**

In `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`:

- Mark `T-005` as `Done`.
- Add a summary of gap counts by disposition.
- Add a note that no target corpus fixes were applied in the audit pack.

- [ ] **Step 5: Run Task 5 verification**

Run:

```bash
rg -n 'sample row|example row|measured gap|measured finding|illustrative row' docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md
rg -n 'WDC-GAP-[0-9]{3}' docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md
git diff --check
bash scripts/validation/check-doc-traceability.sh
```

Expected:

- The first `rg` command finds no remaining template markers.
- The second `rg` command finds at least one gap ID if any gaps were measured.
- Diff whitespace and traceability checks pass.

- [ ] **Step 6: Commit Task 5**

Run:

```bash
git add docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md
git commit -m "docs(audits): Register document contract gaps"
```

Expected: commit succeeds.

### Task 6: Close Evidence, Regenerate Indexes, Validate, and Commit

**Files:**

- Modify: `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
- Modify: `docs/00.agent-governance/memory/progress.md`
- Modify: `docs/90.references/llm-wiki/llm-wiki-index.md`
- Read: `AGENTS.md`

- [ ] **Step 1: Regenerate LLM Wiki index**

Run:

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh
```

Expected: command exits 0 and reports the generated
`docs/90.references/llm-wiki/llm-wiki-index.md` path count.

- [ ] **Step 2: Run final validation**

Run:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash -n scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-repo-contracts.sh
```

Expected:

- The first six commands pass.
- Full repo contract has no audit, reference, provider, LLM Wiki, Stage 99, or
  document-contract failures.
- Full repo contract may still fail only on known out-of-scope infra hardening
  and tech-stack expected-image drift.

- [ ] **Step 3: Attempt graph refresh only if code files changed**

Run:

```bash
if git diff --name-only HEAD | rg -q '(^scripts/|\.sh$|\.py$|\.js$|\.ts$|\.tsx$|\.go$|\.rs$|\.java$)'; then
  graphify update .
else
  printf 'graphify not required: no code files changed\n'
fi
```

Expected:

- If no code files changed, the command prints `graphify not required: no code
  files changed`.
- If code files changed and `graphify` is unavailable, record the skip in task
  evidence.

- [ ] **Step 4: Close task evidence**

In `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`:

- Change top frontmatter `status` to `completed`.
- Mark `T-006` as `Done`.
- Fill `## Validation Results` with pass/fail summaries.
- Replace `Pending` in `## Commit Trail` with the task commit hashes.
- Record known infra drift as out of scope if full repo contract still fails
  only there.

- [ ] **Step 5: Update progress memory**

Add a new top row to `docs/00.agent-governance/memory/progress.md`:

```markdown
| 2026-07-03 | Workspace document contract audit pack implementation | Done | Executed the approved audit pack without target corpus normalization. Created document-contract audit reports for inventories, governance comparison, template gaps, automation coverage, and gap disposition. | N/A | Checks PASS: `git diff --check`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check`; `bash scripts/operations/sync-provider-surfaces.sh --check`; `bash scripts/validation/check-doc-traceability.sh`; `bash scripts/validation/check-doc-implementation-alignment.sh`; `bash -n scripts/validation/check-repo-contracts.sh`. Full repo contract has no audit/reference/provider/LLM Wiki failures and still fails only on known out-of-scope infra drift if unchanged. |
```

If actual validation differs, adjust the row to match measured results.

- [ ] **Step 6: Run final post-close checks**

Run:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash -n scripts/validation/check-repo-contracts.sh
```

Expected: all commands exit 0.

- [ ] **Step 7: Commit Task 6**

Run:

```bash
git add docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md docs/00.agent-governance/memory/progress.md docs/90.references/llm-wiki/llm-wiki-index.md
git commit -m "docs(audits): Close document contract audit evidence"
```

Expected: commit succeeds.

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-WDC-PLAN-001 | Structural | Plan and task evidence use canonical Stage 04 paths. | `test -f docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md && test -f docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md` | Both files exist after Task 1. |
| VAL-WDC-PLAN-002 | Reference | Audit reports live under the Stage 90 audit category. | `test -d docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack` | Directory exists after Task 1. |
| VAL-WDC-PLAN-003 | Template Hygiene | Audit report files do not retain illustrative template rows. | `rg -n 'sample row|example row|measured gap|measured finding|illustrative row' docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack` | No matches after each report is finalized. |
| VAL-WDC-PLAN-004 | Provider Sync | Provider mirrors have no generated drift. | `bash scripts/operations/sync-provider-surfaces.sh --check` | Exit 0. |
| VAL-WDC-PLAN-005 | LLM Wiki | Generated tracked path index is fresh. | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Exit 0 after Task 6 regeneration. |
| VAL-WDC-PLAN-006 | Traceability | Stage 04 task and plan routing stays synchronized. | `bash scripts/validation/check-doc-traceability.sh` | Exit 0 with `failures=0`. |
| VAL-WDC-PLAN-007 | Implementation Alignment | Active docs link to tracked implementation surfaces. | `bash scripts/validation/check-doc-implementation-alignment.sh` | Exit 0 with `failures=0`. |
| VAL-WDC-PLAN-008 | Repo Contract Syntax | Repository contract script remains syntactically valid. | `bash -n scripts/validation/check-repo-contracts.sh` | Exit 0. |
| VAL-WDC-PLAN-009 | Full Repo Contract | Audit changes do not introduce new contract failures. | `bash scripts/validation/check-repo-contracts.sh` | Passes, or fails only on previously known out-of-scope infra drift. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Inventory output is too large to paste into reports. | Medium | Summarize counts, representative examples, and commands; do not paste raw long logs. |
| Stale template references are historical evidence, not active drift. | High | Classify each match before proposing edits and record historical evidence separately. |
| Secret documentation paths are accidentally inspected too deeply. | High | Inspect tracked Markdown structure and path metadata only; do not read secret values or `.env` contents. |
| Full repo contract still fails on infra drift. | Medium | Record known infra hardening and tech-stack expected-image drift as out of scope. |
| README reports become policy surfaces. | Medium | Keep durable rules in Stage 00 and Stage 99 support docs; README files route to reports only. |
| Future batches try to mix too many fixes. | Medium | Gap register groups future work by surface and commit boundary. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: All report files pass template-marker scans and
  `git diff --check`.
- **Sandbox / Canary Rollout**: N/A; this plan writes documentation reports
  only and does not change runtime behavior.
- **Human Approval Gate**: Required before executing any future batch that
  modifies target corpus files, validators, provider runtime configuration,
  remote GitHub settings, or infra versions.
- **Rollback Trigger**: Revert the task-specific commit if a report records
  secret values, rewrites historical evidence, or claims enforcement without
  workflow or validator evidence.
- **Prompt / Model Promotion Criteria**: N/A; no model or prompt artifact is
  promoted by this audit pack.

## Completion Criteria

- [ ] Task evidence exists and records all six tasks.
- [ ] Audit bundle exists under `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/`.
- [ ] Frontmatter, section, README, governance, template-gap, automation, and
      gap-register reports are complete.
- [ ] No target corpus normalization is mixed into this audit pack.
- [ ] LLM Wiki index is regenerated and fresh.
- [ ] Required validation commands pass, or full repo contract fails only on
      known out-of-scope infra drift.
- [ ] Work is committed in logical task-level commits.

## Related Documents

- **Spec**: [Workspace document contract audit pack spec](../../03.specs/102-workspace-document-contract-audit-pack/spec.md)
- **Future Task Path**: `docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md`
- **Audit references**: [Audit references](../../90.references/audits/README.md)
- **Template contract**: [Template contract](../../99.templates/support/template-contract.md)
- **Frontmatter contract**: [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- **Template governance**: [Template governance](../../99.templates/support/template-governance.md)
- **Template selection**: [Template selection](../../99.templates/support/template-selection.md)
- **Stage authoring matrix**: [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
