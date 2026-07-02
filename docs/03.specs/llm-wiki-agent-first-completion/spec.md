---
status: completed
---
<!-- Target: docs/03.specs/llm-wiki-agent-first-completion/spec.md -->

# LLM Wiki Agent-first Completion Specification

## Overview

This specification strengthens the `hy-home.docker` LLM Wiki from a static reference map into a verifiable repo-local index contract. It preserves the existing agent-first/Harness-first structure while adding the previously missing generator, generated index, `wiki-curator`, operations guide, and validator enforcement.

## Strategic Boundaries & Non-goals

- Preserve thin root shims and local governance authority.
- Add only repo-local LLM Wiki path indexing and ownership controls.
- Do not introduce a public wiki, `llms-full.txt`, external model calls, Graphify publication wiring, GitHub-native instruction layers, or Docker runtime changes.

## Related Inputs

- **PRD**: Explicit user request in this implementation task
- **ARD**: N/A; no architecture topology change
- **Related ADRs**: N/A; this is a governance/runtime documentation contract completion

## Contracts

- **Config Contract**: `scripts/knowledge/generate-llm-wiki-index.sh` supports default write mode and `--check` freshness mode.
- **Data / Interface Contract**: `docs/90.references/llm-wiki/llm-wiki-index.md` is a generated tracked repo-local Markdown path index.
- **Governance Contract**: `wiki-curator` is mirrored across `.claude/agents/` and `docs/00.agent-governance/agents/agents/`, and `check-repo-contracts.sh` enforces parity and freshness.

## Core Design

- **Component Boundary**: LLM Wiki indexes repository paths only; canonical content remains in source files.
- **Key Dependencies**: Git tracked paths, existing repo contract validator, docs taxonomy, agent catalog parity check.
- **Tech Stack**: Bash wrapper with Python standard library implementation.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Markdown sections group safe paths by repository role.
- **Migration / Transition Plan**: Keep `llms.txt` thin, keep `repository-map.md` curated, add generated `index.md`, and update references to point to both map and index.

## Interfaces & Data Structures

### Core Interfaces

```text
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
```

## Agent Role & IO Contract

- **Agent Role**: `wiki-curator`
- **Inputs**: changed canonical paths and current LLM Wiki references
- **Outputs**: refreshed LLM Wiki index, reference docs, README registrations, and validation evidence
- **Success Definition**: generated index is fresh, safe-boundary checks pass, and runtime/governance catalogs include `wiki-curator`

## Tools & Tool Contract

- **Tool List**: `git ls-files`, `python3`, `bash`
- **Permission Boundary**: local read/write within repository docs and scripts; no network calls
- **Failure Handling**: stale index fails `--check`; unsafe wording/path inclusion fails repo contract validation

## Prompt / Policy Contract

- **System / Instruction Contract**: `wiki-curator` imports `docs/00.agent-governance/scopes/docs.md`.
- **Policy Constraints**: no secret contents, no public wiki, no Graphify authority, no full-content bundle.
- **Versioning Rule**: update generated index and stage evidence whenever the LLM Wiki contract changes.

## Memory & Context Strategy

- **Short-term Context**: use current changed paths and repository contract output.
- **Long-term Memory**: record final progress in `docs/00.agent-governance/memory/progress.md`.
- **Retrieval Boundary**: memory supports context only and cannot override current repo rules.

## Guardrails

- **Input Guardrails**: generator uses safe path filters and excludes known sensitive/generated areas.
- **Output Guardrails**: repo contract scans LLM Wiki files for unsafe links, public-scope drift, and Graphify authority wording.
- **Blocked Conditions**: stale index, missing `wiki-curator`, missing operations guide, or unsafe path inclusion.
- **Escalation Rule**: stop and ask the user before including any path that may expose private values.

## Evaluation

- **Eval Types**: deterministic generation, freshness check, governance parity check, safety wording scan.
- **Metrics**: zero stale index failures, zero unsafe LLM Wiki wording failures, zero agent catalog parity failures.
- **Datasets / Fixtures**: live repository tracked path inventory.
- **How to Run**: use the verification commands below.

## Edge Cases & Error Handling

- **Untracked implementation files during local work**: generator includes known required LLM Wiki contract files when present locally, then relies on `git ls-files` in clean checkouts.
- **Graphify contamination**: keep Graphify advisory and corroborate conclusions against tracked source files.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: generated index includes an unsafe path.
- **Fallback**: tighten generator exclusions and rerun `--check`.
- **Human Escalation**: ask before changing secret-handling boundaries or adding public-facing wiki behavior.

## Verification

```bash
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Generator writes only the repo-local generated index and `--check` catches staleness.
- **VAL-SPC-002**: `wiki-curator` is present in runtime and governance catalogs.
- **VAL-SPC-003**: Repo contract enforces generator, index, guide, role, safety wording, and stale taxonomy checks.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md](../../04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md)
- **Tasks**: [../../04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md](../../04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md)
- **Guide**: [../../05.operations/guides/90-knowledge/llm-wiki-maintenance.md](../../05.operations/guides/90-knowledge/llm-wiki-maintenance.md)
- **Reference**: [../../90.references/llm-wiki/README.md](../../90.references/llm-wiki/README.md)
