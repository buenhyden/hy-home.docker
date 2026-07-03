---
layer: agentic
---

# Antigravity Workspace Rules

These are Gemini/Antigravity runtime adapter rules for this workspace. They
route the IDE to the canonical Stage 00 governance documents; they do not own
repository policy.

## 1. Governance Alignment

- Policy source of truth: `docs/00.agent-governance/`.
- Provider model and adapter source of truth:
  `docs/00.agent-governance/providers/agents-md.md`,
  `docs/00.agent-governance/providers/gemini.md`, and
  `docs/00.agent-governance/subagent-protocol.md`.
- If this file conflicts with Stage 00 governance, Stage 00 wins. Update the
  owner document first, then adjust this adapter only when Gemini runtime
  behavior needs a local bridge.

## 2. Model Selection (Reasoning Effort Control)

Antigravity IDE controls reasoning effort through model routing. Use the model
tiers defined in `docs/00.agent-governance/subagent-protocol.md`; do not edit
model identifiers in this adapter independently.

Runtime mapping summary:

- Supervisor-tier work follows the Gemini supervisor model in the Stage 00
  Model Policy.
- Worker-tier work follows the Gemini worker model in the Stage 00 Model
  Policy.

## 3. Communication Protocol

- Intermediate artifacts and audit handoffs follow
  `docs/00.agent-governance/subagent-protocol.md`.
- Preserve existing `_workspace/` artifacts unless the user explicitly approves
  deletion.
- Final repository evidence belongs in the canonical stage path defined by
  `docs/00.agent-governance/rules/workflows.md`, not in this adapter.
