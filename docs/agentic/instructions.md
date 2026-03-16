---
layer: agentic
---

# Agent Behavioral Instructions

Core behavioral standards for AI agents in `hy-home.docker`.

## 1. Protocol Baseline

- **Gateway-First**: Agents MUST load `gateway.md` at session start.
- **Lazy Loading**: Load specialized rules from `rules/` ONLY when triggered by `[LOAD:RULES:...]` markers.
- **Spec-Driven**: Never implement complex features without a specification in `docs/specs/`.
- **Validation**: Run `scripts/validate-docker-compose.sh` before infrastructure changes.

## 2. Metadata & Structure

- **Layer Metadata**: Every file MUST include `layer:` frontmatter.
- **Flat Taxonomy**: Use `docs/<category>/` roots. Avoid deep nesting.
- **Relative Links**: Use relative paths for all cross-documentation links.

## 3. Skill & Context Optimization

- **Full Skill Autonomy**: Choose context-fit skills proactively. No skills are restricted.
- **Token Efficiency**: Load only the current task-specific context to keep cumulative descriptions < 15k tokens.
- **Handoffs**: Use `session-handoff` for long-running sessions to prevent context rot.
