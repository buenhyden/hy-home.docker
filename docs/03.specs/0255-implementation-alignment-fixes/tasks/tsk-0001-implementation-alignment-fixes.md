---
title: "Implementation Alignment Fixes Task"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0255-TSK-0001"
parent_ids:
- "SPEC-0255-PLAN-0001"
created: "2026-11-04"
---

# Implementation Alignment Fixes Task

## Scope

### Objective and Parent

#### Objective

Correct the verified discrepancies between current documents and the
implementation that no open branch owns.

- [Spec](../spec.md)
- [Plan](../plan.md)

### Inputs and Authority

The user directed that README, AGENTS.md, `.agents/`, `.claude/`, `.codex/`
and the documents under `docs/01.requirements`, `docs/02.architecture`,
`docs/05.operations` and `docs/99.templates` be checked against the current
implementation and corrected ("현재에 맞게 수정하고 보완한다"), and later added
"ADR-0011, Deleted Spec references, Missing owners도 포함하여 처리. Not checked
처리." Findings come from three read-only audits run on main 4adeb3d37. This
Task pushes and merges nothing; the coordinator pushes the branch and opens
the pull request, and the user merges.

## Execution Log

### Work Performed

#### Current contract decision

The user's direction authorizes this Spec and Plan as written.

#### Current readiness and execution

Inputs, work units and checks are recorded here. The Task is ready and in
progress under the approved parents. Hosted CI has not run.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0255 | draft | approved | #current-contract-decision |
| SPEC-0255-PLAN-0001 | draft | approved | #current-contract-decision |
| SPEC-0255-TSK-0001 | draft | ready | #current-readiness-and-execution |
| SPEC-0255-TSK-0001 | ready | in-progress | #current-readiness-and-execution |

#### Decisions

- Open branches own other findings: SPEC-0252 (Registry, Stage 01–03
  lifecycles, ADR-0011), SPEC-0253 (pre-commit, hook, gate evidence owner,
  DATA-0096) and SPEC-0254 (infra README links, workflow-contract routing,
  ADR-0002, folder guides). Those files are not edited here; see Batch 2.
- Pact Broker and Great Expectations already have requirement and
  architecture owners (REQ-0010 and AD-0009 and ADR-0046; REQ-0005 FR-0006,
  AD-0012 and ADR-0045, with POL/GDE/RUN-0094 as Great Expectations' operations
  owner). The audit searched by directory name; no new owner is needed. AD-0009
  gains the Pact Broker operations link it lacked.
- References to deleted Specs: 263 citations outside excluded paths were
  scanned (Stage 03 bodies, Stage 90 dated research and infra READMEs
  excluded). ADR-0051 decision 6 lets prose name a retired identity to explain
  lineage, so past-tense and provenance citations stay. Present-tense
  ownership or pointer citations are rewritten (table below). ADR-0037 lines
  35 and 41 are decision-body text of an accepted ADR and stay.
- The SonarQube image reads only `SONAR_JDBC_PASSWORD`; its README now says
  the entrypoint exports it from `sonarqube_db_password`.
- POL-0021's management database list now follows the init script, MLflow
  provisioning and the catalog's pre-existing `app_db`.
- Secret names are added only where an owning document already keeps a
  secret list (POL-0028, GDE-0053). Values are never read.
- The Spec number 255 follows the open branches' claims (0252, 0253, 0254).
  After PR #729 merged (Spec high-water 253), the Registry `spec` high-water
  moved to 255 and `next_number` to 256 in this change; 254 stays claimed by
  the open SPEC-0254 branch. That is the only Registry edit here.
- REQ-0023-FR-0002 required every subnet to be a root-owned `10.250.x.0/24`,
  while the leaf-owned `crawl4ai_egress_net` is `10.250.200.0/29`. The user
  decided on 2026-11-04 to keep the implementation and grant a named exception:
  FR-0002 and its acceptance line now allow a small, leaf-owned, internal
  egress-isolation network declared in its own Compose file, naming
  `crawl4ai_egress_net` as the one exception, with no new child ID. AD-0026
  marks the row.

