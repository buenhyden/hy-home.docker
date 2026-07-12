---
status: completed
artifact_id: spec:128-agentic-audit-harness-consolidation
artifact_type: spec
parent_ids:
  - spec:123-agentic-engineering-audit-remediation
---

<!-- Target: docs/03.specs/128-agentic-audit-harness-consolidation/spec.md -->

# Agentic Audit Harness Consolidation Technical Specification (Spec)

## Overview

This specification defines an in-place consolidation and freshness contract for
the Stage 90 audit corpus. It preserves the existing canonical path and dated
evidence while bringing the canonical implementation audit forward to the
current tracked implementation state.

The work separates structural completeness from semantic freshness. The
existing 11-report, 161-criterion contract continues to validate row shape,
identity, vocabulary, and coverage. A new semantic contract validates only
high-confidence remediation closures whose implementation can be proven from
tracked files and completed Stage 04 evidence.

The implementation also corrects security-readiness scope inflation by
separating a scoped ecosystem vulnerability gate from broad dependency SCA and
container-image scanning. The resulting checks are integrated into local
repository contracts and the tracked CI quality workflow.

## Strategic Boundaries & Non-goals

- Keep
  `docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack`
  as the only current agentic implementation audit.
- Keep the 2026-07-03 and 2026-07-04 packs as dated historical snapshots. Do
  not replace their original counts, commands, findings, or closure chronology
  with current values.
- Keep the 2026-07-07 pack as a mapping-only `superseded` ledger.
- Do not physically move the four audit pack directories or the generated
  frontmatter inventory in this workstream.
- Do not add a parallel current-state audit pack, duplicate criterion matrix,
  or second gap source of truth.
- Do not change Docker Compose runtime, infrastructure state, deployment,
  secrets, credentials, remote GitHub settings, provider-global configuration,
  `.gemini` native adoption, provider entitlement, or model-policy literals.
- Do not claim semantic model evaluation, live runtime readiness, CD,
  supply-chain provenance, or remote enforcement from static repository
  evidence.
- Keep Specs 124 through 127 as draft, approval-gated runtime follow-ups.

## Related Inputs

- **PRD**: No dedicated PRD is required. This specification is a bounded
  follow-up to the approved cross-cutting governance and development-harness
  program in Spec 123.
- **ARD**: No dedicated ARD is required because audit organization, local
  validation, and tracked CI wiring do not change runtime architecture.
- **Related ADRs**: No architecture decision is introduced. Any later runtime,
  deployment, identity, registry, or provider-native adoption decision remains
  owned by a separate approved architecture chain.
- **Parent Specification**:
  [Spec 123](../123-agentic-engineering-audit-remediation/spec.md)
