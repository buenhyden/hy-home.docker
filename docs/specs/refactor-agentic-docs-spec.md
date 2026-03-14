---
layer: architecture
---

# Technical Specification: Agentic Documentation Refactor

## 1. Directory Structure

All core engineering documents remain in their category-specific folders under `docs/`:

- `adr/`, `ard/`, `prd/`, `specs/`, `plans/`, `runbooks/`, `operations/`.

## 2. Metadata Standard

Every Markdown file must start with:

```yaml
---
layer: <layer_name>
---
```

Supported layers: `entry | meta | core | ops | agentic | architecture | infrastructure | data | messaging | observability | workflow | ai | tooling | communication`.

## 3. Agent Instruction Consolidation

- **Gateway**: `docs/agentic/gateway.md` (Primary entry point).
- **Instructions**: `docs/agentic/instructions.md` (Behavioral logic).
- **Rules**: `docs/agentic/rules/` (Granular policies).

## 4. Lazy Loading Logic

Agents are instructed to search for `[LOAD:<marker>]` and fetch the corresponding file.
Markers:

- `[LOAD:RULES:PERSONA]` -> `docs/agentic/rules/persona-rule.md`
- `[LOAD:PRD]` -> `docs/prd/README.md`
- ...etc.
