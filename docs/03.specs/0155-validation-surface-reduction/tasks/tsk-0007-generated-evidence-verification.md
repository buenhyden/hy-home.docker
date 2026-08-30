---
profile_id: task
status: completed
artifact_id: task-0155-0007
artifact_type: task
parent_ids: [SPEC-0155, plan-0155]
created: 2026-08-30
updated: 2026-08-30
---

# Generated Evidence Verification

## Objective

Verify the plan's hypothesis that three snapshot pairs under
`docs/90.references/data/` are duplicates, and that generator-written snapshots
lack `generated_by`. Plan Task 7.

## Inputs

- Six packages: `0066`, `0067`, `0068`, `0069`, `0073`, `0074`.
- `scripts/manifest.yaml`, the authoritative declaration of which script writes which output.
- `scripts/validation/target_surface_contract.py` and `check-document-corpus-lifecycle.py`, which read `0069`.

## Work Log

| Step | Action                                                | Result                                       |
| :--- | :---------------------------------------------------- | :------------------------------------------- |
| 1    | Read each of the six and recorded what it measures    | 3 payload packages, 3 rendered summaries     |
| 2    | Compared `0066` against `0067/data.yaml`              | **Same wave, commit, entries, enforcement**  |
| 3    | Searched for a generator that writes any of the six   | **None**                                     |
| 4    | Traced who reads `0069/data.yaml`                     | Pinned **SHA256**, plus `TARGET_MANIFEST`    |
| 5    | Swept all references, untruncated                     | 5 test modules and 1 pinned path list        |
| 6    | Read `outputs` from the manifest for `generated_by`   | 8 declared, **8 already carry the field**    |

**The pair hypothesis is confirmed as duplication and rejected as a merge.**
`0066-foundation-summary/README.md` is a Markdown rendering of
`0067-foundation/data.yaml`: the same wave `foundation`, the same baseline
commit `e00e1483`, the same 24 entries, the same `blocking` enforcement. It is
the same measurement in a second format, which is what the Spec suspected.

Merging is nonetheless refused, because the payload is frozen:
`check-document-corpus-lifecycle.py` pins `0069/data.yaml` through
`TASK7_IMMUTABLE_MANIFEST_SHA256`, `target_surface_contract.py` binds it as
`TARGET_MANIFEST`, `operations_catalog.py` registers all four `0066`–`0069`
paths in a pinned list, and five test modules assert against them. Any merge
changes a digest that three separate contracts treat as immutable.

The plan anticipated this: "A pair that measures different things is not merged;
the Spec's list is a hypothesis to verify, not an instruction." The verification
result is that the pairs measure the *same* thing and still cannot be merged,
because the duplication is held in place by frozen contracts rather than by the
documents themselves. Removing the freeze is the actual fix and it is larger
than this Task; SPEC-0157 owns it.

**`generated_by` is already complete.** The plan's Step 3 expected gaps. The
manifest declares eight generated outputs under `docs/90.references/data/`, and
all eight carry `generated_by`. A first pass using a grep heuristic suggested
three were missing; reading the manifest's `outputs` field, which is the
authority for what a script writes, showed the heuristic had matched scripts
that merely mention a path. The heuristic was wrong, not the corpus.

**No change was invented to justify the Task.** Both steps verified clean. The
Task records the measurement and the reason a merge would be incorrect, which is
the deliverable when a hypothesis fails.

**Rollback.** No production change to revert.

**Skipped checks.** None.

## Verification Evidence

| Measure                                                   | Expected by plan |         Measured |
| :-------------------------------------------------------- | ---------------: | ---------------: |
| Snapshot pairs that can be merged                         |                3 |            **0** |
| Generators writing any of the six                         |               ≥1 |            **0** |
| Contracts pinning `0069/data.yaml`                        |                — |            **3** |
| Test modules asserting against the six                    |                — |            **5** |
| Declared generated data outputs lacking `generated_by`    |               ≥1 |        **0 of 8** |

| Command                                                                                    | Result                                     |
| :----------------------------------------------------------------------------------------- | :----------------------------------------- |
| `check-document-links.py --mode all`                                                       | **failures=0**, 561 documents              |
| `check-document-metadata.py --mode check-changed --base-ref "$(git merge-base main HEAD)"` | **violations=0**                           |
| `run-ci-gate.py --profile full`                                                            | pending, requires the change to be tracked |

## Review Evidence

Pending independent review. Self-review discarded its own first measurement: a
grep heuristic named three snapshots as missing `generated_by`, and the
manifest's `outputs` field showed all eight already carry it.

## Commit Ledger

| Subject                                                          | Paths     |
| :---------------------------------------------------------------- | :---------- |
| `docs(task): Record that the snapshot merge hypothesis fails` | this Task |

## Rulings

Plan rulings 1 to 8 apply. Two execution rulings were made.

1. **Duplication that a frozen contract holds in place is not removed by
   merging the documents.** Three contracts treat `0069/data.yaml` as immutable
   by digest. Merging would break them, and loosening a digest to permit a
   tidier corpus trades a real guarantee for a cosmetic one.
2. **A script that mentions a path is not its writer.** `scripts/manifest.yaml`
   declares `outputs` for exactly this question, and it is the authority. The
   grep heuristic that replaced it produced three false positives.

## Deferred Items

- The six packages remain duplicated in two formats. The freeze that prevents
  merging them, `TASK7_IMMUTABLE_MANIFEST_SHA256` and the pinned path list in
  `operations_catalog.py`, is SPEC-0157's subject.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
- [Script surface ownership convergence](../../0157-script-surface-ownership-convergence/spec.md)
