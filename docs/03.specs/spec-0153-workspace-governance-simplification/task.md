---
status: active
artifact_id: task-0153-01
artifact_type: task
parent_ids:
  - spec-0153
  - plan-0153
created: 2026-08-20
updated: 2026-08-20
---

# Task: Workspace Governance Simplification Bootstrap Evidence

## Overview

This transient Task records actual Task 1 control-plane and Task 2 Stage 99
authority evidence before the canonical prefixless Spec 0153 package and its
numbered Task records exist. Task 3 migrates the evidence into
`tsk-0001-control-plane.md` and `tsk-0002-stage99.md`, verifies field
completeness, and removes this file.

## Inputs

- [Specification](spec.md)
- [Implementation Plan](plan.md)
- [ADR-0029](../../02.architecture/decisions/adr-0029-workspace-governance-authority.md)
- [Migration 0003](../../98.archive/migrations/mig-0003-workspace-governance-simplification.md)
- Frozen baseline commit `889d3868ecd0913cddac79a718584a54a8453525`

## Goals and Non-goals

- Register the cross-stage authority decision and a deterministic approved
  migration selection.
- Prove every tracked transition source is a regular baseline blob and every
  planned-output source has an earlier typed owner.
- Record actual RED/GREEN evidence without prospectively approving or executing
  any transition.
- Do not move or delete a corpus path, change provider surfaces, stage, push,
  merge, or change runtime state. Task 1 did not modify validators; Task 2 may
  modify only its plan-listed Stage 99 adapters and validators.

## Scope and Change Boundaries

The allowed Task 1 paths are the ADR, Migration, this Task, the focused test,
and bounded Spec/Plan evidence. Task 2 is limited to the Registry, schemas,
registered templates, document-governance adapters, their manifest rows and
named tests listed in `plan.md`. All corpus transitions, provider surfaces,
unlisted scripts, runtime, remote, and secret surfaces are excluded.

## Approval Evidence

| Approval source | Protected surface | Boundary | Rollback or recovery | Redaction boundary |
| :--- | :--- | :--- | :--- | :--- |
| User approval of the implementation plan and Subagent-Driven execution | Documentation and AI-agent governance control plane | Task 1 may create review evidence only; Migration execution requires a second explicit approval of the exact row packet | Discard the unstaged Task 1 diff; no corpus transition has executed | Paths, stable IDs, counts, commit objects, command outcomes, and review verdicts only |
| Controller ruling after the initial RED | Migration schema version 2 | Add typed `planned_creations`, sequential `planned-output` provenance, unique row IDs, and active-consumer lists without changing the Spec's semantic contract | Revert the bounded Plan/Test/Migration schema correction | No runtime or credential data |

The user approved the exact Migration selection digest on `2026-08-20`.
`approval.status`, `approved_by`, and `approved_at` now record
`approved/user/2026-08-20`. The Migration document's `status: archived`
frontmatter satisfies the
currently authoritative Stage 99 migration-document profile and describes its
evidence-preservation role; it does not approve the internal transition ledger.

## Work Breakdown

1. Read the advisory Graphify report and corroborate it against live Stage 00,
   Stage 99, Spec, Plan, and tracked inventory.
2. Add the missing-control-plane test and record its actual RED result.
3. Record ADR-0029.
4. Detect and correct the tracked-source-only schema defect without weakening
   source, target, collision, or recovery checks.
5. Freeze planned creations, transitions, active consumers, and the approval
   packet at the baseline commit.
6. Run focused tests, changed metadata, and diff hygiene.
7. Preserve the completed independent re-review and explicit user approval
   evidence, run the approved-state suite, and hand commit ownership to the
   controller.
8. Capture Registry and identity-history RED before creating production files.
9. Establish the immutable Registry, schemas, allocation state, and registered
   copyable templates without deleting the legacy transition input.
