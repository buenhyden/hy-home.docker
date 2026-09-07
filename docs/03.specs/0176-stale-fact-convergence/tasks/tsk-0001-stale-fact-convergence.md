---
title: "Stale Fact Convergence Execution"
version: "0.10.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-07"
layer: "specs"
artifact_id: "SPEC-0176-TSK-0001"
parent_ids:
- "SPEC-0176"
- "SPEC-0176-PLAN-0001"
created: "2026-09-07"
---

# Stale Fact Convergence Execution

## Objective

Own every actual command, result, review finding, blocker, and disposition for
SPEC-0176. This Task is the sole execution and handoff authority for the
package; no second progress ledger is created.

## Inputs

- Position, recorded durably rather than by branch name. Work on this package
  happens on a short branch cut from `main` and retired into `main` as soon as it
  is verified, so any branch name written here is dead by the next integration. A
  resuming session reads its position from Git: `git rev-parse --abbrev-ref HEAD`
  for the branch, `git rev-parse HEAD` for the commit, and
  `git log --oneline origin/main..HEAD` for what is not yet on the remote. The
  durable facts are that `main` is the integration target and that the Commit
  Ledger below lists every commit this package produced.
- Audit baseline: local `main` at
  `e37b2dbcd877f6fbbf32205fd4f5e83680630dc9`, clean worktree, six commits ahead
  of `origin/main` at `d890b862e310b519802a1e837089b87a2b27cdf7`.
- Governing owners: REQ-0024, REQ-0025, REQ-0026, AD-0027, AD-0030, ADR-0033,
  SPEC-0176, SPEC-0176-PLAN-0001.
- Authorization: local investigation, local edits, local commits on this branch,
  and local integration into `main`. Push, pull request, remote reference change,
  deployment, live service action, secret values, and global installation remain
  unauthorized. Pushing to `main` is additionally blocked by a registered hook
  and is not attempted by any other route.
- Evidence classes used throughout, kept non-substitutable: `local-executed`,
  `configured`, `repository-enforced`, `official-source`, `local-parser`,
  `unverified-runtime`, `unverified-entitlement`, `unverified-remote`.

## Work Log

### Audit that opened the package (2026-09-07, local-executed)

Eight registered checks were run first, so that the audit could separate what the
gates already prove from what they cannot see. All eight passed:

```text
check-document-metadata.py                 0 findings, 0 parser failures
check-document-links.py --mode all         documents=711 links=6113 failures=0
check-document-corpus-lifecycle.py         violations=0; recovery violations=0
check-agent-governance-contract.py         PASS mode=repository failures=0
check-script-manifest.py                   PASS
check-operations-catalog.py                PASS
check-agentic-audit-semantic-freshness.py  PASS assertions=11 failures=0
report-provider-hook-parity.sh             PASS matrix fresh
```

That result is the reason this package exists. The registered checks prove a
document's existence, profile, and link targets; none of them reads what a
sentence asserts. Every defect below sat inside that blind spot.

A path-claim scan was run over `.agents/`, `.claude/`, `.codex/`, the root shims,
and `llms.txt`, comparing every backticked path against `git ls-files` and the
working tree. It produced seventy-five unresolved candidates and zero defects:
each was a relative filename, a branch-name prefix, or a deliberate negative
statement such as the `graphify-out/wiki/index.md`, `llms-full.txt`, and
`.codex/config.toml` clauses, which correctly say the path does not exist.

### W1: Package opened (2026-09-07, local-executed)

The Spec, Plan, and Task were written at their lifecycle initial statuses,
because the public gate runs `check-document-metadata.py` with
`enforce_initial_status` and proves the walk to `active` from Git history.

The transition budget was measured before any status was chosen, not assumed:

```text
git merge-base origin/main HEAD    d890b862e310b519802a1e837089b87a2b27cdf7
```

At that base the documents this package promotes hold `active` (SPEC-0175 Spec
and Plan), `in-progress` (SPEC-0175 Task), `proposed` (ADR-0033), `accepted`
(ADR-0031), `approved` (REQ-0026), and `active` (AD-0030). Every transition this
package needs is therefore exactly one step from the base and fits the one
transition per document per branch rate. This package's own three documents are
absent from that base and admit no transition at all, which is why they are
created at `draft` and stay there.

The first metadata run rejected the package for a reason worth recording, because
it is the guard working as designed:

```text
identity_spaces.spec: identity-allocation-not-advanced:
  new identity requires atomic allocation advancement
```

