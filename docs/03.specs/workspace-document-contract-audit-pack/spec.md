---
status: active
---

<!-- Target: docs/03.specs/workspace-document-contract-audit-pack/spec.md -->

# Workspace Document Contract Audit Pack Specification

## Overview

This specification defines the contract-first audit pack for repository-wide
documentation, template, governance, CI/CD, QA, and automation surfaces. The
goal is to prepare safe normalization work without immediately rewriting the
whole corpus.

The audit pack treats the repository as a set of typed document profiles. It
first inventories evidence, then compares each profile against the canonical
template and governance contract, then records gaps for later implementation
batches. This prevents historical evidence from being rewritten as if it were
active policy.

## Status Boundary

This spec intentionally remains `status: active` as the current
document-contract audit and disposition model. The paired Stage 04 plan and
task are completed execution evidence for the 2026-07-03 audit pack; that
closure does not retire this spec because future document-contract batches still
use its profile model, gap disposition rules, protected-surface boundaries, and
Stage 90 audit-output routing.

Move this spec to `status: completed` only when a newer active document-contract
spec supersedes it, all active gap-register references are retargeted, or a
future task explicitly retires this audit model with replacement evidence.

## Strategic Boundaries & Non-goals

This spec owns the design of the audit pack only. It does not directly
normalize every document in the repository.

In scope:

