---
title: "Governance and QA Surface Convergence Implementation Plan"
version: "0.5.1"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0173-PLAN-0001"
parent_ids:
- "SPEC-0173"
created: "2026-09-05"
---

# Governance and QA Surface Convergence Implementation Plan

## Objective

Reconcile the active package with the implementation now integrated on local
main at `8176cdee732954415bc5462d6d4d43da4e319394`, then collect the remaining
acceptance evidence without weakening its input, runtime, or authorization
boundaries. The canonical `.agents/` relocation, clean-worktree ownership and
Wiki repair, recorded evidence, and bounded Python cleanup are the implemented
baseline. They are not prospective migration work.

Tasks 0001 through 0005 retain their implementation milestones while their
frontmatter remains nonterminal with the active package. Task 0006 is the sole
execution and verification ledger. This Plan remains active until the package's
whole acceptance contract can receive an atomic lifecycle disposition.

The current authorization covers the integrated `8176cdee7` checkpoint, local
documentation follow-up and review on the same
`codex/0173-agent-governance-home` branch, and local commits. It does not imply
integration of later unreviewed work. Push, pull request, deployment, secrets,
global runtime settings, installation, Hosted CI and remote-state mutation
remain outside scope.

## Dependencies

- Original relocation provenance: local main
  `e5685b42c92039618ae86cca8736b6a425630221`. This commit remains the comparison
  origin for the reviewed migration; it is not the current execution baseline.
- Current review baseline: local main and the work branch both at
  `8176cdee732954415bc5462d6d4d43da4e319394`.
- Integrated implementation checkpoints: `6c283d395` for the atomic canonical
  relocation, `c265bacc5` for reproducible ownership and tracked-input Wiki
  repair, `a8c6ede82` for isolated follow-up evidence, and `8176cdee7` for the
  affected Python lint cleanup.
- Durable owners: REQ-0024 and REQ-0026; AD-0027 and AD-0030; ADR-0031 and
  accepted ADR-0032. Superseded ADR-0029 remains preserved evidence and is not a
  current decision owner.
- REQ-0026, AD-0030, and accepted ADR-0031 retain pre-existing transient
  Plan/Task deletion language that conflicts with canonical full-package
  preservation and executable package guards. Their alignment is an open
  promotion dependency, not evidence that this package is ready to complete.
- Existing scripts remain executable owners. Stage 99 owns document shapes;
  the Provider Registry owns translation facts; Task 0006 owns actual command,
  review, blocker and disposition evidence.

### Current interface boundary

The public validation entrypoints remain exactly:

- `python3 scripts/validation/run-ci-gate.py --profile changed`
- `python3 scripts/validation/run-ci-gate.py --profile changed --explain`
- `python3 scripts/validation/run-ci-gate.py --profile full`

Provider projection remains a separate direct interface:

- `python3 scripts/operations/provider_surface_renderer.py --check`
- `python3 scripts/operations/provider_surface_renderer.py --write`

The controlled all-files route is
`scripts/validation/run-agent-precommit-all-files.sh`. It is not a substitute
for either public profile and remains NOT_RUN because its owned execution may
install hook environments and invoke container-bound linters.

Canonical skill shape, direct repository loading and static provider checks are
PASS in Task 0006. Normal native startup discovery is not observed. Skill calls
and live hook delivery remain NOT_RUN; static parity cannot promote either state.

## Execution Sequence

1. W1: Preserve the reviewed authority decision, provenance and branch-handoff
   contract while reconciling current package language.
2. W2: Preserve the implemented canonical/provider contracts and their static
   evidence without claiming native runtime discovery.
3. W3: Preserve the implemented document, gate and test ownership contracts and
   their acceptance mappings.
4. W4: Preserve the implemented bootstrap, hook, evaluation and CI routing while
   keeping live runtime observations separate.
5. W5: Preserve the completed source cutover, generated outputs and archive
   dispositions as the integrated baseline.
6. W6: Review the post-integration package, run safe document checks, and resume
   blocked acceptance only when its exact prerequisites are available.

