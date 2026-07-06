---
status: completed
---

<!-- Target: docs/03.specs/107-provider-semantic-parity-validator/spec.md -->

# Provider Semantic Parity Validator Technical Specification

## Overview

This specification defines a narrow validator and generator update that keeps
provider adapters semantically aligned with the Stage 00 canonical agent
catalog. The immediate gap is that provider surfaces can have matching names
and model tiers while Codex or Gemini adapters still point to the wrong role
scope.

## Strategic Boundaries & Non-goals

This spec owns provider adapter role-scope parity only. It does not introduce a
natural-language semantic diff engine, alter runtime provider behavior, or
change model policy. Future work can extend this into broader clause-level
comparison, but this batch enforces the role/policy parity that is already
machine-checkable from Stage 00.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from the completed
  agentic engineering implementation audit candidate `AEA-AUTO-002`.
- **ARD**: No dedicated ARD exists; the architecture boundary is the Stage 00
  Canonical Adapter Model.
- **Related ADRs**: No new ADR is required because this implements the existing
  provider adapter decision.

## Contracts

- **Config Contract**: `scripts/operations/sync-provider-surfaces.sh` must derive
  each agent adapter's role scope from the Stage 00 agent catalog `Scope import`
  literal. If the literal is absent, the script may fall back to the catalog
  frontmatter `layer`, then `agentic`.
- **Data / Interface Contract**: `.codex/agents/<name>.toml` must set `layer`
  and `scope` to the canonical role scope. `.agents/agents/<name>.md` must set
  frontmatter `layer` to the same role scope and remain a short reference index.
- **Governance Contract**: `scripts/validation/check-repo-contracts.sh` must
  reject role-scope drift across Stage 00 catalog entries, Claude adapters,
  Codex adapters, Gemini pointer adapters, and the `subagent-protocol.md` agent
  table.

## Core Design

- **Component Boundary**: Generator logic remains in
  `scripts/operations/sync-provider-surfaces.sh`; enforcement remains in
  `scripts/validation/check-repo-contracts.sh`.
- **Key Dependencies**: Stage 00 agent catalog files, provider adapter folders,
  `docs/00.agent-governance/subagent-protocol.md`.
- **Tech Stack**: Bash for generation, embedded Python for repository contract
  validation.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: The canonical semantic role scope is represented
  as a scope basename such as `infra`, `ops`, `qa`, `docs`, `common`, or
  `agentic`.
- **Migration / Transition Plan**: Regenerate Codex TOML adapters and Gemini
  pointer adapters with the updated generator, then validate the generated
  outputs.

## Interfaces & Data Structures

### Core Interfaces

```text
canonical_scope(agent_catalog_entry) -> scope_basename
codex_adapter.layer == canonical_scope
codex_adapter.scope == docs/00.agent-governance/scopes/<canonical_scope>.md
gemini_pointer.frontmatter.layer == canonical_scope
claude_adapter.frontmatter.layer == canonical_scope
subagent_protocol row contains scopes/<canonical_scope>.md
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Agentic Workflow Specialist / QA Engineer.
- **Inputs**: Stage 00 agent catalog, provider adapter surfaces, subagent
  protocol, and automation candidate audit evidence.
- **Outputs**: Updated generator, generated provider adapters, validator gate,
  and Stage 04 evidence.
- **Success Definition**: provider sync reports no drift, repo contracts pass,
  and Codex/Gemini adapters preserve each agent's canonical role scope.

## Tools & Tool Contract (If Applicable)

- **Tool List**: shell, `rg`, `git`, repository validation scripts.
- **Permission Boundary**: `.agents/**` generated adapter writes require
  approved write access because the sandbox marks `.agents` read-only.
- **Failure Handling**: If generated adapters drift, rerun
  `bash scripts/operations/sync-provider-surfaces.sh --write`; if validation
  fails, inspect the named provider file and canonical Stage 00 catalog entry.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Provider adapters may adapt syntax, but
  must not redefine agent role scope or policy.
- **Policy Constraints**: No model, hook, credential, or remote changes.
- **Versioning Rule**: Validator behavior changes are recorded in Stage 04 task
  evidence and conventional commits.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records the command results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  the completed parity closure.
- **Retrieval Boundary**: Graphify remains advisory and must be corroborated
  against tracked Stage 00 and provider files.

## Guardrails (If Applicable)

- **Input Guardrails**: The validator reads paths and literals only; it does not
  read secret values or local auth files.
- **Output Guardrails**: Report only path, line, and literal drift.
- **Blocked Conditions**: Missing Stage 00 scope import, mismatched generated
  provider scope, or stale provider sync output.
- **Escalation Rule**: Stop before model/config/hook/secret changes.

## Evaluation (If Applicable)

- **Eval Types**: Structural and semantic role-scope validation.
- **Metrics**: zero repo-contract failures; zero provider sync drift.
- **Datasets / Fixtures**: Current Stage 00 agent catalog and provider adapter
  files.
- **How to Run**: use the verification commands in this spec and the linked
  task evidence.

## Edge Cases & Error Handling

- **Catalog entry missing `Scope import`**: fall back to frontmatter `layer`, but
  report future remediation in the task if the fallback hides a real role scope.
- **Pointer adapter remains short but has wrong layer**: repo contracts fail and
  provider sync `--write` regenerates it.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Codex/Gemini adapters drift from the canonical role scope.
- **Fallback**: Regenerate provider surfaces, then rerun provider sync and repo
  contracts.
- **Human Escalation**: Required only if changing Stage 00 catalog semantics,
  model policy, hooks, secrets, or provider runtime configuration.

## Verification

```bash
bash scripts/operations/sync-provider-surfaces.sh --write
bash scripts/operations/sync-provider-surfaces.sh --check
bash -n scripts/operations/sync-provider-surfaces.sh scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Codex TOML adapters use the canonical Stage 00 role scope for
  `layer` and `scope`.
- **VAL-SPC-002**: Gemini pointer adapters use the canonical Stage 00 role scope
  in frontmatter and remain short reference-index pointers.
- **VAL-SPC-003**: Claude, Codex, Gemini, and `subagent-protocol.md` agree on
  each agent's role scope.
- **VAL-SPC-004**: Full repo contracts pass with `failures=0`.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-05-provider-semantic-parity-validator.md](../../04.execution/plans/2026-07-05-provider-semantic-parity-validator.md)
- **Tasks**: [../../04.execution/tasks/2026-07-05-provider-semantic-parity-validator.md](../../04.execution/tasks/2026-07-05-provider-semantic-parity-validator.md)
- **Provider capability matrix**: [../../00.agent-governance/rules/provider-capability-matrix.md](../../00.agent-governance/rules/provider-capability-matrix.md)
- **Provider adapter model**: [../../00.agent-governance/providers/agents-md.md](../../00.agent-governance/providers/agents-md.md)
- **Subagent protocol**: [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
