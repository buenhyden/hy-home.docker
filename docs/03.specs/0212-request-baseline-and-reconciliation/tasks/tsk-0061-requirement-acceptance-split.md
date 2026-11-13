---
title: "Requirement Acceptance Split Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0061"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-13"
---

# Requirement Acceptance Split Task

## Scope

### Objective and Parent

#### Objective

Own W119/criterion 114. Carry the Requirement acceptance items that
[TSK-0058](tsk-0058-w03-templates-metadata-relations.md) held for an owner
decision:

- REQ-0024 to REQ-0027 group their acceptance conditions; give each functional
  and quality requirement identity its own condition;
- the REQ-0003 quality requirements NFR-0005 to NFR-0007 have no acceptance
  condition; add one each.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [REQ-0003](../../../01.requirements/0003-security.md)
- [REQ-0024](../../../01.requirements/0024-agent-governance-standardization.md)
- [REQ-0025](../../../01.requirements/0025-operational-readiness-closure.md)
- [REQ-0026](../../../01.requirements/0026-document-retention-and-retirement.md)
- [REQ-0027](../../../01.requirements/0027-home-development-host.md)

### Inputs and Authority

On 2026-11-13 the owner chose "I draft, you approve" for the held wording,
then approved the draft as written. The draft followed one rule: each
condition is either an existing condition moved to the identity it covers, or
the requirement's own text or stated `measure:` written as a checkable
condition. No condition adds an obligation, and each Verification Method
paragraph is unchanged.

The authorization covers the five Requirement packages, this Task and the
criterion 114 and W119 entries in the Spec and Plan. It grants no runtime
operation, and the validator work TSK-0058 handed to W05 stays there.

## Execution Log

### Work Performed

#### Owner-approved Requirement wording

The owner's approval of 2026-11-13 issues this Task.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0061 | draft | ready | #owner-approved-requirement-wording |
| SPEC-0212-TSK-0061 | ready | in-progress | #owner-approved-requirement-wording |

#### Acceptance conditions 2026-11-13

| Requirement | Before | After | Version |
| --- | --- | --- | --- |
| REQ-0003 | FR-0001 to FR-0004 only | Also NFR-0005 to NFR-0007, from each stated measure | 1.4.0 |
| REQ-0024 | 7 grouped conditions | 15, one per FR and NFR identity | 1.8.0 |
| REQ-0025 | 4 grouped conditions | 15, one per FR and NFR identity | 1.3.0 |
| REQ-0026 | 7 grouped conditions | 13, one per FR and NFR identity | 3.1.0 |
| REQ-0027 | 5 numbered conditions | 13, one per FR and NFR identity | 1.1.0 |

Every grouped condition survives under the identity it covers; a condition
that covered two identities is split between them. The REQ-0025 clause that
focused tests and the full profile pass was already stated by its
Verification Method and is not repeated as a condition.

#### Review fixes 2026-11-13

The independent review found two conditions wider than their requirement,
each narrowed back to the requirement text:

- REQ-0024-FR-0014 asked every category for a Stage 99 profile and root
  inventory; the requirement asks it only of Markdown instruction categories.
- REQ-0026-FR-0001 barred a check from failing a document by age or size; the
  requirement bars only automatic removal.

Minor fixes: REQ-0027-FR-0005 and FR-0006 keep the old "actual results are
recorded" clause that FR-0003 already kept, and REQ-0026-FR-0011 says
"registered link checks", as its Verification Method does, instead of naming
one check mode. The "Stage 98 documents as input" clause stays under
REQ-0024-FR-0008 with its text unchanged.

### Blockers and Decisions

None: the owner approved the wording before any file changed.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Per-ID coverage | 114 | W119 | identity-coverage | Uncommitted change on `main` `16e4e6f5b`: requirement identities under Requirements against bold identities under Acceptance Conditions in the five packages | PASS | Equal sets: REQ-0003 7, REQ-0024 15, REQ-0025 15, REQ-0026 13, REQ-0027 13 | required | - |
| Requirement wording review | 114 | W119 | independent-review | Fresh-context code-reviewer of the uncommitted change on `16e4e6f5b` | FAIL | CHANGES_REQUIRED: REQ-0024-FR-0014 and REQ-0026-FR-0001 wider than their requirement; four minor (REQ-0027 recorded-results clause, REQ-0024 Stage 98 clause placement, REQ-0026 check-mode name, revision missing in this Task) | required | - |

### Resolution Links

The wording review FAIL is resolved by the re-review row once it passes.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 114 | pending | - | - | SPEC-0212 TSK-0061 |

### Remaining Conditions

The checks, an independent review and owner acceptance of criterion 114 are
open.

## Handoff

### Promotion Receipt

None: the change has not landed on `main` yet.

### Next Owner

The current owner is @buenhyden, who decides criterion 114.
