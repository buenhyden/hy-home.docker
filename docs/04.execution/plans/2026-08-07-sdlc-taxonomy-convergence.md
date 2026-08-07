---
status: draft
artifact_id: plan:2026-08-07-sdlc-taxonomy-convergence
artifact_type: plan
parent_ids:
  - spec:136-sdlc-taxonomy-convergence
---

# SDLC Taxonomy Convergence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development`
> (recommended) or `superpowers:executing-plans` to implement this plan
> task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

## Overview

This plan executes waves W1 through W5 of
[specification 136](../../03.specs/136-sdlc-taxonomy-convergence/spec.md): the
structural convergence chain. It repairs the enforcement layer, realigns the
template contract onto the measured corpus, establishes the content archive and
migrates 267 terminal documents, collapses Stage 04 into Stage 03 by
co-location, and renumbers Stage 05 to Stage 04.

**Goal:** Produce a contiguous `00`–`04` active stage sequence in which every
specification directory holds its own durable contract and execution record, and
in which the heading contract actually fires.

**Architecture:** Five sequential waves, each gated on the previous one. W1
changes no document content and only repairs contracts, so that every later wave
has a sound checker to attribute violations against. W2 corrects the contract to
describe the corpus that exists. W3 empties the active stages of terminal work.
W4 collapses the near-empty Stage 04 into Stage 03. W5 renumbers last, so no
path is rewritten twice.

**Tech Stack:** Bash, Python 3, `git mv`, the repository validators under
`scripts/validation/`, and the Stage 99 registry at
`docs/99.templates/support/document-metadata-profiles.yaml`.

Waves W6 through W9 (ARD/ADR vocabulary, date policy, rule consolidation, script
consolidation) are deliberately excluded. They operate on paths that W4 and W5
change, so their steps are authored after W5 lands.

## Context and Inputs

### Global constraints

Every task inherits these. They are copied verbatim from the specification and
from Stage 00 governance.

- `docs/00.agent-governance/` is English-only. Governance-meta Stage 03 and
  Stage 04 documents are English; all sibling documents in this lane carry zero
  Korean characters.
- Commit per logical unit. A wave is never one commit unless it contains one
  logical unit.
- Never write plaintext credentials. Never run `pre-commit run --all-files`
  directly; use `scripts/validation/run-agent-precommit-all-files.sh` only at an
  approved final gate.
- Architecture decision records are never relocated. Supersession is a status
  change plus a `superseded-by` link, applied in place.
- No push to any remote. No change to Compose service topology, images, or
  secrets.
- Every wave re-runs `bash scripts/validation/check-repo-contracts.sh` and
  compares against the baseline captured in Task 1.

### Measured starting state

| Subject                                      | Value                                                      |
| :------------------------------------------- | :--------------------------------------------------------- |
| Stage 03 specification directories           | 59: 41 `completed`, 16 `active`, 1 `superseded`, 1 `draft` |
| Stage 04 leaf documents                      | 231: 225 `completed`, 6 `active`                           |
| Documents to archive                         | 267                                                        |
| Active execution documents to co-locate      | 6, resolving to 4 subjects                                 |
| Stage 05 leaf documents                      | 192 across 77 subjects; 71 additional `README.md` files    |
| Heading violations under the current checker | 0 — the checker is inoperative                             |
| Heading violations under the fixed checker   | 2                                                          |
| `05.operations` literal occurrences          | 3,274 across 597 files                                     |

### The two heading violations W1 exposes

Both are documents that followed the registry vocabulary while the corpus
follows the protocol vocabulary. Under specification D2 the corpus wins, so both
documents are migrated toward the majority rather than the contract being bent
toward them.

| Document                                                                    | Carries                        | Corpus majority                |
| :-------------------------------------------------------------------------- | :----------------------------- | :----------------------------- |
| `docs/05.operations/guides/00-workspace/harness-agent-first-engineering.md` | `## Routine Usage`             | `## Usage`, 65 documents       |
| `docs/05.operations/runbooks/00-workspace/llm-wiki-maintenance.md`          | `## Trigger and Preconditions` | `## When to Use`, 61 documents |

### Archive model refinement

Specification D4 rule 1 requires a forward pointer at every archived document's
original location. W4 removes `docs/04.execution/` entirely, so leaving 231
tombstones inside a directory that is then deleted is self-contradictory. The
rule's purpose is preventing link breakage. This plan therefore splits it by
whether the source stage survives.

| Source stage         | Survives W4? | Mechanism                                        |
| :------------------- | :----------- | :----------------------------------------------- |
| `docs/03.specs/`     | Yes          | Forward-pointer tombstone at the original path   |
| `docs/04.execution/` | No           | Inbound link rewrite plus archive ledger mapping |

Both templates already exist and need no authoring:
`docs/99.templates/templates/common/archive.template.md` for tombstones and
`docs/99.templates/templates/common/content-archive.template.md` for preserved
content.

## Goals and Non-goals

### Goals

- The operations heading contract fires on real violations and passes a corpus
  that satisfies it.
- Template conformance rises from the measured 88 of 631.
- Active stages hold only non-terminal work.
- Each surviving specification directory holds `spec.md` plus its `plan.md` and
  `task.md`.
- The active stage sequence is contiguous `00` through `04`.
- Zero broken relative links at the end of every wave.

### Non-goals

- Backfilling `artifact_id` and `parent_ids` into documents that lack them.
- Retro-creating specifications for terminal orphan execution documents.
- Adding Diátaxis tutorial or explanation document types.
- Changing what any Prometheus alert rule controls. Only documentation paths
  inside annotations change.
- Renaming `docs/00.agent-governance/agents/agents/`. Specification D10 retains
  it; 41 files and 5 test modules reference the path.

## Work Breakdown

### Wave W1 — Contract and enforcement repair

No document is moved in this wave. Corpus content changes only for the two
documents Task 2 migrates.

---

#### Task 1: Capture the baseline

**Files:**

- Create: `/tmp/claude-1000/sdlc-convergence/baseline.txt` (scratch, not committed)

**Interfaces:**

- Produces: the failure count every later task compares against.

- [ ] **Step 1: Record the repository contract baseline**

```bash
cd /home/hy/projects/hy-home.docker
mkdir -p /tmp/claude-1000/sdlc-convergence
bash scripts/validation/check-repo-contracts.sh > /tmp/claude-1000/sdlc-convergence/baseline.txt 2>&1
echo "exit=$?"
grep -c '^FAIL' /tmp/claude-1000/sdlc-convergence/baseline.txt || true
tail -5 /tmp/claude-1000/sdlc-convergence/baseline.txt
```

Expected: a non-zero failure count. Record the exact number. The specification's
first revision recorded `failures=4`; the current tree may differ. **The number
you record here, not the number in the specification, is the baseline.**

- [ ] **Step 2: Record the full-corpus metadata baseline**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-active \
  > /tmp/claude-1000/sdlc-convergence/metadata-baseline.txt 2>&1
tail -3 /tmp/claude-1000/sdlc-convergence/metadata-baseline.txt
```

Expected: a `selected=... violations=N` summary line. Record `N`.

- [ ] **Step 3: Record the link baseline**

```bash
python3 - <<'PY' > /tmp/claude-1000/sdlc-convergence/links-baseline.txt
import pathlib, re
broken = []
for p in pathlib.Path("docs").rglob("*.md"):
    in_fence = False
    for line in p.read_text(errors="ignore").splitlines():
        # Toggle only on a line that STARTS a fence. Counting backtick runs
        # inside the whole text breaks on any code that contains backticks --
        # including this check itself.
        if line.lstrip().startswith("`" * 3):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in re.finditer(r"\]\(([^)]+)\)", line):
            target = m.group(1).split("#")[0]
            if not target or target.startswith(("http", "mailto:")):
                continue
            if not (p.parent / target).exists():
                broken.append(f"{p}: {target}")
print(len(broken))
print("\n".join(broken))
PY
head -1 /tmp/claude-1000/sdlc-convergence/links-baseline.txt
```

Expected: `1`. The single real defect is `../guides/...` in
`docs/00.agent-governance/memory/progress.md`, an ellipsis in prose rather than
a link. Record the number. No commit in this task.

The fence guard is not optional. Without it this check reports 8, of which 7 are
markdown links inside illustrative code blocks — including the tombstone
template in Task 13 and the rule snippets in Task 16. A baseline inflated by
your own plan's example content makes every later link comparison meaningless.
This is the same defect class as the substring matching Task 2 repairs.

---

#### Task 2: Repair the heading checker and migrate the two exposed documents

This is the single most important task in the plan. The two edits must land
together: line-anchoring alone makes all 62 runbooks fail, because the runbook
required list is the only one missing its `##` prefix.

**Files:**

- Modify: `scripts/validation/check-repo-contracts.sh:602-604` and `:673-677`
- Modify: `docs/05.operations/guides/00-workspace/harness-agent-first-engineering.md`
- Modify: `docs/05.operations/runbooks/00-workspace/llm-wiki-maintenance.md`

**Interfaces:**

- Consumes: the baseline from Task 1.
- Produces: a heading checker that matches whole stripped lines. Every later
  wave relies on this to attribute violations.

- [ ] **Step 1: Prove the defect before fixing it**

```bash
cd /home/hy/projects/hy-home.docker
python3 - <<'PY'
t = open("docs/05.operations/guides/00-workspace/harness-agent-first-engineering.md").read()
print("substring '## Usage' present:", "## Usage" in t)
print("line '## Usage' present:", "## Usage" in {l.strip() for l in t.splitlines()})
print("the culprit line:", [l for l in t.splitlines() if l.strip() == "### Usage Type"][:1])
PY
```

Expected output:

```text
substring '## Usage' present: True
line '## Usage' present: False
the culprit line: ['### Usage Type']
```

This is the defect: `### Usage Type` contains the substring `## Usage` starting
at index 1.

- [ ] **Step 2: Fix the runbook required list to carry `##` prefixes**

