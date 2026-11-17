---
title: "W06 Delivery 3.0.0 Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0077"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-16"
---

# W06 Delivery 3.0.0 Task

## Scope

### Objective and Parent

Own W138 and criterion 133 under the [Spec](../spec.md) and [Plan](../plan.md).
Use the exact Git input for each delivery check and remove demonstrated
duplicate or unnecessary work.

### Inputs and Authority

The direct W06-DELIVERY 3.0.0 request, with D04, D05 and D17 3.0.1, authorizes
local implementation and isolated validation in this checkout. The clean
input was `2f53a4ef4`; the implementation branch is `codex/w06-delivery`.
Read-only remote main is `17bbde05a`, with open Renovate PRs 1047 and 1048.
[TSK-0076](tsk-0076-w05-gates-3-0-0.md) supplies the W05 implementation
evidence. No hosted execution or repository setting change is authorized.

## Execution Log

### Work Performed

#### Merged baseline candidate header follow-up

D04, D05 and D17 3.0.1 govern W138. At `2cfeeac734` routing already
reads only the commit header, but the core and document jobs also count
parent-shaped lines from the commit message. Apply the same header bound
to both consumers and preserve the exact parent count and comparison.
Exercise the captured workflow with a valid merge and ordinary prose.
Revert the two captures and their regression as one unit if needed.

#### Design before implementation

Keep the installed pre-commit, commit-msg and pre-push protections and
the stable candidate aggregate. Diagnose an unconfirmed staged-hook
delivery through the existing local-staged wrapper. Retain the current
independent hosted style guarantee. A base-side rename can give the
authenticated merge a path absent from the head-only selection.
Keep the cumulative base-to-head contribution and add the verified
base-to-merge result to hosted selection, preserving both sides of renames
and the changed-path budget. Bind style to that verified merge tree and
its first parent. Reject missing or inconsistent candidate identity.

Keep full ancestry for PR gates that read historical sources. Main
security scans the pushed tree and its tracked blobs, so a depth-one
checkout can serve its distinct lane. Keep the workflow guard and static
projection in sync. Validate topology and style with real disposable
Git fixtures, retain unauthorized-path and missing-result negatives, and
measure native hooks through Trace2. Revert the bounded tracked changes
to recover the previous routes.

#### Resume design

The direct W06 resume request rebinds local execution to the clean
`a6729e578` candidate. Its workflow projection, real merge-path regression
and isolated style contract passed again. The prior native commit and
unchanged push guard remain separate evidence.

Run the canonical changed-plan selector in a small routing job, using only
Git and system Python. Keep the core job independent so its long checks
cannot delay a document job that was selected. The routing job must admit
only the authenticated topology and expose a strict boolean. The document
job starts only on true and runs its existing selection and execution checks.
The stable aggregate rejects a missing or failed routing result, a skipped
selected job, and a successful job that contradicts a negative selection.
Reject a second path-pattern implementation and a route behind core.
Keep candidate-run evidence distinct from remotely adopted independent
enforcement. Reverting the workflow, planner and contract changes together
restores the prior two-shard schedule.

#### Implementation and observation

Read the package observations, decisions, workspace profiles and applicable
research entries S07, S10, S14–S22, S24 and S26 with D04, D05 and D17. Traced
the tracked runner, workflow projection, style controller, installed hook
chain, canonical Git and quality policies, and their script-facing guidance.
Keep verified native pre-commit, commit-msg and ref-only pre-push routes. Keep
the W05 stable aggregate, required receipts, and PR ancestry. The normal
commit guidance now runs the installed checks once. A standalone local
candidate preflight no longer duplicates its selected leaf.

Before the change, the real Git rename fixture selected only `old.md`.
It now selects `old.md` and the merged `renamed.md`. The style regression
also failed on a file created only in the merge tree, then passed when
the wrapper used the first parent and merge SHA. The style fixture uses
a fake pre-commit observer for PR arguments and an installed pre-commit
process for its local staged case.

The installed pre-push hook used five Trace2 samples per synthetic ref set.
Median wall and hook times were 12.39 and 9.40 ms for a feature ref, 12.68
and 9.65 ms for main, 13.40 and 10.06 ms for mixed refs, and 11.34 and 8.51 ms
for a main deletion. Only the feature-only case passed. No transport ran.

