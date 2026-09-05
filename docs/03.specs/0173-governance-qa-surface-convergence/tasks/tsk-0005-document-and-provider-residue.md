---
title: "Document and Provider Residue Task"
version: "0.2.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0005"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Document and Provider Residue Task

## Objective

Remove current paths that reproduce legacy document grammar, retire obsolete
generated snapshots, and reduce provider projections to required native
interfaces backed by one Stage 00 authority.

## Inputs

- [SPEC-0173](../spec.md), its [implementation plan](../plan.md), and the
  ownership boundaries established by Tasks 0001 through 0004.
- Current authored documents, templates, forms, examples, registry and schema,
  LLM Wiki inputs, DATA-0068/0069/0073/0074, and provider renderers.
- `.agents/`, `.claude/`, `.codex/`, hooks, provider projection tests, and
  current consumer searches.

## Work Log

Task 4 converged test and fixture ownership at `85b0fc13`, enabled recursive
discovery at `e8a59d9c`, and recorded focused evidence at `74a6190e`. Task 5
became ready at `0213b0ee` and started at `e7768f8d` from a clean worktree.

Commits `9e9ca916` and `fa0f2a3a` separated current document classification
from historical identity recovery and replaced retired operator path examples.
Commits `8c4d2709` and `db6722b6` removed the active T-AER recovery dependency
and completed-migration manifest assertions. Commit `37a756f2` retired
DATA-0068, DATA-0069, DATA-0073, and DATA-0074 with byte-identical registered
README moves, four Tombstones, and exact Git recovery for unregistered payloads.

Provider compatibility RED proved `.agents/agents` was still generated.
Implementation commit `6aa4287e` then cut the workflow, runner, manifest,
documentation, and tests to the direct renderer; made that Python entrypoint
executable; and removed the shell wrapper. The renderer revalidated and
quarantined exactly 14 owned compatibility role files before their approved
cleanup. It now preserves `.agents/skills`, `.claude`, and `.codex` only.
PostToolUse no longer invokes the aggregate, while Stop invokes the changed
profile for Git-visible dirty state before the logical-commit gate. The resumed
review found that PostToolUse retained formatting but lost the policy-required
lint and diff checks, and that aggregate uniqueness across Stop retries was not
proved. The bounded correction subsequently resolved retry behavior and restored
the checks, but policy re-review found incomplete shell-path coverage. After
explicit approval for one additional path-selection correction, the remaining
policy finding was closed by independent re-review.

On 2026-09-05, execution resumed at `6aa4287e` with only this Task and the Plan
modified. Local `main` and cached `origin/main` both resolved to `71da6654`;
there were two worktrees and no stash entries. No remote refresh occurred.

## Verification Evidence

