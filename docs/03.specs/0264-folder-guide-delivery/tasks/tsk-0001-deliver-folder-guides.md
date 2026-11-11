---
title: "Folder Guide Delivery Task"
version: "0.6.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0264-TSK-0001"
parent_ids:
- "SPEC-0264-PLAN-0001"
created: "2026-11-06"
---

# Folder Guide Delivery Task

## Overview

### Objective

Record the execution and evidence of work units W1 to W5 of the Plan.

## Inputs and Authorization

The owner requested the change on 2026-11-06 and chose one shared hook over
folder `CLAUDE.md` shims, then amended that choice the same day to a shim for
Claude and the hook for Codex (#owner-amendment). Spec approval is the
owner's, in the pull request.

## Work Log

### Implementation

W1 to W3 are implemented on `feat/folder-agents-guide-hook`:
`scripts/lib/hooks/folder_guides.py`, the dispatcher wiring, 8 tests, the
manifest entry, `.claude/provider.md` 1.6.0, `.codex/provider.md` 1.5.0 and the
audit of the 10 `AGENTS.md` files.

W5 is committed on the branch (`13b5f9ce7`, `7384253cf`, `b085cabac`, rebased
onto `cfba0c420`).
`scripts/operations/provider_surface_renderer.py` renders `<folder>/CLAUDE.md`
(marker comment, heading, `@AGENTS.md`) beside each of the 9 Git-tracked
regular folder guides, reports a stale shim, and refuses to overwrite a folder
`CLAUDE.md` without its marker. The Stage 01, 02, 03, 05 and 90 loaders, the
trusted Requirement snapshot, the navigation check and `scripts/manifest.yaml`
admit the shim. `documentation-protocol.md` 3.10.0, `.claude/provider.md`,
`.codex/provider.md` 1.6.0 and `scripts/AGENTS.md` 0.2.2 describe it.

The hook change is committed as `8cc7cffe1`, its suite registration as
`0a37f7655`:
`folder_guides.py` and `agent-event-hook.sh` send full guide text to Codex
only, name the nearest guide on every edit for both providers, and add a
re-read instruction after SessionStart `compact` or `resume`;
`test_folder_guides.py` covers it and is registered in
`.github/workflow-contract.yml`.

The #770 review round, committed as `8ac11bc58`..`13ebb04f1` on `fix/folder-guide-review` above merged main `6e37096a7`, adds:

- Every tracked folder `AGENTS.md` and `CLAUDE.md` selects the
  `agent-governance` suite, so a guide or shim change runs the renderer drift
  gate, and a routing test covers each tracked guide and shim (I1).
- `docs/02.architecture/AGENTS.md` 0.2.4 names the shim as a root entry (I3).
- Claude receives full guide text when its folder shim is missing, not a
  regular file, or does not import `@AGENTS.md`; a Claude read with no edit
  returns before `git ls-files` (M1, M2, M3). `.claude/provider.md` 1.7.1 and
  Spec 0.4.1 describe that fallback.
- The renderer gives no shim to a symlinked guide, the Operations catalog
  requires a regular `CLAUDE.md`, and the Stage 01, 02, 03 and 90 loaders
  reject a `CLAUDE.md` without its `AGENTS.md` (M5, M6, M7); Stage 05 already
  requires both.
- Renderer tests cover untracked, provider-namespace, symlinked and nested
  guides (M8); `.claude/provider.md` names the marker comment (M9); Plan W4
  adds the Codex `compact` source check (M4).

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0264 | draft | approved | #owner-approval |
| SPEC-0264-PLAN-0001 | draft | approved | #owner-approval |
| SPEC-0264-TSK-0001 | draft | ready | #owner-approval |
| SPEC-0264-TSK-0001 | ready | in-progress | #owner-approval |
| SPEC-0264 | approved | in-review | #owner-amendment |
| SPEC-0264-PLAN-0001 | approved | in-review | #owner-amendment |
| SPEC-0264-TSK-0001 | in-progress | blocked | #owner-amendment |
| SPEC-0264 | in-review | approved | #amendment-approval |
| SPEC-0264-PLAN-0001 | in-review | approved | #amendment-approval |
| SPEC-0264-TSK-0001 | blocked | in-progress | #amendment-approval |

### Owner approval

On 2026-11-06 the owner approved the Spec, Plan and Task in the pull request
("SPEC-0264(Spec·Plan·Task 초안) 승인") and assigned the live observation to
the controller ("머지한 뒤 새 Claude 세션과 새 Codex 세션을 각각 repo root에서
시작은 니가 한다").

### Owner amendment

On 2026-11-06, after approving the hook-only design, the owner chose a folder
`CLAUDE.md` shim for Claude and the hook for Codex ("Claude는 shim, Codex는
hook"). The Spec and Plan return to `in-review` for that amendment, and this
Task stays `blocked` until the owner approves them again.

### Amendment approval

On 2026-11-06, asked whether to approve the amended Spec, the owner answered
"승인 (권장)", so the Spec and Plan are `approved` again and this Task is
`in-progress`.

### Review fix approval

On 2026-11-06 the #770 review fix M1 changed the Spec's Normal Behavior
(0.4.1): the hook sends Claude the full guide when the folder's `CLAUDE.md`
shim is missing, is not a regular file or does not import `@AGENTS.md`. Asked
whether to approve that sentence, the owner answered "승인 (권장)", so the
Spec stays `approved`.

### Live observation (criterion 8)

After merge, the controller starts a new Claude session and a new Codex
session at the repository root. In Claude it reads a file under `infra/` and
records whether `infra/CLAUDE.md` loads with `infra/AGENTS.md`; in Codex it
edits a file under `infra/` and records whether the "Folder guide
`infra/AGENTS.md`" context appears once. It also compacts the Codex session
and records whether SessionStart arrives with `source` `compact`, because
re-delivery after compaction depends on it.

### Codex recheck (2026-11-11)

The owner asked for the Codex recheck on 2026-11-11. The controller ran a
headless `codex exec` (codex-cli 0.166.0) at the repository root of main
`602656a52`, because Codex trusts hooks by the path of the root
`.codex/hooks.json`; a worktree would not run them. The session added and then
removed one blank line in `infra/README.md`, and `git status` was clean
afterwards.

- Hook health: SessionStart delivered its context (`hy-home.docker project
  context`) as a developer message, and no `hook ... Failed` appeared. The only
  warning was the ignored user setting `persistent_instructions`. The repo hooks
  are trusted by hash in `~/.codex/config.toml`, and both SessionStart and
  UserPromptSubmit exit 0 in 0.1 s when run by hand.
- Delivery on edit: no folder guide arrived. The session record shows that
  Codex 0.166 runs every tool through one `exec` custom tool whose JavaScript
  input calls `tools.apply_patch(...)` and `tools.exec_command(...)`. No
  PreToolUse hook ran for those nested calls: there is no delivery record under
  `~/.local/state/hy-home/folder-guides/`, and no hook message in the session.
  The registered matcher `Bash|apply_patch` cannot match `exec`, and the
  dispatcher reads only a top-level `apply_patch` or `Bash` payload. With the
  documented `apply_patch` payload the hook still delivers the guide
  (`tests.lib.hooks.test_folder_guides` OK).
- Compaction: `/compact` cannot be run headlessly; NOT_RUN.

Criterion 8 stays pending: Codex delivery fails under its current tool model.
Making it work needs a separate change: confirm whether Codex fires
PreToolUse for `exec` at all, and if so match `exec` and read the nested
`tools.apply_patch` paths.

### Codex 0.167.1 recheck (2026-11-11)

The owner approved the E33 follow-up on 2026-11-11. The CLI had moved to
codex-cli 0.167.1, so the controller first repeated the unchanged probe with
no hook or trust change: a headless `codex exec -s workspace-write --json` at
the repository root of branch commit `72571d481`, applying and reverting one
line in `infra/README.md` through `apply_patch`.

- The JSON event stream shows two `file_change` items for `infra/README.md`.
  No folder guide arrived, and no new record appeared under
  `~/.local/state/hy-home/folder-guides/`.
- The repository Stop hook did fire and reported the leftover change, so the
  trusted repo hooks still run under 0.167.1.
- Codex restored the file itself. Its SHA-256 matched the pre-probe value, and
  `git status` was clean.
- The event stream does not name the tool that carried each patch, so it
  cannot show whether PreToolUse was offered for `exec`.

The next step changes the Codex PreToolUse matcher and re-trusts its hash in
the user-global `~/.codex/config.toml`. That trust is the owner's to grant in
Codex's own prompt; this recheck did not write it.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1, 2, 3, 4, 5 | W1 | folder guide tests | `python -m unittest tests.lib.hooks.test_folder_guides` | PASS | 8 tests OK | required | - |
| E2 | 1, 4 | W1 | hook suites | `test_folder_guides test_tool_payload test_agent_governance_ci_routing test_script_manifest test_validator_entrypoints` | PASS | 162 tests OK | required | - |
| E3 | 1 | W1 | script manifest | `check-script-manifest.py` | PASS | manifest valid | required | - |
| E4 | 6 | W2 | provider surfaces | `provider_surface_renderer.py --check` | PASS | drift=0 | required | - |
| E5 | 7 | W3 | agent governance | `check-agent-governance-contract.py --mode repository` | PASS | exit 0 | required | - |
| E6 | 1, 2, 3, 4, 5 | W1 | folder guide tests | `python -m unittest tests.lib.hooks.test_folder_guides` at `a3695644a`, after the security review fixes | PASS | 15 tests OK, including untracked, symlinked, unreadable, subagent and denied-then-allowed cases | required | - |
| E7 | 1, 4 | W1 | hook suites | `test_folder_guides test_tool_payload test_agent_governance_ci_routing test_script_manifest test_validator_entrypoints test_ci_gate_adapters` at `a3695644a` | PASS | 209 tests OK | required | - |
| E8 | 1, 4, 5 | W1 | security review | `security-auditor` review of the hook diff, then a scoped re-review of the fix commit `c1648d5fa` | PASS | round 1 CHANGES_REQUIRED (F1-F8); round 2 APPROVED; two Low follow-ups fixed in `a3695644a` | required | - |
| E9 | 1 | W1 | manifest, surfaces, contract | `check-script-manifest.py`, `provider_surface_renderer.py --check`, `check-agent-governance-contract.py --mode repository` at `a3695644a` | PASS | manifest valid; drift=0; failures=0 | required | - |
| E10 | 9 | W5 | renderer shim tests | `python -m unittest tests.validation.test_validator_entrypoints` on the W5 working tree | PASS | 8 tests OK, including shim create, drift, stale retirement and hand-written refusal | required | - |
| E11 | 9 | W5 | provider surfaces | `provider_surface_renderer.py --write`, then `--check`, on the W5 working tree | PASS | 9 shims written; drift=0 | required | - |
| E12 | 10 | W5 | document metadata | `check-document-metadata.py --mode check-active` and `--mode check-changed --base-ref origin/main` on the W5 working tree | PASS | violations=0 in both modes | required | - |
| E13 | 10 | W5 | links and contract | `check-document-links.py --mode alignment`, `check-agent-governance-contract.py --mode repository` on the W5 working tree | PASS | failures=0; failures=0 | required | - |
| E14 | 10 | W5 | script manifest | `check-script-manifest.py` on the W5 working tree | FAIL | `path-untracked scripts/CLAUDE.md`: the shims are not yet staged | required | - |
| E15 | 10 | W5 | script manifest | `check-script-manifest.py` with the 9 shims added to its tracked-path set in process | PASS | manifest valid | optional | - |
| E16 | 10 | W5 | suites | `tests.validation.test_agent_governance_ci_routing`, `tests.lib.document_governance.test_spec_packages` on the W5 working tree | FAIL | 172 tests, 1 failure: `test_static_checks_stop_descendants_after_parent_exit` (docker descendant survived), run beside other heavy checks | required | - |
| E17 | 1 | W5 | native shim load | Headless Claude Code 2.1.319 in a throwaway repository with root `CLAUDE.md`, `sub/CLAUDE.md` holding the marker comment then `@AGENTS.md`, run again with a `# sub Folder Guide` heading between them and a new codeword, and only `sub/data.txt` read | PASS | both runs answered the `sub/AGENTS.md` codeword; each trace shows one Read of `sub/data.txt` | optional | - |
| E18 | 10 | W5 | suites | `test_static_checks_stop_descendants_after_parent_exit` rerun alone on the W5 working tree | PASS | 1 test OK; the E16 failure is a timing failure unrelated to W5 | required | E16 |
| E19 | 10 | W5 | script manifest | `check-script-manifest.py` at `d2d5ca525`, with the 9 shims committed | PASS | `PASS: script manifest is valid` | required | E14 |
| E20 | 1, 2, 4 | W1 | hook suites | `test_folder_guides test_tool_payload test_agent_memory test_validator_entrypoints test_agent_governance_ci_routing test_script_manifest test_surface_ownership test_ci_gate_model test_ci_gate_adapters` at `d2d5ca525`, after the edit reminder, restart instruction and Codex-only full delivery (`b905f662f` rebased) and the hook-suite registration | PASS | 258 tests OK | required | - |
| E21 | 9, 10 | W5 | surfaces, contract, metadata | `provider_surface_renderer.py --check`, `check-agent-governance-contract.py --mode repository`, `check-document-metadata.py --mode check-changed` and `--mode check-active`, `check-document-corpus-lifecycle.py`, `check-operations-catalog.py` at `d2d5ca525` | PASS | drift=0; failures=0; violations=0 (15 and 538 selected); occupancy 0; catalog PASS | required | - |
| E22 | 1, 2, 4 | W1 | hook suites | `test_folder_guides test_tool_payload test_agent_memory test_validator_entrypoints test_agent_governance_ci_routing test_script_manifest test_surface_ownership test_ci_gate_model test_ci_gate_plan test_ci_gate_adapters test_github_workflow_contract` on the #770 review working tree above `bce91a1af` | PASS | 370 tests OK, including the shim fallback, the read-skips-git, the symlinked, untracked, provider-namespace and nested guide cases, and the guide and shim routing | required | - |
| E23 | 10 | W5 | stage loader suites | `tests.lib.document_governance` `test_architecture`, `test_requirements`, `test_references`, `test_operations_catalog`, `test_spec_packages`, run one at a time on the #770 review working tree | PASS | 11, 24, 21, 136 and 90 tests OK | required | - |
| E24 | 9, 10 | W5 | surfaces, contract, metadata | `provider_surface_renderer.py --check`, `check-script-manifest.py`, `check-agent-governance-contract.py --mode repository`, `check-document-metadata.py --mode check-changed --base-ref origin/main` and `--mode check-active`, `check-document-corpus-lifecycle.py`, `check-operations-catalog.py`, `check-document-links.py --mode alignment` on the #770 review working tree | PASS | drift=0; manifest valid; failures=0; violations=0 (5 and 538 selected); lifecycle and occupancy violations=0; catalog PASS; links failures=0 | required | - |
| E25 | 6 | W2 | provider surfaces | `provider_surface_renderer.py --check` on the #770 review working tree, after `.claude/provider.md` 1.7.1 | PASS | drift=0 | required | - |
| E26 | 8 | W4 | live Claude load | New headless Claude Code 2.1.319 session at the repository root of merged main `6e37096a7`, reading `infra/README.md` only | PASS | the session answered that `infra/CLAUDE.md` loaded on demand after the read, with `infra/AGENTS.md` imported, as a system reminder | required | - |
| E27 | 8 | W4 | live Codex delivery | New Codex session at the repository root of merged main `6e37096a7`, editing a file under `infra/` and compacting | NOT_RUN | Codex usage limit until 2026-11-09 18:37 KST; delivery once per session and the SessionStart `compact` source are not observed | required | - |
| E28 | 8 | W4 | Codex hook health | The same Codex start at `6e37096a7`, and again at `cfba0c420` before #770 | ERROR | Codex reported `hook: SessionStart Failed` and `hook: UserPromptSubmit Failed` at both revisions, so the failure predates #770; a manual run of `scripts/hooks/agent-event-hook.sh` with `HY_HOME_HOOK_PROVIDER=codex` exits 0. Cause unknown: hook trust in `/hooks` and the hook stderr are checked after the usage limit resets | required | - |
| E29 | 1, 2, 4 | W1 | hook, renderer, routing and loader suites | `test_folder_guides test_validator_entrypoints test_agent_governance_ci_routing test_architecture test_operations_catalog`, then `test_spec_packages`, at committed `13ebb04f1` | PASS | 259 tests OK; 90 tests OK | required | - |
| E30 | 9, 10 | W5 | surfaces, manifest, contract, metadata, links | `provider_surface_renderer.py --check`, `check-script-manifest.py`, `check-agent-governance-contract.py --mode repository`, `check-document-metadata.py --mode check-changed --base-ref origin/main`, `check-document-links.py --mode alignment` at `13ebb04f1` | PASS | drift=0; manifest valid; failures=0; violations=0, with 5 selected because the base is merged main `6e37096a7` and only this follow-up's documents differ; links PASS | required | - |
| E31 | 6 | W2 | scoped review | `code-reviewer` re-review of `6e37096a7..13ebb04f1` against the #770 findings I1-I3 and M1-M9 | PASS | every finding fixed except I2's evidence revision (N1), which E29 and E30 resolve; the reviewer read `.claude/provider.md` 1.7.1 and found it names the marker comment (M9) | required | - |
| E32 | 8 | W4 | Codex hook health | Headless `codex exec` 0.166.0 at the repository root of main `602656a52`, 2026-11-11 | PASS | SessionStart delivered `hy-home.docker project context`; no hook failure reported; hooks trusted by hash; SessionStart and UserPromptSubmit exit 0 in 0.1 s by hand | required | E28 |
| E33 | 8 | W4 | live Codex delivery | The same session, editing `infra/README.md` through `tools.apply_patch` inside the Codex `exec` tool, then reverting | FAIL | no folder guide delivered and no delivery record; Codex 0.166 wraps tool calls in `exec`, which the matcher (`Bash` or `apply_patch`) does not match; compaction NOT_RUN headless | required | - |
| E34 | 8 | W4 | live Codex delivery | Headless `codex exec` 0.167.1 at branch commit `72571d481`, 2026-11-11, applying and reverting one line in `infra/README.md` through `apply_patch` | FAIL | no folder guide and no delivery record; Stop hook fired; file restored byte-identical; matcher and trust unchanged | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | E1, E2, E6, E7, E8, E9, E17, E20, E22, E29 | owner acceptance | @buenhyden |
| 2 | pending | E1, E6, E20, E22, E29 | owner acceptance | @buenhyden |
| 3 | pending | E1, E6 | owner acceptance | @buenhyden |
| 4 | pending | E1, E2, E6, E7, E8, E22, E29 | owner acceptance | @buenhyden |
| 5 | pending | E1, E6, E8 | owner acceptance | @buenhyden |
| 6 | pending | E4, E25, E31 | owner acceptance | @buenhyden |
| 7 | pending | E5 | owner acceptance | @buenhyden |
| 8 | pending | E26, E27, E28, E32, E33, E34 | Claude observed; Codex hook health fixed (E32 resolves E28); Codex delivery FAIL under the `exec` tool model (E33) and again on 0.167.1 (E34), needs a matcher change with owner-granted trust | @buenhyden |
| 9 | pending | E10, E11, E21, E24, E30 | owner acceptance | @buenhyden |
| 10 | pending | E12, E13, E15, E16, E18, E19, E21, E23, E24, E30 | owner acceptance | @buenhyden |

## Review and Completion

The amended Spec and Plan are approved and the #770 review findings are
fixed in commits `8ac11bc58`..`13ebb04f1`, rechecked at `13ebb04f1` (E29, E30). Criterion 8 is observed for Claude (E26); the
Codex observation, including the `compact` source, is NOT_RUN until the Codex
usage limit resets on 2026-11-09 18:37 KST (E27), and Codex reports its
SessionStart and UserPromptSubmit hooks as failed at revisions before and
after #770 (E28). Every criterion needs owner acceptance. A Codex shell read does not trigger delivery, and native delivery
in a live session of this repository is not yet observed.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