Writing `SPEC-0176` into frontmatter does not allocate it. `identity_spaces.spec`
was advanced from `high_water` 175 to 176 and `next_number` 176 to 177 in the
same change, which is what makes the number unavailable to any other allocation.

### The index row implied a status the document did not hold (2026-09-07, local-executed)

The first full changed-profile run passed 356 of 357 tests and failed one:

```text
FAIL: test_current_index_status_matches_each_current_spec
AssertionError: False != True : SPEC-0176
```

The test reads each Stage 03 index row and asserts two things about it: that the
Spec's status word appears in the row, and that the standalone word `active`
appears in the row exactly when the status is `active`. The row satisfied the
first and failed the second, because it described the defect being corrected as
"dead-branch position in the active packages". The word was describing SPEC-0173
and SPEC-0175, not SPEC-0176, but the index is read as a status claim about its
own row and the test is right to refuse the ambiguity. The phrase became "the two
in-flight packages" and the suite returned 33 passed.

Recorded because the failure is worth more than its fix: an index that merely
linked correctly would have passed the link checker, and this test is what makes
the index prose answerable to the frontmatter beside it.

A second point is recorded against this session's own method. The gate was run as
`run-ci-gate.py ... | tail -25` with `echo "GATE EXIT=$?"`, which reports the exit
code of `tail` and printed `GATE EXIT=0` over a failing suite. The failure was
found by reading the output rather than by trusting that number. Exit codes are
read from the gate process directly for the remainder of this Task.

### W2: The Compose facts, measured before anything was edited (2026-09-07, local-executed)

```text
git ls-files 'infra/**/docker-compose*.y*ml'  | wc -l          41
  .yml                                                         40
  .yaml                                                         1
service directories (dirname, unique)                          40
root include entries (yaml.safe_load)                          41
commented include lines: grep -cE '^\s*#\s*-\s*infra/'         0
include entries with no file on disk                            0
disk files absent from the include list                         0
```

The include list and the tracked tree are in exact bijection, and no include
line is commented. The `profiles:` value of every service in all 41 files was
read from the file itself and is the source for every profile name written in
W3 and W4; no profile name was copied from prose.

### W3: The retired enablement model, removed at thirty-nine owners (2026-09-07, local-executed)

A mechanical pass replaced the three exact phrases that carried the retired
include-state claim in twenty files. Twenty-two remaining occurrences needed a
service-specific sentence and were rewritten one at a time against the profile
value W2 measured. A second sweep found fifteen more statements in a different
wording, `주석 처리된 선택 서비스` and its variants, including one inside a
Requirement's functional requirement and one inside an Architecture Description.

```text
grep -rn 'optional/commented' infra docs --include='*.md'      before: 57  after: 0
grep -rn '주석 처리|include가 주석|standalone-only|root-commented'  after: 3 (all in infra/README.md, closed by W4)
```

The sweep exposed a second defect of the same origin that the first scan did not
name. SPEC-0171 resolved its six sibling pairs by folding each duplicate into the
file it duplicated and deleting it, so eighteen references in twelve documents
pointed at `docker-compose.dev.yml` and `docker-compose.cluster.yml` files that
no longer exist, including four tree diagrams that drew them as present. Those
were corrected to name the surviving file and the profile that now selects each
topology.

One reference is deliberately left in place:

```text
docs/02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md:27
  - `docker-compose.dev.yml` 경로 정합성 수정
```

ADR-0020 is `accepted` and that line records a decision taken when the file
existed. Editing it would rewrite an accepted decision to agree with a later
contract, which the retention policy forbids and which this package's Rulings
repeat. It is a correct historical record and stays.

### W4: The four documents that carried their own wording (2026-09-07, local-executed)

`infra/README.md` claimed 48 Compose files, 47 `.yml`, and 17 root includes
against a measured 41, 40, and 41, and defined a four-state vocabulary whose
`root-commented-optional` and `standalone-only` members describe states the
tracked tree no longer has. The counts were replaced with the measured values and
the vocabulary with the fact that decides activation, which is the selected
profile.

The MinIO README forbade describing `docker-compose.cluster.yaml` as part of the
root include while that file sits in the include list. Both topologies are now
described as separated by profile, `storage` against `storage-cluster`, which is
what the two files actually declare.

POL-0078 counted "41 of 47 files" and described SPEC-0171 as holding six files
back. That package completed and the six were merged away, so the system scope is
41 files, all included.

