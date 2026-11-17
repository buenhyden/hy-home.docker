---
title: "W07 Native Provider Adapter Task"
version: "0.4.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0079"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-16"
---

# W07 Native Provider Adapter Task

## Scope

### Objective and Parent

Own W140 and criterion 135 in the [Plan](../plan.md) and [Spec](../spec.md).
Align the registered native hooks with their event contracts and record the
observations and remaining gaps for each provider.

### Inputs and Authority

The direct W07-ADAPTER 3.0.0 request authorizes local implementation and
verification at the clean `fbac0fde1` baseline. The current brief binds the
exact change paths. [W01](tsk-0068-w01-contract-3-0-1.md) is accepted.
Provider trust, accounts, external writes, spending and production are outside
this request's approved local change scope.

## Execution Log

### Work Performed

#### Design before implementation

D17, D08 and D07 at 3.0.1 require event-specific output, observed authority,
and separately accounted capture and memory. Reuse the existing Registry,
dispatcher, provider-shaped denial and request brief check. Read the supplied
research entries S06, S10, S11, S15, S20–S24 and the Docker binding profile,
decisions, repository observations and PR observations.

Long Stop inputs can exceed the system's environment string limit before
Python reads the retry flag. The same transport is used for event detection
and SessionStart. Reuse the file descriptor approach already used by
PreToolUse. Avoid truncating event JSON, which can discard a needed field.
Claude discards SessionEnd JSON and this registration has no cleanup or
capture side effect. Retire the registration and keep the Stop reminder and
its existing native continuation decision. Revert the dispatcher,
registration, projection and manifest together if a consumer regresses.
Verify both command routes on long retry input, valid startup context and
unchanged denial output. Check projection, manifest and independent review.

#### Local implementation

Pass the event JSON on a descriptor to event detection,
SessionStart and the Stop retry check. Stop retains the existing Git worktree
continuation decision and reminder. Retire the authored Claude SessionEnd
wrapper from the Provider Registry, project settings and script manifest.
The Claude adapter records the distinction between turn continuation and
acceptance. There is no new policy owner or runtime input from the workspace
design package.

KEEP_VERIFIED covers the accepted W01 contract. Reused local components
include the existing PreToolUse denial shape, request brief checks and
provider renderer. Their fixture coverage and native delivery have separate
evidence. No broader runtime or owner acceptance was inferred from reuse.

#### Capability observations

| Provider and feature | Configured | Installed support | Discovered | Authorized | Observed | Verified scope |
| --- | --- | --- | --- | --- | --- | --- |
| Claude 2.1.325 SessionStart | Project settings and wrapper | CLI starts and trace recognizes event | Project command in isolated trace | Trust or permission notice | No hook result or lifecycle message | Local command fixture only |
| Claude PreToolUse, prompt and Stop | Project settings and wrappers | Official hook interface, local version identified | Repository projection check | Native trust and account unknown | Provider-shaped command fixtures | No native allow, deny or Stop result |
| Codex desktop prompt and edits | Project hooks and request brief | Actual session accepts the traced events | Active project hooks | Current session and exact bound paths | Prompt state readable, scoped Task edit proceeds, excluded README patch denied before application | Current desktop recognized patch route only |
| Codex CLI 0.169.0 | Project hooks | Local app-server protocol schema exposes hook list and notifications | Installed schema generation, no CLI hook invocation | CLI trust and account unknown | Sandbox launcher prerequisite failure | No CLI permission or hook delivery result |
| Both reviewer roles | Registry and generated roles | Claude tools omit Bash and render plan mode, Codex renders read-only | Projection parity | Effective reviewer identity and restrictions unobserved | No native reviewer shell or synthetic sensitive-path deny | Configuration only |
| Both capture and shared memory | Existing explicit memory CLI, capture binding absent | Hook transcript metadata varies by provider | Repository source only | No transcript collection scope approved | No raw transcript opened or memory changed | W08-CAPTURE and W08-MEMORY own delivery and recovery |
| Both prepared worker dispatch | Explicit request brief preflight from W07-BRIEF | CLI and provider-shaped hook fixtures | Local preflight and call sites | Current exact request and scope required | No provider worker mutation dispatched for this check | Fixture evidence and prior Task only |