- Root shims: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`.
- Optional root design surface: `DESIGN.md` if it exists in a future run.
- Provider and runtime surfaces: `.agents/`, `.claude/`, `.codex/`.
- CI/CD and repository automation: `.github/`, `scripts/`.
- Official documentation stages: `docs/00` through `docs/05`, `docs/90`,
  `docs/98`, and `docs/99`.
- Supporting repository areas with README or Markdown contracts: `archive/`,
  `examples/`, `infra/`, `projects/`, `secrets/`, and `tests/`.
- Contract and governance analysis for document type, frontmatter, sections,
  README profiles, QA, CI/CD, and automation coverage.

Out of scope for this spec:

- Reading secret values, credentials, tokens, certificates, or private keys.
- Changing Docker Compose runtime behavior.
- Fixing existing infra image/version drift.
- Bulk rewriting historical execution evidence.
- Deleting uncertain legacy documents without a later approved implementation
  plan and task evidence.

## Related Inputs

- **Template Contract**: [../../99.templates/support/template-contract.md](../../99.templates/support/template-contract.md)
- **Frontmatter Contract**: [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Template Governance**: [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
- **Template Selection**: [../../99.templates/support/template-selection.md](../../99.templates/support/template-selection.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Task Checklists**: [../../00.agent-governance/rules/task-checklists.md](../../00.agent-governance/rules/task-checklists.md)
- **CI Quality Workflow**: [../../../.github/workflows/ci-quality.yml](../../../.github/workflows/ci-quality.yml)
- **Repository Contracts**: [../../../scripts/validation/check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh)

This design is a governance/specification follow-up and has no dedicated PRD or
ARD. Its parent evidence is the approved user request in the active Codex
thread and the existing Stage 99 contract-standardization work.

## External Basis

The audit pack uses external sources only as principles that are adapted into
repo-local contracts:

| Source | Repo-local use |
| --- | --- |
| [Diataxis documentation framework](https://diataxis.fr/) | Separate how-to, reference, explanation, and tutorial-like purposes so guides, references, policies, and runbooks do not collapse into one document type. |
| [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) and [workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions) | Check least-privilege `permissions`, branch/PR trigger scope, pinned actions, and credential persistence in `.github/workflows/**`. |
| [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/) | Keep incident/postmortem records factual, blameless, timeline-based, and action-item oriented. |
| [ISTQB CTFL overview](https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/) | Treat QA as work-product evaluation, defect discovery, coverage evidence, and verification planning, not only test execution. |
| [Microsoft Security Development Lifecycle](https://www.microsoft.com/en-us/securityengineering/sdl) | Map security activities to requirements, design, implementation, verification, and release stages. |
| [OpenSSF Scorecard](https://scorecard.dev/) | Treat automated supply-chain/security checks as advisory quality signals that can become CI or local QA gates when adopted. |

## Contracts

- **Config Contract**: The audit pack must not change runtime configuration.
  It may inspect tracked file paths, frontmatter, Markdown sections, workflow
  YAML, script references, and validator output.
- **Data / Interface Contract**: Audit outputs use path-stable records with
  document role, profile, frontmatter keys, required sections, forbidden
  sections, contract source, automation coverage, and disposition.
- **Governance Contract**: Active policy belongs in `docs/00.agent-governance/`
  and `docs/99.templates/support/`. README files remain routing and index
  surfaces. Historical evidence is preserved unless a later plan proves it is
  active guidance drift.

## Core Design

### Component Boundary

The audit pack has four workstreams:

1. **Contract and governance inventory**: compare Stage 00 rules, Stage 99
   support docs, root shims, provider docs, and runtime guidance.
2. **Document type inventory**: classify README, PRD, ARD, ADR, Spec, Plan,
   Task, Guide, Policy, Runbook, Incident, Postmortem, Reference, Archive,
   provider docs, agent docs, skill docs, script docs, and CI docs.
3. **Application surface inventory**: classify the requested target surfaces by
   edit risk, protected-surface status, and whether content is active policy,
   active target documentation, generated reference, or historical evidence.
4. **Automation coverage inventory**: map what repository validators and CI jobs
   already enforce, what they only report, and what is currently unguarded.

### Key Dependencies

- `docs/99.templates/support/frontmatter-contract.md`
- `docs/99.templates/support/template-selection.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `scripts/validation/check-repo-contracts.sh`
- `scripts/validation/check-doc-traceability.sh`
- `scripts/validation/check-doc-implementation-alignment.sh`
- `scripts/operations/sync-provider-surfaces.sh`
- `scripts/knowledge/generate-llm-wiki-index.sh`

### Tech Stack

- Markdown and YAML frontmatter for document metadata.
- Bash and Python fragments inside existing validation scripts.
- Git tracked-file inventory using `git ls-files` and `rg`.
- GitHub Actions YAML for CI/CD surface inspection.

## Data Modeling & Storage Strategy

The implementation plan should create a Stage 04 task record before broad
auditing starts. Detailed audit outputs should live under
`docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/` unless the plan chooses a more
specific Stage 90 path.

Recommended records:

| Record | Purpose |
| --- | --- |
| `frontmatter-inventory.md` | Counts and examples of keys by document profile. |
| `section-profile-inventory.md` | Required, optional, duplicate, and forbidden sections by document type. |
| `readme-profile-inventory.md` | Root, docs, governance, infra folder, infra service, scripts, secrets, projects, tests, and examples README profile comparison. |
| `template-application-gaps.md` | Files that appear to retain template instructions, stale template paths, or unresolved placeholders. |
| `automation-coverage-map.md` | CI, QA, validation, provider sync, LLM Wiki, hardening, and local QA coverage matrix. |
| `gap-register.md` | Disposition table for direct fixes, batch fixes, historical evidence, and out-of-scope drift. |

## Interfaces & Data Structures

### Audit Record Shape

```text
path: repo-relative path
surface: root | provider | github | docs-stage | infra | project | script | secret-doc | test-doc | archive | example
document_role: README | PRD | ARD | ADR | Spec | Plan | Task | Guide | Policy | Runbook | Incident | Postmortem | Reference | Archive | Agent | Skill | Workflow | Other
profile: path-derived profile name
frontmatter_keys: observed top-frontmatter keys
required_sections: contract-derived expected headings
forbidden_sections: headings or metadata that contradict the profile
contract_source: template/support/rule path used for comparison
automation_coverage: existing validator or CI gate, if any
disposition: direct-fix | batch-fix | historical-evidence | out-of-scope-gap | no-action
evidence: command, file line, or validator output summary
```

### Gap Disposition Rules

- `direct-fix`: active guidance or active contract drift in a small protected
  surface with clear validation.
- `batch-fix`: target corpus normalization that needs staged commits.
- `historical-evidence`: completed plans/tasks/specs that record old truth and
  should not be rewritten for style alone.
- `out-of-scope-gap`: runtime, infra, secret, remote, or uncertain drift that
  must be recorded rather than fixed in the audit cycle.
- `no-action`: valid broad catalog or scope reference, generated artifact, or
  intentional template-time instruction.

## Tool Contract

The implementation plan should prefer existing repo-local tools before adding
new scripts:

- `rg` and `git ls-files` for inventory.
- `bash scripts/validation/check-repo-contracts.sh` for contract coverage.
- `bash scripts/validation/check-doc-traceability.sh` for plan/operations
  traceability.
- `bash scripts/validation/check-doc-implementation-alignment.sh` for active
  docs versus tracked implementation surfaces.
- `bash scripts/operations/sync-provider-surfaces.sh --check` for generated
  provider mirror drift.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` for generated
  index freshness.

New scripts are allowed only if the plan proves that existing validators cannot
express the required check without making `check-repo-contracts.sh` overly
large or noisy.

## Guardrails

- Do not read or print secret values from `secrets/**`; inspect path metadata
  and Markdown docs only.
- Do not bulk-edit historical Stage 04 evidence just to match newer templates.
- Do not collapse support contracts into README files.
- Do not add parallel templates for the same role.
- Do not replace broad catalog references to `docs/99.templates/` when the
  broad reference is semantically correct.
- Do not treat every stale-looking template path as a bug; classify whether it
  is active guidance, historical evidence, or template-time link guidance.
- Do not claim CI coverage for a rule unless a workflow or local validator
  actually enforces it.

## Evaluation

The audit pack is successful when it produces enough evidence for a later
subagent-driven implementation plan to execute bounded tasks without
rediscovering the whole repository.

Expected implementation phases:

1. Baseline inventory and protected-surface evidence.
2. Contract and governance comparison.
3. Document type and README profile comparison.
4. CI/CD and QA automation coverage map.
5. Gap register and implementation batch proposal.

## Edge Cases & Error Handling

- If `DESIGN.md` is absent, record it as absent rather than creating it unless a
  later approved plan defines a root design surface.
- If a generated file fails a human-authored document contract, verify whether
  the generator owns the format before editing the generated output.
- If a file has Markdown fences containing `---`, only top-of-file frontmatter
  counts as metadata.
- If full repository validation fails because of known infra image/version
  drift, record that as an out-of-scope gap unless the approved implementation
  plan includes infra version correction.
- If external guidance conflicts with repo-local governance, prefer repo-local
  governance and record the external guidance as rationale for a proposed
  future change.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Inventory finds thousands of possible gaps.
  **Fallback**: Group by profile and validator coverage before proposing edits.
  **Human Escalation**: Ask for approval to prioritize a batch.
- **Failure Mode**: A stale-looking path appears in completed evidence.
  **Fallback**: Classify as historical-evidence unless active docs consume it as
  current guidance.
  **Human Escalation**: Ask before rewriting historical meaning.
- **Failure Mode**: Protected surface requires runtime, secret, remote GitHub,
  model, or provider behavior changes.
  **Fallback**: Record a gap and define a separate Stage 04 task.
  **Human Escalation**: Require explicit approval for the protected surface.

## Verification

The design/spec commit must pass:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash -n scripts/validation/check-repo-contracts.sh
```

Full repository contract validation should be run and recorded. It may continue
to fail only on known out-of-scope infra drift unless the implementation plan
later includes that drift.

## Success Criteria & Verification Plan

- **VAL-WDC-001**: The spec defines scope, non-goals, protected boundaries, and
  external basis without authorizing broad corpus edits.
- **VAL-WDC-002**: The document type model covers root shims, provider/runtime
  surfaces, GitHub workflows, official docs stages, infra/project/script/secret
  documentation, tests, archive, and examples.
- **VAL-WDC-003**: The frontmatter and section comparison model distinguishes
  template sources, support governance, target-stage docs, generated docs, and
  README profiles.
- **VAL-WDC-004**: The gap disposition model prevents historical evidence and
  active policy from being treated the same way.
- **VAL-WDC-005**: The automation coverage model names current validators and
  CI gates before proposing new checks.
- **VAL-WDC-006**: The next implementation plan can decompose work into logical
  commits for inventory, governance, validator, direct fallout, corpus batches,
  and final evidence.

## Related Documents

- [Spec index](../README.md)
- [Template contract](../../99.templates/support/template-contract.md)
- [Frontmatter contract](../../99.templates/support/frontmatter-contract.md)
- [Template governance](../../99.templates/support/template-governance.md)
- [Template selection](../../99.templates/support/template-selection.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Repository README](../../../README.md)
