---
title: "W07 Native Provider Adapter Task"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-16"
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
| Claude native delivery | 135 | W140 | isolated init-only and trusted delivery acceptance | Claude 2.1.325, projected project settings | NOT_RUN | Project hook found, trust or permission notice, no hook execution evidence | required | - |
| Native malformed output | 135 | W140 | native unsupported-pretool-output control case | Both provider runtimes | NOT_RUN | No disposable trusted runtime with the control input observed | required | - |
| Native reviewer boundaries | 135 | W140 | shell write and sensitive path denial | Both provider review roles | NOT_RUN | Effective role permission and denial have no witness | required | - |
| Native cross-provider integration | 135 | W140 | capture, memory and worker dispatch witness | Both provider runtimes | NOT_RUN | Capture and memory are W08 dependencies and native dispatch needs an authorized worker fixture | required | - |
| Resume focused verification | 135 | W140 | focused unittest, governance contract all, renderer and manifest | e2c307bcc and installed clients | PASS | 31 tests, zero projection drift, all four commands exit 0 | required | - |
| Installed Codex discovery probe | 135 | W140 | app-server hooks/list discovery | Codex CLI 0.169.0 with an isolated temporary profile | PASS | Native protocol responded and reported zero project hooks in that profile | optional | - |
| Resume Claude native delivery | 135 | W140 | isolated init-only and trusted delivery acceptance | Claude 2.1.325 and stream-json in a disposable profile | NOT_RUN | Hook found in startup trace, trust or permission notice, no hook result | required | - |
| Codex CLI native sandbox probe | 135 | W140 | read-only launcher and synthetic write-open | Codex 0.169.0 CLI and app-server | NOT_RUN | Server permission request timed out and launcher did not reach the target | required | - |
| Codex desktop reviewer write-open | 135 | W140 | normal reviewer shell open of a synthetic file | Managed desktop code-reviewer and disposable temporary path | FAIL | Write-mode open succeeded without an override, fixture content untouched | required | - |
| Resume evidence review | 135 | W140 | independent document diff and witness scope | TSK-0079 and authored Codex adapter against e2c307bcc | PASS | Review distinguished write-mode open from a file mutation and CLI role isolation | optional | - |
| Existing-profile Claude startup | 135 | W140 | native interactive startup and init-only delivery preflight | Claude 2.1.325, abf8d6b9b workspace, no model prompt | NOT_RUN | Read-only filesystem error observed and no hook lifecycle result | required | - |
| Nested Codex namespace preflight | 135 | W140 | native read-only launcher and bubblewrap namespace preflight | Codex 0.169.0, abf8d6b9b workspace, nested runtime | ERROR | Launcher stopped at socket directory check and both bubblewrap preflights denied namespace creation | optional | - |
| Codex native CLI read-only control | 135 | W140 | read-only launcher and synthetic write-open | Installed Codex 0.169.0 and approved host launch | PASS | CLI allowed the ordinary read and denied write-open with EROFS | required | Codex CLI native sandbox probe |
| Codex native CLI protected read control | 135 | W140 | explicit deny profile with managed config enabled | Installed Codex 0.169.0 and synthetic protected directory | PASS | Workspace HEAD and ordinary read allowed, write-open EROFS, protected read EACCES | required | - |

### Resolution Links

The focused command suite resolves the length regression. The lifecycle
table resolves the authoring check failure. Those checks supply no native
evidence for the remaining observations.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 135 | pending | - | Owner decision after verification | @buenhyden |

### Remaining Conditions

Trusted Claude hook delivery and allow or deny decisions remain open.
The Codex desktop pass covers the observed route. Unsupported-output
behavior, native reviewer isolation, worker dispatch and automatic
capture and memory evidence remain open. W08-CAPTURE owns the protected
collector and null or delayed transcript reconciliation. Owner acceptance
depends on the required observations.

## Handoff

### Promotion Receipt

The dispatcher, Provider Registry and authored provider adapter own the
behavior. This Task records the execution and acceptance.

### Next Owner

The implementer owns W140. The owner decides criterion 135.
