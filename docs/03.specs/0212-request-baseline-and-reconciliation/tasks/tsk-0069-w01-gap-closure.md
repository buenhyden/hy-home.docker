---
title: "W01 Gap Closure Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-15"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0069"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-15"
---

# W01 Gap Closure Task

## Scope

### Objective and Parent

#### Objective

Own W130/criterion 125. Audit the W01-CONTRACT record (TSK-0068) against
every step and acceptance test of the 3.0.1 W01 prompt, close what it left
open, and resolve the owner disagreement it created (D-13), with the
requirement taking priority.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [3.0.1 W01 contract](tsk-0068-w01-contract-3-0-1.md)

### Inputs and Authority

On 2026-11-15 the user asked to examine the W01 prompt for remaining,
unverified, unreviewed, unconfirmed, unstarted, conflicting and missing
items, correct them with the requirement first, start what can start, and
commit, push, open a pull request and merge. Decision Q03 (document and
contract versions are `X.X.X`) is owner-confirmed in the git-ignored package
`_workspace/governance/workspace_governance_3_0_1_20261115/`.

## Execution Log

### Work Performed

#### Audit of TSK-0068 against the prompt

| Gap | Prompt requirement | TSK-0068 state | Closure |
| --- | --- | --- | --- |
| G-01 | Acceptance: every rule has purpose, owner, consumers and enforcement | Only the seven compared rules | Policy inventory below |
| G-02 | Step 3: one rule is never authored independently in two owners | D-13 left the glossary and the protocol disagreeing on the version profile | Fixed below |
| G-03 | Step 6: verify with fit and violation cases | Tests for vocabulary and template versions; review class and draft rule by review only | Recorded below; no new gate, per Q08 and D03 |
| G-04 | Step 5: no repeated approval for low-risk edits | Not stated | KEEP_VERIFIED: `workflows.md` step 3 keeps an explicit request effective for its unchanged scope |
| G-05 | Report: real latency comparison | Missing | Latency below |
| G-06 | Pending hosted CI of PR 1038 | Pending | PASS; merged as `108006595` |

#### Version profile fix (D-13)

The shared vocabulary 3.0.1 and Q03 limit document and contract versions to
three integers; since W06 (PR 1019) the Stage 99 schemas accepted full SemVer.
The requirement wins. The frontmatter `version`, `template_initial_version`,
`vocabulary_contract.version` and the `common_form_contract` version now
match three integers with no leading zero, suffix or trailing newline;
`documentation-protocol.md` 5.1.0 states the numeric profile; product and
release versions keep full SemVer through `semver.py`. Narrowing is breaking
in principle; no tracked document carries a prerelease or build version, and
all 569 active documents pass the narrowed schema, so no document migrates.
Three W06 tests that asserted the widening now assert the narrowing.

The rest of W03-VERSION stays with it: the parser fullmatch for
non-string types, splitting the combined `common_form_contract` string, and
the compatibility rules for each object.

#### Policy inventory

Code consumers are files under `scripts/`, `tests/` and `.github/` that name
the policy file; a policy with none is enforced by review only.

