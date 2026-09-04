---
title: "Agent Quality and Security Standards"
version: "1.0.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
---

# Agent Quality and Security Standards

Universal quality gate for agent-driven changes in this repository.

## 1. Documentation Quality Rubric

| Grade | Description | Requirements                                                           |
| :---- | :---------- | :--------------------------------------------------------------------- |
| A     | Elite       | Accurate routing, valid commands, no policy conflicts, SSoT alignment  |
| B     | Strong      | Mostly aligned with minor omissions                                    |
| C     | Functional  | Works but has clarity or coverage gaps                                 |
| D     | Weak        | Multiple stale references or ambiguous guidance                        |
| F     | Failing     | Hardcoded secrets, broken governance links, contradictory instructions |

Quality dimensions:

- Actionability: instructions are concrete and testable.
- Conciseness: avoid generic filler.
- Accuracy: references match current repository structure.

## 2. Security Baseline

- Never commit plaintext credentials.
- Prefer secret managers or mounted secret files.
- Keep inter-service networking restricted by intended network boundaries.
- Use least-privilege runtime defaults when modifying infrastructure.
- Identity and access: centralized authentication via Keycloak (OIDC/SAML), and
  least-privilege RBAC/ABAC at API and data layers.
- Secrets management: plaintext credentials in source-controlled configs are
  prohibited; Docker secrets and/or a Vault-backed secret flow are mandatory.
- Container hardening, mandatory where compatible: non-root runtime,
  `no-new-privileges`, minimal capabilities, read-only mounts for static
  config, and secret injection by file rather than image layer or plaintext
  environment value. These are manual review expectations unless an existing
  validator or hook enforces the specific field.
- Network hardening: isolate traffic on intended networks and enforce TLS at
  ingress boundaries.

## 3. Reliability Baseline

- Include health checks for long-running services when applicable.
- Keep validation explicit in plans and task evidence.
- Avoid introducing commands that do not exist in this repository.
- Maintain a strict minimum of 90% unit test coverage for domain logic.
- Mark the 90% target N/A only for docs-only, policy-only, infrastructure configuration, or validation-script changes where no domain-code coverage signal applies.
- Bug fixes require regression evidence; refactors require behavior-preserving validation evidence.
- Agent-loop changes require deterministic fixture and mutation coverage for
  routing, retired-role rejection, boundary escalation, hook denial, bounded
  retry, completion evidence, adapter rendering, model fallback, and
  calibration.
- E2E coverage verifies critical paths via Playwright. Load coverage verifies
  API performance via k6 or Locust.
- A SEV1 or SEV2 incident requires a retrospective as `postmortem.md` inside
  its incident packet folder.

## 4. Execution Boundary

- **Local**: fail-fast validation, for example
  `scripts/validation/run-ci-gate.py --profile changed`, automatic commit hooks
  for formatting and linting, and pre-push structural contract scripts. Agents
  must not invoke `pre-commit run` directly. Approved final QA all-files
  execution uses only `scripts/validation/run-agent-precommit-all-files.sh` from
  an initially clean linked worktree with a tracked co-located Task and reviewed
  prefixes.
- **Remote (GitHub CI)**: the ultimate SSoT quality gate. Heavy analysis such as
  E2E, Zizmor SARIF upload, and SonarQube belongs here.
- **CI-only pre-commit**: `scripts/validation/run-ci-precommit.sh` accepts no
  arguments, no Agent-wrapper variables, and no caller-supplied `SKIP`. It
  requires `GITHUB_ACTIONS=true` and `CI=true`, sets its own skip list, and
  executes the exact pinned CI command. It is not a local or Agent
  authorization path. The public gate reaches it as the `leaf.pre-commit`
  root of the `repository-integrity` suite, which is the changed-profile
  fallback, so formatting and linting gate every push and pull request.
- **Anti-duplication**: do not execute the same heavy workloads redundantly. A
  task with a dedicated gate leaf is skipped in the CI `pre-commit` runner. The
  `public-validation-changed` and `public-validation-full` hooks are skipped
  for a second reason: the gate invokes the runner, so running them from inside
  it would make the two orchestrators call each other without end.

## 5. Change-Type Verification Matrix

Use the smallest meaningful checks for the touched layer. When a listed check is
not applicable, record the skipped-check rationale in the task evidence.