In `scripts/validation/check-repo-contracts.sh`, replace this line:

```python
    "runbooks": ["When to Use", "Procedure", "Evidence", "Escalation"],
```

with:

```python
    "runbooks": ["## When to Use", "## Procedure", "## Evidence", "## Escalation"],
```

- [ ] **Step 3: Replace substring matching with stripped-line matching**

In the same heredoc, replace this block:

```python
        for literal in required[bucket]:
            if literal not in text:
                failures.append(f"{path}: missing {bucket} profile heading: {literal}")
        for literal in forbidden[bucket]:
            if literal in text:
                failures.append(f"{path}: {bucket} document contains cross-profile heading: {literal}")
```

with:

```python
        heading_lines = {line.strip() for line in text.splitlines()}
        for literal in required[bucket]:
            if literal not in heading_lines:
                failures.append(f"{path}: missing {bucket} profile heading: {literal}")
        for literal in forbidden[bucket]:
            if literal in heading_lines:
                failures.append(f"{path}: {bucket} document contains cross-profile heading: {literal}")
```

- [ ] **Step 4: Run the checker and confirm exactly two failures appear**

```bash
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep 'profile heading'
```

Expected exactly two lines:

```text
FAIL: docs/05.operations/guides/00-workspace/harness-agent-first-engineering.md: missing guides profile heading: ## Usage
FAIL: docs/05.operations/runbooks/00-workspace/llm-wiki-maintenance.md: missing runbooks profile heading: ## When to Use
```

If you see 63 failures, Step 2 was not applied. If you see 0, Step 3 was not
applied. Do not continue until you see exactly these two.

- [ ] **Step 5: Migrate the guide to the corpus majority heading**

In `docs/05.operations/guides/00-workspace/harness-agent-first-engineering.md`,
change the heading `## Routine Usage` to `## Usage`. Leave `### Usage Type` and
every other heading untouched.

- [ ] **Step 6: Migrate the runbook to the corpus majority heading**

In `docs/05.operations/runbooks/00-workspace/llm-wiki-maintenance.md`, change
the heading `## Trigger and Preconditions` to `## When to Use`. Leave
`## Verification Record`, `## Rollback or Recovery`, and every other heading
untouched — they are not in the required or forbidden lists for runbooks.

- [ ] **Step 6b: Retarget the two registry headings these migrations depend on**

Two checkers enforce headings from different sources. `check-repo-contracts.sh`
reads the protocol vocabulary; `check-document-metadata.py` reads the registry
at `docs/99.templates/support/document-metadata-profiles.yaml`. Steps 5 and 6
moved two documents to the protocol vocabulary, so until the registry agrees the
metadata checker reports them as deficits and this task leaves the tree red.

The end state is already decided by specification D2 and is not in question:
`## Usage` carries 65 documents against 1, and `## When to Use` carries 61
against 2. Task 9 retargets the full operations registry. The two headings these
migrations depend on move here so that this task closes green.

Under `guide:` replace:

```yaml
required_headings:
  [
    '## Overview',
    '## Audience and Prerequisites',
    '## Routine Usage',
    '## Common Checks',
    '## Runbook Handoff',
    '## Related Documents',
  ]
```

with:

```yaml
required_headings:
  [
    '## Overview',
    '## Audience and Prerequisites',
    '## Usage',
    '## Common Checks',
    '## Runbook Handoff',
    '## Related Documents',
  ]
```

Under `runbook:` replace:

```yaml
required_headings:
  [
    '## Overview',
    '## Trigger and Preconditions',
    '## Procedure',
    '## Verification Record',
    '## Evidence',
    '## Rollback or Recovery',
    '## Escalation',
    '## Related Documents',
  ]
```

with:

```yaml
required_headings:
  [
    '## Overview',
    '## When to Use',
    '## Procedure',
    '## Verification Record',
    '## Evidence',
    '## Rollback or Recovery',
    '## Escalation',
    '## Related Documents',
  ]
```

Change nothing under `policy:` — Task 9 owns that one, along with the template
bodies and the conditional-scope removal.

- [ ] **Step 6c: Confirm both checkers now agree**

```bash
python3 -c "import yaml; yaml.safe_load(open('docs/99.templates/support/document-metadata-profiles.yaml')); print('yaml ok')"
python3 scripts/validation/check-document-metadata.py --mode check-changed 2>&1 | tail -1
```

Expected: `violations=0`. If it still reports the two documents, the registry
edit did not take.

- [ ] **Step 7: Confirm the heading contract now passes cleanly**

```bash
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep -c 'profile heading' || echo 0
```

Expected: `0`.

- [ ] **Step 8: Confirm no baseline regression**

```bash
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep -c '^FAIL' || echo 0
```

Expected: less than or equal to the Task 1 baseline. The heading repair removes
no pre-existing failure, so the count should be unchanged.

- [ ] **Step 9: Commit**

```bash
git add scripts/validation/check-repo-contracts.sh \
        docs/05.operations/guides/00-workspace/harness-agent-first-engineering.md \
        docs/05.operations/runbooks/00-workspace/llm-wiki-maintenance.md
git commit -m "fix(validation): anchor operations heading checks to whole lines

The heading contract tested \`literal not in text\`, a substring match against
the whole document. \`### Usage Type\` therefore satisfied the \`## Usage\`
requirement and the check passed a corpus containing two real violations.

Anchor both the required and forbidden checks to stripped lines, and add the
missing \`##\` prefixes to the runbooks required list. Without the second edit
line anchoring fails all 62 runbooks.

Migrate the two exposed documents to the corpus majority vocabulary per
specification D2: \`## Routine Usage\` to \`## Usage\` (65 documents) and
\`## Trigger and Preconditions\` to \`## When to Use\` (61 documents)."
```

---

#### Task 3: Withdraw the `archived` retired-alias contradiction

**Files:**

- Modify: `docs/00.agent-governance/rules/documentation-protocol.md:94-95`

**Interfaces:**

- Consumes: nothing.
- Produces: an unambiguous status vocabulary that W3 relies on when it writes
  `status: archived` into 267 documents.

- [ ] **Step 1: Confirm the contradiction**

```bash
sed -n '87,88p;94,95p' docs/00.agent-governance/rules/documentation-protocol.md
```

Expected: line 88 mandates `status: archived`; line 95 lists `archived` as a
retired alias that must be normalized when found.

- [ ] **Step 2: Remove `archived` from the retired-alias list**

Replace:

```markdown
A document without this frontmatter is **INCOMPLETE**. Retired aliases such
as `approved`, `done`, and `archived` must be normalized when found.
```

with:

```markdown
A document without this frontmatter is **INCOMPLETE**. Retired aliases such
as `approved` and `done` must be normalized when found. `archived` is a
current status value, required by the archive profile, and is never
normalized away.
```

- [ ] **Step 3: Confirm the archive profile still permits the value**

```bash
grep -n 'allowed_statuses' docs/99.templates/support/document-metadata-profiles.yaml | grep -i archive
```

Expected: at least one line permitting `archived`.

- [ ] **Step 4: Verify and commit**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
git add docs/00.agent-governance/rules/documentation-protocol.md
git commit -m "docs(governance): withdraw the archived retired-alias contradiction

Line 88 mandates \`status: archived\` for archive tombstones while line 95
listed \`archived\` among retired aliases requiring normalization. The two
statements are seven lines apart and mutually exclusive.

\`archived\` is a current status value required by the archive profile."
```

---

#### Task 4: Retarget the `audit` role onto its corpus

The plan's first revision of this task prescribed `forbidden_headings: []`. That
is structurally impossible: `check-document-metadata.py:4288` rejects an empty
list, and `role.get(heading_key)` returning `None` fails the same check, so
deleting the key is rejected too. Both exits are closed.

Measurement then showed the real problem is larger than a vacuous forbidden
rule. All 34 audit documents carry an identical heading set, and it is the
`reference` set — not the `audit` set:

| Heading                                                                                                                   | Audit documents carrying it |
| :------------------------------------------------------------------------------------------------------------------------ | :-------------------------- |
| `## Overview`, `## Purpose`, `## Scope`, `## Definitions / Facts`, `## Sources`, `## Maintenance`, `## Related Documents` | 34 of 34                    |
| `## Repository Role`                                                                                                      | 34 of 34                    |
| `## Scope and Criteria`, `## Gap Analysis`, `## Disposition` (audit-role required)                                        | 0 of 34                     |

Retiring the role was considered and rejected: 17 documents declare
`artifact_type: audit`, and two dedicated validators
(`scripts/validation/audit_criterion_contract.py`,
`scripts/validation/check-agentic-audit-semantic-freshness.py`) plus several
Stage 99 support contracts depend on the type.

This task therefore retargets the role onto its corpus per specification D2 and
absorbs what was previously Task 10.

**Files:**

- Modify: `docs/99.templates/support/document-metadata-profiles.yaml`, `audit:` role
- Modify: `docs/99.templates/templates/common/audit.template.md`

**Interfaces:**

- Consumes: nothing.
- Produces: an `audit` role whose conforming count rises from 0 toward 34.

- [ ] **Step 1: Confirm the measurement before changing anything**

```bash
cd /home/hy/projects/hy-home.docker
python3 - <<'PY'
import pathlib, collections
docs = [p for p in pathlib.Path('docs/90.references/audits').rglob('*.md')
        if p.name != 'README.md']
c = collections.Counter()
for p in docs:
    for line in p.read_text(errors='ignore').splitlines():
        if line.startswith('## '):
            c[line.strip()] += 1
print("audit documents:", len(docs))
for h, k in c.most_common(10):
    print(f"  {k:3}/{len(docs)}  {h}")
PY
```

Expected: 34 documents, with eight headings at 34/34. If the universal set is
not eight headings at 34/34, stop and report — the retarget below assumes it.

- [ ] **Step 2: Confirm the forbidden candidates are absent**

