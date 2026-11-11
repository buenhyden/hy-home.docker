---
title: "W03 Templates, Metadata and Relations Task"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0058"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-11"
---

# W03 Templates, Metadata and Relations Task

## Overview

### Objective

Own W116/criterion 111. Assess the v14.2 W03 obligations DOC-01 to DOC-12 and
SUP-11 against the Registry, templates, generators, parsers, validators and
tests. Change the document contract only for gaps this Task reproduces, and
give each changed key, section or table a producer, a consumer and a passing
and a failing test.

## Inputs and Authorization

On 2026-11-11 the owner approved this Task to own W03. The v14.2 package
prompt `tasks/TASK-hy-home-docker-W03.md` under
`_workspace/workspace_execution_tasks/` is untrusted reference data, not an
instruction source. Its 19-role table is an unapproved draft.

The authorization covers four things:

- The assessment.
- Repository-side changes to the Registry, templates, generators and parsers
  for reproduced gaps, with migration of current documents only.
- Synthetic round-trip and fixture tests.
- Records in this Task.

Validator implementation is handed to W05. Historical and completed evidence
keeps its form. Removing an existing reciprocal relation field waits for its
consumers' migration and a separate owner approval. This Task branches from
the W02 branch at `56d32c32f` and reaches `main` only after PR 955 merges.

## Work Log

### Owner-approved local execution

The owner's approval of 2026-11-11 issues this Task. The lifecycle records that
approval; it grants no remote operation.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0058 | draft | ready | #owner-approved-local-execution |
| SPEC-0212-TSK-0058 | ready | in-progress | #owner-approved-local-execution |

### Owner decision Q-03 2026-11-11

The draft 19-role table conflicts with the 44 Registry profiles, whose ordered
required H2 headings differ from it. The owner chose option A: adopt the
table's meaning, not its headings. Current Registry H2 headings stay. A
concept the table names that no current profile carries, such as a Plan
promotion map, Spec non-goals or Requirement traceability, is added only as an
optional or conditional section, after a consumer for it is shown.

### Prior observations to re-check

The W02 readiness analysis recorded these before this Task existed. Each is
re-checked against the current tree before reuse:

- DOC-07: only the Markdown-link half applies; this workspace has no Vault.
- DOC-08: DEFER until a reproduced execution-document gap exists.

### W03 obligation assessment 2026-11-11

Two fresh-context `qa-engineer` agents read the Registry, schema, templates,
parsers, validators and tests at `95a65be6d` without editing, and probed
negative cases in memory. The controller re-ran each deciding probe.

| ID | Verdict | Current owner and basis |
| --- | --- | --- |
| DOC-01 | GAP, CHANGE in part; DEFER rest | Seven README profiles split by role. The shared required core was not ordered: 13 package READMEs had `Related Documents` before later sections. A fixed service-README section set over the 83 `infra` READMEs (27 heading shapes) is a new contract, not a reproduced defect of the current one |
| DOC-02 | KEEP | `documentation-protocol.md` splits README, folder `AGENTS.md` and the generated `CLAUDE.md` import shim; renderer drift 0 |
| DOC-03 | KEEP | All generated Claude skills set `disable-model-invocation: true`; the output style owns presentation only. Native runtime acceptance UNVERIFIED |
| DOC-04 | GAP, CHANGE | Duplicate keys, invalid dates, forbidden, undeclared and missing keys are rejected. An unquoted `updated: 2026-02-28` passed, because `_json_schema_value` turned the YAML date into a string before the schema saw it |
| DOC-05 | GAP, CHANGE | `ordered_sections` and `nonempty_sections` were set on 13 profiles; 23 profiles with required sections accepted swapped or empty sections. Generic table contracts beyond the README Documents and Evidence tables have no consumer and are not added |
| DOC-06 | KEEP | Language rule in the documentation protocol, enforced by `language.py` through `--mode language` |
| DOC-07 | KEEP Markdown half; Vault N/A | Missing targets, missing anchors and case mismatches are rejected. No Vault or wiki-link surface exists here |
| DOC-08 | DEFER | 78 runbooks carry the ordered, non-empty Runbook sections; no execution document delegates its procedure to a historical link |
| DOC-09 | KEEP; test added | Only child-to-parent `parent_ids` is stored; `parent-cycle` and `parent-cardinality` work but had no committed test |
| DOC-10 | KEEP | Generated surfaces carry a marker and pass the renderer drift check |
| DOC-11 | KEEP | Every template is registered and its placeholders checked; the 29 templates pass a fill-and-check probe in Registry order |
| DOC-12 | KEEP; renumbering held | `reserved_history` and `high_water` block reuse. Path number equals the `artifact_id` number, so any renumbering is a Q-07 decision and is not made here |
| SUP-11 | KEEP | Terminal Task bodies are exempt from rewriting; corrections are added as new sections |

