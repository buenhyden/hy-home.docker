---
title: "Stale Fact Convergence Execution"
version: "0.20.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-15"
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
  and local integration into `main`. Deployment, live service action, secret
  values, and global installation remain unauthorized. The operator extended
  this twice, as W19 and W20 record: push on 2026-09-14, and then push, local
  integration and branch cleanup for W20. The local push hook did not block a
  direct push to `main`. GitHub reported each such push as bypassing the
  pull-request and required-check rules, and the Task records that as observed.
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

### W12: The predicate that was wrong in a language it never searched (2026-09-07, local-executed)

The Deferred Items required a review of the corrections themselves. One
independent reviewer, not the author, judged the working tree at `edc5162fb`
against the eighteen criteria and returned `block` with five findings. The
reviewer had no shell and said so before reviewing anything, then reported which
criteria its method could not reach.

Two findings were blocking and both held on re-measurement.

The first is the one that matters. Criterion 1 had been recorded PASS twice, and
both records were false. The first predicate searched two English literals. The
correction replaced it with eleven English literals and reported "591 documents
scanned, 1 match", which reads like thorough verification. It was not: the
repository's output-style contract authors Stage 01-05 documents in Korean, and
the surviving assertions were written `선택 include`. Six catalog guides told an
operator to check an include state that has not existed since SPEC-0156, and
`infra/04-data/lake-and-object/minio/README.md:62` called `docker-compose.cluster.yaml`
"local only" while the root file includes it at line 226.

`docs/05.operations/catalog/04-data/0025-cassandra/guide.md` contradicted itself
inside eighteen lines: line 22, corrected by this package in W3, states that the
root includes the file unconditionally; line 40, untouched, told the reader to
verify the optional include state.

The second blocking finding is that Review Evidence row 7 dispositioned four
surfaces "Fixed" when two of them were not. `airflow/README.md:17` and `:87`,
`n8n/README.md:88`, and `POL-0044:41` still described one Compose file as two
leaves. Measured against the tree: `infra/07-workflow/airflow/` holds exactly one
Compose file, and `airflow-valkey` sits at line 368 with a `profiles:` list
whose only entry is `dedicated-valkey`. The broker is chosen by
`${AIRFLOW_VALKEY_HOST:-mng-valkey}`, which is the same shape the corrected
oauth2-proxy README already states.

All seven criterion 1 survivors and all four two-leaf surfaces are corrected.
Each replacement names the profiles read from the service's own `profiles:` list,
parsed with `yaml.safe_load` rather than grepped.

Criterion 1's wording was never the problem; it says "commented, optional, or
absent" without naming a language. The Spec now records that the verifying
predicate must cover every language the corpus uses, and that a low match count
from a single-language predicate is not evidence. That is a tightening of the
verification requirement, not a relaxation of the criterion.

The lifecycle statement in the Spec's Boundaries was also wrong, and this Task
had repeated it. It said a document absent from the merge base "admits none" of
its transition budget. Measured by setting this Spec to `active` and reading the
diagnostic, the check emits `invalid-initial-status: new spec documents must
start at draft` — a creation rule, not a budget rule. The distinction changes the
remedy: once the remote carries this package at `draft`, one later change can
advance it, rather than one change per branch. The Spec now states the measured
rule and names `resolve_base_selection` as its owner.

Two items left the Deferred list by being fixed. `.gitignore` lost the
`repo-support` negation when `a13bfd79c` replaced the recursive `_workspace/**`
pattern with the anchored `/_workspace/*`; a file cannot be re-included while its
parent directory is excluded, so the anchored form silently dropped
`_workspace/repo-support/README.md`, a tracked file, to ignored. The three-step
ladder is restored and verified in an isolated repository before being applied
here. `_workspace/README.md` documents its own verification commands but no
registered check runs them, which is why every gate passed over a broken
contract; its Tracking Contract now states the rule that actually holds and why
changing the outer pattern breaks the inner one.

### W13: The deferred items, worked under an explicit scope extension (2026-09-07, local-executed)

Five Deferred Items were carried because each needed either a surface this
package excluded or an authorization it did not hold. The operator named all
five and asked for them, which is the authorization the earlier rows were
waiting on. This section records what that produced, including where the answer
was "measured, not done".

#### The two-leaf residue, corrected as one mistake rather than 48

The earlier row counted 86 statements in 48 documents and called it a separate
package. Working it showed the count was the wrong unit. Only one infra
directory holds more than one Compose file (`infra/04-data/lake-and-object/minio`);
every other holds exactly one. So every statement describing a directory as a
root-included leaf plus a separate service-local leaf is the same mistake: when
SPEC-0156 and SPEC-0171 replaced conditional includes with "include everything,
let the profile select", the documents were never re-expressed. What reads as a
file distinction is a profile distinction. Forty-one statements across
twenty-six documents were corrected on that translation, each against the parsed
Compose file rather than against the vocabulary.

Not every match was a defect, and the triage mattered more than the sweep. Two
shapes look alike: a claim that two files exist, which is false, and a statement
that a service's own Compose file cannot be rendered standalone because it needs
root `infra_net` and secret context, which is true and describes the single file
correctly. Roughly thirty lines of the second kind were left untouched.

| Family | Documents' claim | Measured |
| --- | --- | --- |
| Airflow and n8n broker | a root-included dev compose and a service-local compose declare different brokers | one file each; `airflow-valkey` and `n8n-valkey` sit in it under `profiles: [dedicated-valkey]`, and `${AIRFLOW_VALKEY_HOST:-mng-valkey}` / `${N8N_VALKEY_HOST:-mng-valkey}` default to the shared broker |
| Kafka broker count | a root dev single-broker compose and a service-local full 3 broker compose | one file; `kafka-1` is `messaging`/`dev`, `kafka-2` and `kafka-3` are `messaging-cluster` |
| nginx linkage | `not root-included by default` | root `docker-compose.yml:213` includes it, one of 41 unconditional entries |
| k6 and StarRocks linkage | `local compose only` | both root-included; selected by `tooling`/`testing` and `data` |

Three matches survive deliberately. `ADR-0007:31` and `ADR-0022:26` keep their
original sentences because an accepted decision records what was decided, not
what the implementation later became; each gained a note naming SPEC-0156 and
SPEC-0171 and the profile that replaced the file boundary, so the change is
recorded rather than silent. `descriptions/0006:90` is not a defect: it lists
two validation activities, not two files.

#### The `_workspace` check, and the flag the whole thing turns on

The contract now has a registered check:
`test_workspace_contract_documents_stay_reachable` in
`tests/lib/test_surface_ownership.py`, reached by
`leaf.repository-integrity-regressions`.

The first version of it passed against a deliberately broken `.gitignore`. That
is the finding worth keeping. `git check-ignore` consults the index first and
will not call a tracked file ignored, so after `a13bfd79c` dropped the negation
the document stayed tracked and every question about its ignored state answered
no while the rule that re-included it was gone. `--no-index` asks the exclude
rules alone. The check was rebuilt on it and then proven by breaking the
contract on purpose: it fails with
`[] != ['_workspace/repo-support/README.md']` and passes again on restore.

