---
profile_id: task
status: completed
artifact_id: task-0153-0004
artifact_type: task
parent_ids:
  - SPEC-0153
  - plan-0153
created: 2026-08-21
updated: 2026-08-22
completed_at: 2026-08-22
---

# Task 0004: Stage 00

## Objective

Converge Stage 00 and provider surfaces on Claude and Codex while removing Gemini, Antigravity, and project memory.

## Inputs

- [Specification](../spec.md)
- [Implementation Plan](../plan.md)
- [Migration 0003](../../../98.archive/migrations/mig-0003-workspace-governance-simplification.md)
- Task 3 canonical package, Stage 99 governance profiles, approved Migration owner_task 4 rows.

## Work Log

| Event | Actual result |
| :--- | :--- |
| Boundary freeze | `owner_task: 4` is exactly rows `r0004` through `r0131`: 128 rows, 81 native renames, 47 deletes, and 1,134 declared active-consumer edges. All sources were tracked before execution. |
| RED | The initial target test failed because `load_agent_governance` did not exist. The four focused modules then produced 20 tests with 1 pass, 11 failures, and 8 errors on the old three-provider, extra-root, handoff, generated-authority, and projection assumptions. |
| Native moves | Executed one `git mv` for each of the 81 registered rename rows; no recursive unregistered path was moved. |
| Registered deletes | Deleted all 47 registered sources only after their durable facts were routed or classified obsolete. The set includes Gemini/Antigravity authority, project memory, superseded Stage 00 contracts, compatibility overlays, and two retired governance templates. |
| Consumer rewrite | Rebased 677 registered literals across 226 files, corrected 41 Markdown links, and replaced 102 consumers of deleted authority with current Stage 00, Stage 99, or active Task evidence before source deletion. |
| Contract simplification | Replaced the oversized Stage 00 validator and renderer with focused two-provider modules below 800 lines and split tests by contract, native surface, renderer, and CI routing responsibility. |
| Projection regeneration | Regenerated only registered `.agents/`, `.claude/`, and `.codex/` compatibility surfaces. The changed projection set is 41, 40, and 15 paths respectively; the retired project-memory skill projections were removed. |
| GREEN | The four focused provider modules pass 20 tests, the Stage 99 registry module passes 23 tests, and the agent-output evaluation unit module passes 38 tests: 81/81 focused unit tests. The executable runner separately validates 10/10 fixtures and 14/14 semantic regressions. |
| Fix round 1 | Preserved the staged implementation digest and completed 14 review findings as unstaged fixes: strict typed provider/workflow records, confined descriptor-safe rendering, registry-native Stage 99 consumers and body contracts, provider-neutral hooks, historical correction, durable dirty/scratch safeguards, strong hook parity, fail-closed active scans, and the exact executable Migration verifier. Final amended focused selection: 53 tests in 9.185 seconds, PASS. |
| Fix round 2 | Preserved the same staged digest and completed all eight follow-up findings as unstaged fixes: active Stage 01/02/05/pre-commit authority cleanup, identity-bound renderer cleanup, pre-write post-tool path confinement, Stage 01/02/03/05 active inventory, exact loop/layer/state typing, approval-policy body-envelope alignment, immutable provider/event commands, and layer-specific Migration negatives. Focused RED was 39 tests with 34 failures and one test-fixture error; corrected focused GREEN was 39 tests in 16.376 seconds. |
| Fix round 3 | Replaced the remaining quarantine validation-to-unlink boundary with owner-only retained quarantine and fail-closed behavior, rejected multi-link formatter targets, and replaced the blanket Stage 03 package exemption with exact path plus document-digest evidence. Exact RED: 4 tests, 5 intended failures in 0.892 seconds. Exact GREEN: the same 4 tests in 0.855 seconds; amended modules pass 33 tests in 6.143 seconds. |
| Final approval | Governance review and Python/security review both approved the complete round-3 packet at `C0/I0/M0`. The reviewed packet SHA is `10c7cd003d46a31900afc9071dab6471b730eb3c8ba4835da93af261f2edc8f3`; implementation was approved for the parent-owned logical commit. |
| Post-review evidence stability | Replaced this mutable Task's whole-file token-evidence digest with three exact, single-use removal statements while retaining whole-file digests for immutable historical evidence. Focused RED was one intended failure in 0.364 seconds; focused GREEN was 1/1 in 0.394 seconds, and the three directly affected regressions passed in 1.464 seconds. |
| Controlled closeout | The final controller gate passed 42/42 with governance repository/all failures 0, renderer 2/0, parity 13/4/8, and Migration 128/81/47/1,134. The parent then created the 386-path logical commit `6daa5e2a1713300ab0076da71ad02087da5ac126` (`refactor(governance): converge claude and codex authority`). |