The root `docker-compose.yml` comment said SPEC-0171 owns the six absent members.
It now says they were folded into the files they duplicated and that the package
is completed, which is why every Compose file under `infra/` appears in the list.

```text
python3 scripts/validation/check-document-links.py --mode all
  documents=714 links=6135 failures=0
python3 scripts/validation/check-operations-catalog.py            PASS
python3 scripts/validation/check-document-metadata.py --mode check-changed
  selected=39 violations=0
bash scripts/validation/validate-docker-compose.sh
  selections=28 services_total=232, every profile OK
```

### W5: The preservation owner, promoted in one result tree (2026-09-07, local-executed)

Three current-authority documents stated a rule the repository already breaks by
design. `REQ-0026`'s acceptance criteria required that no `completed` Spec
Package retains a `plan.md` or a Task; `AD-0030` and accepted `ADR-0031` called
Plan and Task transient carriers removed at completion. Measured against the
tracked tree:

```text
docs/98.archive/completed/03.specs/0156-compose-enablement-model-convergence/  spec+plan+task, all status: completed
docs/98.archive/completed/03.specs/0169-document-lifecycle-convergence/        spec+plan+task, all status: completed
docs/98.archive/completed/03.specs/0170-archive-preservation-model/            spec+plan+task, all status: completed
docs/98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/       spec+plan+task, all status: completed
```

Four packages satisfy exactly what the criterion says none may. The executable
guard agrees with the tree and not with the Requirement:
`scripts/lib/document_governance/spec_packages.py:1054` states that preservation
"moves a finished package to the archive and keeps every document", and
`.agents/governance/documentation-protocol.md` carries the same model.

`ADR-0033` had been written as the successor for precisely this and had waited at
`proposed`. SPEC-0173's Plan declared the promotion sequence and named it an open
dependency it could not close inside its own package. This package performed it
as one result tree: `ADR-0033` to `accepted` with `supersedes: ADR-0031`,
`ADR-0031` to `superseded` with `superseded_by: ADR-0033` and its body preserved
under `docs/98.archive/superseded/02.architecture/decisions/`, then `REQ-0026`
and `AD-0030` amended to the accepted preservation unit.

The preserved body was compared rather than asserted:

```text
git hash-object <before move>   904677b0303d277bea44904af68ba86758a10425
git hash-object <after move>    5bc18f381d1505e108d6fb28a994c2801c58ad83
diff <(git show HEAD:docs/02.architecture/decisions/0031-preserved-archive-record.md) <preserved>
  5c5   status: "accepted"  ->  status: "superseded"
  13a14 superseded_by: "ADR-0033"
```

Only the two frontmatter fields the transition owns differ. No sentence of the
accepted decision was edited to agree with its successor, and no already
preserved Spec-only package was back-filled with a Plan or Task it never had.

Eight documents linked the old path. Each was repointed to the archive location
rather than left to fail, which is what `AD-0030` itself requires of a residual
document pointing at a moved path. Two of them are Stage 90 dated evidence: the
link target moved, the observation did not.

The same pass closed a third index defect found while editing: the decisions
index described `ADR-0034` as a `proposed` decision while its frontmatter has read
`accepted` since its own package landed.

```text
python3 scripts/validation/check-document-metadata.py --mode check-changed
  selected=48 violations=0 transition_overrides=0
python3 scripts/validation/check-document-links.py --mode all
  documents=713 links=6137 archive_direct_links_total=64 failures=0
python3 scripts/validation/check-document-corpus-lifecycle.py
  violations=0; preserved=153 decisions=254 recovery violations=0
python3 -m unittest tests.lib.document_governance.test_taxonomy test_architecture test_archive
  Ran 60 tests, OK
```

The lifecycle budget held: each of the two decisions spent its single
merge-base transition, and `REQ-0026` and `AD-0030` changed content only, so
neither needed one.

### W9 (partial): The Stage 02 index counted what it should have routed (2026-09-07, local-executed)

`docs/02.architecture/README.md` claimed "26개의 Architecture Description과 26개의
ADR" against a measured 26 and 28, and its structure block named `0031-` as the
last decision when `0034-` had been the last for two packages. The sibling
`decisions/README.md` had already reasoned its way out of this class of defect:
"개수는 유지 기준이 아니므로 아래 Current Inventory와 실제 파일 목록이 권위이다."
The parent now states the same thing rather than carrying a number that stales on
the next decision, and its structure block names the current highest identifier.