`_workspace/README.md` had worked around the same blind spot without naming it,
by probing a scratch path instead of a contract document. Its verification block
now names `--no-index` and says to read the printed rule rather than the exit
status, because `-v` exits 0 whether the matching pattern excludes or
re-includes.

#### The two items that were measurement, not change

`oauth2-proxy` declared `dev` twice at `docker-compose.yml:17-18`. Parsing all
Compose files confirmed it was the only duplicate in the repository; the line is
removed and `profiles` reads `['core', 'auth', 'dev']`.

SPEC-0173 was not advanced, and the reason is its own ruling rather than a
missing effort. `tsk-0006:198` records that a BLOCKED check is not a valid
terminal transition and instructs that the Spec and Plan stay active with
in-progress Tasks, and that acceptance criterion 15 is not waived. Completing it
by editing statuses is the one thing that Task forbids.

What is new is the shape of the blocker, measured rather than repeated. Docker
is available here (server 29.7.2) and the handoff directory
`_workspace/repo-support/task-2026-07-19-.../postgres` is empty, so
`invalidate_canonical_handoff` would destroy nothing. The block is not stale
state; it is that `leaf.postgres-logical-upgrade-config` runs
`scripts/operations/rehearse-postgres-logical-upgrade.sh --check-config-only`,
and `RUN_MODE=check` still reaches `assert_safe_images_paths_and_project`
(`docker image inspect` and `docker image save` into
`/tmp/hyhome-ior-evidence.<pid>`) and `cleanup_owned_projects_and_tmp`
(`docker ps -aq --filter label=...` followed by removal). Those are runtime
Docker operations, including container removal, and they need an explicit
approval this Task does not carry. The item stays deferred with that named.

The `--check-config-only` half of that was then authorized and run; the evidence
is recorded in SPEC-0173's `tsk-0006` where it belongs. It exited 0 with
`status=check-passed` and moved nothing: containers 15 to 15, images 71 to 71,
handoff entries 0 to 0, `/tmp` evidence directories 0 to 0. One leaf changed
state; the package did not.

#### The gate's own defect, found while it kept failing

Two gate runs failed on two different tests, both in the "changed while opening"
guard family. Neither failure was caused by this work.
`_open_directory_path` in `scripts/lib/document_governance/spec_packages.py`
walks from the filesystem root down and verifies every parent component, and
`_directory_snapshot` compares `st_nlink` and `st_mtime_ns` alongside `st_dev`
and `st_ino`. A test fixture under `/tmp` therefore makes `/tmp` a verified
parent. Creating one directory in `/tmp` changes the snapshot while the identity
fields are untouched:

```text
before: (2096, 73729, 17407, 487, 1788773190218409786, ...)
after:  (2096, 73729, 17407, 488, 1788773190218972267, ...)
```

`st_dev` and `st_ino` prove it is the same directory, so no symlink swap
occurred; only fields that any other process can move differ. Seven or more
concurrent test and gate processes, including another session's, were writing to
`/tmp` throughout. The consequence is that the public suites are
non-deterministic on a shared machine. The same comparison appears at
`references.py:252,360`, `archive.py:322,415`, `architecture.py:126` and
`requirements.py:455`. Not fixed here: `scripts/**` is protected and this is a
guard change, not a stale fact. Recorded as a Deferred Item.

#### A reading mistake worth recording

Mid-commit, `git status` showed thirteen edited files as unmodified and the work
appeared lost. Nothing was lost. `pre-commit` sets unstaged changes aside in its
own cache, not `git stash`, and restores them when hooks finish, so the working
tree during a running commit is the hook's intermediate state and not the
repository's. The same shape as reading a gate's exit code from the wrapper
instead of from inside the redirect: the observation was taken from the wrong
process at the wrong moment.

### W14: The third review round, and the third time the predicate was the defect (2026-09-07, local-executed)

An independent reviewer judged `7e1a23d40..ec041eff3` and returned `block` with
three blockers. It opened by reporting that it had no shell, could not reproduce
the diff, and had reviewed the working tree instead, naming which of its checks
were tool-verified and which were reasoning. Every finding it raised was
reproduced here and every one was correct.

| # | Severity | Finding | Reproduced |
| --- | --- | --- | --- |
| 1 | `blocker` | `infra/01-gateway/nginx/README.md:17,19` still says the leaf is not root-included, contradicting rows 58 and 61 of the same file, which W13 rewrote | Yes, in English and Korean, in a file W13 edited |
| 2 | `blocker` | `ADR-0001:31` carries the same false claim in Korean, present tense, with no note | Yes |
| 3 | `blocker` | `infra/05-messaging/kafka/README.md:17` — a W13 rewrite left a false second clause contradicting its own first clause | Yes |
| 4 | `high` | `airflow/README.md:54` and `n8n/README.md:55` name the same file on both sides of a distinction | Yes |
| 5 | `medium` | The `root-active` versus `profile-only` contrast has no basis: `traefik` is `core`/`dev`, `nginx` is `nginx`, and neither resolves without a profile | Yes |
| 6 | `low` | POL-0006 says 39 service directories; `infra/README.md` implies 40 | Yes, measured 40 directories and 41 files |
| 7 | `low` | The new negative test does not neutralise ambient `core.excludesFile` | Yes, accepted as advisory |

The third round found the same class the first two did, for the third distinct
reason. Round one searched English against a corpus the output-style contract
requires to be Korean. Round two swept only the lines an earlier review had
named. Round three used a vocabulary list — `dev compose`, `local compose`,
`service-local` — while the survivors said `not included in the current root
compose stack by default`, `기본 include되지 않으므로`, `production-like compose`
and `full 3 broker Kafka compose`. Not one of them contains a listed term.

The pattern is now legible and belongs in the record: each round defined the
defect by the shape its own predicate could see, and each predicate's boundary
was mistaken for the defect's boundary. The fix that finally held was to stop
enumerating vocabulary and search for the claim instead — any sentence that
denies a root include or asserts a second Compose file, in either language —
and then to check every match against the parsed YAML rather than against the
wording.

Twenty-three statements were corrected across fourteen documents. The root
`docker-compose.yml:204-205` settles the gateway question in its own words:
"Every file below is included unconditionally; Compose profiles decide what
starts. Selecting no profile resolves no service." So `traefik` (`core`, `dev`)
and `nginx` (`nginx`) differ in which profile selects them, never in whether the
root includes them. The operational distinction was kept and the false include
framing removed. `ADR-0001:31` keeps its sentence and gains a note in the shape
already used for `ADR-0007` and `ADR-0022`.

### W15: Rounds four and five, and the shape no text predicate reaches (2026-09-07, local-executed)

Two more independent reviews ran. Both blocked. Both were right.

Round four found `infra/09-tooling/k6/README.md:71` denying its own root
include while lines 88 and 91 of the same file asserted it, and
`REQ-0012:45` naming four of the six services the `admin` profile selects.
Round five found five more, and its diagnosis is the part worth keeping.

