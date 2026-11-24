---
title: "Harness Maintenance"
version: "2.10.0"
type: "governance/workspace-guide"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-24"
created: "2026-11-19"
observed_at: "2026-11-19"
reviewed_at: "2026-11-20"
review_cycle: "on-tool-change"
---

# Harness Maintenance

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the guide payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

How a person keeps the workspace's local agent tooling healthy: the shared
agent memory store, session capture, scheduled session analysis, task
forecasts, parallel work dispatch and the observe report. Each tool's command
line and output contract stays in its script; this guide owns the routine
upkeep, diagnosis and recovery a maintainer runs by hand. How an agent uses
these tools is agent procedure in `.agents/governance/`, and product backup and
restore stays in
[RUN-0021](../../05.operations/03.runbooks/10.platform-and-backup/0021-backup-and-restore.md).

#### Prerequisites

Included: `scripts/operations/agent_memory.py`, `scripts/lib/hooks/session_capture.py`,
`scripts/operations/session_analysis.py`, `scripts/operations/task_forecast.py`,
`scripts/operations/work_dispatch.py` and `scripts/operations/observe.py`, and the
local stores they keep under `.workspace-memory/` and `.workspace-capture/`.
Excluded: product services, backups (the shared memory store is excluded from
backup, as RUN-0021 records), and any approval, gate or Task acceptance. No
store here is evidence of approval or acceptance.

This active workspace-maintenance guide is the registered documentation owner
for the memory, analysis, forecast, dispatch, observe and managed-execution
manifest entries that name it. Session capture retains its agent-policy owner. This registration
does not grant execution permission or accept those tools;
[approval boundaries](../04.quality/approval-boundaries.md) remain applicable.

The memory, capture, deterministic analysis and shell workers below describe the
current implementation. Further memory, native session integration and provider
work dispatch changes remain with P09, P10 and P12 respectively; this guide
adoption implements none of those later changes.

#### Procedure

##### Shared agent memory store

The entrypoint is `scripts/operations/agent_memory.py`. `scripts/lib/ops/memory_cli.py`
interprets commands and `scripts/lib/ops/memory_capacity.py` keeps the capacity
ledger and request records. Shared memory is not backed up, so this guide owns
only ledger adoption and lookup.

###### Capacity and first adoption
<!-- core-payload-level:4 -->

The memory database keeps schema 3 and its per-body and database limits, and a
separate `.workspace-memory/capacity.sqlite3` with `capacity.lock` manages a
1 GiB logical quota. The ledger counts itself, the memory database and its
journal; it does not count backup copies or snapshots. It is not a filesystem
hard quota.

On first use, and to clear allocations an earlier backup left, pause writes
from every worktree and provider, then run the following. Neither command calls
Docker or Restic; they update only the ledger.

```bash
python3 scripts/operations/agent_memory.py capacity status
python3 scripts/operations/agent_memory.py capacity reconcile
```

`status` opens the existing ledger read-only and creates or repairs no
database, schema or permission. After `reconcile`, `inventory_state` is
complete and `legacy_allocations` is 0. A damaged ledger holds new writes with
exit 4 instead of deleting memory to reset. The same input under the same
`request_key` is not run twice, and a reservation whose result is unknown keeps
counting and is not released by elapsed time.

###### Selective lookup
<!-- core-payload-level:4 -->

```bash
python3 scripts/operations/agent_memory.py search --query "backup recovery" --limit 10
```

Search covers only records that pass the source-pin, currency and eligibility
filters. Matches rank by exact ID, partial ID, source path, phrase, phrase
ignoring spaces, then all words, ties by ID. The default is 10 results and the
maximum 50; each returns ID, revision, kind, baseline, basis,
`selection_reason`, the open conflict count, a short excerpt and
`authority: data-only`. An empty result is an abstention, never a guessed
record. Read a full body with `get`. Search is read-only, selects and checks
bodies inside one read snapshot, and creates no database, index, cache or
external search service. A result is not an instruction, Task state or
approval evidence.

