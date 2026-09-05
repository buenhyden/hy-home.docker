---
title: "Generated Evidence and Final Verification Task"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0006"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Generated Evidence and Final Verification Task

## Objective

Regenerate only affected derived artifacts, prove the converged surface with
focused checks and one final canonical full gate, and obtain independent review
without expanding into remote delivery.

## Inputs

- [SPEC-0173](../spec.md), its [implementation plan](../plan.md), and the
  completed local changes from Tasks 0001 through 0005.
- Canonical generators, generated-freshness checks, public validation profiles,
  script manifest validation, document validators, and Git diff checks.
- The final invocation-identity inventory and deletion consumer searches.

## Work Log

Task 5's implementation milestone passed independent code, Python, and policy
review; its corrections are committed as `0b237043`, `0fbbb962`, and `3fbb62aa`.
The user authorized proceeding with final verification and cleaning the feature
branch/worktree after local integration. No remote mutation is authorized.

The Task 5 read-only preflight identified two stale outputs: DATA-0059's
generator emits an obsolete metadata envelope, and DATA-0078 has old inventory
counts. DATA-0065 must preserve the corrected source audits' historical
designation in derived tables. Correct these reproduced generator defects at
their existing source owners with RED/GREEN tests before regeneration; never
hand-edit generated output or weaken validators. No Task 6 write or aggregate
had run at the ready checkpoint `f99508d4`. Execution starts from that commit.
The user committed the separate main WIP as `facfeec5` and root verified main
clean. This Task did not stage, stash, reset, or otherwise change that WIP.
Main and this feature diverge from baseline `71da6654`; their authority conflict
is not resolved by merely having a clean working tree.

### Renewed bounded correction checkpoint

On 2026-09-05 the user explicitly approved one additional correction and
independent re-review of the reported operation, gate/manifest, Stop/provider,
and current-path/generator findings, plus consistency review of the new main.
The independent rules-engineer approved that exact scope before production
edits. Implementation remains isolated in the existing feature worktree.

The PostgreSQL correction and provider absence enforcement passed independent
Python review and are committed separately. The manifest/discovery correction
also passed review and remains in the task-owned patch. Stop and remaining
README guidance did not pass re-review; do not treat their focused GREEN tests
as completion or silently take another correction attempt.

Root verified `.agents/agents` was untracked and empty, then removed only that
directory with `rmdir`. No files or user content were deleted; the prior role
projections remain recoverable in Git history. No recursive or force removal
was used.

### Approved integration and renewed correction checkpoint

The user fixed integration at `c02fa282db30fa4576fa04bcd328a47fe7da8511`,
requested completion of the existing package without new Spec/Plan/Task or IDs,
and approved local main merge and safe branch/worktree cleanup after verification.
The latest approval explicitly names existing document-disposition policy
adjustment and the two remaining Stop/README corrections with independent review.
Earlier failed attempts remain recorded below; this is a new bounded approval,
not retrospective acceptance.

The rules-engineer cleared the generic divergent-branch handoff design:
preserve the entire committed source packet byte-for-byte, retain its original
metadata, retain the same-ID immutable completed record, bind the exact source
and distinct active target through a typed Task receipt, and reject ordinary
nonterminal archive shortcuts. This is design clearance only; implementation,
negative tests, receipt verification and final independent review are pending.
No per-ID/commit allowlist, frozen-body edit, or new artifact is authorized.

Main is clean at the fixed baseline; implementation continues in the existing
feature worktree at `5547e07a2` plus the preserved task-owned patch. The requested
provider target permits only an absent/empty real `.agents/` root and keeps main's
direct Stage 00 skill loading. No shared projections or global settings return.

### Generator ownership and ordering

The manifest declares seven data/index generators; the provider renderer owns
native projections separately. Every command below ran in the isolated feature
worktree, with no runtime or external provider access.

