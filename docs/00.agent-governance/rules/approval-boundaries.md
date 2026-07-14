---
layer: agentic
---

# Approval Boundaries

Single approval-boundary matrix for harness surfaces in `hy-home.docker`.
This rule consolidates the Hard Stops that are otherwise scattered across
`rules/environment-constraints.md`, `rules/agentic.md`, and provider notes. It
points to existing policy; it does not redefine it.

## 1. Core Rules

- Secret value files are read-forbidden. Never open or echo secret values,
  tokens, private keys, or certificate contents.
- Secret-related changes record only path, ID, registry, and redacted evidence.
- Protected surfaces require explicit, recorded user approval before any state
  change.
- Operational service restart, rollout, or deployment requires separate
  approval beyond a code or doc change.
- Approval granted for one surface does not extend to another.

## 2. Surface Matrix

| Surface                                    | Default State                     | Approval Required When                                          | Required Validation                                                    | Evidence Location                                   | Rollback                          |
| ------------------------------------------ | --------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------- | --------------------------------- |
| `docker-compose.yml` (root-active include) | Protected                         | Any include, profile, secret, volume, network, or port change   | `bash scripts/validation/validate-docker-compose.sh` + all-profile run | PR Validation Evidence + `docs/04.execution/tasks/` | `git revert`; no runtime mutation |
| `infra/**/docker-compose*.yml`             | Protected                         | Port, volume, network, or secret mount change                   | `validate-docker-compose.sh` (core + all-profile)                      | PR Validation Evidence                              | `git revert`                      |
| `infra/**/README.md`                       | Read-only                         | Service contract or readiness evidence change                   | Doc link integrity                                                     | PR Validation Evidence                              | `git revert`                      |
| `secrets/**`                               | Protected (values read-forbidden) | Path, registry, or secret mapping change (never values)         | `validate-docker-compose.sh --preflight` (path-only)                   | PR (redacted) + runbook link                        | `git revert` of mapping only      |
| `.env.example`                             | Guarded                           | Variable name, default, or comparison-doc change                | `check-repo-contracts.sh`                                              | PR Validation Evidence                              | `git revert`                      |
| `scripts/**`                               | Guarded                           | Validation, hardening, hook, or operation behavior change       | `validate-harness.sh`                                                  | PR Validation Evidence                              | `git revert`                      |
| `.github/workflows/**`                     | Protected                         | Any permission expansion, `pull_request_target`, or `write-all` | `check-repo-contracts.sh` + workflow security review                   | PR Validation Evidence                              | `git revert`                      |
| `docs/00.agent-governance/**`              | Governance SSOT                   | Policy text, agent/skill catalog, or provider parity change     | `validate-harness.sh`                                                  | PR + `memory/progress.md`                           | `git revert`                      |
| `docs/05.operations/**`                    | Operations SSOT                   | Guide, policy, runbook, or incident change                      | `check-doc-traceability.sh`                                            | PR + runbook                                        | `git revert`                      |
| `docs/99.templates/**`                     | Template SSOT                     | Template add, remove, or contract change                        | `check-repo-contracts.sh` template loop                                | PR Validation Evidence                              | `git revert`                      |

## 3. Hard Stops

Stop and record an approval request when work requires any of:

- Reading a secret value, private key, token, or certificate file.
- Creating, modifying, or deleting a Docker secret file.
- Changing `.env` real values.
- Changing the root-active include of `docker-compose.yml`.
- Changing `infra/**` port, volume, network, or secret mount.
- Restarting or deploying an operational service.
- Expanding GitHub Actions permissions, or using `pull_request_target` or
  `write-all`.
- Pushing directly to the `main` branch.

## 4. Required Validation Entry Point

For harness-surface work, run the harness-scoped gate:

```bash
bash scripts/validation/validate-harness.sh
```

## Related Documents

- `docs/00.agent-governance/rules/environment-constraints.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/harness-implementation-map.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/99.templates/templates/sdlc/task.template.md`
