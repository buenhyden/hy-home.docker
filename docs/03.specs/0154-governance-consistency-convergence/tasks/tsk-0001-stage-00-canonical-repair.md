---
profile_id: task
status: completed
artifact_id: task-0154-0001
artifact_type: task
parent_ids: [SPEC-0154, plan-0154]
created: 2026-08-30
updated: 2026-08-30
---

# Stage 00 Canonical Repair

## Objective

Move every normative statement out of the eight `roles/` layer documents into the policy that owns it, delete the unverified claims and the two contradiction sources, and remove the eight files. Plan Task 1.

## Inputs

- SPEC-0154 section 1 triage table.
- `docs/00.agent-governance/roles/{agentic,architecture,common,docs,infra,ops,qa,security}.md`.
- Destinations: `policies/quality-standards.md`, `policies/environment-constraints.md`, `policies/approval-boundaries.md`, `policies/standards.md`.

## Work Log

| Step | Action | Result |
| :--- | :--- | :--- |
| 1 | Baseline `check-agent-governance-contract.py --mode repository --section all` | `PASS failures=0`, exit 0. `roles/` held 22 files, 1,355 lines |
| 2 | Moved the QA content into `policies/quality-standards.md` | New sections 4 to 7: Execution Boundary, Change-Type Verification Matrix, Generated-Artifact Freshness, Local QA/CI Orchestration. 65 to 158 lines |
| 3 | Moved the infrastructure content into `policies/environment-constraints.md` | New section 2 with 2.1 Approved Runtime Mutation Protocol and 2.2 Approved Secrets Work Protocol. 70 to 118 lines |
| 4 | Moved the security and ops content | `security.md` section 2 into `quality-standards.md` section 2; SEV1/SEV2 postmortem rule into section 3 |
| 5 | Moved the documentation permission rule | `policies/approval-boundaries.md` gained a Documentation Write Permission block |
| 6 | Deleted five unverified claims instead of moving them | See Rulings below |
| 7 | Dropped `PRD, SRS, Interface Requirement` and the root-shim restatements | `policies/standards.md` section 3 now names registry profiles; `bootstrap.md:40` keeps the single shim statement |
| 8 | `git rm` on the eight layer documents | `roles/` holds 14 agent roles |
| 9 | Repointed references | 27 canonical files (14 agent roles, 13 skills), 3 script or snapshot references, 2 hand-authored references, 2 Stage 03 links |
| 10 | Verified | See Verification Evidence |
| 11 | Committed | See Commit Ledger |

**Deviation from the plan.** Step 9 was written as a single grep-and-repoint
step. The actual blast radius was 81 generated files across three projections
plus 27 canonical sources, because every agent role and 13 of 21 skills carried
a `scope` link into a layer document. The generated files were regenerated, not
edited.

**Second deviation.** The plan assumed Stage 03 link repair belonged to Task 4.
It does not: `docs/03.specs` is inside the current `DOC_ROOTS` of the link gate,
so deleting the layer documents turned the gate red immediately with two
`missing-link-target` failures in SPEC-0134. Both were repointed inside this
Task so that it ends green.

**Third deviation.** The plan's step for regeneration called
`sync-provider-surfaces.sh` with no argument. Its default is `--check`, which
reports drift and exits 1 without writing. Regeneration requires `--write`.

**Rollback.** `git revert` of the Task 1 commit restores the eight files and
every reference intact; no content was rewritten during the move.

**Skipped checks.** `run-ci-gate.py --profile full` was not run at this Task
boundary; it runs at the plan's final Verification after Task 5. Compose,
hardening, and runtime checks are N/A for a documentation-only change.

## Verification Evidence

| Command | Before | After |
| :--- | :--- | :--- |
| `python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all` | exit 0, `failures=0` | exit 0, `failures=0` |
| `python3 scripts/validation/check-document-metadata.py` | exit 0, 595 tracked, 13 findings | exit 0, 596 tracked, 13 findings |
| `python3 scripts/validation/check-document-links.py --mode all` | `failures=0`, documents 351 | `failures=2` after the delete, `failures=0` after the SPEC-0134 repoint, documents 350 |
| `bash scripts/operations/sync-provider-surfaces.sh --check` | exit 0 | exit 1 with 68 drift lines, then exit 0 after `--write` reported `providers=2 drift=0` |
| `grep -rn "File Ownership SSOT\|Subagent Bridge\|@import" docs/00.agent-governance` | 8 files matched | no match |

**Content-arrival check.** Each moved heading was grepped in its destination
after the delete: the verification matrix, freshness rule, QA/CI orchestration,
and `run-ci-precommit.sh` contract in `quality-standards.md`; both approved
protocols, `no-new-privileges`, and the `docker system prune` consent rule in
`environment-constraints.md`; the postmortem rule in `quality-standards.md`; the
`doc-writer` permission in `approval-boundaries.md`. All present.

**Absence check.** The five deleted claims were grepped across
`policies/`: none leaked into a policy.

## Review Evidence

Pending independent review. The implementer self-check found and fixed one
material defect during execution: deleting the layer documents broke two
Stage 03 links and left the registered link gate red. That is recorded as a
plan-ordering defect rather than a content defect.

## Commit Ledger

| Subject | Paths |
| :--- | :--- |
| `docs(governance): Move layer-document rules into the policies that own them` | `docs/00.agent-governance/`, `docs/03.specs/0134-*/`, `docs/90.references/data/00{64,76,82}-*/`, `.agents/`, `.claude/`, `.codex/`, `scripts/manifest.yaml`, `scripts/validation/agent_output_eval.py`, `README.md`, `docs/05.operations/catalog/00-workspace/0007-*/runbook.md` |

## Rulings

Plan rulings 1 to 4 apply. Three execution rulings were made.

1. **Five claims were deleted, not moved.** Each asserts an operational fact
   that no registered check or runbook supports: verified daily off-site backups
   for `04-data` volumes, periodic disaster-recovery drills, quarterly
   architectural reviews, a gateway `LATENCY_SLO < 200ms`, and automated backup
   tags on all persistent data volumes.
2. **Already-present rules were not duplicated.** `quality-standards.md`
   section 3 already carried the 90% coverage floor and its N/A applicability
   rule, in the same words as `roles/qa.md` section 2. The duplicate was
   dropped rather than appended, which is the outcome the Spec asks for.
3. **`scope` links resolve to the policy that now owns the scope.** The mapping
   is `common`, `qa`, `ops`, `security` to `quality-standards.md`; `infra` to
   `environment-constraints.md`; `agentic` to `policies/agentic.md`; `docs` to
   `documentation-protocol.md`; `architecture` to `stage-authoring-matrix.md`.
   The `AOE-ROLE-001` fixture authority moved to `approval-boundaries.md`,
   which now owns the write-permission rule.

## Deferred Items

- `scripts/validation/check-document-links.py` `SUPPORT_DOCS` still names the
  deleted `roles/qa.md`. The lookup is guarded by `is_file()` so nothing breaks;
  Task 5 replaces the whole tuple.
- Eight Stage 03 and Stage 98 documents still name the deleted paths in prose,
  code spans, or table cells rather than links. These are records of what
  existed at the time. Task 4 rules on the Stage 03 ones; Stage 98 does not
  change.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