##### Deleted Spec reference decisions

| Location | Citation | Decision |
| --- | --- | --- |
| `decisions/README.md` (ADR-0037, ADR-0048 entries) | SPEC-0179 / SPEC-0236 "owns implementation" | rewritten: implemented, deleted |
| AD-0011:21 | capabilities "under SPEC-0197" | rewritten: SPEC-0197 moved them, retired |
| AD-0030:128 | SPEC-0173-TSK-0006 "owns" cleanup evidence | rewritten: recorded, retired |
| AD-0026 heading | "Networks (SPEC-0180 S05)" | heading renamed; GDE-0077 anchor updated |
| GDE-0100:84 | evidence "is in" SPEC-0202-TSK-0002 | rewritten: recorded, deleted |
| GDE-0064:106 | "current SPEC-0203" verification | rewritten: recorded by deleted SPEC-0203 |
| POL-0100:20 and policies README | SPEC-0202 "preserved" evidence | rewritten: deleted Spec, version history |
| POL-0085:111 | window "(SPEC-0243, …)" | rewritten: RUN-0105 owns; SPEC-0243 introduced it |
| RUN-0085:193 | decision "(SPEC-0242)" | rewritten: decided in SPEC-0242, deleted |
| RUN-0100:46 | "follows SPEC-0202-TSK-0002 evidence" | rewritten: evidence left by deleted Task |
| RUN-0105:345 | custody record "(SPEC-0242)" | rewritten: links the custody procedure section |
| RUN-0021:261 | "SPEC-0201-TSK-0002's proposed path" | rewritten: branch proposed there, deleted |
| REQ-0005:45, :92 | SPEC-0180 "owns" with POL-0094 | rewritten: POL-0094 sole owner, SPEC-0180 retired |
| `.agents/knowledge/repository-map.md:101` | path into deleted SPEC-0211 | rewritten: ID and commit kept, path removed |
| ADR-0037:35, :41 | SPEC-0179 "records" / "owns" | kept: accepted decision body |
| remaining citations | past events, provenance parentheticals | kept: lineage prose (ADR-0051 D6) |

#### Changed

- `docs/02.architecture/descriptions/0026-standardize-infra-net.md`: ten
  network rows added or corrected (`dev_data_net`, `experience_ingress_net`,
  `redisinsight_ingress_net`, `seaweedfs_metrics_net`, `n8n_blog_ingest_net`,
  `blog_export_net`, both n8n runner networks, `crawl4ai_net`,
  `crawl4ai_egress_net`, `crawl4ai_outbound_net`); heading renamed.
- `docs/05.operations/guides/02-gateway-and-networking/0077-ip-address-management.md`:
  anchor updated.
- `docs/05.operations/policies/01-common/0004-harness-agent-first-engineering.md`:
  scope globs.
- `docs/01.requirements/0005-data-analytics.md`: ownership.
- `docs/02.architecture/descriptions/0009-tooling-architecture.md`: Related
  Documents deduplicated; Pact Broker link added.
- The deleted-Spec rewrites in the table above.
- `docs/05.operations/policies/10-platform-and-backup/0021-backup-and-restore.md`:
  management database list.
- `infra/11-quality/sonarqube/README.md`: `SONAR_JDBC_PASSWORD` key.
- `docs/05.operations/policies/05-databases-and-storage/0028-management-database.md`
  and `docs/05.operations/guides/08-workflows-and-automation/0053-n8n.md`:
  secret names.
- `_workspace/README.md`: agent audience entry removed.
- `README.md`: pointer to `AGENTS.md` for agent working rules.
- `docs/01.requirements/0023-standardize-infra-net.md`: FR-0002 named
  exception (version 1.2.0).
- `docs/99.templates/registry.json`: `spec` high-water 255, `next_number` 256.

#### Open issues

##### Batch 2 (after the open branches merge)

- 249 backticked operations paths without their domain folder in 46 infra
  READMEs and the root README (SPEC-0254 edits infra READMEs).