The survivors carry no include vocabulary at all:

| Finding | Shape |
| --- | --- |
| `POL-0078:140-142` | a conditional deferral: "이 쌍의 topology selector는 SPEC-0171이 결정할 때까지 등록하지 않는다", for six sibling files SPEC-0171 merged and a package that completed |
| `POL-0078:18` | a bare cardinal in a scope sentence: `24개`, measured 28 |
| `infra/11-laboratory/README.md:88-90` | a parenthetical marker on three of five list rows |
| `infra/README.md:127-134` | a runnable fence that cannot run: `cd infra/01-gateway/traefik && docker compose up -d` fails on the undefined `infra_net`, and `traefik` is `core`/`dev` so a bare `up` resolves nothing |
| `infra/09-tooling/k6/README.md:65` | an environment table documenting `LOCUST_HOST_PORT`/18089, the pre-split state POL-0078:133 records as retired in favour of `K6_HOST_PORT`/18189 |

Five predicates have now been wrong in five ways: language, position,
vocabulary, claim shape, and now form — a deferral clause, a cardinal, a
parenthesis, a code fence, a table row. The reviewer's reading is the one to
record: the recurrences share a property no text predicate has. **A document
contradicts itself, or contradicts its governing sibling, about a fact the
parsed YAML settles.** Two mechanical checks would have caught all six
documentation findings: assert that every service and profile enumeration under
Stage 01-05 and `infra/**` agrees with the generated `DATA-0059` snapshot, and
assert that every fenced command in a README or runbook is non-empty and names
a path that exists. Both belong under `scripts/**` and `tests/**`; neither is
written.

The reviewer also read the working tree while a commit was in flight and
reported four findings that were already corrected. That is the same window
that made thirteen files look lost earlier in this package, and it is recorded
here because it cost a review round's credibility, not because the reviewer
erred: a review of an uncommitted tree cannot attribute a line to a commit.

#### The guard change, and the record that denied it

W13 recorded the parent-component guard defect as deferred because `scripts/**`
is a protected surface. The operator then authorized it, and the change was
made in the same session while the Deferred Item still said it was not. Round
five caught that discrepancy. The record is corrected here.

`_path_identity(metadata) -> (st_dev, st_ino)` now carries the open-time check
in `spec_packages.py:139`, `references.py:201` and `archive.py:294`. The fuller
six-field snapshot is retained for load-time verification and for enumeration,
and file-content guards such as `architecture.py:124` are untouched. Type is
still enforced three ways: `S_ISLNK`/`S_ISDIR` on the pre-open stat, `S_ISDIR`
on the opened descriptor, and `O_NOFOLLOW | O_DIRECTORY` on the open itself.

Measured with one thread creating and removing directories in `/tmp`:

```text
before the change: 242 loads, 65 failures ("Stage 03 parent changed while opening")
after  the change: 236 loads,  0 failures
```

No security property is weakened. The check exists to prove the descriptor
refers to the object that was stat'd, and device plus inode is exactly that.
Link count and timestamps move whenever any unrelated process writes into a
shared parent, and an attacker who swaps a directory can match a timestamp with
`utimensat` but cannot match an inode. Two tests were added first and failed
first: one asserts that benign churn in a traversed parent leaves identity
unchanged while the full snapshot moves, the other that distinct directories
still separate.

### W16: The re-baseline that measured this package against a later HEAD (2026-09-10, local-executed)

A repository-wide convergence request arrived on 2026-09-10 with local `main` at `82ebe9d22` and a clean worktree, asking for the governance, QA, CI/CD and commit surfaces to be investigated, converged and committed. It was written on the assumption that the convergence had not happened. Measuring this package's fourteen behavior-contract items against that HEAD showed thirteen already satisfied by W1-W15, and located the fourteenth as a sweep that reached two of the three files it needed to reach.

| Contract item | Measured result at `82ebe9d22` |
| --- | --- |
| 1 Compose enablement wording | Zero hits for a bilingual predicate over `infra/**`, `docs/05.operations/catalog/**` and `docs/02.architecture/descriptions/**`. Recorded as a fifth predicate result and not as a promotion: this Task's Ruling on criterion 1 stands, and a fifth predicate finding nothing is exactly the weak evidence that Ruling describes |
| 2 conditional-activation model | `infra/README.md:61` and root `README.md:95` both state unconditional include with profile selection |
| 3 Compose counts | 41 root `include:` entries, 41 tracked Compose files, 40 service directories; every claim matches |
| 4 retention owner chain | `REQ-0026:109` and `AD-0030:76` both state Spec, Plan and every Task |
| 5 ADR-0031 preservation | `status: superseded` with `superseded_by: ADR-0033`, preserved under `docs/98.archive/superseded/` |
| 6 no retroactive Plan or Task | unchanged |
| 7 Stage 02 index | NOT satisfied; see below |
| 8 repository map load order | `.agents/knowledge/**` and `.agents/prompts/**` appear in both the surface table and the restated order |
| 9 knowledge provenance | each transcribed source carries its own commit |
| 10 no dead branch as position | `codex/0173-agent-governance-home` resolves nowhere and appears in no active Spec or Plan. Its remaining occurrences are dated Work Log evidence inside SPEC-0173 `tsk-0006`, which is what a dated observation is supposed to look like |
| 11 SPEC-0175 preserved | three bodies at `completed` under `docs/98.archive/completed/` |
| 12 SPEC-0173 fixture sentence | `spec.md:124` reads "and the directory is absent" |
| 13 generated outputs | `provider_surface_renderer.py --check` reported `PASS providers=2 drift=0` |
| 14 changed profile | exit 0 in 28.37 s on a clean tree; 302 s once a Stage 02 document is in the change set, because three document suites join the fallback |

Item 7 was a partial sweep. W9 corrected the parent `docs/02.architecture/README.md` by adopting the sibling `decisions/README.md` wording, and named the wording it adopted. It did not reach `docs/02.architecture/descriptions/README.md`, which kept `현재 26개의 Description을 보유한다` against a measured 25. The wording W9 chose is now in the third file, so the defect class is closed across all three rather than in two of them. Correcting 26 to 25 was available and was not taken, for the reason W9 had already recorded.

Three numbers in the root README were outside every criterion. Criterion 2 verified that file's Compose counts and nothing else. The same snapshot table carried `Root Compose secret declarations | 69` against 70 top-level `secrets:` keys, `Parent-repo tracked README files | 173` against the 185 that its own note says `git ls-files '*README.md'` reports, and `secrets/ value/cert files | 94`, which matches neither the 19 tracked paths nor the 97 files on this disk. The first two are corrected and the secret row now names the source it is read from. The third row is removed rather than corrected, because `secrets/` is deliberately untracked: no check can reproduce a number there, and a number no check can reproduce is the thing this package exists to remove. A closing sentence records that rule so the row is not restored later.

These three are the class the Deferred Item on enumeration and fence-integrity checks describes. They are not a regression of W1-W15, because no criterion asked for them.

