---
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

`docs/00.agent-governance/providers/claude.md` — Hook Parity Contract:

> "Claude hook events must stay behaviorally aligned with Codex hook events where both runtimes support the event."

**When changing hook files, confirm:**

| Check | Claude | Codex |
| ----- | ------ | ----- |
| Config file | `.claude/settings.json` | `.codex/hooks.json` |
| Event coverage | SessionStart, PreToolUse, PostToolUse, SessionEnd, Stop, PreCompact | same |
| File edit matcher | `Write\|Edit\|MultiEdit\|apply_patch\|ApplyPatch` | same |
| Shared dispatcher | `.claude/hooks/*.sh` thin wrapper to `scripts/hooks/agent-event-hook.sh` | `scripts/hooks/agent-event-hook.sh` |
| README guidance | target-stage template guidance plus README folder/service-leaf guidance | same |

**Parity checklist:**

- [ ] Event added or removed: apply the same change to the other runtime file.
- [ ] Timeout changed: keep both runtime files aligned.
- [ ] New event matcher: add the handler in `agent-event-hook.sh`.
- [ ] README edit guidance: preserve the folder index vs. infra service leaf readiness contract.
- [ ] `.codex/README.md`: update the Current Hook Contract if behavior changed.

**After completion, verify:**

```bash
bash scripts/validation/check-repo-contracts.sh
python3 -m json.tool .claude/settings.json >/dev/null && echo "Claude JSON valid"
python3 -m json.tool .codex/hooks.json >/dev/null && echo "Codex JSON valid"
```

## Related Documents

- `docs/00.agent-governance/README.md`
