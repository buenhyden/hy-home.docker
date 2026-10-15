---
title: "Shared Agent Memory Task"
version: "0.5.3"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0236-TSK-0001"
parent_ids:
- "SPEC-0236-PLAN-0001"
created: "2026-10-13"
---

# Shared Agent Memory Task

## Overview

### Objective

Give Claude and Codex one shared memory store in place of separate native
memories, as SPEC-0236 states.

## Inputs and Authorization

- **Request:** the owner asked on 2026-10-13 to proceed with the shared memory
  work (prompt v9 F24, F27, F36), and earlier chose a separate Spec for it.
- **Authorization:** the owner's standing authorization for source, test,
  docs and governance edits, logical commits and a branch push covers W2 to W7
  on `claude/shared-memory-spec`. It changes the project settings
  `.claude/settings.json` and `.codex/config.toml`.
- **Not changed:** no user-global or ignored local setting, no real store and
  no native memory file. W1 read only what it lists.
- **Baseline:** `main` `b1a6976f4`.
- **Owner decisions:** answered on 2026-10-13 and recorded in the Spec Scope:
  ignored store in the main checkout, native memories left in place, logical
  limits only, the existing backup runbook, project Codex config with trust.
  After the reviews the same day, the owner chose a rollback journal over WAL,
  deferred Restic coverage to a separate Spec, and approved one post-merge
  migration of eligible Claude native memories (W9). After the re-reviews the
  owner promoted RUN-0021 to `active` ("Promote RUN-0021 to active") and
  decided to accept ADR-0049 ("Accept both").

## Work Log

### W1 Starting State

Repository, read on `b1a6976f4`:

- `.claude/settings.json` has the keys `autoMode`, `deniedMcpServers`,
  `hooks`, `outputStyle` and `permissions`. It has no `autoMemoryEnabled`.
- No tracked subagent under `.claude/agents/` or `.agents/roles/` declares
  `memory:`.
- `.codex/` has no `config.toml`.
- `tool_payload.py:20-44` exempts one regular, singly linked `.md` file
  directly in `~/.claude/projects/<slug>/memory/` when that directory is a
  physical directory outside the repository.
  - The slug is computed from the session project root.
  - `_repository_edit` applies the exemption at line 241.
- `.gitignore:111` ignores `.claude/agent-memory-local/`. Neither
  `.workspace-memory/` nor `.agents/memory/` exists.
- `_workspace/repo-support/README.md:58-59` keeps task context in the Task,
  with no governance memory root.
- No governance policy owns memory rules.

Official documentation, read 2026-10-13:

