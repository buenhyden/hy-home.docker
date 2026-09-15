---
title: "Archive Disposition Enforcement Execution"
version: "0.2.0"
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
  and worktree cleanup. A pull request is the default route to `main` under
  `.agents/governance/github-governance.md`; the operator directed a direct
  push, which GitHub reports as a rule bypass and this Task records as such.
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

The text also contradicts six registered contracts. The operator chose to apply
it in stages: the policy, the Stage 98 README, `REQ-0026`, `AD-0030` and the
knowledge members state the model now, with a transition paragraph naming each
check that lags, and this package moves the checks. The third decision keeps
every sealed Tombstone and Migration in the form it was written in.

| Contract | Where it is enforced | Model |
| --- | --- | --- |
| Links from outside Stage 98 | `links.py` `_CITABLE_ARCHIVE_PREFIX` admits only `completed/` and the index | Also `resolved/` |
| Tombstone sections | `archive.py` requires `Recovery Commit`; the template carries it | No recovery commit |
| Tombstone pairing | `archive.py` reports a `retired/` body with no Tombstone and a Tombstone on a `completed/` or `superseded/` record | No pairing |
| Migration sections | Registry requires `Path Mapping` and `Recovery` | Moved scope and current owner |
| `resolved/` subtree | `load_archive` admits only the registered preservation subtrees, so creating it fails the loader | A retention class created with its first record |
| Retention Envelope | Not defined; a Tombstone carries the withdrawal reason | Names the source Git object once |
| Git-history-only disposition | No profile registered; `REQ-0026`'s Constraint and ADR-0033 Decision 5 keep every preserved body out of Git alone | Allowed where the profile says so |

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
`completed/`, all of which the model admits:

- `docs/01.requirements/0023-standardize-infra-net.md`
- `docs/01.requirements/0024-agent-governance-standardization.md`
- `docs/02.architecture/decisions/0026-standardize-infra-net.md`
- `docs/02.architecture/decisions/0032-canonical-agent-governance-home.md`
- `docs/02.architecture/decisions/0033-full-spec-package-preservation.md`
- `docs/02.architecture/decisions/0034-canonical-knowledge-and-prompt-surfaces.md`
- `docs/02.architecture/descriptions/0026-standardize-infra-net.md`
- `docs/03.specs/0176-stale-fact-convergence/spec.md`
- `docs/03.specs/0176-stale-fact-convergence/tasks/tsk-0001-stale-fact-convergence.md`
- `docs/03.specs/README.md`
- `docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/guide.md`
- `docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/policy.md`
- `docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/runbook.md`
- `docs/05.operations/catalog/00-workspace/0008-new-service-onboarding/guide.md`
- `docs/05.operations/catalog/00-workspace/0009-release-management/runbook.md`
- `docs/05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/README.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0002-agent-model-selection.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0008-harness-engineering.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0010-loop-engineering.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0015-scope-application-matrix.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0017-security-governance.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0019-verification-validation.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0020-workspace-baseline.md`
- `docs/90.references/research/0084-github-actions-platform/README.md`
- `docs/90.references/research/0084-github-actions-platform/m0001-platform-mechanics.md`
- `docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/README.md`
- `docs/90.references/research/0085-workspace-engineering-main-baseline-assessment/m0001-request-scope.md`
- `docs/README.md`

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

### W2: The four Open Questions answered, and the Spec put to review (2026-09-15, local-executed)

The operator asked for SPEC-0177 to be reviewed and taken forward. Reviewing it
showed that nothing past W2 could start in this integration. The Spec is
`draft`, each document admits one transition per integration, and
`_validate_execution_states` in `spec_packages.py` requires an `active` Spec for
an `active` Plan or an `in-progress` Task. Implementation therefore waits for
the Spec to reach `active`, which is two integrations after this one.

The four Open Questions were design choices, so they went to the operator with
a recommendation each, and each recommendation was taken.

| Question | Answer | Reason it was recommended |
| --- | --- | --- |
| Where the Retention Envelope lives | A Retention Catalog table in the Stage 98 README | The operator's text calls it the catalog's envelope and routes frozen records through the index; a README table needs no change to the Stage 98 root allowlist |
| Where a withdrawn body's reason is named | In the same catalog row, as the value its class must name | A frozen body cannot be edited, and one row per record keeps every class obligation in one place a check can read |
| Which profiles are Git-history-only | None in this package | Registering one would amend `REQ-0026` and `ADR-0033` Decision 5 as well, which widens the package for a need nothing has shown |
| How acceptance treats `ADR-0033` | `ADR-0035` supersedes it and restates its full-package unit | Supersession here is whole-document, and one decision should own Stage 98 disposition |

