---
layer: agentic
---

# Postflight Checklist

Run after every agent task before declaring completion.

## Infrastructure Gate (infra layer only)

- [ ] `bash scripts/validation/validate-docker-compose.sh` exits 0
- [ ] `docker compose ps` shows all expected services UP
- [ ] No plaintext secrets introduced in any changed file
- [ ] Named volumes follow `[Service]-[Data]-[Volume]` convention

## Settings Gate (any settings change)

- [ ] `settings.json` contains team-shared config (git tracked)
- [ ] `settings.local.json` contains personal overrides only
- [ ] No duplication across both files

## Documentation Gate (DOCS 3 RULES)

- [ ] R1: Template loaded, required sections filled, and lifecycle `status` set according to the target template/stage
- [ ] R2: Parent `README.md` updated for any folder-level change (including content modifications that affect folder-level descriptions)
- [ ] R3: `## Related Documents` section present with upstream links
- [ ] Changed/new target Markdown passes `check-document-metadata.py --mode check-changed` with a safe explicit base

## Secrets Gate (all layers)

- [ ] No plaintext credentials in source-controlled files
- [ ] Docker Secrets / `secrets/` mounts used for sensitive values
- [ ] `.env` files excluded from git if they contain real values

## Lint Gate (all layers)

- [ ] Direct `pre-commit run` was not used; normal commit hooks remain automatic
- [ ] At an approved final QA all-files gate,
      `scripts/validation/run-agent-precommit-all-files.sh` ran from a clean
      linked worktree, or task evidence records why it was skipped
- [ ] Wrapper evidence covers only Git-visible, non-ignored repository paths and
      records command, allowed prefixes, hook exit, unexpected paths, and review
- [ ] Evidence does not claim ignored/outside-repository observation or process/
      filesystem sandboxing
- [ ] No linter suppressions added without comment explaining why

## Agent Harness Gate (agent/provider/hook surfaces)

- [ ] `check-agent-governance-contract.py --mode repository --section all`
      exits 0
- [ ] `run-agent-output-eval-fixtures.sh --check-fixtures` reports exactly eight
      fixtures, ten regressions, `fixtures_check=pass`, and
      `regressions_check=pass`
- [ ] Loop owner and independent reviewer are different, retry bounds were not
      exceeded, and evidence uses only the four sanitized fields
- [ ] Provider sync, when applicable, ran only with explicit `--check`
- [ ] SessionStart performed no Docker or live-service probe

## Completion Blockers (HALT if any fail)

| Condition                          | Action                               |
| ---------------------------------- | ------------------------------------ |
| `validate-docker-compose.sh` fails | Fix compose; do not proceed          |
| Settings duplicated                | Remove from `settings.local.json`    |
| Template not used                  | Apply template before closing        |
| `README.md` not updated            | Update before closing                |
| `## Related Documents` missing     | Add before closing                   |
| Changed/new metadata check fails   | Correct typed metadata or approved transition evidence |
| Controlled wrapper reports exit 20 | Stop and review unexpected paths; do not reset, checkout, or clean |
| Plaintext secret found             | Replace with Docker Secret reference |
| Typed harness or eval gate fails   | Stop; preserve value-free findings and remediate before completion |

## Related Documents

- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/subagent-protocol.md`
- `AGENTS.md` — Verification