```bash
python3 - <<'PY'
import pathlib
docs = [p for p in pathlib.Path('docs/90.references/audits').rglob('*.md')
        if p.name != 'README.md']
for h in ("## Procedure", "## Controls", "## Usage"):
    n = sum(1 for p in docs
            if any(l.strip() == h for l in p.read_text(errors='ignore').splitlines()))
    print(f"  {n:3}/{len(docs)}  {h}")
PY
```

Expected: `0/34` for all three. These mark a document as an operations artifact
rather than an audit, so forbidding them catches a genuine misfile instead of
never firing.

- [ ] **Step 3: Retarget the `audit` role**

In `docs/99.templates/support/document-metadata-profiles.yaml`, under `audit:`,
replace the three heading lists with:

```yaml
required_headings:
  [
    '## Overview',
    '## Purpose',
    '## Repository Role',
    '## Scope',
    '## Definitions / Facts',
    '## Sources',
    '## Maintenance',
    '## Related Documents',
  ]
conditional_headings:
  ['## Findings', '## Method', '## Source Rules', '## Evidence Snapshot Boundary', '## Comparison']
forbidden_headings: ['## Procedure', '## Controls', '## Usage']
```

All three lists are non-empty, every entry starts with `## `, and no list
contains a duplicate — the three conditions `check-document-metadata.py:4288`
and `:4297` enforce.

- [ ] **Step 4: Update the template body to match**

Rewrite the heading list in
`docs/99.templates/templates/common/audit.template.md` to the eight required
headings from Step 3, in that order, keeping exactly one `## Related Documents`
as the final heading.

- [ ] **Step 5: Verify the role loads and the conforming count rose**

```bash
python3 -c "import yaml; d=yaml.safe_load(open('docs/99.templates/support/document-metadata-profiles.yaml')); r=d['template_roles']['audit']; print({k: r[k] for k in ('required_headings','conditional_headings','forbidden_headings')})"
python3 scripts/validation/check-document-metadata.py --mode check-changed 2>&1 | tail -1
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep -c '^FAIL'
```

Expected: the three lists print as set in Step 3; `violations=0`; `2` contract
failures. A `configuration-error: template role audit ... must be a non-empty
H2 heading list` means one of the three lists came out empty — fix it before
continuing.

- [ ] **Step 6: Commit**

```bash
git add docs/99.templates/support/document-metadata-profiles.yaml \
        docs/99.templates/templates/common/audit.template.md
git commit -m "docs(templates): retarget the audit role onto its corpus

34 audit documents exist and none satisfied the audit heading contract. The
required headings were never the ones audit authors write: all 34 carry the
reference heading set plus ## Repository Role, and zero carry ## Scope and
Criteria, ## Gap Analysis, or ## Disposition.

The role is retained rather than retired. 17 documents declare
artifact_type: audit, and audit_criterion_contract.py,
check-agentic-audit-semantic-freshness.py, and several Stage 99 support
contracts depend on the type.

forbidden_headings could not be emptied: check-document-metadata.py:4288
rejects an empty list and a missing key alike. It is retargeted to three
operations headings, each carried by 0 of 34 documents, so the rule catches a
misfiled operations document instead of never firing."
```

#### Task 5: Document the enforced `reviewed_at` and `review_cycle` fields

**Files:**

- Modify: `docs/99.templates/support/frontmatter-contract.md`

**Interfaces:**

- Consumes: nothing.
- Produces: documentation for two fields the policy, runbook, and postmortem
  profiles already require.

- [ ] **Step 1: Confirm the fields are enforced but undocumented**

```bash
grep -n 'reviewed_at\|review_cycle' docs/99.templates/support/document-metadata-profiles.yaml | head
grep -c 'reviewed_at\|review_cycle' docs/99.templates/support/frontmatter-contract.md || echo 0
```

Expected: the registry lists both fields as required for the policy and runbook
profiles and `reviewed_at` for postmortem; the contract document mentions them
zero times.

- [ ] **Step 2: Add a section documenting both fields**

Insert the following before the `## Related Documents` heading of
`docs/99.templates/support/frontmatter-contract.md`:

```markdown
## Review Fields

Two fields are required by the `policy`, `runbook`, and `postmortem` profiles
and are enforced by
[`document-metadata-profiles.yaml`](./document-metadata-profiles.yaml).

| Field          | Type         | Required by                 | Meaning                                                  |
| :------------- | :----------- | :-------------------------- | :------------------------------------------------------- |
| `reviewed_at`  | `YYYY-MM-DD` | policy, runbook, postmortem | Date the document's content was last confirmed accurate. |
| `review_cycle` | string       | policy, runbook             | Cadence or trigger governing the next review.            |

`review_cycle` accepts either a fixed cadence such as `quarterly` or an
event trigger such as `on-source-change`. A document whose `reviewed_at`
predates its cadence is stale, but staleness is not currently a blocking check.
```

- [ ] **Step 3: Verify and commit**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
git add docs/99.templates/support/frontmatter-contract.md
git commit -m "docs(templates): document the enforced review fields

\`reviewed_at\` and \`review_cycle\` are required by the policy, runbook, and
postmortem profiles and drive real findings, yet the document designated as the
frontmatter interpreter never mentioned them.

Undocumented enforcement is now documented."
```

---

#### Task 6: Resolve the duplicate lifecycle declaration

**Files:**

- Modify: `docs/00.agent-governance/rules/agentic.md:74-76`

**Interfaces:**

- Consumes: nothing.
- Produces: one lifecycle statement. `task-checklists.md:75-77` already binds
  provider adapters to the `workflows.md` formulation.

- [ ] **Step 1: Confirm both files declare a singular lifecycle**

```bash
sed -n '74,76p' docs/00.agent-governance/rules/agentic.md
sed -n '92,93p' docs/00.agent-governance/rules/workflows.md
sed -n '75,77p' docs/00.agent-governance/rules/task-checklists.md
```

Expected: `agentic.md` says "The sole lifecycle is" and lists 8 phases;
`workflows.md` says "The exact provider-neutral lifecycle is" and lists 5;
`task-checklists.md` binds adapters to the `workflows.md` formulation.

- [ ] **Step 2: Demote the `agentic.md` statement to a reference**

Replace:

```markdown
- The sole lifecycle is
  `discover -> design/plan -> approval -> implement -> validate ->
independent-review -> evidence -> handoff`.
```

with:

```markdown
- The lifecycle is owned by
  [`workflows.md`](./workflows.md). This rule adds no second sequence; the
  agent-first phases `discover -> design/plan -> approval -> implement ->
validate -> independent-review -> evidence -> handoff` describe agent
  behavior within that lifecycle, not a competing one.
```

- [ ] **Step 3: Verify no other file claims a third lifecycle**

```bash
grep -rn 'sole lifecycle\|exact provider-neutral lifecycle\|the lifecycle is' \
  docs/00.agent-governance/rules/
```

Expected: exactly one authoritative declaration, in `workflows.md`.

- [ ] **Step 4: Verify and commit**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
git add docs/00.agent-governance/rules/agentic.md
git commit -m "docs(governance): resolve the duplicate lifecycle declaration

agentic.md declared an 8-phase lifecycle as 'the sole lifecycle' while
workflows.md declared a 5-phase one as 'the exact provider-neutral lifecycle'.
Both claimed singularity and the two sequences differ.

task-checklists.md already binds provider adapters to the workflows.md
formulation, so the agentic.md sequence had no downstream consumer. It is
demoted to a description of agent behavior within the owned lifecycle."
```

---

#### Task 7: Correct the stale fixture and regression counts

**Files:**

- Modify: `docs/00.agent-governance/rules/quality-standards.md:61-63`

**Interfaces:**

- Consumes: nothing.
- Produces: a completion gate whose numbers match the fixture catalog.

- [ ] **Step 1: Derive the ground truth**

```bash
python3 - <<'PY'
import re
s = open('docs/90.references/data/governance/agent-output-eval-fixtures.md').read()
fixtures = sorted({i for i in re.findall(r'AOE-[A-Z]+-\d+', s) if '-REG-' not in i})
regressions = sorted(set(re.findall(r'AOE-REG-\d+', s)))
print("fixtures:", len(fixtures))
print("regressions:", len(regressions))
PY
```

Expected: `fixtures: 11`, `regressions: 16`.

- [ ] **Step 2: Confirm the two rule files disagree**

```bash
sed -n '61,63p' docs/00.agent-governance/rules/quality-standards.md
sed -n '51,53p' docs/00.agent-governance/rules/postflight-checklist.md
```

Expected: `quality-standards.md` says eight and ten; `postflight-checklist.md`
says 11 and 16. The latter matches ground truth.

- [ ] **Step 3: Correct the stale counts**

In `docs/00.agent-governance/rules/quality-standards.md`, replace:

```markdown
6. For agent-harness changes, require all eight fixture catalog entries, all ten
   deterministic regressions, `fixtures_check=pass`, and
   `regressions_check=pass` without a network model call.
```

with:

```markdown
6. For agent-harness changes, require all 11 fixture catalog entries, all 16
   deterministic regressions, `fixtures_check=pass`, and
   `regressions_check=pass` without a network model call.
```

- [ ] **Step 4: Verify no other file carries the stale numbers**

```bash
grep -rn 'eight fixture\|ten deterministic' docs/00.agent-governance/
```

Expected: no output.

- [ ] **Step 5: Verify and commit**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
git add docs/00.agent-governance/rules/quality-standards.md
git commit -m "fix(governance): correct stale fixture and regression counts

quality-standards.md required eight fixtures and ten regressions;
postflight-checklist.md required 11 and 16. The fixture catalog holds 11
distinct AOE fixtures and 16 AOE-REG regressions, so postflight-checklist.md
was correct and quality-standards.md was stale by three and six."
```

---

#### Task 8: Close W1 and confirm the wave gate

**Files:** none modified.

- [ ] **Step 1: Run the full gate**