Nothing in this entry changes a recorded result, a status, or a criterion of this package or of SPEC-0173.

### W17: The two rows that outlived their inputs (2026-09-10, local-executed)

Re-reading this Task's Deferred Items against `82ebe9d22` found two rows describing a repository that has moved. The lifecycle row waited on a push to carry the package at `draft`; `git show origin/main:` reports `draft` for the Spec, the Plan and this Task, so that push has happened and the row's blocking condition no longer holds. The enumeration row named the generated `DATA-0059` snapshot as the comparison input; that package is retired with a tombstone and SPEC-0173 W34 emptied Stage 90 data, so the design cannot be built as written.

Neither row was wrong when it was written. Both are the finding this package exists to record: a statement that was true stops being true and nothing reads it again.

### W18: One check earned its place and one did not (2026-09-11, local-executed)

This row deferred two mechanical checks. Both were measured before either was written, and they came out differently.

The fence check found real defects. Seven active surfaces carried a fenced command naming a script that no longer exists, all of them casualties of the generator retirement in SPEC-0173 W34: `.agents/governance/hooks/hookify.warn-hook-parity-edit.md` instructed `report-provider-hook-parity.sh`, the Compose profile vocabulary policy instructed the coverage generator whose `DATA-0059` output is itself retired, the release-management runbook and SPEC-0173's own plan instructed `generate-llm-wiki.py`, and `scripts/README.md` carried five such lines. None of these is reachable by a link check, because a fenced line is not a link. All are corrected, and `--mode commands` now exits 0.

The check is a mode on `check-document-links.py` rather than a new validator, so `leaf.docs-traceability` reaches it through the `--mode all` it already runs and no gate node, suite, or contract entry changed. Preserved bodies under `docs/98.archive/` are excluded through the existing `_PRESERVED_LINK_PREFIXES`, because naming a dropped path is what a preserved record is for and its bytes may not be edited. `secrets/` is excluded because those files are the operator's. The remaining five blocks are illustrative rather than runnable — two anti-pattern examples, a `git check-ignore` probe whose argument must not exist, a negative search pattern, and a usage placeholder — and each says so with `# doc-paths: illustrative`, a stated marker in the document rather than a predicate that has to guess. Authoring rule 16 owns the marker.

The enumeration check was not written, for the reason the row now records: 534 `--profile` references across tracked documents, one exception, and that one in a Stage 90 note about a different tool. Its original design named the generated `DATA-0059` snapshot as the comparison input, and rebuilding it on a static parse of the tracked Compose files is possible; what is missing is a defect for it to catch.

Locating an enumeration inside prose is also the exact operation that produced five wrong predicates in W12 through W15. The fence check avoids that by reading a delimited block rather than a sentence, which is why it is the half of this row that could be built honestly.

### W19: The enumeration check, built on the owner's table, and criterion 1 amended (2026-09-14, local-executed)

The operator asked for both open items to be resolved, approved fixing separate defects found along the way, and authorized commit, local merge, push, and branch cleanup. That push authorization is the operator's, given for this entry. It does not change what this Task's Inputs recorded for earlier entries, and the hook-blocked direct push to `main` is still not attempted by another route. `git fetch` showed `origin/main` at `1bfa67525`, equal to local `main`, so the commits W16 through W18 produced are already on the remote.

W18 measured the wrong input. It counted `--profile` references in prose, found one exception in 534, and concluded there was no defect to catch. The enumeration that has an owner is POL-0078's three tables. Its Verification section states two facts: the tables' names equal the declared `profiles:` values, and each row's service count equals the number of services declaring that profile. The root `include:` comment states a third, that every Compose file under `infra/` appears in the list. The input that used to be compared against those numbers was the `DATA-0059` snapshot, retired in SPEC-0173 W34, and nothing has read them since. A stated invariant without a check is the class this package exists to record, whether or not it has drifted yet.

`validate_compose_profile_vocabulary` in `scripts/lib/document_governance/operations_catalog.py` makes the comparison, and `check-operations-catalog.py` calls it, so `leaf.operations-catalog` reaches it without a new gate node, suite, contract entry, or manifest row. It reads only table rows, a backticked name in the first cell and an integer in the last, so the mutually exclusive pairs table is never read as vocabulary. It parses every tracked `infra/**/docker-compose*.yml` and `.yaml` with `yaml.safe_load`. YAML drops comments, so a commented `include:` entry is reported as missing rather than guessed at.

Eight tests were written first and failed first on the import. They cover the current repository, a matching fixture, a declared profile with no row, a row no service declares, a wrong service count, a tracked file missing from `include:`, an included path that is not a tracked Compose file, and an unparseable Compose file. All eight pass. On the current tree the check reports zero findings over 41 files, 138 services, and 28 profiles. Three drifts injected into the real tree through the reader produced exactly three findings: the `data` count lowered to 57, the `sync` row removed, and the `k6` include line commented out.

```text
compose-include-drift: docker-compose.yml: infra/09-tooling/k6/docker-compose.yml is tracked and not included
compose-profile-vocabulary-drift: …/policy.md: profile sync is declared by 1 service(s) and has no row
compose-profile-vocabulary-drift: …/policy.md:59: profile data row counts 57 service(s); Compose declares 58
```

Criterion 1 is amended in the Spec rather than promoted. This Task's Ruling that kept it NOT MET is sound and stands: no text predicate over a bilingual prose corpus has been shown complete. That also means no evidence could ever satisfy the old wording, which makes it a permanent NOT MET rather than a criterion. W9 met the same shape with a count criterion and amended it to require a routing statement. The amended criterion requires what can be proven. A registered check holds the fact every include-state sentence depends on, and the two owners state the model. The five predicate results are recorded as supporting evidence and not as proof. The original universal negative is not claimed.

Three other statements in the Spec had gone stale through this package's own work and are corrected. The out-of-scope list named every validator as unchanged, although W18 and W19 each changed one. The interfaces section and the operational impact section said the same. The Open Question about this package's own lifecycle walk had been answered by the walk. POL-0078's Traceability also named the retired coverage generator as its evidence, and it now names the check.

Two separate defects were found and fixed. `.agents/skills/style-validation/SKILL.md` and `.agents/skills/infra-validate/SKILL.md` named the scripts they own as `scripts/classify-changed-files.sh` and `scripts/static-checks.sh`. A reader takes those as repository-root paths, where no such file exists, and the link checker reads them the same way: `_normalized_target` resolves a `scripts/` prefix from the root. Written as `./scripts/…` links, both now resolve beside the skill and are checked. The first attempt without `./` produced three `missing-link-target` findings, and that is how the resolution rule was found.

One observation was investigated and is not a defect. `test_python_entrypoints_expose_closed_cli_help` fails three subtests under a bare `python3 -m unittest`, because `ci_gate_contract.py`, `ci_gate_runner.py`, and `github_workflow_contract.py` import `scripts.` without touching `sys.path`. Commit `17bb5cdd5` chose that on purpose. It replaced the path manipulation with an isolated, descriptor-anchored bootstrap passed as `PYTHONPATH` under `PYTHONSAFEPATH=1`, so the test passes only through the registered gate. Restoring `sys.path.insert` to satisfy a bare runner would undo that hardening. The code is not changed.

