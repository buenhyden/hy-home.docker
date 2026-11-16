---
title: "W03 Version 3.0.1 Task"
version: "0.2.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-11-17"
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

#### Standalone W03-VERSION design

The 2026-11-16 W03-VERSION request exercises D02 3.0.1 directly against
local commit `0386a1f90`. The prior W130 acceptance and W133 evidence
cover the existing bindings and syntax. A 5,000-digit core component
passes both the schema grammar and Python fullmatch but raises an
uncaught conversion error in precedence. A numeric product prerelease
identifier reaches the same conversion. Use exact integer conversion
for both paths. Preserve accepted input width instead of introducing
a new grammar cap or raising the interpreter limit for the process.

Keep the Stage 99 schemas independently readable. Treat their numeric
patterns as checked projections of the Python numeric core and test
them against the authored grammar. In the version-policy owner, state
the compatibility rule for producer/consumer pairs and the reset rule
for lower components. Compatibility of prose and contracts is a review
decision. The comparator keeps its existing precedence diagnostics.
Use focused RED and GREEN tests, historical Registry validation, the
bundled syntax examples and product release regression. Revert the
follow-up source and policy together if the new behavior regresses.

#### Standalone W03-VERSION compatibility decision

The prior acceptance policy compared precedence and delegated compatibility
to review. The documentation protocol now requires the correct bump class
and lower-component resets, which can reject a previously admissible change.
Its version rises from 5.2.0 to 6.0.0. The comparator correction preserves
the version grammar and returns exact integers through the existing
interface. The Registry, TemplateDefinition projection, template default,
product values and identity counters keep their existing revisions.
No consumer reads the bundled fixtures during normal operation.

On 2026-11-16, a paired Python 3.12.3 timing sample compared the
`0386a1f90` source with the follow-up. The median of five passes over
40,000 ordinary comparisons was 0.241927 seconds before and 0.243602
seconds after. The pair exercises numeric component ordering and
numeric product prerelease ordering.

#### Pre-1.0 compatibility alignment

The repeated W03-VERSION request starts at `efdf08f92`. D02 3.0.1
requires MAJOR for a previously valid producer or consumer that breaks.
The Version objects section already says so. The authoring section of
the same policy still instead directs authors below 1.0.0 to use MINOR
for breaking changes. Route authors to Version objects and apply the
same compatibility decision to 0.x versions. Keep the initial 0.1.0
template pin. Record the owner's approval of the exact revision in the
lifecycle. An approval-only transition keeps its content version.

The policy advances from 6.0.0 to 7.0.0 because an author following the
former 0.x exception could submit a breaking MINOR increase. Approval
alone also ceases to require a jump to 1.0.0.
For a breaking change from 0.4.2 the new rule requires 1.0.0 and
rejects 0.5.0. For a compatible addition it requires 0.5.0, and for
a correction preserving the consumer contract it requires 0.4.3.
An approval-only transition of 0.4.2 keeps 0.4.2.
Review the cases against the policy. Reuse the existing numeric
precedence checker and keep its output, schema and product domain.
Reverting this source unit restores the former policy text.

#### Resumed lifecycle-only comparison

At `427ca60f0`, D02 3.0.1 and the Version objects policy exempt
lifecycle-only edits. The frontmatter reader accepts quoted keys and
multiline scalar values. The version checker strips whole lines by
their literal prefix, so it can still ask for a version increase when
only a lifecycle field changes in one of those forms.

Reuse the validated frontmatter parser to compare the non-lifecycle
mapping and the full Markdown body. Preserve scalar types at every
depth, including the integer type used by cancellation criteria.
Ignore frontmatter serialization differences that preserve its
parsed values and types. Leave malformed YAML to
its existing diagnostics and compare raw content if parsing fails.
Keep the existing version diagnostics, same-path merge base and
product comparison. Test the changed path through a committed fixture
with lifecycle-only and substantive edits. Revert the source unit to
restore the former comparison.

For 500 lifecycle-only fixture comparisons, the median of five local
runs was 0.02398 seconds before and 0.61511 seconds after. Both runs
supplied the same merge-base text in memory, so this measures parsing
and file reading without Git subprocess time.

The expanded metadata reference run was interrupted. The first
focused rerun used a wrong module path for the Registry tests. The
corrected selection includes the version checks, the two relevant
CLI integration cases, Registry and projection checks, product version
checks, and release regression.

#### W03-VERSION 4.2.0 recheck

The 2026-11-17 W03-VERSION request read D02 and D27 of the 4.2.0 package
at `615d46546`. Since 3.0.1, D02 adds a follow-up rule and a 4.1.0
boundary section. The 24 version fixtures are byte-identical to 3.0.1.
The Docker attachment item D-W03 is a path plan owned by DOC-PATH-PLAN
for the final cutover, so it adds no version action.

| D02 rule | Disposition | Basis |
| --- | --- | --- |
| Numeric three-part fullmatch, rejecting space, newline, leading zero, suffix and non-ASCII digits | KEEP_VERIFIED | Python fullmatch, five schema patterns and Node agree on all 24 fixtures |
| Integer precedence, including long components | KEEP_VERIFIED | 1.9.0 is below 1.10.0 and a 5,000-digit core compares without error |
| Separate `contract_id` and `contract_version` | KEEP_VERIFIED | The Registry, TemplateDefinition schema and glossary keep them apart; a package label and a combined value are rejected |
| Product tags, external labels and integer counters keep their own domains | KEEP_VERIFIED | Product parsing passes its release tests; the Hermes submit contract stays an integer |
| MAJOR, MINOR and PATCH by consumer compatibility | KEEP_VERIFIED | The documentation protocol Version objects rules from the earlier runs still apply |