```bash
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep -c '^FAIL' || echo 0
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
```

Expected: failure count at or below the Task 1 baseline; `violations=0` on
changed documents; traceability zero failures.

- [ ] **Step 2: Confirm no document was moved**

```bash
git diff --name-status 19ee4727..HEAD -- docs/ | grep -c '^R' || echo 0
```

Expected: `0` renames in W1. If non-zero, a task exceeded its boundary.

---

### Wave W2 — Template retargeting onto the corpus

Precondition: W1 complete. The checker must be sound before the contract is
rewritten, or the effect of the rewrite cannot be measured.

---

#### Task 9: Retarget the operations heading registry to the corpus vocabulary

**Files:**

- Modify: `docs/99.templates/support/document-metadata-profiles.yaml:361-381`
- Modify: `docs/99.templates/templates/operations/guide.template.md`
- Modify: `docs/99.templates/templates/operations/policy.template.md`
- Modify: `docs/99.templates/templates/operations/runbook.template.md`

**Interfaces:**

- Consumes: the sound checker from Task 2.
- Produces: a registry whose `required_headings` match the 61-to-65 document
  majority. Task 13's archive migration relies on this to avoid mass violations.

- [ ] **Step 1: Measure the split before changing anything**

```bash
cd docs/05.operations
for pair in "guides:## Usage:## Routine Usage" \
            "policies:## Policy Scope:## Scope" \
            "runbooks:## When to Use:## Trigger and Preconditions"; do
  b=${pair%%:*}; rest=${pair#*:}; legacy=${rest%%:*}; registry=${rest#*:}
  nl=$(grep -rl "^${legacy}$" $b --include='*.md' | grep -v README | wc -l)
  nr=$(grep -rl "^${registry}$" $b --include='*.md' | grep -v README | wc -l)
  echo "$b  legacy '$legacy'=$nl   registry '$registry'=$nr"
done
cd /home/hy/projects/hy-home.docker
```

Expected: `guides 65 vs 1`, `policies 63 vs 1`, `runbooks 61 vs 2`. Each ratio
must exceed the 61:1 threshold specification D2 sets before the corpus is
promoted. If any ratio is below it, stop and escalate.

> **Already applied in Task 2 Step 6b:** the `guide` and `runbook`
> `required_headings` were retargeted there, because Task 2's document
> migrations would otherwise leave the metadata checker red. Steps 2 and 4 below
> are therefore verification steps in this task, not edits. Confirm each value
> matches and move on. Step 3 (`policy`) is a real edit and has not been applied.

- [ ] **Step 2: Verify the `guide` role was retargeted**

In `docs/99.templates/support/document-metadata-profiles.yaml`, under `guide:`,
replace:

```yaml
required_headings:
  [
    '## Overview',
    '## Audience and Prerequisites',
    '## Routine Usage',
    '## Common Checks',
    '## Runbook Handoff',
    '## Related Documents',
  ]
```

with:

```yaml
required_headings:
  [
    '## Overview',
    '## Audience and Prerequisites',
    '## Usage',
    '## Common Checks',
    '## Runbook Handoff',
    '## Related Documents',
  ]
```

- [ ] **Step 3: Retarget the `policy` role**

Under `policy:`, replace:

```yaml
required_headings:
  [
    '## Overview',
    '## Scope',
    '## Controls',
    '## Exceptions',
    '## Verification',
    '## Review Cadence',
    '## Related Documents',
  ]
```

with:

```yaml
required_headings:
  [
    '## Overview',
    '## Policy Scope',
    '## Controls',
    '## Exceptions',
    '## Verification',
    '## Review Cadence',
    '## Related Documents',
  ]
```

- [ ] **Step 4: Verify the `runbook` role was retargeted**

Under `runbook:`, replace:

```yaml
required_headings:
  [
    '## Overview',
    '## Trigger and Preconditions',
    '## Procedure',
    '## Verification Record',
    '## Evidence',
    '## Rollback or Recovery',
    '## Escalation',
    '## Related Documents',
  ]
```

with:

```yaml
required_headings:
  [
    '## Overview',
    '## When to Use',
    '## Procedure',
    '## Verification Record',
    '## Evidence',
    '## Rollback or Recovery',
    '## Escalation',
    '## Related Documents',
  ]
```

- [ ] **Step 5: Update the three template bodies to match**

In `docs/99.templates/templates/operations/guide.template.md` change the
`## Routine Usage` heading to `## Usage`. In `policy.template.md` change
`## Scope` to `## Policy Scope`. In `runbook.template.md` change
`## Trigger and Preconditions` to `## When to Use`. Change nothing else; all
three already end with exactly one `## Related Documents`.

- [ ] **Step 6: Remove the frontmatter-conditional scope workaround**

The checker papers over the `## Scope` versus `## Policy Scope` split with a
frontmatter-conditional. With the registry retargeted, one heading is canonical
and the conditional is dead. In `scripts/validation/check-repo-contracts.sh`
replace the `if bucket == "policies":` block with:

```python
        if bucket == "policies":
            scope_count = sum(
                1 for line in text.splitlines() if line.strip() == "## Policy Scope"
            )
            if scope_count != 1:
                failures.append(
                    f"{path}: policy document must contain exactly one ## Policy Scope heading; found {scope_count}"
                )
```

- [ ] **Step 6b: Migrate the one policy outlier the repair exposes**

Removing the conditional in Step 6 exposes a document that was passing only
because the old conditional had the two heading generations backwards. It is the
single `## Scope` document from the 63:1 measurement in Step 1:

```bash
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep 'Policy Scope'
```

Expected: one failure naming
`docs/05.operations/policies/00-workspace/llm-wiki-maintenance.md`.

Change that document's `## Scope` heading to `## Policy Scope`. Change nothing
else in the file.

This is the same situation Task 2 resolved for `guide` and `runbook`: repairing
a checker exposes a real violation, and specification D2 sends the outlier to the
corpus majority rather than bending the contract to the outlier. Task 2 migrated
two documents on that basis; this migrates the third and last.

- [ ] **Step 6c: Confirm the exposure is closed**

```bash
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep -c '^FAIL'
```

Expected: `2`. A `3` means the migration did not take. Do not adjust the
expected baseline to accommodate the failure — the baseline of 2 is the two
known out-of-scope subjects, and nothing in this wave may add a third.

- [ ] **Step 6d: Complete the required-set retarget for guide and runbook**

Steps 2 through 6c retargeted only the one contested heading per role. The
remaining required headings are still registry inventions, which is why `policy`
reached 64 of 64 while `guide` stayed at 1 of 66 and `runbook` at 2 of 62.

Measured against the corpus:

| Role    | Heading                                                                                                             | Documents carrying it | Verdict                          |
| :------ | :------------------------------------------------------------------------------------------------------------------ | --------------------: | :------------------------------- |
| guide   | `## Usage`, `## Common Checks`, `## Runbook Handoff`, `## Related Documents`                                        |              66 of 66 | Keep required                    |
| guide   | `## Overview`                                                                                                       |               1 of 66 | Demote — 65:1 clears D2          |
| guide   | `## Audience and Prerequisites`                                                                                     |               1 of 66 | Demote — 65:1 clears D2          |
| runbook | `## When to Use`, `## Procedure`, `## Evidence`, `## Rollback or Recovery`, `## Escalation`, `## Related Documents` |              62 of 62 | Keep required                    |
| runbook | `## Verification Record`                                                                                            |               2 of 62 | Demote — 60:2 clears D2          |
| runbook | `## Overview`                                                                                                       |              25 of 62 | Demote — 37:25 does NOT clear D2 |

The last row is the only judgement call. At 37 against 25 neither side is
decisive, so D2 forbids promoting the corpus. Demoting to
`conditional_headings` is the one state that neither asserts a majority that
does not exist nor requires a heading 60 percent of the corpus lacks. Adding
`## Overview` to the 37 documents that lack it was considered and rejected: it
is authoring work in the opposite direction to D2.

Demote all four to `conditional_headings` — never to `forbidden_headings`,
which would break the documents that do carry them.

In `docs/99.templates/support/document-metadata-profiles.yaml`, under `guide:`:

```yaml
required_headings: ['## Usage', '## Common Checks', '## Runbook Handoff', '## Related Documents']
conditional_headings: ['## Overview', '## Audience and Prerequisites', '## Troubleshooting']
```

Under `runbook:`:

```yaml
required_headings:
  [
    '## When to Use',
    '## Procedure',
    '## Evidence',
    '## Rollback or Recovery',
    '## Escalation',
    '## Related Documents',
  ]
conditional_headings: ['## Overview', '## Verification Record']
```

Then remove the demoted headings from the two template bodies
(`guide.template.md`, `runbook.template.md`) so a newly authored document is not
told to write a heading its role no longer requires. Keep exactly one
`## Related Documents` as the final heading in each.

- [ ] **Step 6e: Confirm both roles now conform**

```bash
python3 -c "
import yaml,re,pathlib
reg=yaml.safe_load(open('docs/99.templates/support/document-metadata-profiles.yaml'))['template_roles']
for role,d in (('guide','guides'),('runbook','runbooks')):
    req=reg[role]['required_headings']
    docs=[p for p in pathlib.Path('docs/05.operations/'+d).rglob('*.md') if p.name!='README.md']
    n=sum(1 for p in docs if all(any(l.strip()==h for l in p.read_text(errors='ignore').splitlines()) for h in req))
    print(role, n, '/', len(docs))"
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep -c '^FAIL'
python3 scripts/validation/check-document-metadata.py --mode check-changed 2>&1 | tail -1
```

Expected: `guide 66 / 66`, `runbook 62 / 62`, `2` contract failures,
`violations=0`.

- [ ] **Step 7: Measure the conformance improvement**