The first attempt to commit the check failed in `public-validation-changed` on `test_timeout_still_cleans`. It exited 60 (`owned-cleanup-failed`) where the test expects 20. The test overrides the budget to 5 seconds in total with a 2 second cleanup reserve, which is tighter than the script's own timeout negative case of 20 and 8. It then passed three times alone and twelve times concurrently, and the retried commit passed the same hook. Because it was not reproduced, the budget is not changed on a guess. It is recorded so that a recurrence has a first data point.

```text
python3 -m unittest …ComposeProfileVocabularyTests          Ran 8 tests  OK
python3 scripts/validation/check-operations-catalog.py      operations-catalog: PASS
check-document-links.py --mode all                          documents=881 links=6593 failures=0
check-agent-governance-contract.py                          PASS failures=0
provider_surface_renderer.py --check                        PASS providers=2 drift=0
check-document-metadata.py                                  exit 0
markdownlint-cli2 (four edited documents)                   0 error(s)
ruff check / ruff format --check (three Python files)       clean
```

### W20: A repository-wide audit, round six, and the first lifecycle step (2026-09-15, local-executed)

The operator asked on 2026-09-14 for the documents under `docs/` to be checked for stale facts and for statements that contradict the implementation. Every Spec, Plan and Task was to be checked for unfinished work and for conflicts with later requests. Nothing unfinished was to be implemented; work already done was to be recognised, and work that later implementation overtook was to be superseded or dropped. The request also authorized fixing separate defects, commit, integration, push and branch cleanup.

Seven read-only audits covered Stage 01, 02, 05, 90 and 99 and the indexes. One more reviewed SPEC-0173, and round six reviewed this package. Their findings were re-measured before any edit. One class was closed mechanically rather than by reading. Every documented `repo:tag` was compared with the tags the Compose files and Dockerfiles pin, which found forty stale tags, including service READMEs the audits had scoped out. Three dependabot updates then merged to `main` during the work and moved twenty-one of the tags that had just been aligned. They also left `infra/tech-stack.versions.json` behind, so the required drift leaf failed every commit on top of `main` until `14d9ff6dc` carried the registry and its documents together. Copying a tag into prose is what makes each bump stale a document; the comparison is recorded as repeatable, not as a one-time sweep.

The audits also found claims the implementation does not carry. A registry policy required a delete setting nothing sets. A k6 volume contract had been copied from Locust. A hardening guide named a Dockerfile user the image does not use. An address table listed an Atlantis service no Compose file defines. `scripts/README.md` described seven retired scripts as current entrypoints. The documentation index still routed LLM navigation to a retired index. Each was corrected at its owner.

SPEC-0173 was taken to completion rather than implemented further; its Task 0006 W40 holds the reasoning. Preserving it exposed a validator defect that no earlier completion had reached. RES-0085-m0001 records an identity recovery whose decision lives in SPEC-0173 Task 0001, and the recovery check accepted only a Task under Stage 03. The retention policy therefore made every valid disposition of that record fail. The check now also accepts a Task preserved as completed and still rejects superseded and retired ones (`c36bda522`). The commit hook first reported the preserved package as `package-retirement-unrecorded`. The actual cause was two receipt cells that opened with a qualifier instead of the PASS marker; the completion check swallowed that error and reported a missing tombstone instead.

Round six and its dispositions are recorded under Review Evidence. This entry takes one lifecycle step: the Spec moves from `review` to `approved`. The Plan and the Task stay where they are, because an active Plan or an in-progress Task requires an active Spec.

### W21: Round seven, and the second lifecycle step (2026-09-15, local-executed)

The round-six corrections were reviewed by a reviewer who had not made them, and
the thirteen findings are recorded under Review Evidence with their
dispositions. Two of them were blockers of the kind W20 had already met in
SPEC-0173: a result cell that opened with a qualifier, and work units that no
receipt row named. A completion check that reads the receipt would have
rejected this package on both.

This entry takes the second lifecycle step. The Spec moves from `approved` to
`active`, the Plan from `approved` to `active`, and this Task from `ready` to
`in-progress`, measured against `origin/main` at `9c039bcf9`, where the first
step already stands. The corrections this entry makes are themselves
unreviewed, so completion still waits on a review of them and on the changed
profile over the final path set.