### Delete-source disposition

| Retired source | Durable fact disposition before deletion |
| :--- | :--- |
| Agent catalog | Fourteen role frontmatters now own role ID, scope, tier, work profile, permission, and skill membership. Twenty-three skill frontmatters own canonical skill ID and role owner. Generated inventory is tested against these sources. |
| Provider/model contract | `providers/registry.yaml` owns exactly two providers, active model rows, lifecycle/source/status facts, work profiles, permissions, semantic events, eight control layers, four bounded loops, and value-free evidence rules. Unselected catalog rows are explicitly non-authoritative research requiring revalidation. |
| Artifact contract | `docs/99.templates/registry.json` now owns governance policy, hook-policy, role, provider, SDLC, and skill profiles. The Stage 00 validator asserts the required profile set. |
| Deferred-path contract | Its approved state was an empty exemption list. Fail-closed ownership is retained by explicit task scope, dirty-worktree preservation in approval policy, and tests that reject orphan/unowned generated files. |
| Harness map | Stage 00 README owns the compact source/adapter/validator route; provider registry owns generated roots; scripts README owns executable entry points; Task evidence owns observed results. |
| Delegation protocol | `policies/agentic.md` owns the exact envelope, shared-worktree rule, status vocabulary, retry bound, conflict stop, and evidence handoff. Role frontmatter and the provider registry own routing. |
| Historical handoff notes | Current execution state and durable facts are routed to this co-located Task, current policies, active Spec/Plan, Migration, and Git history. Reviewer dirty-state protection, ignored scratch limits, fail-closed ownership, and value-free evidence are retained in approval, agentic, environment, and task-checklist policies. Historical provider-only and progress payloads are obsolete. |
| Provider compatibility overlay | Root shims and `providers/README.md` retain provider-neutral bootstrap behavior; `providers/registry.yaml` owns the two supported adapters and generated destinations. |
| Retired governance templates | Stage 99 governance README routes authors to registry profiles and canonical sources; execution evidence uses the registered Stage 03 Task profile. |

## Verification Evidence

