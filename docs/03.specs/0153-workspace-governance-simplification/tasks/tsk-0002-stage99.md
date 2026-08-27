---
profile_id: task
status: completed
artifact_id: task-0153-0002
artifact_type: task
parent_ids:
  - SPEC-0153
  - plan-0153
created: 2026-08-20
updated: 2026-08-21
completed_at: 2026-08-21
---

# Task 0002: Establish Stage 99 Registry Authority

## Objective

Establish `docs/99.templates/registry.json` as the sole default machine
authority for document profiles, paths, identities, lifecycle, traceability,
and template registration without executing a corpus transition.

## Inputs

- [Specification](../spec.md)
- [Implementation Plan](../plan.md)
- [Stage 99 Registry](../../../99.templates/registry.json)
- [Migration 0003](../../../98.archive/migrations/0003-workspace-governance-simplification.md)
- Frozen Task 1 baseline commit `71f89ba1`

## Work Log

| Event | Actual result |
| :--- | :--- |
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

| Check | Command or scope | Result |
| :--- | :--- | :--- |
| Initial RED | Registry, identity-history, four-digit focused tests | Three expected import/setup errors before production files existed. |
| Final Registry and history | `tests.validation.test_document_registry` plus `tests.validation.test_identity_history` | `28/28` passed in `7.925s`. |
| Final metadata and lifecycle | focused metadata Registry regression plus lifecycle public contracts | `10/10` passed in `1.806s`. |
| Default contract CLI | `check-document-metadata.py --mode check-contracts` | `violations=0`. |
| Full-history contract CLI | `check-document-metadata.py --mode check-contracts --history-scope full` | `violations=0`. |
| Static validation | JSON parse, Ruff, `py_compile`, `git diff --check` | Passed. |
| Baseline lifecycle debt | clean approved baseline reproduction | Five identical legacy-fixture failures; no Task 2 regression claimed. |
| Broad suite bound | lifecycle and script-manifest broad commands | Stopped at the enforced `300s` cutoff; not reported as PASS. |

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

### Migrated Evidence Provenance

The original bootstrap evidence is recoverable as Git blob
`f271bcf127e2ad766b6006210e9cba1d41176887` with SHA-256
`1fc246c7b23a9d998939d1f40ae1af82fc41f7aed151ae3a1b162bbb9d2010ba`.
Every Task 2 Work Log, Verification, Review, and Commit field from that source
is represented above or below; Task 1 fields are owned by
`tsk-0001-control-plane.md`.

The completeness mapping is field-based: all fourteen source Task 2 Work Log
rows above are copied verbatim; the Task 2 verification results and bounded
baseline-debt statements are represented in the verification table; the source
Task 2 review row and commit entry are preserved below. The source also records
that the controller staged exactly `39` Task 2 paths, verified the cached
boundary and diff hygiene, and committed without a Task 3 corpus transition.

## Review Evidence

| Review | Status | Findings and disposition |
| :--- | :--- | :--- |
| Specification closure | approved | Final `C0/I0/M0`; canonical Registry semantics and exact Task 2 boundary verified. |
| Task 2 Python review | complete | Final quality closure `APPROVED C0/I0/M0`. Exact closure evidence: focused policy/path/symlink `2/2`, Registry plus identity `28/28`, metadata plus lifecycle public contracts `10/10`, default and full-history contract CLIs each `violations=0`. The legacy lifecycle `I1` remains withdrawn after clean-baseline reproduction. |
| Legacy lifecycle finding | withdrawn | The cited five failures reproduced identically in a clean approved baseline and remain owned by later migration tasks. |

## Commit Ledger

- `c891118e736ee46c709b22de459c20858467ddd3` —
  `feat(docs): establish stage 99 registry authority`
- `8cc65475` — `docs: record stage 99 registry commit`

## Rulings

- The Registry is the default authority; the legacy Stage 99 support tree is a
  bounded compatibility input until its consumers migrate.
- Broad commands that reached the mandatory five-minute boundary are recorded
  as bounded evidence, never as successful gates.

## Deferred Items

- Exact Operations subject membership is owned by Task 8's approved migration
  manifest because subject number and role artifact ID are intentionally
  independent identities.
- The proven legacy lifecycle and script-manifest baseline debt remains with
  the later owning tasks.
