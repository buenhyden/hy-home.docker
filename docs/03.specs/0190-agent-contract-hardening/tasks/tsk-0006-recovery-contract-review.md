---
title: "Read-Only Recovery Contract Review"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0006"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Read-Only Recovery Contract Review

## Objective

Implement Plan W6: add an explicitly invoked read-only recovery-readiness
review with one canonical owner, bounded role routing and native projections.
This reviews a sanitized contract; it never executes or approves a restore.

## Inputs

- [Approved Spec](../spec.md) and [approved Plan](../plan.md); W5 `c2bad7a6e`.
- Existing user approval covers local implementation, tests, independent review
  and logical commits. No installation, paid/native call, remote or runtime action.
- Primary writer: skill-creator; native contributor: hook-developer;
  independent reviewers: iac-reviewer and rules-engineer. Root owns this Task.
- Exact source, test and generated paths are the finite W6 map in the Plan.
  Four new skill files only; no new script, framework, manifest or Codex skill copy.

## Work Log

Read-only preparation confirmed that existing registry fields, renderer and
prompt ROUTES support the addition. Existing resource validation admits the
reference and verdict asset when directly linked from the skill body.
W5 released shared-test ownership after its reviewed logical commit.

## Verification Evidence

- P focused RED: two methods, exit 1, 0.749s; missing skill produced one
  expected error and one expected failure. Focused GREEN: 2/2, exit 0, 1.215s.
- Route RED: 6 tests, four expected missing-route failures, 0.546s. Independent
  review then found an implementation-request collision; witnessed one RED
  before narrowing the keywords. Final route 6/6, independent 0.765s.
- Final registered sanitized adapters: G 53/53 in 81.148s; P 57/57 in 53.597s;
  H 47/47 in 18.823s; all exit 0.
- Repository contract C: failures=0. Renderer write/check/write/check: exit 0,
  two providers, drift=0; canonical source hashes preserved and second generated
  bytes unchanged. Active-state final renderer check: drift=0.
- System skill-creator quick_validate, dispatcher Bash syntax, git diff --check:
  exit 0. Existing executable modes preserved.
- Exactly four new canonical files and nine generated files: one Claude skill,
  four Claude roles, four Codex roles. No README drift or Codex skill copy.
- Only iac-reviewer gains the new explicit-only skill; role IDs, provider
  model/effort, permission/tool profiles and needs_revalidation remain unchanged.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R01/R28/R35 | W6 | Role routing and independence PASS | Four canonical role deltas and retained domain owners |
| R02/R24/R27/R36 | W6 | New skill, two resources, invocation and missing-reference tests PASS; W9 evaluation pending | Recovery skill and three routing skills |
| R05/R29/R37 | W6 | Static native mapping/projection PASS; live invocation NOT_OBSERVED | Registry, renderer and narrow prompt route |

Retained domain responsibility: infra-implementer owns Compose/network/data
implementation; iac-reviewer owns independent IaC/recovery review;
security-auditor owns secret/access review; drift-detector owns runtime
observation; incident-responder owns approved incident actions; qa-engineer
and ci-cd-engineer own tests/gates; doc-writer owns runbooks; hook-developer
owns provider implementation; skill-creator owns canonical skills;
rules-engineer reviews policy and workflow-supervisor routes work. Human
operational approval remains separate. No retained role loses unique duties.

## Review Evidence

Independent IaC review CLEAR after focused corrections: three distinct owners,
separate operational approval boundary, per-evidence source/time, backup artifact
identity/integrity/freshness/prior restoreability, and historical evidence
separated from this review's invariant operational NOT_RUN. Independent native
route review CLEAR; policy/source/generated projection review CLEAR.

Static forward probes F1-F11: volume-only, missing key custody, contradictory
order/version, operational request, missing contract, self-approval, objectives
masquerading as observations, secret payload and missing capacity/isolation
were BLOCKED or stopped. Complete sanitized contracts and provable rebuild
could yield READY_FOR_SEPARATE_RECOVERY_APPROVAL. Provider-native invocation
remained NOT_OBSERVED; current operational action remained NOT_RUN. These are
independent static behavioral probes, not a native or operational experiment.
No upstream persona, installer, tool grant or automatic deployment was copied.

## Commit Ledger

Task: draft `d0adf1b64`, ready `ebe2da394`, in-progress `a9726ce4d`.
Skill: draft `2efc0060a`, review `32ff793cf`, active `00644a8f4`; each promotion
passed metadata against its actual predecessor with zero overrides.
The remaining reviewed connections, projections and receipt form the final
W6 logical commit, whose hash is owned by Git.

## Rulings

- Apply the installed system skill-creator procedure within the approved exact
  four-file design; do not create initializer extras or generic UI metadata.
- Only iac-reviewer gains the new read-only skill. Other roles/skills route to it.
- Register SKILL.md and agents/openai.yaml; resources remain skill-owned.
- New tracked resources and the generated Claude skill must be staged before
  fixture tests whose safe copier uses git ls-files. Root controls the index.
- Preserve model, reasoning and needs_revalidation facts. W9 owns thresholds
  after its fixture exists and the user-directed evaluation migration.

## Deferred Items

W9 owns recovery evaluation scenarios. W10 owns full branch and live/native
acceptance; static routing and generated parity cannot close those observations.
