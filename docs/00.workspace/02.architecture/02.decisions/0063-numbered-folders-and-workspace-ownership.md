---
title: "Numbered Classification Folders and Workspace Ownership"
version: "0.3.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-11-20"
layer: "architecture"
artifact_id: "ADR-0063"
parent_ids:
- "AD-0030"
created: "2026-11-19"
---

# ADR-0063: Numbered Classification Folders and Workspace Ownership

## Context

### Problem and Drivers

Classification folders under `docs/` had bare names (`descriptions/`,
`guides/`, `tasks/`, `01-common/`) beside numbered Stage folders, and
workspace-wide structure decisions sat with product architecture under
Stage 02. People and agents shared one vocabulary that lived under `.agents/`.

- A reader orders and finds folders the same way at every level.
- Workspace structure and product structure have different owners.
- Shared terms have one owner that people and agents both read.
- Issued identities, versions and history never change because of a move.

#### Sources

No runtime state is claimed.

- [AD-0030 Document lifecycle governance](../01.descriptions/0030-document-lifecycle-governance.md)
- [ADR-0057 Operations documents in role and domain folders](0057-operations-role-and-domain-folders.md)
- SPEC-0212 TSK-0088 (move plan and rehearsal) and TSK-0096 (cutover)

### Decision Scope

Classification folders under `docs/`, the placement of workspace-scope
architecture documents and the shared vocabulary. Native provider paths,
`infra/`, document identities and allocators are outside it.

## Options

### Considered Options

- Keep bare classification names: rejected; folder order and level stay implicit.
- Number every classification folder `NN.name`, keep identities: selected.
- Number folders and reset identity allocators in the same change: rejected;
  a folder move is not a reason to renumber documents.
- Give workspace ADs and ADRs their own profiles and template: rejected; the
  Registry binds one template source to one role and one profile, so a second
  profile needs a copied form.

### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Keep bare classification names | No moves | Order and level stay implicit | Rejected; folders are not found the same way at every level. |
| Number every classification folder, keep identities | One ordering rule, identities stable | Every consumer and link converts at once; history reads through a route map | Selected; issued identities never change because of a move. |
| Number folders and reset allocators together | One cutover | Every identity and reference changes for no reader benefit | Rejected; a move is not an identity change. |
| Separate workspace AD and ADR profiles | `layer` could name the workspace | A copied template form and a second owner of one form | Rejected; the existing profile owns both routes instead. |

- Negative: historical snapshots and immutable Task rows keep unnumbered
  routes, so readers translate them through one route map.
- Negative: a workspace AD or ADR carries `layer: architecture`, the layer of
  its document role, while its folder states its workspace scope.

## Decision

### Chosen Option

1. Classification folders are numbered `NN.name`: Stage 02 `01.descriptions`
   and `02.decisions`; a Spec Package's `01.tasks` and `02.contracts`; Stage
   05 `01.guides`, `02.policies`, `03.runbooks`, `04.incidents` with domain
   folders `01.common` to `15.labs`; Stage 90 `01.research`, `02.audits`,
   `03.data`; Stage 99 `01.contracts` and `02.templates` with numbered form
   folders. Document, request and incident identities and year partitions
   keep their names.
2. `docs/00.workspace/` holds six classes: `01.project`, `02.architecture`,
   `03.process`, `04.quality`, `05.environment` and `06.maintenance`, each
   created only when it has content.
3. Workspace-scope ADs and ADRs (AD-0027, AD-0030 and the ADRs that refine
   them) live under `docs/00.workspace/02.architecture/` with their issued
   identities; the existing AD and ADR profiles own both routes, and product
   and workspace share one identity namespace.
4. Original 2026-11-19 placement, replaced below on 2026-11-20: the shared vocabulary lives at `docs/00.workspace/01.project/glossary.md`;
   agent- and provider-only terms live in `.agents/knowledge/agent-glossary.md`.
5. Approval boundaries are a quality owner at
   `docs/00.workspace/04.quality/approval-boundaries.md`.
6. A pre-numbering route in a snapshot or an immutable Task row resolves
   through `scripts/lib/document_governance/numbered_folders.py`; a current
   document uses only the numbered route.

### Authority and Effect

Decided by the owner, @buenhyden, who accepted it in this chat on 2026-11-19
after PR #1124 merged; status `accepted`, effective from 2026-11-19. Executed
by SPEC-0212 TSK-0096 and TSK-0097.

#### Supersession

The direct P03-OWNERSHIP 1.1.0 requirement of 2026-11-20 explicitly
replaces only Chosen Option 4: common Repository Vocabulary, including
agent/provider meanings, belongs at
[`.agents/knowledge/glossary.md`](../../../../.agents/knowledge/glossary.md);
[the docs00 glossary](../../01.project/glossary.md) owns narrower local
bindings. The separate agent glossary is retired after its meanings migrate,
without a redirect. This scoped owner-directed amendment preserves the
original accepted choice above as history, all numbering and architecture
placements, and the pending environment/maintenance follow-up below.
SPEC-0212 criterion157/W173 and TSK-0101 own implementation and evidence;
this amendment records the decision, not implementation or acceptance.

ADR-0057's role-and-domain layout carries forward; only its folder names
`<role>/<NN-domain>/` become `<NN.role>/<NN.domain>/`.

## Consequences

### Impacts

- Positive: every folder level sorts and reads the same way.
- Positive: workspace structure, shared vocabulary and approval boundaries
  each have one canonical owner; the current vocabulary placement follows the scoped amendment above.

### Follow-up

TSK-0097 moved the workspace sections of RUN-0021 to
`docs/00.workspace/06.maintenance/harness-maintenance.md` and added
`05.environment/onboarding.md`; RUN-0021 stays the registered runtime
authority of those scripts until the maintenance guide is active. The harness
subject 0004 stays in Stage 05.

#### Compliance

`check-document-links.py --mode all`, `check-document-corpus-lifecycle.py`,
`check-document-metadata.py`, `check-operations-catalog.py` and
`tests/lib/document_governance/test_numbered_folders.py`.