- **Canonical Audit Pack**:
  [Agentic engineering implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- **Audit Index**:
  [Audit references](../../90.references/audits/README.md)
- **Historical Snapshots**:
  [2026-07-03 document-contract audit](../../90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md)
  and
  [2026-07-04 restructure audit](../../90.references/audits/2026-07-04-document-restructure-audit-contract-archive/README.md)
- **Supersession Ledger**:
  [2026-07-07 audit mapping](../../90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md)

## Contracts

### Audit Lifecycle Contract

| Surface | Required behavior |
| --- | --- |
| Root audit index | Separate the sole canonical current audit, dated historical snapshots, and supersession ledgers. |
| 2026-07-03 and 2026-07-04 packs | Preserve original evidence and add unambiguous as-of/current-route boundaries. Existing files are listed as included reports, not planned work. |
| 2026-07-05 pack | Remain the only current implementation audit and describe the post-Task-12 tracked state. |
| 2026-07-07 pack | Remain mapping-only and `superseded`; it cannot supply current counts, status, or recommendations. |
| Physical paths | Stay stable to preserve completed evidence, generator paths, metadata profiles, and downstream links. |

### Criterion Contract

- The canonical pack retains exactly one overview and eleven criterion reports.
- The eleven reports retain exactly 161 unique criterion IDs and the existing
  ten-field row schema.
- Every one of the 161 rows is reassessed against current tracked source and
  completed Task 8 through Task 12 evidence.
- A state change must update the row evidence, depth, disposition, owner,
  automation impact, verification, and confidence when those fields are
  affected.
- The overview state distribution and category summaries are derived from the
  reassessed rows rather than copied from the Task 4-6 baseline.
- Historical Task 4-6 facts may remain as dated assessment-method context, but
  must not be presented as the current implementation state.

### Semantic Freshness Contract

The semantic validator complements the structural criterion parser. Its
machine-readable closure assertions contain:

| Field | Meaning |
| --- | --- |
| `criterion_id` | Existing canonical criterion ID. |
| `report` | Criterion report that owns the row. |
| `required_state` | Current state proven by tracked implementation and completed task evidence. |
| `required_evidence_paths` | Tracked paths that must exist for the closure claim. |
| `completed_task_ids` | Stage 04 remediation tasks that establish the closure. |
| `forbidden_stale_phrases` | Narrow phrases that would incorrectly describe a completed closure as future or missing work. |

The assertion set is intentionally smaller than the 161-row corpus. It covers
only deterministic, high-confidence closures such as typed metadata
enforcement, the controlled all-files wrapper, and completed provider/CI
contract synchronization. Runtime facts, provider entitlement, global config,
network state, and remote enforcement are not converted into local assertions.

### Security Readiness Contract

Security readiness must distinguish these independent signals:

1. a scoped ecosystem vulnerability gate;
2. broad dependency SCA coverage; and
3. container/image vulnerability scanning.

A scoped Storybook `npm audit` may satisfy only the first signal. It cannot
satisfy broad dependency SCA or container/image scanning. Existing SBOM,
provenance, attestation, signing, verification, and Scorecard gaps remain
explicit and route to draft Spec 126.

### QA and CI Contract

- Local repository contracts execute structural audit coverage, semantic
  freshness, generated-matrix freshness, and security-readiness freshness.
- The tracked CI quality workflow invokes the semantic freshness check
  explicitly so failures have a named CI surface.
- Checks are deterministic, offline, and independent of Git history depth,
  provider APIs, network access, runtime services, and remote GitHub state.
- Validators report the owning report, criterion, failed condition, and
  expected evidence. They never rewrite audit conclusions automatically.
- The full all-files pre-commit gate is run only through
  `scripts/validation/run-agent-precommit-all-files.sh` from an initially clean
  linked worktree, with result evidence recorded in the Stage 04 task.

## Core Design

### Component Boundary

| Component | Responsibility |
| --- | --- |
| Audit documents | Human-reviewable current findings, gaps, evidence, ownership, and approval boundaries. |
| Structural criterion parser | Exact report/ID/schema/vocabulary completeness for the 11/161 contract. |
| Semantic closure contract | Machine-readable assertions for deterministic completed remediations. |
| Semantic freshness validator | Evidence-path, state, completed-task, stale-phrase, and lifecycle routing checks. |
| Audit matrix generator | Derived coverage, state distribution, and separate structural/semantic results. |
| Security readiness generator | Scoped and broad vulnerability-control signals without inflated claims. |
| Repository and CI gates | Deterministic orchestration and visible failure routing. |

### Key Dependencies

- `scripts/validation/audit_criterion_contract.py`
- `scripts/validation/generate-audit-implementation-matrix.sh`
- `scripts/validation/check-repo-contracts.sh`
- `scripts/validation/generate-security-automation-readiness.sh`
- `scripts/validation/check-document-metadata.py`
- `.github/workflows/ci-quality.yml`
- completed task evidence in
  `docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md`
- Stage 00 approval, QA, documentation, provider, and task-evidence contracts

### Tech Stack

- Python standard library for semantic parsing and validation.
- JSON for the machine-readable closure assertion contract.
- Bash for existing generator and repository-check orchestration.
- Markdown and YAML for Stage 90 references and tracked workflow definitions.

## Data Modeling & Storage Strategy

### Canonical Ownership

Criterion rows remain canonical in the eleven audit reports. The semantic
closure contract does not duplicate every row; it records only the subset whose
state must not regress below a proven remediation closure.

The implementation overview owns cross-category summaries and the current gap
and improvement-priority view. Category reports own detailed evidence. The
generated audit matrix remains derived data and cannot override either source.

### Transition Plan

1. Clarify pack lifecycle roles without moving files.
2. Reassess all canonical rows and overview summaries.
3. Add semantic closure assertions for deterministic completed work.
4. Correct security-readiness signal granularity.
5. Integrate checks into repository and tracked CI quality gates.
6. Regenerate derived references and record final evidence.

## Interfaces & Data Structures

### Semantic Closure Assertion

```json
{
  "criterion_id": "QAF-12",
  "report": "sdlc-quality-formatting-implementation.md",
  "required_state": "Implemented",
  "required_evidence_paths": [
    "scripts/validation/run-agent-precommit-all-files.sh",
    "tests/validation/test_run_agent_precommit_all_files.sh"
  ],
  "completed_task_ids": ["T-AER-009"],
  "forbidden_stale_phrases": [
    "controlled wrapper does not yet exist",
    "Task 9 will add wrapper"
  ]
}
```

Exact assertion content is implementation data and must be reviewed with the
reassessed criterion rows. The example defines the interface, not the complete
manifest.

### Validator Result

```text
audit_semantic_freshness: PASS assertions=<count> failures=0
```

On failure, diagnostics include the criterion ID, report path, failed rule,
and expected evidence or state. Output excludes raw logs, secrets, credentials,
tokens, and provider-global configuration.

## API Contract (If Applicable)

Not applicable. This work introduces repository-local scripts and document
contracts only; it exposes no external API.

## Agent Role & IO Contract

- **Agent Role**: A fresh implementation agent performs each bounded task; a
  separate reviewer evaluates specification compliance and quality.
- **Inputs**: This specification, the approved Stage 04 task brief, current
  tracked source, and only the interfaces required by that task.
- **Outputs**: One logical commit, focused test evidence, self-review, and a
  concise implementation report.
- **Success Definition**: Each task passes both independent review verdicts
  before the next task begins; a final whole-branch review approves the exact
  merge-base-to-HEAD range.

## Tools & Tool Contract

- **Tool List**: repository reads, `apply_patch`, focused validation commands,
  Git status/diff/commit operations, Graphify refresh after code changes, and
  the controlled pre-commit wrapper at the final gate.
- **Permission Boundary**: No runtime service, remote mutation, secret access,
  provider-global config inspection, or model-policy mutation.
- **Failure Handling**: Stop on ambiguous evidence, structural or semantic
  validation failure, unexpected wrapper paths, or unresolved independent
  review findings.

## Prompt / Policy Contract

- Stage 00 remains the policy authority.
- Historical snapshots never override current tracked source or the canonical
  audit.
- Structural freshness and semantic freshness are reported as separate facts.
- `Partial`, `Missing`, and `Needs Revalidation` are retained whenever local
  evidence cannot justify a stronger state.
- Provider differences are not normalized into false parity.

## Memory & Context Strategy

- Stage 04 task evidence is the durable execution ledger.
- `docs/00.agent-governance/memory/progress.md` records material progress and
  final verification.
- Subagent task briefs, reports, and review packages remain implementation
  scratch evidence; canonical conclusions are written only to Stage 90 and
  Stage 04 targets.

## Guardrails

- **Input Guardrails**: Parse only the canonical pack, the declared semantic
  assertion contract, and tracked evidence paths under the repository root.
- **Output Guardrails**: Emit deterministic diagnostics and generated
  references without network-derived or secret-bearing data.
- **Blocked Conditions**: Missing criterion IDs, invalid states, unresolved
  evidence ambiguity, runtime-only claims, failed tests, or unapproved
  protected-surface expansion.
- **Escalation Rule**: Route runtime, remote, secret, provider-native adoption,
  and model-policy findings to their existing draft specs or a new approved
  active-stage chain rather than implementing them here.

## Evaluation

- **Eval Types**: Unit, adversarial fixture, integration, generation
  idempotence, documentation-contract, and independent review.
- **Metrics**: 11 reports, 161 unique criterion IDs, zero structural failures,
  zero semantic assertion failures, zero generated drift, and zero unresolved
  Critical or Important review findings.
- **Fixtures**: Wrong criterion state, missing evidence path, completed task
  described as future work, invalid pack lifecycle routing, and scoped
  vulnerability evidence mislabeled as broad SCA/container coverage.
- **How to Run**: Use the commands in the Verification section and the final
  controlled pre-commit wrapper invocation defined by the Stage 04 plan.

## Edge Cases & Error Handling

- A historical leaf may use present tense inside preserved evidence. Its
  snapshot boundary must prevent that sentence from being cited as current
  truth; original evidence is not rewritten merely for style.
- A criterion can remain `Partial` even when one sub-control becomes
  implemented. The state must reflect the criterion wording and evidence scope,
  not the existence of any related file.
- A completed task reference is not sufficient by itself. Required tracked
  implementation paths must also exist.
- A missing runtime or remote observation remains `Needs Revalidation`; the
  validator must not convert uncertainty into `Missing` or `Implemented`.
- Generated documents cannot be hand-edited to satisfy freshness; their owner
  generator must produce the final bytes.
- A shallow Git checkout must not make semantic validation indeterminate,
  because the contract does not depend on path commit history.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Structural and semantic contracts disagree.
  **Fallback**: Treat the audit as invalid, identify the owning criterion, and
  correct the canonical row or assertion before generation.
- **Failure Mode**: Evidence supports more than one reasonable state.
  **Fallback**: Retain the more conservative state and record the uncertainty
  in confidence and follow-up text.
- **Failure Mode**: A proposed fix requires runtime, secret, remote, provider,
  or model-policy mutation.
  **Human Escalation**: Stop and request separate approval through the owning
  active-stage chain.
- **Failure Mode**: Final controlled pre-commit changes unexpected paths.
  **Fallback**: Stop without cleanup, review every Git-visible path, and record
  the disposition in task evidence.

## Verification

```bash
python3 -m unittest discover -s tests/validation -q
python3 scripts/validation/check-document-metadata.py check-changed --base <safe-base>
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/report-audit-pack-coverage.sh --check
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
git diff --check
```

The Stage 04 plan must replace `<safe-base>` with the exact merge base or task
base. It must also define the final
`scripts/validation/run-agent-precommit-all-files.sh` invocation and allowed
prefixes before execution.

## Success Criteria & Verification Plan

- **VAL-AHC-001**: The audit index exposes exactly one canonical current audit,
  two dated historical snapshots, and one supersession ledger without moving
  pack paths.
- **VAL-AHC-002**: The historical snapshot values and evidence chronology are
  preserved and cannot be mistaken for current corpus truth.
- **VAL-AHC-003**: All eleven criterion reports and 161 unique rows pass the
  structural contract after current-state reassessment.
- **VAL-AHC-004**: The overview, category reports, generated state
  distribution, and deterministic closure assertions agree.
- **VAL-AHC-005**: Regressing a proven closure to stale future/missing wording
  or removing required evidence causes a focused semantic validation failure.
- **VAL-AHC-006**: Security readiness distinguishes scoped ecosystem audit,
  broad dependency SCA, and container/image scanning without overclaiming.
- **VAL-AHC-007**: Local repository contracts and tracked CI quality wiring
  execute the semantic check without network, runtime, remote, or Git-history
  dependence.
- **VAL-AHC-008**: Generated audit, metadata, security, and LLM Wiki references
  are fresh and idempotent.
- **VAL-AHC-009**: The controlled final pre-commit gate passes from an initially
  clean linked worktree and records changed/unexpected-path evidence.
- **VAL-AHC-010**: Six logical implementation tasks receive separate
  implementer and reviewer verdicts, and the whole branch finishes with zero
  unresolved Critical or Important findings.

## Related Documents

- [Implementation plan](../../04.execution/plans/2026-07-12-agentic-audit-harness-consolidation.md)
- [Execution task](../../04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md)
- [Parent agentic audit remediation spec](../123-agentic-engineering-audit-remediation/spec.md)
- [Canonical agentic implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Audit references index](../../90.references/audits/README.md)
- [Audit implementation matrix](../../90.references/data/governance/audit-implementation-matrix.md)
- [Security automation readiness](../../90.references/data/security/security-automation-readiness.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Task checklists](../../00.agent-governance/rules/task-checklists.md)
- [Typed metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [Spec template](../../99.templates/templates/sdlc/spec.template.md)
