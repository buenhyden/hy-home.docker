---
title: "W04 Lifecycle 3.0.1 Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-16"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0074"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-16"
---

# W04 Lifecycle 3.0.1 Task

## Scope

### Objective and Parent

Own W135 and criterion 130 under the [Spec](../spec.md) and [Plan](../plan.md).
Apply the settled draft boundary to the current authority consumers and close
the outstanding lifecycle checks supported by this workspace.

### Inputs and Authority

The direct 2026-11-16 W04-LIFECYCLE 3.0.1 request authorizes local source,
document and test changes for this scope. D03 and D15 3.0.1 and decision
Q-DRAFT govern the design. Survey entries S03 through S07 inform Markdown,
role ownership, traceability and impact checks. The installed contracts
govern current behavior. Local HEAD was `60609d51a`, with a clean worktree.
Local and remote main resolved to `17bbde05a`. The only open PRs targeted
dependency updates. [TSK-0073](tsk-0073-w03-forms-3-0-1.md) proves the form
prerequisite locally and retains its separate acceptance decision.
Local checks use Python 3.12.3 and the installed MarkdownIt 4.2.0 grammar.

## Execution Log

### Work Performed

#### Design before implementation

Keep the accepted W04 state axes and typed relations. Keep draft authoring
and focused checks available. Preserve separate trusted authorization for
applicable scope and treat package records as observations. D-12 in
[TSK-0067](tsk-0067-w00-delta-gap-closure.md) identifies author markers in
prose that survive into an effective document. Existing form checks handle
template tokens, placeholder-only optional sections and registered table
cells. D03 requires a check for explicit author markers in effective
authored prose as well.

Use the metadata body validator at its existing registered authoring
boundary. Interpret visible Markdown author markers and keep examples,
literal tokens, ordinary future-work narration, generated documents and
copy sources outside the new check. Report the missing authored content
without treating the reader as an approval authenticator. A global draft
scan would block independent work and cannot establish authority. A new
approvals ledger or ambient provider gate would extend the trust boundary
beyond what a static repository reader can establish. Revert the source
change and its tests together to restore the previous validation behavior.

Check draft and review authoring, effective-state body failures, clean
examples and complete documents, existing execution and evidence boundaries,
typed relation closure and the active corpus. Audit the actual dispatch and
provider boundaries before selecting any additional change.

#### Fresh closure design

The package loader admits closed Task states under a Spec or Plan in review so
past results can survive a new revision. The committed-base checks must
distinguish those records from a new completion or acceptance. Check only
freshly completed Tasks and work units and new `accepted` or `not-required`
decisions in the current generation. Require an approved Spec and Plan for
that package's new closure. Use the authorized Task that owns independent work, including
draft preparation, to record its own result without promoting the draft.
Keep the historical records and their existing evidence readers. Test fresh
closure, retained earlier decisions and approval-backed closure.

#### Resume and reference impact design

The SessionStart dispatcher supplies a fresh-context reminder for compaction
but leaves the same Task reassessment implicit on resume. Extend the existing
reminder to compact, resume and unrecognized sources when carrying over work.
Re-read the active Task and trusted request, check
current authority and revision, and stop dependent work when the current source
does not support it. This is provider context guidance. The controller owns
the decision and existing native entitlements remain separate. Test both
provider-shaped response variants through the tracked hook with synthetic payloads.

The SDLC uses the existing Approval Boundaries owner for the latest trusted
request, exact scope, revision and current applicability. The worker envelope,
handoff view and Task template carry that binding. Review the affected action
when the request changes, expires or is withdrawn, and reuse still-applicable
authority without asking again. The policy version increases for the new
effective-document rejection. The delegation and handoff contracts increase
their major versions because an input complete under the old rules lacks the
current revision binding. No machine policy changes its trust source.

Move and delete preflight requires incoming references by type. Add a
categorized readback from the existing document graph and retain the current
normative impact and transitive closure. Evidence URLs pinned to a revision
do not become dependencies on the live tree. Validate the categorized query
and show the negative and corrected path closure when a document moves or
is deleted. Keep ambiguous prose relations with their existing reviewers.
These extensions can be reverted by reverting their individual source and
regression test changes.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0074 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0074 | ready | in-progress | #design-before-implementation |

#### Reused boundaries and read scope

Read D03 and D15 3.0.1, local survey entries S03 through S07, Docker
workspace observations E10 through E12, PR observations 1034 and 1035 and
the Docker workspace profile. Cross-checked REQ-0024, the governing Spec
Package, the two Architecture parent routes, Stage 99 lifecycle and
relation bindings, current policies and templates, the hook dispatcher,
document validators, and the tests of the affected consumers.