```text
python3 -m unittest …test_operations_catalog          Ran 51 tests  OK
python3 scripts/validation/check-operations-catalog.py  operations-catalog: PASS
provider_surface_renderer.py --check                    PASS providers=2 drift=0
```

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W12 | PASS: supporting evidence under the amended criterion; the bilingual predicate closed the language gap its English-only predecessors left, and it is not claimed complete | [spec.md criterion 1](../spec.md) |
| 1 | W14 | PASS: supporting evidence under the amended criterion; the claim-shape sweep corrected the residue rounds three and four found, and round six showed it moved the blind spot rather than closing it | [spec.md criterion 1](../spec.md) |
| 1 | W19 | PASS: as amended in W19, `check-operations-catalog.py` holds the root include list and the POL-0078 tables to the tracked Compose files, exits 0 on the current tree and reports each injected drift; the root `include:` comment and POL-0078 state the model | [Operations catalog check](../../../../scripts/validation/check-operations-catalog.py) |
| 1 | W3 | PASS: supporting evidence under the amended criterion; the retired enablement wording was replaced at its owners with the profile that selects each service | [POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md) |
| 1 | W13 | PASS: supporting evidence under the amended criterion; the duplicate `oauth2-proxy` profile and the two-leaf residue were corrected and the `_workspace` tracking check was registered | [POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md) |
| 1 | W17 | PASS: supporting evidence under the amended criterion; the enumeration row's comparison input was shown retired, which W19 replaced with the POL-0078 tables | [this Task](tsk-0001-stale-fact-convergence.md) |
| 1 | W20 | PASS: `018d437b3` hardened the check against the cases round six found and `904c844c2` corrected the residue it named; `check-operations-catalog.py` reports PASS | [Operations catalog check](../../../../scripts/validation/check-operations-catalog.py) |
| 1 | W21 | PASS: round seven's OpenSearch and MinIO topology residue now names the `data-cluster` and `storage-cluster` profiles, and a non-ASCII digit count is reported rather than aborting the leaf; 51 tests OK | [Operations catalog check](../../../../scripts/validation/check-operations-catalog.py) |
| 2 | W4 | PASS: after review correction, `infra/README.md` and the repository root `README.md` both state the measured 41 files, 40 directories and 41 include entries; the root README had carried 48 / 17 and was missed by the first pass | [root README](../../../../README.md) |
| 2 | W2 | PASS: the counts W4 wrote were measured first from the tracked tree, with the commands recorded in the W2 entry | [infra README](../../../../infra/README.md) |
| 2 | W16 | PASS: re-measured at `82ebe9d22`, 41 include entries, 41 tracked Compose files and 40 service directories, and the root README snapshot rows outside the criterion corrected | [root README](../../../../README.md) |
| 3 | W4 | PASS: the system scope sentence counts only files that exist | [POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md) |
| 3 | W15 | PASS: round five removed a second SPEC-0171 deferral clause 97 lines below the first and corrected `24개` to the 28 profiles the tables define | [POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md) |
| 4 | W4 | PASS: the include comment describes the six former sibling files as merged and the package as completed | [root docker-compose.yml](../../../../docker-compose.yml) |
| 5 | W5 | PASS: ADR-0033 accepted with supersedes ADR-0031; ADR-0031 superseded with superseded_by ADR-0033 | [ADR-0033](../../../02.architecture/decisions/0033-full-spec-package-preservation.md) |
| 6 | W5 | PASS: blob 904677b0303d277bea44904af68ba86758a10425 to 5bc18f381d1505e108d6fb28a994c2801c58ad83; diff shows only status and superseded_by | preserved ADR-0031 |
| 7 | W5 | PASS: FR-0009, Constraints and Acceptance Criteria state the Spec/Plan/Task preservation unit; no transient-removal clause remains | [REQ-0026](../../../01.requirements/0026-document-retention-and-retirement.md) |
| 8 | W9 | PASS: the count is replaced by the routing statement the sibling index already uses, and the structure block names 0030- and 0034- | [Stage 02 index](../../../02.architecture/README.md) |
| 8 | W16 | PASS: the routing wording W9 adopted now also stands in `descriptions/README.md`, the third file of the class | [Stage 02 index](../../../02.architecture/README.md) |
| 9 | W6 | PASS: step 3 names both categories with the conditions bootstrap.md states, and names bootstrap.md as the owner of the order | [repository map](../../../../.agents/knowledge/repository-map.md) |
| 10 | W6 | PASS: the workflow contract half is unchanged since 9ede309a5 and the pre-commit half is dated to 9051977aa, each named separately | [verification surface map](../../../../.agents/knowledge/verification-surface-map.md) |
| 11 | W7 | PASS: `git rev-parse --verify` resolves neither the local nor the remote branch; both packages now state the three Git commands | [SPEC-0173 spec](../../../98.archive/completed/03.specs/0173-governance-qa-surface-convergence/spec.md) |
| 12 | W7 | PASS: contract 9 names the underscore-prefixed modules; `git ls-files tests/fixtures` returns zero paths and no acceptance criterion changed | [SPEC-0173 spec](../../../98.archive/completed/03.specs/0173-governance-qa-surface-convergence/spec.md) |
| 13 | W8 | PASS: all three members are `completed` under the archive path and at W8 `ls docs/03.specs/` showed only 0173, 0176 and README.md | [preserved SPEC-0175](../../../98.archive/completed/03.specs/0175-governance-knowledge-and-prompt-surface/spec.md) |
| 14 | W8 | PASS: the index row describes SPEC-0175 as preserved with its archive paths and lists SPEC-0176 as the package in flight | [Stage 03 index](../../README.md) |
| 14 | W1 | PASS: W1 added the Stage 03 index row that lists SPEC-0176 and advanced `identity_spaces.spec` to 176 | [Stage 03 index](../../README.md) |
| 15 | W9 | PASS: both rows state that the bodies are not preserved and name Git history as the recovery path | [Documentation index](../../../README.md) |
| 16 | W10 | PASS: the generated outputs this package touched are fresh by the generators that remain, and `provider_surface_renderer.py --check` reports PASS providers=2 drift=0; the AUD-0023 report, the LLM Wiki and the hook parity matrix this row first cited were retired with their generators on 2026-09-10 and are no longer outputs | [Provider renderer](../../../../scripts/operations/provider_surface_renderer.py) |
| 16 | W18 | PASS: seven fenced commands that named retired generators were corrected, and `check-document-links.py --mode commands` exits 0 | [Documentation protocol rule 16](../../../../.agents/governance/documentation-protocol.md) |
| 16 | W20 | PASS: on 2026-09-15 `provider_surface_renderer.py --check` printed `PASS providers=2 drift=0` with exit 0; no other registered generator remains for the outputs this package touched | [Provider renderer](../../../../scripts/operations/provider_surface_renderer.py) |
| 17 | W11 | PASS: `run-ci-gate.py --profile changed` GATE_EXIT=0 read from the gate process; 13 unittest suites OK, zero FAILED lines, zero violations across every check | [this Task](tsk-0001-stale-fact-convergence.md) |
| 17 | W20 | PASS: `run-ci-gate.py --profile full` exited GATE_EXIT=0 on the clean tree at `9c039bcf9`, every FAIL line an `AOE-CATALOG` negative marker. This is the full profile at W20's head, not the changed profile on the final path set, which the completing integration still runs | [this Task](tsk-0001-stale-fact-convergence.md) |
| 18 | W11 | PASS: round one, two reviewers over `git diff e37b2dbcd..3725e08c7`; eleven of twelve accepted findings were corrected and one was routed to another author | [Review Evidence](tsk-0001-stale-fact-convergence.md) |
| 18 | W12 | PASS: round two reviewed the corrections themselves; both blocking findings held on re-measurement and were corrected, and finding 3 is recorded at its measured scale | [Review Evidence](tsk-0001-stale-fact-convergence.md) |
| 18 | W15 | PASS: rounds three through five reviewed the W13 and W14 corrections, and every accepted finding was corrected in W14 and W15 | [Review Evidence](tsk-0001-stale-fact-convergence.md) |
| 18 | W20 | PASS: round six reviewed `e43380153` through `f60c097cc` and blocked with ten findings, and W20 corrected each one | [Review Evidence](tsk-0001-stale-fact-convergence.md) |
| 18 | W21 | PASS: round seven reviewed `018d437b3` through `9c039bcf9` and blocked with thirteen findings, and W21 corrected each accepted one; those corrections are not yet reviewed | [Review Evidence](tsk-0001-stale-fact-convergence.md) |

### Predicate Triage for criterion 1 (2026-09-07, local-executed)

The bilingual predicate carries twenty-four patterns across English and Korean
and is deliberately loose: a false positive costs one line of reading, a false
negative is recorded as a passing check. Over 618 tracked current documents,
excluding `docs/98.archive/**` as frozen and this package as self-describing, it
returns 26 matches and zero true violations.

| Matches | Kind | Disposition |
| --- | --- | --- |
| 23 | ADR closing boilerplate, `별도 실행 증거가 없는 런타임 상태는 주장하지 않는다` | False positive. `별도 실행` here means "separate execution evidence" for a runtime claim, not a separately executed Compose file |
| 1 | `docs/05.operations/catalog/04-data/0023-minio/policy.md:38` | False positive. The control forbids describing either topology as excluded; it is the prohibition, not the defect |
| 1 | `docs/90.references/research/0084-github-actions-platform/m0001-platform-mechanics.md:316` | False positive. `local only` names a GitHub Actions allowlist policy |
| 1 | `infra/README.md:69` | False positive by construction. The row asserts that no commented include entry exists |

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
| 7 | medium | The deleted `docker-compose.dev.yml` was removed from tables and trees but the surrounding prose still described one file as two leaves, in oauth2-proxy, observability, airflow and n8n, and in the oauth2-proxy catalog subject | Partially fixed at first, then completed. oauth2-proxy and the observability README were corrected; `airflow/README.md:17,87`, `n8n/README.md:88` and `POL-0044:41` were dispositioned Fixed while still carrying the defect, which the second review caught. All four are corrected now |
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

