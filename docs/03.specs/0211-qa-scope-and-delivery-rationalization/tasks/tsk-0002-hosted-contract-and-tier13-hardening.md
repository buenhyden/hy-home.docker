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
This is local source and unit evidence. Document minimum and independent review
passed on the frozen input. Optional
native Compose cases and every HOME operation remain NOT_RUN; a skipped native
case is not promoted to PASS by this Task.

The first actual hosted candidate at
`f1f45648ac18f9b08423e385afe94bbff7a60074` failed in run `38773315753`, job
`116554471043`: 955 tests passed, 79 skipped and one OpenBao preflight test
errored because its positive fixture inherited the hosted runner GID instead
of fixing the required GID 1000. Production still rejects every other GID.
The test-only follow-up at `e459c4ec1aaf652ad26d17e67daaf7ff5bb23aac`
fixes the positive fixture at GID 1000 while retaining its explicit GID 1001
rejection. The exact test passed under an outer host-GID 4242 mock, and the
complete affected module passed 34 tests.

The module run also exposed local checkout metadata drift on its three pinned
public dependencies. In the repository, SPEC-0204 and SPEC-0211 worktrees,
only `protected-maintenance.py`, `protected-snapshot-archive.py` and
`protected-semantic-execution.py` changed from mode 0664 to their tracked mode
0644. All nine files remained regular, non-symlink, UID 1000 files with their
expected Git blobs and SHA-256 values unchanged. This was a checkout metadata
correction, not a source or HOME runtime change.

Hosted retry run `38774555839`, job `116558702899` then passed all 955 tests
with the same 79 declared runtime skips, but the adapter correctly rejected the
receipt set. `ArtifactRehearsalTests` in the required Restic module contributed
four skips without appearing in the closed optional-class list. One already
allowed OpenBao native method also rendered unittest's two-line
`shortDescription` receipt, so the same-line parser counted only 78 of 79
skips. Focused routing and native-shaped parser regressions failed before the
sources changed. The follow-up registers exactly the Restic class, keeps the
module required, and admits only an immediate two-line description/status
receipt while preserving summary-count, duplicate, unknown-class, malformed
and missing-status rejection. It also replaces two unrelated optional-class
count assertions with selector uniqueness and exact module exclusion. The
affected batch passed 121 tests, the Restic adapter route passed five tests
with four declared skips, and the typed workflow checker passed. No Restic or
OpenBao native rehearsal ran. The next exact-head hosted candidate remains
NOT_RUN at this receipt boundary.