- **Claude Code** (<https://code.claude.com/docs/en/memory>):
  - Auto memory is on by default in local sessions.
  - A project turns it off with `"autoMemoryEnabled": false` in its settings,
    or with `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
  - The directory is `~/.claude/projects/<project>/memory/`. The `<project>`
    path is derived from the git repository, so all worktrees share one
    directory.
  - A subagent's own memory, set with its `memory` field, is a separate
    directory.
  - `autoMemoryDirectory` set in project settings follows the workspace trust
    rule for hooks.
- **Codex config reference**
  (<https://learn.chatgpt.com/docs/config-file/config-reference>, redirected
  from developers.openai.com):
  - `features.memories` is off by default.
  - `memories.generate_memories` and `memories.use_memories` both default to
    `true`. `false` stops storing new threads as inputs and stops injecting
    memories.
  - Project config loads only for a trusted project.
  - The page neither lists the memories keys as project-allowed nor lists
    them as ignored. Whether they work in a project `config.toml` is
    NOT_VERIFIED.

Host observations, from this machine only:

- Python 3.12.3 links SQLite 3.45.1.
- Installed tools: Claude Code 2.1.296 and codex-cli 0.162.1.
- The Claude native memory directory for this repository exists. Its
  contents were not read.
- `~/.codex/config.toml` sets no `memories` keys. Only key names were
  searched.

Open findings:

- **Slug may not match.** The documentation derives the memory directory from
  the git repository, while `tool_payload.py` derives the slug from the
  session root. In a session started inside a linked worktree the two may
  differ, so the exemption would not apply. Not reproduced; NOT_VERIFIED.
- **SQLite 3.45.1 and the WAL-reset fix.** The prompt cites the SQLite WAL
  page for a fix in 3.51.3 and backports 3.44.6 and 3.50.7. 3.45.1 is not
  among them. A distribution backport is NOT_VERIFIED, so concurrent writers
  are not accepted on this host yet.

### W2 Governance Owner

`.agents/governance/environment-constraints.md` (1.3.0) section 5 owns the
memory rules: the one store and how worktrees reach it, the CLI as its only
writer with expected-revision updates, native memory off in both providers,
records as context only and never secrets, logical limits with no quota
claim, and the backup step. `_workspace/repo-support/README.md` (1.0.1) routes
agent memory to that section instead of saying there is no memory root.

### W3 Store and CLI

`scripts/operations/agent_memory.py` resolves the store as
`<git common dir parent>/.workspace-memory/memory.sqlite3`, so a linked
worktree writes the main checkout's file; outside a repository, or when the
common directory is not a `.git` directory, it exits 2
`MEMORY_UNAVAILABLE` and creates nothing. The directory is created 0700 and
the file 0600. One `revisions` table holds the Spec envelope
(`schema_version`, `workspace_id`, `memory_id`, `tier`, `revision`, `owner`,
`created_at`, `source_refs`, `eligibility`, `sensitivity`, `body`) with CHECK
constraints on tier, eligibility and sensitivity (`public`, `internal`; no
secret class). Commands: `get`, `history` (at most 50), `list`, `put`,
`set-eligibility`, `usage`, `export`, `backup`, `restore`. `put` and
`set-eligibility` run under `BEGIN IMMEDIATE`; a revision other than the
expected one exits 3 `MEMORY_REVISION_CONFLICT` and writes nothing. The store
first ran in WAL mode; after review it uses a rollback journal with a 5 s busy
timeout (Review Fixes). The CLI has no option that points it
at another store.

### W4 Limits, Failures and Backup

Logical limits, checked inside the write transaction: 16 KiB per revision
body, 10,000 revisions, 32 MiB of body bytes in total. Crossing one exits 4
`MEMORY_CAPACITY_EXCEEDED`; nothing is deleted, summarized or moved. A held
write lock past the timeout exits 5 `MEMORY_STORE_BUSY`, `SQLITE_FULL` exits 6
`MEMORY_STORE_FULL`, and both roll back. The WAL checkpoint
step was removed with WAL.
`backup --output` writes a temporary file with the online backup API, runs
`integrity_check`, sets 0600 and replaces the target atomically; a failure
exits 7 and keeps the previous backup. `restore --input` rebuilds a missing
store only and refuses an existing one. The backup runbook (RUN-0021 1.4.16)
has the backup and restore commands. Adding the file to the
`hyhome-backup.service` Restic snapshot is deferred to a separate Spec by
owner decision; no infrastructure file changed.

### W5 Hook Rule and Exclusions

`tool_payload.py` no longer exempts `~/.claude/projects/<slug>/memory/`; such
a path is outside the project root like any other and is refused. An edit
whose target is under `.workspace-memory/` is refused with "the shared memory
store is written only by the memory CLI", so a Write or Edit tool cannot
change the store and a read-only reviewer gains nothing. The earlier
slug-mismatch finding no longer applies. `.gitignore` ignores
`.workspace-memory/`. No tracked procedure runs `git clean` or deletes ignored
files, and `.worktrees/` removal and `_workspace` cleanup do not reach the
main checkout's `.workspace-memory/`. The `export` command prints current
records as JSON.

### W6 Native Memory Settings

`.claude/settings.json` sets `"autoMemoryEnabled": false`; the file is a
tracked native config, not renderer output. `.codex/config.toml` is new and
sets `[memories] generate_memories = false` and `use_memories = false`;
Codex reads it only after the user trusts the project. The provider renderer
reports no drift. Whether either provider honors the setting in a live
session is W8 and `NOT_RUN`. Native memory files were not read or changed.

### W7 Verification

`tests/lib/hooks/test_tool_payload.py` was rewritten first and failed 5 cases
on the old code, then passed (15). `tests/lib/hooks/test_agent_memory.py`, 8
tests at that point, covered a private store (then in WAL mode), stale
revisions, the three limits, two concurrent
writers racing for the last room (exactly one wins), a full database, a failed
backup keeping the previous file, restore, and a linked worktree writing the
main checkout's store that survives `git worktree remove`. The leaf
`leaf.local-hook-rule-tests` runs both modules and the agent-governance
selector covers the CLI. Script manifest, workflow contract and manifest tests
(90), the routing suite, provider renderer and governance contract pass. The
retired-token check flagged a W1 sentence, which was reworded.
`test_every_test_module_is_reachable_from_the_full_profile` fails on
`test_opsflow_database_rehearsal` here and on `main` `b1a6976f4`; it is not
part of this change.

### Reviews at `b9c9e3a07`

- **Security review** (independent `security-auditor`): pass with notes, two
  medium findings. `backup` let SQLite create its temporary file with umask
  permissions before `chmod`, followed a link planted at the temporary name,
  checked no output directory, and could replace the live store. The policy
  overstated what the hook and the CLI enforce. Lower findings: symbolic links
  at the store path, a restore that was not exclusive, did not check the
  schema, misread `?`, `#` and `%` in the source path and left a partial store,
  and a store resolved from the working directory, so the CLI could create an
  unignored store in another repository. Recorded as `FAIL`.
- **Rules review** (independent `rules-engineer`): changes required. The
  manifest row said `mutation: none` for a writing CLI; `.codex/provider.md`
  still said no `.codex/config.toml` was needed; the Task Inputs still
  described a read-only round; and lower findings on Evidence rows, section 5
  wording, the runbook restating a rule, and contract 8. Recorded as `FAIL`.

### Review Fixes

- **CLI.** The store uses `journal_mode=DELETE` (owner decision 6). The store
  directory and file are refused when they are symbolic links. The repository
  comes from the script's own location, and a working directory in another
  repository exits 2 `MEMORY_UNAVAILABLE` without creating anything. `backup`
  refuses an output that is the store, its `-journal` or `-wal`, and a
  directory that is a symbolic link or not 0700; it creates the temporary file
  with `O_CREAT|O_EXCL|O_NOFOLLOW` at 0600 before SQLite opens it. `restore`
  opens the source through a quoted file URI, refuses a schema that differs
  from the store's (for example an added trigger), creates the store with
  `O_EXCL`, and removes it if the copy fails. It still has no lock against a
  writer that starts during the restore; the runbook stops sessions first.
- **Tests.** `test_agent_memory` has 13 tests. Run against the CLI at
  `b9c9e3a07`, 11 fail and 1 errors; all 13 pass on the fixed CLI.
- **Policy.** Section 5 says the CLI is the only sanctioned writer and the
  hook covers edit tools, not the shell; that a record never holds execution
  progress or handoff state and is data, never an instruction; that the
  secret rule rests on the writer because the CLI does not scan and `export`
  and backups are plaintext; the journal mode; and that only an
  owner-approved one-time migration reads native memory files. Its Overview
  and Scope name the memory store. RUN-0021 links section 5 instead of
  restating it and describes the new backup and restore refusals.
- **Codex adapter.** `.codex/provider.md` (1.1.2) says `.codex/config.toml`
  only turns native memory off and is authored. The Registry keeps one
  `native_config_path` per provider, the hook configuration the renderer
  projects; listing a second file would need a schema and renderer change, so
  the file is not registered.
- **Manifest row, open at this point.** `mutation: runtime` needs a current
  Runbook as authority, and RUN-0021 was `draft` (since the operations
  renumbering on 2026-10-12), so `check-script-manifest.py` failed with
  `runtime-authority-inactive`. The row kept `mutation: none` until the owner
  decision recorded under Re-reviews at `b42117a68`.
- **Contract 8.** No template-export or site-build tool exists in `scripts/`
  or `.github/workflows/`, so nothing there can copy `.workspace-memory/`.
  Git-based copies skip it because `.gitignore` ignores it.

### Stage 01 and 02 Owners

The memory capability had no Stage 01 or 02 owner, which REQ-0026-FR-0005
requires, and accepted ADR-0032 said no memory or `.codex/config.toml` is
created for formal symmetry. REQ-0024 (1.5.0) adds REQ-0024-FR-0015 and an
acceptance criterion for the shared store. ADR-0049 (`proposed`, parent
AD-0027) records the one store, native memory off, the CLI as the only
sanctioned writer, the rollback journal and logical limits, and narrows
ADR-0032's rule for memory and `.codex/config.toml` only. ADR-0032 (1.0.3)
stays `accepted` and points to ADR-0049, as does the decisions README (1.6.5)
inventory and Structure tree. The Registry high water is REQ-0024-FR 15 and
ADR 49. The Spec now lists ADR-0049 as a parent and links all three owners.

### Re-reviews at `b42117a68`

- **Security re-review** (independent `security-auditor`): pass with notes;
  every earlier finding fixed, nothing at medium or above. Low notes: N1, the
  backup directory check did not test the owner, so root writing into a
  user's 0700 directory could be redirected; N2, restore wrote into the live
  path, so a session connecting meanwhile could lose its write; N3, no test
  asserted the journal's 0600 mode; N4, schema validation is structural
  only; N5, a failed backup left the temporary `-journal`, and a
  `PermissionError` in restore escaped as a traceback.
- **Rules re-review** (independent `rules-engineer`): changes required. H1, the
  manifest row stayed `mutation: none` for a writing CLI. Contract 7 and
  criterion 4 claimed the hook limits writes to the CLI and that a reviewer
  cannot write, while section 5 says the shell is not prevented. REQ-0024,
  ADR-0049 and the Spec each repeated section 5's record exclusions, and
  ADR-0032 said ADR-0049 narrows it while ADR-0049 was only proposed.

Fixes, after the owner decisions of 2026-10-13:

- **Runbook and manifest.** RUN-0021 (1.4.17) is `active`. The CLI's manifest
  row is `mutation: runtime` with RUN-0021 as authority, and the manifest
  test's mutation table lists it as `runtime`.
- **ADR-0049** (0.2.0) records the owner's acceptance decision. A new ADR must
  enter as `proposed` (`invalid-initial-status` otherwise), so it stays
  `proposed` here and becomes `accepted` in the first change after merge.
  ADR-0032 now says ADR-0049 narrows it once accepted.
- **Spec** (0.3.0). Contract 7 says the hook refuses Edit and Write on the
  store and does not cover the shell; criterion 4 says an Edit or Write is
  refused while the CLI reads and writes. Contract 3 and REQ-0024-FR-0015
  cite section 5 for what a record may hold, and ADR-0049 decision 6 does the
  same.
- **CLI.** `backup` refuses an output directory the caller does not own (N1)
  and removes the temporary `-journal` on failure (N5). `restore` builds the
  copy under a temporary name and publishes it with `os.link`, which never
  replaces a store created meanwhile and never shows a partial file (N2); an
  `OSError` such as `PermissionError` becomes `MEMORY_RESTORE_FAILED` (N5). A
  new test asserts the journal is 0600 (N3); it passed before the change.
  N4 is unchanged: a backup is trusted as far as its contents.
- **Tests.** Three new tests (directory owner, atomic publish, permission
  failure) failed on `b42117a68` (2 failures, 1 error); `test_agent_memory`
  now has 17 tests and all pass.

### W8 Native Acceptance

Run on 2026-10-13 after #450 merged as `40f194e99`, from two detached
worktrees of that commit under `.claude/worktrees/` (`w8-claude`, `w8-codex`),
on record `w8-two-provider-probe` (short-term):

1. Claude Code 2.1.296 (this session) wrote revision 1 from `w8-claude`.
2. codex-cli 0.162.1 (`codex exec --ephemeral`) in `w8-codex` read revision 1
   with Claude as owner, wrote revision 2 with `--expected-revision 1`, and a
   second write with `--expected-revision 1` exited 3 with
   `MEMORY_REVISION_CONFLICT: w8-two-provider-probe is at revision 2, not 1`.
   Its `git rev-parse --show-toplevel` was the `w8-codex` worktree.
3. Claude read revision 2 (owner codex) from `w8-claude` and wrote revision 3.
4. A new Claude Code session (`claude -p`, allowed only the memory CLI) read
   revision 3 and wrote revision 4.

Neither worktree held a `.workspace-memory/` directory; every call used the
one store in the main checkout. The probe was then set `ineligible`
(revision 5), and `w8-codex` was removed.

Codex ran with `-s danger-full-access` because its `bwrap` sandbox cannot
start on this host (SPEC-0232 W7). Codex project trust reaches linked
worktrees under the trusted main checkout path: the repository hooks, which
Codex runs only for a trusted project, ran in such a worktree in the SPEC-0232
W7 observation. Whether Codex honours `[memories]` in the project
`config.toml` cannot be observed from outside and stays `NOT_VERIFIED`.

### W9 Native Memory Migration

Run on 2026-10-13 after #450 merged. The main session read the six Claude
native memory files once and judged each against §5: none holds a secret,
Task progress, handoff state, approval or a governance rule copy, so all six
were eligible. Each entered the store at revision 1 with `--owner claude`, a
`native-claude-memory:<file>` source reference and `internal` sensitivity:
`env-key-parity`, `local-gate-metadata-base`, `no-stash-in-background-probes`
and `translate-with-humanize` as long-term, `umask-permission-test-failures`
and `local-gate-governance-timeout` as domain. The last one was rewritten to
its current facts (the 45-minute node timeout of SPEC-0235 and the measured
22-minute runtime) instead of copying its stale text. No native file was
changed or removed. `usage` then reported 6 revisions and 5148 body bytes
under logical limits; the store directory is 0700 and the file 0600.

### Restic Coverage Handoff

The owner asked on 2026-10-13 to proceed with Restic coverage, deferred here
earlier. SPEC-0237 owns it: the daily `hyhome-backup.sh` run now copies the
store into staging before Restic. The "Restic coverage" row below keeps the
result recorded here; SPEC-0237's Task records the new evidence.

### Renumbering

This package was drafted as SPEC-0234. SPEC-0235 reached `main` first
(`4072f8af8`), and the Registry then forbids issuing a number below its high
water (`identity-reuse-forbidden`), so the package was renumbered to SPEC-0236
during the rebase onto `ec0877f10`, and every reference in this package and
in ADR-0049 was updated. Other packages' Tasks keep the SPEC-0234 name they
recorded at the time.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Starting state | 5, 6 | W1 | Read-only file and settings inventory | `b1a6976f4` | PASS | W1 Starting State | - |
| Provider settings | 1 | W1 | Official Claude and Codex documentation | Pages read 2026-10-13 | PASS | W1 Starting State | - |
| Host library | 3 | W1 | Linked SQLite version | This host | PASS | W1 Starting State | - |
| Governance owner | 6 | W2 | Governance contract | Branch | PASS | W2 Governance Owner | - |
| Store and CLI | 2, 3 | W3 | `test_agent_memory` (8) | Branch | PASS | W3 Store and CLI | - |
| Failure handling | 3 | W4 | Stale, limits, race, full, backup failure, restore tests | Branch | PASS | W4 Limits, Failures and Backup | - |
| Hook rule | 4, 5 | W5 | `test_tool_payload` RED (5) then GREEN (15) | Branch | PASS | W5 Hook Rule and Exclusions | - |
| Native settings | 1 | W6 | JSON and TOML parse; provider renderer `--check` | Branch | PASS | W6 Native Memory Settings | - |
| Security review | 7 | W7 | Independent `security-auditor` review: pass with notes, two medium findings | `b9c9e3a07` | FAIL | Reviews at `b9c9e3a07` | - |
| Rules review | 7 | W7 | Independent `rules-engineer` review: changes required | `b9c9e3a07` | FAIL | Reviews at `b9c9e3a07` | - |
| Review fixes | 3 | W4 | `test_agent_memory` 11 failures and 1 error on `b9c9e3a07`, then 13 pass | Branch | PASS | Review Fixes | - |
| Stage owners | 6 | W2 | Metadata `check-changed` (11, 0 violations); `test_identity_history` (27); corpus lifecycle (0); links `--mode all` (0 failures); governance contract | Branch | PASS | Stage 01 and 02 Owners | - |
| Review checks | 7 | W7 | `test_agent_memory`, `test_tool_payload`, script manifest and routing tests (141); manifest, workflow contract, renderer `--check` | Branch | PASS | Review Fixes | - |
| Restic coverage | 3 | W4 | Memory backup in the `hyhome-backup.service` snapshot | - | NOT_RUN | W4 Limits, Failures and Backup | - |
| Codex trust | 1 | W6 | Main checkout `trusted`; repository hooks ran for Codex in a linked worktree | SPEC-0232 W7 observation | PASS | W8 Native Acceptance | - |
| Security re-review | 7 | W7 | Independent `security-auditor` re-review: pass with notes, low only | `b42117a68` | PASS | Re-reviews at `b42117a68` | Security review |
| Rules re-review | 7 | W7 | Independent `rules-engineer` re-review: changes required (H1, contract 7, criterion 4) | `b42117a68` | FAIL | Re-reviews at `b42117a68` | - |
| Re-review fixes | 7 | W7 | New tests RED on `b42117a68` (2 failures, 1 error) then GREEN; `test_agent_memory`, `test_tool_payload`, script manifest and routing tests (145); manifest, workflow contract, renderer `--check` (drift 0), governance contract; metadata `check-changed` (11, 0 violations); corpus lifecycle (0); `test_identity_history` (27) | Branch | PASS | Re-reviews at `b42117a68` | - |
| Rules final review | 7 | W7 | Independent `rules-engineer` final review: approve; low notes applied (RUN-0021 Overview and Trigger name the memory store) | `f46ea2ee0` | PASS | Work Log | Rules review, Rules re-review |
| Candidate | 7 | W7 | Hosted `candidate-quality`, run 38393988883 | PR #450 at `4229ac8c4` | PASS | W7 Verification | - |
| Local gate | 7 | W7 | `run-ci-gate.py --profile changed` | - | NOT_RUN | W7 Verification | - |
| Native acceptance | 1, 2, 4 | W8 | Claude, Codex and a new Claude session revise one record from two worktrees; stale write refused | `40f194e99` | PASS | W8 Native Acceptance | - |
| Migration | 1 | W9 | Six eligible Claude native memories entered once through the CLI | `40f194e99` | PASS | W9 Native Memory Migration | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 1 | pending | - | - |
| 2 | pending | - | - |
| 3 | pending | - | - |
| 4 | pending | - | - |
| 5 | pending | - | - |
| 6 | pending | - | - |
| 7 | pending | - | - |

## Review and Completion

ADR-0049 changed to `accepted` after #450 merged, as the owner decided on
2026-10-13. W8 and W9 passed. The local changed gate remains unrun, and
Codex project `[memories]` effectiveness remains unverified. Restic coverage
is no longer deferred: SPEC-0237 records the source change and a real snapshot
path in W4; that memory step succeeded while the whole service run failed on
the separate OpenBao snapshot-token gap. Its source/snapshot observation does
not establish a restore or accept this package's pending criteria. No criterion
is accepted until the owner accepts it.

W2 to W7 merged in #450 with the review and re-review fixes, after the final
rules review approved.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
