---
layer: agentic
status: active
---

# Current Project Memory

## Current objective

- Current task: `docs/04.execution/tasks/2026-08-07-agentic-research-pack-extension.md`
- T-ARPE-001 through T-ARPE-011 are complete. The canonical agentic research
  pack gained three leaves covering documentation architecture, the LLM-WIKI
  system, and the agent memory hierarchy, and its fifteen existing leaves were
  revalidated against repository facts and current external sources. This Task
  is the successor Task the previous handoff asked for, so the lifecycle
  boundary that paused
  `task:2026-07-26-agent-governance-canonical-convergence` is released.

## Approved decisions

- The pack is extended in place. No new dated research pack directory is
  created, which preserves the Spec 122 consolidation outcome.
- The superseded `2026-07-07-agentic-research-pack-update/` pack stays in place
  for link continuity and canonical mapping.
- Revalidation covers two axes: repository-local counted facts and current
  official external sources.
- Governance lifecycle for this work is one Stage 04 Task, without a new Spec
  or Plan.
- Fixed historical boundaries stay unchanged by this revalidation: the
  2026-07-10 model cutoff, the 2026-07-26 typed contract timestamps, and every
  claim recorded as unverified.

## Active boundary

- The Task covers three new Stage 90 leaves, fifteen revalidated leaves, both
  README indexes, this record, and the three generated artifacts whose
  freshness contracts the added documents tripped.
- Push, remote mutation, live provider calls beyond read-only public
  documentation retrieval, runtime changes, Compose operations, Stage 00 policy
  changes, and the controlled all-files wrapper stay outside this Task.
- Independent review of this Task has not happened.

## Verified state

- Verified commit: `e90a81af7e9400f29488f9299557f92ab1ec22bc`
- Verified at: `2026-08-07T13:03:07+09:00`
- Coverage analysis before authoring found that nineteen of twenty-two
  requested research topics already had canonical coverage across fifteen
  leaves totalling 3,523 lines, and that three had none.
- Workspace fact re-derivation confirmed twenty-one of twenty-three cited
  figures and found one real drift: local QA runner step counts were
  understated by four in both modes because two helper functions were omitted
  from the original enumeration. Re-derived counts are 24 default and 22
  harness steps, which reconciles with the 25 bullets the list mode prints
  minus one advisory recommender.
- External revalidation corrected the Codex `SessionEnd` claim in five places,
  the Gemini per-agent reasoning claim, the Codex effort range, the Claude and
  Gemini hook event counts, and six stale or redirected source URLs.
- Five external sources could not be re-fetched and are recorded as not
  re-verified rather than removed, since none was disproven.
- The repository contract check exits with ten failures, down from thirteen
  during this Task. Every failing subject is untouched by this work, and no
  `infra/`, `scripts/`, or `.github/` path changed.
- Changed-document metadata validation selected twenty-four documents and
  reports three findings, all the same heading-contract conflict on the three
  new leaves.
- Traceability passes with forty-six catalog pairs and zero failures, and the
  final diff has no whitespace drift.
- Ten logical-unit commits span `19ee4727` to `e90a81af`.

## Blockers and unverified facts

- A new Stage 90 reference cannot satisfy both heading contracts at once. The
  repository contract check looks for the literal `## Definitions / Facts`
  while the reference role in the document metadata profiles looks for the H2
  `## Facts and Definitions`. Each choice fails the other gate with exactly
  three findings. The three new leaves use the sibling-matching heading and
  carry the metadata finding. Both candidate fix sites sit outside this Task's
  allowed paths, so correcting the conflict needs separate approval.
- Ten predecessor repository-check failures stay open: the private environment
  key comparison pair, the missing `html5lib` validation-runtime dependency,
  the Keycloak hardening image tag, the stale tech-stack provenance snapshot,
  and version drift for Traefik, Keycloak, PostgreSQL, Prometheus, Alloy, and
  Ollama. These route to a separate approved runtime task.
- Provider acceptance and entitlement, live comparative model evaluation, and
  authenticated remote GitHub enforcement stay unverified.
- A typed domain-memory taxonomy with validator-enforced promotion, retention,
  archival, and deletion stays outside current scope. The new memory-hierarchy
  leaf records the research basis for it. That leaf also corrects the record
  that the deferral wording originates in the Stage 04 Task ledger rather than
  in Spec 134.

## Evidence links

- [Active Task ledger](../../04.execution/tasks/2026-08-07-agentic-research-pack-extension.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Documentation architecture leaf](../../90.references/research/2026-07-05-agentic-research-pack-refresh/documentation-architecture.md)
- [LLM-WIKI system leaf](../../90.references/research/2026-07-05-agentic-research-pack-refresh/llm-wiki-system.md)
- [Memory hierarchy leaf](../../90.references/research/2026-07-05-agentic-research-pack-refresh/memory-hierarchy.md)
- [Predecessor convergence Task](../../04.execution/tasks/2026-07-26-agent-governance-canonical-convergence.md)

## Next handoff

- Keep the result on the local branch and do not push. Seek separate approval
  for the heading-contract correction, for independent review of this Task, and
  for the runtime and Compose drift task. A future Stage 03 memory-governance
  specification can build on the new memory-hierarchy leaf.
