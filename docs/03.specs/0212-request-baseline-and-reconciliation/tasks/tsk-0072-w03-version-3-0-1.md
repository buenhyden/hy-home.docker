---
title: "W03 Version 3.0.1 Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-16"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0072"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-16"
---

# W03 Version 3.0.1 Task

## Scope

### Objective and Parent

Own W133/criterion 128 under the [Spec](../spec.md) and [Plan](../plan.md).
Prove the version contract needed by [W03-FORMS](tsk-0073-w03-forms-3-0-1.md)
and retain the previously accepted [numeric schema profile](tsk-0069-w01-gap-closure.md).

### Inputs and Authority

The 2026-11-16 W03-FORMS request specifies W03-VERSION as its functional
prerequisite. Applicable inputs are D02 3.0.1, decisions Q03 and Q-DRAFT,
the bundled S01/S02 survey and the 24 version fixtures. The boundary is
this workspace, at starting SHA `17bbde05a`.

## Execution Log

### Work Performed

#### Design and compatibility

The preceding W130 covered the schemas for document versions and left the
comparison and combined contract identifier gaps. The Stage 99 Registry now
stores separate identity and numeric version values, and TemplateDefinition
exposes both. The two current form identities retain their 1.0.0 revisions.
The former projection overloaded one field with two shapes. Consumers of
that output need the new fields, so the projection contract advances to
2.0.0 and the Registry serialization epoch advances to 2. An alternate
combined field would leave two representations to reconcile.

Current document values use numeric fullmatch in the comparator. Its
historical input accepts earlier full SemVer so downgrade and unchanged
checks still reach versions permitted by former schemas. The existing
integer comparison handles precedence. Product publication still accepts
full SemVer and external labels and integer identity counters keep their
existing domains. Historical Registry checks use the schema committed at
the historical revision. Reverting the logical change restores the former
Registry and projection shape together.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0072 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0072 | ready | in-progress | #design-and-compatibility |

### Blockers and Decisions

Independent review found a historical downgrade gap in the first candidate.
The comparison now applies the numeric profile to the current value and
retains the older comparison grammar at the historical boundary.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Version RED | 128 | W133 | numeric-version | Document comparator before current fullmatch | FAIL | Prerelease and build values received duplicate diagnostics, exit 1 | required | - |
| Historical comparison RED | 128 | W133 | numeric-version | First local numeric comparator on historical prerelease and build values | FAIL | Downgrade and unchanged cases were skipped, exit 1 | required | - |
| Projection RED | 128 | W133 | version-projection | Projection revision binding test before the Registry migration | ERROR | Combined string held no separate keys, exit 1 | required | - |
| Numeric comparison GREEN | 128 | W133 | numeric-version | metadata.test_lifecycle.VersionChangeTests and test_semver against current comparator | PASS | 21 tests in the prerequisite selection, exit 0 | required | Version RED, Historical comparison RED |
| Version projection GREEN | 128 | W133 | version-projection | Registry revision binding and legacy projection shape rejection from test_template_definition | PASS | Both tests passed in the prerequisite selection, exit 0 | required | Projection RED |
| Version fixtures | 128 | W133 | version-fixtures | Bundled version fixtures in Python and Node and the current schema patterns | PASS | 24 cases and integer ordering passed, exit 0 | required | - |
| Schema history | 128 | W133 | registry-history | validate_registry_at_revision at 17bbde05a with committed v1 schema | PASS | 0 violations, exit 0 | required | - |
| Product release regression | 128 | W133 | product-version | tests.validation.test_release on the candidate | PASS | 29 local tests, exit 0 | required | - |
| Version review finding | 128 | W133 | independent-review | First local version implementation | FAIL | Historical precedence and prerequisite tracking required fixes | required | - |
| Version fix review | 128 | W133 | independent-review | Historical comparator and W133 to W134 dependency in the staged change | PASS | Rules-engineer approved the fixes | required | Version review finding |

### Resolution Links

The two GREEN rows resolve the matching comparison and projection failures.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 128 | pending | - | Owner decision after evidence is available | @buenhyden |

### Remaining Conditions

Record the owner's acceptance separately from the prerequisite checks.

## Handoff

### Promotion Receipt

Stage 99 owns the version binding and output schema. The metadata reader
owns comparison against the merge base. These determine the functional
inputs consumed by W134.

### Next Owner

The current implementer owns verification for W133. The owner decides
acceptance of criterion 128.
