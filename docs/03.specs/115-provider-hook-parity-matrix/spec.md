---
status: active
---

<!-- Target: docs/03.specs/115-provider-hook-parity-matrix/spec.md -->

# Provider Hook Parity Matrix Technical Specification

## Overview

This specification defines a generated Stage 90 provider hook parity matrix for
Claude, Codex, and Gemini. The matrix compares tracked Claude/Codex hook
configuration and records Gemini as a behavioral reminder checklist because the
Stage 00 provider capability matrix treats Gemini hooks as a non-native
capability.

## Strategic Boundaries & Non-goals

This feature is generated reference data only. It does not change provider
configuration, add native Gemini hook claims, execute hook payloads, inspect
personal settings, read hook logs, mutate model policy, change CI, or touch
runtime/remote/secret state.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from the provider hooks
  row in the agentic engineering automation candidates reference.
- **ARD**: No dedicated ARD exists; the implementation stays within the
  existing Stage 00 provider governance and Stage 90 governance-data boundaries.
- **Related ADRs**: No new ADR is required because this is a small generated
  reference-data report.

## Contracts

- **Config Contract**: `scripts/validation/report-provider-hook-parity.sh`
  generates
  `docs/90.references/data/governance/provider-hook-parity-matrix.md`.
- **Data / Interface Contract**: The generator reads tracked
  `.claude/settings.json`, `.codex/hooks.json`, Claude hook wrappers, Gemini
  provider notes, the provider capability matrix, and `.agents/README.md`.
- **Governance Contract**: `scripts/validation/check-repo-contracts.sh` must run
  `report-provider-hook-parity.sh --check` so generated hook parity evidence
  cannot drift.

## Core Design

- **Component Boundary**: A Bash wrapper invokes an embedded Python renderer,
  matching existing generated reference-data patterns.
- **Key Dependencies**: Stage 00 provider governance, tracked provider hook
  configs, Claude wrapper scripts, provider-neutral hook dispatcher.
- **Tech Stack**: Bash and Python 3 standard library.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Each hook event is rendered with Claude status,
  Codex status, Gemini behavioral reminder, matcher, command, timeout, and
  source references.
- **Migration / Transition Plan**: Add the generator, generated data reference,
  freshness gate, script inventory, Stage 03/04 evidence, and automation
  candidate closure.

## Interfaces & Data Structures

### Core Interfaces

```text
bash scripts/validation/report-provider-hook-parity.sh
bash scripts/validation/report-provider-hook-parity.sh --check
bash scripts/validation/report-provider-hook-parity.sh --dry-run
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Agentic Workflow Specialist / QA Engineer.
- **Inputs**: Tracked provider hook configs, Stage 00 provider notes, and
  provider runtime README guidance.
- **Outputs**: Generated provider hook parity matrix under Stage 90 governance
  data.
- **Success Definition**: Audit consumers can inspect Claude/Codex native hook
  parity and Gemini behavioral reminders without opening every source file.

## Tools & Tool Contract (If Applicable)

- **Tool List**: Git, Bash, Python 3, repo-contract validator.
- **Permission Boundary**: Read tracked provider/governance files and write only
  the generated Stage 90 snapshot plus related docs/evidence.
- **Failure Handling**: `--check` fails when generated output is missing or
  stale.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Treat generated output as audit context,
  not active provider policy.
- **Policy Constraints**: Do not read `.claude/settings.local.json`, hook logs,
  shell history, credentials, tokens, `.env` values, or live provider runtime
  state.
- **Versioning Rule**: Generator, generated output, contracts, and evidence are
  committed as one logical unit.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records generation and
  validation results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  closure of the provider hooks follow-up.
- **Retrieval Boundary**: Graphify remains advisory and must be corroborated
  against tracked provider files and Stage docs.

## Guardrails (If Applicable)

- **Input Guardrails**: Parse tracked configs only; never inspect personal
  settings, hook logs, secrets, shell history, or runtime telemetry.
- **Output Guardrails**: Store event names, status labels, commands, timeouts,
  and behavioral reminders only.
- **Blocked Conditions**: Provider config mutation, native Gemini hook claims,
  hook execution, CI publication, remote state changes, credential edits, or
  model policy changes.
- **Escalation Rule**: Any provider runtime change, CI summary publication, or
  Gemini native hook policy change requires a separate approved Stage 03/04
  plan.

## Evaluation (If Applicable)

- **Eval Types**: Generator write/check, shell syntax, repo-contract freshness
  gate, documentation validation.
- **Metrics**: hook events tracked, Claude native wrapper events, Codex native
  dispatch events, Gemini behavioral reminders, missing contract literals.
- **Datasets / Fixtures**: Current tracked provider hook configs and Stage 00
  provider governance files.
- **How to Run**: Use the verification commands below and linked task evidence.

## Edge Cases & Error Handling

- **Claude wrapper indirection**: The generator checks wrapper existence and
  delegation to `scripts/hooks/agent-event-hook.sh`.
- **Gemini non-native hooks**: The generator renders behavioral reminders, not
  native support assertions.
- **Personal provider config**: `.claude/settings.local.json` is explicitly out
  of scope.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Generated matrix becomes stale after provider hook or
  provider governance changes.
- **Fallback**: Regenerate with
  `bash scripts/validation/report-provider-hook-parity.sh`.
- **Human Escalation**: Required before changing provider runtime config,
  adding new hook events, claiming new Gemini native support, or publishing the
  matrix into CI.

## Verification

```bash
bash scripts/validation/report-provider-hook-parity.sh
bash scripts/validation/report-provider-hook-parity.sh --check
bash -n scripts/validation/report-provider-hook-parity.sh scripts/validation/check-repo-contracts.sh
git diff --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-PHM-001**: Generated provider hook parity matrix exists under
  `docs/90.references/data/governance/`.
- **VAL-PHM-002**: Matrix reports Claude/Codex hook event status and Gemini
  behavioral reminders.
- **VAL-PHM-003**: Repo contracts check matrix freshness.
- **VAL-PHM-004**: Stage 03/04 evidence, governance-data indexes, script
  inventory, and automation candidate closure are in sync.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-06-provider-hook-parity-matrix.md](../../04.execution/plans/2026-07-06-provider-hook-parity-matrix.md)
- **Tasks**: [../../04.execution/tasks/2026-07-06-provider-hook-parity-matrix.md](../../04.execution/tasks/2026-07-06-provider-hook-parity-matrix.md)
- **Generated matrix**: [../../90.references/data/governance/provider-hook-parity-matrix.md](../../90.references/data/governance/provider-hook-parity-matrix.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
