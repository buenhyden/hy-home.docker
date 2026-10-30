---
title: "Native Memory Controlled Verification Task"
version: "0.1.24"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "specs"
artifact_id: "SPEC-0244-TSK-0001"
parent_ids:
- "SPEC-0244-PLAN-0001"
created: "2026-10-16"
---

# Native Memory Controlled Verification Task

## Overview

### Objective

Record only what an authorized, non-mutating native-session verification can
prove about memory and hooks, with unsupported state left visible as
unverified or unknown.

## Inputs and Authorization

- **Request:** on 2026-10-16 the owner asked to continue Claude memory-off
  and hook verification as part of the bounded operational follow-up.
- **Authorization boundary:** a normal Claude session may use the approved
  read-only status and menu actions. After it proves effective memory-off, one
  provider prompt may read and write only the exact ignored fixture, with at
  most three turns, USD 0.10, strict empty MCP, and no Chrome, Bash, or network
  tools. It may not read or write native/shared memory, change settings or
  trust, inspect raw private diagnostics, or widen the fixture boundary.
- **Baseline:** `main` `89eb43f683a11587cf4f125be534ae720c20a55c`.
- **Related evidence:** SPEC-0212 TSK-0009 contains the prior sanitized menu
  observation. It is historical input only; this Task does not reopen it.

## Work Log

### Initial State

The approved Spec and Plan define W1 through W6. No new native-session action
has run under this Task.

### Spec Approval

The direct 2026-10-16 user authorization approved the bounded SPEC-0244
contract before this Task was created.

### Plan Approval

The same direct authorization approved SPEC-0244-PLAN-0001's bounded work and
verification sequence before this Task was created.

### Ready Transition

On 2026-10-16, a security review approved one final non-mutating UI attempt
that recognizes only the provider-exposed `Auto-memory` boolean, without
activating its control. The same review approved the conditional fixture probe
only after the UI proves effective memory-off: one exact ignored-fixture
read/write prompt, at most three turns and USD 0.10, strict empty MCP, no
Chrome/Bash/network tools, raw-output disposal, and wrapper cleanup. This
reviewed plan is sufficient to make the Task `ready`; it is not an attempt,
effective-memory proof, fixture execution, or hook-delivery receipt.

### In-progress Observation

The approved final UI attempt started and completed on 2026-10-16. Its
event-name-only wrapper witnessed `SessionStart=1` and `SessionEnd=1`, but the
provider's effective `Auto-memory` boolean remained unknown. No provider
prompt or tool ran, so the conditional fixture probe remains `NOT_RUN`.

The attempt also left thirteen newly created zero-byte untracked markers in an
older isolated native checkout. The markers contain no observed payload, but
their cleanup remains a required open finding. Security approved a narrowly
proven-new cleanup method; its cause and execution result remain separate from
this observation until recorded.

### Lifecycle Delivery Note

The first post-draft source commit recorded the already observed `draft` to
`ready` planning event and the subsequent `ready` to `in-progress` UI attempt
together. It contains both registered direct-edge rows but no separate ready
Git snapshot. This is a delivery-granularity limitation, not a claim that a
direct `draft` to `in-progress` transition occurred. Future transitions record
one clear actual event per commit where practical.

### Cleanup Follow-up

The thirteen proven-new zero-byte markers in the old isolated checkout were
removed and its Git status returned to the recorded state. A privacy environment
scrub also created eight proven-new zero-byte placeholders at a user-global
location. Automatic deletion there was rejected because it would mutate global
state; four ambiguous files and all directories remain untouched. The owner
then approved guarded removal of exactly those eight proven-new files, which
completed without touching the retained entries. No provider retry or further
probe ran.

### Forced-off Hook Delivery Plan

Security approved one conditional, session-only hook-delivery attempt after the
guarded global cleanup. It sets `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` for that
session only and does not use the privacy-environment scrub that created the
placeholders. Its sole successful label is
`HOOK_DELIVERY_VERIFIED_WITH_SESSION_FORCED_MEMORY_OFF`. The attempt is a
distinct hook-delivery proof class: it neither changes configuration nor proves
that the normal merged project setting is effectively off, so criterion 3
remains pending. The operator may start the one frozen attempt after this Task
record; all other boundaries and stop conditions in the approved plan remain
in force.

### Forced-off Hook Attempt

The one authorized forced-off provider attempt failed closed at startup with
exit 1. It produced no stdout; stderr was discarded. No hook, tool, or model
output occurred and no timeout was observed. Therefore its sole successful
label was not earned. The normal no-model UI observation remains limited to
`SessionStart=1` and `SessionEnd=1`, and normal merged auto-memory remains
unknown.

### Forced-off Hook Retry 02 Plan

Security approved one fresh retry plan with digest
`4f59ea1279ac9233b50cc33262a3ca50a3015920a6b1f1ce37280e389d92e414`.
It is session-only forced-off with `sandbox=false`, so it makes no OS
confinement claim. The task-owned witness accepts only the exact guarded
fixture `Write` payload and denies every other operation. The attempt permits
no Read, Bash, or MCP tool; it has at most two turns, USD 1, and 180 seconds.
It is one new retry only. Guard tests passed before release. Normal merged
auto-memory remains unknown, and this plan does not change its criterion.

### Forced-off Hook Retry 02 Result

