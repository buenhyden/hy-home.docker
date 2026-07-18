---
layer: agentic
---

# Corpus Migration Contract

## Overview

This document is the sole human owner for corpus migration. It explains how a
reviewer classifies a bounded document set, proves a disposition, and promotes
one reviewed wave without turning a dry run into repository truth.

The executable owner is
[`document-corpus-migration-contract.yaml`](./document-corpus-migration-contract.yaml).
The metadata registry and checker remain authoritative for artifact profiles,
identity, relations, lifecycle transitions, serialization, and path matching.
This contract neither redefines those semantics nor authorizes a corpus wave.

## Ownership Boundary

The manifest owns classification and evidence for one approved baseline scope.
It does not select document profiles, invent identities, decide lifecycle state,
or mutate targets. A Plan approves the wave and protected boundaries; its Task
records actual commands, review verdicts, commits, deviations, and rollback.

The repository-local manifest dispositions are `migrate`, `preserve`, `move`, `merge`, `archive`, `delete`, `regenerate`, `exempt`.
Their target conditions are exact machine-contract values:

| Disposition | Target condition |
| --- | --- |
| `migrate` | `migrate` -> `source-equals-target` |
| `preserve` | `preserve` -> `source-equals-target` |
| `move` | `move` -> `target-distinct` |
| `merge` | `merge` -> `target-distinct` |
| `archive` | `archive` -> `target-distinct` |
| `delete` | `delete` -> `target-null` |
| `regenerate` | `regenerate` -> `source-equals-target` |
| `exempt` | `exempt` -> `source-equals-target` |

## Manifest Shape and Evidence

The top-level fields are `schema_version`, `wave`, `baseline_commit`, `generated_by`, `enforcement`, `entries`.

Foundation remains valid under schema version 1; schema version 2 keeps those
top-level fields while replacing `artifact_type` in each row with nullable
`artifact_type_before` and `artifact_type_after`, plus the required
`surface_class`. This makes an unsupported/native baseline and its reviewed
target classification explicit without pretending that a binary or
platform-owned file is typed Markdown.

A v2 wave may select complete source roots and exact direct source paths. The
generator expands source roots from Git tree metadata at the pinned baseline,
unions the direct source paths, and emits one sorted row per selected path.
Native and binary surfaces are classified from safe path, mode, and blob
metadata; only declared Markdown/profile surfaces are decoded as UTF-8.

Each entry uses `source_path`, `target_path`, `artifact_id`, `artifact_type`, `status_before`, `status_after`, `parent_ids`, `disposition`, `canonical_replacement`, `active_consumers`, `partition_plan`, `preservation_class`, `evidence`, `review_verdict`.

The evidence object uses `commands`, `sources`, `repository_paths`, `consumer_scan`, `rollback`.
The review object uses `specification`, `quality`, and each verdict is one of `pending`, `pass`, `changes-required`.

The machine contract owns exact types, nullability, and domains for `schema_version`,
`wave`, `baseline_commit`, `generated_by`, `enforcement`, `entries`,
`source_path`, `target_path`, `artifact_id`, `artifact_type`, `status_before`,
`status_after`, `parent_ids`, `disposition`, `canonical_replacement`,
`active_consumers`, `partition_plan`, `preservation_class`, `evidence`,
`review_verdict`, `evidence.commands`, `evidence.sources`,
`evidence.repository_paths`, `evidence.consumer_scan`, `evidence.rollback`,
`review_verdict.specification`, and `review_verdict.quality`. Authors must use
YAML null where the machine contract permits absence; sentinel text is not a
substitute for missing data.

Lists and entries are serialized deterministically for reviewable diffs. Their
order does not create approval rank, dependency priority, or semantic truth.

### Foundation reviewed evidence