10. Switch metadata and lifecycle entry points to Registry authority while
    bounding the lifecycle translation adapter until Task 3.
11. Run focused and named GREEN suites, bounded manifest checks, static checks,
    and an independent Python review before handoff.

## Work Log

| Event | Actual result |
| :--- | :--- |
| Graph corroboration | Graphify was built from `f8a72211` and is advisory. Live HEAD, Stage 00/99, Spec, Plan, and tracked inventory were used as authority. |
| Initial RED | The control-plane test failed because ADR-0029 was absent. |
| Ruling | A row contract that required every source to be tracked at the baseline could not represent ADR-0029, Migration 0003, and later Spec Task outputs consumed by subsequent Tasks. Schema version 2 separates typed creations from transitions and resolves planned outputs only through earlier owners. |
| Selection freeze | `17` planned creations and `903` transition rows; `3,571` owner-ordered literal/Markdown consumer edges; edge SHA-256 `2f1840983d98ed93ffdc183305c49b389b17e5c8362538e5df97d451be2b9139`; baseline-and-policy-bound selection SHA-256 `9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1`. |
| Consumer-scope correction | The first GREEN over-selected `6,550` edges and the initial review remediation then under-selected `1,840` by excluding every delete-disposition consumer. The current derivation excludes a delete consumer only when its owner Task is no later than the source transition owner, resolves repository-local Markdown links, and retains Stage 98, Graphify, and immutable/generated Stage 90 exclusions. |
| Initial review remediation | An initial review attempt edited shared files and therefore cannot serve as an independent review. Local re-audit retained independently justified technical corrections: the active-consumer exclusions above, a requirement that `git cat-file -t <baseline_commit>` return `commit`, and rejection of placeholder artifact IDs. No review approval is claimed. |
| Placeholder artifact correction | Owner review found `16` deleted template rows with `artifact_id: <artifact-id>`. Those template placeholders are not stable artifact identities, so the rows now use `artifact_id: null`, the test rejects placeholder IDs, and the selection SHA-256 changed to `b79f7da97811ab51fadb33ada15efaaaf51a40cef9bf55a31d4448ff30a2f9cf`. |
| Final quality review | `CHANGES_REQUIRED`, `C0/I5/M0`: consumer ordering/relative links, strict YAML, canonical namespaces, baseline/digest binding, and final Migration compaction were incomplete. |
| Quality remediation RED | The expanded focused suite ran `8` tests with `7` failures in `6.089s`, covering both required consumer edges, four noncanonical path variants, missing policy/compaction data, and ambiguous YAML acceptance. |
| Quality remediation | Added owner-order-aware consumer derivation, shared safe Markdown link resolution, one-fence duplicate/alias/anchor/tag rejection, canonical POSIX namespaces and collision mutations, pinned `ls-tree -rz` blob provenance, policy/edge digest selection binding, and Task 10/13 final-compaction requirements. |
| Quality re-review | `CHANGES_REQUIRED`, `C0/I1/M0`: execution approval states and the final compacted lifecycle state were not explicitly separated. |
| Lifecycle remediation RED | The focused suite ran `11` tests with one failure and one error in `6.545s`: the execution-state validator was absent and schema version `2` was accepted as a final compacted ledger. |
| Lifecycle remediation | Schema version `2` accepts only state-specific `pending` or `approved` approval fields; schema version `3` is the field-minimal durable mapping/recovery ledger. Approval and final-state mutations run in the same suite. |
| Final independent re-reviews | Specification `C0/I0/M0`; quality `C0/I0/M0`. The earlier quality `I5` and lifecycle `I1` are addressed. |
| Exact row-set approval | The user approved selection SHA-256 `9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1` on `2026-08-20`. The execution ledger records `approved/user/2026-08-20`; row/edge counts and both digests are unchanged. |
| Approved-state GREEN | The approved execution ledger passed `11/11` in `7.590s`. The Migration is `503,198` bytes over `1,039` lines, with one YAML flow row per mapping. |
| Changed metadata | `selected=5 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Diff hygiene | `git diff --check` exited `0` with no output. |
| Task 2 Registry RED | The focused Registry/identity/four-digit command failed with three import/setup errors because `registry.py`, `identity_history.py`, and `registry.json` did not exist. |
| Task 2 initial GREEN | Registry, identity-history, and four-digit suites passed `31/31` in `7.36s`; the metadata Registry contract reported `violations=0`. |
| Task 2 compatibility convergence | The full metadata suite passed `243/243` in `130.177s`. Active machine-template safety tests use Registry paths; bounded legacy YAML behavior remains explicit fixture coverage. |
| Task 2 bounded combined GREEN | Registry, identity-history, metadata, and four-digit suites first passed `273/273` in `135.204s`, then passed `282/282` in `146.631s` after the first independent-review remediation wave. |
| Task 2 final focused GREEN | The scope-frozen Registry suite passed `16/16` in `3.255s`; after spec-review remediation identity history passed `6/6` in `14.615s`; Registry-first lifecycle `PublicContractTests` passed `8/8` in `0.740s`. |
| Task 2 lifecycle adapter | Three focused default-Registry archive and diagnostic cases passed in `11.742s`. A full lifecycle run was stopped by the mandatory `300s` cutoff. The three independently cited merge-owner tests fail five `manifest-replacement-invalid` assertions identically in both this worktree and a clean archive of approved HEAD, so they remain proven baseline debt. |
| Task 2 manifest boundary | Sorted schema, taxonomy evidence, and authority tests passed together `3/3` in `0.998s`. Two consumer-evidence failures (`scripts/manifest.yaml`, `sync-provider-surfaces.sh`) and six unmanifested validation scripts are outside Task 2 and pre-existing; the broad manifest command was stopped at the same `300s` bound. |
| Task 2 history performance RED/GREEN | An early single broad `git log -G` scan hit its `45s` fail-closed timeout. A temporary `-S artifact_id:` split passed but did not satisfy the Plan. The spec-review regression RED then failed because no exact query registry existed. Six stage-scoped canonical-and-legacy ID-family `git log --no-ext-diff -U0 -G` queries now share one cumulative `45s`/`16 MiB` bound; identity passed `6/6` in `14.615s`, and the exact full-history CLI completed with `violations=0` in `9.284s`. |
| Task 2 static checks | Registry contract `violations=0`; registered-template concrete-target scan had no matches; JSON parse, Ruff, `py_compile`, and `git diff --check` passed. |
| Task 2 independent re-review | Final bounded review returned `C0/I0/M0`. An initial lifecycle `I1` was withdrawn after the exact five failures reproduced identically in the clean approved baseline. |
| Task 2 final quality review | The final quality pass returned `C0/I3/M0`: non-identical path-language intersections, post-hoc Git output caps, and the Registry contract early-return bypass remained. |
| Task 2 quality remediation RED | The overlap tests could not import the missing decider; fake stdout/stderr Git producers each reached the `4s` timeout instead of the `1 KiB` cap; the default Registry CLI omitted the tracked README body finding. |
| Task 2 quality remediation GREEN | Segment-NFA path intersection, streaming cumulative stdout/stderr enforcement, and merged Registry/repository contracts passed final Registry+identity `25/25` in `7.799s` and focused metadata/lifecycle `9/9` in `1.028s`. Default and full-history contract CLIs each report `violations=0`. |
| Task 2 final quality closure | `APPROVED C0/I0/M0`. The closure evidence is focused policy/path/symlink `2/2`, Registry plus identity `28/28`, metadata plus lifecycle public contracts `10/10`, default and full-history contract CLIs each `violations=0`, and passing Ruff, `py_compile`, and `git diff --check`. |

## Verification Evidence

### Initial RED

Command:

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_workspace_governance_migration -v
```