The retry's local route, shim, atomic, and guard preflight checks passed, but
the provider attempt again failed closed before hook initialization: exit 1,
stderr-only output discarded, and zero events, tools, or model output. Exact
cleanup and Git-status restoration passed. A separate no-session static
validation found that an empty `--mcp-config '{}'` argument is rejected as
`Invalid MCP` before lifecycle initialization; an empty wrapped `mcpServers`
form is rejected too. This static diagnosis is not a retained provider stderr
receipt. No third attempt ran under the cap.

### Forced-off Hook Retry 03 Plan

Security independently approved one fresh, frozen retry only after the pinned
Claude Code 2.1.301 headless path and its asserted binary identity showed that
literal `--strict-mcp-config`, with no `--mcp-config` argument, selects empty
MCP servers. The approved harness digest is
`98af87fab954dc515d54f43153bab36966f328a2137ed64868eda97c9b2ebc02`.

The prior no-further-attempt cap is amended only for this distinct 03 retry:
both earlier attempts reached no provider lifecycle, hook, tool, or model
output, and the static diagnosis identified the invalid empty MCP argument
that this plan removes. This is not general retry authority or a claim that a
usage limit was reached. The owner has continued to authorize the requested
verification, subject to this review and a Task release.

Retry 03 keeps every Retry 02 guard: a session-only forced-memory-off setting,
`sandbox=false` with no outer OS-confinement claim, a named tracked witness,
only the exact guarded fixture `Write`, no Read, Bash, or MCP tool, and at
most two turns, USD 1, and 180 seconds. Normal settings, hooks, inherited
authentication, and environment remain active. A public `mcp list` attempt
timed out while health-checking normally approved servers, because that
subcommand does not use the headless strict resolver; it supplies no dynamic
proof. No child process remains and no further list attempt is planned.

Retry 03 has not started. It can start once the root releases this exact
reviewed plan. It cannot prove normal merged auto-memory is off; that state
remains unknown. Its only successful hook-delivery label remains
`HOOK_DELIVERY_VERIFIED_WITH_SESSION_FORCED_MEMORY_OFF`.

### Forced-off Hook Retry 03 Result

The released retry exited 0 with a valid stream and no stderr. It reached one
final token and one `Write` tool. The tracked wrapper delivered
`SessionStart=1`, `UserPromptSubmit=1`, `PreToolUse=1`, `Stop=1`, and
`SessionEnd=1`; `PostToolUse=0` and `PreCompact=0`. No output file or exact
output was retained, and one nested-Bash token was classified `UNEXPECTED`.

The required full label was therefore not earned. This is a failed-closed,
partial delivery receipt, not proof of complete hook delivery or a normal
merged memory-off state. Cleanup and Git-status restoration passed. No further
retry is planned.

### Normal Settings Memory Control Query Plan

Security approved one normal-settings, read-only memory-control query with
plan SHA-256
`a30ac627797ebb013c9e6f9b87cf56f4b544f70e2e908a24b55a8543e811565c` and
harness SHA-256
`bf8baf16b7a3d64317f64c2d9e74e8f3f16061489577717b833baf1188555eda`.
It may only initialize a session, call `get_memory_dialog`, and end the
session. It may not invoke a model, user prompt, tool, or MCP.

The query uses `sandbox=false` and makes no OS-confinement claim. It leaves
memory settings unchanged; forced-off, safe, simple, and scrub environment
controls are absent. Transient private rows are discarded, retaining only the
classified Boolean or enum result. `enabled=false` with a plain off result is
the only merged-off PASS. An enabled/on result is known ON; unavailable or
safe results are narrower classifications; any other result remains unknown.

Normal startup authentication, configuration, update, and telemetry effects,
along with SessionStart/SessionEnd shared-DB effects, remain residual
boundaries. The query has not started and can run once after this Task record
is released; it neither accepts criterion 3 nor changes the prior normal
merged state from unknown.

### Normal Settings Memory Control Query Result

The one released normal-settings query completed with the classified result
`CLAUDE_NORMAL_MERGED_AUTO_MEMORY_OFF_VERIFIED`. Its sanitized result was
`enabled=false` with a plain off status, no detail, a settings-source suffix,
and `toggleable=false`. Initialization, `get_memory_dialog`, and session end
succeeded; the process exited 0 with no stderr, timeout, model, user prompt,
tool, MCP, permission event, or status change.

The sanitized receipt SHA-256 is
`e24e56cbfc5c2a022462029df4f3c2c686603bffb110d27b76d7ea1c7679015f`; the
sanitized observation SHA-256 is
`a245a0d61d190482d0985c3dd89312b655072202d8f3c7993b70240a5b574a1f`.
Independent security review confirmed this normal merged memory-off claim.
The earlier UI observation remains historical `UNKNOWN`; it is superseded only
for the normal effective-memory result. The forced-off hook Retry 03 remains
partial, with `PostToolUse` and complete Write delivery unverified.

### Forced-off Hook Attempt 04 Plan

Security independently approved one final forced-off session attempt with plan
SHA-256
`b1511ff25ffb89b0d7050bf9f506f7733d50b8e2622267f5681875d1fbacc6ae` and
harness SHA-256
`3105c920cb2a2250f58a7f8f917c24d449d441d9dc3dcb93b69f42d1661978c2`.
It retains a session-only forced-memory setting and `sandbox=false`, with no
OS-confinement claim. The offered provider capability is exact-fixture Write
only, bounded to two turns, USD 1, and 180 seconds.