| Check | Command | Result |
| :--- | :--- | :--- |
| Migration row completeness | Task 4 row/source/target verifier | PASS: `rows=128 rename=81 delete=47 bad=0`; all 47 deletes and 81 native move targets are complete. |
| Provider-focused unit tests | `PYTHONPATH=. python3 -m unittest tests.validation.test_agent_governance_contract tests.validation.test_provider_native_surfaces tests.validation.test_provider_surface_renderer tests.validation.test_agent_governance_ci_routing -v` | PASS: 20/20. RED before implementation was 1 pass, 11 failures, and 8 errors. |
| Stage 99 registry tests | `PYTHONPATH=. python3 -m unittest tests.validation.test_document_registry -v` | PASS: 23/23. |
| Agent-output unit tests | `PYTHONPATH=. python3 -m unittest tests.validation.test_agent_output_eval_fixtures -v` | PASS: 38/38, including fail-closed mutation cases. |
| Provider projection parity | `bash scripts/operations/sync-provider-surfaces.sh --check` | PASS: `providers=2 drift=0`. |
| Stage 00 repository contract | `python3 scripts/validation/check-agent-governance-contract.py` | PASS: `mode=repository section=all failures=0`; contract mode also reports 14 roles, 23 skills, and two providers. |
| Agent-output evaluation | `bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions` | PASS: fixtures 10/10; semantic regressions 14/14. |
| Audit-pack coverage | `bash scripts/validation/report-audit-pack-coverage.sh` | PASS: 161/161 criterion rows and 15/15 overview categories. |
| Active stale-token scan | Registered active-authority retired-token scan | PASS: no active-authority match. The two remaining test literals are the bounded Migration target guard in `test_workspace_governance_migration.py`. |
| Retired-path scan | Scan active authority for old `rules/`, `scopes/`, agent/function roots, Stage 00 contracts, subagent protocol, and harness map | PASS: no match. |
| Syntax and style | `python3 -m py_compile ...`; `ruff check ...`; `git diff --check` | PASS. |
| Changed-document metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base 112b9f1f` | Baseline/later-task debt: 28 violations in unsupported legacy Stage 03/04 paths and four unchanged legacy exceptions; no Task 4 governance-profile deficit. |
| Initial Task 4 repository gate | `bash scripts/validation/check-repo-contracts.sh` | Before review fixes, completed in 107.7 seconds with `failures=13`, down from 19 before the initial Task 4 section fixes. Residual failures were classified for later tasks. |
| Fix-round renderer and governance | `bash scripts/operations/sync-provider-surfaces.sh --check`; `python3 scripts/validation/check-agent-governance-contract.py --mode contract`; repository/all | PASS: `providers=2 drift=0`; 14 roles, 23 skills, two providers; repository/all has zero failures. |
| Fix-round hook parity | `bash scripts/validation/report-provider-hook-parity.sh --validate-only`; `--check` | PASS: 13 dispatchers, four loops, eight workflow states; generated matrix is fresh. |
| Exact Task 4 Migration | `python3 scripts/validation/check-task4-migration.py` | PASS: 128 rows, 81 rename, 47 delete, 1,134 edges. Selection `9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1`; edges `2f1840983d98ed93ffdc183305c49b389b17e5c8362538e5df97d451be2b9139`; rows `2fd01449c78581374d37153175455ca0d08e2ca05e36812dcab8189a97208f95`. |
| Fix-round focused suites | Amended governance/renderer/registry/routing/parity/migration selection; metadata legacy-consumer selection | PASS: 53 tests in 9.185 seconds; PASS: 11 tests in 6.425 seconds. |
| Fix-round repository gate | `bash scripts/validation/check-repo-contracts.sh` | Completed in about 99 seconds, exit 1, `failures=15`. No traceback/configuration failure or Task 4 controlled-wrapper finding remains; all failures are later-task corpus/template/routing debt. |
| Fix-round-2 renderer races and post-tool confinement | Deterministic validation-to-unlink replacement, post-write managed-root symlink, absolute/traversal/noncanonical/symlink/control changed-path mutations | PASS: user replacement and outside directory/file preserved; invalid hook paths fail before formatter or other write-capable tooling. |
| Fix-round-2 active authority inventory | Governance repository/harness scan plus exact Stage 01/02/05/pre-commit raw scan | PASS: 703 text paths; Stage 01/02/03/05 and `.pre-commit-config.yaml` covered; zero active findings and no raw Stage 01/02/05/pre-commit retired-token match. |
| Fix-round-2 registry/parity typing | Unknown/corrupt state owner/return, layer owner/gate/return, loop owner/reviewer/stop/failure, and synchronized command-prefix mutations | PASS: governance and parity fail closed; current 13 dispatchers, 8 layers, 8 states, and 4 loops validate. |
| Fix-round-2 metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed --changed-path docs/00.agent-governance/policies/approval-boundaries.md` | PASS: selected 1, violations 0, legacy exceptions 0, overrides 0; bounded eight-file Stage 01/02/05/approval selection also has zero violations. |
| Fix-round-2 Migration negatives | Row identity/action/target, totals, selection digest, edge digest, and Task 4 row digest mutations | PASS with layer-specific failures; approved Migration packet and three digests unchanged. |
| Fix-round-2 focused/static gates | Same 39-test RED selection; focused Ruff, `py_compile`, `bash -n`, `git diff --check` | PASS: 39 tests in 16.376 seconds; all static gates exit zero. |
| Fix-round-3 quarantine retention | Normal stale isolation plus deterministic post-validation quarantine pathname replacement | PASS: no quarantined pathname deletion exists; normal and raced objects remain in owner-only isolation, replacement bytes survive, and the operation fails closed. |
| Fix-round-3 hard-link confinement | Post-tool payload naming a repository hard link to an outside inode | PASS: `st_nlink != 1` is rejected before write-capable tooling; outside inode bytes are identical. |
| Fix-round-3 Stage 03 evidence | Exact unchanged historical evidence, mutated evidence, and active `9999-current/spec.md` | PASS: only the exact path/digest evidence is allowed; both mutations produce `AGC-UNSUPPORTED-TOKEN`. |
| Fix-round-3 bounded gates | Renderer, governance contract/repository/inventory, focused Ruff, `py_compile`, post-tool `bash -n`, `git diff --check` | PASS: drift 0; 14 roles, 23 skills, 2 providers; repository failures 0; active paths 703; static checks exit zero. |
| Final approved local gate packet | Governance reviewer; Python exact-four and amended-module suites; renderer; governance; parity; Migration; one-file metadata; static checks | PASS: governance reviewer 41/41; Python exact 4/4 and amended modules 33/33; renderer `providers=2 drift=0`; governance failures 0; parity 13 dispatchers, 4 loops, 8 states; Migration 128 rows, 81 renames, 47 deletes, 1,134 edges; metadata selected 1 with 0 violations; Ruff, `py_compile`, bash syntax, and `git diff --check` all pass. |
| Post-review mutable-evidence regression | Exact mutable-Task mutation test; affected Stage 03/current-repository tests; governance repository/all; focused static checks | PASS: evidence-only non-token edits remain clean; new active-authority text and altered allowed statements fail; 3/3 affected regressions pass; governance failures 0; Ruff, `py_compile`, and `git diff --check` pass. |
| Controlled pre-commit and final controller gate | Controller-focused suite and Task 4 contract gates | PASS: 42/42; governance repository/all failures 0; renderer `providers=2 drift=0`; parity 13 dispatchers, 4 loops, 8 workflow states; Migration 128 rows, 81 renames, 47 deletes, 1,134 edges. |

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Independent governance review | APPROVED — `C0/I0/M0` | All 41 governance reviewer checks pass against round-3 packet SHA `10c7cd003d46a31900afc9071dab6471b730eb3c8ba4835da93af261f2edc8f3`; no Critical, Important, or Minor finding remains. |
| Independent Python/security review | APPROVED — `C0/I0/M0` | The exact four round-3 regressions and all 33 amended-module tests pass; no Critical, Important, or Minor finding remains. |
| Final governance evidence-stability review | APPROVED — `C0/I0/M0` | The 42/42 controller packet and governance repository/all result close the mutable-evidence regression with no remaining finding. |
| Final Python/security evidence-stability review | APPROVED — `C0/I0/M0` | The exact single-use statement boundary remains fail closed for unmatched authority text; no Critical, Important, or Minor finding remains. |