### Independent review of the corrections (2026-09-07, local-executed)

Required by this Task's own Deferred Item. One reviewer, not the author, over
the working tree at `edc5162fb` against the eighteen criteria. Disposition
`block`.

The reviewer opened by reporting that no shell was available to it, so it never
reproduced `git diff 3725e08c7..edc5162fb` and never re-ran a registered check.
It named criteria 5, 6, 13, 16 and 17 as resting on the contributor's records
rather than on anything it measured. That disclosure is what makes the rest of
its report usable.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | blocker | Criterion 1 still unmet. The replacement predicate missed the Korean `선택 include` and the English `local only`; seven current-authority assertions survived while the receipt recorded PASS a second time | Accepted. Re-measured: six catalog guides plus `minio/README.md:62`, each against a root `include:` line that is uncommented. All seven corrected; receipt row 1 rewritten to record both false PASSes |
| 2 | high | Review Evidence row 7 dispositions four surfaces "Fixed" while `airflow/README.md:17,87`, `n8n/README.md:88` and `POL-0044:41` still carry the two-leaf residue | Accepted. Re-measured: airflow and n8n each hold exactly one Compose file, and Pyroscope has one file with `obs` and `dev`. All four corrected; row 7 re-dispositioned |
| 3 | medium | The same two-leaf residue exists at roughly ten times the scope this package declared, outside its in-scope set | Accepted as advisory, not fixed. Measured at 86 statements in 48 current documents. Recorded as a Deferred Item at that measured scale rather than absorbed by widening scope a second time |
| 4 | low | The Spec still says "thirty-nine documents" while the corrected set is larger | Accepted. Measured: 74 documents changed under the three named roots. Both sentences corrected, and the growth is now recorded as evidence for the package's own thesis |
| 5 | low | `minio/README.md:18` gives `minio-create-buckets` the `nginx` profile its Compose file withholds, and line 61 omits `nginx` from `minio` | Accepted. Verified against `minio/docker-compose.yml:14-18,60-63`; both lines corrected |

On the scope widening it was asked to judge, the reviewer found it legitimate
rather than goalpost-moving, on the ground that every amendment added obligation
or replaced a false boundary claim, and none weakened a criterion. It separately
noted that the one weakening-shaped amendment, criterion 8, happened in
`3725e08c7`, outside the range it reviewed, and declined to judge it.

Finding 1 is the reason this round existed. Round one's reviewers judged
`3725e08c7`; the corrections that answered them went unreviewed, and this Task
recorded that gap as a Deferred Item. The gap contained a false PASS on the
package's first criterion.

### Independent review round six (2026-09-15, local-executed)

One reviewer, not the author, reviewed every commit from `e43380153` through
`f60c097cc` that touches this package. Disposition `block`. Unlike round two,
this reviewer had a shell. It measured the Compose facts, ran the operations
catalog check and its tests, exercised the new check with eleven probe inputs,
and ran two bilingual residue searches with blame. It read the W14-W19 prose
without re-measuring it.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | blocker | Retired include-model wording survives as a precondition ("root include 활성 상태에서"), as an adjective ("root optional context", "optional leaf") and as the root-active versus optional contrast, including in subjects the Spec names | Accepted. Corrected in `904c844c2`. Each sentence now names the profile that selects the service. Sentences saying `root include active` are true and were left |
| 2 | high | Criterion 1 was amended while Behavior Contract 1 still stated the universal negative | Accepted. Contract 1 amended in W20 in the terms criterion 1 uses |
| 3 | medium | Receipt rows 1, 14, 16 and 18 were stale, and several joined work units in one cell | Accepted. Rows 1, 3, 14, 16 and 18 rewritten with one work unit per row; row 16 restated against the generators that remain |
| 4 | medium | The Commit Ledger missed seven commits and kept a `pending` row | Accepted. Every commit through `c36bda522` added, and the `pending` row replaced by `41e83d25e` |
| 5 | medium | Authorization text, the Plan's thirty-nine, its baseline and its terminal-status sentence were stale, and the Plan stopped at W11 | Accepted. Spec and Task record the operator's extensions; the Plan says seventy-four, lists W12-W20 and states the three-step walk |
| 6 | medium | The review and lifecycle Deferred Items described states that had moved | Accepted. Both restated; the SPEC-0173 row removed after that package completed |
| 7 | medium | The check kept the first of two rows for one profile and never compared the second | Accepted. Reported as drift in `018d437b3`, with a test |
| 8 | low | `!reset` and `!override` tags and an empty Compose file aborted the whole leaf | Accepted. Read as valid input in `018d437b3`, with a test |
| 9 | low | Mapping-form and `./` include entries, names with `_`, non-integer count cells and services without profiles were misread or unchecked | Accepted and fixed in `018d437b3`, except `infra/**/compose.yaml`, which POL-0078's scope does not name |
| 10 | low | The k6 README still described a Locust engine, and several READMEs say `root include active` | Accepted for the k6 README, corrected in `904c844c2`. `root include active` is true and is kept |

On the question this round was asked, the reviewer found that the W14
claim-shape sweep moved the blind spot rather than generalising: it searched
for sentences denying an include, and the survivors asserted a precondition or
used an adjective instead. It judged the criterion 1 mechanics sound and the
amendment goalpost-shaped only while Behavior Contract 1 kept the old wording,
which finding 2 closes. The corrections this round produced are themselves
unreviewed, and the Deferred Items carry that.

### Independent review round seven (2026-09-15, local-executed)