Actual result:

```text
test_governance_migration_control_plane_exists ... FAIL
AssertionError: False is not true
Ran 1 test in 0.000s
FAILED (failures=1)
```

The failure was specifically the missing
`docs/02.architecture/decisions/adr-0029-workspace-governance-authority.md`.

### Task 2 Registry RED and GREEN

The required focused RED command failed before production implementation with
three import/setup errors for the absent Registry loader, identity-history
module, and Registry document. After implementation, the exact focused command
passed `31/31` in `7.36s`.

The final bounded named command was:

```bash
PYTHONPATH=. python3 -m unittest -v \
  tests.validation.test_document_registry \
  tests.validation.test_identity_history \
  tests.validation.test_document_metadata \
  tests.validation.test_four_digit_document_identity
```

It passed `273/273` in `135.204s`. After the first independent-review
remediation wave, the same bounded command passed `282/282` in `146.631s`.
The scope-frozen final checks were intentionally focused: Registry passed
`16/16` in `3.255s`, identity history passed `6/6` in `14.615s`, and the
Registry-first lifecycle public contract passed `8/8` in `0.740s`.

An early identity run exposed a real performance RED: the single broad
historical `git log -G` query exceeded its fail-closed `45s` timeout. A
temporary `-S artifact_id:` split restored runtime but did not meet the Plan's
exact ID-family pickaxe contract. The spec-review regression test therefore
failed before remediation because the module had no registered exact query
set. The implementation now uses six stage-scoped canonical-and-known-legacy
ID-family `git log --no-ext-diff -U0 -G` queries under one cumulative `45s` and
`16 MiB` budget, while retaining the tracked-current-corpus, rename, no-follow,
and UTF-8 checks. Identity history passed `6/6` in `14.615s`; the exact
`check-document-metadata.py --mode check-contracts --history-scope full`
command completed with `violations=0` in `9.284s`.

