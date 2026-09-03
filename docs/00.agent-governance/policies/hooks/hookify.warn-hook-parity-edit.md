---
title: "WARNING: hook parity contract review required"
version: 1.0.0
type: governance/hook-policy
status: active
owner: "@buenhyden"
name: warn-hook-parity-edit
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: (\.claude/settings\.json|\.codex/hooks\.json)$
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

**Hook file edit detected; parity contract review required (project rule)**

**When changing hook files, confirm:**

| Contract | Claude | Codex |
| --- | --- | --- |
| Registry owner | `providers/registry.yaml` `semantic_events.claude` and `hook_contracts.claude` | `providers/registry.yaml` `semantic_events.codex` and `hook_contracts.codex` |
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
bash scripts/validation/report-provider-hook-parity.sh --validate-only
bash scripts/validation/report-provider-hook-parity.sh --check
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all
```

## Related Documents

- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/providers/registry.yaml`