One reviewer, not the author, reviewed the eight commits from `018d437b3`
through `9c039bcf9`. It read both code diffs, the Spec, the Plan and this Task's
W20 onward in full, sampled the large documentation commits, ran both test
modules and the operations catalog check, and compared every documented
`repo:tag` with the Compose pins. Disposition `block`.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | blocker | The criterion 2 / W4 result cell opened with a qualifier and failed the completion regex | Accepted. Rewritten as `PASS: after review correction, …` |
| 2 | blocker | W1, W2, W3, W13, W16, W17, W18 and W20 had no receipt row | Accepted. One row per unit added, each against the criterion its entry serves |
| 3 | high | Criterion 17 rested on the W11 gate run, which predates W12 to W20 | Accepted in part. A W20 row records the full profile at `9c039bcf9`; the changed-profile run on the final path set stays with the completing integration |
| 4 | high | The Spec, the Plan and a Ruling still said SPEC-0173 was untouched and not advanced | Accepted. Each now names W20's completion as a unit of its own |
| 5 | medium | The Spec's in-scope list omitted the surfaces W20 changed | Accepted. W20 and W21 surfaces added |
| 6 | medium | OpenSearch documents still called the three-node topology an optional variant | Accepted. The policy, guide, runbook and README now name the `data-cluster` profile, and REQ-0005-FR-0003 and the MinIO policy and README name their profile-selected topologies too |
| 7 | medium | `infra/04-data/relational/README.md` listed `postgres:18.4-alpine` for the init job, which Compose pins at 18.6 | Accepted and corrected. The 18.4 pins under `examples/operations/postgres-logical-upgrade/` and the rehearsal script are deliberate rehearsal targets and are kept |
| 8 | medium | The criterion 13 cell read as a current directory listing | Accepted. It is dated to W8 |
| 9 | medium | Criterion 18 had no row for round six or for this round | Accepted. Rows for W20 and W21 added |
| 10 | low | The ledger omitted `83d2e15f6` and `2a7470f82`, which edited this package | Accepted. Both added, with `9c039bcf9` |
| 11 | low | The Plan said W6 and W7 spend the transition budget | Accepted. W5 and W8 do |
| 12 | low | A non-ASCII digit passed `isdigit()` and aborted the leaf in `int()`; the row pattern would also read a future non-profile table | Accepted for the digit, with a test written first that failed on `ValueError`. The row pattern is kept: a stray row is reported as drift rather than passing silently, and Compose profile names may contain dots |
| 13 | low | Criterion 16 named no command or exit code for W20 | Accepted. The W20 row records the renderer run and its output |

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `80b42feaa` | W1 package definition |
| `51e203b71` | W2-W4 Compose enablement convergence |
| `f71449eff` | W5 and W9 preservation-owner promotion |
| `b5d4181d0` | W6 and W7 knowledge routing and Git-read position |
| `c98df20dd` | W8 and W9 SPEC-0175 preservation and archive evidence |
| `3725e08c7` | W10 and W11 entry-path closure and final verification |
| `edc5162fb` | Round-one review-finding corrections |
| `1aa7bf039` | W12 `_workspace` tracking contract restoration |
| `7e1a23d40` | W12 round-two corrections and the bilingual predicate, carrying the ADR-0034 discharge note because the commit that was to hold it alone failed on the flaky guard below |
| `028ed751d` | W13 `oauth2-proxy` duplicate profile |
| `8513b912d` | W13 `_workspace` tracking contract check |
| `ec041eff3` | W13 two-leaf convergence |
| `fe01cad20` | W13 Task record |
| `e43380153` | W14 round-three corrections |
| `11a838f35` | W14 Task record |
| `eed5fa2f0` | W15 directory-identity guard fix |
| `da964ba61` | W15 round-four corrections |
| `5f912285d` | W15 round-five corrections |
| `14554a768` | W16 Stage 02 sibling index wording |
| `8a6c951b7` | W16 root README snapshot numbers |
| `41e83d25e` | W15 Task record, the guard record, and the full PostgreSQL rehearsal evidence |
| `be696fe52` | W16 and W17 Task record |
| `0d1b0dee4` | W17 Deferred Item corrections |
| `83d2e15f6` | SPEC-0173 W34 commit that also unlinked this package's references to the preserved ADR-0031 body |
| `2a7470f82` | SPEC-0173 commit that also rewrote this package's AD-0014 scope line after AD-0002 superseded it |
| `d8214fc09` | W18 fenced command path check and the seven surfaces it found |
| `1bfa67525` | W18 commit grammar body constraint |
| `578e85850` | W19 Compose include and profile check |
| `4968c730d` | W19 skill-owned script links |
| `f60c097cc` | W19 criterion 1 amendment and Task record |
| `018d437b3` | W20 profile check cases the sixth review found |
| `904c844c2` | W20 operations image tags, implementation claims and include-state residue |
| `a0dc93610` | W20 documentation and research index routes to retired packages |
| `d337e057b` | W20 architecture facts |
| `14d9ff6dc` | W20 tech-stack registry and document tags after the merged image bumps |
| `658114fff` | W20 SPEC-0173 reconciliation at HEAD |
| `c36bda522` | W20 SPEC-0173 completion and the preserved-Task recovery fix |
| `9c039bcf9` | W20 round-six answers and the Spec approval |

## Rulings

- SPEC-0173 is not modified beyond the two stale sentences SPEC-0176 names,
  extended once on 2026-09-07 when the operator authorized single-instance
  runtime Docker operations and asked for the config-only run. The extension is
  recorded here rather than taken silently: SPEC-0173's `tsk-0006` gained the
  execution evidence, which is that Task's own business, and its version moved
  to 0.4.10. Nothing else in that package was touched until W20, which completed it under
  the operator's 2026-09-14 request.
- A guard that fires is treated as correct until proven otherwise; the change is
  adjusted rather than the guard weakened.
- Static configuration and local test results never establish native runtime
  discovery, provider entitlement, Hosted CI, or remote state.
- Unexecuted checks are recorded as NOT_RUN or BLOCKED with their missing input
  and are never promoted to a PASS.

### ADR-0034's discharged Follow-up, resolved on the rule's text (2026-09-07, local-executed)

An earlier round deferred this item on the ground that "editing an accepted body
to agree with a later state is what the retention policy forbids". Reading the
rule instead of paraphrasing it, `documentation-protocol.md:172` says "Do not
change an existing accepted decision **silently**", and it says so in a Release
Record context rather than as a general immutability rule. The prohibition is on
silence, not on change. The deferral rested on a remembered paraphrase that the
source does not carry.

The item is therefore resolved, in the narrowest form the rule allows. The
original instruction is preserved verbatim and a discharge note is appended
naming the evidence: SPEC-0175 is completed and preserved, and ADR-0034 has read
`accepted` since. Nothing in Context, Decision, or Consequences is touched, and
this Task carries the record, so the change is not silent. If the decision owner
prefers the note removed, the instruction it annotates is intact.

## Deferred Items

| Item | Blocking input or reason |
| --- | --- |
| Review of the round-seven corrections | Round seven blocked with thirteen findings and W21 corrects each accepted one. Criterion 18 requires an independent review of corrections before completion, so the completing integration owns that review |
| The changed profile on the final path set | Criterion 17 names the changed profile on the path set completion leaves. W20 recorded the full profile at its own head, and each later commit moves the path set, so the run belongs to the completing integration |
| This package's own lifecycle walk | One step remains after W21 takes the Spec and Plan to `active` and this Task to `in-progress`. The completing integration moves all three to `completed` and preserves them together |
| Whether `ADR-0007` and `ADR-0022` should carry notes at all | The notes record a realization change on decisions that remain in force, which the retention rule permits because it forbids silence rather than change. A decision owner may prefer the annotation removed or promoted into a superseding decision; the instructions they annotate are intact either way |

## Related Documents

- [Specification](../spec.md)
- [Implementation plan](../plan.md)
- [Stage 03 index](../../README.md)