### W1: Reviewed authority decision

Implemented baseline: the original source inventory and branch-handoff receipt
are recorded in Task 0006. ADR-0032 is the accepted canonical-home decision;
ADR-0029 is legally superseded and preserved. Current validators distinguish
current-path grammar from historical recovery.

Keep current Spec, Plan, Task and index prose consistent with `8176cdee7`. Do
not allocate another canonical-home ADR, repeat ADR-0032, repeat source
disposition, or reopen the handoff. The separate retention-owner promotion uses
this sequence:

1. Compare the conflicting REQ-0026, AD-0030, and ADR-0031 clauses with the
   canonical policy and executable full-package guards.
2. Produce and independently review one bounded successor design covering the
   required preservation invariant, owner updates, lifecycle transitions,
   alternatives, consumer effects, and recovery.
3. Only after that design is accepted, update REQ-0026 and AD-0030 and introduce
   the successor required to change ADR-0031. Preserve ADR-0031's accepted body
   and use the applicable reciprocal supersession lifecycle.
4. Record actual promotion, review, validation, and consumer evidence only in
   Task 0006.

No successor identity or substantive decision is selected before step 2.
Acceptance rows 11 and 12 retain the W1 mapping.

### W2: Canonical and provider contracts

Implemented baseline: strict bounded `.agents/` inventory, native skill
envelopes, explicit-invocation controls, provider source/output separation,
deterministic rendering and focused actual-root regression evidence are present.
Acceptance row 14 retains the W2 mapping.

Normal native startup remains a separate observation. Its required input is an
environment where the ordinary installed runtime can start and expose
repository-local discovery without unapproved authentication or global-state
effects. The decision is whether that input boundary becomes available within
an authorized follow-up. Resume only through ordinary startup and record the
observed discovery result in Task 0006. Do not use a bypass flag, direct file read,
static check or model call as replacement evidence.

### W3: Document and knowledge consumers

Implemented baseline: Stage 99 classification, hidden canonical discovery,
current and historical link boundaries, Wiki source scope, canonical invocation
identity, manifest ownership and the repaired library/CLI test split are present.
Acceptance rows 1 through 10 retain their W3 mapping.

For this reconciliation, preserve those contracts and update only current
package descriptions and navigation. No Registry, schema, generator, test,
workflow, model or permission behavior changes are planned. A changed-profile
selection describes the final unstaged, staged and untracked path set together
with required fallback validators; it does not prove an arbitrary committed
range.

### W4: Hooks, entrypoints and repository routing

Implemented baseline: canonical bootstrap routes, fail-closed policy loading,
provider event conversion, evaluation paths, manifest routing, CI selection and
active navigation have been cut over. Native hook setting files and event facts
remain unchanged.

Live hook delivery and enforcement remain NOT_RUN. No hook activation, trust
change, user-local configuration write or new runtime session is part of this
documentation reconciliation.

### W5: Protected cutover and generated outputs

Implemented baseline: the canonical move, native outputs, tracked-input Wiki
refresh, former-root removal, frozen-body preservation and four DATA
dispositions are committed and reviewed. Acceptance row 13 retains the W5
mapping.

Do not rerun migration, source allocation or protected cutover steps. A later
canonical source change must use the registered generator and receive its own
review; this reconciliation changes no generator input outside the active Spec
package and Stage 03 index.

### W6: Final evidence and review