## Commit Ledger

| Commit | Description |
| :--- | :--- |
| `6daa5e2a1713300ab0076da71ad02087da5ac126` | `refactor(governance): converge claude and codex authority`; parent-owned logical Task 4 commit, 386 paths. |

## Rulings

- None recorded.

## Deferred Items

- The final fix-round repository gate reports 15 baseline or later-task sections: the frozen operations manifest retains deleted historical consumers, legacy metadata/path/archive and Stage 03/05 routing remain outside Task 4, registry-profile enforcement now exposes unregistered legacy generated documents, executable interface templates need later Stage 99 ownership work, and service guides remain absent pending the operations task.
- The pre-commit script-reference check observed the staged native moves and deletes before the complete Task 4 set was assembled. The controlled final gate is green, and no Task 4 active source references a retired path.
- The broad metadata suite observed 254 tests in 117.721 seconds with 2 failures and 1 error before the last bounded legacy-fixture correction. That Task 4 fixture regression then passed in the focused 11-test selection; the remaining failure/error are Task 2/Task 5 taxonomy expectations, and no further broad rerun was started.
- `check-script-manifest.py` remained silent for 4.5 minutes and was interrupted before the five-minute limit. Focused manifest registration is covered by the green CI-routing test; the silent whole-manifest audit remains baseline tooling debt.
- Round 2 intentionally did not rerun the broad repository, broad metadata, or silent manifest gates. The round-1 repository result (`failures=15`) remains the bounded baseline/later-task debt statement; every Task 4-owned amended gate is green.
- Round 3 ran only its focused renderer/hook/inventory/governance/static gates. The prior broad baseline and manifest debt remain unchanged.
- Task 5+ baseline debt is excluded from Task 4 acceptance and from both final `C0/I0/M0` approvals; it is not a residual Task 4 finding.