Claude startup used `--init-only`, project settings only, an empty MCP
configuration and disposable configuration and state. Account and global
settings were outside inspection scope. Codex desktop observations identify
the active runtime separately from the installed CLI. Upstream
[Claude hook reference](https://code.claude.com/docs/en/hooks#sessionend)
and [Codex hook reference](https://learn.chatgpt.com/docs/hooks#pretooluse)
establish documented output behavior. No invalid output was installed in the
active project to observe fail-open behavior.

#### Local latency

Nine paired runs per provider-shaped Stop input at the same worktree measured
dispatcher subprocess wall time with the old and new scripts. With a
140,000-byte synthetic assistant message and the retry flag set, Claude-shaped
median latency changed from 151.56 to 69.84 ms and Codex-shaped latency from
188.99 to 80.97 ms. Both changed from zero to nine silent successful retries.
With an 80-byte message, both versions completed all nine retries and medians
were 61.11 to 67.80 ms and 62.37 to 54.00 ms respectively. The large-message
baseline took the wrong Stop path. These measurements cover local command
startup and dispatch only. The large SessionStart fixture uses a synthetic
extra field to exercise transport independent of the provider payload schema.

#### Resume verification at e2c307bcc

The direct W07-ADAPTER resume request binds this clean baseline and the
Task and authored Codex adapter paths. Reuse the reviewed dispatcher and
registered hook bindings. Recheck the focused fixture cases and use the
installed clients with disposable profiles to identify which remaining
guarantees can be measured locally. Preserve project trust and account
settings. If a runtime exposes effective permissions that differ from
the projection, record the particular route and target in its adapter.
A rollback of that documentation leaves the runtime behavior unchanged.

The focused `python3 -m unittest` invocation selected
`HookOutputAndMainPushTests`, the long Stop retry case and
`tests.lib.hooks.test_request_brief`. All 31 tests passed. Repository
contract, provider renderer and script manifest checks returned zero
failures. The hook implementation and timing inputs did not change, so the
previous paired measurements still describe the implementation change.
The same two PRs remained open in the new read-only lookup.

Codex CLI 0.169.0 returned a native `initialize` and `hooks/list`
response from `codex app-server --listen stdio://` in a fresh temporary
profile. The response listed no project-defined hooks at this workspace
path. The local desktop proxy could not connect. The standalone
`command/exec` request with the `readOnly` policy produced no response
within the probe budget. The separate `codex sandbox linux` launch
stopped at its app-server socket directory prerequisite before the
permission check ran.

Claude Code 2.1.325 also ran `--print --init-only --output-format stream-json`
with project settings, an empty MCP configuration and disposable state.
It returned zero, and the trace again showed project SessionStart discovery
and a trust or permission notice. The stream produced no hook lifecycle
result. The probe submitted no model prompt.

In the current Codex desktop collaboration route, the `code-reviewer` role
could open the synthetic temporary fixture with `O_WRONLY` through its
normal shell tool. The operation wrote zero bytes and the author checked
the unchanged fixture before removing it. The witness confirms that opening
this exact temporary path for writing was allowed. The installed
CLI role and protected paths require their own tests. The authored Codex
adapter now records this distinction without changing any role or permission.

#### Trusted launch checks at abf8d6b9b

The direct resume request asks for an existing trusted Claude session and
an enforced read-only Codex reviewer path. Use the normal launchers in the
same workspace. Retain the prior local source verification because the
dispatcher, Registry and hook bindings are unchanged. An inconclusive
startup or sandbox constructor failure leaves the dependent trial open.
Record the witnesses in this Task and the authored Codex adapter.

No Claude CLI process was visible with this workspace as its working
directory. A normal interactive Claude Code 2.1.325 startup used the
existing profile and a private terminal with no keystrokes or model prompt.
It emitted a filesystem permission error and produced no registered
SessionStart result during the bounded observation. The existing-profile
`claude --init-only` probe, with structured output and no MCP connections,
returned zero and reported a read-only filesystem error. It emitted no
hook lifecycle result. Neither observation verified the profile's trust.

The initial nested Codex launcher saw a socket directory prerequisite
error, and both `bwrap` mount preflights failed at namespace creation.
A separately approved host preflight using a read-only root mount and
network namespace exited zero. The initial command still passed
`linux` as a subcommand. The installed help showed that
`codex sandbox` now takes command arguments directly.

Using the installed Codex CLI 0.169.0 with `sandbox_mode = "read-only"`
on the approved host route, the synthetic read passed and the write-mode
open returned `EROFS`. A second run used a disposable named profile
extending `:read-only` with networking disabled and an explicit read deny
for a synthetic protected directory. The launcher used
`--include-managed-config`. It again allowed the
ordinary read, rejected the write-open with `EROFS`, and rejected the
protected read with `EACCES`. Both commands exited zero with their
expected outcomes and left the ordinary file unchanged. The scratch
profiles and fixtures were removed. The named CLI profile also read the
current workspace HEAD through Git while repeating both denials.
The provider adapter records this route and the separate managed desktop
reviewer failure.

An approved Claude interactive preflight under a read-only root with
networking disabled and a disposable output path also returned no hook
result during the bounded observation. Resume Claude delivery and decision
checks in an operator-provided trusted session for this workspace.
Continue managed desktop reviewer validation when the launcher provides
an effective role restriction. Provider settings, credentials and host
permissions were left intact.

#### Trusted Claude session checks at f05d4e805

The direct resume request runs in an existing interactive Claude Code
session in this workspace with its current permission mode. Project
settings, the dispatcher and hook bindings are unchanged from the prior
verification. The session observed hook delivery and exercised the
PreToolUse brief guard with Claude's native Edit tool on two gitignored
synthetic `*.tmp` fixtures at the workspace root. No secret file, raw
session log, user setting or managed setting was opened or changed.

Hook results. Project SessionStart delivered the `hy-home.docker project
context` text from `scripts/hooks/agent-event-hook.sh`. Project
UserPromptSubmit delivered the request brief notice and recorded request
state that `request_brief status` returned for this session. A brief bound
this Task and `w07-synthetic-in.tmp` as allowed edits and listed
`w07-synthetic-out.tmp` as out of scope. Project PreToolUse allowed the
in-scope Edit. It denied the out-of-scope Edit with `This action exceeds
the bound request brief scope.` and Claude reported the tool as not run.
On edits to this Task, project PreToolUse also returned the stage
document and template warnings and the folder guide reminder as
additional context. The ECC GateGuard plugin hook separately asked for
first-touch facts before the project hook decided. Those plugin prompts
are not project hook results.

File state. The in-scope fixture changed from SHA-256 `711f1a1d…f798`
(`v0`) to `3a531e49…b45b` (`v1`) with a new modification time. The
out-of-scope fixture kept SHA-256 `8de8965a…2010`, its 34-byte size, its
`v0` content and its original modification time. Both fixtures were
removed after recording.

Project Stop then blocked the first stop attempt, named this Task as an
uncommitted path and continued the turn. The continuation records no
acceptance and grants no commit permission.

The session report contained no visible PostToolUse result, so its
execution remains unverified. PreCompact and the silent second Stop
also lack a reported result. The unsupported-output control case,
reviewer role boundaries, worker dispatch, and capture or memory
delivery remain unverified on this Claude path.

The Claude session reported a metadata check selecting 92 documents,
zero violations and exit 0 on its Task edit. Alignment and command-link
checks were still running when that report was sent.

#### Claude PostToolUse follow-up at b3cff1273

The later trusted-session report observed the project dispatcher and its
child process after a native Edit to the only synthetic file in the bound
scope. The file changed from `v1` to `v2` and its reported SHA-256 prefix
changed from `2d27fbdf` to `81db67b6`. The process monitor saw the
PostToolUse invocation at 07:42:26.041 and both processes had ended by
07:42:26.103. It did not capture either exit status. The fixture change
confirms the Edit outcome. Process completion confirms hook delivery
but leaves the hook success result open.

The report included a Stop closing reminder and the terminal's completed
turn indicator. It contained no preceding block paired with that Stop in
the same turn. PreCompact was planned and no invocation or completion was
reported for it.

#### Claude manual PreCompact at 62426a1d2

The user ran `/compact` in the trusted Claude session. The terminal
reported that the project `.claude/hooks/pre-compact.sh` completed
successfully and returned the state snapshot for `codex/w07-brief` at
`62426a1d2` with zero changed files. Claude also reported that compaction
finished. The terminal separately reported a plugin PreCompact success.
The project result is the evidence for this check. The pasted result
reported success without displaying a numeric exit code.

#### Claude Stop retry at 62426a1d2

In the earlier 07:42 trial, the session reported a Stop reminder with
`preventedContinuation: false`. That trial ended without a retry.

In the later trial, the user reported that the project Stop blocked the
turn and named the uncommitted Task. A filtered read of that Claude
session's hook diagnostics verified the project block feedback and the
first `.claude/hooks/stop.sh` completion at 23:14:22.131 UTC. It also
verified the next project Stop completion at 23:14:31.547 UTC with exit
code 0. The trace contains no intervening UserPromptSubmit completion
and no further project block response in the retry group. This records
the project hook's retry outcome separately from plugin hooks.

The same diagnostic read found PostToolUse completion codes for plugin
hooks. No project PostToolUse exit code was available for the monitored
synthetic Edit. The earlier project invocation and process completion
remain the only confirmed results for that test.

#### Claude project PostToolUse exit at 62426a1d2

A separate trusted Claude trial bound only the ignored synthetic README.
Its native Edit changed `v1` to `v2`. The user supplied the filtered
completion result from the project `.claude/hooks/post-tool-validate.sh`
route, `2026-11-15T23:35:01.179Z PostToolUse:Edit exit=0`. This records
the project hook process's exit status. The internal validator's
outcome requires separate evidence.

#### W07-ADAPTER 4.2.0 recheck

The 2026-11-18 W07-ADAPTER request read D17, D08 and D07 of the 4.2.0
package at `94f551cb6`. D17 adds the separation of preparation failure from
target denial, the meaning of a reached boundary, and the rule to keep both
the official text and the installed observation when they differ. D08 adds
the brief rules that TSK-0078 rechecked. D07 adds capture and scheduled
analysis rules owned by W08-CAPTURE and W08-ANALYSIS. No attachment
disposition targets W07-ADAPTER; D-A03 assigns projection checks to
RUNTIME-CLOSE. No external source was rechecked.

Since `ffc3247ce` the dispatcher, hook wrappers, Provider Registry bindings
and settings are unchanged. `.claude/provider.md` gained only the owner
attribution of four deny rules, and the renderer change concerns README
forms. Renderer drift is zero and the governance contract passes. The
installed CLIs report Claude Code 2.1.326 and codex-cli 0.169.0. The
adapter keeps the documented `onFailure` translation and states that a
timeout denial has not been observed, as D17 requires.

This continued Claude session observed the project hooks on the Bash route,
beyond the earlier Edit route evidence:

| Observation | Route | Result |
| --- | --- | --- |
| `hookify.block-direct-main-push` | PreToolUse Bash | Denied `git push origin --delete` and an explicit `:refs/heads/` deletion run from `main`; the deletions then used the GitHub API. The rule over-approximates a branch deletion from `main` as a main push; this is recorded, not changed |
| `hookify.warn-pre-commit-manual` | PreToolUse Bash | Warning delivered as context for a command that only contained the text `pre-commit run` |
| `hookify.warn-conventional-commit` | PreToolUse Bash | Warning delivered for a valid subject followed by a second `-m` body, a false positive |
| `code-reviewer` subagent | Native role tools | The reviewer reported having no Bash and used Read and Grep only; this shows its configured tool set, not a tested shell or sensitive-path denial |

The commit warning pattern took the last `-m` through a greedy `.*`, so any
body paragraph after a valid subject warned, and it missed a combined flag
such as `-am`. The rule now reads only the first message flag, including
combined short flags. The regression first failed on two valid commands and
one invalid `-am` command, then passed. In this session the native hook then
warned for an `echo` of `git commit -m "unknown: Subject" -m "docs: Body"` and
stayed silent for `git commit -q -am "fix(ci): Subject" -m "Body paragraph."`.

Unsupported pre-tool output, the reviewer shell and sensitive-path denials,
worker dispatch, the Codex desktop reviewer write-open failure, and capture
and memory integration remain unobserved here. RUNTIME-CLOSE owns the native
matrix and W08-CAPTURE owns the collector.

#### RUNTIME-CLOSE native adapter observations

The 2026-11-18 RUNTIME-CLOSE request ran these owner-authorized cases with
synthetic files only. No repository or managed setting changed.

| Case | Client and input | Observed |
| --- | --- | --- |
| Claude reviewer tools | `code-reviewer` subagent in this session | Tools are Read, Grep and Glob; no write, edit or shell tool exists |
| Claude reviewer sensitive path | Read of a synthetic file under a scratch `secrets/` directory, with a normal synthetic file as positive control | Positive control read; the `secrets/` file refused: "File is in a directory that is denied by your permission settings." |
| Claude malformed PreToolUse output | Headless Claude Code 2.1.327, `--setting-sources project`, `acceptEdits`, a temporary project whose Write hook returns truncated JSON, an explicit deny or nothing, chosen by file name | The hook ran for all three Writes. No output: created. Truncated JSON: created, so the tool ran. Explicit deny: refused with the hook's reason, file absent. One run, $0.23 |
| Codex read-only sandbox | codex-cli 0.169.0 `exec --sandbox read-only --ephemeral` in a temporary directory | BLOCKED: the account usage limit failed the turn before any tool call; the target was not reached and nothing was written |

The malformed case shows that Claude proceeds when a PreToolUse hook prints
invalid JSON and exits 0. The repository dispatcher emits every denial with
`json.dumps` and turns its own import failure into a denial, so it does not
produce that output. The probe hook carried no `onFailure` key, so whether
the repository's `onFailure: block` binding fails closed on invalid output is
still unobserved. The reviewer cases show the configured tool set and a
permission-rule refusal; they are not a sandbox test of a shell.

At the owner's direction, a second headless run used the same synthetic
project with the repository's hook form, `"timeout": 30` and
`"onFailure": "block"`, and a fourth file whose hook exits 1. On Claude Code
2.1.327 all four Writes reached the hook. No output and truncated JSON with
exit 0 were created. Exit 1 was refused with "failed; blocking because
onFailure is \"block\"" and the hook's stderr. The explicit deny was refused
with its reason. One run, $0.23. The key therefore fails closed on a hook
failure but does not cover invalid output on exit 0, which the dispatcher
avoids by always printing a well-formed decision. `.claude/provider.md`
now states this. Timeout behavior remains unobserved.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0079 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0079 | ready | in-progress | #design-before-implementation |

### Blockers and Decisions

GitHub read-only status showed PRs 1047 and 1048 open. Local work stayed on
`codex/w07-brief`, the branch already carrying the prerequisite changes.
The installed Git configuration reports no explicit `core.hooksPath`.
Native permission tests need a trusted test profile and disposable
role-scoped targets. An isolated Claude probe requires operator-controlled
project trust before it can supply the missing delivery evidence.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Long lifecycle regression before fix | 135 | W140 | long event command tests | fbac0fde1 dispatcher with new tests | FAIL | Both provider formats fail on environment argument length, four failing subcases | required | - |
| Long lifecycle regression after fix | 135 | W140 | long event command tests | W140 dispatcher and tests | PASS | Startup and Stop retry succeed with 140,000-byte synthetic values | required | Long lifecycle regression before fix |
| Configured hook commands | 135 | W140 | commands from both project hook JSON files | Synthetic long Stop retry and malformed PreToolUse JSON | PASS | Silent retry, exact supported deny output, exit 0 | required | - |
| Local suites | 135 | W140 | governance CI routing, folder guides, request brief, tool payload and ownership unittest suites | W140 source with synthetic inputs | PASS | 159 tests, exit 0 | required | - |
| Provider and manifest checks | 135 | W140 | governance contract all, provider renderer check and script manifest | W140 Registry, settings and tracked source | PASS | Zero failures or drift, exit 0 | required | - |
| Independent adapter review | 135 | W140 | staged source and event contract inspection | W140 dispatcher, Registry, binding and manifest against fbac0fde1 | PASS | Retry preserved, no stale SessionEnd route, no material finding | required | - |
| Initial Task metadata and lifecycle | 135 | W140 | document metadata check-changed and corpus lifecycle | Initial W140 Spec, Plan and Task | FAIL | Missing the required Task transition chain, exit 1 | required | - |
| Updated Task metadata and lifecycle | 135 | W140 | document metadata check-changed and corpus lifecycle | W140 Stage 03 paths against fbac0fde1 with explicit transitions | PASS | Three selected documents and corpus lifecycle report zero violations, exit 0 | required | Initial Task metadata and lifecycle |
| Authored source and navigation | 135 | W140 | ShellCheck, bash -n, Ruff, document links alignment and commands, graphify update | W140 source and local navigation | PASS | Checks exit 0, navigation rebuilt from AST, optional SQL and HCL extraction dependencies absent | optional | - |
| Codex desktop scope | 135 | W140 | live UserPromptSubmit and PreToolUse | Active managed desktop session, W140 exact paths | PASS | In-scope Task patch applied and inert out-of-scope README patch denied | required | - |
| Claude native delivery | 135 | W140 | native Claude SessionStart delivery | Claude 2.1.325, isolated init-only and projected project settings | NOT_RUN | Project hook found, trust or permission notice, no hook execution evidence | required | - |
| Native malformed output | 135 | W140 | native unsupported-pretool-output control case | Both provider runtimes | NOT_RUN | No disposable trusted runtime with the control input observed | required | - |
| Native reviewer boundaries | 135 | W140 | shell write and sensitive path denial | Both provider review roles | NOT_RUN | Effective role permission and denial have no witness | required | - |
| Native cross-provider integration | 135 | W140 | capture, memory and worker dispatch witness | Both provider runtimes | NOT_RUN | Capture and memory are W08 dependencies and native dispatch needs an authorized worker fixture | required | - |
| Resume focused verification | 135 | W140 | focused unittest, governance contract all, renderer and manifest | e2c307bcc and installed clients | PASS | 31 tests, zero projection drift, all four commands exit 0 | required | - |
| Installed Codex discovery probe | 135 | W140 | app-server hooks/list discovery | Codex CLI 0.169.0 with an isolated temporary profile | PASS | Native protocol responded and reported zero project hooks in that profile | optional | - |
| Resume Claude native delivery | 135 | W140 | native Claude SessionStart delivery | Claude 2.1.325, isolated init-only and stream-json in a disposable profile | NOT_RUN | Hook found in startup trace, trust or permission notice, no hook result | required | - |
| Codex CLI native sandbox probe | 135 | W140 | read-only launcher and synthetic write-open | Codex 0.169.0 CLI and app-server | NOT_RUN | Server permission request timed out and launcher did not reach the target | required | - |
| Codex desktop reviewer write-open | 135 | W140 | normal reviewer shell open of a synthetic file | Managed desktop code-reviewer and disposable temporary path | FAIL | Write-mode open succeeded without an override, fixture content untouched | required | - |
| Resume evidence review | 135 | W140 | independent document diff and witness scope | TSK-0079 and authored Codex adapter against e2c307bcc | PASS | Review distinguished write-mode open from a file mutation and CLI role isolation | optional | - |
| Existing-profile Claude startup | 135 | W140 | native Claude SessionStart delivery | Claude 2.1.325, abf8d6b9b workspace, interactive startup and init-only preflight, no model prompt | NOT_RUN | Read-only filesystem error observed and no hook lifecycle result | required | - |
| Nested Codex namespace preflight | 135 | W140 | native read-only launcher and bubblewrap namespace preflight | Codex 0.169.0, abf8d6b9b workspace, nested runtime | ERROR | Launcher stopped at socket directory check and both bubblewrap preflights denied namespace creation | optional | - |
| Codex native CLI read-only control | 135 | W140 | read-only launcher and synthetic write-open | Installed Codex 0.169.0 and approved host launch | PASS | CLI allowed the ordinary read and denied write-open with EROFS | required | Codex CLI native sandbox probe |
| Codex native CLI protected read control | 135 | W140 | explicit deny profile with managed config enabled | Installed Codex 0.169.0 and synthetic protected directory | PASS | Workspace HEAD and ordinary read allowed, write-open EROFS, protected read EACCES | required | - |
| Trusted Claude SessionStart | 135 | W140 | native Claude SessionStart delivery | Reported interactive Claude session, f05d4e805, project settings | PASS | Project context delivered to the session | required | Claude native delivery, Resume Claude native delivery, Existing-profile Claude startup |
| Trusted Claude UserPromptSubmit | 135 | W140 | native Claude UserPromptSubmit delivery | Reported interactive Claude session, f05d4e805, project settings | PASS | Project brief notice delivered and request state readable | required | - |
| Trusted Claude in-scope allow | 135 | W140 | native Edit under a bound brief | Gitignored synthetic in-scope fixture, f05d4e805 | PASS | Native Edit proceeded under existing permissions and digest changed v0 to v1 | required | - |
| Trusted Claude out-of-scope deny | 135 | W140 | native Edit outside the bound brief | Gitignored synthetic out-of-scope fixture, f05d4e805 | PASS | Hook denied before execution, digest, size and mtime unchanged | required | - |
| Trusted Claude Stop continuation | 135 | W140 | live Stop with an uncommitted Task change | Same session, f05d4e805 | PASS | Project Stop blocked the first stop, named the uncommitted Task path and continued the turn | required | - |
| Trusted Claude PostToolUse process delivery | 135 | W140 | native PostToolUse invocation and process completion | Reported trusted Claude session, b3cff1273, native Edit of a scoped synthetic file | PASS | Dispatcher and child observed, both ended, fixture changed from v1 to v2 | optional | - |
| Trusted Claude PostToolUse exit status | 135 | W140 | native PostToolUse exit-status witness | Synthetic Edit process monitor and later filtered hook diagnostics | NOT_RUN | Monitor captured no exit code and the diagnostic completion codes identified plugin hooks | required | - |
| Trusted Claude project PostToolUse exit | 135 | W140 | native PostToolUse exit-status witness | User-filtered project hook result from a separate native Edit at 62426a1d2 | PASS | PostToolUse:Edit exited 0 at 2026-11-15T23:35:01.179Z | required | Trusted Claude PostToolUse exit status |
| Trusted Claude PreCompact | 135 | W140 | native PreCompact witness | Reported trusted Claude session | NOT_RUN | Planned trigger only, no invocation or completion reported | required | - |
| Trusted Claude manual PreCompact completion | 135 | W140 | native PreCompact witness | Reported trusted Claude session, manual /compact at 62426a1d2 | PASS | Project hook reported successful completion and returned its state snapshot, compaction finished | required | Trusted Claude PreCompact |
| Trusted Claude Stop retry | 135 | W140 | silent native Stop retry witness | Reported trusted Claude session | NOT_RUN | Closing reminder and turn end observed, no same-turn block and retry pair reported | required | - |
| Trusted Claude project Stop retry completion | 135 | W140 | silent native Stop retry witness | Trusted Claude hook diagnostics and reported first block, 62426a1d2 | PASS | Same-turn project retry exited 0 with no further project block response | required | Trusted Claude Stop retry |
| Reported Claude Task metadata | 135 | W140 | document metadata | Claude-authored Task snapshot before reconciliation | PASS | Session reported 92 documents selected, zero violations and exit 0 | optional | - |
| 4.2.0 commit warning RED | 135 | W140 | commit contract translation test | Two valid multi-message commands and one invalid `-am` command at `94f551cb6` | FAIL | Two false warnings and one missed warning | required | - |
| 4.2.0 commit warning GREEN | 135 | W140 | commit contract translation test | First-message-flag pattern | PASS | All cases pass; adapter and governance routing modules pass, renderer drift zero, governance contract clean | required | 4.2.0 commit warning RED |
| 4.2.0 native Bash hook route | 135 | W140 | live PreToolUse Bash in this Claude session | Main push denial, two warnings and the corrected commit pattern | PASS | Deny and warn delivered on the Bash route; corrected pattern warned on the invalid probe and stayed silent on the valid one | optional | - |
| RUNTIME-CLOSE Claude reviewer | 135 | W140 | live subagent tool list and Read | `code-reviewer` subagent, synthetic public and `secrets/` files | PASS | No write or shell tool; positive read allowed; sensitive path refused by permission settings | required | - |
| RUNTIME-CLOSE Claude malformed output | 135 | W140 | headless PreToolUse output control | Claude Code 2.1.327, synthetic project hook, three Writes | PASS | Invalid JSON let the Write run; explicit deny refused it; no output allowed it | required | - |
| RUNTIME-CLOSE Codex sandbox | 135 | W140 | read-only exec write attempt | codex-cli 0.169.0, synthetic directory | NOT_RUN | Blocked by the account usage limit before any tool call; target not reached | required | - |
| RUNTIME-CLOSE Claude onFailure | 135 | W140 | headless PreToolUse failure control | Claude Code 2.1.327, synthetic project hook with `onFailure: block`, four Writes | PASS | Exit 1 refused by onFailure; invalid JSON on exit 0 still ran; explicit deny refused; no output allowed | required | - |

### Resolution Links

The focused command suite resolves the length regression. The lifecycle
table resolves the authoring check failure. The trusted interactive
SessionStart witness resolves the earlier missing Claude startup delivery
evidence for criterion 135. The isolated startup observations retain their
original outcomes. The manual PreCompact completion resolves the earlier
missing PreCompact witness. The later same-turn Stop pair resolves the
missing retry witness. The filtered exit code from a separate native
Edit resolves the missing project PostToolUse exit-status witness.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 135 | pending | Trusted Claude SessionStart, Trusted Claude UserPromptSubmit, Trusted Claude in-scope allow, Trusted Claude out-of-scope deny, Trusted Claude Stop continuation, Trusted Claude manual PreCompact completion, Trusted Claude project Stop retry completion, Trusted Claude project PostToolUse exit | Owner @buenhyden chose per-criterion acceptance on 2026-11-16 in this chat; held by unresolved required rows Native malformed output, Native reviewer boundaries, Native cross-provider integration and Codex desktop reviewer write-open | @buenhyden |

### Remaining Conditions

A trusted Claude session observed SessionStart and UserPromptSubmit
delivery and a PreToolUse allow and deny on the native Edit route only.
The Claude evidence also covers manual PreCompact success, a project
Stop block followed by a successful same-turn retry, and a native Edit
whose project PostToolUse hook exited 0.
The Codex desktop hook pass covers the observed edit route. Its separate
reviewer write-open failure remains unresolved. RUNTIME-CLOSE observed the
Claude reviewer boundaries, nested worker dispatch and malformed output.
The Codex read-only sandbox run was blocked by the account usage limit.
`onFailure: block` refused a failing hook but not invalid output on exit 0,
and hook timeout, automatic capture and memory evidence remain open. W08-CAPTURE owns the protected
collector and null or delayed transcript reconciliation. Owner acceptance
depends on the required observations.

## Handoff

### Promotion Receipt

The dispatcher, Provider Registry and authored provider adapter own the
behavior. This Task records the execution and acceptance.

### Next Owner

RUNTIME-CLOSE owns the Codex sandbox and reviewer cases after the usage
limit resets, and W08-CAPTURE the collector. The owner decides criterion
135.