The final quality pass then reported `C0/I3/M0`. Focused RED proved three
remaining gaps: the path overlap mutation could not import a language
intersection decider, adversarial fake Git processes writing stdout and stderr
each ran to the `4s` timeout instead of failing at the `1 KiB` test cap, and the
default Registry contract omitted an incomplete tracked README body. The
remediation uses a finite segment NFA product to decide every registered path
grammar intersection, rejects any intersecting non-fallback profile pair, and
keeps exact disjoint literals valid. Git output is now consumed through
nonblocking `Popen` pipes under the shared deadline and remaining byte budget;
overflow terminates, drains, kills when necessary, and reaps the child without
retaining bytes beyond the cap. The Registry contract now combines its schema,
template and optional history findings with Registry-aware repository README
checks, while Release and legacy support duplication gates stay disabled.

The resulting focused Registry and identity suites passed `25/25` in `7.799s`;
metadata Registry regression plus lifecycle public contracts passed `9/9` in
`1.028s`. Both the default contract CLI and the exact full-history form report
`violations=0`, with findings deduplicated before rendering.

A subsequent bounded quality re-review reported `C0/I3/M0`. Focused RED proved
that noncanonical path patterns with repeated separators, dot segments,
unconsumed braces, or controls could pass; canonical Markdown profiles without
template roles did not share one explicit `profile_id` ownership rule; and the
public no-profile manifest generator passed the flat Registry mapping into a
legacy-envelope inference path. The Registry now declares one
`frontmatter_policy` per profile: every canonical Markdown profile requires an
exact `profile_id`, machine contracts prohibit frontmatter, and only the
unsupported fallback is unmanaged. A parameterized minimal-artifact regression
passes every Markdown profile, including package, Operations, Stage README,
governance, generated, and repository-support roles. Path patterns require an
exact canonical POSIX round trip and consume every registered token. The public
manifest generator now constructs the bounded Registry transition adapter and
records canonical Spec before/after types as `spec`/`spec`.