This changes acceptance criterion 8, which asked for the corrected counts. The
criterion is amended in the Spec to require the routing statement instead,
because writing 28 would have reproduced the defect at the next ADR.

### W6: The map that routes did not route to two of its own categories (2026-09-07, local-executed)

`repository-map.md` lists `.agents/knowledge/**` and `.agents/prompts/**` in its
Surface Ownership table and then restates a canonical load order whose step 3
reads "Only the policies, canonical role, and explicitly invoked skills the
request needs". `bootstrap.md` step 3 has named both categories and their
conditions since SPEC-0175 W14 corrected exactly this failure in the provider
adapters. The knowledge map was the third entry path with the same gap and was
not corrected then.

The step now states when to read each category and repeats that neither grants a
tool, a path, or an approval. It also names `bootstrap.md` as the owner of the
order and this list as a restatement, so a future divergence is a defect here
rather than an open question, and a refresh trigger was added for a change to
that order.

`verification-surface-map.md` named one commit as the provenance for two files
that were not read at the same time. Its `.pre-commit-config.yaml` rows describe
the selector after `9051977aa` added the `_workspace/` and `evals/` prefixes,
while the stated commit `9ede309a5` predates that fix. The workflow-contract half
was verified unchanged before rewriting the stanza:

```text
git diff 9ede309a5 HEAD -- .github/workflow-contract.yml   (empty)
git diff 9ede309a5 HEAD -- .pre-commit-config.yaml         two selector lines
```

Each source now carries its own commit and date.

### W7: Position recorded from Git instead of a branch that no longer resolves (2026-09-07, local-executed)

```text
git rev-parse --verify codex/0173-agent-governance-home          fatal: Needed a single revision
git rev-parse --verify origin/codex/0173-agent-governance-home   fatal: Needed a single revision
git rev-list --count 8176cdee7..HEAD                             45
```

SPEC-0173's Spec called local main `8176cdee7` the "current review baseline" and
said the branch points at the same commit. The branch was retired at `2a939c68a`
and `main` is forty-five commits past that checkpoint. SPEC-0175 stated the same
branch as its baseline in its Spec and Plan, even though its own Task had already
concluded that "a branch name in a Task is stale by construction" and replaced
its own reference with three Git commands. The correction that package applied to
itself is now applied to its Spec and Plan and to SPEC-0173's two documents:
each commit hash that names a dated event stays, each claim that a hash or branch
is current is replaced by the commands that read position.

Two further stale facts were corrected in the same pass. SPEC-0173's behavior
contract 9 described `tests/fixtures/` as holding test-only synthetic input while
its own Task 0004 emptied that directory, which `git ls-files tests/fixtures`
confirms holds zero paths; the contract now names the underscore-prefixed modules
that replaced it. SPEC-0175's Plan called ADR-0034 proposed after that decision
reached `accepted`.

SPEC-0173's acceptance criteria are otherwise untouched, and no status in that
package changed.

```text
python3 scripts/validation/check-document-metadata.py --mode check-changed
  selected=53 violations=0
python3 scripts/validation/check-document-links.py --mode all
  documents=713 links=6142 failures=0
python3 scripts/validation/check-agent-governance-contract.py   PASS failures=0
python3 -m unittest tests.lib.agent_governance.test_agent_governance_contract
  Ran 39 tests, OK
```

### W8: SPEC-0175 completed and preserved (2026-09-07, local-executed)

That package had measured its own completion contract as satisfied and left one
row in Deferred Items: the move itself, described as a bounded change with its
own approval. The approval was given for this session and SPEC-0176 owns the
change, so the deferral is closed rather than carried.

The three documents transitioned and moved in one result tree, because a terminal
status inside an active stage is what the corpus check rejects and moving one
member while its siblings stay is what the retention guard rejects. The
preservation unit is the whole package under the decision accepted at W5, so the
Plan and the Task are preserved beside the Spec. No Tombstone was created:
completion is explained by terminal status and lineage, and one would have
recorded a withdrawal that did not happen.

```text
docs/98.archive/completed/03.specs/0175-governance-knowledge-and-prompt-surface/
  spec.md                                        status: completed
  plan.md                                        status: completed
  tasks/tsk-0001-knowledge-and-prompt-surface.md status: completed
ls docs/03.specs/                                0173, 0176, README.md
```

