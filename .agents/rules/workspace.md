---
layer: agentic
---

# Antigravity Workspace Rules

These are the global workspace rules for agents running within the Antigravity IDE, as specified by the Provider Parity Model.

## 1. Governance Alignment

- This workspace leverages the central governance definitions from `docs/00.agent-governance/`.
- The native rules defined here override fallback instructions for Gemini.

## 2. Model Selection (Reasoning Effort Control)

Antigravity IDE controls reasoning effort explicitly through model routing:

- **`gemini-3.1-pro`**: Must be used for tasks requiring high reasoning effort, such as:
  - Architecture and planning (`workflow-supervisor`)
  - Complex code refactoring
  - System design reviews
- **`gemini-3.5-flash`**: Must be used for standard or low reasoning effort tasks, such as:
  - Documentation generation and formatting
  - Routine QA checks
  - Summarization and iterative text editing

## 3. Communication Protocol

- Intermediate artifacts must be written to `_workspace/<phase>_<agent>_<artifact>.<ext>`.
- Final audit handoffs are routed to `.agent-work/report/`.
- No dead `_workspace/` files should be deleted without user approval.
