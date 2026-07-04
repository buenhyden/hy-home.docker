---
status: active
---
<!-- Target: docs/90.references/research/agentic-engineering/quality-ci-formatting.md -->

# Reference: Quality, CI/CD, QA, and Formatting

## Overview

This reference analyzes CI/CD, QA, formatting, and secure quality gates, then compares them with GitHub Actions, validation scripts, pre-commit, hook-mediated formatting, and repository contracts in `hy-home.docker`.

## Purpose

Help agent-first work treat quality as a combination of local/remote feedback loops, formatting gates, security checks, traceability checks, and evidence capture rather than a final manual review step.

## Repository Role

This reference provides background for the QA scope, CI workflow, scripts README, and HAFE policy. It does not define new CI jobs, branch protection, pre-commit hooks, or formatters.

## Scope

### In Scope

- GitHub Actions workflow/job/step model
- DORA delivery metrics and CI/CD feedback
- pre-commit and formatting tools
- Secure workflow and supply-chain guardrails
- Repo-local QA/CI gate mapping

### Out of Scope

- GitHub remote settings changes
- CI workflow changes
- pre-commit configuration changes
- Branch protection changes
- Security scanner adoption

## Definitions / Facts

- **Workflow**: GitHub Actions workflows are configurable automated processes defined in YAML files and triggered by repository events.
- **Jobs and steps**: GitHub Actions can run jobs sequentially or in parallel, and each job runs steps on a runner or container.
- **Required status checks**: Protected branches can require status checks to pass before merge.
- **DORA metrics**: DORA frames software delivery performance through throughput and instability metrics such as deployment frequency, lead time, change failure, and recovery.
- **Pre-commit**: The pre-commit framework catches simple issues before code review so reviewers can focus on architecture rather than trivial style issues.
- **EditorConfig**: EditorConfig provides a file format and editor plugins for consistent coding style across editors and IDEs.
- **Prettier**: Prettier is an opinionated formatter that parses and reprints code to enforce consistent style.
- **Secure workflow use**: GitHub Actions security guidance highlights risks around untrusted input, third-party actions, token/secrets exposure, and cache trust boundaries.
- **Secure SDLC**: NIST SSDF provides practices for integrating secure development into SDLC implementations.

## Repo-local Quality Gate Map

| Quality Area | Repo-local Gate | Role |
| --- | --- | --- |
| Docs traceability | `check-doc-traceability.sh`, `docs-traceability` job | plan/task/operations link synchronization |
| Implementation alignment | `check-doc-implementation-alignment.sh` | active docs alignment with tracked implementation surfaces |
| Repository contracts | `check-repo-contracts.sh`, `repo-contracts` job | taxonomy, templates, runtime catalog, Docker image/tag policy, workflow/script checks |
| Compose validation | `validate-docker-compose.sh`, compose jobs | root and all-profile Compose rendering |
| Hardening | `check-all-hardening.sh`, infrastructure-hardening job | tier hardening baseline |
| Template/security | `check-template-security-baseline.sh` | template adoption and security baseline |
| QuickWin | `check-quickwin-baseline.sh` | QuickWin baseline controls |
| Pre-commit | CI pre-commit job, `.pre-commit-config.yaml` | formatting/lint hook policy |
| Frontend | Next.js lint/typecheck/build/Storybook | UI project quality gate |
| Security scan | `zizmor` job | GitHub Actions security analysis |
| Diff hygiene | `git diff --check` | whitespace and conflict-marker hygiene |

## Analysis

The QA system in `hy-home.docker` is broader than a single test command. Documentation traceability, repository contracts, Compose rendering, hardening, template/security, QuickWin, pre-commit, frontend build, and zizmor each cover a different risk class. This fits GitHub Actions' workflow/job/step model.

From a DORA perspective, this repository's CI does not directly measure runtime deployment frequency or recovery time. Instead, it reduces lead time and change-failure risk through pre-merge validation gates. That is a practical quality model for a documentation-heavy infrastructure workspace.