In five interleaved local checkout pairs on a synthetic 65-commit repository,
median full-history checkout took 0.3758 s and depth one took 0.0326 s.
The Git pack was 4,214,039 versus 634 bytes. The same HEAD, tracked adapter
blob and byte-identical offline SARIF were observed in both checkout modes.
The test used the production Git owner fixture to model a root-owned binary.
These data measure local checkout only. Existing hosted PR 43727005599
recorded approximately 2 s to the document job, 7 s for checkout, 1 s each
for uv and dependency installation, and 1,255 s for validation. Existing
main run 43729056797 completed in 37 s with only main security selected.
Hosted queue, setup, run and retry costs for W138 remain unmeasured.

#### Resume implementation and observation

Routing and execution use the same registered document gate plan. Routing
uses system Python without site packages and produces only `selected=true`
or `selected=false`. Core starts independently. When selected, the document
job recomputes its plan before running leaves and publishing evidence.
A distinct runner with full Git ancestry still supplies routing. It replaces
unused document setup on non-applicable inputs and adds a scheduling and
checkout dependency for selected inputs.

In seven local pairs per synthetic merge, the planner median was 0.3378 to
0.3268 s for a README change and 0.3365 to 0.3186 s for a document validator
change. The paired predecessor modeled its original YAML import. Neither
sample wrote execution evidence. Checkout, queue, setup and installation time
are outside the interval, so no hosted critical path is estimated.

#### Candidate model repair for PR 1049

The owner separately authorized delivery of this Spec Package. The first
hosted attempt at `3282d1e47` selected the document shard successfully
in run 43776564841. The core job failed because the public runner model
test's exact job inventory omitted the registered `candidate-routing`
job. The focused test reproduced the same assertion locally. Add the
routing job to the expected inventory. Keep the exact inventory check
and the existing checks for the executing shards and aggregate. The
workflow and its enforcement remain unchanged.

#### W06-DELIVERY 4.2.0 recheck

The 2026-11-18 W06-DELIVERY request read D04, D05 and D17 of the 4.2.0
package at `0e58e6608`. D04 adds the complete reuse key, the exact expected
required set and the stage-split bottleneck measurement, which
[TSK-0076](tsk-0076-w05-gates-3-0-0.md) verified for the gates. D05 adds
reviewer independence by execution context and evidence, owned by
W10-REVIEW and RUNTIME-CLOSE. D17 separates native preparation failures
from target denials, owned by W07-ADAPTER and RUNTIME-CLOSE. No attachment
disposition targets W06-DELIVERY. No external source was rechecked.

Since the reported completion at `ffc3247ce`, no workflow, hook installer,
push guard or delivery runner changed. PR 1076 changed only which hook
environments the changed style leaf installs, and
[TSK-0080](tsk-0080-w00-w07-follow-up.md) records its hosted comparison.

| W06 requirement | Disposition | Basis |
| --- | --- | --- |
| Installed hook chain and Trace2 | KEEP_VERIFIED | No `core.hooksPath` locally or globally; pre-commit and commit-msg come from pre-commit and pre-push is the native guard. Three normal commits of one staged guide edit took 2.57 s median wall, 1.62 s pre-commit and 0.87 s commit-msg |
| Commit, push, PR and merge each check their own input | KEEP_VERIFIED | Commit hooks read the exact index, the push guard reads ref records, PR selection keeps the base-to-head contribution plus the verified merge result including base-side renames, and main runs only its security lane |
| A required workflow cannot vanish through a filter | KEEP_VERIFIED | No workflow declares `paths` or `paths-ignore`; `candidate-quality` always reports, and protection requires it from App 15368 with strict status, administrator enforcement and resolved conversations; no ruleset applies |
| Non-applicable route without heavy setup | KEEP_VERIFIED, now hosted | Routing uses system Python and decides before any document runner starts; see the route table |
| No speed from skipping verification | KEEP_VERIFIED | No `--no-verify` route; the aggregate refuses a missing or failed routing result, a skipped selected job and a success that contradicts a negative selection |

The route table uses the 36 successful pull request runs of this workflow
since 2026-11-16 12:00 UTC, with job start and end times from the Actions API.

| Route | Runs | Routing median and range | Core median | Document shard median and range | Workflow median and range |
| --- | --- | --- | --- | --- | --- |
| Documents not selected | 17 | 12 s, 10–53 s | 243 s | not started | 252 s, 188–367 s |
| Documents selected | 19 | 12 s, 8–20 s | 280 s | 1,155 s, 758–1,378 s | 1,177 s, 790–1,414 s |