The Stage 03 index row moved to the archive paths in the same tree, and two
inbound links were repointed. The Task's dated observations were not rewritten;
the four stale statements W7 corrected were fixed before the move so the archive
receives a body that is accurate about the branch it ran on rather than one that
freezes a dead branch name as current.

### W9: The archive evidence claim that pointed at nothing (2026-09-07, local-executed)

`docs/README.md` listed "Plan and Task evidence: co-located in the owning Spec
Package" for SPEC-0095 and SPEC-0096, and both archives hold `spec.md` alone:

```text
find docs/98.archive/completed/03.specs/0095-infra-secrets-docs-refresh -type f   spec.md
find docs/98.archive/completed/03.specs/0096-llm-wiki-agent-first-completion -type f   spec.md
```

Those two packages were disposed under the Spec-only model, so the rows now say
the bodies are not preserved and name Git history as their only recovery path,
with the decision that changed the rule linked beside them. This is the
distinction ADR-0033 keeps: the current rule preserves every member, and the
scope a past package was preserved with stays a historical fact rather than
becoming a gap to back-fill.

```text
python3 scripts/validation/check-document-metadata.py --mode check-changed
  selected=57 violations=0
python3 scripts/validation/check-document-corpus-lifecycle.py
  violations=0; preserved=156 recovery violations=0
python3 scripts/validation/check-document-links.py --mode all
  documents=713 links=6146 archive_direct_links_total=70 failures=0
python3 -m unittest tests.lib.document_governance.test_spec_packages test_archive
  Ran 61 tests, OK
```

### W10 and W11: Generated outputs and the final gate (2026-09-07, local-executed)

The LLM Wiki generator builds its inventory from `git ls-files --cached`, so it
was run after staging in every commit that changed the corpus rather than once at
the end, and its freshness check was run on the staged tree each time. The
provider hook parity matrix reported fresh without regeneration because no
provider surface changed.

```text
python3 scripts/validation/run-ci-gate.py --profile changed
GATE_EXIT=0
```

The exit code was read from the gate process, not through a pipe. That
distinction is not pedantic here: the W1 run was invoked as
`run-ci-gate.py | tail -25` with `echo $?`, which reported the exit status of
`tail` and printed 0 over a suite that had failed one test.

That run was made against a dirty worktree, and the scope this records is
therefore not reproducible from a clean checkout. `collect_changed_paths` in
`scripts/validation/ci_gate_runner.py` builds the local changed set from staged,
unstaged and untracked paths, so a fully committed tree presents an empty changed
set and the profile narrows to six suites. Both states exit 0; only the selected
scope differs. A later reader reproducing this command should expect the narrower
run and judge by the verdict, not by the suite count.

The output of the dirty-tree run contains 84 lines beginning `FAIL:` and the gate
still exits 0. Those lines are the agent-output eval checker's diagnostic codes
printed by `tests/validation/test_agent_output_eval_fixtures.py`, which feeds
deliberately malformed fixtures and asserts the codes appear; each such test line
ends `ok`. The verdicts are what decide the run: thirteen unittest suites report
`OK`, no line begins `FAILED`, and no check reports a violation.

```text
provider_surface_renderer          PASS providers=2 drift=0
agent_governance_contract          PASS failures=0
document metadata check-changed    selected=58 violations=0
document links mode=all            documents=713 links=6146 failures=0
document corpus lifecycle          violations=0; preserved=156 recovery violations=0
operations catalog                 PASS
script manifest                    PASS
audit semantic freshness           PASS assertions=11 failures=0
LLM Wiki freshness                 both outputs fresh
provider hook parity               matrix fresh
compose validation                 selections=28 services_total=232
template + security baseline       compose_files_total=40 template_adoption_missing=0
unittest suites                    13 runs, all OK
```

One fact was restored rather than corrected while reading that output. The
original `infra/README.md` sentence conflated two different exclusions: the
`.yaml` file is excluded from the template security baseline check, which is
true and the gate prints it as `compose_yaml_files_excluded=1`, and it was
described as excluded from the root include, which is false. The W4 rewrite
removed both halves. The true half is now a row of its own that says which check
excludes it and that the root include does not.

`AGENTS.md` step 4 was found to enumerate `.agents/README.md`, roles and skills
without the two canonical categories, which is the same routing gap W6 closed in
the knowledge map and SPEC-0175 W14 closed in the provider adapters. It is the
third and last entry path with that shape. The Spec's scope and criterion 9 were
amended to cover it rather than leaving the defect outside the contract.