| Change Type                                  | Local Checks                                                                                                                                                                                            | CI-Only / Remote Gate                                            | Hook or Script Evidence                                                | Skip Rationale Required                                              |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Documentation-only stage docs                | `python3 scripts/validation/run-ci-gate.py --profile changed` and LLM Wiki regeneration via `scripts/knowledge/generate-llm-wiki.py --write` when docs are added, removed, or renamed | Public document suites selected by the changed-path contract | Post-edit validation hook and Task evidence                           | Domain tests, coverage, Docker runtime checks                        |
| Historical-file cleanup                     | Documentation checks, stale active-reference scans, and minimal metadata/link checks                                                                                                                       | Remote docs implementation-alignment, traceability, and repo contracts | Task evidence and Git recovery reference                              | Domain tests, coverage, Docker runtime checks                        |
| Governance or provider policy docs           | Documentation checks plus `sync-provider-surfaces.sh --check` when provider surfaces are affected                                                                                                       | Remote repo contracts and required checks                        | Provider sync check output and policy-gate evidence                    | Runtime tests unless behavior/config changed                         |
| Provider adapter, hook, or validation script | Targeted script self-check, `run-local-qa-gates.sh` when the change affects shared script/CI behavior, repo contracts, provider sync, quickwin/template-security baselines when relevant; controlled all-files wrapper only at an approved final QA gate | Required GitHub quality gates and security scans | Wrapper command/prefix/exit/path/review evidence or targeted script output | CI-only tools such as SARIF upload are named, not duplicated locally; skipped wrapper rationale is explicit |
| Runtime, Docker, or Compose config           | Compose validation, hardening scripts, targeted service smoke checks when safe                                                                                                                          | Compose and hardening jobs, any protected-branch required checks | Docker/Compose command output or explicit approval gate                | Live service mutation skipped unless approved                        |
| CI workflow or GitHub protection             | Static workflow validation, repo contracts, ruleset documentation review                                                                                                                                | GitHub Actions jobs, branch protection/ruleset verification      | `gh` or workflow evidence where approved                               | Local execution of GitHub-only jobs such as `zizmor` SARIF upload    |
| Model policy or reasoning-effort config      | Stage 00 policy review, provider sync, validator support check                                                                                                                                          | Required repo contracts after generated surfaces update          | Validator output and task evidence                                     | Any unsupported value remains blocked, not skipped                   |
| Agent lifecycle or semantic evaluation       | Typed repository `all` section, provider sync `--check`, the registered model-free fixture/regression suite, and selector tests                                                                          | Existing repository-contract and agent-output eval jobs           | Deterministic pass markers and sanitized lifecycle evidence             | Live model/provider execution remains unclaimed unless separately observed |
| Approved high-risk surface                   | Surface-specific local checks plus co-located Task approval/evidence review; secrets use metadata-only evidence unless a concrete redacted target exists                                                | Remote GitHub, CI, runtime, or provider gates named in task      | Approval source, before/after evidence, rollback path, redaction notes | Approved but unexecuted surfaces are recorded as verified-only       |

## 6. Generated-Artifact Freshness

Some artifacts are generated from repository content and must be regenerated as
part of QA before completion. Treat regeneration as a verification step, not an
optional cleanup.

- **LLM Wiki outputs**: when documents are added, removed, or renamed under
  indexed scopes, regenerate both tracked outputs with
  `python3 scripts/knowledge/generate-llm-wiki.py --write`. Use `--check` for
  read-only freshness validation; a stale output is a hard failure.
- **Knowledge graph**: refresh `graphify-out/` with one-shot `graphify update .`
  after code or doc changes when the CLI is available; report when it is skipped.
  Do not rely on a live `graphify watch` daemon during commits: `pre-commit`
  takes an intermediate stash of unstaged changes, and concurrent watcher writes
  to the tracked `graphify-out/` snapshots conflict on stash restore, which rolls
  back the commit. Refresh the graph, then stage and commit `graphify-out/` as a
  dedicated `chore(graph)` unit. The tracked snapshots are also excluded from
  `pre-commit` file hooks (`exclude: '^graphify-out/'`) so formatters never
  rewrite them mid-commit.
- **General rule**: never hand-edit a generated artifact to pass a check. Re-run
  its generator and commit the generated result as a separate logical unit.

## 7. Local QA/CI Orchestration

Use `bash scripts/validation/run-local-qa-gates.sh --explain` to render the
selected public suite-to-validator mapping without execution. The wrapper
contains no child-command inventory: `--changed`, `--full`, and `--explain`
delegate once to the public runner. These routes do not
upload SARIF, verify remote branch protection, install CI-only dependencies, or
declare protected-branch readiness. The `repo-contracts` gate also blocks
stage-document runtime version drift for implementation-pinned images and
components, so docs-only changes that mention service versions must keep those
literals aligned with current compose declarations and
`infra/tech-stack.versions.json`.

The local runner validates `.github/workflow-contract.yml` and all seven
tracked workflow definitions through
`scripts/validation/check-github-workflow-contract.py`. It lists
`tech-stack-version-sync.yml` as non-gating remote automation, never runs real
pre-commit through the CI-only entry point, and exercises that wrapper only
with the fake-binary regression.

## 8. Workflow and Language Routing

- Follow the sole load order in `policies/bootstrap.md#canonical-load-order`.
- Follow repeatable orchestration in `policies/workflows.md`.
- Apply the document-role language table in
  `policies/documentation-protocol.md#authoring-rules`.
- Resolve write permission through `policies/approval-boundaries.md`.

## 9. Completion Routing

Use only `policies/task-checklists.md#before-completion`. Its conditional
harness, evidence, documentation, and controlled-gate clauses determine which
quality checks apply. PR-specific completion remains owned by the Completion
Gate in `policies/github-governance.md`.

## 10. Formatting and Linting Ownership

- Every tracked file type has exactly one formatting owner, and
  `.pre-commit-config.yaml` is where that owner is named. A tool absent from it
  does not govern this repository, whatever configuration it leaves behind.
- Formatting settings are pinned in the repository, not left to a tool default
  or to whichever version a machine has. `ruff.toml` pins Python.
- An agent editor hook may format a file only in agreement with the registered
  owner. Where a hook lives outside the repository and cannot be registered,
  the repository states its own boundary in the tool's ignore file;
  `.prettierignore` does this for Prettier.
- Do not add a second tool over a file type that already has an owner. Two
  formatters on one file type is a conflict, not redundancy.
- A validator must not depend on where a line breaks. A check that a formatter
  can break was satisfied by typography rather than by content, and the
  exemption belongs on the line as a stated marker.
- Adopting or changing a formatter reformats the corpus once, in its own
  commit, after every check that the reformatting would break is fixed.

## Related Documents

- `docs/00.agent-governance/policies/github-governance.md`
- `docs/00.agent-governance/policies/git-workflow.md`
- `docs/00.agent-governance/policies/agentic.md`
