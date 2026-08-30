---
profile_id: task
status: completed
artifact_id: task-0154-0004
artifact_type: task
parent_ids: [SPEC-0154, plan-0154]
created: 2026-08-30
updated: 2026-08-30
---

# Retired Taxonomy Removal and Link Repair

## Objective

Remove the Stage 04 model from the six active Specs that state it, delete the parallel redirect table from `docs/README.md`, repair 817 dead links, and apply the lifecycle disposition to 38 Stage 90 audit packs and 28 active Spec Packages. Plan Task 4.

## Inputs

- Task 3 result: `completed` is a valid Spec status.
- Baseline measurement: 817 dead links across 93 files.
- SPEC-0154 section 3 disposition rule and section 4 pattern table.

## Work Log

| Step | Action | Result |
| :--- | :--- | :--- |
| 1 | Captured the dead-link baseline | 817 links across 92 files |
| 2 | Rewrote the Stage 04 passages in four Specs | 0093, 0094, 0105, 0134; 0093's line recording the removal is correct and stays |
| 3 | Replaced the `docs/README.md` Migration Map with a pointer to Stage 98 | 11 rows removed |
| 4 | Repaired 5 dead links outside Stage 90 | 2 off-by-one depths, 3 hook-policy example links |
| 5 | Measured the disposition inputs per pack | status, `superseded_by`, current citers, script and gate consumers, dead-link count |
| 6 | Retired 15 audit packs; kept 17 active | Rule: active if cited or consumed by a script or gate, else retired |
| 7 | Transitioned SPEC-0131 and SPEC-0103 | superseded and retired respectively |
| 8 | Repaired 362 links by identity resolution | Includes a systematic off-by-one depth from the flat-to-directory move |
| 9 | Repaired 34 `spec-####` and three-digit spec paths | Resolver had classed them ambiguous |
| 10 | Delinked 37 references whose targets are gone | Label kept, `(retired path: ...)` appended |

**Deviation 1, the successor direction was the reverse of the numbering.**
`0033` to `0038` are the *old* packs, each declaring `superseded_by` pointing at
`0019`, `0020`, `0021`, `0026`, `0028`, or `0030`. No active pack had a
successor to name, so the approved rule's `retired` branch applied throughout
and no supersession was invented.

**Deviation 2, the disposition rule needed a guard.** A citation-only rule
retired seven generated snapshots including
`data/0072-provider-hook-parity-matrix`, whose freshness a registered gate
checks. The rule was extended: a pack that a script or gate consumes stays
active regardless of citations.

**Deviation 3, `research/` and `data/` were excluded from retirement.** The
finding is about `audit` packs, whose `point-in-time` lifecycle makes a past
observation meaningful. `research/0081-roadmap` and `data/0062-stable-reference-terms`
were both authored 2026-08-23 and are `living` profiles; retiring a week-old
document for lack of inbound links would have been wrong.

**Deviation 4, SPEC-0103 retired rather than superseded.** The approved answer
was `superseded` for both 0103 and 0131. 0131 has evidence: SPEC-0136 declares
`SPEC-0131` as a parent and is 0131's own Wave E. 0103 has no absorber named in
any document, and the approved rule requires `superseded` to name one, so it
retires instead. Recorded here rather than resolved by inventing a successor.

**Rollback.** Each step is its own commit; `git revert` of any one restores that
step. No document body was deleted, only relinked or delinked.

**Skipped checks.** `run-ci-gate.py --profile full` runs at the plan's final
Verification.

## Verification Evidence

| Measure | Before | After |
| :--- | ---: | ---: |
| Dead links, all statuses | 817 | **379** |
| Dead links in `active` documents | ~750 | **158** |
| Dead links in `active` documents outside the research packs | ~176 | **0** |
| Stage 90 audit packs `active` | 32 | 17 |
| Stage 90 audit packs `retired` | 0 | 15 |
| Spec Packages `active` | 28 | 26 |

| Command | Result |
| :--- | :--- |
| `check-document-links.py --mode all` | exit 0, `failures=0` |
| `check-document-metadata.py` | exit 0, 596 tracked, 11 findings |
| `check-agent-governance-contract.py --mode repository --section all` | exit 0 |

All 158 remaining `active` dead links are inside
`docs/90.references/research/0001-*` and `0002-*`, the agentic research packs
whose disposition SPEC-0137 owns and SPEC-0155 decides. None is outside them.

## Review Evidence

Pending independent review. The implementer self-check corrected two of its own
errors before they landed: a misread supersession direction, and a disposition
rule that would have retired gated generated snapshots.

## Commit Ledger

| Subject | Paths |
| :--- | :--- |
| `docs(specs): Replace the retired Stage 04 model with the co-located package` | `docs/03.specs/009{3,4}-*`, `0105-*`, `0134-*`, `docs/README.md`, `docs/00.agent-governance/skills/`, `policies/hooks/` |
| `docs(lifecycle): Retire the audits that observed a repository that no longer exists` | `docs/90.references/audits/`, `research/`, `docs/03.specs/010{3}-*`, `0131-*` |
| `docs(references): Resolve or delink the paths that no longer exist` | `docs/90.references/`, `docs/03.specs/0136-*/tasks/` |

## Rulings

Plan rulings 1 to 5 apply. Four execution rulings were made.

1. **Disposition is measured, not judged.** A pack stays `active` if a current
   non-Stage-90 document cites it or a script, gate, or workflow consumes it.
   Otherwise it retires. Session logs were excluded from the citation count
   after an initial pass wrongly counted this session's own command output.
2. **Links resolve by identity, not by pattern substitution.** Each dead target
   is matched to the file that now carries its identifier, and the relative path
   is recomputed. This caught a systematic off-by-one depth that pattern rules
   would have missed.
3. **A target that is gone is delinked, not repointed.** The label survives and
   the retired path is stated inline, so the record keeps what was referenced
   without asserting a live route.
4. **Stage 98 navigation was corrected; Stage 98 history was not.** The Task
   stated that Stage 98 does not change. Two `Related Documents` routes in
   `migrations/0001` and `0002` were repointed from
   `03.specs/spec-0136-.../spec.md` to `03.specs/0136-.../spec.md`. That is the
   same document at its current path, and the migration ledgers' `records:`
   blocks are untouched. Recorded because the statement and the diff differ.
5. **The research packs are out of scope.** `research/0001-*` and `0002-*` are
   the subject of SPEC-0137's undecided deletion, which SPEC-0155 owns. Editing
   their links here would prejudge that disposition.

## Deferred Items

- 158 dead links in `docs/90.references/research/0001-*` and `0002-*`, pending
  the SPEC-0137 disposition owned by SPEC-0155.
- `SPEC-0136` declares `superseded_by: SPEC-0153`, and no SPEC-0153 exists. The
  slug matches `docs/98.archive/migrations/0003-workspace-governance-simplification.md`,
  so the work appears to have landed as `mig-0003`, but no document states that.
  This is the same phantom identity that
  `tests/validation/test_agent_governance_contract.py` pins. Routed to
  SPEC-0155 with the metadata validator, which does not check that a
  `superseded_by` target exists.
- 164 dead links inside `retired` documents and 54 inside `superseded` ones are
  left as observations of the state those documents recorded. Task 5 exempts
  `superseded` from the link gate; whether `retired` needs the same exemption is
  decided there.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