- `infra/06-observability/grafana/README.md:84` links a Compose file that is
  in the parent folder.
- `infra/09-platform-ops/README.md:36-37` agent audience entries.
- Registry `root_exceptions` (SPEC-0123 path) and `inventory_excludes`
  (AUD-0023 path) point at missing files (SPEC-0252 edits the Registry).
- Secret names with no owning secret list: the oauth2-proxy, airflow and n8n
  monitor ACL overlays; `dev-db` admin, platform and inspector names; the
  RedisInsight inspector names; four SeaweedFS keys; `grafana_reader_password`;
  `pact_broker_db_password`; `dbt_db_password`; `superset_db_password` and
  `superset_secret_key`; `seaweedfs_s3_lakehouse_secret_key` for Flink, Spark
  and Trino. Their owning documents mention credentials only in prose, so
  adding them needs a decision on where each list lives.

##### Other

- ADR-0040:28-29 names the retired `service_valkey_password` inside an
  accepted decision; left as history.

### Blockers and Decisions

None: nothing was recorded here before this Task moved to the common form.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 3 | W3 | metadata-changed | `check-changed --base-ref origin/main` on the content edits, before this package, uncommitted tree on 4adeb3d37 | PASS | selected 18, zero violations | required | - |
| E2 | 3 | W3 | document-links | links `alignment`, `navigation`, `language`, `traceability` on the content edits, same tree | PASS | 864 documents, 8091 links, zero failures in each mode | required | - |
| E3 | 4 | W4 | metadata-changed | `check-changed --base-ref origin/main`, full batch-1 tree with this package, uncommitted on 4adeb3d37 | FAIL | selected 26; one violation: `identity-allocation-not-advanced` for SPEC-0255, because the Registry Spec high-water stays 251 in this batch; batch 2 advances it after SPEC-0252 merges | required | - |
| E4 | 4 | W4 | metadata-active | `check-active`, same tree | PASS | selected 497, zero violations | required | - |
| E5 | 4 | W4 | corpus-lifecycle | `check-document-corpus-lifecycle.py`, same tree | PASS | lifecycle zero, occupancy zero | required | - |
| E6 | 4 | W4 | operations-and-links | `check-operations-catalog.py`; links `alignment`, `navigation`, `language`, `traceability`, same tree | PASS | operations catalog PASS; every link mode PASS | required | - |
| E7 | 4 | W4 | hosted-ci | GitHub Actions | NOT_RUN | branch not pushed | required | - |
| E8 | 4 | W4 | metadata-changed | `check-changed --base-ref origin/main` after the rebase onto 46a7811dd (PR #729) with the Spec allocation and REQ-0023 edits, uncommitted on 1d8d35205 | PASS | selected 27, zero violations | required | E3 |
| E9 | 4 | W4 | metadata-active | `check-active`, same tree | PASS | selected 497, zero violations | required | - |
| E10 | 4 | W4 | corpus-lifecycle | `check-document-corpus-lifecycle.py`, same tree | PASS | lifecycle zero, occupancy zero | required | - |
| E11 | 4 | W4 | operations-and-links | `check-operations-catalog.py`; links `alignment`, `navigation`, `language`, `traceability`, same tree | PASS | operations catalog PASS; every link mode PASS | required | - |

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

Local checks are recorded above. Independent review and hosted CI have not
run, and no criterion is accepted yet.

#### Merge receipt 2026-11-10

Recorded 2026-11-10 from `gh pr view`: #732 merge `b56fd4480` at
2026-11-04T03:15:49Z. Hosted checks on the merged PR: every completed check
SUCCESS, the rest SKIPPED, none failing. Candidate quality: the merged change
is a candidate that passed hosted CI. This receipt is not owner acceptance: no
criterion is accepted and the status is unchanged.

## Handoff

### Promotion Receipt

None: nothing was recorded here before this Task moved to the common form.

### Next Owner

None: nothing was recorded here before this Task moved to the common form.