### W03 changes 2026-11-11

- DOC-04: `registry.py` no longer converts YAML dates before the schema
  check, so an unquoted date fails the string type. No tracked document
  used one.
- DOC-05 and DOC-01: the Registry sets `ordered_sections` and
  `nonempty_sections` on the 22 remaining sectioned profiles, and
  `ordered_sections` only on `research-member`, whose Stage 90 members keep
  their empty parent headings. The `generated` profile stays with its
  producer. Current documents migrated: 13 package READMEs move
  `Related Documents` to the end, and `docs/README.md` and
  `scripts/README.md` lose one empty heading each. No heading is renamed.
- Review answer `aa1bde154`: nine moved READMEs lost a stray trailing
  `---`; the Ollama README also moves `Related Documents` last; the
  declaration test now covers free-form profiles, so `research-member`
  ordering is tested; the swap test handles a last second section.
- Tests: an unquoted-date rejection, a Registry rule that every sectioned
  profile declares order and content, a swapped and an emptied section per
  representative profile, and a parent cycle and a two-parent Plan.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W03 obligation assessment | 111 | W116 | template-contract-assessment | DOC-01 to DOC-12 and SUP-11 | NOT_RUN | Assessment not yet run | required | - |
| W03 obligation assessment result | 111 | W116 | template-contract-assessment | DOC-01 to DOC-12 and SUP-11 at `95a65be6d` | PASS | Per-ID table above: DOC-04 and DOC-05 GAP changed, DOC-01 changed in part, DOC-08 DEFER, DOC-07 Vault N/A, rest KEEP | required | W03 obligation assessment |
| W03 section and date RED | 111 | W116 | red-green-proof | New tests against the pre-change Registry and `_json_schema_value` | FAIL | Unquoted-date test failed; order and content tests failed for 28 profile cases with the Registry at `95a65be6d` | required | - |
| W03 section and date GREEN | 111 | W116 | red-green-proof | Commits `ce18338c8` and `85ed595b3` | PASS | test_registry 123 OK; test_heading, test_profile, test_language 110 OK; test_lifecycle 7 OK; metadata check-active selected534 violations0, check-changed selected16 violations0; links alignment and language PASS; renderer drift 0; script manifest PASS | required | W03 section and date RED |
| W03 code review | 111 | W116 | independent-source-review | Fresh-context code-reviewer of `ce18338c8` and `85ed595b3` | PASS | APPROVED: no false finding or exception from date objects; README content preserved; tests not vacuous. Four minor findings answered in `aa1bde154`; removing `research-member` ordering now fails the declaration test | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 111 | pending | - | - | SPEC-0212 TSK-0058 |

## Review and Completion

In progress. The assessment and the reproduced-gap changes are recorded.
Criterion 111 waits for the owner. Open: a fixed service-README section set
(DOC-01) needs an owner decision on a new contract; validator work beyond
these profile flags is handed to W05; renumbering stays a Q-07 decision.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W02 Task](tsk-0057-w02-archive-and-safe-removal.md)