The inputs differ between routes, so the table shows where each route
spends time, not a paired speedup. When selected, the document shard is the
critical path. The pre-W06 and current implementations cannot run on hosted
runners with the same input, because every candidate merges the current
`main` and the pre-W06 code sits under later changes. No paired hosted
comparison is claimed.

Independent remote enforcement is still not adopted: it needs a base-owned
verifier that treats candidate objects as data, a separate check with a
verified App identity, and main protection naming both. Creating that App
and changing protection need the owner's separate authority, which this
request does not grant.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0077 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0077 | ready | in-progress | #design-before-implementation |

### Blockers and Decisions

Candidate Git histories are local or synthetic. Existing hosted runs may
be read as historical evidence. Publication, remote writes, full-stack
operation and changes to branch protection remain outside this request.
The Kubernetes-specific provision does not apply to this Docker checkout.
The unprivileged PR jobs execute candidate code. Routing and the aggregate
record candidate self-check evidence. Independent enforcement needs a
base-owned verifier that treats candidate objects as data and a separate
check with a verified App identity. Main protection must name that check
and App ID after separate approval and read-back. The trusted base definition
observed locally is `origin/main` at `17bbde05a`. The current Verifier App
mapping and permissions are unobserved. The existing `qa-control` environment
admits protected branches and has no custom main-only policy. Hosted proof
is needed for both selected and non-applicable routing paths.
Read-back on remote main confirmed an up-to-date required `candidate-quality`
check, resolved conversations and administrator enforcement. The rulesets
endpoint returned no applicable rules. This is a read-only observation.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Intake | 133 | W138 | workspace and delivery baseline | Clean 2f53a4ef4 and read-only remote state | PASS | Workflow projection and W05 evidence checks passed | required | - |
| Installed push guard | 133 | W138 | git hook run with Trace2 | Four synthetic ref sets, five samples each | PASS | Feature accepted; main, mixed and main deletion refused | required | - |
| Style controller | 133 | W138 | bash tests/validation/test_run_ci_precommit.sh | Real merge and staged fixture commits, PR observer and local pre-commit | PASS | Candidate SHA, one invocation, mutation and bad-parent negatives | required | - |
| Workflow projection | 133 | W138 | workflow contract and adapter unittest modules | Candidate workflow, depth-only checkout change and negatives | PASS | 102 tests; 5 workflows, 9 jobs and 9 actions | required | - |
| Checkout comparison | 133 | W138 | paired native local clone and offline SARIF | Five pairs with the same synthetic tip and scanner pin | PASS | Identical relevant bytes, depth-one timing recorded above | optional | - |
| Runner regressions | 133 | W138 | unittest runner, execution context and result evidence modules | Bound PR and merge candidates, evidence and missing-result negatives | PASS | 124 tests in 42.658 s | required | - |
| Scope and lint | 133 | W138 | changed plan, script manifest, surface ownership unittest, Ruff and ShellCheck | W138 executable and owner surfaces | PASS | Changed routing, 8 ownership tests, manifest and scoped lint | required | - |
| Canonical policy and projection | 133 | W138 | independent rules review, provider renderer and governance contract | Conditional fallback text, unchanged hook matchers and selected preflight leaf | PASS | Policy review passed, two providers with zero drift and no governance findings | required | - |
| Document structure and relationships | 133 | W138 | metadata, lifecycle and alignment and command links checks | W138 Spec, Plan and Task before final evidence additions | PASS | Three scoped metadata documents, zero lifecycle, occupancy and link violations | required | - |
| Remote protection read-back | 133 | W138 | read-only GitHub API branch protection and rules | Current main settings | PASS | Strict candidate-quality, resolved conversations, administrator enforcement, no applicable rulesets | optional | - |
| Independent code review | 133 | W138 | independent review of W138 against 2f53a4ef4 | Selection, style, checkout and candidate aggregate | PASS | No defect in the implemented changes | required | - |
| Independent scope review | 133 | W138 | independent review of W06 coverage | Hosted trust and early shard routing | FAIL | Independent trust and pre-setup non-applicability remain open | required | - |
| Installed commit hooks | 133 | W138 | normal git commit with Trace2 | Reviewed and staged W138 candidate | NOT_RUN | Pending final local delivery | required | - |
| Hosted continuation | 133 | W138 | actual PR and main Actions run | W138 revision | NOT_RUN | No hosted dispatch or transport in scope | required | - |
| Prior native commit observed | 133 | W138 | normal git commit with Trace2 | a6729e578 | PASS | Wall 3.28 s; pre-commit 2.593 s and commit-msg 0.648 s | required | Installed commit hooks |
| Resume baseline | 133 | W138 | workflow projection, merge-path unit and style wrapper | Clean a6729e578 | PASS | Exact Git candidate and style checks passed again | required | - |
| Resume planning and receipt regressions | 133 | W138 | focused runner, contract, workflow, evidence and context tests | W138 routing and aggregate changes on a6729e578 | PASS | 120 planner and contract tests, 88 workflow and evidence tests, 32 context and ownership tests | required | - |
| Resume hosted workflow structure | 133 | W138 | actionlint and workflow contract | W138 candidate job graph | PASS | Five workflows, ten jobs, nine actions | required | - |
| Resume routing timing | 133 | W138 | interleaved subprocess comparison | Seven synthetic merge pairs per outcome | PASS | Planner timings and excluded costs recorded above | optional | - |
| Resume protection read-back | 133 | W138 | read-only GitHub API | Current main and qa-control | PASS | candidate-quality App 15368, strict; environment lacks a custom branch policy | optional | - |
| Resume independent route review | 133 | W138 | implementation review against a6729e578 | Routing, aggregate, trust and performance | PASS | Local change approved; hosted comparison and independent trust remain open | required | - |
| Hosted public candidate model | 133 | W138 | public candidate job model test | PR 1049 at 3282d1e47, run 43776564841 | FAIL | candidate-core reproduced the omitted candidate-routing job in the exact inventory assertion | required | - |
| Corrected public candidate model | 133 | W138 | public candidate job model test | Corrected job inventory for PR 1049 | PASS | Local public model and ownership suites passed 16 tests, exit 0 | required | Hosted public candidate model |
| Hosted selected route and main security | 133 | W138 | actual PR and main Actions run | PR 1049 at 75e1c3079, run 43778700250; merged main at 2cfeeac734, run 43780546570 | PASS | Route 12 s, selected documents 805 s, core 952 s, required aggregate 5 s and main security 32 s | required | Hosted continuation |
| 4.2.0 hook chain | 133 | W138 | git config, hook header and normal git commit with Trace2 | Three commits of one staged guide edit on `0e58e6608` in a disposable worktree | PASS | No hooks path; median wall 2.57 s, pre-commit 1.62 s, commit-msg 0.87 s | required | - |
| 4.2.0 hosted routes | 133 | W138 | read-only Actions run and job metadata | 36 successful PR runs since 2026-11-16 12:00 UTC | PASS | 17 non-applicable and 19 selected document routes, medians in the route table | required | - |
| 4.2.0 protection read-back | 133 | W138 | read-only GitHub API | Current main protection and rules | PASS | candidate-quality from App 15368, strict, administrators enforced, conversations resolved, no ruleset | optional | - |
| 4.2.0 delivery regressions | 133 | W138 | unittest gate plan and workflow contract, style wrapper contract | PR 1076 candidate on 2026-11-18 | PASS | 135 tests including both rename paths and the base-side merge rename, wrapper contract passed | required | - |

### Resolution Links

Local evidence resolves the demonstrated rename, checkout and late document
selection defects. Hosted runs now show the non-applicable route deciding
before any document runner starts. The independent scope finding stays
unresolved because the independent verifier is not adopted and no
independent re-review of W06 coverage has run.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 133 | pending | - | Owner @buenhyden chose per-criterion acceptance on 2026-11-16 in this chat; held by unresolved required rows Independent scope review | @buenhyden |

### Remaining Conditions

Criterion 133 stays pending on the Independent scope review row. The
selected and non-applicable hosted routes are observed. A paired hosted
comparison of the pre-W06 and current implementations is not possible for
the reason above. Adopting independent remote enforcement needs the owner's
authority to create a verifier App and change main protection, followed by
an independent re-review. The separate `main-security` job passed on the
actual merge commit.

## Handoff

### Promotion Receipt

The existing delivery runner, style wrapper and workflow own the changes.

### Next Owner

The owner decides whether to authorize the independent verifier and
protection change, or how to decide criterion 133 without it.