The harness has explicit exact rules for both Write and Edit dispatches, but
the offered attempt allows Write only. Its nested dispatcher reports known
counts transparently through the new decision categories; those counts are
not promoted to delivery proof. It permits only known zero-to-two
line-feed-delimited markers, bounds raw pipes, requires empty stderr, pins 11
source paths through `O_NOFOLLOW`, and rechecks the guard directory before
use. No raw payload, memory body, credential, or private diagnostic may enter
Task evidence.

Attempt 04 has not run. Root GO is conditional on this Task receipt and an
immediate hash recheck, after which exactly one post-completion diagnostic may
run. It cannot change the accepted normal merged memory-off result, and it
does not turn Retry 03's partial hook evidence into complete delivery proof.

### Forced-off Hook Attempt 04 Result

Attempt 04 produced the sanitized receipt SHA-256
`89ea175746a446cb58b3c1dbc068e418a2b1ebc194b540529a78c87026aa0d2a` with
classification `HOOK_DELIVERY_PROBE_FAILED_CLOSED` and
`provider_probe_ok=false`. The process exited 0 while the harness returned 1;
there was no timeout, cap breach, or stderr. Stdout was present and a final
token was observed.

The exact offered Write was observed once, but its tool result was an error
with string content and output was absent. The only guard decision was
forwarded, not denied: the root, input, tool, path, normalized path, marker,
fixture, runtime, binary identity, and output-absent checks were all true;
the marker had one line feed. The Write never changed the filesystem.

Native and dispatcher each recorded `SessionStart=1`,
`UserPromptSubmit=1`, `PreToolUse=1`, `Stop=1`, and `SessionEnd=1`.
`PostToolUse=0`, `PreCompact=0`, and `PostToolValidate=0`; `UNKNOWN=1`.
Static review of the tracked project branch found no additional Bash and one
project Pre hook. The unknown event is therefore an inference of an additional
unclassified, non-project invocation, not an exact retained argv or path. It
may be a plugin or user layer, or a CLI Write internal Bash helper; the current
evidence does not distinguish those possibilities. The fail-closed shim
blocked it. Cleanup and status restoration passed (status SHA-256 prefix
`e3b0…`).

The security pre-execution GO covered the exact plan and harness; post-result
review remains pending. This failed-closed receipt leaves criterion 4 pending
and does not affect the accepted normal merged memory-off result.

### Metadata Validation Provenance

The full changed-document metadata check after SPEC-0244/Plan v0.1.1 alignment
exited 0 with seven selected documents, zero violations, zero legacy
exceptions, and zero transition overrides. It launched at `8219c9b` using the
same eight-path/base-`89eb43f683a11587cf4f125be534ae720c20a55c` selection as
the prior record. Task receipt edits occurred while it ran; the Spec, Plan,
and registry bytes were unchanged. This is not an immutable whole-worktree
snapshot, and later Task receipts rely on their own narrow checks.

### Merged Hook Listing Control Plan

Security approved one read-only merged-hook control query with plan
`/tmp/hyhome-r13-hooks-listing-control-plan.md` SHA-256
`75ccecddb0fc621e1225fd8e965f054a41dc7692a68253a532e6817e28bc3d40` and
harness `/tmp/hyhome-r13-run-hooks-listing-control-probe.py` SHA-256
`f92d170c438cea41ec8b5f5bbe8524eeb1c63e817b09659c959c08a5961d573c`. Its
sanitized receipt target is
`/tmp/hyhome-r13-native-hooks-listing-control-receipt.json`.

The control may only initialize a session, call `get_hooks_listing`, and end
the session. It may not mutate settings or invoke a model, user prompt, tool,
or MCP. It retains fixed enum/count aggregates only: an ECC Bash PreTool
candidate requires the same row to be active Write, untracked, plugin-hook
source, exact public ECC, and Bash command kind; generic additional and
tracked-only classifications are narrower alternatives. If the aggregate is
insufficient, it fails closed as
`CLAUDE_MERGED_PRETOOL_HOOKS_REMAIN_UNKNOWN`.

No raw hook listing, command, path, plugin name, label, error, configuration,
authentication, memory, user, model, tool, or MCP content may be retained or
emitted. No plugin or command hash and no per-hook row may enter the receipt.
The result can identify a candidate class only: it cannot validate or forward a
script, prove `PostToolUse`, or accept criterion 4. It has not run. Root may
release exactly this control after the Task receipt is committed.

### Merged Hook Listing Control Result

The released control completed with receipt SHA-256
`8345aa34cdf14e06f3d3fa0dbd7d16e372bbb87ea103bb3b8764260ee724d2fc` and
classification `CLAUDE_ADDITIONAL_PRETOOL_HOOK_IDENTIFIED`. It found 12
PreTool entries: six active Write entries, comprising one tracked project entry
and five plugin-hook entries. The aggregate command kinds were one Bash
(tracked project) and five Node (plugin); ECC, additional Bash, and their
intersection were each zero.

Initialization, listing, and session end succeeded with exit 0. There were no
user, assistant, model, tool, permission, MCP, or unexpected frames; stderr,
timeout, and malformed flags were false; repository status was equal and
empty. Raw/private fields and fingerprints were absent.