```bash
python3 - <<'PY'
import yaml, re, glob, os

reg = yaml.safe_load(open("docs/99.templates/support/document-metadata-profiles.yaml"))
roles = reg.get("template_roles", {})
STAGES = ("docs/01", "docs/02", "docs/03", "docs/04", "docs/05", "docs/90")

total = conforming = 0
for name, spec in sorted(roles.items()):
    files = {f for g in spec.get("target_globs", []) or []
             for f in glob.glob(g, recursive=True)
             if f.endswith(".md") and os.path.isfile(f)
             and f.startswith(STAGES) and not f.endswith("README.md")}
    required = spec.get("required_headings", []) or []
    n = sum(1 for f in files
            if all(re.search("^" + re.escape(h) + r"\s*$",
                             open(f, errors="replace").read(), re.M)
                   for h in required))
    if files:
        print(f"  {name:14} {n:4} / {len(files):4}")
    total += len(files)
    conforming += n
print(f"TOTAL conforming: {conforming} / {total}")
PY
```

Expected: `guide` near 60 of 66, `policy` near 60 of 64, `runbook` near 55 of
62, and a total well above the 88 of 631 baseline. Exact figures depend on
other required headings each document may still lack; the direction is what
matters.

- [ ] **Step 8: Verify and commit**

```bash
python3 -c "import yaml; yaml.safe_load(open('docs/99.templates/support/document-metadata-profiles.yaml')); print('yaml ok')"
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep -c '^FAIL' || echo 0
python3 scripts/validation/check-document-metadata.py --mode check-changed
git add docs/99.templates/support/document-metadata-profiles.yaml \
        docs/99.templates/templates/operations/ \
        scripts/validation/check-repo-contracts.sh
git commit -m "docs(templates): retarget operations headings onto the corpus

The registry named different headings from the ones the corpus uses. On every
one of the three contested headings the corpus is consistent at 61:1 or better
and the registry is the outlier:

  guides    ## Usage 65        vs ## Routine Usage 1
  policies  ## Policy Scope 63 vs ## Scope 1
  runbooks  ## When to Use 61  vs ## Trigger and Preconditions 2

Per specification D2 the corpus is promoted to canonical. This resolves guide,
policy, and runbook conformance without editing 190 documents.

The frontmatter-conditional scope workaround is removed; it existed only to
straddle the split."
```

---

#### Task 10: Absorbed into Task 4

This task retargeted the `audit` role. It was pulled forward into Task 4,
because Task 4's original disposition (`forbidden_headings: []`) proved
structurally impossible and the investigation that followed produced the
measurement this task depended on. Splitting the same role across two waves
would have edited one registry entry twice.

- [ ] **Step 1: Confirm Task 4 already applied the retarget**

```bash
python3 -c "import yaml; r=yaml.safe_load(open('docs/99.templates/support/document-metadata-profiles.yaml'))['template_roles']['audit']; print('required:', r['required_headings']); print('forbidden:', r['forbidden_headings'])"
```

Expected: eight required headings beginning `## Overview`, `## Purpose`,
`## Repository Role`; and `['## Procedure', '## Controls', '## Usage']`
forbidden. If either differs, Task 4 did not complete — return to it.

No commit. This task has no remaining work.

#### Task 11: Mark the not-yet-exercised templates

**Files:**

- Modify: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Modify: `docs/99.templates/templates/README.md`

**Interfaces:**

- Consumes: the zero-instantiation measurement.
- Produces: an explicit record distinguishing "unused because unneeded" from
  "unused because broken". Task 9 and Task 10 fixed the broken ones; these are
  genuinely unexercised.

- [ ] **Step 1: Confirm the zero-instantiation set**

```bash
for t in incident postmortem release api-spec data-model service tests agent-design; do
  case $t in
    incident)   g='docs/05.operations/incidents/*.md' ;;
    postmortem) g='docs/05.operations/incidents/**/*postmortem*.md' ;;
    release)    g='docs/05.operations/releases/*.md' ;;
    *)          g="docs/03.specs/*/$t.md" ;;
  esac
  n=$(ls $g 2>/dev/null | grep -v README | wc -l)
  echo "$t: $n"
done
```

Expected: every count is `0` except `agent-design`, which is `1` and
non-conforming.

- [ ] **Step 2: Add a not-yet-exercised table to the stage authoring matrix**

Insert before the `## Related Documents` heading of
`docs/00.agent-governance/rules/stage-authoring-matrix.md`:

```markdown
## Not-Yet-Exercised Templates

These templates are registered, valid, and retained. No document has been
authored from them. They are retained because the lifecycle event they serve has
not yet occurred, not because they are defective.

| Template       | Target path                                | Trigger that would create the first instance  |
| :------------- | :----------------------------------------- | :-------------------------------------------- |
| `incident`     | `docs/05.operations/incidents/YYYY/`       | A recorded production incident                |
| `postmortem`   | `docs/05.operations/incidents/YYYY/`       | A reviewed incident                           |
| `release`      | `docs/05.operations/releases/`             | A tagged release                              |
| `api-spec`     | `docs/03.specs/NNN-<slug>/api-spec.md`     | A specification defining an HTTP or RPC API   |
| `data-model`   | `docs/03.specs/NNN-<slug>/data-model.md`   | A specification defining persisted entities   |
| `service`      | `docs/03.specs/NNN-<slug>/service.md`      | A specification introducing a Compose service |
| `tests`        | `docs/03.specs/NNN-<slug>/tests.md`        | A specification with a formal test matrix     |
| `agent-design` | `docs/03.specs/NNN-<slug>/agent-design.md` | A specification defining a new agent role     |

Authoring against one of these is expected to require template revision, since
none has been validated against a real document.
```

- [ ] **Step 3: Verify and commit**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
git add docs/00.agent-governance/rules/stage-authoring-matrix.md docs/99.templates/templates/README.md
git commit -m "docs(governance): record the not-yet-exercised templates

Eight templates have zero instances. Unlike the guide, policy, runbook, and
audit roles repaired in this wave, these are unused because their lifecycle
event has not occurred, not because their contract was wrong.

Recording the distinction prevents a future audit from reading all twelve
zero-instance roles as the same defect."
```

---

### Wave W3 — Archive model and the 267-document migration

Precondition: W2 complete. Moving documents before the contract describes them
produces violations that cannot be attributed to the move.

---

#### Task 12: Wire the content-archive role into the retention contract

**Files:**

- Modify: `docs/99.templates/support/archive-retention-contract.md`
- Modify: `docs/98.archive/README.md`

**Interfaces:**

- Consumes: `docs/99.templates/templates/common/content-archive.template.md`,
  which already exists.
- Produces: the two-role archive model Task 13 and Task 14 write into.

- [ ] **Step 1: Confirm both templates exist and note their heading sets**

```bash
for f in docs/99.templates/templates/common/archive.template.md \
         docs/99.templates/templates/common/content-archive.template.md; do
  echo "=== $f"; grep '^#' "$f"
done
```

Expected: `archive.template.md` carries Overview, Archive Metadata, Archive
Ledger, Related Documents; `content-archive.template.md` additionally carries
Current-use Warning.

- [ ] **Step 2: Add the two-role table to the retention contract**

Insert before the `## Related Documents` heading of
`docs/99.templates/support/archive-retention-contract.md`:

```markdown
## Archive Roles

`docs/98.archive/` serves two distinct roles. Both use `status: archived`.

| Role            | Purpose                                                                  | Template                      | Retains body |
| :-------------- | :----------------------------------------------------------------------- | :---------------------------- | :----------- |
| Tombstone       | Path redirect only                                                       | `archive.template.md`         | No           |
| Content archive | Full preservation of terminal work, mirroring the source stage structure | `content-archive.template.md` | Yes          |

Three rules govern the model.

1. An archived document leaves a forward pointer at its original location when
   the source stage survives. When the source stage is itself removed, inbound
   links are rewritten to the archive path and the mapping is recorded in the
   archive ledger instead. A dangling pointer inside a deleted directory serves
   no reader.
2. Architecture decision records are never moved. Supersession is a status
   change plus a `superseded-by` link, applied in place.
3. Content archive entries retain their date prefix. The archive is the one
   place where a filename date is an accurate event record.
```

- [ ] **Step 3: Verify and commit**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
git add docs/99.templates/support/archive-retention-contract.md docs/98.archive/README.md
git commit -m "docs(templates): wire the content-archive role into the retention contract

The archive stage held 21 tombstones and had no role that preserves content,
while 267 terminal documents stayed in the active stages because no destination
existed for them.