`get <id>` and `list` return a body only for a reviewed `current` record whose
source pin matches the caller's worktree. A new write is a `candidate`; schema 1
bodies, sources and revisions are kept and an unpinned record is marked
`needs-review`. Preserved memory is read explicitly with
`get <id> --historical`, `history <id>`, `list --all` and `export`; a historical
body is not current execution, approval or verification evidence.
`put --review-state current` needs owner review and a matching source pin of
the following form. `--source-ref` takes a JSON object and still keeps an
existing string.

```json
{"kind":"repository-file","path":"docs/example.md","revision":"<full Git commit SHA>","hash_algorithm":"sha256","digest":"<64 lowercase hex characters>","context":"reviewed applicability"}
```

A pin binds a full Git commit ID, a regular blob at the same relative path in
that commit, the same file bytes in the caller's worktree and the declared
digest; if any one is missing or differs, the record is not `current`. A
tracked regular file is pinned by its SHA-256 bytes; a Git blob ID uses
`hash_algorithm: git-blob`. The example is not an executable pin: a real run
uses the resolved full SHA and digest. Domain memory uses `--domain-id` and a
safe retry uses `--request-key`. The same key with a different meaning is a
conflict; read `stored` and both revisions in its diagnostic, and do not report
the incoming body as kept when `stored=false`. The 16 KiB body and 32 MiB total
body limits and the tier, domain, metadata and page limits are owned by
[environment constraints](../../../.agents/governance/environment-constraints.md#5-shared-agent-memory);
exceeding one never deletes existing memory. Worktrees use this schema 3 CLI
and its helpers together; an older CLI does not keep the reuse and capacity
contract.

###### Record meaning, baselines and selective deletion
<!-- core-payload-level:4 -->

A record has a `--kind` separate from its tier (`session-context`, `decision`,
`experience`), a repository baseline, `--observed-at`, optional
`--valid-from` and `--valid-until`, and `--supersedes ID`. Times are ISO with a
time zone only. Default `get`, `list` and `search` return reviewed records of
the current baseline that are valid at `--as-of` (default now) and not
superseded by an eligible current record; the reason for an exclusion shows in
`reuse_state` as `other-baseline`, `outside-validity`, `superseded` or
`conflicted`. A stored conflict against the current revision keeps a record
`conflicted` until a new revision written with the current expected revision
reconciles it. A reviewed record also shows `source_state`: `current`,
`changed` (the tracked file differs from its pin), `unavailable` (it cannot be
checked) or `content_expired` (the session content it names passed
retention). A boolean revision or a non-finite number is refused with exit 2
(`MEMORY_INVALID`). An older
record without a kind derives one from its tier (short-term is
`session-context`, the rest `experience`) and has the baseline `initial`.

A store created before schema 3 refuses writes (`MEMORY_MIGRATION_REQUIRED`,
exit 2) and keeps serving reads. Pause writes from every worktree and provider
and run it once; it adds only `store_meta`, changes no revision and is
idempotent.

```bash
python3 scripts/operations/agent_memory.py migrate
python3 scripts/operations/agent_memory.py baseline show
python3 scripts/operations/agent_memory.py baseline cutover --expected initial --to "<new baseline ID>"
python3 scripts/operations/agent_memory.py export --memory-id "<ID>" --history
python3 scripts/operations/agent_memory.py erase --memory-id "<ID>" --confirm "<sorted ID list>"
```

A baseline cutover is refused with exit 3 when the expected baseline differs.
Afterwards, records of the earlier baseline leave the default view but remain
in `list --all`, `export` and `history`. `erase` takes only owner-approved
records, and `--confirm` is the sorted IDs joined by commas. It removes every
revision, provenance and conflict of those records and overwrites free SQLite
pages, but it claims nothing about journal, filesystem or device remnants.
Memory is not backed up, so there is no backup copy to delete.

The store Claude and Codex share (`.workspace-memory/memory.sqlite3`) is ignored
by Git, so Git cannot restore it, and backup excludes it.

##### Session capture

`scripts/lib/hooks/session_capture.py` records this workspace's user prompts
and visible final responses, with secret values masked, and event metadata from
the shared hook dispatcher into `.workspace-capture/capture.sqlite3`. Each text
is masked whole, cut to 16 KiB and masked again; a cut text has
`content_state` `truncated`. The directory is mode 0700 and excluded from Git
and backup. Text and its fingerprint are cleared 30 days after the event
(`content_state` `expired`) and the record is removed after 90 days, at
reconciliation and at each analysis run. Past a 256 MiB store only metadata is
kept (`content_state` `quota`). A failed tool call keeps its tool name and its
failure text, masked and cut to 4 KiB: Claude sends it through
`PostToolUseFailure`, Codex through `PostToolUse` when the shell exit is not 0.
Hidden reasoning, intermediate replies, tool input and successful tool output
are not copied, and no other personal session file is read. An event ID comes
from the provider, session, event and its turn, tool call or offset marker,
never from captured text; a prompt row whose ID came from its text, from an
older checkout, is rekeyed on the next connection, and the next analysis run
rewrites its references.
The first connection after an upgrade migrates an older store once: it adds the
ingest sequence, masks and cuts stored prompts again and replaces digests of
unmasked text. A linked worktree shares the primary checkout's store, so a
checkout on older code may still write a row without a sequence; the next
connection from current code adopts it the same way, and the analysis reads
it once.

```bash
python3 -m scripts.lib.hooks.session_capture status
python3 -m scripts.lib.hooks.session_capture reconcile
```

Each session's `completeness` in `status` is complete, partial or unavailable,
and `reason` says what is missing. Codex cannot separate user prompts in its
transcript format, so it is captured by hook only and stays partial; one end
hook alone never makes a capture complete. When `capture_failures` rises, read
the cause in `.workspace-capture/degraded.log`. A capture failure never blocks
a hook result or development work. A capture is evidence only, never memory,
policy, approval or Task acceptance. A test that runs a real hook points
`HY_HOME_CAPTURE_DIR` at a temporary directory so no test session lands in the
operating capture.

##### Scheduled session analysis

`scripts/operations/session_analysis.py` analyses the capture with
deterministic rules and no language model (owner decision, 2026-11-18). It
turns repeated prompts (the same normalized text three or more times within the
30-day content), three or more corrections right after a visible response,
three or more tool failures with the same tool and first failure line,
incomplete sessions and capture failures into candidates, each with its source
event IDs, frequency, condition, proposal, risk and acceptance test. Source
events only accumulate; `candidates` counts those whose record expired as
`source_expired`. A candidate's captured `pattern` clears with its content, a
pending candidate is removed 90 days after creation and a decided one 30 days
after the decision; one linked to a Task with no effect recorded yet stays
until 90 days after the decision. Results go
to `.workspace-capture/analysis.sqlite3`; the last run's state goes to
`analysis-status.json` and the systemd journal.

```bash
python3 scripts/operations/session_analysis.py install-timer
python3 scripts/operations/session_analysis.py run
python3 scripts/operations/session_analysis.py status
python3 scripts/operations/session_analysis.py candidates
python3 scripts/operations/session_analysis.py decide "<candidate ID>" rejected --owner "<reviewer>"
python3 scripts/operations/session_analysis.py promote
python3 scripts/operations/session_analysis.py promote --include-earlier
python3 scripts/operations/session_analysis.py link "<candidate ID>" --task SPEC-0212-TSK-0111 --check "<evidence row>"
python3 scripts/operations/session_analysis.py effect "<candidate ID>" unchanged --sample 3
```

`install-timer` installs the user systemd timer
`hy-home-session-analysis-<workspace key>.timer` for 03:00 Asia/Seoul daily, and
`Persistent=true` catches up a missed run at the next start. The key is derived
from the checkout path, the service names that working directory and its
capture store, and the command refuses a linked worktree. It moves this
checkout's earlier fixed-name `hy-home-session-analysis` unit and leaves one
that names another checkout. The service has no `Restart`, so a failure does
not repeat. A run reads at most 5,000 events after its ingest-sequence cursor
and the failure log after its byte offset, and commits both with its
candidates, so an event in the same second as the last run is still read once;
`status` shows `cursor_start`, `cursor_end` and the unread `backlog`, which the
next run continues. While a lease holds, a duplicate
run exits 75; a run that lost its lease writes nothing (fenced), and SIGTERM is
recorded as a cancellation. `decide ... accepted` records the decision and the
whole promotion request together, then writes it through the memory CLI as one
unreviewed `candidate` record; the record holds the reviewed proposal, never the
captured prompt text, and names its source events with their content expiry.
If that write is refused the intent stays `pending` with its reason and the
command exits 1; rerun `promote`, which reuses the same request key, so a lost
receipt neither writes twice nor revives an erased record. A candidate whose
reviewed fields changed is marked `stale` and not promoted.
`--include-earlier` first records intents for candidates accepted before the
outbox existed; run it only on the owner's decision. Making the record
`current` still needs owner review and a source pin, and a policy, skill or
checker changes only through a separate Task and approval. `link` ties an
accepted candidate to the Task that carries its change and the evidence row
that checks it; `effect` records `improved`, `unchanged` or `worsened` only
after a later comparison with the sample size it used. Until then the effect is
null and counted as unobserved, never as a success or a zero. Missing capture or a failed analysis never blocks a commit, push
or other work. Remove the timer with
`systemctl --user disable --now hy-home-session-analysis-<workspace key>.timer`.

##### Task forecasts

`scripts/operations/task_forecast.py` records P30, P50 and P80 completion
minutes before a task starts, records the outcome once afterwards, and scores
each quantile. P30, P50 and P80 are the times by which the task completes with
probability 0.3, 0.5 and 0.8, not progress shares. A forecast needs
`--assumptions` (including expected blocking waits) and `--reference-class`;
the store counts the completed tasks of the same type and time basis that had
ended before it (`comparable_prior`), and below 20 the forecast is shown as an
`uncalibrated prior`. Records live in `.workspace-capture/forecast.sqlite3`, excluded
from Git and backup. The default time basis is elapsed time; to measure working
time only, use `--time-basis active` and `--active-minutes` on the outcome.

```bash
python3 scripts/operations/task_forecast.py forecast TASK-REF --type ci-run --p30 10 --p50 15 --p80 25 --assumptions "one runner, no queue" --reference-class "hosted CI runs of this repository"
python3 scripts/operations/task_forecast.py observe TASK-REF --status completed --started-at 2026-11-18T10:00:00+09:00 --finished-at 2026-11-18T10:18:00+09:00
python3 scripts/operations/task_forecast.py score --type ci-run --time-basis elapsed
```

A changed estimate adds a revision; existing values cannot be edited or
replaced (REPLACE), and a task with an outcome takes no new estimate. This
protection stops SQL edits only, not dropping triggers or replacing the store
file. Minutes must be finite, and a future finish time or active time longer
than elapsed time is refused. An outcome is completed, failed, cancelled or
blocked (ended waiting on a permission or decision), stores the last revision
fixed before the task started and is scored against it; an outcome whose only
estimates came after the start is refused.
`score` reports per-quantile sample size, the share of actual values at or
under the estimate (coverage) with its 95% Wilson interval, and pinball loss,
counting failed, cancelled and blocked tasks apart as censored samples and
forecasts without an outcome as `open`. It lists each task type and time basis
group; a selection mixing elapsed and active time shows `mixed time bases`,
fewer than 20 completed samples show `insufficient sample`, and a mix of task
types shows `pooled across types`; none reads as a calibrated 80% guarantee.
A forecast error never blocks a commit; under- and over-estimation per group
is read in the observe report. A forecast
is a planning reference, never a deadline, an approval or a reason to skip a
required check, and the completion distribution of parallel work is not the sum
of per-task P80s.

##### Parallel work dispatch

`scripts/operations/work_dispatch.py` runs the work units of a JSON plan as shell
or provider workers, each in its own Git worktree. A unit names its command, or
a `provider` with `name` (`claude` or `codex`), `model`, `prompt` and
`max_budget_usd` (at most 5), plus dependencies, owned paths and shared
resources (for example `port:5432`, `registry:writer`). A plan with a provider
unit also names the brief `session`, `request_revision` and `brief_revision`;
right before the spawn the dispatcher runs the brief's `check ... dispatch`
for the unit's owned paths and fails the unit if the brief does not allow it.
A provider worker runs the installed CLI non-interactively (Claude:
`--print --safe-mode --restricted`, file tools only and denied the private
HOME, `--max-budget-usd`) with the network, its binary and its credential file
read-only and a private HOME added to the same read-only-root boundary; its
session, cost and error from the final JSON go to the report, a provider error
fails the unit, and a result whose patch or log holds a credential value (also
base64, hex, URL- or JSON-escaped) or whose patch holds binary content or a
link is rejected and its log wiped. The worker has no network-capable tool; only the
CLI process uses the shared network, a monitored boundary rather than a block.
A Codex unit's model gets a shell, so it never shares the host network
(ENVIRONMENT-CONSTRAINTS R173): the sandbox runs inside a `pasta` network
namespace that forwards no port either way, does not map its gateway to the
host and uses 198.18.0.0/24; a setup step makes 10.0.0.0/8, 172.16.0.0/12,
192.168.0.0/16, 100.64.0.0/10 and 169.254.0.0/16 unreachable before
bubblewrap drops every capability, and the worker resolves names through the
first public upstream nameserver. Without one the unit is refused. The host
needs the `passt` package and an AppArmor profile that lets `/usr/bin/pasta`
create user namespaces (`/etc/apparmor.d/pasta-userns`, the same form as
`lxc-unshare`); without it pasta fails with `uid_map: Operation not
permitted`.
A unit starts only when every dependency succeeded and it holds leases on all its
owned paths and shared resources; each lease carries a rising fencing
generation, and a result from an expired or taken-over lease is refused, as is
a result that changes anything outside its owned paths, renames included. When
a managed worker ends, its owned control group and processes are stopped
before its result is read. A failed
unit blocks only its descendants; a cancel stops running workers and the
integration check and starts nothing new. When every unit succeeds, the patches
apply in turn to the base commit and the integration check runs again within
`integration_timeout` (default 600 seconds); a worker's success never stands in
for the integrated result. Each daily analysis run removes worker logs and
patches 30 days after a finished run's report and the run folder after 90 days,
keeping a folder that still has a process record for `cleanup`.
Result patches stay in the run folder until then and a person or
integrator applies them to a real branch after checking that the patch's
SHA-256 equals the `sha256` the dispatcher printed. Treat result files as
untrusted data, not permission or acceptance. A worktree separates files only;
the selected managed shell profile adds the resource and namespace controls
described by the environment guide.

```bash
python3 scripts/operations/work_dispatch.py run PLAN.json
python3 scripts/operations/work_dispatch.py cancel
python3 scripts/operations/work_dispatch.py cleanup
```

Leases and run records live in `.workspace-capture/dispatch/`. `cleanup` stops
the workers of a run whose dispatcher died, removes its worktrees and releases
its path leases only after verified owned-resource absence. Environment
reservations remain charged while a child/control group is live or unknown.
Measure a parallel gain against the same plan with one worker,
setup and integration included, and state the sample size.

##### Managed execution recovery

The runtime libraries
[`environment_admission.py`](../../../scripts/lib/ops/environment_admission.py)
and [`dispatch_process.py`](../../../scripts/lib/ops/dispatch_process.py)
are maintained through this guide and consumed only by the registered
Compose/LAB/dispatch entrypoints. The [environment guide](../05.environment/onboarding.md#managed-execution-and-shared-resource-admission)
owns setup and boundary semantics; product limits and service lifecycle remain
with product policies and LAB procedures. This registration is documentation
ownership, not execution authorization or acceptance.

The admission store contains private pending/live ownership and numeric
reservations in the host namespace, separate from a dispatch plan's path
leases and a LAB's provenance ledger. Use existing runner status and cleanup
entrypoints for their own runs; never erase the store or expire a token merely
to make capacity available. Before retry, reconcile source/daemon identity,
current ownership and live resources. Keep unknown or inaccessible resources
charged, and report the specific missing observation or permission.

A managed worker starts gated, with durable token and stable process identity.
Cancellation/timeout stops the token-matching control group and namespace before
releasing the reservation. A reused PID, stale process group or mismatched LAB
token is not ownership. After a controller interruption, inspect the recorded
identity and owned resources through the existing recovery path; release only
on verified absence. LAB cleanup keeps unrelated projects and persistent data;
no global prune or automatic operating-root teardown is part of recovery.

The root operating-start command reports a recovery token when its result is
uncertain. Run `python3 scripts/operations/compose-start.py recover --token
<token>` from this checkout. Recovery stops only the matching controller scope
and releases its reservation once every running selected container is
accounted in the current live inventory. A partial start is released and its
missing or failed services are reported as `incomplete_services`; an unknown
controller or unaccounted running container keeps the reservation charged.
A start that was killed before printing its token is recovered by running
`recover` without `--token`, which reconciles each owned start claim whose
process has exited. Recovery never tears down the operating Compose project.

Changes to these libraries select their mirrored behavior regressions and
actual LAB/Compose/dispatch consumers. A temporary dummy environment can prove
admission, read/write boundaries, readiness and owned cleanup; it does not
prove product authentication, persistence, backup or every service's health.
Record actual commands, scopes and failure dispositions in the current Task,
then delete completed owned probes. Persistent state and tests remain.

##### End-of-work cleanup

When a Task or run ends, list what it made outside its durable owners: probes,
one-off tests and scripts, dumps, traces, copied fixtures and
`_workspace/repo-support/<task>/` output. For each, record the owner, the
consumer that still reads it and the condition that ends it
(ENVIRONMENT-CONSTRAINTS R169-R172). Move any lasting conclusion into its
canonical owner first, then remove only what the Task owns and nothing reads.
Keep the shared memory, capture, analysis, forecast and dispatch stores, the
scheduled units, current regressions, LAB data and another Task's material; a
dispatch run folder expires on its own schedule. Delete exact paths only:
never follow a symlink or mount out, and never prune the host. Material kept
to recover a failure, or an input package a later step still reads, names its
owner, the point where work resumes and the condition that deletes it. Confirm
`git ls-files _workspace/` still lists only the seven contract READMEs.

##### Observe report

`scripts/operations/observe.py report` counts what happened in a time window
(default the last 24 hours) across the capture store, session analysis runs,
forecast outcomes, dispatch reports and the journals of `hyhome-backup.service`
and this checkout's `hy-home-session-analysis-<workspace key>.service`. Each failure names its owner document
and next step: backup failures go to RUN-0021, the others to this guide.
Journal lines are counted, never copied, and no log text, prompt or secret is
moved. The report records its own run time as observation cost and lists what it
cannot measure (queue wait outside dispatch, context loading, billed cost). An unreadable
store, a journal that hides lines, and a daily unit with no run in 29 hours
(allowing a 30-minute timer delay and up to 4 hours of run time) are reported as
failures, not as zero. Runs of the analysis unit under its earlier fixed name
count for the current unit. Dispatch reports are worker-writable, so only fields of
the fixed format are copied. A unit that failed before it started (brief, plan
or admission refusal) counts as `blocked`, and a run with only such units is
`blocked`, not `failed`. Dispatch also shows run and unit seconds, the wait from
run start to each unit start, and per provider the CLI's own cost estimate,
turns and units whose cost it did not report; billed cost stays unmeasured. The
analysis `chain` counts candidates from source events through review, Task
link and effect, with unobserved effects apart. The report is not a check or an approval, and each
failure is resolved in its owner record.

```bash
python3 scripts/operations/observe.py report --since 2026-11-12T00:00:00+00:00
```

#### Verification

##### Provenance

On 2026-11-19 SPEC-0212 TSK-0097 moved the shared memory, session capture,
session analysis, forecast, dispatch and observe sections of RUN-0021 (1.22.0)
here, translated from Korean without changing a command, limit or exit code.
RUN-0021 keeps product backup and restore and the backup exclusion of shared
memory.

The P05 [typed-guide adoption Task](../../03.specs/0212-request-baseline-and-reconciliation/01.tasks/tsk-0103-p05-docs-sdlc.md)
records the 2026-11-20 role and contract review. The original observations above
remain dated to their actual inputs. This adoption executes no maintenance
command and does not complete any outstanding runtime or owner acceptance.

##### Refresh Triggers

- A command, store path, limit or exit code of a tool above changes.
- A tool is added to or retired from the workspace harness.
- The backup exclusion of shared memory changes.

#### Related Documents

- [Environment onboarding](../05.environment/onboarding.md)
- [RUN-0021 Backup and Restore](../../05.operations/03.runbooks/10.platform-and-backup/0021-backup-and-restore.md)
- [Environment constraints](../../../.agents/governance/environment-constraints.md)
- [Scripts README](../../../scripts/README.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
