---
layer: agentic
---

# Language Policy

This repository implements a dual-language strategy to balance AI token efficiency with human clarity.

## 1. Agentic Governance (English)

All internal AI instructions, rules, and logic MUST be written in **English**.

- **Location**: `docs/00.agent-governance/`
- **Rationale**: LLMs demonstrate higher precision and lower token usage when processing technical governance in English.

## 2. User Interaction (Korean)

All direct communication with the User (Human) MUST be performed in **Korean**.

- **Action**: Always translate tool outputs, summaries, and notifications into natural, humanized Korean.
- **Tone**: Professional yet approachable, following the `humanizer` skill principles.

## 3. Dual-Purpose Documentation

- **Human-First Docs** (`docs/[01~11]`): Written primarily in **Korean** to ensure stakeholder alignment. Technical terms and code-level references stay in English.
- **AI-Doc Shims**: Root instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) are minimal shims in English to redirect to the correct governance hub.

## 4. Enforcement Rule

> [!IMPORTANT]
> All responses to the User must be in Korean.
> Failure to follow this policy constitutes a governance breach.