Both templates already existed; only the contract was missing. Rule 1 is stated
with its survives-the-stage branch, because Stage 04 is removed in W4 and a
forward pointer inside a deleted directory is not reachable."
```

---

#### Task 13: Migrate the 41 terminal Stage 03 specifications

**Files:**

- Move: 42 directories under `docs/03.specs/` to `docs/98.archive/03.specs/`
- Create: 42 forward-pointer tombstones at the original paths

**Interfaces:**

- Consumes: the archive roles from Task 12.
- Produces: a Stage 03 holding only 17 directories, which Task 16 co-locates
  into.

- [ ] **Step 1: Enumerate the terminal specifications**

```bash
cd /home/hy/projects/hy-home.docker
for d in docs/03.specs/*/; do
  s=$(awk '/^---$/{n++;next} n==1 && /^status:/{print $2; exit}' "$d/spec.md" 2>/dev/null)
  case "$s" in completed|superseded) echo "$s $d" ;; esac
done | tee /tmp/claude-1000/sdlc-convergence/terminal-specs.txt | wc -l
```

Expected: `42` lines — 41 `completed` plus 1 `superseded`.

- [ ] **Step 2: Record inbound links before moving anything**

```bash
while read -r _ d; do
  slug=$(basename "$d")
  n=$(grep -rl "03\.specs/$slug" docs/ --include='*.md' | grep -v llm-wiki | wc -l)
  echo "$n $slug"
done < /tmp/claude-1000/sdlc-convergence/terminal-specs.txt \
  | sort -rn | tee /tmp/claude-1000/sdlc-convergence/spec-inbound.txt | head
```

Records how many documents link to each specification. Any slug with a non-zero
count needs its forward pointer to resolve.

- [ ] **Step 3: Move one specification and verify the mechanics before batching**

```bash
d=$(head -1 /tmp/claude-1000/sdlc-convergence/terminal-specs.txt | awk '{print $2}')
slug=$(basename "$d")
mkdir -p docs/98.archive/03.specs
git mv "$d" "docs/98.archive/03.specs/$slug"
ls docs/98.archive/03.specs/$slug/
```

Expected: the directory and its contents are now under the archive.

- [ ] **Step 4: Write the forward-pointer tombstone for that specification**

Create `docs/03.specs/<slug>/spec.md` with this content, substituting the slug,
today's date, and the recorded status:

```markdown
---
layer: archive
status: archived
archived_from: docs/03.specs/<slug>/spec.md
archived_on: 2026-08-07
archive_reason: 'Terminal governance-meta specification relocated to the content archive under specification 136 wave W3.'
current_replacement: docs/98.archive/03.specs/<slug>/spec.md
---

<!-- Target: docs/03.specs/<slug>/spec.md -->

# Archived Tombstone: <Title>

## Overview

This specification reached a terminal status and its content moved to the
content archive. This tombstone exists so inbound links continue to resolve.

## Archive Metadata

| Field       | Value                                     |
| :---------- | :---------------------------------------- |
| Archived on | 2026-08-07                                |
| Source      | `docs/03.specs/<slug>/spec.md`            |
| Destination | `docs/98.archive/03.specs/<slug>/spec.md` |
| Wave        | W3                                        |

## Archive Ledger

| Event    | Date       | Authority                               |
| :------- | :--------- | :-------------------------------------- |
| Archived | 2026-08-07 | `spec:136-sdlc-taxonomy-convergence` D4 |

## Related Documents

- [Archived specification](../../98.archive/03.specs/<slug>/spec.md)
- [SDLC taxonomy convergence](../136-sdlc-taxonomy-convergence/spec.md)
```

- [ ] **Step 5: Verify the single case passes before batching**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
```

Expected: `violations=0`. If the archive profile rejects the frontmatter, fix
the shape here — before it is replicated 41 times.

- [ ] **Step 6: Commit the single case as the pattern**

```bash
git add -A docs/03.specs docs/98.archive
git commit -m "docs(archive): migrate the first terminal specification

Establishes the directory-move plus forward-pointer pattern that the remaining
41 terminal specifications follow. Committed separately so the pattern is
reviewable before it is replicated."
```

- [ ] **Step 7: Apply the pattern to the remaining 41**

Repeat Steps 3 and 4 for every remaining line in
`/tmp/claude-1000/sdlc-convergence/terminal-specs.txt`. Commit in batches of at
most ten directories, each batch a logical unit named by what it archives.

- [ ] **Step 8: Verify Stage 03 is reduced and links resolve**

```bash
ls -d docs/03.specs/*/ | wc -l
python3 - <<'PY'
import pathlib, re
broken = []
for p in pathlib.Path("docs").rglob("*.md"):
    in_fence = False
    for line in p.read_text(errors="ignore").splitlines():
        # Toggle only on a line that STARTS a fence. Counting backtick runs
        # inside the whole text breaks on any code that contains backticks --
        # including this check itself.
        if line.lstrip().startswith("`" * 3):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in re.finditer(r"\]\(([^)]+)\)", line):
            target = m.group(1).split("#")[0]
            if not target or target.startswith(("http", "mailto:")):
                continue
            if not (p.parent / target).exists():
                broken.append(f"{p}: {target}")