### A concurrent writer moved HEAD under the final commit (2026-09-07, local-executed)

The final commit ran its full hook chain and passed every stage, then git refused
the ref update:

```text
Public validation suites (changed)   Passed
commitizen check                     Passed
fatal: cannot lock ref 'HEAD': is at a13bfd79c005f2ab62f7b5f5716af6cb2490ae3c
       but expected c98df20ddcfc2715c2712ab6dc239fcc00ce1db3
```

A `.gitignore` change, `a13bfd79c`, landed on this branch while the hook chain
was running. Git cannot corroborate who made it: every commit in this range
carries the same `AI Agent <agent@example.com>` identity, so the separate-author
claim rests on the ref-lock error and on session timing rather than on
attribution. What is verifiable is that it was not made by this package's work. Git's ref lock prevented a lost update; nothing
of this package was overwritten and the staged tree survived intact.

The incident was handled by not intervening. The approval boundaries require
preserving another worker's state and not mutating the index during a
concurrency incident, so the in-flight commit was allowed to finish on its own
before anything was inspected, and the other worker's commit was left alone.

The other change was then checked for interference rather than assumed harmless,
because it rewrites ignore rules and this package had just added files:

```text
git check-ignore on every staged path            none ignored
git ls-files _workspace                          README.md and repo-support/README.md still tracked
git ls-files | git check-ignore --stdin          no tracked file is newly ignored
```

It touches one file this package does not own and ignores nothing this package
added. The commit was then re-run against the new HEAD, and the affected gates
were re-run after it, which the same policy requires after a concurrency
incident.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W3 | PASS after review correction: the first PASS was wrong. Verified now by a predicate matching the criterion — 591 tracked current documents scanned, 1 match and it is `infra/README.md:69` asserting that no commented include entry exists | [infra and operations documents](../../../../infra/README.md) |
| 2 | W4 | PASS after review correction: `infra/README.md` and the repository root `README.md` both state the measured 41 files, 40 directories and 41 include entries; the root README had carried 48 / 17 and was missed by the first pass | [root README](../../../../README.md) |
| 3 | W4 | PASS: system scope states 41 files, all included; the SPEC-0171 pending clause is replaced by its completion | [POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md) |
| 4 | W4 | PASS: the include comment describes the six former sibling files as merged and the package as completed | [root docker-compose.yml](../../../../docker-compose.yml) |
| 5 | W5 | PASS: ADR-0033 accepted with supersedes ADR-0031; ADR-0031 superseded with superseded_by ADR-0033 | [ADR-0033](../../../02.architecture/decisions/0033-full-spec-package-preservation.md) |
| 6 | W5 | PASS: blob 904677b0303d277bea44904af68ba86758a10425 to 5bc18f381d1505e108d6fb28a994c2801c58ad83; diff shows only status and superseded_by | [preserved ADR-0031](../../../98.archive/superseded/02.architecture/decisions/0031-preserved-archive-record.md) |
| 7 | W5 | PASS: FR-0009, Constraints and Acceptance Criteria state the Spec/Plan/Task preservation unit; no transient-removal clause remains | [REQ-0026](../../../01.requirements/0026-document-retention-and-retirement.md) |
| 8 | W9 | PASS: the count is replaced by the routing statement the sibling index already uses, and the structure block names 0030- and 0034- | [Stage 02 index](../../../02.architecture/README.md) |
| 9 | W6 | PASS: step 3 names both categories with the conditions bootstrap.md states, and names bootstrap.md as the owner of the order | [repository map](../../../../.agents/knowledge/repository-map.md) |
| 10 | W6 | PASS: the workflow contract half is unchanged since 9ede309a5 and the pre-commit half is dated to 9051977aa, each named separately | [verification surface map](../../../../.agents/knowledge/verification-surface-map.md) |
| 11 | W7 | PASS: `git rev-parse --verify` resolves neither the local nor the remote branch; both packages now state the three Git commands | [SPEC-0173 spec](../../0173-governance-qa-surface-convergence/spec.md) |
| 12 | W7 | PASS: contract 9 names the underscore-prefixed modules; `git ls-files tests/fixtures` returns zero paths and no acceptance criterion changed | [SPEC-0173 spec](../../0173-governance-qa-surface-convergence/spec.md) |
| 13 | W8 | PASS: all three members are `completed` under the archive path and `ls docs/03.specs/` shows only 0173, 0176 and README.md | [preserved SPEC-0175](../../../98.archive/completed/03.specs/0175-governance-knowledge-and-prompt-surface/spec.md) |
| 14 | W8 | PASS: the index row names the archive paths and describes the package as preserved; SPEC-0176 is listed as the draft package | [Stage 03 index](../../README.md) |
| 15 | W9 | PASS: both rows state that the bodies are not preserved and name Git history as the recovery path | [Documentation index](../../../README.md) |
| 16 | W10 | PASS after review correction: AUD-0023 was hand-edited and is now produced by `check-document-metadata.py --mode report`, which places the moved ADR-0031 row in the archive block as `archive-record-superseded`; LLM Wiki and provider hook parity fresh | [frontmatter semantic inventory](../../../90.references/audits/0023-frontmatter-semantic-inventory/README.md) |
| 17 | W11 | PASS: `run-ci-gate.py --profile changed` GATE_EXIT=0 read from the gate process; 13 unittest suites OK, zero FAILED lines, zero violations across every check | [this Task](tsk-0001-stale-fact-convergence.md) |
| 18 | W11 | PASS: two independent reviewers, neither the author, over `git diff e37b2dbcd..3725e08c7`. One approved with follow-up; one blocked with twelve findings. Eleven were accepted, re-measured and corrected; one is routed to another author | [Review Evidence](tsk-0001-stale-fact-convergence.md) |