| Boundary | Disposition | Basis |
| --- | --- | --- |
| Document form prerequisite | KEEP_VERIFIED | TSK-0073 has local function and corpus evidence, with owner acceptance independently pending. |
| State axes, transitions, cancellation records and parent rank | KEEP_VERIFIED | TSK-0063 criterion 116, TSK-0068 criterion 124 and current negative fixtures. Source labels in cancellation evidence remain structural. |
| Typed forward relations and stable IDs | KEEP_VERIFIED | Registry, metadata and link tests keep single writers, derived ID routes, cardinality and reference integrity. The inbound readback adds a typed path inventory. |
| Outstanding work disposition | KEEP_VERIFIED | The accepted TSK-0070 decision keeps prior work with its owners. Retired SPEC-0251 and SPEC-0259 have no new consumer here. |
| Effective prose, fresh closure and resume binding | CHANGE | D-12 and the reproduced current-reader and handoff gaps are implemented in their existing owners. |
| Provider-native authorization and Hosted QA | NOT_RUN | The source boundary and hook response are inspected locally. Native delivery and trusted-origin enforcement need their own evidence. |

The D15 semantic pass here covers the affected lifecycle, source and consumer
claims. The remaining corpus-wide prose review belongs to W04-CONTENT.

#### Observed latency

On the same already-built graph of 876 current documents and 8,543 legacy
links, the previous impact lookup took 5.157 seconds. The lookup with the
complete typed inventory took 14.257 seconds, an additional 9.100 seconds.
This was one local sample with concurrent tests. The same sample measured
alignment at 70.505 seconds before and 62.778 seconds with the shared reader,
with zero findings on both runs. The elapsed alignment difference does not
establish a speedup. Supplemental CommonMark diagnostics identify the
containing block's first line.

### Blockers and Decisions

