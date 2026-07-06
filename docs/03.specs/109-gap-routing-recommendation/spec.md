---
status: completed
---

<!-- Target: docs/03.specs/109-gap-routing-recommendation/spec.md -->

# Gap Routing Recommendation Technical Specification

## Overview

This specification defines a non-mutating advisory recommender for routing gaps
to their canonical repository owner. The recommender reads the Stage 00
documentation protocol table and applies simple path-prefix and keyword
heuristics for local use.

## Strategic Boundaries & Non-goals

The recommender is intentionally advisory. It does not create documents, edit
the suggested owner, dispatch remote jobs, change provider runtime behavior, or
decide ambiguous cases without human confirmation.

## Related Inputs

- **PRD**: No dedicated PRD exists; this is a follow-up from the completed
  agentic engineering implementation audit candidate `AEA-AUTO-004`.
- **ARD**: No dedicated ARD exists; the architecture boundary is the existing
  Stage 00 documentation protocol and scripts validation surface.
- **Related ADRs**: No new ADR is required because this adds a local advisory
  script and reference data without changing architecture decisions.

## Contracts

- **Config Contract**: `scripts/validation/recommend-gap-routing.sh` must parse
  the Stage 00 gap-to-stage routing table from
  `docs/00.agent-governance/rules/documentation-protocol.md`.
- **Data / Interface Contract**: The script must accept `--text`, `--stdin`,
  `--files`, and `--list`. It must print suggested owner, matched gap type,
  routing rule, confidence, and reason.
- **Governance Contract**: The script must remain non-mutating and advisory.
  `scripts/validation/check-repo-contracts.sh` must verify representative
  routing behavior.

## Core Design

- **Component Boundary**: Recommendation logic lives in
  `scripts/validation/recommend-gap-routing.sh`; stable explanation lives in
  `docs/90.references/data/governance/gap-to-stage-routing.md`.
- **Key Dependencies**: Stage 00 documentation protocol table and Python
  standard library.
- **Tech Stack**: Bash wrapper with embedded Python for markdown-table parsing
  and recommendation output.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: A routing row is `{gap_type, owner, rule}`.
  A recommendation is `{input_type, input, suggested_owner, matched_gap_type,
  routing_rule, confidence, reason}`.
- **Migration / Transition Plan**: Add the advisory script, register it in the
  script inventory, document the reference data, and add repo-contract behavior
  checks.

## Interfaces & Data Structures

### Core Interfaces

```text
recommend-gap-routing.sh --text <gap description>
recommend-gap-routing.sh --stdin
recommend-gap-routing.sh --files <path> [path...]
recommend-gap-routing.sh --list
```

## API Contract (If Applicable)

Not applicable. This change exposes no external API.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation Specialist / QA Engineer.
- **Inputs**: Stage 00 documentation protocol, optional text descriptions,
  optional repository path inputs.
- **Outputs**: Advisory routing recommendation and Stage 90 reference data.
- **Success Definition**: Representative text and path inputs route to the
  expected canonical owner and repo contracts pass.

## Tools & Tool Contract (If Applicable)

- **Tool List**: shell, `git`, Python standard library, repository validation
  scripts.
- **Permission Boundary**: The recommender reads repository governance text and
  prints recommendations only. It must not read secret values, local auth files,
  raw logs, shell history, or remote state.
- **Failure Handling**: If the Stage 00 table cannot be parsed, fail clearly
  and route the gap manually through documentation protocol.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: Recommendation output is advisory and must
  not override current user instructions or protected-surface approval rules.
- **Policy Constraints**: No automatic edits, no remote actions, no runtime
  actions, and no secret handling.
- **Versioning Rule**: Changes are recorded through Stage 04 evidence and a
  logical commit.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: Stage 04 task evidence records command results.
- **Long-term Memory**: `docs/00.agent-governance/memory/progress.md` records
  the completed automation candidate closure.
- **Retrieval Boundary**: Graphify remains advisory and must be corroborated
  against Stage 00 and the script.

## Guardrails (If Applicable)

- **Input Guardrails**: Redact assignment-like sensitive values from displayed
  text input.
- **Output Guardrails**: Print stage/path recommendations and confidence only.
- **Blocked Conditions**: Missing Stage 00 routing section, too few parsed
  routing rows, or unsupported command mode.
- **Escalation Rule**: Stop before editing protected runtime, remote, provider,
  credential, secret, or CI workflow surfaces.

## Evaluation (If Applicable)

- **Eval Types**: Shell syntax, representative text routing, representative
  path routing, redaction behavior, repo contracts, docs alignment.
- **Metrics**: zero repo-contract failures; expected owner for representative
  fixtures.
- **Datasets / Fixtures**: Current Stage 00 gap-to-stage routing table and
  representative CLI inputs.
- **How to Run**: use the verification commands below and linked task evidence.

## Edge Cases & Error Handling

- **Ambiguous text**: Return Stage 04 task/audit gap first with low confidence.
- **Unknown path**: Return Stage 04 task/audit gap first with low confidence.
- **Sensitive-looking input**: Redact displayed text while still using keywords
  for classification.
- **Operations text with rollback keyword**: Prefer explicit operations terms
  such as runbook and recovery over generic plan terms.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Recommender chooses an unexpected owner.
- **Fallback**: Use the Stage 00 documentation protocol table manually and
  update the heuristic only after validation evidence.
- **Human Escalation**: Required if routing implies protected-surface changes
  or policy changes not already approved.

## Verification

```bash
bash -n scripts/validation/recommend-gap-routing.sh scripts/validation/check-repo-contracts.sh
bash scripts/validation/recommend-gap-routing.sh --text "runbook recovery procedure is missing rollback evidence"
bash scripts/validation/recommend-gap-routing.sh --files docs/03.specs/108-compose-profile-service-coverage-snapshot/spec.md
bash scripts/validation/check-repo-contracts.sh
```

## Success Criteria & Verification Plan

- **VAL-GRR-001**: Operations text with runbook/recovery wording routes to
  `docs/05.operations/`.
- **VAL-GRR-002**: Spec path input routes to `docs/03.specs/`.
- **VAL-GRR-003**: Sensitive-looking text input is redacted in output.
- **VAL-GRR-004**: Full repo contracts pass with `failures=0`.

## Related Documents

- **Plan**: [../../04.execution/plans/2026-07-05-gap-routing-recommendation.md](../../04.execution/plans/2026-07-05-gap-routing-recommendation.md)
- **Tasks**: [../../04.execution/tasks/2026-07-05-gap-routing-recommendation.md](../../04.execution/tasks/2026-07-05-gap-routing-recommendation.md)
- **Gap routing reference**: [../../90.references/data/governance/gap-to-stage-routing.md](../../90.references/data/governance/gap-to-stage-routing.md)
- **Documentation protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
- **Automation candidates**: [../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
