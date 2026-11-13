---
title: "REQ-0027 Approval Task"
version: "0.1.3"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0261-TSK-0001"
parent_ids:
- "SPEC-0261-PLAN-0001"
created: "2026-11-04"
---

# REQ-0027 Approval Task

## Scope

### Objective and Parent

#### Objective

Approve REQ-0027 and promote the dependent documents that match the
implementation.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Operations](../../../05.operations/README.md)
- [Stage authoring matrix](../../../../.agents/governance/stage-authoring-matrix.md)
- [Document Registry](../../../99.templates/registry.json)

### Inputs and Authority

On 2026-11-04 the owner answered "REQ-0027 승인" to approve REQ-0027
(`docs/01.requirements/0027-home-development-host.md`). Earlier that day, for
documents still draft although implemented, the owner answered "Review, then
promote (recommended)": compare each with the implementation and promote only
those that match. This Task pushes and merges nothing.

## Execution Log

### Work Performed

#### Current contract decision

The owner decisions authorize this Spec and Plan as written.

#### Current readiness and execution

Inputs, work units and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0261 | draft | approved | #current-contract-decision |
| SPEC-0261-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0261-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0261-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

#### Decisions

- REQ-0027 moved draft to approved, a direct Registry transition. Only the
  sentence that called the requirement a draft was reworded; the requirements,
  acceptance criteria and risks are unchanged. Backup and restore, OpenBao
  bootstrap and resource acceptance stay unverified acceptance conditions.
- AD-0032 matches `infra/13-experience/storybook/docker-compose.yml`: services
  `storybook` and `storybook-mcp`, profile `experience`, label
  `hy-home.tier: experience`, `pull_policy: never`, unprivileged users, no
  host port, `sso-auth` only on the static origin, only `/mcp` and the
  protected-resource path routed for the MCP, group `/admins`, the Compose
  include in the root file, and the three tool names in
  `projects/storybook/nextjs`. Promoted.
- AD-0031 matches the source: every profile in its HOME candidate list and
  `dev-data` exists in Compose, `dev-pg` loads `timescaledb`, the directory
  names under `04-data`, `11-quality`, `12-analytics`, `06-observability` and
  `08-ai` exist, `renovate.json5` and a Storybook-only `dependabot.yml` exist,
  and its risk section keeps backup, bootstrap and resource acceptance as
  prerequisites. Promoted.
- 0087 Gatus (policy, guide, runbook) matches `infra/06-observability`: profiles
  `obs`, `availability`, `dev`, secret `gatus_oidc_client_secret`, no host
  port, router with `gateway-standard-chain@file` and `/metrics` excluded,
  `home-gatus` client, callback path, `session-ttl: 1h`, SQLite at
  `/data/gatus.db`, `gatus-data` volume, Dockerfile checksum, zero-fuzz patch
  and `go test`, and the entrypoint checks. Promoted.
- 0086 dependency version management matches `renovate.json5` (enabled
  managers, Monday schedule, 7 day age with `timestamp-optional`, no
  automerge), `.github/dependabot.yml` (npm for Storybook only),
  `sync-tech-stack-versions.sh` options `--check`, `--dry-run`, `--write`,
  `check-config-mount-hashes.py` options, `validate-docker-compose.sh` and
  `ImageTagPolicyTests`. Promoted. The guide link labelled as the Guide index
  pointed at the repository README; it now points at `guides/README.md`.
- 0100 development database matches `infra/04-data/dev-db/docker-compose.yml`:
  services, profiles, exporter ports 9187 and 9121 on `dev_data_net` and
  `obs_net` without host ports, monitor secret names, `archive_mode=on`,
  `archive_timeout=300`, `timescaledb`, and the `quality-results` perf job. The
  three unit test modules named in the runbook ran. Promoted.
- Static comparison proves declaration only. No runtime, backup, restore or
  login result is claimed for any promoted document.

#### Changed

- REQ-0027, AD-0031, AD-0032 and the nine Stage 05 documents: status,
  minor version and date.
