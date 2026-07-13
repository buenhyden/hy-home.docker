---
layer: agentic
---

# Harness Implementation Map

Single map of the harness surfaces in `hy-home.docker` and the canonical source
that governs each one. This is a routing aid only; detailed policy stays in the
linked sources. It does not define new policy.

## Control / Governance

| Surface             | Source                                                     | Role                                  | Required Validation               | Evidence               |
| ------------------- | ---------------------------------------------------------- | ------------------------------------- | --------------------------------- | ---------------------- |
| Root shims          | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`                      | Thin entry routing into Stage 00      | `check-repo-contracts.sh`         | PR Validation Evidence |
| Governance hub      | `docs/00.agent-governance/README.md`, `rules/bootstrap.md` | Policy SSOT and bootstrap sequence    | `validate-harness.sh`             | `memory/progress.md`   |
| Approval boundaries | `rules/approval-boundaries.md`                             | Protected-surface and approval matrix | Link integrity                    | PR Validation Evidence |

## Docker Compose Runtime

| Surface        | Source                           | Role                             | Required Validation                               | Evidence               |
| -------------- | -------------------------------- | -------------------------------- | ------------------------------------------------- | ---------------------- |
| Root compose   | `docker-compose.yml`             | Root-active include and profiles | `validate-docker-compose.sh`                      | PR Validation Evidence |
| Service stacks | `infra/**/docker-compose*.yml`   | Per-domain service definitions   | `validate-docker-compose.sh` (core + all-profile) | PR Validation Evidence |
| Version pins   | `infra/tech-stack.versions.json` | Tech-stack version SSOT          | `sync-tech-stack-versions.sh --check`             | CI drift gate          |

## Secrets / Credentials

| Surface           | Source                                                  | Role                                               | Required Validation                      | Evidence               |
| ----------------- | ------------------------------------------------------- | -------------------------------------------------- | ---------------------------------------- | ---------------------- |
| Secret layout     | `secrets/README.md`                                     | Path and registry contract (values read-forbidden) | `validate-docker-compose.sh --preflight` | PR (redacted)          |
| Secret generation | `scripts/operations/gen-secrets.sh`                     | Approved secret generation                         | Preflight path check                     | Runbook link           |
| Env contract      | `.env.example`, `secrets/SENSITIVE_ENV_VARS.md.example` | Variable name and default contract                 | `check-repo-contracts.sh`                | PR Validation Evidence |

## Scripts / Automation

| Surface            | Source                  | Role                                            | Required Validation                     | Evidence               |
| ------------------ | ----------------------- | ----------------------------------------------- | --------------------------------------- | ---------------------- |
| Script inventory   | `scripts/README.md`     | Purpose-folder ownership, no duplicate wrappers | `check-repo-contracts.sh`               | PR Validation Evidence |
| Operations scripts | `scripts/operations/**` | Provider/version sync, secret generation        | `run-local-qa-gates.sh --script-backed` | PR Validation Evidence |

## Validation / CI

| Surface        | Source                                       | Role                                          | Required Validation               | Evidence               |
| -------------- | -------------------------------------------- | --------------------------------------------- | --------------------------------- | ---------------------- |
| Harness gate   | `scripts/validation/validate-harness.sh`     | Thin wrapper for harness-surface validation    | self                              | PR Validation Evidence |
| Local QA gate  | `scripts/validation/run-local-qa-gates.sh`   | Script-backed, all-profile, and harness modes  | `--harness` and `--script-backed` | PR Validation Evidence |
| Repo contracts | `scripts/validation/check-repo-contracts.sh` | Structure, template, and parity contracts     | self                              | PR Validation Evidence |
| CI quality     | `.github/workflows/ci-quality.yml`           | Remote enforcement of the same gates          | GitHub Actions                    | PR required checks     |

## Hardening

| Surface                    | Source                                                   | Role                                   | Required Validation | Evidence               |
| -------------------------- | -------------------------------------------------------- | -------------------------------------- | ------------------- | ---------------------- |
| Hardening checks           | `scripts/hardening/check-all-hardening.sh`               | Infra hardening baseline (QW-001..005) | self                | PR Validation Evidence |
| Template/security baseline | `scripts/validation/check-template-security-baseline.sh` | Template and security baseline         | self                | PR Validation Evidence |

## Provider Hooks

| Surface              | Source                                | Role                             | Required Validation               | Evidence               |
| -------------------- | ------------------------------------- | -------------------------------- | --------------------------------- | ---------------------- |
| Hook dispatcher      | `scripts/hooks/agent-event-hook.sh`   | Provider-neutral hook routing    | `validate-harness.sh`             | PR Validation Evidence |
| Post-tool validation | `scripts/hooks/post-tool-validate.sh` | Changed-file style normalization | self                              | PR Validation Evidence |

## Evidence / Progress

| Surface            | Source                                        | Role                                   | Required Validation         | Evidence |
| ------------------ | --------------------------------------------- | -------------------------------------- | --------------------------- | -------- |
| Progress log       | `docs/00.agent-governance/memory/progress.md` | Mandatory work progress log            | `check-repo-contracts.sh`   | self     |
| Execution evidence | `docs/04.execution/tasks/**`                  | Task execution and validation evidence | `check-doc-traceability.sh` | self     |

## PR / Review

| Surface           | Source                             | Role                                                 | Required Validation       | Evidence               |
| ----------------- | ---------------------------------- | ---------------------------------------------------- | ------------------------- | ---------------------- |
| PR template       | `.github/PULL_REQUEST_TEMPLATE.md` | Validation, risk, secret, and Harness Impact capture | `check-repo-contracts.sh` | PR Validation Evidence |
| GitHub governance | `rules/github-governance.md`       | Completion gate and review policy                    | self                      | PR required checks     |

## Operations / Runbooks

| Surface          | Source                                                   | Role                                      | Required Validation                     | Evidence               |
| ---------------- | -------------------------------------------------------- | ----------------------------------------- | --------------------------------------- | ---------------------- |
| Operations index | `docs/05.operations/README.md`                           | Guides, policies, runbooks, incidents     | `check-doc-traceability.sh`             | PR Validation Evidence |
| Task form        | `docs/99.templates/templates/sdlc/task.template.md`      | Ordinary and harness execution evidence   | `check-repo-contracts.sh` template loop | Stage 04 Task           |

## Related Documents

- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/rules/approval-boundaries.md`
- `docs/00.agent-governance/rules/environment-constraints.md`
- `docs/99.templates/templates/sdlc/task.template.md`
- `scripts/README.md`