print("broken:", len(broken))
print("\n".join(broken))
PY
```

Expected: `59` directories still (42 tombstones remain in place), and broken
links at or below the Task 1 baseline.

---

#### Task 14: Migrate the 225 completed Stage 04 documents

**Files:**

- Move: 225 files from `docs/04.execution/` to `docs/98.archive/04.execution/`
- Modify: every document containing an inbound link to a moved file
- Modify: `docs/98.archive/README.md` (ledger mapping)

**Interfaces:**

- Consumes: the archive roles from Task 12.
- Produces: a Stage 04 holding 6 documents, which Task 16 empties.

- [ ] **Step 1: Enumerate the completed documents**

```bash
cd /home/hy/projects/hy-home.docker
for f in docs/04.execution/plans/*.md docs/04.execution/tasks/*.md; do
  [ "$(basename "$f")" = "README.md" ] && continue
  s=$(awk '/^---$/{n++;next} n==1 && /^status:/{print $2; exit}' "$f")
  [ "$s" = "completed" ] && echo "$f"
done | tee /tmp/claude-1000/sdlc-convergence/completed-exec.txt | wc -l
```

Expected: `225`.

- [ ] **Step 2: Build the source-to-destination mapping**

```bash
while read -r f; do
  echo "$f -> docs/98.archive/${f#docs/}"
done < /tmp/claude-1000/sdlc-convergence/completed-exec.txt \
  > /tmp/claude-1000/sdlc-convergence/exec-mapping.txt
head -3 /tmp/claude-1000/sdlc-convergence/exec-mapping.txt
wc -l /tmp/claude-1000/sdlc-convergence/exec-mapping.txt
```

Expected: 225 mapping lines of the form
`docs/04.execution/tasks/X.md -> docs/98.archive/04.execution/tasks/X.md`.

- [ ] **Step 3: Count the inbound links that must be rewritten**

```bash
n=0
while read -r f; do
  rel=${f#docs/}
  c=$(grep -rl "$rel" docs/ --include='*.md' | grep -v llm-wiki | grep -v "^$f\$" | wc -l)
  n=$((n + c))
done < /tmp/claude-1000/sdlc-convergence/completed-exec.txt
echo "inbound references to rewrite: $n"
```

Record the number. Step 6 must reduce it to zero.

- [ ] **Step 4: Move the files preserving directory structure**

```bash
mkdir -p docs/98.archive/04.execution/plans docs/98.archive/04.execution/tasks
while read -r f; do
  git mv "$f" "docs/98.archive/${f#docs/}"
done < /tmp/claude-1000/sdlc-convergence/completed-exec.txt
find docs/04.execution -name '*.md' ! -name 'README.md' | wc -l
```

Expected: `6` files remain in Stage 04.

- [ ] **Step 5: Set the archived status on every moved file**

```bash
while read -r f; do
  d="docs/98.archive/${f#docs/}"
  python3 - "$d" <<'PY'
import sys, re, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
t = re.sub(r'(?m)^status: completed$', 'status: archived', t, count=1)
if 'archived_from:' not in t:
    src = str(p).replace('docs/98.archive/', 'docs/')
    t = t.replace('status: archived',
                  f'status: archived\narchived_from: {src}\narchived_on: 2026-08-07', 1)
p.write_text(t)
PY
done < /tmp/claude-1000/sdlc-convergence/completed-exec.txt
grep -c 'status: archived' docs/98.archive/04.execution/tasks/*.md | grep -c ':1' || true
```

- [ ] **Step 6: Rewrite every inbound link**

```bash
while read -r line; do
  src=${line%% -> *}; dst=${line##* -> }
  s=${src#docs/}; d=${dst#docs/}
  grep -rl "$s" docs/ --include='*.md' | grep -v llm-wiki | while read -r target; do
    python3 - "$target" "$s" "$d" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
p.write_text(p.read_text().replace(sys.argv[2], sys.argv[3]))
PY
  done
done < /tmp/claude-1000/sdlc-convergence/exec-mapping.txt
```

- [ ] **Step 7: Confirm zero remaining references to the old paths**

```bash
n=0
while read -r f; do
  rel=${f#docs/}
  c=$(grep -rl "$rel" docs/ --include='*.md' | grep -v llm-wiki | grep -v '98.archive' | wc -l)
  n=$((n + c))
done < /tmp/claude-1000/sdlc-convergence/completed-exec.txt
echo "remaining stale references: $n"
```

Expected: `0`. If non-zero, Step 6 missed a path form; inspect and repeat.

- [ ] **Step 8: Record the mapping in the archive ledger**

Append a `## Archive Ledger` mapping table to `docs/98.archive/README.md`
listing each source path and its destination, generated from
`/tmp/claude-1000/sdlc-convergence/exec-mapping.txt`. This replaces the forward
pointers that Stage 04 cannot carry, per Task 12 rule 1.

- [ ] **Step 9: Verify and commit in batches**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
```

Commit in batches of at most 25 files, each batch named by what it archives.

---

#### Task 15: Remove the superseded redirect stubs

**Files:**

- Delete: `docs/90.references/audits/2026-07-07-*-audit-pack-update/` (6 files)
- Move: the 21 `2026-06-05-language-policy-*` documents to the content archive

**Interfaces:**

- Consumes: the mapping mechanics from Task 14.
- Produces: removal of the two surfaces specification 136 marks for disposal.

- [ ] **Step 1: Confirm the stubs carry no analysis and no inbound links**

```bash
d=$(ls -d docs/90.references/audits/2026-07-07-*-audit-pack-update 2>/dev/null | head -1)
echo "dir: $d"
find "$d" -name '*.md' | wc -l
wc -l "$d"/*.md | tail -1
grep -rl "$(basename "$d")" docs/ --include='*.md' | grep -v llm-wiki | grep -v "^$d"
```

Expected: 6 files, roughly 395 lines total, and no inbound references outside
the directory itself. If any real inbound link exists, stop and escalate.

- [ ] **Step 2: Delete the stub directory**

```bash
git rm -r "$d"
```

- [ ] **Step 3: Confirm the language-policy tasks have no real consumers**

```bash
ls docs/98.archive/04.execution/tasks/2026-06-05-language-policy-* 2>/dev/null | wc -l
```

Expected: these were already moved by Task 14 if they carried
`status: completed`. If any remain in `docs/04.execution/`, move them now using
the Task 14 mechanics.

- [ ] **Step 4: Verify and commit**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
git add -A docs/
git commit -m "docs(archive): delete the superseded audit-pack redirect stubs

The 2026-07-07 audit pack update held six redirect stubs, roughly 395 lines,
all superseded and with zero real inbound consumers. Its twin research pack was
removed for the same reason under specification 122."
```

---

### Wave W4 — Stage 04 collapse into Stage 03

Precondition: W3 complete. Stage 04 holds 6 documents.

---

#### Task 16: Co-locate the six active execution documents

**Files:**

- Move: 6 files from `docs/04.execution/` into their parent specification
  directories
- Modify: `docs/99.templates/support/template-selection.md`
- Modify: `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- Delete: `docs/04.execution/`

**Interfaces:**

- Consumes: the reduced Stage 04 from Task 14.
- Produces: the target specification directory shape that W5 renumbers around.

- [ ] **Step 1: Confirm exactly six active documents remain**

```bash
find docs/04.execution -name '*.md' ! -name 'README.md' | sort
```

Expected exactly:

```text
docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md
docs/04.execution/plans/2026-07-26-agent-governance-canonical-convergence.md
docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md
docs/04.execution/plans/2026-08-07-sdlc-taxonomy-convergence.md
docs/04.execution/tasks/2026-07-26-agent-governance-canonical-convergence.md
docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
docs/04.execution/tasks/2026-08-07-agentic-research-pack-extension.md
```

Seven files: the six active documents plus this plan, which carries
`status: draft` and was therefore not archived by Task 14. It moves with them.

- [ ] **Step 2: Resolve each document to its parent specification**

```bash
for f in $(find docs/04.execution -name '*.md' ! -name 'README.md'); do
  p=$(awk '/^---$/{n++;next} n==1 && /^ *- *spec:/{print $NF; exit}' "$f")
  echo "$f  ->  $p"
done
```

Expected pairings: the two convergence documents map to specs 134 and 135, the
research pack extension to spec 104, and this plan to spec 136. The
`2026-03-27-infra-service-optimization-priority-plan.md` has no `spec:` parent —
it is the single active orphan.

- [ ] **Step 3: Move the four paired subjects into their specification directories**

```bash
git mv docs/04.execution/plans/2026-07-26-agent-governance-canonical-convergence.md \
       docs/03.specs/134-agent-governance-canonical-convergence/plan.md
git mv docs/04.execution/tasks/2026-07-26-agent-governance-canonical-convergence.md \
       docs/03.specs/134-agent-governance-canonical-convergence/task.md
git mv docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md \
       docs/03.specs/135-target-surface-delta-convergence/plan.md
git mv docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md \
       docs/03.specs/135-target-surface-delta-convergence/task.md
git mv docs/04.execution/plans/2026-08-07-sdlc-taxonomy-convergence.md \
       docs/03.specs/136-sdlc-taxonomy-convergence/plan.md
```

The research pack extension task moves to whichever specification Step 2
resolved for it.

- [ ] **Step 4: Handle the single active orphan**

`2026-03-27-infra-service-optimization-priority-plan.md` has no parent
specification. Per specification D5, active orphans get a specification authored
for them rather than being archived. Author
`docs/03.specs/137-infra-service-optimization-priority/spec.md` from
`docs/99.templates/templates/sdlc/spec.template.md`, capturing the scope the
plan already describes, then:

```bash
git mv docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md \
       docs/03.specs/137-infra-service-optimization-priority/plan.md
```

- [ ] **Step 5: Update the frontmatter `artifact_id` of every moved file**

Each moved file's `artifact_id` still carries its dated form. Rewrite it to the
directory-derived form, for example
`plan:2026-07-26-agent-governance-canonical-convergence` becomes
`plan:134-agent-governance-canonical-convergence`, and add a `created` field
carrying the date the filename used to hold. Do not remove the date; move it.

- [ ] **Step 6: Rewrite inbound links to the six moved documents**

Use the Task 14 Step 6 mechanics with a mapping file built from Step 3 and
Step 4. Confirm zero stale references afterward with the Task 14 Step 7 check.

- [ ] **Step 7: Remove the empty stage**

```bash
find docs/04.execution -type f
git rm -r docs/04.execution
```

Expected: only `README.md` files remain before removal. Preserve any content
from `docs/04.execution/plans/README.md` and `tasks/README.md` that is still
true by folding it into `docs/03.specs/README.md`.

- [ ] **Step 8: Update the routing contracts**

In `docs/99.templates/support/template-selection.md`, replace the plan and task
target-path rows:

```markdown
| Plan | `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` | plan.template.md |
| Task | `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` | task.template.md |
```

with:

```markdown
| Plan | `docs/03.specs/NNN-<slug>/plan.md` | plan.template.md |
| Task | `docs/03.specs/NNN-<slug>/task.md` | task.template.md |
```

Update the corresponding `target_globs` in
`docs/99.templates/support/document-metadata-profiles.yaml` for the `plan` and
`task` roles, and the Stage 04 rows in
`docs/00.agent-governance/rules/stage-authoring-matrix.md`.

- [ ] **Step 9: Codify the write-back rule**

Co-location without write-back is exactly the configuration specification D5
identifies as degrading to spec deletion. The rule must be enforced text, not
plan prose, or the orphan-execution ratio returns.

Insert the following into
`docs/00.agent-governance/rules/task-checklists.md`, in its completion section:

```markdown
- **Write-back before archive.** A task is not complete until its result is
  written back into the parent `spec.md` in the same directory. Record what the
  specification now states differently because the work happened. A directory
  whose `task.md` is terminal but whose `spec.md` still describes the
  pre-implementation state is not archivable.
```

Add the corresponding lifecycle statement to
`docs/00.agent-governance/rules/documentation-protocol.md` immediately after the
frontmatter status rule:

```markdown
- **Specification write-back (R6):** When a co-located `task.md` reaches a
  terminal status, its parent `spec.md` MUST be updated to describe the
  delivered state before the directory is archived. Separation of durable
  contract from execution record survives co-location only through this rule.
```

- [ ] **Step 10: Verify the rule has no competing statement**

```bash
grep -rn 'write-back\|write back' docs/00.agent-governance/rules/
```

Expected: the two statements added above and no third, contradicting one.

- [ ] **Step 11: Verify and commit**

```bash
ls -d docs/04.execution 2>/dev/null && echo "STILL PRESENT" || echo "removed"
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep -c '^FAIL' || echo 0
git add -A
git commit -m "refactor(docs): collapse Stage 04 into Stage 03 by co-location

Each specification directory now holds its durable contract and its execution
record together: spec.md, plan.md, task.md.

Co-location is bound to archive-on-completion by specification D3. A directory
is archived whole, never emptied in place and never deleted, so this does not
reproduce the spec-deletion outcome documented for co-located tooling.

225 of 231 Stage 04 documents were already archived in W3, so this moves six
active documents and authors one specification for the single active orphan."
```

---

### Wave W5 — Stage 05 renumbering

Precondition: W4 complete. No path is rewritten twice.

---

#### Task 17: Rename the directory and rewrite every reference

**Files:**

- Move: `docs/05.operations/` to `docs/04.operations/`
- Modify: 597 files containing the literal `05.operations`

**Interfaces:**

- Consumes: the completed structural movement from W4.
- Produces: a contiguous `00`–`04` active stage sequence.

- [ ] **Step 1: Re-measure the blast radius immediately before acting**

```bash
cd /home/hy/projects/hy-home.docker
grep -rl "05\.operations" . --exclude-dir=.git --exclude-dir=graphify-out \
  --exclude-dir=node_modules | wc -l
grep -ro "05\.operations" . --exclude-dir=.git --exclude-dir=graphify-out \
  --exclude-dir=node_modules | wc -l
```

Record both numbers. W3 and W4 changed some of these files, so the counts will
differ from the 597 and 3,274 measured at planning time. Use what you measure.

- [ ] **Step 2: Move the directory**

```bash
git mv docs/05.operations docs/04.operations
ls -d docs/0*/
```

Expected: `00.agent-governance 01.requirements 02.architecture 03.specs 04.operations`.

- [ ] **Step 3: Rename the archive subtree and pin its historical values**

`docs/98.archive/05.operations/` is a real directory holding 9 documents. A
content-only replacement would rewrite every reference to it while leaving the
directory in place, breaking all 9. Rename it too:

```bash
git mv docs/98.archive/05.operations docs/98.archive/04.operations
find docs/98.archive/04.operations -name '*.md' | wc -l
```

Expected: `9`.

`archived_from` records where a document lived when it was archived, which was
`docs/05.operations/...`. That value is historical and must survive the rename.
Capture the current values now so Step 4 can restore them:

```bash
grep -rn '^archived_from:' docs/98.archive/ \
  > /tmp/claude-1000/sdlc-convergence/archived-from-historical.txt
wc -l /tmp/claude-1000/sdlc-convergence/archived-from-historical.txt
```

- [ ] **Step 4: Rewrite every textual reference**

```bash
grep -rl "05\.operations" . --exclude-dir=.git --exclude-dir=graphify-out \
  --exclude-dir=node_modules | while read -r f; do
  python3 - "$f" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
p.write_text(p.read_text(errors="ignore").replace("05.operations", "04.operations"))
PY
done
grep -rl "05\.operations" . --exclude-dir=.git --exclude-dir=graphify-out \
  --exclude-dir=node_modules | wc -l
