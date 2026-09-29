---
title: "Document Authority and Link Normalization"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0002"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Document Authority and Link Normalization

## Objective

Implement Plan W2 and own R03, R11 and R23 acceptance evidence, with supporting
W7/W9 evidence still required before those criteria can close.

## Inputs

- [Approved Spec](../spec.md), [approved Plan](../plan.md), W1 local predecessors.
- User Plan/execution approval on 2026-09-29 includes this protected canonical
  policy and validator change; no runtime, secret, remote or global access.
- Primary writer: qa-engineer; documentation contributor: doc-writer.
  Independent reviewer: rules-engineer.
- Exact write scope: Plan W2 paths plus this Task. Code/scanner and policy
  describe one invariant; historical/provenance and narrow machine inputs stay.

## Work Log

- Read-only semantic audit identified stale provider-model evaluation path,
  ADR-as-current-authority labels in scripts/root/GitHub documentation, archived
  closure context in evals and shared Git-policy/runbook coupling.
- Current W2 map adds the four exact documentation owners before mutation.
  Manifest/evaluator changes remain W9; Git workflow wording remains W7.
- Implemented normalized own-repository stage links while preserving README and
  directory navigation, literal examples, provenance and docs-internal links.
- Current agent authority now points to canonical governance. The stale evaluation
  route points to root evals. Public CLI and general graph semantics remain.
- Scope: the exact ten Plan W2 files; no installation or remote action.

## Verification Evidence

- RED: Verification L exited 1, 90 tests in 97.706s; seven expected failures
  exposed absolute paths, separator/case variants, GitHub URLs, fenced links
  and previously forbidden README/directory navigation.
- Focused boundary tests witnessed RED then GREEN for slash-containing refs,
  file-like trailing slash, comments/fences, autolinks and file URLs.
- Final Verification L: the Plan registered sanitized run-unittest adapter with
  `tests.lib.document_governance.test_links -v`; exit 0, 90 tests in 85.025s.
- `python3 scripts/validation/check-document-links.py --mode entrypoint`:
  exit 0, 978 documents, 9891 links, 0 failures and 0 warnings.
- `git diff --check`: exit 0. No installed ruff/coverage; no coverage claim.
- R03/R11/R23: W2 implementation and static evidence PASS; overall criteria
  remain open for the separately owned W7/W9 semantic consumer corrections.

## Review Evidence

- Independent pre-implementation semantic inventory completed by rules-engineer.
- Preserve ADR provenance, README navigation, output-path examples, negative
  fixture references and scoped machine inputs. Current authority is distinct.

- Independent rules-engineer final review CLEAR after six boundary findings
  were corrected and rerun; reviewed all ten changed files.
- Preserved machine use: hardening tier 03 reads REQ-0003 solely to assert its
  architecture trace link; Compose reads the named HOME profile section;
  document validators and authoring use registered schema/template inputs.
  These are bounded validation inputs, never current agent instruction owners.

## Commit Ledger

This Task is committed with the reviewed W2 implementation; Git owns the hash.

## Rulings

- Ruling: add four observed current-authority documentation defects to the exact
  W2 map under its approved semantic-audit amendment rule — fulfills existing
  R23 rather than creating new scope; cost if wrong is excess wording change,
  controlled by preserving proven historical references and independent review.
- A path-to-artifact-ID rewrite alone cannot cure current authority dependence;
  move the needed current rule to its canonical owner instead.

## Deferred Items

W7 and W9 own the audit's cross-unit Git/evaluation/manifest transitions. Until
those pass, R11/R23 remain open even if this scanner passes.