## Review Evidence

### Independent exact-diff review (2026-09-07, local-executed)

Performed over `git diff e37b2dbcd..3725e08c7`, 90 files, through
[diff-review](../../../../.agents/prompts/diff-review.md), by two reviewers that
did not write the change and did not edit anything.

The verification reviewer re-ran eleven registered checks from a clean checkout,
reading each exit code from the process itself, and confirmed every measured
claim in this Task byte-for-byte or count-for-count, including the ADR-0031
two-line move diff. Disposition: **approve with follow-up**.

The contract reviewer read the diff and the tracked worktree against the
eighteen acceptance criteria. Disposition: **block**, with three findings at
blocker or high severity that this Task had recorded as PASS. Its verdicts are
accepted as given; each was re-measured before being acted on, and each held.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | blocker | Criterion 1 was not met while row 1 recorded PASS. The verifying grep searched the literal strings `optional/commented` and `주석 처리` and never searched `optional include`, the more common phrasing, leaving sixteen assertions in fourteen documents including two lines inside a file this package had edited | Fixed: nineteen statements corrected; criterion 1 is now verified by a predicate that matches the criterion rather than by two literals |
| 2 | blocker | The repository root `README.md` carried the same 48 / 17 counts and the same `주석 처리된 optional include` vocabulary that `infra/README.md` was corrected from, so two current documents stated different values for one measurement and behavior contract 3 was false | Fixed: counts replaced with the measured 41 / 41 and the vocabulary with the profile model; the root README is added to the Spec's in-scope set |
| 3 | high | `docs/90.references/audits/0023-frontmatter-semantic-inventory/README.md` declares `generated_by: scripts/validation/check-document-metadata.py`, and this package hand-edited one row's path in place, leaving that row asserting `status=accepted` and profile `adr` for a document that is now `superseded` | Fixed: regenerated with its own generator, which places the row in the archive block with profile `archive-record-superseded` |
| 4 | high | `infra/04-data/analytics/opensearch/README.md:87` was rewritten to name the surviving file and then, in the same sentence, told the operator to validate with `-f docker-compose.cluster.yml`, a file SPEC-0171 deleted | Fixed: the command now selects `--profile data-cluster` |
| 5 | high | POL-0025 requires Cassandra documentation to identify the implementation as a "single-node optional include", which the guide and runbook this package rewrote now contradict | Fixed: the control names the `data` and `obs` profiles and states that include state never decides whether a service runs |
| 6 | high | POL-0023 and GDE-0023 forbid describing `docker-compose.cluster.yaml` as part of the root include that contains it, and GDE-0023 asserts it is not in the root include | Fixed: both describe the two topologies as separated by `storage` against `storage-cluster` |
| 7 | medium | The deleted `docker-compose.dev.yml` was removed from tables and trees but the surrounding prose still described one file as two leaves, in oauth2-proxy, observability, airflow and n8n, and in the oauth2-proxy catalog subject | Fixed: the two-leaf split is replaced by the `dedicated-valkey` profile distinction the single file actually declares |
| 8 | medium | REQ-0006 was corrected to say `messaging-cluster` renders three brokers; that profile selects `kafka-2` and `kafka-3` only, because `kafka-1` declares `messaging` and `dev` | Fixed: the requirement states which profile selects which broker and that three brokers need both |
| 9 | medium | The Spec's Boundaries declared `docs/99.templates/registry.json` unchanged and SPEC-0173's Task untouched, while the diff changes the identity high-water and repoints links in that Task | Fixed in the Spec, not by reverting: both changes are necessary and are now named as bounded exceptions with their reason |
| 10 | low | The Cassandra guide attributed `cassandra-node1` to `data` alone; the service declares `data` and `obs` | Fixed |
| 11 | low | The tooling claim that role profiles select services individually is false for `locust-worker`, which declares `tooling` only | Fixed in both the tier README and AD-0009 |
| 12 | low, advisory | The `.gitignore` rewrite in `a13bfd79c` drops the `repo-support` negation while its retained comment still describes two tracked contract documents | Not fixed: authored by a different session and outside this package's scope; routed to that author |