```

Expected: `0`.

- [ ] **Step 5: Restore the historical `archived_from` values**

Step 4 rewrote `archived_from` along with everything else, but that field records
where a document lived when it was archived. Restore the captured values:

```bash
while IFS= read -r line; do
  file=${line%%:*}
  rest=${line#*:}
  value=${rest#*:}
  python3 - "$file" "$(echo "$value" | sed 's/^ *//')" <<'PY'
import sys, re, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text()
t = re.sub(r'(?m)^archived_from:.*$', f'archived_from: {sys.argv[2]}', t, count=1)
p.write_text(t)
PY
done < /tmp/claude-1000/sdlc-convergence/archived-from-historical.txt
grep -rc '^archived_from: docs/05\.operations' docs/98.archive/ 2>/dev/null | grep -v ':0' | wc -l
```

Expected: the archived operations documents again carry their historical
`docs/05.operations/...` provenance while living at `docs/98.archive/04.operations/`.
Current location and historical origin are different facts and are recorded
separately.

- [ ] **Step 6: Confirm the hardcoded validator path was rewritten**

```bash
grep -n 'operations' scripts/validation/check-repo-contracts.sh | grep 'pathlib.Path'
```

Expected: `root = pathlib.Path("docs/04.operations") / bucket`. This line is the
one that silently disables the entire operations heading contract if missed.

- [ ] **Step 7: Confirm the infrastructure references changed but their targets did not**

```bash
git diff --stat -- infra/ | tail -3
git diff -- infra/06-observability/prometheus/config/alert_rules/ | grep '^[+-]' | grep -v '^[+-][+-]' | head -20
```

Expected: only documentation path strings differ. No `expr`, `for`, `severity`,
`alert`, or threshold value appears in the diff. If any does, revert that file
and rewrite only the path.

- [ ] **Step 8: Run the full verification set including infrastructure**

```bash
bash scripts/validation/validate-docker-compose.sh
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep -c '^FAIL' || echo 0
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
```

Expected: Compose validation passes; contract failures at or below the Task 1
baseline; zero metadata violations on changed documents; traceability clean.

- [ ] **Step 9: Confirm zero broken links across the whole corpus**

```bash
python3 - <<'PY'
import pathlib, re
broken = []
for p in pathlib.Path("docs").rglob("*.md"):
    in_fence = False
    for line in p.read_text(errors="ignore").splitlines():
        # Toggle only on a line that STARTS a fence. Counting backtick runs
        # inside the whole text breaks on any code that contains backticks --
        # including this check itself.
        if line.lstrip().startswith("`" * 3):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in re.finditer(r"\]\(([^)]+)\)", line):
            target = m.group(1).split("#")[0]
            if not target or target.startswith(("http", "mailto:")):
                continue
            if not (p.parent / target).exists():
                broken.append(f"{p}: {target}")
print("broken:", len(broken))
print("\n".join(broken))
PY
```

Expected: at or below the Task 1 baseline.

- [ ] **Step 10: Commit**

```bash
git add -A
git commit -m "refactor(docs): renumber Stage 05 operations to Stage 04

Collapsing Stage 04 into Stage 03 in W4 left a gap in the stage sequence.
Renumbering restores a contiguous 00-04 active sequence.

The rename crosses out of docs/: infra service READMEs, four Prometheus alert
rule files, CODEOWNERS, and the validators carry documentation paths. Only
those path strings change; nothing any alert rule controls is modified.

Executed after all structural movement so no path is rewritten twice."
```

---

#### Task 18: Regenerate derived artifacts and close the plan

**Files:**

- Modify: generated indexes under `docs/90.references/llm-wiki/`
- Modify: `docs/00.agent-governance/memory/current.md`
- Create: `docs/03.specs/136-sdlc-taxonomy-convergence/task.md`

**Interfaces:**

- Consumes: the completed W1 through W5.
- Produces: the evidence record W6 through W9 are planned against.

- [ ] **Step 1: Regenerate every derived index**

```bash
bash scripts/knowledge/generate-llm-wiki-coverage.sh
git diff --stat -- docs/90.references/
```

Expected: path rows update to the new stage numbers. If the generator is not
the right entry point, locate it with
`grep -rl 'llm-wiki-index' scripts/`.

- [ ] **Step 2: Record the final measurements**

```bash
ls -d docs/03.specs/*/ | wc -l
find docs/98.archive -name '*.md' | wc -l
ls -d docs/0*/
bash scripts/validation/check-repo-contracts.sh 2>&1 | grep -c '^FAIL' || echo 0
python3 scripts/validation/check-document-metadata.py --mode check-active 2>&1 | tail -1
```

Compare every number against the Task 1 baseline and against the specification's
measured starting state.

- [ ] **Step 3: Author the Stage 04 task record**

Create `docs/03.specs/136-sdlc-taxonomy-convergence/task.md` from
`docs/99.templates/templates/sdlc/task.template.md`, recording per wave: the
commands run, their output, the commit range, and any deviation from this plan.

- [ ] **Step 4: Refresh the current-state memory record**

Replace the body of `docs/00.agent-governance/memory/current.md` in place with
the bounded seven-section envelope: current task, approved decisions, active
boundary, verified state, blockers, evidence links, and next handoff. Do not
append a second current-state section.

- [ ] **Step 5: Verify and commit**

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed
bash scripts/validation/check-doc-traceability.sh
git add -A
git commit -m "docs(task): record SDLC taxonomy convergence W1-W5 evidence"
```

## Verification Plan

Run after every task, not only at wave boundaries.

| Check                     | Command                                                                          | Acceptance                                    |
| :------------------------ | :------------------------------------------------------------------------------- | :-------------------------------------------- |
| Repository contracts      | `bash scripts/validation/check-repo-contracts.sh`                                | Failure count at or below the Task 1 baseline |
| Changed-document metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed`     | `violations=0`                                |
| Full-corpus metadata      | `python3 scripts/validation/check-document-metadata.py --mode check-active`      | Monotonically decreasing per wave             |
| Traceability              | `bash scripts/validation/check-doc-traceability.sh`                              | Zero failures                                 |
| Link integrity            | The Python snippet in Task 1 Step 3                                              | At or below the Task 1 baseline               |
| Heading contract          | `bash scripts/validation/check-repo-contracts.sh 2>&1 \| grep 'profile heading'` | Zero after Task 2 Step 7                      |
| Whitespace                | `git diff --check`                                                               | No output                                     |
| Infrastructure            | `bash scripts/validation/validate-docker-compose.sh`                             | Passes; required for Task 17 only             |
| Rename completeness       | `grep -rl "05\.operations" . --exclude-dir=.git \| wc -l`                        | `0` after Task 17; required for Task 17 only  |

## Risks and Rollback

| Risk                                                                      | Detection                                    | Rollback                                                          |
| :------------------------------------------------------------------------ | :------------------------------------------- | :---------------------------------------------------------------- |
| Line anchoring applied without the `##` prefix fix fails all 62 runbooks  | Task 2 Step 4 shows 63 failures instead of 2 | Revert the single commit; reapply both edits together             |
| Removing the substring match exposes violations beyond the predicted two  | Task 2 Step 4 shows more than 2              | Stop. Re-measure and escalate; do not widen the corpus edit       |
| Retargeting templates entrenches a corpus error                           | Task 9 Step 1 shows a ratio below 61:1       | Stop. The threshold is the guard; do not promote a close call     |
| A moved specification breaks an inbound link                              | Task 13 Step 8 link count rises              | The tombstone is the fix; author the missing one                  |
| Link rewriting in Task 14 corrupts an unrelated substring                 | `git diff` review before each batch commit   | Revert the batch; narrow the match to a full path form            |
| Removing `docs/04.execution/` loses README content still true             | Task 16 Step 7 inspection                    | Recover from git; fold into `docs/03.specs/README.md`             |
| The rename misses the hardcoded validator path, silently disabling checks | Task 17 Step 4                               | Apply the path edit; re-run the heading check                     |
| The rename alters Prometheus alert behavior                               | Task 17 Step 5 diff review                   | Revert the alert rule file; rewrite only the documentation path   |
| A wave regresses the contract baseline                                    | The per-task contract check                  | Revert the wave's commits; the waves are independently revertable |

Every task is a separate commit or a small batch of them, so `git revert` at
task granularity is always available. No task depends on an uncommitted state
from another task.

## Approval Gates

| Gate                                          | Required before                     |
| :-------------------------------------------- | :---------------------------------- |
| Human review of the Task 2 exposure count     | Task 2 Step 5, the corpus edit      |
| Human approval of the Task 9 promotion ratios | Task 9 Step 2, the registry rewrite |
| Human approval of the 267-document migration  | Task 13 Step 7, the batch phase     |
| Human approval of authoring specification 137 | Task 16 Step 4                      |
| Human approval of the infrastructure diff     | Task 17 Step 6                      |
| Independent review by a non-author            | Closing Task 18                     |

No push to any remote at any gate. The controlled all-files pre-commit wrapper
runs only at the final gate, and only via
`scripts/validation/run-agent-precommit-all-files.sh`.

## Completion Criteria

- The heading contract fires: Task 2 Step 4 showed exactly two failures, and
  Task 2 Step 7 shows zero after migration.
- Template conformance exceeds the measured 88 of 631.
- `docs/03.specs/` holds 17 live directories plus 42 tombstones; every live
  directory with active execution holds `plan.md` and `task.md`.
- `docs/04.execution/` does not exist.
- `docs/04.operations/` exists and `docs/05.operations/` does not.
- `grep -rl "05\.operations"` returns zero files.
- `docs/98.archive/` holds the 267 migrated documents plus the pre-existing 21.
- Broken relative links are at or below the Task 1 baseline of 1, counted with
  the fence-aware check.
- The repository contract failure count is at or below the Task 1 baseline of 2.
  The specification records 4; the tree measured 2, and the measured value
  governs.
- `docs/03.specs/136-sdlc-taxonomy-convergence/task.md` records every wave's
  commands, output, and commit range.
- `docs/00.agent-governance/memory/current.md` reflects the post-W5 state.

## Related Documents

- [SDLC taxonomy convergence specification](../../03.specs/136-sdlc-taxonomy-convergence/spec.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Template selection](../../99.templates/support/template-selection.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Archive retention contract](../../99.templates/support/archive-retention-contract.md)
- [Current project memory](../../00.agent-governance/memory/current.md)
