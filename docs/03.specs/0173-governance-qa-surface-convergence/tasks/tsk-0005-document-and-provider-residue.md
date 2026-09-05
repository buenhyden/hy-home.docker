---
title: "Document and Provider Residue Task"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0005"
parent_ids:
- "SPEC-0173"
- "SPEC-0173-PLAN-0001"
created: "2026-09-05"
---

# Document and Provider Residue Task

## Objective

Remove current paths that reproduce legacy document grammar, retire obsolete
generated snapshots, and reduce provider projections to required native
interfaces backed by one Stage 00 authority.

## Inputs

- [SPEC-0173](../spec.md), its [implementation plan](../plan.md), and the
  ownership boundaries established by Tasks 0001 through 0004.
- Current authored documents, templates, forms, examples, registry and schema,
  LLM Wiki inputs, DATA-0068/0069/0073/0074, and provider renderers.
- `.agents/`, `.claude/`, `.codex/`, hooks, provider projection tests, and
  current consumer searches.

## Work Log

This planning artifact was created on 2026-09-05. No document family, data
package, provider projection, renderer, or hook has been changed. During an
authorized execution, update every current inbound link and generated owner in
the same logical change as its source transition.

## Verification Evidence

No execution evidence exists in this draft. Acceptance requires metadata,
lifecycle, identity, link, projection, generated-freshness, and focused hook
checks with their actual exit codes recorded.

## Review Evidence

No implementation review has occurred. Independent review must confirm that
Stage 90 evidence did not become policy and that generated provider surfaces do
not outrank their Stage 00 sources.

## Commit Ledger

No implementation commit exists. The planning-package changes are not
implementation or acceptance evidence.

## Rulings

- Keep stable frontmatter IDs while removing banned basename prefixes from
  current authored paths.
- Retain `.agents/skills`, `.claude`, and `.codex` native interfaces; retire
  `.agents/agents` only after renderer and consumer cutover is proven.
- Generated snapshots without a current consumer are retired through the
  canonical lifecycle rather than preserved as active authority.
- Create one sealed package Tombstone for each retired DATA artifact and move
  each registered `README.md` byte for byte; recover unregistered payloads from
  the exact Git commit recorded by the Tombstone.

## Deferred Items

- User-global Claude or Codex configuration, credentials, and private state
  remain inaccessible and undocumented.
- Provider entitlement and live provider execution remain unverified.

## Related Documents

- [SPEC-0173 package](../spec.md)
- [SPEC-0173 implementation plan](../plan.md)
- [Test and fixture convergence Task](tsk-0004-test-and-fixture-convergence.md)
