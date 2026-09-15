---
title: "Archive Disposition Enforcement Execution"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0177-TSK-0001"
parent_ids:
- "SPEC-0177"
- "SPEC-0177-PLAN-0001"
created: "2026-09-15"
---

# Archive Disposition Enforcement Execution

## Objective

Record the execution of SPEC-0177: the change that applied the Stage 98
disposition model to governance, and each later integration that moves a
registered check onto it.

## Inputs

- Operator request of 2026-09-15 supplying the Stage 98 disposition text and the
  archive link rule, with three decisions taken the same day. `ADR-0038` and
  `Spec 0079` in the supplied text are mapped to the next issued identifiers,
  `ADR-0035` and `SPEC-0177`, because neither identifier exists here. The model is
  applied in stages: governance text now, validators under this package. Sealed
  Tombstones and Migrations keep their recorded form, and only records created
  after acceptance take the new contract.
- Authorization: local edits, commits, integration into `main`, push, and branch
  and worktree cleanup.
- Position is read from Git: `git rev-parse --abbrev-ref HEAD`,
  `git rev-parse HEAD`, and `git log --oneline origin/main..HEAD`.

## Work Log

### W1: The model applied to governance, and the checks that lag it (2026-09-15, local-executed)

The operator supplied the Stage 98 model as text and asked for it to be applied
to the archive's governance, structure, policy and rules. Three facts about the
text were measured before any edit, and each was put to the operator as a
decision rather than resolved by guess.

The text names `ADR-0038` and `Spec 0079`. Neither exists here: the Registry's
`adr` identity space stood at high water 34 and `spec` at 176, and no commit on
any ref mentions `ADR-0038` or `Retention Envelope`. The operator chose the next
issued identifiers, so `ADR-0035` holds the decision and this package holds the
validator move.

The text also contradicts four executable contracts. The operator chose to apply
it in stages: the policy, the Stage 98 README, `REQ-0026`, `AD-0030` and the
knowledge members state the model now, with a transition paragraph naming each
check that lags, and this package moves the checks. The third decision keeps
every sealed Tombstone and Migration in the form it was written in.

| Contract | Where it is enforced | Model |
| --- | --- | --- |
| Links from outside Stage 98 | `links.py` `_CITABLE_ARCHIVE_PREFIX` admits only `completed/` and the index | Also `resolved/` |
| Tombstone sections | `archive.py` requires `Recovery Commit`; the template carries it | No recovery commit |
| Tombstone pairing | `archive.py` reports a `retired/` body with no Tombstone | No pairing |
| Migration sections | Registry requires `Path Mapping` and `Recovery` | Moved scope and current owner |

The Stage 98 README contradicted itself before this change. Its boundary section
admitted only `completed/`, and a later paragraph said an active document may
link `superseded/` bodies directly. The validator enforced the first. The
rewrite removes the second.

The consumers the link rule's transition clause enumerates were measured over
every tracked Markdown file and `llms.txt` with `build_document_graph`. Outside
Stage 98 there were 94 links into the archive: 90 into `completed/` from 32
documents and 4 to the index from 3 documents. None pointed into `superseded/`,
`retired/`, `tombstones/` or `migrations/`. The new boundary therefore breaks no
current link, and the enumerated consumers are the 32 documents that cite
`completed/`, all of which the model admits.

Writing the change exposed one guard worth recording. A bare child identifier
such as `FR-0013` in a Requirement or an active Spec is rejected by
`_BARE_CHILD_ID`, so every requirement reference here uses its full
`REQ-0026-FR-####` form.

Allocating `ADR-0035` also required one line outside the documents: the
`ADR_TO_AD` table in `tests/lib/document_governance/test_taxonomy.py` lists every
decision identity with its parent Description, and the test failed with
`ADR-0035` missing until the row naming `AD-0030` was added. The Registry's
`adr` and `spec` identity spaces moved to 35 and 177, and `REQ-0026.FR` to 15
for the three new functional requirements.

## Verification Evidence

No acceptance criterion is claimed. The package is `draft`, and every criterion
is owned by a later work unit.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W3 | NOT_RUN: the link boundary has not moved | N/A: pending W3 |

## Review Evidence

None yet.

## Commit Ledger

| Commit | Scope |
| --- | --- |

## Rulings

- No sealed Tombstone, Migration, or frozen body is edited.
- Unexecuted checks are recorded as NOT_RUN or BLOCKED and never promoted to PASS.

## Deferred Items

| Item | Blocking input or reason |
| --- | --- |
| W2 to W8 | The Spec's Open Questions, then one integration per lifecycle step |