Two further findings came from the verification reviewer and are corrected in
this Task rather than in the tree:

- The `--profile changed` evidence recorded at W11 is worktree-state dependent.
  `collect_changed_paths` in `ci_gate_runner.py` scopes the local changed set to
  staged, unstaged and untracked paths, so the thirteen suites and eighty-four
  diagnostic `FAIL:` lines recorded there were produced against a dirty tree, and
  the same command on a clean committed checkout selects six suites and prints
  none. Both exit 0. The record now says which state produced it.
- This Task attributed `a13bfd79c` to "another worker" on the strength of the
  ref-lock error and session timing. Git cannot corroborate that: every commit in
  the range carries the same `AI Agent <agent@example.com>` identity. The claim
  that stands on evidence is narrower and is what matters here — the commit's
  content is orthogonal to this package and newly ignores no tracked file.

Neither reviewer covered runtime, provider entitlement, Hosted CI, or remote
state. The contract reviewer executed no commands, so criteria 16 and 17 rest on
the verification reviewer's re-run and on this Task's own records. Neither
reviewer re-checked the corrections made in response to their findings; that
re-review is recorded below as its own state.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `80b42feaa` | W1 package definition |
| `51e203b71` | W2-W4 Compose enablement convergence |
| `f71449eff` | W5 and W9 preservation-owner promotion |
| `b5d4181d0` | W6 and W7 knowledge routing and Git-read position |
| `c98df20dd` | W8 and W9 SPEC-0175 preservation and archive evidence |
| `3725e08c7` | W10 and W11 entry-path closure and final verification |
| pending | Review-finding corrections |

## Rulings

- SPEC-0173 is not modified beyond the two stale sentences SPEC-0176 names.
- A guard that fires is treated as correct until proven otherwise; the change is
  adjusted rather than the guard weakened.
- Static configuration and local test results never establish native runtime
  discovery, provider entitlement, Hosted CI, or remote state.
- Unexecuted checks are recorded as NOT_RUN or BLOCKED with their missing input
  and are never promoted to a PASS.

## Deferred Items

| Item | Blocking input or reason |
| --- | --- |
| Re-review of the corrections made in response to the blocking review | The two reviewers judged the tree at `3725e08c7`; the eleven corrections that followed have not themselves been independently reviewed |
| The `.gitignore` `repo-support` negation dropped by `a13bfd79c` | Authored by a different session and outside this package's scope; routed to that author |
| This package's own lifecycle walk to `active` | The transition check reads the merge base with `origin/main`, and the remote cannot advance without a push that no authorization here grants |
| `ADR-0034`'s discharged Follow-up item | Its first bullet still says to transition the decision to `accepted` only after SPEC-0175 records its evidence, and the decision has read `accepted` since that package landed. ADR-0034 is an accepted decision, and editing an accepted body to agree with a later state is what the retention policy forbids, so this is routed to the decision owner rather than corrected here |
| SPEC-0173 completion | Unchanged by this package. Its aggregate remains BLOCKED on the actual PostgreSQL operating and image leaf, and its native runtime and Hosted CI evidence remain unobserved. This package closed only its retention-owner dependency |
| `oauth2-proxy` declaring the `dev` profile twice | Observed while reading `profiles:` values in W2. It is a Compose file change, not a document change, and this package's scope excludes every Compose file |

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
- [Stage 03 index](../../README.md)
