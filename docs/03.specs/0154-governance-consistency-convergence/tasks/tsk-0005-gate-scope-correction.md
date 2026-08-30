---
profile_id: task
status: completed
artifact_id: task-0154-0005
artifact_type: task
parent_ids: [SPEC-0154, plan-0154]
created: 2026-08-30
updated: 2026-08-30
---

# Gate Scope Correction

## Objective

Widen `check-document-links.py` from its four-root selection to the full tracked Markdown corpus, exempting `superseded` documents. Plan Task 5.

## Inputs

- Task 4 result: zero dead links outside `superseded` documents.
- `scripts/validation/check-document-links.py` lines 25 to 40.
- `tests/lib/document_governance/test_links.py`.

## Work Log

| Step | Action | Result |
| :--- | :--- | :--- |
| 0 | Measured what a widened gate would report | 161 dead links would remain after exempting `superseded` and `retired`: 158 in the two research packs, 3 in Stage 98 navigation |
| 1 | Repaired the four Stage 98 navigation routes | Stage 98 dead links 4 to 0 |
| 2 | Wrote three failing selection tests | All three FAIL against the four-root tuple |
| 3 | Replaced `DOC_ROOTS` and `SUPPORT_DOCS` with a tree walk plus two exemptions | Status exemption and one named deferred-pack rule |
| 4 | Ran the tests | 3 OK; the full `test_links` module 39 OK |
| 5 | Ran the gate at the widened scope | documents 342 to 532, links 2,457 to 4,278, `failures=0` |
| 6 | Ran the registered profiles | `changed` exit 0 after commit; `full` exit 1 on the routed identity-scan test |
| 7 | Repaired `docs/README.md` | See the deviation below |

**Deviation, `docs/README.md` was still describing a repository that does not
exist.** The acceptance measurement found the top-level documentation index
still listing `04.execution/plans/` and `tasks/` in its structure block, routing
table, and language table, plus `02.architecture/requirements/` and the three
`05.operations/guides|policies|runbooks/` directories, none of which exist. Two
Current Evidence tables pointed at Stage 04 plan and task files. All were
corrected here rather than deferred, because this is the document a reader opens
first.

**Rollback.** `git revert` of the Task 5 commits restores the previous selection
and the previous README.

**Skipped checks.** None. `--profile full` was run and its single failure is the
one routed to SPEC-0155.

## Verification Evidence

| Measure | Before | After |
| :--- | ---: | ---: |
| Documents the link gate reads | 342 | **532** |
| Links the link gate checks | 2,457 | **4,278** |
| Link gate failures | 0 | **0** |
| Stage 98 dead links | 4 | **0** |

| Command | Result |
| :--- | :--- |
| `python3 -m unittest tests.lib.document_governance.test_links.LinkSelectionScopeTests` | 3 FAIL before, **3 OK** after |
| `python3 -m unittest tests.lib.document_governance.test_links` | **39 OK** |
| `check-document-links.py --mode {all,traceability,alignment}` | exit 0, 0, 0 |
| `check-document-metadata.py` | exit 0, zero `invalid-status` |
| `check-document-corpus-lifecycle.py` | exit 0 |
| `check-agent-governance-contract.py --mode repository --section all` | exit 0 |
| `sync-provider-surfaces.sh --check` + `git diff --exit-code` | exit 0 |
| `run-ci-gate.py --profile changed` | **exit 0** |
| `run-ci-gate.py --profile full` | exit 1, one test, routed to SPEC-0155 |

The gate refused to run before the change was committed:
`FAIL [ci-gate-entrypoint-identity] scripts/validation/check-document-links.py:
the entrypoint identity differs from the tracked object`. A validator edit is
only exercised by the registered gate once it is tracked.

## Review Evidence

Pending independent review. The acceptance measurement served as the
implementer's own check and found two of the Spec's acceptance items to be
wrong proxies rather than unmet obligations, plus one genuine gap in
`docs/README.md`.

## Commit Ledger

| Subject | Paths |
| :--- | :--- |
| `fix(validation): Read the corpus the link gate is supposed to protect` | `scripts/validation/check-document-links.py`, `tests/lib/document_governance/test_links.py`, `docs/98.archive/migrations/` |
| `docs(readme): Describe the repository this is, not the one it was` | `docs/README.md`, `docs/03.specs/0154-*/spec.md`, `tasks/tsk-0005-*.md` |

## Rulings

Plan rulings 1 to 5 apply. Three execution rulings were made.

1. **Exemption by status, not by path.** `superseded` and `retired` documents
   record a past observation, so their links are evidence of what resolved when
   they were written. That is a property of the document, not of where it lives.
2. **One named path exemption, with an owner and a removal condition.** The two
   agentic research packs are excluded because SPEC-0137's deletion is
   undecided and SPEC-0155 owns it. The rule states this in the source and says
   when to delete it. A path exemption without an owner would be a permanent
   blind spot of the kind this Task exists to remove.
3. **Two Spec acceptance items were wrong proxies and were corrected, not
   waived.** Item 6 demanded that `Stage 04` appear in no active document; the
   corpus has 1,068 such mentions across 142 files, nearly all factual records
   inside execution ledgers and observation inventories. The Behavior Contract
   asks that no active document *describe Stage 04 as current procedure*, which
   is what was verified. Item 7 demanded that `PRD, SRS` appear nowhere in Stage
   00; the one remaining occurrence is the prohibition in
   `documentation-protocol.md`, which must keep naming what it forbids.

## Deferred Items

- The two research-pack prefixes in `DEFERRED_PREFIXES`, removable when
  SPEC-0155 records the SPEC-0137 disposition. 158 dead links sit behind it.
- 218 dead links inside `superseded` and `retired` documents are permanently out
  of the gate's scope by rule 1. They are observations, not routes.

## Related Documents

- [Plan](../plan.md)
- [Specification](../spec.md)