Foundation reviewed rows use the lifecycle validator's canonical NUL-safe Git
scan. Its positive scope covers current tracked root files, provider adapters,
Stage 00 through Stage 05 authoring and execution roots, Stage 99 contracts and
templates, and the active examples, infrastructure, projects, scripts, secrets,
and tests roots. It omits Stage 90 reference or generated evidence, Stage 98 and
root archive payloads, Graphify collateral, and `_workspace` staging by root
policy. The row source and the Foundation Spec, Plan, and Task are exact
exclusions because they are self or review evidence, not downstream consumers.
Every remaining fixed-string match is a current tracked direct consumer and the
sorted scan result must equal `active_consumers`; a raw repository-wide grep or
an unverified empty list is invalid.

Once Foundation review has started—because enforcement is `blocking` or either
independent verdict is `pass`—`commands`, `sources`, `repository_paths`, and
`consumer_scan` must each be non-empty. Both `sources` and `repository_paths`
must equal the deterministic set containing the row source, the Foundation
Spec, and the Foundation Plan. This keeps the evidence owner set explicit and
prevents a promoted row from discarding the proof that supported review. A
pending advisory skeleton may retain all five evidence lists empty.

Foundation evidence commands pin both ends of the reviewed range with full Git
commit IDs. For each source, rollback is either one `git revert --no-commit`
command containing exactly the source-changing commits in newest-to-oldest
order, or an empty list only when the immutable range proves an unchanged
`preserve` row. A symbolic ref, floating range, unrelated commit, empty rollback
for another disposition, or invented rollback action is invalid. After an
authored rollback, canonical generated owners are rerun in their declared
order; later promotion rollback is recorded separately against the immutable
promotion commits.

## Classification and Destructive Proof

Manifest-first classification occurs before target mutation. Every selected
baseline path appears exactly once. Declared outputs are not fictional source
rows, and an unapproved future wave remains empty and advisory.

A candidate hash, title, topic, or type match is only review input. Merge,
archive, or deletion requires one canonical owner, proof that role, purpose,
topic, and scope agree, an enumeration of every active consumer, replacement
semantics where applicable, preservation evidence, complete rollback evidence,
and independent specification and quality verdicts of `pass`. An honestly
verified orphan keeps an empty consumer list and records the scan that proved
it; authors never fabricate a consumer.

`canonical_replacement` is required for merge, optional for archive and delete,
and forbidden for migrate, preserve, move, regenerate, and exempt. Any supplied
replacement must resolve to the one validated current target. Archive-specific
replacement truth is interpreted with the archive disposition by the
[archive and retention contract](./archive-retention-contract.md).

## Wave Promotion and Dry Runs

Generator output under `_workspace/repo-support/` is transient, ignored,
non-secret dry-run material. It is not canonical evidence and cannot promote a
wave. Promotion requires an approved manifest in its declared Stage 90 path,
machine validation, complete Task evidence, independent passing reviews, and
an explicit contract change from advisory to blocking. A skeleton remains
pending and never invents parents, consumers, replacements, evidence, or
approval.

Full-corpus debt remains advisory until its separately approved wave promotes
that exact scope. Exceptions, when the later gate permits them, must remain
finding-specific, path-bounded, owned, reasoned, approved, expiring, and tied
to a non-empty exit condition and safe evidence paths.

## Rollback and Preservation

Rollback reverts the affected logical wave commits in reverse order and then
regenerates only their derived outputs. Never rewrite history, weaken the
contract, or delete evidence merely to make a manifest pass. A failed later
wave does not authorize reverting a previously approved wave.

Manifest evidence may record bounded paths, stable codes, commands, counts,
and Git object identities. The shared value classifier applies to every string
in `commands`, `sources`, `repository_paths`, `consumer_scan`, and `rollback`.
None may contain body payloads, snapshot bytes, credential or secret
assignments, tokens, private keys, auth files, shell history, raw logs, or
diagnostic payloads. Findings remain value-free and never echo rejected data;
safe credential-related option names without assigned values remain allowed.

## Related Documents

- [archive and retention contract](./archive-retention-contract.md)
- [document metadata profiles](./document-metadata-profiles.yaml)
- [frontmatter contract](./frontmatter-contract.md)
- [lifecycle status](./lifecycle-status.md)
- [template governance](./template-governance.md)
- [Foundation task evidence](../../04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md)