This removes an additional top-level Bash PreTool command as the explanation
for Attempt 04's unknown invocation. A nested Bash path from a plugin Node
hook or CLI internals remains possible. The control identifies neither script
delivery nor `PostToolUse`, so criterion 4 remains pending.

### Merged Hook Listing Classification Qualification

The immutable control receipt remains valid for transport and cleanup, but its
classifier undercounted the aggregate. The public ECC identifier is `ecc@ecc`,
where the prior allowlist expected a different identifier; `.*` matchers also
missed applicable rows. The actual plugin Write aggregate is seven rather than
the receipt's five. The receipt is retained unchanged with this qualification.

The control transport remains valid, but candidate attribution and counts are
not complete proof. Independent security review qualified the result on that
boundary. It cannot attribute Attempt 04's unknown invocation or establish
hook delivery, so criterion 4 remains pending.

### Native PostToolUse Attempt 05 Plan

Security approved one Native-05 diagnostic with plan
`/tmp/hyhome-r13-posttool-probe-plan-05.md` SHA-256
`139634cb63898f23d82dfa4a0d0892313655d13f102eb6741fd249eb486dba4f` and
harness `/tmp/hyhome-r13-run-native-hook-probe-05.py` SHA-256
`ce345a4ed7b1091f0607560f427623dfc452a5a32b9d7fee3e480692261d7e9e`. Its
prospective sanitized receipt is
`/tmp/hyhome-r13-native-hook-probe-receipt-05.json`.

The diagnostic retains normal merged memory OFF without an override and sets
`ECC_HOOKS_ENABLED=false` for this session only. It tests only named project
Claude native wrappers, dispatcher, and post validator; it makes no ECC plugin
delivery, global hook correctness, or OS-sandbox claim. The exact double-slash
Write permission and path/content guard is bounded to two turns, USD 1, and
180 seconds with strict no-MCP.

Raw stdout/stderr, authentication, session IDs, tool bodies, hook payloads,
memory rows, plugin-private identifiers, model and error text are excluded.
Only fixed enums/counts/booleans, public source identities, output hash/line
feed, and cleanup/status hashes may be retained. Same-UID TOCTOU, provider
authentication/telemetry, and non-ECC merged hooks remain residual boundaries.
The only full-pass label is
`POSTTOOLUSE_DELIVERY_VERIFIED_WITH_NORMAL_MERGED_MEMORY_OFF`. Attempt 05 has
not run; root may release exactly this plan after its Task receipt commits.

### Native PostToolUse Attempt 05 Result

Attempt 05 failed closed before provider launch. Its sanitized receipt SHA-256
is `7662bae15c4b64b47c862f4632edfc65b6a4d7cfa460a565273e7c84fbc78e5d` and
its classification is `HOOK_DELIVERY_PROBE_FAILED_CLOSED`. The ECC root mode
was 0775, causing `ecc_root_guard=false`; provider exit code is null.

There was no stdout, stderr, tool, or event. Guard tests passed 12/12; cleanup
passed and status was equal. No retry ran under the Attempt 05 plan. This does
not change the accepted normal merged memory-off result and leaves criterion 4
pending.

### Native PostToolUse Attempt 06 Plan

Security approved Native-06 as a correction to Attempt 05's preflight only:
plan `/tmp/hyhome-r13-posttool-probe-plan-06.md` SHA-256
`b63759b956db133f0c7f2a1ec6c430befb9dd4623df3c2dd14ac767f57803990`; harness
`/tmp/hyhome-r13-run-native-hook-probe-06.py` SHA-256
`e33dbd56a113285318ab5c9d7ef6ed90a921966a6e1ad93c9e553912ceac3d34`; receipt
target `/tmp/hyhome-r13-native-hook-probe-receipt-06.json`.

It verifies public ECC root mode 0775, private primary group, current-UID
exclusivity, the full nine-check chain, no ACL, and no other writer before
launch; immediate checks on the offline host passed 9/9 and guard tests passed
12/12. Attempt 05's session-only ECC disable, normal merged memory OFF, exact
Write boundary, two turns/USD 1/180 seconds, and no MCP remain unchanged.

The only full-pass label remains
`POSTTOOLUSE_DELIVERY_VERIFIED_WITH_NORMAL_MERGED_MEMORY_OFF`, limited to named
tracked project wrappers/dispatcher/post-validator in this ECC-disabled
session. It proves no ECC/Codex hooks, OS isolation, or broader provider
behavior. It retains fixed aggregates, public identities/hashes, guard
decisions, and exit/status/cleanup only; raw provider output, auth/session
data, hook payloads, private paths/content, and memory rows are excluded.
Sandbox remains disabled; same-UID/current-primary-group TOCTOU and ordinary
provider authentication/telemetry are residual. Attempts 01–05 remain
preserved. Attempt 06 has not run; root may release this exact plan once.

### Native PostToolUse Attempt 06 Result