Formatting is less about taste and more about where drift is caught. pre-commit, post-tool validation, and `git diff --check` catch trivial drift early. Repository guidance does not make manual pre-commit runs the default procedure, so documentation tasks should prioritize repository scripts and diff hygiene.

QA covers formatting, linting, syntax checks, documentation contracts, Compose rendering, hardening, security baselines, and CI-only gates as separate evidence classes. This matters because a docs traceability failure, a Compose rendering failure, and a GitHub-only SARIF gate require different owners, evidence, and skipped-check rationale.

Docker Compose infrastructure work still follows Stage 01-05 when it changes requirements, architecture, implementation contracts, execution evidence, or operations behavior. Quality gates can verify Compose rendering and hardening, but they do not replace active-stage requirements, specs, task evidence, or operations guidance.

For secure quality gates, GitHub Actions SHA pinning, minimal permissions, zizmor SARIF, secret boundaries, cache caution, NIST SSDF, SLSA, and OWASP SAMM are useful references. Secure SDLC frameworks remain references unless adopted through a separate approved policy, spec, or task.

## Application Notes for This Workspace

- QA evidence should separate local checks, CI-only gates, hook/script evidence, and skipped-check rationale.
- Docs-only changes still require repository contracts, traceability, and diff hygiene.
- QA evidence should name formatting, linting, syntax, documentation contracts, Compose rendering, hardening, security baselines, and CI-only gates separately.
- CI workflow changes require separate approval because local files do not prove remote GitHub behavior.
- Formatting drift should be treated as review noise and contract-failure risk, not personal style.
- Security scanner results remain reference evidence until active finding triage connects them to remediation work.
- Secure SDLC frameworks remain references unless adopted through a separate approved policy, spec, or task.

## Potential Follow-up / Gap

- Actual remote required-check settings cannot be proven from local repository files alone.
- Operating DORA metrics would require deployment and recovery data sources.
- Formal SLSA, OWASP SAMM, or NIST SSDF mappings would require separate approved policy/spec work.

## Source Rules

- CI/CD and formatting facts should prefer official docs.
- Metrics frameworks are interpretation references, not adopted targets.
- Repo-local gates must be verified against the scripts README, QA scope, and CI workflow.

## Sources

- [GitHub Actions workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions) - workflow YAML model
- [GitHub Actions jobs](https://docs.github.com/actions/using-jobs/using-jobs-in-a-workflow) - jobs in workflows
- [GitHub protected branches](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) - required status checks behavior
- [GitHub secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) - workflow security guidance
- [DORA metrics](https://dora.dev/guides/dora-metrics/) - throughput and instability metrics
- [Martin Fowler: Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html) - continuous delivery framing
- [pre-commit official docs](https://pre-commit.com/) - pre-commit hook framework
- [EditorConfig](https://editorconfig.org/) - cross-editor style consistency
- [EditorConfig specification](https://spec.editorconfig.org/) - file format details
- [Prettier docs](https://prettier.io/docs) - opinionated formatter behavior
- [Prettier CLI](https://prettier.io/docs/cli) - `--check` CI usage
- [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) - secure software development practices
- [OWASP SAMM](https://owasp.org/www-project-samm/) - secure software assurance maturity model
- [SLSA](https://slsa.dev/) - supply-chain integrity framework
- [QA scope](../../../00.agent-governance/scopes/qa.md) - repo-local QA policy
- [Scripts README](../../../../scripts/README.md) - repo-local script and QA gate inventory
- [CI workflow](../../../../.github/workflows/ci-quality.yml) - repo-local CI jobs

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when CI workflow, validation scripts, formatting tools, or security gate sources change
- **Update Trigger**: Update when QA gate inventory or external CI/CD/formatting guidance changes

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [spec-driven SDLC](./spec-driven-sdlc.md)
- [QA scope](../../../00.agent-governance/scopes/qa.md)
- [Scripts README](../../../../scripts/README.md)
