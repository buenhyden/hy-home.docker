---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "specs"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids:
- "{{PARENT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->
<!-- Author prompt: Before setting status to cancelled, supply cancellation frontmatter with a nonempty reason, an actual authorization_ref, and criteria_disposition entries containing an integer criterion plus exactly one successor Task identity or approved withdrawal_ref. A successor is another non-cancelled Task in the same package. authorization_ref and withdrawal_ref use unambiguous same-Task heading anchors to actual structural evidence; those records do not authenticate or grant approval. An empty criteria_disposition list states that this Task held no criterion; it does not close any Spec criterion. Never seed or infer cancellation approval. -->
<!-- Author prompt: Keep the Evidence header, separator, and every data row in one contiguous pipe-table block. Narrative may appear before or after that block; put other pipe tables outside the Results subsection. -->
<!-- Author prompt: Evidence records observations only. Required is required or optional. Result is PASS, FAIL, ERROR, NOT_RUN, CANCELLED or NOT_APPLICABLE; every required non-PASS observation remains open until an equivalent PASS explicitly resolves it. Name each row uniquely. In Resolves, write `-` or the names of earlier non-PASS rows with the same Check and Work Unit in this Task that this PASS row resolves for a shared criterion. -->
<!-- Author prompt: Criterion Acceptance holds one row for each Spec criterion this Task owns. A criterion the Plan assigns to a current, non-cancelled Task has exactly one row, in one such Task; a criterion whose assigned Tasks are all historical or cancelled has none. Acceptance is pending, accepted, rejected or not-required; accepted needs a PASS row for the criterion and no unresolved required observation; not-required and rejected need a Decision. Current Owner names the durable owner or a reasoned N/A disposition. The Evidence cell is `-` or names of this Task's Evidence rows. Keep that table in the Criterion Decisions subsection and put no other pipe table there. -->
<!-- Author prompt: For several independently tracked items, add an `#### Execution Items` table under Work Performed with `Item | Work Unit | Scope | Owner | Status | Blocker` and at least two rows, and remove the frontmatter `status`; each row then owns its status, each Work Unit belongs to one item, and a blocked or cancelled item names its Blocker. -->

# {{TITLE}}

## Scope

### Objective and Parent

{{OBJECTIVE_AND_PARENT_PLAN_AND_WORK_UNITS}}

### Inputs and Authority

<!-- Author prompt: Name the Spec criteria, the Plan work units and the authority this Task works under. An authorization grants no operation by being named here. -->

{{INPUTS_AND_AUTHORITY}}

## Execution Log

### Work Performed

<!-- Author prompt: Record what was done in order, with the commits or artifacts it produced. Keep each lifecycle event, execution item and reconciliation table under Work Performed as its own `####` heading, and anything a reader links to as a heading of that level or deeper. A section with nothing to record says why in one sentence instead of staying empty. -->

{{WORK_PERFORMED}}

### Blockers and Decisions

{{BLOCKERS_DEFERRALS_AND_RULINGS}}

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{EVIDENCE}} | {{CRITERIA}} | {{WORK_UNIT}} | {{CHECK}} | {{INPUT}} | {{RESULT}} | {{LOCATION}} | {{REQUIRED}} | {{RESOLVES}} |

### Resolution Links

{{LINKS_FROM_FAILED_OBSERVATIONS_TO_THEIR_RESOLUTION}}

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| {{CRITERION}} | {{ACCEPTANCE}} | {{ACCEPTANCE_EVIDENCE}} | {{DECISION}} | {{CURRENT_OWNER}} |

### Remaining Conditions

{{REMAINING_CONDITIONS_AND_DEFERRED_ITEMS}}

## Handoff

### Promotion Receipt

<!-- Author prompt: Name the durable document that now holds what this Task established, and the check that shows it does. -->

{{PROMOTION_TARGET_AND_RECEIPT}}

### Next Owner

{{NEXT_OWNER_AND_RESUME_CONDITIONS}}
