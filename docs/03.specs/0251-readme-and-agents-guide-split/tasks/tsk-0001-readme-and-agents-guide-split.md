---
title: "README and Agent Guide Split Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0251-TSK-0001"
parent_ids:
- "SPEC-0251-PLAN-0001"
created: "2026-11-03"
---

# README and Agent Guide Split Task

## Overview

### Objective

Give people a `README.md` and agents a folder `AGENTS.md`, placed only where
the folder's role needs agent-specific working rules.

## Inputs and Authorization

The user directed that every README targets people and every AGENTS.md targets
AI agents; that this be reflected in governance, structure and rules; that each
AGENTS.md reference the matching `.agents/`, `.claude/` and `.codex/` documents
and fit its folder's purpose; that AGENTS.md not be placed wherever a README
exists, with a defined rule for README with AGENTS.md versus README only; and
that `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`,
`docs/05.operations`, `docs/90.references` and `docs/99.templates` carry one.
The user then chose `infra/`, `scripts/` and `tests/` as the only further
locations and kept `secrets/` README-only. Exclusions: root shims stay as they
are; no push, pull request or merge from this Task.

## Work Log

### Current contract decision

The user's direction authorizes this Spec and Plan as written.

### Current readiness and execution

Inputs, work units and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0251 | draft | approved | #current-contract-decision |
| SPEC-0251-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0251-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0251-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

### Decisions

- Placement: a folder carries AGENTS.md only when an agent needs folder-specific
  working rules no single canonical owner routes: a stage with templates,
  identities and lifecycle, a protected or generated surface, or owned
  registered checks. `secrets/` stays README-only because approval boundaries
  already owns its only agent rule.
- One Registry profile, `folder-agent-guide` (`governance/agent-guide`,
  English, `living`), lists the nine paths; adding a guide means adding its
  path there. New guides start at `draft`, as the metadata check requires, and
  move to `active` in a later change.
- Claude Code does not load nested `AGENTS.md`; a bootstrap step requires
  reading the folder guide, and no folder `CLAUDE.md` pointer is added. Codex
  documents a root-to-working-directory merge of `AGENTS.md`, not observed
  here.
- SPEC-0251 is used because the completed-package deletion branch claims
  SPEC-0250; this branch must land after it, or the 250 gap must be reconciled
  at rebase.

### Changed

- Governance: `documentation-protocol.md` (new "README and AGENTS.md" rule,
  AGENTS.md language rule, navigation note), `bootstrap.md` (load step 4),
  `stage-authoring-matrix.md` (`agent-guide` kind), `.claude/provider.md`,
  `.codex/provider.md`.
- Registry: `folder-agent-guide` profile with its `template_roles`,
  `transitions` and disposition entries; `AI Agent Guidance` removed from the
  `documentation-readme` optional sections and from its template; Spec
  high-water 251.
- Code: `registry.py` owns `scripts/AGENTS.md` and `tests/AGENTS.md` and lets
  the trusted Requirement history read skip `docs/01.requirements/AGENTS.md`;
  `scripts/manifest.yaml` registers `scripts/AGENTS.md`; the
  Stage 01, 02, 03 and 90 loaders and the operations catalog accept a root
  `AGENTS.md`; the navigation check ignores `AGENTS.md` when classifying a
  folder router.
- READMEs: the nine matching READMEs drop `AI Agents` from their audience,
  the Stage 01, Stage 02 decisions and descriptions READMEs lose their
  `AI Agent Guidance` sections, the `infra` README loses its agent step list,
  and each points to its AGENTS.md.

### Open issues

- `.github/CODEOWNERS` and `.github/labeler.yml` name only the root
  `AGENTS.md`; adding folder guides there is a protected-surface change left
  for a separate approval.
- ADR-0002 keeps an `AI Agent Guidance` subsection in its accepted decision
  body; the README rule does not apply to it.
- The folder guides start at `draft` and need a later change to become
  `active`.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | agent-governance-contract | `check-agent-governance-contract.py` after the governance edits | PASS | repository mode, zero failures | required | - |
| E2 | 1 | W1 | renderer-parity | `provider_surface_renderer.py --check` | PASS | providers 2, drift 0 | required | - |
| E3 | 2 | W2 | operations-catalog | `check-operations-catalog.py` after the root-entry change | PASS | zero findings | required | - |
| E4 | 2, 3 | W3 | document-links | `alignment`, `navigation` and `language` modes | PASS | 964 documents, 8495 links, zero failures | required | - |
| E5 | 2, 3 | W3 | document-entrypoint | `entrypoint` mode | FAIL | 8 findings, identical on main d6b535503: three `infra` READMEs link Stage 03 Task bodies; not caused by this change | required | - |
| E6 | 4 | W4 | corpus-lifecycle | `check-document-corpus-lifecycle.py` | PASS | lifecycle and occupancy zero violations | required | - |
| E7 | 4 | W4 | metadata-changed | `check-changed --base-ref origin/main`, revision 20da707ba | PASS | 25 selected, zero violations | required | - |
| E8 | 4 | W4 | metadata-active | `check-active`, revision 20da707ba | PASS | 497 selected, zero violations | required | - |
| E9 | 4 | W4 | script-manifest | `check-script-manifest.py`, revision 20da707ba | FAIL | `scripts/AGENTS.md` had no manifest row | required | - |
| E10 | 4 | W2 | governance-unit-tests | `tests/lib/document_governance` discovery, revision 20da707ba, quiet tree | FAIL | 763 tests: 1 failure and 10 errors, all from the trusted Requirement history read rejecting `docs/01.requirements/AGENTS.md` | required | - |
| E11 | 4 | W4 | script-manifest | after the manifest row, revision c78cf723f | PASS | script manifest is valid | required | E9 |
| E12 | 4 | W2 | governance-unit-tests | the 11 E10 tests after the history-read fix, revision c78cf723f | PASS | 11 tests OK | required | E10 |
| E13 | 4 | W4 | validation-suites | `tests/validation/lifecycle`, CI routing and surface ownership, revision 20da707ba | PASS | all OK; 92 routing and ownership tests | required | - |
| E14 | 1 | W1 | agent-governance-and-renderer | contract check and renderer `--check`, revision 20da707ba | PASS | zero failures; providers 2, drift 0 | required | - |
| E15 | 4 | W2 | governance-unit-tests | `tests/lib/document_governance` discovery, revision 4d4fefc26, quiet tree | PASS | 763 tests OK; metadata check-changed 25 and check-active 497 selected with zero violations; Script Manifest and link alignment PASS | required | E10 |
| E16 | 4 | W4 | hosted-ci | GitHub Actions | NOT_RUN | branch not pushed | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |

## Review and Completion

Local checks are recorded above. No independent review has run, hosted CI has
not run, and no criterion is accepted yet.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