After this remediation, Registry plus identity passed `26/26` in `9.062s`;
focused metadata and lifecycle public contracts passed `10/10` in `2.154s`.
The default and full-history contract CLIs both report `violations=0`. Ruff,
`py_compile`, and `git diff --check` pass. The path-language automaton was
separated into the existing taxonomy responsibility, leaving `registry.py` at
`726` lines and `taxonomy.py` at `404` lines.

The last bounded Python re-review returned `C0/I1/M0` because SIGKILL was
followed by a timed `wait()` whose timeout was swallowed. A deterministic fake
child reproduced the unreaped state. Cleanup now treats termination or reap
failure as an explicit `IdentityHistoryError`, performs an unbounded reap only
after successful SIGKILL, and asserts `poll()` is terminal. The focused reap
and adversarial stdout/stderr tests passed `2/2` in `0.052s`; the final Registry
plus identity run passed `27/27` in `8.179s`, focused metadata and lifecycle
public contracts passed `10/10` in `1.901s`, both contract CLIs report
`violations=0`, and Ruff, `py_compile`, and `git diff --check` pass.

The subsequent final quality closure returned `C0/I3/M0`. Exact RED produced
four failures: a Guide could switch to `frontmatter_policy: absent` with empty
key lists, U+0085 and U+200B could enter a registered path pattern, and the CLI
resolved a Registry symlink before the loader's no-follow check. Registry
semantics now derive the Markdown obligation from every non-fallback `*.md`
path profile rather than trusting its declared policy. Path grammar rejects all
Unicode non-printable characters, including control and format categories. The
CLI passes the original Registry path to the bounded loader, preserving its
symlink and non-regular-file checks. The focused RED cases passed `2/2` in
`0.718s`; Registry plus identity passed `28/28` in `7.925s`; focused metadata
and lifecycle public contracts passed `10/10` in `1.806s`; default and full
history contract CLIs both report `violations=0`; Ruff, `py_compile`, and
`git diff --check` pass.

The final read-only quality closure approved Task 2 with `C0/I0/M0` using the
exact closure evidence: focused policy/path/symlink `2/2`, Registry plus
identity `28/28`, metadata plus lifecycle public contracts `10/10`, and default
and full-history contract CLIs each at `violations=0`.

The lifecycle adapter's Registry-default public contract suite passed `8/8`.
The full historical lifecycle suite cannot complete within the enforced
five-minute command boundary; it exited `124` at `300s`. The three independently
cited merge-owner tests were then run serially. They fail five
`manifest-replacement-invalid` assertions identically in the Task 2 worktree
and in a clean `git archive HEAD` of approved baseline `71f89ba1`, whose
tracebacks resolve under the temporary baseline directory. Those tests
explicitly load the legacy YAML profile fixture, so this is recorded as proven
baseline debt rather than hidden as a Task 2 success.

The Registry contract command reported:

```text
metadata repository contracts: violations=0
```

Bounded script-manifest checks passed Registry-related schema, taxonomy, and
authority assertions (`3/3` in `0.998s`). Remaining failures name only the pre-existing
`scripts/manifest.yaml` and `sync-provider-surfaces.sh` consumer evidence plus
six validation scripts absent from the manifest; Task 2 did not modify those
unowned surfaces.

### Focused GREEN

Command:

```bash
PYTHONPATH=. python3 -m unittest \
  tests.validation.test_workspace_governance_migration -v
```

Actual result:

```text
test_consumer_policy_covers_ordered_and_relative_edges ... ok
test_execution_ledger_lifecycle_mutations ... ok
test_final_compaction_contract_is_minimal ... ok
test_governance_migration_control_plane_exists ... ok
test_namespace_mutations_fail_closed ... ok
test_paths_are_canonical_posix ... ok
test_approved_selection_is_exact_and_reviewable ... ok
test_planned_creations_are_unique_and_typed ... ok
test_structural_source_families_are_complete ... ok
test_transition_rows_fail_closed ... ok
test_yaml_contract_rejects_ambiguity ... ok
Ran 11 tests in 7.590s
OK
```