| Owner command | Write disposition | Check result |
| --- | --- | --- |
| `python3 scripts/operations/provider_surface_renderer.py` | Task 5 already generated the changed Registry projection; no later input/output drift | `--check`: exit 0, two providers, drift 0 |
| `bash scripts/operations/generate-compose-profile-service-coverage.sh` | Correct source envelope; `--write` reproduced the existing output byte for byte, 138 services/28 profiles | `--check`: exit 0 |
| `bash scripts/operations/generate-tech-stack-version-provenance.sh` | Skip write: version inputs and output are unchanged by Tasks 4/5 | `--check`: exit 0 |
| `bash scripts/validation/generate-audit-implementation-matrix.sh` | `--write`: preserve historical designation in the complete criterion, normalized/raw status, and candidate-closure tables | `--check`: exit 0 |
| `bash scripts/validation/generate-security-automation-readiness.sh` | `--write`: refresh input-derived script/reachable-gate counts only | `--check`: exit 0 |
| `bash scripts/security/generate-supply-chain-sample-service-summary.sh` | Skip write: its moved example consumers were already cut over; source evidence and output unchanged since their accepted regeneration | `--check`: exit 0 |
| `bash scripts/validation/report-provider-hook-parity.sh` | Skip write: Task 5 parity check proved the output fresh; no subsequent hook/Registry input changed | `--check`: exit 0 |
| `python3 scripts/knowledge/generate-llm-wiki.py` | Task 5 already regenerated changed tracked paths; no later indexed path was added, removed, or renamed | `--check`: exit 0 for both outputs |

### Measured surface comparison

This is dated evidence for baseline `71da6654` versus the Task 6 branch, not
permanent numeric policy. Inventory uses `git ls-tree` and the manifest at each
revision; invocation counts use the current runner's canonical identity.

| Surface | Before | After |
| --- | ---: | ---: |
| Manifest file records | 89 | 78 |
| Manifest validator records | 30 | 21 |
| Manifest transition records | 18 | 0 |
| Purpose-folder `.py`/`.sh` paths, excluding `scripts/lib/` | 46 | 39 |
| Static `tests/fixtures` files / orphan files | 34 / not separately measured | 0 / 0 |
| Reusable `examples/operations` inputs | 0 | 23 |
| Current Spec packages | 1 (SPEC-0172) | 1 (SPEC-0173) |

The reviewed wrapper candidates retain `run-ci-gate.py` and
`check-github-workflow-contract.py` as current interfaces. Seven obsolete
compatibility/wrapper candidates were removed: the two document-link wrappers,
two target-surface CLI wrappers, local QA dispatcher, harness compatibility
dispatcher, and provider sync wrapper. This is a named candidate comparison,
not a byte-size definition of every public interface.

| Public profile/context | Baseline invocations / identities | Current invocations / identities |
| --- | --- | --- |
| changed/local | Not separately recorded | 18 / 18 |
| changed/pull-request | 31 / 30 | 30 / 30 |
| full/local | 50 / 49 | 43 / 43 |
| full/push | 63 / 61 | 55 / 55 |
| full/workflow-dispatch | 62 / 60 | 54 / 54 |

Library test module ownership remains agent-governance (1), document-governance
(18 top-level modules plus focused subpackages), gate (3), and surface ownership
(1); supply-chain grows from 1 to 2 while CLI/context modules grow from 26 to
30. The former ops module moves to validation and the two obsolete target-
surface modules are removed. Helpers remain outside `test_*.py` discovery.

Residue scans found no production `tests/fixtures/` reference, shorthand
frontmatter Requirement artifact ID, or artifact-number basename prefix
violation. The lexical `adr-writing.md` skill name is not an ADR artifact path.
The initial narrow scans found legacy paths in rejection/recovery tests, migration documentation,
explicitly superseded RES-0002 paragraphs, historical-marked audits/derived
tables, and DATA-0067's exact `e00e1483` foundation migration evidence. These are
not current operation routes. A broader independent review subsequently found
deleted paths in REQ-0025, ADR-0028, and AD-0028; their focused correction now
passes re-review. Bare generator examples in the scripts README remain open.
Stable identity/recovery checks remain enforced; no frozen archive body was edited.

## Verification Evidence

Final execution evidence is pending. Final acceptance requires all
focused checks in the Plan, `git diff --check`, and exactly one successful
`python3 scripts/validation/run-ci-gate.py --profile full` on the final local
tree.

