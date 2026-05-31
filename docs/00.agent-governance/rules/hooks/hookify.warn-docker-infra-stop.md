---
name: warn-docker-infra-stop
enabled: true
event: stop
pattern: .*
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

**Docker infrastructure completion checklist (project rule)**

`docs/00.agent-governance/rules/postflight-checklist.md` — checks before completing infra-layer work:

**Infrastructure Gate (when the infra layer changes):**

- [ ] `bash scripts/validation/validate-docker-compose.sh` passes.
- [ ] Changed files contain no plaintext secrets; use Docker Secrets or `secrets/` mounts.
- [ ] Named volumes follow the `[Service]-[Data]-[Volume]` rule.

**Settings Gate (when settings change):**

- [ ] `settings.json` contains only team-shared settings (git tracked).
- [ ] `settings.local.json` contains only personal overrides.
- [ ] The two files have no duplicate settings.

**Governance memory update:**

- [ ] Record the work log in `docs/00.agent-governance/memory/progress.md`.
- [ ] Record changed files, verification evidence, and unresolved risk.

**Completion blockers (halt conditions):**

| Condition | Action |
| --------- | ------ |
| `validate-docker-compose.sh` fails | fix Compose and rerun |
| duplicate settings | remove duplicates from `settings.local.json` |
| plaintext secret found | replace with Docker Secret reference |

For PR-related work, also check the Completion Gate in
`docs/00.agent-governance/rules/github-governance.md`.

## Related Documents

- `docs/00.agent-governance/README.md`
