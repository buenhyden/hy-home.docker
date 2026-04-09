---
layer: agentic
---

# Postflight Checklist

Run after every agent task before declaring completion.

## §1 Infrastructure Gate (infra layer only)

- [ ] `bash scripts/validate-docker-compose.sh` exits 0
- [ ] `docker compose ps` shows all expected services UP
- [ ] No plaintext secrets introduced in any changed file
- [ ] Named volumes follow `[Service]-[Data]-[Volume]` convention

## §2 Settings Gate (any settings change)

- [ ] `settings.json` contains team-shared config (git tracked)
- [ ] `settings.local.json` contains personal overrides only
- [ ] No duplication across both files

## §3 Documentation Gate (DOCS 3 RULES)

- [ ] R1: Template loaded, all sections filled, `status: draft` set
- [ ] R2: Parent `README.md` updated for any folder-level change
- [ ] R3: `## Related Documents` section present with upstream links

## §4 Secrets Gate (all layers)

- [ ] No plaintext credentials in source-controlled files
- [ ] Docker Secrets / `secrets/` mounts used for sensitive values
- [ ] `.env` files excluded from git if they contain real values

## §5 Lint Gate (all layers)

- [ ] `.pre-commit-config.yaml` hooks will pass (never run manually)
- [ ] No linter suppressions added without comment explaining why

## §6 Completion Blockers (HALT if any fail)

| Condition                          | Action                               |
| ---------------------------------- | ------------------------------------ |
| `validate-docker-compose.sh` fails | Fix compose; do not proceed          |
| Settings duplicated                | Remove from `settings.local.json`    |
| Template not used                  | Apply template before closing        |
| `README.md` not updated            | Update before closing                |
| `## Related Documents` missing     | Add before closing                   |
| Plaintext secret found             | Replace with Docker Secret reference |

## Related Documents

- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `AGENTS.md` §4 Orchestration Protocol