| Check | Observed result |
| --- | --- |
| Manifest | `python3 scripts/validation/check-script-manifest.py`: exit 0 |
| Generator regression RED | Named Compose-envelope and historical-table tests: exit 1, 2 intended failures; stale diagnostic test: exit 1, 1 intended failure |
| Initial generator focused GREEN | Named tests passed 2/2 and 1/1; combined manifest/audit-criterion suites passed 57 tests in 13.898 seconds; review subsequently rejected the date-pinning test, so this is not final acceptance |
| Metadata focused discovery | `PYTHONPATH=. python3 -m unittest discover -s tests/lib/document_governance/metadata -p 'test_*.py'`: exit 0, 65 tests in 76.586 seconds |
| Lifecycle focused discovery | `PYTHONPATH=. python3 -m unittest discover -s tests/validation/lifecycle -p 'test_*.py'`: exit 0, 15 tests in 27.526 seconds |
| Gate library discovery | `PYTHONPATH=. python3 -m unittest discover -s tests/lib/gate -p 'test_*.py'`: exit 0, 78 tests with 11 pre-existing Wave-C skips |
| Gate CLI/context discovery | `PYTHONPATH=. python3 -m unittest discover -s tests/validation -p 'test_ci_gate*.py'`: exit 0, 32 tests in 3.645 seconds, including canonical invocation uniqueness |
| Provider renderer suite | `PYTHONPATH=. python3 -m unittest tests.validation.test_provider_surface_renderer -v`: exit 0, 28 tests in 6.025 seconds |
| Link contract | `python3 scripts/validation/check-document-links.py --mode all`: exit 0, 693 documents/5,744 links/0 failures |
| Corpus and recovery | `python3 scripts/validation/check-document-corpus-lifecycle.py`: exit 0, 0 violations; 3 migrations, 108 tombstones, 145 preserved bodies, 254 decisions, 342 recovery rows |
| First candidate gate admission | `python3 scripts/validation/run-ci-gate.py --profile full`: exit 1, `ci-gate-entrypoint-identity` for the edited uncommitted audit generator, before any leaf executed. Commit the reviewed owner patch before retrying; never bypass descriptor admission |
| Admitted candidate full gate | After `062cb611` and `f5d3702b`, full profile exited 60 at `leaf.postgres-logical-upgrade-config`: held-descriptor root resolved to `/proc`, producing `unsafe-canonical-parent` and cleanup failure. This is not a full pass |
| PostgreSQL descriptor regression | Original source in an isolated fixture reproduced exit 60; corrected actual `execute_execution_plan` check-only invocation returned 0, `status=check-passed`, and `cleanup_status=passed`. Operation suite: 53 tests passed; bash syntax, shellcheck, compilation and scoped diff passed |
| Full-profile reachability | Named reachability test failed for `tests.lib.document_governance.lifecycle.test_promoted`; registering it once and adding the package initializer made reachability and five-context uniqueness pass |
| Transition contract | Named regression first failed because transition+retain passed; corrected checker rejects retain, missing/blank/non-string removal conditions, and invalid successors. Combined transition/reachability/uniqueness: 3 tests passed in 0.061 seconds; manifest validation passed; manifest validation class: 25 tests passed in 7.491 seconds |
| Generator guidance | Both owner `--dry-run` outputs failed the explicit-write regression before correction; named regression and DATA-0059/0061 check modes now pass. The separate scripts README guidance is not fully corrected |
| Stop oversized/malformed status | Two named tests initially had 4 provider subtest failures; FD transport and parser guard made those tests and 18 routing tests pass. Independent review still found downstream environment-size exposure; this is not accepted completion |
| Retired projection absence | Two tests initially produced 6 failing subcases. Shared helper and check/write callers made 54 library/CLI tests pass in 14.828 seconds; renderer and governance providers checks passed. Unowned bytes and existing projection drift remain unchanged on rejected write |
| Audit evidence refresh | After source audit corrections, `bash scripts/validation/generate-audit-implementation-matrix.sh --write` and `--check` both exited 0 |
| Additional static diagnostic | Direct Ruff on the existing wildcard-import manifest test reported F403/F405 (69 at committed baseline, initially 70 in the patch). Explicitly importing the new regression's ROOT dependency leaves 50 existing wildcard-import diagnostics; this whole-file check is not green. The two new manifest/generator tests passed again in 0.382 seconds. Scoped production-checker, PostgreSQL and provider Ruff reviews passed |
| Generator static checks | Both `bash -n` commands, test compilation, and diff check passed; `shfmt -d` returned 1 on pre-existing generator formatting outside the changed hunks, which was not reformatted |

## Review Evidence

Read-only `task5_policy_review` accepted the ready transition and bounded
generator correction scope: PASS, quality A, 0 Critical, 0 Important, 0 Minor.
The final reviewer must receive the
exact commit and verification evidence and must be independent of the
implementation work.

Initial generator code and Python reviews each returned 0 Critical, 1 Important,
0 Minor: the new full-envelope equality pinned mutable publication dates and
version. The single narrower retry changes only that regression to validate
the envelope and value grammar while allowing valid future publication values.
That narrow generator re-review passed. The subsequent whole-branch review
reported seven Important code findings and two Important policy findings, with
no Critical findings. The renewed correction has these dispositions:

