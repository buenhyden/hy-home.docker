---
title: "WARNING: hook parity contract review required"
version: "1.0.2"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(\\.claude/settings\\.json|\\.codex/hooks\\.json)$"
enabled: true
event: "file"
name: "warn-hook-parity-edit"
---

# WARNING: hook parity contract review required

## Overview

Apply the declared `warn` action for warn-hook-parity-edit.

## Scope

The declared `file` event and structured `conditions` define the matching scope; native event delivery remains a separate observation.

## Rules

**Hook file edit detected; parity contract review required (project rule)**

**When changing hook files, confirm:**

| Contract | Claude | Codex |
| --- | --- | --- |
| Registry owner | `.agents/governance/providers/registry.yaml` `semantic_events.claude` and `hook_contracts.claude` | `.agents/governance/providers/registry.yaml` `semantic_events.codex` and `hook_contracts.codex` |
| Native consumer | `.claude/settings.json` | `.codex/hooks.json` |
| Dispatch | `.claude/hooks/*.sh` thin wrappers | `scripts/hooks/agent-event-hook.sh` |

**Parity checklist:**

- [ ] Change the Provider Registry contract and matching native consumer in the
      same approved unit.
- [ ] Preserve provider-specific unsupported events instead of claiming false
      parity.
- [ ] Bind each command to its registered executable and semantic event.
- [ ] Keep Claude wrappers thin and route shared behavior through
      `scripts/hooks/agent-event-hook.sh`.

**After completion, verify:**

```bash
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section providers
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all
python3 scripts/operations/provider_surface_renderer.py --check
```

## Exceptions

No exception is declared by this rule.

## Related Documents

- `.agents/README.md`
- `.agents/governance/providers/registry.yaml`
