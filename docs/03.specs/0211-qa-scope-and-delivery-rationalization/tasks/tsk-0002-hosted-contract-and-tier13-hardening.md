---
title: "Hosted Contract and Tier 13 Hardening"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0211-TSK-0002"
parent_ids:
- "SPEC-0211-PLAN-0001"
created: "2026-10-16"
---

# Hosted Contract and Tier 13 Hardening

## Overview

### Objective

Support the existing SPEC-0211 criteria by closing the hosted changed-selection
gap for deterministic CI, Compose and
repository contract regressions, and make the unified hardening route cover
`infra/13-experience`. Preserve local-only ownership for document-library,
mocked native, HOME-dependent and other isolated implementation checks.
This support Task owns no additional Spec criterion or acceptance decision.

## Inputs and Authorization

The current user request on 2026-10-16 authorizes this source-only correction
and its focused tests. The implementation unit starts from `origin/main`
`e6807a7d16d8b9e180ff58456ab64e4ee721ca69` in branch
`feature/spec-0211-infra-gates`. It authorizes no deployment, release, secret,
credential, HOME runtime, branch-protection or other remote mutation.

Read-only branch-protection observation found strict mode and administrator
enforcement enabled but no required status contexts or checks. This is a
confirmed delivery risk, not authorization to change protection. The candidate
workflow remains the source-level execution owner until a separate remote
protection change is reviewed and approved.

The latest successful PR observation binds `candidate-quality` metadata to
GitHub Actions App ID 15368 on one past SHA. The tracked protection record and
RUN-0009 now hold the minimal required-check PATCH proposal, current empty-check
rollback, configuration read-back, and missing/failed/stale/wrong-App/matching
enforcement rehearsal steps. They were prepared only; no PATCH or enforcement
case ran, and the wrong-App input remains unavailable.

## Work Log

### W70 Focused RED

Removing the three deterministic leaves from `local_only_gate_ids` exposed two
closed-contract assumptions: the parser required every registered unittest
leaf to remain local-only, and the runner admitted `run-unittest` only in the
local context. Focused contract and execution-plan tests failed before those
owners changed. The new tier 13 behavior test also failed because the hardening
script rejected `13-experience` as an unknown tier. These failures reproduce
the missing hosted execution and missing hardening route rather than changing
expectations after implementation.

### W70 Minimal Implementation

The workflow contract promotes exactly these leaves:

- `leaf.ci-gate-contract-regressions`
- `leaf.compose-baseline-regressions`
- `leaf.repository-integrity-regressions`

The contract parser requires that exact closed set to be registered and absent
from local-only ownership, while every other registered unittest leaf remains
local-only. The runner admits hosted unittest execution only when the gate ID
belongs to that set and the existing unittest argv grammar accepts it. Changed
path tests cover the workflow contract, root Compose, Airflow SQL and n8n
workflow inputs in both the normal local changed plan and hosted PR plan, with
each promoted leaf selected exactly once. The `--local-only` plan retains only
the complementary unit lane. A behavior test injects a nonzero promoted-leaf
result and proves the candidate executor stops with the same result.

The workflow captures the immutable GitHub event and merge SHA, ordered raw
merge parents, absolute system Git executable and configured Python interpreter
before dependency installation through the fixed system Bash path.
The runner authenticates that capture before loading the candidate contract,
disables replacement refs and inherited Git configuration, and uses the same
captured executable for hosted changed-path selection. A real temporary
two-parent merge proves the positive `--requirements` route; poisoned custom
event, base/head/merge identity and hostile PATH cases fail closed before
selection or keep using the captured system Git.
The captured Python path prevents later PATH redirection but does not make the
candidate checkout, installed dependencies or interpreter files immutable;
independent review and the actual hosted candidate remain required evidence.

Two stale count assertions now check semantics: optional changed roots compare
with the contract-owned registry, and SMTP optional selectors must be children
of a required module. They no longer encode incidental list lengths.

The unified hardening script now registers and runs `13-experience` in explicit,
alias and no-argument full routes. It checks the Storybook and Storybook MCP
gateway chains, intended networks, healthchecks and absence of published host
ports. The regression mutates the SSO chain and removes the tier Compose file
to prove explicit and full-route failures.

### W70 Focused GREEN and Remaining Boundary

The exact eight-module source batch passed 198 tests in 33.620 seconds:

```text
tests.lib.gate.test_ci_gate_contract
tests.lib.gate.test_ci_gate_adapters
tests.lib.gate.test_github_workflow_contract
tests.validation.test_ci_gate_execution_context
tests.validation.test_ci_gate_model
tests.validation.test_ci_gate_plan
tests.validation.test_smtp_ci_routing
tests.validation.test_infra_tier_layout
```