| Finding | Independent disposition |
| --- | --- |
| PostgreSQL held-descriptor execution | PASS; actual runner regression closes the earlier test-depth finding |
| Missing promoted test / invalid manifest transition | PASS; single registration and explicit removal condition contract |
| Retired provider output reintroduction | PASS; one library owner, two consumers, physical-path rejection without deletion |
| Current REQ/ADR/AD deleted paths | PASS |
| DATA-0059/0061 source and output write guidance | PASS for those source/output pairs |
| Quality policy and six source audit corrections | PASS/A; 0 Critical, 0 Important, 0 Minor for the seven-document slice |
| Stop diagnostic transport | OPEN Important: selected paths are limited to 80 lines, not bytes, then exported in `GATE_OUTPUT`/`STOP_REASON`; long legal paths can exceed the environment limit |
| Scripts README generator guidance | OPEN Important: maintenance entries for audit matrix, security readiness and supply-chain summary, plus the first audit generate/check example, still omit `--write` |

Code re-review is correction-required (0 Critical, 2 Important, 0 Minor).
The rules-engineer requires renewed direction after this frozen correction's
failed re-review. No final full aggregate is run on a knowingly rejected tree.

### Main integration decision and execution status

Read-only review identified 17 overlapping authority paths between main
`facfeec5` and the feature: three SPEC-0172 modify/delete conflicts, seven
content conflicts, and seven textual auto-merges requiring semantic review.
Main's SPEC-0172 v0.2 follow-up meaning differs from the feature's already-frozen
completed SPEC-0172. Restoring the same current ID duplicates authority;
discarding main loses user evidence; rewriting the archive breaks preservation.
The later user approval selects existing SPEC-0173 as integration owner without
allocating another package. Its generic branch-handoff receipt and exact
full-source preservation replace the earlier unresolved disposition proposal;
implementation and final verification remain pending.

Main also exempts three legacy migrations from linting in configuration while
its archive README still says migrations remain linted. Reconcile that current
prose with the exact Registry exceptions as part of the approved integration,
not by editing frozen migration bodies. No merge or main mutation occurred.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `f99508d4` | Accept Task 5 corrections and prepare Task 6 after authority review |
| `f2ce74ff` | Begin Task 6 through a separate ready-to-in-progress commit |
| `062cb611` | Reviewed generator envelope and dated-evidence correction |
| `f5d3702b` | Refresh security-readiness generated inventory |
| `f8ce954cc` | Descriptor-aware PostgreSQL root and actual runner regression |
| `5547e07a2` | Shared retired-provider absence enforcement and safe CLI regression |
| `3059a277c` | Byte-bounded Stop diagnostics and descriptor transport; independent specification/quality PASS, 18 routing tests passed in 21.122 seconds |
| `4eee3e58f` | Register promoted lifecycle behavior exactly once and restore discovery |
| `4aa319a40` | Reviewed manifest transition guards and explicit generator write guidance with regression coverage |

The renewed Stop and README re-reviews each returned PASS with 0 Critical,
0 Important and 0 Minor findings. The README regression reproduced four missing
write flags, then passed with the generator guidance regression (2 tests).
These close the two previously open findings, not final integrated acceptance.
The latest instruction allows conflict resolution on local main after merge,
requests push-ready state without an actual push, and minimizes checks: reuse
unchanged focused evidence and execute the final mandatory gate once on final
content. Cleanup remains conditional on complete preservation and verification.

## Rulings

- Generated output changes are accepted only when their canonical source set
  changed and write/check modes agree.
- A local full-gate pass proves repository enforcement only; it does not prove
  Hosted CI, runtime, deployment, entitlement, or remote protection state.
- The completion full gate runs after durable evidence and evidence-derived
  outputs are final; no content edit follows that verification.
- Final lifecycle completion happens only after review findings are resolved
  and durable evidence is written to the canonical owner.
- Graphify CLI is available, but its update is deliberately skipped: its
  unregistered output writes are outside Task 6, and AST-only refresh cannot
  refresh July semantic evidence. Independent policy review accepted this
  reported scope boundary (PASS/A, zero findings). Existing graph data remains
  stale/advisory, not authority or acceptance evidence. No graph update, LLM,
  network, or global-settings operation occurred.

## Deferred Items

- Push, pull request, Hosted CI, branch protection, deployment, tag, and release
  remain outside scope. The user's later cleanup instruction authorizes local
  integration and branch/worktree removal only after verification and safe
  reconciliation with their separately committed main WIP.
- Runtime and remote observations remain explicitly unverified.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Document and provider residue Task](tsk-0005-document-and-provider-residue.md)
- [Stage 03 index](../../README.md)