| Check | Result |
| --- | --- |
| Current/history RED and GREEN | Paired legacy-path tests first exposed current fallback; current classification now rejects it while Git/archive history recovery retains `REQ-0042` |
| Target-surface retirement | Four registered README blobs preserved byte-identically; Tombstones 0199–0202 and recovery commit `db6722b63fcc3711909bfd87e80c52b51168ca7c` passed archive recovery |
| Provider compatibility RED | `test_projection_omits_provider_neutral_agent_compatibility_root` failed before renderer cutover and passed after `.agents/agents` retirement |
| Renderer write/check | First write quarantined exactly 14 revalidated generated role files and returned nonzero; exact cleanup plus second write/check returned `provider_surface_renderer: PASS providers=2 drift=0` |
| Provider and hook tests | 81 renderer, typed contract, native surface, parity, routing, and Stop deferral tests passed |
| Document governance | Focused discovery passed 379/379 after the first run's two stale DATA-0082 links were regenerated through the LLM Wiki owner |
| Metadata and lifecycle | Active metadata selected 374 documents with 0 violations; lifecycle/archive reported 0 violations with 3 migrations, 108 Tombstones, and 145 preserved bodies |
| Links and generated paths | All-mode links passed for 693 documents and 5,744 links; LLM Wiki write/check reported both outputs fresh |
| Script ownership | `check-script-manifest.py` and provider hook parity passed; the deleted wrapper has no active workflow, manifest, runner, Stage 00, operation, script, or test consumer |
| Whitespace | Unstaged and cached `git diff --check` passed before `6aa4287e` |
| Resumed evidence check | `check-document-metadata.py --mode check-changed --base-ref HEAD` selected 2 documents with 0 violations; corpus lifecycle and archive recovery both returned 0 violations; manifest and diff checks passed |
| Generated preflight | Provider, provenance, audit matrix, supply-chain summary, LLM Wiki, and hook parity checks passed; Compose coverage and security readiness checks failed as stale. Compose dry-run reproduces obsolete frontmatter; readiness differs in derived inventory counts. No output was written |
| Correction RED: hooks | `PYTHONPATH=. python3 -m unittest tests.validation.test_agent_governance_ci_routing -v` ran 14 tests and returned exit 1 with 10 expected failures: missing checks, retry re-entry, failed Git inspection, and missing inner timeout |
| Correction RED: history APIs | The focused `test_history_reader_parses_legacy_requirement_children` and `test_archive_reader_recovers_legacy_parent_identities` tests returned exit 1 with 2 missing-helper errors before the recovery-owner implementation |
| Correction intermediate GREEN | History/archive/registry focused tests passed 115/115. The first hook/parity/deferral rerun passed 32/33; its remaining source-shape assertion still expected the old unbounded command and is being updated to assert the approved timeout wrapper. This intermediate result is not final acceptance |
| Correction hook GREEN | `PYTHONPATH=. python3 -m unittest tests.validation.test_agent_governance_ci_routing tests.validation.test_stop_gate_deferred_paths tests.validation.test_provider_hook_parity -v`: exit 0, 34 tests passed in 30.417 seconds, including exit-0 denial JSON, retry non-reentry, failed Git inspection, timeout/kill-after argv, and invalid second-shell syntax |
| Correction history GREEN | `PYTHONPATH=. python3 -m unittest tests.lib.document_governance.test_identity_history tests.lib.document_governance.test_archive tests.lib.document_governance.test_registry -v`: exit 0, 115 tests passed; after the final import/caller adjustment, the three focused helper/delegation tests passed in 0.076 seconds |
| Correction audit GREEN | `PYTHONPATH=. python3 -m unittest tests.validation.test_audit_criterion_contract tests.validation.test_agentic_audit_semantic_freshness -v`: exit 0, 40 tests passed in 2.337 seconds; direct semantic freshness passed 11 assertions |
| Correction contract checks | Manifest, renderer check, hook parity check, metadata for the 3 changed audits, corpus lifecycle/archive recovery, all-mode links, shell formatting/lint/syntax, Python compilation, and diff checks passed. DATA-0072 remained fresh without regeneration |
| Rejected diagnostic invocation | `python3 scripts/validation/check-archive-recovery.py` exited 2 because that CLI does not exist. It was not acceptance evidence; the canonical corpus-lifecycle command subsequently verified archive recovery |
| Approved path correction RED | `PYTHONPATH=. python3 -m unittest tests.validation.test_agent_governance_ci_routing.AgentGovernanceCiRoutingTests.test_post_tool_checks_shell_files_outside_scripts -v`: exit 1, all 9 subcases failed as expected because root, infra, and tests shell paths bypassed formatting, lint, and syntax checks |
| Approved path correction GREEN | `PYTHONPATH=. python3 -m unittest tests.validation.test_agent_governance_ci_routing tests.validation.test_stop_gate_deferred_paths tests.validation.test_provider_hook_parity -v`: exit 0, 35 tests passed in 30.100 seconds, including all 9 new subcases and existing unsafe-path checks |
| Approved path correction static checks | `shellcheck scripts/hooks/post-tool-validate.sh`, `shfmt -d scripts/hooks/post-tool-validate.sh`, `bash -n scripts/hooks/post-tool-validate.sh`, and `git diff --check`: exit 0 |

## Review Evidence

Independent code and policy reviewers reviewed `e7768f8d..6aa4287e` before
Task 6 activation. Code review reported 0 Critical, 5 Important, and 1 Minor;
policy review reported 0 Critical, 5 Important, and 0 Minor. Both returned
correction-required compliance and quality verdicts. Overlapping findings are
one correction responsibility rather than duplicate validators.

| Finding | Correction boundary | Status |
| --- | --- | --- |
| Missing PostToolUse lint/diff checks | Restore bounded policy-required checks and regression tests, not the aggregate | Closed by independent policy re-review after explicitly approved path correction |
| Stop re-enters the aggregate on retry | Inspect provider retry sentinel before execution; escalate without a cache | Closed by code and policy re-review |
| Git inspection failure treated as clean | Distinguish clean, dirty, and unknown; fail closed | Closed by code and policy re-review |
| Claude outer timeout truncates aggregate | Registered 600-second outer budget, bounded inner attempt, explicit incomplete result and manual revalidation | Closed by policy re-review |
| Removed provider commands/surfaces in source audits | Delimit dated evidence and add the current direct-renderer route; regenerate derived output | Source correction closed; derived historical designation remains a Task 6 dependency |
| Historical grammar still owned by registry/metadata modules | Move recovery-only parsing into the existing history/archive owners and cut actual callers over | Closed by code and Python re-review |
| Old Stop helper name in hook-rule comment | Correct the comment with the hook fix | Closed by code re-review |

Plan Steps 3, 8, and 9 were reopened for the bounded correction and independent
re-review. They are now checked after the explicit additional path correction
and all independent acceptance verdicts. This implementation milestone permits
Task 6 activation; the active-stage Task retains `in-progress` until the
separate package disposition process.

The frozen correction received independent scoped re-review on 2026-09-05:

- `task5_review`: specification PASS and code APPROVED; 0 Critical,
  0 Important, and 0 Minor findings in the reviewed correction.