The Spec is amended to the answers and moves from `draft` to `review`. The Plan
and this Task stay `draft`, because the governance rule adds a Plan and Tasks
only for an approved change, and advancing them now would not reach `active`
any sooner. The policy, the Stage 98 README, `AD-0030` and `ADR-0035` now say
that this package moves five of the six lagging contracts and registers no
Git-history-only profile.

## Verification Evidence

No acceptance criterion is claimed. The package is `draft`, and every criterion
is owned by a later work unit.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W3 | NOT_RUN: the link boundary has not moved | N/A: pending W3 |

## Review Evidence

### Independent review of W1 (2026-09-15, local-executed)

One reviewer, not the author, reviewed `fb29286b2` against the operator's text
and the tracked checks. It read the new policy sections, the Stage 98 README,
ADR-0035, REQ-0026, AD-0030 and this package in full, reproduced the link-graph
counts, and read the lagging code in `links.py` and `archive.py`. Disposition
`block`. The SPEC-0176 findings it also raised are recorded in that Task.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | high | `docs/README.md` still allowed citing `superseded/` bodies and described Stage 98 in the old terms | Accepted. Both passages restate the admitted targets and the two kinds |
| 2 | high | `REQ-0026`'s Constraint and ADR-0033 Decision 5 forbid leaving a body in Git alone, against the Git-history-only disposition, and neither transition note named them | Accepted. The policy, REQ-0026 and ADR-0035 name the conflict, and the Spec makes it an Open Question whose answer amends both |
| 3 | high | REQ-0026-FR-0003, FR-0008, FR-0012, NFR-0007 and the namespace acceptance criterion still read as unconditional | Accepted. The REQ-0026 transition constraint names each |
| 5 | medium | The policy said five lagging places, the README, Spec and Task four, and AD-0030 a third set | Accepted. All five surfaces now name the same six |
| 6 | medium | The transition omitted that the loader rejects a `resolved/` subtree and that `archive.py` rejects a Tombstone on `completed/` or `superseded/` | Accepted. Both are in the six, and the Spec and Plan W6 own the loader change |
| 7 | medium | The Tombstone namespace sentence stayed unconditional against create-on-first-use | Accepted. The first Tombstone's change creates the namespace, and the rest is scoped to the transition |
| 8 | medium | The policy said this Task lists the pre-acceptance consumers, and it gave only counts | Accepted. The 32 documents are listed |
| 9 | medium | The Spec added that the Envelope names the withdrawal reason and each class obligation | Accepted. The Envelope names the source Git object only, and where the reason lives is an Open Question |
| 10 | low | The policy's stage list and its citability paragraph were not in the reviewer's summary of the text | Not a defect. Both are the operator's own wording, which the reviewer saw only as a summary |
| 11 | low | The repository map called `resolved/` citable with no qualifier | Accepted. The row names what is admitted today |
| 12 | low | The incident skill said "the one profile" and named two | Accepted |
| 13 | low | Criterion 2's lint half could not be observed inside a package that never creates `resolved/` | Accepted. Criterion 2 now needs a fixture test, and the lint exclusion stays an obligation of the creating change |
| 14 | low | The authorization named direct integration and push while the GitHub governance policy makes a pull request the default | Accepted in part. The operator's direction stands, and the Spec and this Task now record that a direct push is a reported rule bypass, not the policy route |

The changed profile ran on the clean tree at `fb29286b2` before these
corrections: `python3 scripts/validation/run-ci-gate.py --profile changed`
exited `GATE_EXIT=0`, and every FAIL line was an `AOE-CATALOG` negative marker.
The corrections move the path set, so that run is not evidence for the tree they
leave.

## Commit Ledger

| Commit | Scope |
| --- | --- |
| `fb29286b2` | W1 Stage 98 model applied to governance and the package opened |
| `e7ec6e78b` | W1 review corrections naming the six lagging contracts on every surface |

## Rulings

- No sealed Tombstone, Migration, or frozen body is edited.
- Unexecuted checks are recorded as NOT_RUN or BLOCKED and never promoted to PASS.

## Deferred Items

| Item | Blocking input or reason |
| --- | --- |
| W3 to W8 | The Spec is `review`. W3 to W6 start once the Spec is `active` with an `active` Plan and an `in-progress` Task, two integrations after W2 |