The accepted [earlier W04 Task](tsk-0063-w04-sdlc-promotion.md) retains its
original scope and evidence. This revision owns new results. A local
observation cannot establish hosted, provider-native or operational approval.
The [W02 Task](tsk-0070-w02-disposition-3-0-1.md#criterion-decisions)
records criterion 126 as accepted. Its earlier pending wording is historical.
Separate open dispositions still belong to the owners that Task identifies.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Preflight | 130 | W135 | workspace-intake | HEAD 60609d51a, local tracking ref and read-only GitHub main and open PR query | PASS | Clean worktree, matching main, no W04 candidate PR | required | - |
| Metadata baseline | 130 | W135 | metadata-regression | metadata.test_heading and metadata.test_lifecycle at 60609d51a | PASS | 144 tests in 57.730 seconds, exit 0 | required | - |
| Prose markers RED | 130 | W135 | effective-prose | Approved Spec fixtures before the implementation | FAIL | 3 markers survived approval, exit 1 | required | - |
| Visible markers RED | 130 | W135 | effective-prose | First parser candidate with split CommonMark markers and inline line break | FAIL | 3 escaped markers and 1 false positive, exit 1 | required | - |
| Fresh closure RED | 130 | W135 | draft-closure | AcceptanceDecisionTests and ParentAuthorityBranchTests before the new closure checks | FAIL | New accepted criterion, Task completion and item completion produced no authority finding, exit 1 | required | - |
| Withdrawal decision RED | 130 | W135 | draft-closure | First candidate on new and changed not-required decisions under draft parents | FAIL | 2 closure cases produced no authority finding, exit 1 | required | - |
| Focused authoring and closure GREEN | 130 | W135 | effective-prose | TemplateAndAuthoredResidueTests and both fresh closure tests on the corrected reader | PASS | 16 tests in 7.018 seconds, exit 0 | required | Prose markers RED, Visible markers RED |
| Fresh closure GREEN | 130 | W135 | draft-closure | AcceptanceDecisionTests and ParentAuthorityBranchTests after both disposition states were covered | PASS | 16 tests in 37.684 seconds, exit 0 | required | Fresh closure RED, Withdrawal decision RED |
| Resume RED | 130 | W135 | session-start | HookOutputAndMainPushTests.test_session_start_context_reaches_the_model before the dispatcher change | FAIL | 4 missing reminders among synthetic provider/event combinations, exit 1 | required | - |
| Unknown source RED | 130 | W135 | session-start | Compact and resume candidate with unrecognized and non-string sources | FAIL | 4 missing reminders, exit 1 | required | - |
| Resume GREEN | 130 | W135 | session-start | HookOutputAndMainPushTests and test_folder_guides on the corrected hook | PASS | 31 tests in 15.849 seconds, exit 0 | required | Resume RED, Unknown source RED |
| Inbound RED | 130 | W135 | typed-inbound | Mixed-link and rename fixture before the categorized query | FAIL | Missing inbound query on 2 tests, exit 1 | required | - |
| Wrapped links RED | 130 | W135 | typed-inbound | Wrapped inline and shortcut reference fixtures before the CommonMark supplement | FAIL | Missing categories for both forms, exit 1 | required | - |
| Path closure RED | 130 | W135 | typed-inbound | Wrapped and shortcut links on the initial readback-only candidate | FAIL | Rename and deletion left stale links without an alignment finding, exit 1 | required | - |
| Typed references GREEN | 130 | W135 | typed-inbound | Mixed inventory, wrapped and shortcut rename, and deletion fixtures on the shared reader | PASS | 3 tests in 6.109 seconds, exit 0 | required | Inbound RED, Wrapped links RED, Path closure RED |
| Link integration fixture | 130 | W135 | link-regression | RelationLookupTests, DocumentGraphTests, DeclaredHistoricalLinkTests and RetiredPackageLinkTests on the first shared reader fixture | FAIL | 1 of 65 failed because frozen graph metadata was used as raw frontmatter, exit 1 | required | - |
| Link integration GREEN | 130 | W135 | link-regression | The same four classes with the deletion fixture reading saved frontmatter | PASS | 65 tests in 134.020 seconds, exit 0 | required | Link integration fixture |
| Lifecycle regression | 130 | W135 | metadata-regression | Heading, metadata lifecycle, generation 6 parents, current authority, acceptance and allowed cancellation-source tests on the integrated candidate | PASS | 168 tests in 101.124 seconds, exit 0 | required | - |
| Registry and template | 130 | W135 | registry-template | test_registry and test_template_definition with the Task authority prompt | PASS | 197 tests in 164.724 seconds, exit 0 | required | - |
| Active metadata | 130 | W135 | document-metadata | check-document-metadata.py --mode check-active on the integrated authority and authoring candidate | PASS | 569 selected, 0 violations in 61.09 seconds, exit 0 | required | - |
| Governance and renderer | 130 | W135 | governance | check-script-manifest.py, provider_surface_renderer.py --check, check-agent-governance-contract.py on the integrated candidate | PASS | Manifest valid, 0 renderer drift, 0 governance failures, exit 0 | required | - |
| Changed metadata | 130 | W135 | document-metadata | check-document-metadata.py --mode check-changed --base-ref 60609d51a | PASS | 7 selected, 0 violations, exit 0 | required | - |
| Corpus lifecycle | 130 | W135 | lifecycle | check-document-corpus-lifecycle.py --base-ref 60609d51a after the closure correction | PASS | 0 lifecycle and occupancy violations in 142.55 seconds, exit 0 | required | - |
| Corpus alignment | 130 | W135 | links | check-document-links.py --mode alignment after the shared CommonMark correction | PASS | 876 documents, 0 failures or warnings, exit 0 | required | - |
| Corpus command paths | 130 | W135 | links | check-document-links.py --mode commands with the current Task | PASS | 876 documents, 0 failures or warnings, exit 0 | required | - |
| Candidate preflight | 130 | W135 | candidate-preflight | check-candidate-preflight.sh on the local branch with 17bbde05a as its main merge base | PASS | 11 documents, 0 violations and synchronized tech-stack registry, exit 0 | required | - |
| Staged style and secret check | 130 | W135 | local-precommit | run-ci-precommit.sh --mode local-staged on the reviewed candidate | PASS | Applicable checks passed, exit 0 | required | - |
| Independent review | 130 | W135 | independent-review | Applied prose, closure, hook, reference and protected policy slices against 60609d51a | PASS | Reviewers rechecked their own correction ranges and found no remaining material issue | required | - |

### Resolution Links

GREEN rows resolve the named earlier observations using the same fixture cases.
Policy and provider-native evidence are separate from these local runs.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 130 | pending | - | Owner decision after verification is available | @buenhyden |

### Remaining Conditions

Hosted candidate validation, live provider delivery, trusted-origin runtime
authorization, operational changes and criterion acceptance each require
their own evidence. No external action was performed to obtain them.

## Handoff

### Promotion Receipt

The current request is recorded in the Spec and Plan. The registered metadata
validator and package lifecycle checker carry the structural boundaries. The
SDLC and agentic policy, handoff and Task template carry authority semantics.
SessionStart supplies the context reminder, and the link query and alignment
check share the categorized local relationship reader. The evidence rows show
which consumers were exercised. No runtime depends on the intake package.

### Next Owner

The implementer owns local checks for W135. The owner decides criterion 130.