| Policy | Version | Purpose | Code consumers | Enforcement |
| --- | --- | --- | --- | --- |
| `agentic.md` | 1.9.1 | Auditable provider-neutral agent execution | 1 (`workflow-contract.yml`) | Governance contract leaf |
| `approval-boundaries.md` | 1.5.1 | Approval bound to surface, operation, evidence and recovery | 4 (`agent_governance_contract.py`, `spec_packages.py`) | Governance contract, Spec Package reader |
| `bootstrap.md` | 1.8.1 | The one bootstrap sequence | 8 (`agent-event-hook.sh`, `agent_governance_contract.py`) | Hooks, governance contract |
| `documentation-protocol.md` | 5.1.0 | One document authority per role, truthful provenance | 12 (`links.py`, `identity_history.py`) | Metadata, links, lifecycle checks |
| `environment-constraints.md` | 1.10.2 | Execution boundaries, Graphify, shared memory | 1 (`manifest.yaml`) | Review mostly |
| `git-workflow.md` | 1.8.0 | Git workflow for contributors and agents | 2 (`test_ci_gate_adapters.py`) | Commit grammar, hooks |
| `github-governance.md` | 1.10.0 | GitHub operations baseline | 2 (`test_ci_gate_contract.py`) | Workflow contract, remote rulesets |
| `output-style.md` | 1.2.3 | Outcome-first reporting | 0 | Review only |
| `persona.md` | 1.0.4 | One canonical role identity | 0 | Review only |
| `postflight-checklist.md` | 1.1.2 | Completion verification routing | 0 | Review only |
| `provider-capability-matrix.md` | 1.2.3 | Claude and Codex capability facts | 0 | Review only |
| `quality-standards.md` | 1.12.1 | Universal quality gate | 11 (`post-tool-validate.sh`, `ci_gate_evidence.py`) | Gate runner, CI |
| `sdlc.md` | 1.11.0 | One lifecycle without duplicated shape rules | 10 (`lifecycle.py`, `spec_packages.py`) | Lifecycle and Spec Package checks |
| `stage-authoring-matrix.md` | 1.3.3 | Stage to owner and completion evidence | 1 (`metadata/profile.py`) | Metadata profile check |
| `standards.md` | 1.2.2 | Instruction design and execution quality | 11 (gate files) | Gate runner |
| `task-checklists.md` | 1.5.1 | Scope, evidence and completion checks | 1 (`metadata/profile.py`) | Review mostly |
| `workflows.md` | 1.5.0 | Workflow order and review by risk | 0 | Review only (Q08 adds no gate) |

#### Fit and violation cases

| Rule | Fit case | Violation case | Where |
| --- | --- | --- | --- |
| Vocabulary 3.0.1 | Glossary passes | Missing Korean column, empty Korean cell, renamed term, wrong version | `VocabularyContractTests` |
| Version profile | `0.1.0`, `1.10.0` | `1.0.0-rc.1`, `1.2.3+build.7`, `01.0.0`, trailing newline | `test_registry` schema tests |
| Template version | Edited template at `0.1.0` | Template downgrade | `test_a_template_source_keeps_its_initial_version` |
| Draft authority | Task under approved Spec and Plan runs | Task under a draft parent stays `draft` or `blocked` | `spec_packages.py:686-696` tests |
| Review by risk | - | - | Review only, by design |

#### Latency

PR 1038 (code, Registry and policy changes): `candidate-core` 5 min 30 s,
`candidate-documents` 17 min 43 s. The document-only PRs 1036 and 1037 took
3 min 12 s to 4 min 14 s for `candidate-documents`. One sample each; the
difference follows the leaves the changed paths select.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0069 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0069 | ready | in-progress | #audit-of-tsk-0068-against-the-prompt |

### Blockers and Decisions

No new question. Q03 settles D-13.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Version profile RED | 125 | W130 | red-green-proof | `test_every_schema_version_pattern_is_the_same_semver_pattern` before the change | FAIL | `1.0.0-rc.1` matched | required | - |
| Version profile GREEN | 125 | W130 | red-green-proof | `test_registry` at `431313255` | PASS | module OK | required | Version profile RED |
| Active documents | 125 | W130 | document-metadata | `check-document-metadata.py --mode check-active` at `431313255` | PASS | selected 569, violations 0 | required | - |
| Gap audit | 125 | W130 | source-review | TSK-0068 against each W01 step and acceptance test | PASS | G-01 to G-06 | required | - |
| PR 1038 hosted | 125 | W130 | remote-candidate | PR 1038 at `ba64ba551`, run 43702920379 | PASS | `candidate-quality` success; merged as `108006595` | required | - |

### Resolution Links

Version profile RED is resolved by Version profile GREEN.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 125 | pending | Version profile GREEN, Active documents, Gap audit, PR 1038 hosted | Awaiting independent review and owner acceptance | SPEC-0212 TSK-0069 |

### Remaining Conditions

An independent review of the schema change, hosted candidate checks and
owner acceptance of criteria 123, 124 and 125.

## Handoff

### Promotion Receipt

| Criterion | Work Unit | Task result | Target | Consumer update and check |
| --- | --- | --- | --- | --- |
| 125 | W130 | Version profile GREEN | Stage 99 schemas, `documentation-protocol.md` 5.1.0 | `test_registry`; metadata checks |

### Next Owner

@buenhyden accepts criterion 125. W02-DISPOSITION is ready.