- `docs/05.operations/guides/10-platform-and-backup/0086-dependency-version-management.md`:
  one link target.
- `docs/99.templates/registry.json`: `spec` high-water 261, next 262.
- `docs/03.specs/README.md`: index row.

#### Open issues

- RUN-0087 mentions "Task 0004" without a link; the text is historical and was
  left as is.
- Hosted CI has not run.
- REQ-0027 and the promoted documents are not Task package members, so their
  transitions are recorded under Decisions, not in Lifecycle Events.

#### Supersession note 2026-11-10

On 2026-11-10 the Dependabot references at lines 68 and 79 are superseded:
`.github/dependabot.yml` no longer exists and `renovate.json5` is the sole
dependency updater (PR #850, merge `87d3a18c8`). Earlier entries are unchanged.

#### Hosted CI evidence follow-up 2026-11-10

A read-only GitHub lookup on 2026-11-10 for the actual implementation commit
`a30e3598eb29bba094fbf76934d04eeac2b82858` returned CI Quality Gates run
[41780400564](https://github.com/buenhyden/hy-home.docker/actions/runs/41780400564)
with conclusion success. Job126410378613, `candidate-quality`, completed
successfully; `main-security` was skipped in that pull-request run. This
resolves E5's missing hosted-CI observation for that original candidate only.
The earlier unpushed/NOT_RUN text and E5 are preserved as dated history, not
rewritten. It does not prove the current source diff, runtime, backup, login,
restore, or a new owner acceptance. A fresh-context independent document
review and criteria1-4 owner decisions remain pending.

### Blockers and Decisions

None: nothing was recorded here before this Task moved to the common form.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | source-review | REQ-0027 edited, tree uncommitted on e3bdc5133 | PASS | status approved, draft sentence reworded | required | - |
| E2 | 2 | W2 | source-review | AD-0031 and AD-0032 against Compose and scripts | PASS | both promoted, see Decisions | required | - |
| E3 | 3 | W3 | source-review | nine Stage 05 documents against Compose, scripts and configuration | PASS | all promoted, see Decisions | required | - |
| E4 | 3 | W3 | unit-tests | `python3 -m unittest` for test_dev_pg_provision, test_dev_valkey_acl, test_dev_data_boundary; `docker compose --profile dev-data config --quiet` | PASS | 41 tests OK; compose exit 0 | required | - |
| E5 | 4 | W4 | hosted-ci | GitHub Actions | NOT_RUN | branch not pushed | required | - |
| E6 | 4 | W4 | metadata | `check-changed --base-ref origin/main` and `check-active`, package complete and staged on e3bdc5133 | PASS | selected 16, zero violations; selected 544, zero violations | required | - |
| E7 | 4 | W4 | corpus-lifecycle | `check-document-corpus-lifecycle.py --base-ref origin/main`, same tree | PASS | lifecycle zero, occupancy zero | required | - |
| E8 | 4 | W4 | operations-and-links | `check-operations-catalog.py`; links `alignment`, `navigation`, `language`, `traceability`, `entrypoint`, same tree | PASS | catalog PASS; every link mode PASS, 879 documents, 8109 links, zero failures | required | - |
| E9 | 4 | W4 | hosted-ci | Original implementation commit a30e3598eb29bba094fbf76934d04eeac2b82858 | PASS | Read-only 2026-11-10 lookup: run41780400564, candidate-quality job126410378613 success; main-security skipped | required | E5 |

### Resolution Links

None: nothing was recorded here before this Task moved to the common form.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |

### Remaining Conditions

Local checks are recorded above. The original candidate hosted-CI result is
now evidenced by E9. Hosted CI for the current diff, fresh-context independent
review and owner criterion decisions remain pending; no criterion is accepted
yet. Earlier unrun statements are preserved as the history they recorded.

## Handoff

### Promotion Receipt

None: nothing was recorded here before this Task moved to the common form.

### Next Owner

None: nothing was recorded here before this Task moved to the common form.