The first actual local changed-profile run on the staged follow-up reached the
local document metadata leaf and failed one of 151 tests after 767.606 seconds.
The canonical governance-policy registry and approval-boundaries body require
`Verification`, while the test's expected tuple and synthetic valid body were
stale. The test-only correction adds that heading to both expectations and
proves that omitting only `Verification` is rejected. The exact focused test
passed, independent review found no validator weakening, and the full metadata
batch passed 151 tests in 796.977 seconds. A final actual changed-profile run
then reached the full document-governance batch. That batch failed one of 772
tests after 1122.705 seconds because an architecture CLI fixture used
`retired`, which is not in the live architecture-decision lifecycle, so input
validation masked the intended ineffective-successor finding. The same run
also exposed that the test-owned subprocess removed `HYHOME_CI_GATE_ROOT` but
retained the gate-only `PYTHONPATH` bootstrap that requires it. The test-only
correction uses the admitted but ineffective `proposed` status and removes
`PYTHONPATH` only when it removed an inherited gate root. The exact method
passed normally and under a gate-bootstrap replica, and the complete
architecture module passed 13 tests in 6.836 seconds. A final actual
changed-profile rerun on staged tree
`863ec351291c064cd3f481ffa7f9f56290d459b0` stopped at changed-metadata
validation before the long suites because the new architecture GREEN evidence
row used a different Check label from the FAIL row it resolved. The receipt now
uses the same Check and Work Unit on both rows, and the canonical Stage 03
loader passed all 36 packages. The next actual changed-profile run on staged
tree `1e64f66a8f2bb394b62cddd4a27ec327ba447840` passed the metadata batch
(151 tests in 803.796 seconds) and the full document-governance batch (772
tests in 1230.038 seconds), then found three stale approval expectations in
the 265-test supply-chain fixture-policy leaf after 109.778 seconds. Commit
`a5972f973f9afa8f692b66093b0ac06c09123f36` records the owner's approval for
one Grype DB update while keeping Scorecard unapproved, but the tests still
required both exact markers to be absent. The test-only correction binds the
tracked Grype marker exactly once, retains Scorecard absence, and exercises
both missing-marker paths without policy, Docker or network execution. The
exact nine-module leaf passed all 265 tests in 108.132 seconds. A final actual
changed-profile run on staged tree
`5d45abff5d78a55230172ac24f79ddd7259f56ff` passed the metadata batch (151
tests in 756.986 seconds), full document-governance batch (772 tests in
1123.683 seconds), supply-chain fixture-policy leaf (265 tests in 106.107
seconds), all 66 declared Compose selections covering 316 services, and the
364-, 69- and 18-case Conftest batches. It then exited 254 in the promoted
compose-baseline leaf because checkout metadata had restored group write on
two OpenBao public sources. After aligning only
`protected-raft-snapshot.py` and `protected-snapshot-custody.py` from mode
0664 to tracked mode 0644, the exact two affected modules passed 53 tests.
The complete leaf then exposed the same checkout-only drift on the OpenWebUI
entrypoint. That file changed from mode 0775 to tracked mode 0755. All three
files remained regular, non-symlink, UID 1000 files with their Git blobs and
SHA-256 content unchanged. The only other executable permission guard in the
leaf, Gatus, was already at tracked mode 0755. With those checkout corrections,
the authenticated registered compose-baseline leaf passed all 955 tests in
113.207 seconds with 78 declared native skips. The full changed-profile result
remains FAIL rather than being promoted from this narrower recovery proof.

Frozen implementation SHA-256 values before document-only result updates are:

| Path | SHA-256 |
| --- | --- |
| `.github/workflow-contract.yml` | `c55ab52e92a367d23d89c344ac8dba055ea82c6274aaa6dbc990f27d3a936f3f` |
| `.github/workflows/ci-quality.yml` | `4e12ef9e82a46e52564404e84c3004c889afcd8fb1c32e1434acb48d7152120e` |
| `scripts/lib/gate/ci_gate_contract.py` | `bef405da70edfc27129a9a37acd78dc355c26ab8214fc0c9b8a2e98acfc045c7` |
| `scripts/lib/gate/ci_gate_adapters.py` | `1d4632e7a62dfd87ecf27f50ecc063663c0dfd56943b2cc4ba20e230f0b22380` |
| `scripts/lib/gate/github_workflow_contract.py` | `4a4f62849f5666de54dbedf193252feec2fa9c5a0e71b05113019e126e83f90f` |
| `scripts/validation/ci_gate_runner.py` | `7d43292a5d2909415b8aafc89a91ac0846f67a794711898caae5b3d0be617e47` |
| `scripts/hardening/check-all-hardening.sh` | `8ffb28b04a18415cef3cf59cadf17d93bcb497d55847971b910f15c2d4485319` |
| `tests/lib/gate/test_ci_gate_contract.py` | `746eedef3fb9dab4703c4ad0b10a29e0e7be2ea8e7ae0c0d96593233a2075e8c` |
| `tests/lib/gate/test_ci_gate_adapters.py` | `394aa793954685ea95e7e8d8c107cc0d90fe761bdf7526ad645a1c499aa6dd7d` |
| `tests/lib/gate/test_github_workflow_contract.py` | `2b7e940ab936703dee4c38ae8af26c59b4c057899e8a290f49c14b2ec4248288` |
| `tests/validation/test_ci_gate_execution_context.py` | `4eacd89b4955ec57328d69d5cf9fa22c62ff78d726434180aac76e34c493c906` |
| `tests/validation/test_ci_gate_model.py` | `69a7f5c2d39c1c1f9d1eca6160737ce16c25ebc298ffe3e3df292b183cdc718c` |
| `tests/validation/test_ci_gate_plan.py` | `bf2f38719dd9280b4346cec67c58d933c23b87ce070da82e18f7b5ecb94fa214` |
| `tests/validation/test_infra_tier_layout.py` | `2858cbd2a182f67370ba60bebd33dee13ce2a53114316804f6f91c61cd5ee3a9` |
| `tests/validation/test_smtp_ci_routing.py` | `eeb2934205bdbe164984727303d26b37f3a7578361b87a1adcf453e37b47f4c3` |
| `tests/validation/test_sec01_ci_routing.py` | `da85de0ed0e3b236080583fad89c85ef64bdf2889f034892d772fa8da2f92ac0` |
| `tests/validation/test_openbao_protected_semantic_restore.py` | `5c87d0cc8a2301105c5261df5548e6be9746bfbb54e206aeab3136857a213a57` |
| `tests/lib/document_governance/metadata/test_profile.py` | `d8e1d8952548ae41faa7e580dad6f983901f81e1d7c9a68ec3a3c2af2256f0f9` |
| `tests/lib/document_governance/test_architecture.py` | `1de841e550931828a1a5d7fad73b3e415f2937bbb59de7ad88b5d1fcb35a2665` |
| `tests/lib/supply_chain/test_grype_db_seed.py` | `1585f6863fa213e00c254d2038aa300819097befe6185503094888514062eafe` |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hosted ownership RED | 2, 3 | W70 | Hosted deterministic regression ownership | Three promoted gate IDs on the source baseline | FAIL | Focused contract and plan tests | required | - |
| Tier 13 routing RED | 5 | W70 | Explicit `13-experience` hardening behavior | Pre-change hardening dispatcher | FAIL | Tier-layout regression | required | - |
| Hosted ownership GREEN | 2, 3 | W70 | Hosted deterministic regression ownership | Frozen implementation hashes above | PASS | Exact eight-module batch; 198 tests in 33.620 seconds | required | Hosted ownership RED |
| Candidate context GREEN | 2, 3 | W70 | Pre-install PR identity, raw merge topology and trusted Git binding | Frozen implementation hashes above | PASS | Real merge, replacement-ref, hostile-PATH and poisoned-environment behavior tests in the exact batch | required | - |
| Tier 13 routing GREEN | 5 | W70 | Explicit `13-experience` hardening behavior | Frozen implementation hashes above | PASS | Exact eight-module batch; 198 tests in 33.620 seconds | required | Tier 13 routing RED |
| Compatibility source GREEN | 2, 3, 5 | W70 | Workflow contract, CI model, SMTP routing and tier layout | Frozen implementation hashes above | PASS | Exact eight-module batch; 198 tests in 33.620 seconds | required | - |
| First hosted candidate RED | 2, 3 | W70 | Actual PR candidate | `f1f45648ac18f9b08423e385afe94bbff7a60074` | FAIL | Run 38773315753, job 116554471043; 955 passed, 79 skipped, one host-GID-dependent fixture error | required | - |
| OpenBao fixture GREEN | 2, 3 | W70 | Positive preflight fixture is independent of host GID and retains non-1000 rejection | `e459c4ec1aaf652ad26d17e67daaf7ff5bb23aac`; test hash above | PASS | Outer GID 4242 exact method; complete affected module 34 tests | required | - |
| Hosted retry | 2, 3 | W70 | Actual PR candidate | `e459c4ec1aaf652ad26d17e67daaf7ff5bb23aac` | FAIL | Run 38774555839, job 116558702899; 955 passed, 79 skipped, exact skip-set mismatch | required | - |
| Restic skip route RED | 2, 3 | W70 | Exact Restic optional skip route | Required Restic module without its native class declaration | FAIL | Focused security CI-routing regression | required | - |
| Restic skip route GREEN | 2, 3 | W70 | Exact Restic optional skip route | Frozen contract and routing-test hashes above | PASS | Focused batch 74 tests; exact adapter route 5 tests with 4 declared skips; typed workflow checker | required | Restic skip route RED |
| Multiline skip receipt RED | 2, 3 | W70 | Exact unittest two-line skip receipt | Native-shaped header, description and skipped status | FAIL | Focused adapter behavior regression | required | - |
| Multiline skip receipt GREEN | 2, 3 | W70 | Exact unittest two-line skip receipt | Frozen adapter and adapter-test hashes above | PASS | Affected batch 121 tests including unknown, duplicate, malformed and missing-status negatives | required | Multiline skip receipt RED |
| Governance profile baseline RED | 2, 3 | W70 | Governance-policy required-heading contract | Canonical registry/body plus stale test expectation | FAIL | Actual changed-profile; metadata batch 150 passed, 1 failed in 767.606 seconds | required | - |
| Governance profile baseline GREEN | 2, 3 | W70 | Governance-policy required-heading contract | Frozen metadata-test hash above | PASS | Exact focused test; complete metadata batch 151 tests in 796.977 seconds | required | Governance profile baseline RED |
| Architecture CLI baseline RED | 2, 3 | W70 | Ineffective supersession CLI and test-owned child isolation | Staged tree `e84ec9dfcb3cbf9a5261c94071d27ef580009678` | FAIL | Actual changed-profile; full document-governance batch 771 passed, 1 failed in 1122.705 seconds | required | - |
| Architecture CLI baseline GREEN | 2, 3 | W70 | Ineffective supersession CLI and test-owned child isolation | Frozen architecture-test hash above | PASS | Exact method in ordinary and gate-bootstrap-replica environments; complete architecture module 13 tests in 6.836 seconds | required | Architecture CLI baseline RED |
| Task receipt schema RED | 2, 3 | W70 | Task evidence resolution contract | Staged tree `863ec351291c064cd3f481ffa7f9f56290d459b0` | FAIL | Actual changed-profile stopped at changed metadata because Resolves did not use the same Check label | required | - |
| Task receipt schema GREEN | 2, 3 | W70 | Task evidence resolution contract | Same Check and Work Unit on both evidence rows | PASS | Canonical Stage 03 loader; 36 packages | required | Task receipt schema RED |
| Supply-chain approval baseline RED | 2, 3 | W70 | Supply-chain approval behavior contract | Staged tree `1e64f66a8f2bb394b62cddd4a27ec327ba447840` | FAIL | Actual changed-profile; supply-chain fixture-policy leaf 262 passed, 3 failed in 109.778 seconds | required | - |
| Supply-chain approval baseline GREEN | 2, 3 | W70 | Supply-chain approval behavior contract | Frozen approval-test hash above | PASS | Exact nine-module supply-chain fixture-policy leaf; 265 tests in 108.132 seconds | required | Supply-chain approval baseline RED |
| Checkout mode baseline RED | 2, 3 | W70 | Checkout mode alignment for promoted compose baseline | Staged tree `5d45abff5d78a55230172ac24f79ddd7259f56ff`; group-writable OpenBao public sources | FAIL | Actual changed-profile exited 254 after metadata 151, document governance 772, supply chain 265, Compose 66 selections/316 services and Conftest 364/69/18 passed | required | - |
| Checkout mode baseline GREEN | 2, 3 | W70 | Checkout mode alignment for promoted compose baseline | Same Git blobs and SHA-256 content; only 0664 to 0644 and 0775 to 0755 checkout mode corrections | PASS | Exact OpenBao modules 53 tests; authenticated registered compose-baseline leaf 955 tests in 113.207 seconds with 78 declared skips | required | Checkout mode baseline RED |
| Final local changed profile | 2, 3, 5 | W70 | Actual default changed-profile execution | Staged tree `5d45abff5d78a55230172ac24f79ddd7259f56ff` before checkout mode correction | FAIL | Exit 254 in promoted compose-baseline leaf after all earlier selected leaves above passed; recovered by the narrower exact-leaf proof | required | - |
| Final local changed profile recovery | 2, 3, 5 | W70 | Actual default changed-profile execution | Frozen staged tree `9db843aa3de4322fb8c8b73112a47ce95eedf78b` with checkout modes aligned to tracked metadata | PASS | `run-ci-gate.py --profile changed` exited 0; repository-integrity 591 tests passed in 210.731 seconds after Compose 66 selections/316 services and the selected contract batches passed | required | Final local changed profile |
| Node prerequisite routing RED | 2, 3 | W70 | Selected Node prerequisites for promoted regression leaves | Registered `leaf.compose-baseline-regressions` and `leaf.repository-integrity-regressions`; infra-only Compose selector | FAIL | Two focused methods produced three exact false-negative assertions; independent model receipt `30474f6616fd6f9513321e3a5a0969e17811017b28d593bd311863e703434af6` | required | - |
| Node prerequisite routing GREEN | 2, 3 | W70 | Selected Node prerequisites for promoted regression leaves | Runner `bb2a2720cdb94918bef5c080e5659a11cef35c610b3168e7f492830800d3c267`; plan test `ec642a47f1a1e6342f91f30e9ac1458859b40138d750507e2085c748dc3d2d2a` | PASS | Focused two-method batch and complete runner/execution-context batch passed; independent security review approved the exact two-ID change | required | Node prerequisite routing RED |
| Final hosted candidate | 2, 3 | W70 | Actual PR candidate | Final receipt commit not yet created | NOT_RUN | A new exact-head hosted run is required | required | - |
| Final hosted candidate recovery | 2, 3 | W70 | Actual PR candidate | PR 505 head `9bf618a80d192d974d494b164b8af4df07dfb6ae`; run 38826848451, job 116736189044 | PASS | Required App 15368 `candidate-quality` passed in 12 minutes 16 seconds; CodeQL and GitGuardian passed; protected PR merged as main `2de045e3b6f79967b4b4050e5cff53ee0b38158f` | required | Final hosted candidate |
| Merged main security | 3, 5 | W70 | Actual merged-main security | Main `2de045e3b6f79967b4b4050e5cff53ee0b38158f`; run 38828232689, job 116740637022 | PASS | Audit merged workflow revision and SARIF upload steps passed; candidate PR job was skipped on push by design | optional | - |
| Remote protection observation | 3 | W70 | Read-only main protection, effective rules and latest successful candidate App identity | Current remote main; run 38695709347 | FAIL | Required contexts/checks empty; App 15368 observed; no mutation | optional | - |
| Remote protection recovery observation | 3 | W70 | Read-only main protection, effective rules and latest successful candidate App identity | Separately approved main setting change recorded on current `origin/main`; independent API read-back | PASS | Strict required `candidate-quality` is bound to App 15368; PR 505 head `e459c4ec1aaf652ad26d17e67daaf7ff5bb23aac` remained `BLOCKED` on its failed current-head check; no mutation by this Task | optional | Remote protection observation |
| Remote protection matching-success observation | 3 | W70 | Read-only main protection, effective rules and latest successful candidate App identity | PR 506 head `2fbcf8982945d6e8d3666e6940e3accde728c768`; main `89eb43f683a11587cf4f125be534ae720c20a55c` | PASS | App 15368 `candidate-quality` succeeded on the exact head and the protected PR merged; receipt SHA-256 `09a65fe2baf67725c2b4d781ed69007ef9b3a40d6c907224af809c3309ab51e6` | optional | - |

## Criterion Acceptance

This support Task owns no acceptance decision. TSK-0001 remains the unique
current owner of criteria 2, 3 and 5.

## Review and Completion

The source correction, independent review, exact-head hosted retry, protected
merge and merged-main security run are complete. The original Task retains
every SPEC-0211 criterion decision. The current required check was applied
under a separate approved setting change recorded on main; this Task performed
no remote protection mutation.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Earlier QA rationalization evidence](tsk-0001-qa-scope-and-delivery-rationalization.md)
- [Quality standards](../../../../.agents/governance/quality-standards.md)