The typed workflow checker and tier 13 hardening command passed.
This is local source and unit evidence. Document minimum, independent review
and actual hosted candidate remain required on the frozen input. Optional
native Compose cases and every HOME operation remain NOT_RUN; a skipped native
case is not promoted to PASS by this Task.

Frozen implementation SHA-256 values before document-only result updates are:

| Path | SHA-256 |
| --- | --- |
| `.github/workflow-contract.yml` | `8b5df08b38b979e39ecbe1753fff5ceddf2122d6262269976b97368b18e4ffe0` |
| `.github/workflows/ci-quality.yml` | `4e12ef9e82a46e52564404e84c3004c889afcd8fb1c32e1434acb48d7152120e` |
| `scripts/lib/gate/ci_gate_contract.py` | `bef405da70edfc27129a9a37acd78dc355c26ab8214fc0c9b8a2e98acfc045c7` |
| `scripts/lib/gate/github_workflow_contract.py` | `4a4f62849f5666de54dbedf193252feec2fa9c5a0e71b05113019e126e83f90f` |
| `scripts/validation/ci_gate_runner.py` | `7d43292a5d2909415b8aafc89a91ac0846f67a794711898caae5b3d0be617e47` |
| `scripts/hardening/check-all-hardening.sh` | `8ffb28b04a18415cef3cf59cadf17d93bcb497d55847971b910f15c2d4485319` |
| `tests/lib/gate/test_ci_gate_contract.py` | `746eedef3fb9dab4703c4ad0b10a29e0e7be2ea8e7ae0c0d96593233a2075e8c` |
| `tests/lib/gate/test_github_workflow_contract.py` | `873fa98ac0227cbcff2bd895540f95277f31be7dfceda49fd83c3afc7b45b91a` |
| `tests/validation/test_ci_gate_execution_context.py` | `4eacd89b4955ec57328d69d5cf9fa22c62ff78d726434180aac76e34c493c906` |
| `tests/validation/test_ci_gate_model.py` | `69a7f5c2d39c1c1f9d1eca6160737ce16c25ebc298ffe3e3df292b183cdc718c` |
| `tests/validation/test_ci_gate_plan.py` | `bf2f38719dd9280b4346cec67c58d933c23b87ce070da82e18f7b5ecb94fa214` |
| `tests/validation/test_infra_tier_layout.py` | `2858cbd2a182f67370ba60bebd33dee13ce2a53114316804f6f91c61cd5ee3a9` |
| `tests/validation/test_smtp_ci_routing.py` | `eeb2934205bdbe164984727303d26b37f3a7578361b87a1adcf453e37b47f4c3` |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hosted ownership RED | 2, 3 | W70 | Hosted deterministic regression ownership | Three promoted gate IDs on the source baseline | FAIL | Focused contract and plan tests | required | - |
| Tier 13 routing RED | 5 | W70 | Explicit `13-experience` hardening behavior | Pre-change hardening dispatcher | FAIL | Tier-layout regression | required | - |
| Hosted ownership GREEN | 2, 3 | W70 | Hosted deterministic regression ownership | Frozen implementation hashes above | PASS | Exact eight-module batch; 198 tests in 33.620 seconds | required | Hosted ownership RED |
| Candidate context GREEN | 2, 3 | W70 | Pre-install PR identity, raw merge topology and trusted Git binding | Frozen implementation hashes above | PASS | Real merge, replacement-ref, hostile-PATH and poisoned-environment behavior tests in the exact batch | required | - |
| Tier 13 routing GREEN | 5 | W70 | Explicit `13-experience` hardening behavior | Frozen implementation hashes above | PASS | Exact eight-module batch; 198 tests in 33.620 seconds | required | Tier 13 routing RED |
| Compatibility source GREEN | 2, 3, 5 | W70 | Workflow contract, CI model, SMTP routing and tier layout | Frozen implementation hashes above | PASS | Exact eight-module batch; 198 tests in 33.620 seconds | required | - |
| Remote protection observation | 3 | W70 | Read-only main protection, effective rules and latest successful candidate App identity | Current remote main; run 38695709347 | FAIL | Required contexts/checks empty; App 15368 observed; no mutation | optional | - |

## Criterion Acceptance

This support Task owns no acceptance decision. TSK-0001 remains the unique
current owner of criteria 2, 3 and 5.

## Review and Completion

The source correction is implemented but the support unit is not complete.
Freeze the exact diff, run the remaining scoped checks, obtain independent
policy/security/code review, and record the hosted candidate separately. The
original Task retains every SPEC-0211 criterion decision. Do not claim branch
enforcement while required contexts remain empty, and do not change remote
protection under this Task's authorization.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Earlier QA rationalization evidence](tsk-0001-qa-scope-and-delivery-rationalization.md)
- [Quality standards](../../../../.agents/governance/quality-standards.md)