`lifecycle.py` changed three times after `427ca60f0`, for input reuse and
root README discovery. The focused version selection still passes on the
current source. No source change is needed.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0072 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0072 | ready | in-progress | #design-and-compatibility |
| SPEC-0212-TSK-0072 | in-progress | completed | #criterion-decisions |

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
| Long component RED | 128 | W133 | long-version-order | test_semver long core and product prerelease fixture against 0386a1f90 | ERROR | 5,000-digit core raises ValueError, exit 1 | required | - |
| Long component GREEN | 128 | W133 | long-version-order | test_semver, metadata VersionChangeTests, two Registry syntax tests and product test_release | PASS | 51 tests in 3.461 seconds, exit 0 | required | Long component RED |
| Standalone syntax probe | 128 | W133 | version-fixtures | 24 bundled values through Python fullmatch, three schema rules and Node RegExp | PASS | 24 cases per reader and 1.9.0 below 1.10.0, exit 0 | required | - |
| Standalone governance | 128 | W133 | governance-contract | check-agent-governance-contract.py with compatibility policy 6.0.0 | PASS | 0 failures, exit 0 | required | - |
| Standalone metadata | 128 | W133 | metadata | check-document-metadata.py --mode check-changed --base-ref HEAD with the policy and this Task selected | PASS | Base 0386a1f90, 2 documents and 0 violations, exit 0 | required | - |
| Standalone review finding | 128 | W133 | standalone-review | Initial comparator, compatibility policy and schema test diff | FAIL | The test could miss a deleted schema start anchor | required | - |
| Standalone review resolution | 128 | W133 | standalone-review | Raw schema pattern parity and the prefixed input case | PASS | Rules-engineer approved the fix. Both focused schema tests passed and a missing anchor mutation was detected | required | Standalone review finding |
| Pre-1.0 review finding | 128 | W133 | pre-one-review | First policy reconciliation | FAIL | Mandatory 1.0.0 on approval changed content version without a compatibility change | required | - |
| Pre-1.0 review resolution | 128 | W133 | pre-one-review | Version objects rules and the four cases from 0.4.2 | PASS | Rules-engineer confirmed the compatibility classes and approval of the exact revision | required | Pre-1.0 review finding |
| Version recheck | 128 | W133 | version-regression | test_semver, metadata VersionChangeTests, the Registry syntax pair, the TemplateDefinition binding pair and test_release on efdf08f92 | PASS | 53 tests, exit 0 | required | - |
| Fixture recheck | 128 | W133 | version-fixtures | Bundled values in Python, five schema rules and Node plus the Registry at 17bbde05a | PASS | 24 cases per reader and no historical Registry violations, exit 0 | required | - |
| Policy alignment checks | 128 | W133 | policy-alignment | Governance contract, document link alignment and change metadata for the policy and this Task | PASS | Governance and links had no failures. Metadata selected 2 and reported 0 violations in 224.48 seconds | required | - |
| Resumed version baseline | 128 | W133 | version-regression | Prior focused version selection at 427ca60f0 | PASS | 53 tests, exit 0 | required | - |
| Lifecycle serialization RED | 128 | W133 | lifecycle-version | Quoted key and multiline scalar in the same-path committed fixture | FAIL | Both lifecycle-only changes reported version-unchanged, exit 1 | required | - |
| Nested type RED | 128 | W133 | lifecycle-version | Cancellation criterion switches from integer to float under the initial parser comparison | ERROR | Expected version-unchanged was absent, exit 1 | required | - |
| Lifecycle comparison GREEN | 128 | W133 | lifecycle-version | Corrected focused selection with typed nested comparison, CLI checks and product regression | PASS | 64 tests in 7.568 seconds, exit 0 | required | Lifecycle serialization RED, Nested type RED |
| Resumed changed metadata | 128 | W133 | metadata | check-document-metadata.py --mode check-changed --base-ref HEAD with this Task selected, before the nested type correction | PASS | Base 427ca60f0, 1 document and 0 violations, exit 0 | required | - |
| Lifecycle review finding | 128 | W133 | lifecycle-version-review | Initial structured comparison | FAIL | Python equality could equate an integer and float in nested metadata | required | - |
| Lifecycle review resolution | 128 | W133 | lifecycle-version-review | Recursive scalar type preservation and committed fixture | PASS | Independent reviewer approved the fix | required | Lifecycle review finding |
| 4.2.0 fixture recheck | 128 | W133 | version-fixtures | 4.2.0 bundled values through Python fullmatch, five schema patterns and Node RegExp at `615d46546` | PASS | 24 cases per reader, 1.9.0 below 1.10.0, 5,000-digit core ordered, exit 0 | required | - |
| 4.2.0 version regression | 128 | W133 | version-regression | test_semver, metadata version and product classes, five Registry and two TemplateDefinition version tests, test_release at `615d46546` | PASS | 66 tests in 6.437 seconds, exit 0 | required | - |

### Resolution Links

The GREEN rows resolve the matching comparison, projection and long
component failures.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 128 | accepted | Resumed version baseline, Lifecycle comparison GREEN, Lifecycle review resolution | Owner @buenhyden accepted on 2026-11-16 in this chat | @buenhyden |

### Remaining Conditions

None. The owner accepted criterion 128 on 2026-11-16 and every non-PASS
row has a resolving row, so W133 is complete.

## Handoff

### Promotion Receipt

Stage 99 owns the version binding and output schema. The metadata reader
owns comparison against the merge base. These determine the functional
inputs consumed by W134.

### Next Owner

None for W133. A later version change is owned by the Task that makes it.