W6 remains in progress. Review the reconciled package at the current local-main
baseline and record actual results in Task 0006 under
[Post-integration package review](tasks/tsk-0006-generated-evidence-and-final-verification.md#post-integration-package-review-2026-09-06)
and
[Package reconciliation verification](tasks/tsk-0006-generated-evidence-and-final-verification.md#package-reconciliation-verification-2026-09-06).
Acceptance rows 15 and 16 retain the W6 mapping.

Apply this order for the documentation follow-up:

1. Inspect the exact working-tree paths and diff, confirm that only the active
   package and required index are involved, and review their inbound links.
2. Run `git diff --check` on the scoped files.
3. Inspect
   `python3 scripts/validation/run-ci-gate.py --profile changed --explain` on the
   final path set. Trace every selected leaf and its inputs before execution.
4. Run the applicable formal document checks and the changed profile only when
   the inspected leaves can use the reviewed isolated input boundary. Record
   command, path set, input boundary, exit and state in Task 0006.
5. Obtain independent exact-diff package review and correct only findings within
   the current authorization. Root owns the resulting Task update and commits.

No native model, web, installed-version or runtime probe needs repetition for
this wording-only package reconciliation because no native contract changes.

The whole-migration aggregate remains BLOCKED by the actual PostgreSQL
operating/image leaf. Required input is the real image and operation input set
selected by that leaf under an execution boundary that permits using them. The
decision is whether those inputs and that execution scope are supplied for a
future run. Resume only after both are available, inspect the selected plan
again, and execute the exact aggregate without removing, replacing or hiding the
PostgreSQL leaf. Focused fixture and isolated Compose results do not satisfy it.

The all-files wrapper remains NOT_RUN while its installer and container-bound
inputs are unavailable or outside scope. Resume only if the completion policy
requires that route, its separately controlled execution is authorized, and
all inputs are reviewed. Hosted CI and remote protection remain unverified and
outside this local Plan; local results do not infer their state.

## Risk and Rollback

| Risk | Guard | Recovery |
| --- | --- | --- |
| Current prose reopens completed implementation | Treat `8176cdee7` as the implemented baseline and keep W1-W6 labels stable | Revert only the package-reconciliation documentation slice |
| Original provenance is mistaken for current HEAD | Name `e5685b42c` as migration origin and `8176cdee7` as review baseline | Correct the receipt against Git and Task 0006 before further evidence |
| Static evidence is promoted to native acceptance | Keep direct reads, shape checks, discovery, invocation and hook delivery separate | Restore the prior state label and require direct observation |
| Aggregate blocker is hidden by focused PASS results | Preserve the actual PostgreSQL leaf and acceptance row 15 as BLOCKED | Stop; restore the selected plan and record the unmet input |
| Changed selection is treated as committed-range proof | Bind it to the observed working-tree path set and fallback validators | Record the exact comparison separately or retain UNVERIFIED |
| Wrapper or remote work exceeds authorization | Keep all-files, Hosted CI and remote state explicitly conditional | Leave NOT_RUN or unverified and request the required input/scope later |

## Verification

Task 0006 records every actual command, cwd, selected inputs, exit code, scope,
review finding and PASS/FAIL/BLOCKED/NOT_RUN/N/A state. This Plan records order
and resume conditions only. It makes no new execution claim.

Package completion requires acceptance criterion 15 to be satisfied as written;
the current BLOCKED aggregate is not a waiver. Completion also requires the
open REQ-0026, AD-0030, and ADR-0031 owner promotion to follow its reviewed
design and lifecycle. Tasks 0001 through 0005 and the Spec/Plan stay nonterminal
until Task 0006 proves the whole package can transition atomically. The current
per-check blocker does not change Task 0006's `in-progress` lifecycle state
while it carries the active branch receipt. Preserve criterion 16's distinction
among local execution, configuration, repository enforcement, runtime,
entitlement and remote state.

## Rulings

- No new policy, configuration, model, permission, hook activation, Spec, Plan,
  Task or secondary status ledger is introduced by this reconciliation.
- The implemented migration and ADR-0032 remain stable. The retention-owner
  successor design is a separate promotion dependency and must preserve
  accepted ADR-0031 through its registered lifecycle.
- Frozen Tasks remain durable full-body evidence. Git history does not replace
  preservation, and no frozen body is edited to manufacture completion.
- Current authorization covers local follow-up on the existing branch and local
  commits; it does not authorize later unreviewed integration or remote work.

## Related Documents

- [Specification](spec.md)
- [Task 0006 evidence](tasks/tsk-0006-generated-evidence-and-final-verification.md)
- [Stage 03 index](../README.md)