Attempt 06 ran, but this Task did not record it. On 2026-10-30 the sanitized
receipt `/tmp/hyhome-r13-native-hook-probe-receipt-06.json` was read. The
receipt is dated 2026-10-16 10:20:59 KST, and its SHA-256 is
`1086eaa64f84bb83676e3f19efbe499e46935539b552bcfa787e3b4eda32be30`. It classifies
the run `HOOK_DELIVERY_PROBE_FAILED_CLOSED`: timed out at the 180-second cap,
exit 1, no final token, no stderr and no guard decision. Both Native and
Dispatcher counted one `UserPromptSubmit` and one `SessionEnd`. `SessionStart`,
`PreToolUse` and `PostToolUse` counted zero, and one `UNKNOWN` event token
appeared. Every preflight check passed, including the nine-check ECC chain,
and cleanup passed. So the session reached the prompt but never called Write.
`SessionStart` had counted one in earlier attempts and counted zero here. One
hypothesis is that the `UNKNOWN` event is a refused `SessionStart` that
stalls the session, but the receipt cannot show which event it was. Criterion
4 stays pending. Attempt 07 needs an owner decision: (a) make the harness
record the `UNKNOWN` event class and per-phase timings, then rerun after a
fresh security review; (b) stop W4 and leave criterion 4 pending; or (c) rerun
06 unchanged.

### Native PostToolUse Attempt 07 Plan

On 2026-10-30 the owner chose option (a): record the `UNKNOWN` event's class and
per-phase timing, then rerun after a fresh security review. The candidate
harness is
`/tmp/claude-1000/-home-hyunyoun-data-hy-home-docker/abdf464e-1ee1-47b0-a9b5-818d08efdd35/scratchpad/hyhome-r13-run-native-hook-probe-07.py`,
SHA-256 `a74f4984e8f8d89198e6e3148507051f01a817d4b4984573a501ab4b6204c81d`. Its
changes from 06:

- the -07 runtime, fixture and receipt paths;
- the Claude binary pinned at 2.1.312
  (`4f4178ce41d83e23341ebfbaecdbcf8ea6bf7baea0690025abe49eeec3a5d01d`), because
  2.1.301 is no longer installed;
- a shim line with the event name, argument count, a closed class (`known`,
  `native-argc`, `dash-c`, `empty`, `abs-other` or `rel-other`) and a
  millisecond clock, and never an argument value;
- receipt fields `unknown_event_details` (counts per argc and class) and
  `event_first_offset_ms` (earliest offset from launch per event).

The shim still refuses a `bash -c` call as `UNKNOWN`, so a refused user-level
hook would show as `dash-c`. An independent security review found no leak and
returned READY_WITH_NOTES. Its notes were applied: field-length bounds, counts
instead of a set, and the earliest offset. The re-review returned READY.

The owner must re-establish these before the single release:

- recreate `/tmp/hyhome-r13-governance` as a clean checkout of a named commit;
- re-hash the ten frozen tracked files, the ten ECC files and the binary in
  that checkout;
- re-confirm the ECC root identity `(64512, 4478294, 0775, 1000, 1000)` and the
  nine-component chain;
- confirm the -07 paths do not exist;
- hash the harness against the value above;
- record a security GO that names 2.1.312.

On 2026-10-30 the tracked hook files on `main` matched the frozen hashes for
`.claude/settings.json`, `session-start.sh` and `agent-event-hook.sh`, and the
ECC root identity was unchanged. Attempt 07 has not run.

### Native PostToolUse Attempt 07 Result

Attempt 07 ran once on 2026-10-30 from a clean governance worktree at `main`
`b6a1fb085`. All ten frozen tracked hashes and all ten ECC hashes matched, and
the harness hash was `a74f4984…`. The receipt
`/tmp/hyhome-r13-native-hook-probe-receipt-07.json` has SHA-256
`3af58d3424f8edd65fbfae2704df76f8a70c13ebbbea4e2f8ce6a44e249defa6`. It
classifies the run `HOOK_DELIVERY_PROBE_FAILED_CLOSED`, harness exit 1.

Hook delivery itself worked:

- Native and Dispatcher each counted one `SessionStart`, `UserPromptSubmit`,
  `PreToolUse`, `PostToolUse`, `Stop` and `SessionEnd`.
- `PostToolValidate-Check` counted one.
- The guard forwarded exactly one Write, the output was exact, the final
  token was seen, the provider exited 0, and there was no timeout or stderr.
- The first offsets were SessionStart at 1.4 s, PreToolUse at 4.9 s,
  PostToolUse at 5.3 s and SessionEnd at 7.6 s.

The 06 stall did not recur.

It failed closed for two reasons. First, there were seven `UNKNOWN` shim
calls, all of class `abs-other`: three with one argument and four with two.
The first came at 1.4 s, alongside SessionStart. Shell calls to absolute
paths outside the reviewed hook set are consistent with user-level plugin
hooks, which the session-only ECC disable does not cover. Second, the one tool
result's `is_error` was not a boolean (`UNKNOWN` 1), while the harness
expects `false` 1. Criterion 4 stays pending. An Attempt 08 would need either
user-level hooks excluded from the session, or the owner to accept foreign
`abs-other` calls and a missing `is_error` as outside the probe. It also needs
the harness to classify those cases, a fresh review, and a release.

### Native PostToolUse Attempt 08 Result

On 2026-10-30 the owner chose option (a) for Attempt 08: foreign shell calls to
absolute paths outside the reviewed hook set, and a missing `is_error` on the
tool result, are outside this probe. The shim still refuses and records them.
Harness 08 is
`/tmp/claude-1000/-home-hyunyoun-data-hy-home-docker/abdf464e-1ee1-47b0-a9b5-818d08efdd35/scratchpad/hyhome-r13-run-native-hook-probe-08.py`,
SHA-256 `7df03fae87f38c681ae6e0d01104f62d2c87562f14dac547136688e253d49acb`. It
differs from 07 in these ways:

- It adds `dispatcher-argv` and `repo-other` shim classes, so a repo hook is
  never excused.
- It passes the event check only when every `UNKNOWN` token is a classified
  `abs-other` line.
- It splits `is_error` into `ABSENT` and a non-boolean `UNKNOWN` and accepts
  only `false` or `ABSENT`.
- It adds two preflight guard tests and a `scope_exclusions` receipt field.

An independent security review returned READY_WITH_NOTES. Its four notes were
applied, and the re-review returned READY.

Attempt 08 ran once from a clean governance worktree at `main` `bdaab6d2e`. The
receipt `/tmp/hyhome-r13-native-hook-probe-receipt-08.json` has SHA-256
`44894122d868c9f0bb7eb82a5e4769c2d6f4a508fb4ac119ef7a2c73176a5481`. Its
classification is `POSTTOOLUSE_DELIVERY_VERIFIED_WITH_NORMAL_MERGED_MEMORY_OFF`,
with harness exit 0. Preflight passed, including all 14 guard tests. Native and
Dispatcher each counted one `SessionStart`, `UserPromptSubmit`, `PreToolUse`,
`PostToolUse`, `Stop` and `SessionEnd`, and `PostToolValidate-Check` counted
one. The guard forwarded exactly one Write, the output was exact, and the
final token was seen. There were seven foreign `abs-other` calls and one
`ABSENT` `is_error`, both within the stated scope. The label keeps its limits.
It covers the named tracked project wrappers, dispatcher and post-validator in
this ECC-disabled session with normal merged memory off, on Claude 2.1.312. It
does not cover ECC or Codex hooks, OS isolation, or user-level plugin hooks.
The row below resolves the earlier diagnostic failures with the same Check.
Criterion 4's acceptance is the owner's.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0244 | draft | approved | #spec-approval |
| SPEC-0244-PLAN-0001 | draft | approved | #plan-approval |
| SPEC-0244-TSK-0001 | draft | ready | #ready-transition |
| SPEC-0244-TSK-0001 | ready | in-progress | #in-progress-observation |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Initial native execution state | 1 | W1 | No controlled session, review, conditional fixture probe, or selected document gate had run when this Task was created | Initial record on `89eb43f683a11587cf4f125be534ae720c20a55c` | NOT_RUN | Initial State | optional | - |
| Ready security plan review | 1 | W1 | Independent security review approved the exact UI recognition rule and conditional fixture bounds | Sanitized security GO, Claude Code 2.1.301 | PASS | Ready Transition | required | - |
| Scoped metadata pre-ready attempt | 6 | W6 | `check-document-metadata.py --mode check-changed` | Session 60502 against `92b16fe`; cancelled before completion because the ready transition changed this Task source | CANCELLED | Ready Transition | optional | - |
| Final UI witness observation | 4 | W4 | Event-name-only wrapper witnesses SessionStart and SessionEnd around the final allowed UI attempt | `SessionStart=1`; `SessionEnd=1`; no provider prompt or tool | PASS | In-progress Observation | required | - |
| Effective memory-off view | 3 | W3 | Provider exposes a non-mutating effective Auto-memory value | Final UI attempt: value unknown; historical observation superseded for criterion 3 by Normal settings memory-control query result | NOT_RUN | In-progress Observation | optional | - |
| Conditional fixture probe | 4 | W4 | Exact ignored-fixture read/write provider prompt after effective-memory-off proof | Precondition not met because effective value is unknown | NOT_RUN | In-progress Observation | required | - |
| Native marker cleanup finding | 5 | W5 | Detect and remove only proven-new zero-byte markers from the old isolated native checkout | Thirteen untracked zero-byte markers; security-approved cleanup method not yet executed | FAIL | In-progress Observation | required | - |
| Local marker cleanup | 5 | W5 | Detect and remove only proven-new zero-byte markers from the old isolated native checkout | Thirteen proven-new zero-byte markers removed; Git status restored | PASS | Cleanup Follow-up | required | Native marker cleanup finding |
| Global marker cleanup boundary | 5 | W5 | Delete only proven-new zero-byte privacy-environment placeholders at the user-global location | Eight proven-new zero-byte files detected; automatic deletion rejected; four ambiguous files and all directories retained | FAIL | Cleanup Follow-up | required | - |
| Global marker cleanup | 5 | W5 | Delete only proven-new zero-byte privacy-environment placeholders at the user-global location | Guarded cleanup deleted all eight approved proven-new zero-byte files; four ambiguous files and all directories preserved | PASS | Cleanup Follow-up | required | Global marker cleanup boundary |
| Forced-off hook plan review | 4 | W4 | Security review of one session-only forced-off hook-delivery attempt without privacy-environment scrub | `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`; sole PASS label `HOOK_DELIVERY_VERIFIED_WITH_SESSION_FORCED_MEMORY_OFF`; normal merged effective-off remains unknown | PASS | Forced-off Hook Delivery Plan | required | - |
| Forced-off hook attempt | 4 | W4 | One approved session-only forced-off hook-delivery attempt | Startup exit 1; stdout absent; stderr discarded; zero hooks, tools, and model output; no timeout | FAIL | Forced-off Hook Attempt | required | - |
| Forced-off hook retry 02 plan review | 4 | W4 | Security review of one fresh session-only forced-off retry with guarded Write-only witness | Plan `4f59ea1279ac9233b50cc33262a3ca50a3015920a6b1f1ce37280e389d92e414`; sandbox false with no OS-confinement claim; no Read/Bash/MCP; max two turns/USD 1/180 seconds; guard tests PASS | PASS | Forced-off Hook Retry 02 Plan | required | - |
| Forced-off hook retry 02 attempt | 4 | W4 | One approved fresh session-only forced-off hook-delivery retry | Local route/shim/atomic/guard preflight PASS; provider exit 1 before hook initialization; stderr-only discarded; zero events, tools, and model output; cleanup/status PASS | FAIL | Forced-off Hook Retry 02 Result | required | - |
| Forced-off MCP static diagnosis | 4 | W4 | No-session validation of the retry MCP argument forms | Empty `--mcp-config '{}'` and empty wrapped `mcpServers` each reject as `Invalid MCP` before lifecycle initialization; no third attempt | PASS | Forced-off Hook Retry 02 Result | optional | - |
| Forced-off hook retry 03 plan review | 4 | W4 | Independent security review of one frozen strict-MCP, no-config retry with the Retry 02 guards retained | Harness `98af87fab954dc515d54f43153bab36966f328a2137ed64868eda97c9b2ebc02`; pinned 2.1.301 headless strict path selects empty servers; no `--mcp-config`; Write-only, max two turns/USD 1/180 seconds, sandbox false without OS-confinement claim | PASS | Forced-off Hook Retry 03 Plan | required | - |
| Forced-off MCP dynamic-proof boundary | 4 | W4 | Public `mcp list` observation under the reviewed investigation | Timed out health-checking normally approved servers; subcommand bypasses the headless strict resolver; no child remains | NOT_RUN | Forced-off Hook Retry 03 Plan | optional | - |
| Forced-off hook retry 03 attempt | 4 | W4 | One released frozen strict-MCP, no-config hook-delivery retry | Exit 0; valid stream; no stderr; final token and one Write; SessionStart/UserPromptSubmit/PreToolUse/Stop/SessionEnd each 1; PostToolUse and PreCompact each 0; no output file or exact output retained; one nested-Bash token `UNEXPECTED`; cleanup/status PASS | FAIL | Forced-off Hook Retry 03 Result | required | - |
| Normal settings memory-control query plan review | 3 | W3 | Independent security review of one read-only normal-settings memory query | Plan `a30ac627797ebb013c9e6f9b87cf56f4b544f70e2e908a24b55a8543e811565c`; harness `bf8baf16b7a3d64317f64c2d9e74e8f3f16061489577717b833baf1188555eda`; initialize/get_memory_dialog/end_session only; no model/user/tool/MCP; sandbox false with no OS-confinement claim | PASS | Normal Settings Memory Control Query Plan | required | - |
| Normal settings memory-control query result | 3 | W3 | One released non-mutating normal-session effective-memory query | `CLAUDE_NORMAL_MERGED_AUTO_MEMORY_OFF_VERIFIED`; enabled false/plain off/no detail/settings-source suffix/toggleable false; init/get/end PASS; exit 0; no stderr/timeout/model/user/tool/MCP/permission/status change; receipt `e24e56cbfc5c2a022462029df4f3c2c686603bffb110d27b76d7ea1c7679015f`; observation `a245a0d61d190482d0985c3dd89312b655072202d8f3c7993b70240a5b574a1f`; independent security PASS | PASS | Normal Settings Memory Control Query Result | required | - |
| Forced-off hook attempt 04 plan review | 4 | W4 | Independent security review of one final forced-off exact-Write attempt | Plan `b1511ff25ffb89b0d7050bf9f506f7733d50b8e2622267f5681875d1fbacc6ae`; harness `3105c920cb2a2250f58a7f8f917c24d449d441d9dc3dcb93b69f42d1661978c2`; Write only, max two turns/USD 1/180 seconds; forced-off session; sandbox false with no OS-confinement claim; 11 `O_NOFOLLOW` pins and guard-directory recheck | PASS | Forced-off Hook Attempt 04 Plan | required | - |
| Forced-off hook attempt 04 | 4 | W4 | One released final forced-off exact-Write diagnostic | Receipt `89ea175746a446cb58b3c1dbc068e418a2b1ebc194b540529a78c87026aa0d2a`; failed closed; process exit 0/harness 1; Write observed once but tool result error/output absent; one forwarded guard; native/dispatcher SS/UserPromptSubmit/PreToolUse/Stop/SE each 1; PostToolUse/PreCompact/PostToolValidate 0; UNKNOWN 1; filesystem unchanged; cleanup/status PASS; post-result security pending | FAIL | Forced-off Hook Attempt 04 Result | required | - |
| Metadata validation after native contract alignment | 6 | W6 | Full changed-document metadata selection with the active eight-path/base selection | Launched at `8219c9b`; exit 0; selected 7; violations 0; legacy exceptions 0; transition overrides 0; concurrent Task receipt edits, while Spec/Plan/registry bytes unchanged; not an immutable worktree snapshot | PASS | Metadata Validation Provenance | required | - |
| Merged hook listing control plan review | 4 | W4 | Independent security review of one read-only merged-hook aggregate query | Plan `75ccecddb0fc621e1225fd8e965f054a41dc7692a68253a532e6817e28bc3d40`; harness `f92d170c438cea41ec8b5f5bbe8524eeb1c63e817b09659c959c08a5961d573c`; initialize/get_hooks_listing/end only; fixed enum/count aggregate; no model/user/tool/MCP/settings mutation or raw hook data | PASS | Merged Hook Listing Control Plan | required | - |
| Merged hook listing control result | 4 | W4 | One released read-only merged-hook aggregate query | Immutable receipt `8345aa34cdf14e06f3d3fa0dbd7d16e372bbb87ea103bb3b8764260ee724d2fc`; historical classifier output `CLAUDE_ADDITIONAL_PRETOOL_HOOK_IDENTIFIED`; transport/cleanup PASS; counts qualified separately | PASS | Merged Hook Listing Control Result | required | - |
| Merged hook listing classifier qualification | 4 | W4 | Validate candidate attribution and aggregate counts from the immutable control receipt | Public ECC identifier `ecc@ecc` differed from prior allowlist expectation; `.*` matchers missed rows; actual plugin Write aggregate 7, not receipt 5; transport valid but classification incomplete; independent security qualified result | FAIL | Merged Hook Listing Classification Qualification | required | - |
| Native PostToolUse attempt 05 plan review | 4 | W4 | Independent security review of one ECC-disabled, normal-memory-off named-project wrapper diagnostic | Plan `139634cb63898f23d82dfa4a0d0892313655d13f102eb6741fd249eb486dba4f`; harness `ce345a4ed7b1091f0607560f427623dfc452a5a32b9d7fee3e480692261d7e9e`; session-only `ECC_HOOKS_ENABLED=false`; double-slash Write guard; max two turns/USD 1/180 seconds; strict no-MCP; no ECC delivery claim | PASS | Native PostToolUse Attempt 05 Plan | required | - |
| Native PostToolUse attempt 05 | 4 | W4 | One released ECC-disabled, normal-memory-off named-project wrapper diagnostic | Receipt `7662bae15c4b64b47c862f4632edfc65b6a4d7cfa460a565273e7c84fbc78e5d`; failed closed before provider launch because ECC root mode 0775 made `ecc_root_guard=false`; null exit code; zero stdout/stderr/tool/events; guard tests 12/12; cleanup PASS; status equal; no retry | FAIL | Native PostToolUse Attempt 05 Result | required | - |
| Native PostToolUse attempt 06 plan review | 4 | W4 | Independent security review of one preflight-corrected ECC-disabled, normal-memory-off named-project wrapper diagnostic | Plan `b63759b956db133f0c7f2a1ec6c430befb9dd4623df3c2dd14ac767f57803990`; harness `e33dbd56a113285318ab5c9d7ef6ed90a921966a6e1ad93c9e553912ceac3d34`; public root mode/private group/current UID/full nine chain/no ACL/no writer checks; offline host 9/9 and guard tests 12/12; Write-only/max two turns/USD 1/180 seconds/no MCP unchanged | PASS | Native PostToolUse Attempt 06 Plan | required | - |
| Native PostToolUse attempt 06 | 4 | W4 | One released ECC-disabled, normal-memory-off named-project wrapper diagnostic | Receipt SHA-256 `1086eaa6…`, 2026-10-16 | FAIL | Native PostToolUse Attempt 06 Result; timed out, `SessionStart` 0, `PostToolUse` 0, one `UNKNOWN` event | required | - |
| Native PostToolUse attempt 07 | 4 | W4 | One released ECC-disabled, normal-memory-off named-project wrapper diagnostic | Receipt SHA-256 `3af58d34…`, 2026-10-30, Claude 2.1.312 | FAIL | Native PostToolUse Attempt 07 Result; all native and dispatcher hooks delivered once and the Write was exact, but seven `abs-other` UNKNOWN calls and a non-boolean `is_error` failed the closed checks | required | - |
| Native PostToolUse attempt 08 | 4 | W4 | One released ECC-disabled, normal-memory-off named-project wrapper diagnostic | Receipt SHA-256 `44894122…`, 2026-10-30, Claude 2.1.312, harness `7df03fae…` | PASS | Native PostToolUse Attempt 08 Result; `POSTTOOLUSE_DELIVERY_VERIFIED_WITH_NORMAL_MERGED_MEMORY_OFF` with the owner's two scope exclusions | required | Native PostToolUse attempt 05, Native PostToolUse attempt 06, Native PostToolUse attempt 07 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | Await W1 control record | @buenhyden |
| 2 | pending | - | Await W2 observation | @buenhyden |
| 3 | accepted | Normal settings memory-control query result | Normal non-mutating effective-memory-off proof and independent security review passed | @buenhyden |
| 4 | pending | - | Await W4 receipt classification | @buenhyden |
| 5 | pending | - | Await W5 boundary and cleanup record | @buenhyden |
| 6 | pending | - | Await W6 review and gates | @buenhyden |

## Review and Completion

Criterion 3 is accepted for the recorded normal-session effective-memory-off
query and independent security review. Criteria 1, 2 and 4–6 remain pending;
that bounded result does not prove hook delivery or authorize another native
attempt. This 2026-10-22 summary correction reuses the existing receipt and
performs no provider action. Completion is limited to the source
verification contract in SPEC-0244; it does not accept provider-global state,
individual hook delivery without a receipt, or shared-memory implementation.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