- `history_python_review`: specification PASS and code PASS; 0 Critical,
  0 Important, and 0 Minor findings. Fresh-process imports in both orders passed;
  the four reported Ruff findings predate the correction at `6aa4287e`.
- `task5_policy_review`: CHANGES_REQUIRED, quality C; 0 Critical,
  1 Important, and 0 Minor findings. PostToolUse selects shell files only under
  `.claude/hooks/` and `scripts/`, whereas the current Agentic policy promises
  checks on changed shell files. Hook-selected `infra/` and `tests/` shell files
  are omitted, and the current regression inputs exercise only `scripts/`.

The minimum proposed correction was to select all applicable hook-selected
`.sh` files without changing the path-safety boundary, then add a non-`scripts/`
regression and re-run focused checks plus independent policy review. Execution
paused because the original attempt and its single narrower retry had exhausted
the Stage 00 workflow bound.

The user then explicitly approved one additional correction limited to target
selection and regression tests plus independent re-review. The implementation
replaced the directory-restricted shell selector with an existing-file `.sh`
selector and added one table-driven test with 9 subcases. It did not change
path-safety validation, policy, provider projections, or aggregate routing.
`task5_policy_review` returned PASS, quality A, with 0 Critical, 0 Important,
and 0 Minor findings; residual I1 is closed. DATA-0065 historical designation
remains a Task 6 dependency. `history_python_review` also returned specification
and code PASS with 0 Critical, 0 Important, and 0 Minor findings for this
incremental correction. Its whole-module Ruff check reported an existing unused
`shutil` import outside the approved incremental diff; that warning was not
modified or represented as a clean whole-module lint result.
The user subsequently authorized continuing Task 6 and cleaning the development
branch/worktree after integration. The reviewed corrections are committed below;
no final aggregate or remote/runtime result is claimed by this Task.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `e7768f8d` | Start Task 5 from the accepted Task 4 milestone |
| `9e9ca916` | Isolate historical document grammar from current classifiers |
| `fa0f2a3a` | Replace retired current operator examples |
| `8c4d2709` | Remove retired T-AER execution evidence from the current audit checker |
| `db6722b6` | Remove completed script-manifest migration assertions |
| `37a756f2` | Retire target-surface DATA packages and their current production subsystem |
| `6aa4287e` | Retire provider role compatibility output and converge completion validation |
| `0b237043` | Isolate recovery-only parsing in history/archive owners; focused 115-test and 3-test evidence above |
| `0fbbb962` | Restore bounded post-edit checks and fail-closed Stop behavior; focused 35-test evidence above |
| `3fbb62aa` | Delimit historical audit provider evidence; focused 40-test and semantic freshness evidence above |

This evidence checkpoint does not predict its own commit identity.

## Rulings

- Keep stable frontmatter IDs while removing banned basename prefixes from
  current authored paths.
- Retain `.agents/skills`, `.claude`, and `.codex` native interfaces; retire
  `.agents/agents` only after renderer and consumer cutover is proven.
- Generated snapshots without a current consumer are retired through the
  canonical lifecycle rather than preserved as active authority.
- Create one sealed package Tombstone for each retired DATA artifact and move
  each registered `README.md` byte for byte; recover unregistered payloads from
  the exact Git commit recorded by the Tombstone.
- Ruling: preserve the hook validator's 600-second cap. Policy review accepts
  Claude Stop at that outer budget with a 540-second inner attempt, leaving
  room to report incomplete validation and request the same canonical command
  manually. This is not a guarantee that every changed plan finishes inside a
  hook; if the budget is insufficient, completion is blocked rather than
  accepted. No persistent success/approval cache is introduced.
- Ruling: use the repository's one-narrower-retry bound rather than the generic
  skill's five-round loop. Remaining blocking findings after re-review require
  escalation, not an unbounded correction sequence.
- Ruling: after that escalation, explicit user approval authorized exactly one
  additional shell-path selection and regression correction with independent
  re-review. This bounded approval does not change the shared retry policy or
  authorize unrelated implementation.
- Ruling: distinguish internal validator failure from successful delivery of a
  blocking hook response. The [official Claude hook reference](https://code.claude.com/docs/en/hooks),
  checked on 2026-09-05, requires exit 0 for JSON decision control. The outer
  Stop dispatcher must deliver block/terminal JSON with exit 0 without calling
  SessionEnd; a nonzero internal gate result still selects that denial path.
  This documents the protocol, not an observed native runtime execution.

## Deferred Items

- User-global Claude or Codex configuration, credentials, and private state
  remain inaccessible and undocumented.
- Provider entitlement and live provider execution remain unverified.
- Hosted CI, remote branch protection, and deployed runtime remain unverified;
  this Task changed only tracked local definitions and repository enforcement.
- Reverting `6aa4287e` restores the former wrapper, compatibility Registry
  route, role projections, and per-edit aggregate. Partial restoration of only
  generated files is not a valid rollback because the renderer would remove or
  reject them according to its current Registry.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Test and fixture convergence Task](tsk-0004-test-and-fixture-convergence.md)