### Quality Remediation RED

The expanded suite initially ran `8` tests with `7` failures in `6.089s`.
Failures proved that the pending contract omitted the ordered
`check-repo-contracts.sh` consumer, the Architecture Decisions README relative
ADR link, canonical-path rejection, consumer policy and final-compaction data,
and strict one-fence YAML parsing. No corpus transition executed during RED or
GREEN.

### Lifecycle Remediation RED

The quality re-review suite ran `11` tests with one failure and one error in
`6.545s`. It proved there was no explicit pending/approved execution-state
validator and that execution schema version `2` could incorrectly pass as the
final compacted ledger. The corrected suite validates pending null fields,
approved nonempty identity and real `YYYY-MM-DD` date, invalid state/date
combinations, schema-version-3 final minimality, null recovery, and forbidden
execution fields.

### Initial Review Remediation Probe

During the invalid initial review attempt, a mutation replaced `baseline_commit`
with the same commit's tree object SHA. The test suite failed before any row
validation:

```text
AssertionError: baseline_commit must identify a Git commit
Ran 0 tests in 0.013s
FAILED (errors=1)
```

Changed metadata then reported
`selected=5 violations=0 legacy_exceptions=0 transition_overrides=0`, and
`git diff --check` exited `0` with no output. A later owner review correction
changed deleted template placeholder artifact IDs to null and added a
placeholder rejection assertion before the current GREEN run.

## Controlled Agent Pre-commit Evidence

The controller staged exactly the six Task 1 paths, verified the cached path
set and `git diff --cached --check`, and created the approved logical commit.
No corpus transition, push, merge, runtime mutation, or secret operation was
performed.

For Task 2, the controller staged exactly `39` owned paths (`21` added and `18`
modified), verified the cached boundary and diff hygiene, and created logical
commit `c891118e736ee46c709b22de459c20858467ddd3`. Task 2 is complete with final
quality closure `APPROVED C0/I0/M0`; no Task 3 corpus transition was included.

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Implementation self-review | complete | Focused tests, exact selection digest, family counts, changed metadata, and diff hygiene are current. |
| Independent specification review | complete | Final re-review returned `C0/I0/M0` for the corrected exact packet. |
| Independent quality review | complete | Initial final review returned `C0/I5/M0`, lifecycle re-review returned `C0/I1/M0`, and final re-review returned `C0/I0/M0`; all findings are addressed. |
| User row-set approval | approved | Exact selection SHA-256 `9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1`, approved as `user` on `2026-08-20`. |
| Task 2 Python review | complete | Final quality closure `APPROVED C0/I0/M0`. Exact closure evidence: focused policy/path/symlink `2/2`, Registry plus identity `28/28`, metadata plus lifecycle public contracts `10/10`, default and full-history contract CLIs each `violations=0`. The legacy lifecycle `I1` remains withdrawn after clean-baseline reproduction. |

## Commit Ledger

- `e58d91796409fd562a8b395293942c0f73949c24` —
  `docs: register workspace governance migration`
- `c891118e736ee46c709b22de459c20858467ddd3` —
  `feat(docs): establish stage 99 registry authority`

## Deferred and Blocked Items

- Task 1 is complete. Task 2 may install the Stage 99 authority before any
  approved corpus transition executes.
- Recovery commits remain null while rows are planned. They become mandatory
  before a moved or deleted row is completed.
- Ordinary in-place semantic edits remain in the owning Task file lists and are
  intentionally not duplicated as Migration rows.

## Related Documents

- [Specification](spec.md)
- [Implementation Plan](plan.md)
- [ADR-0029](../../02.architecture/decisions/adr-0029-workspace-governance-authority.md)
- [Migration 0003](../../98.archive/migrations/mig-0003-workspace-governance-simplification.md)
