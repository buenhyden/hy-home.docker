---
title: "Terrakube LAB Move Plan Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-26"
layer: "specs"
artifact_id: "SPEC-0263-TSK-0004"
parent_ids:
- "SPEC-0263-PLAN-0001"
created: "2026-11-26"
---

# Terrakube LAB Move Plan Task

## Scope

### Objective and Parent

#### Objective

Carry out the planning half of Plan work unit W9: record what moving
Terrakube from HOME (`infra/09-platform-ops/terrakube`) to `labs/terrakube/`
touches, which HOME data it leaves behind and which choices belong to the
owner, so that a later change can move it under this package's LAB contract.
This Task moves no file.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [LAB Promotion Contract Task](tsk-0001-lab-promotion-contract.md)
- [ADR-0062](../../../02.architecture/02.decisions/0062-home-lab-membership.md)

### Inputs and Authority

ADR-0062 item 9 makes Terrakube a LAB as its own change under this package,
and item 5 calls it the largest move. On 2026-11-26, after the D03 lifecycle
v8 review (SPEC-0212 TSK-0120) found its Valkey login without an ACL user, the
owner chose in chat to plan the move only and to start the move separately.

This Task starts, stops and recreates no container, reads no secret value and
edits nothing under `secrets/` or `labs/`.

## Execution Log

### Work Performed

#### Inventory

A read-only census on `main` `350d52d1f`, checked against the sources.

| Area | Current state |
| --- | --- |
| Services | `terrakube-api`, `terrakube-ui`, `terrakube-executor` (2.33.3, digest pinned), profile `iac`, not running in HOME; routes `terrakube-api`, `terrakube-ui` and `terrakube-executor` behind `gateway-standard-chain`, `sso-errors` and `sso-auth`; networks `edge_net`, `terrakube_net`, `terrakube_ui_ingress_net`, `mng_data_net`, `object_net`; no named volume |
| Docker socket | The executor binds `/var/run/docker.sock` read-write; `lab.py check` refuses any LAB Docker socket bind |
| Secrets | `terrakube_db_password` (PG-010), `seaweedfs_s3_terrakube_secret_key` (STRG-014), `terrakube_valkey_password` (CACHE-010), `terrakube_internal_secret` (AUTO-007), `terrakube_pat_secret` (AUTO-008); `TERRAKUBE_DB_USERNAME` (PG-009); the OIDC client is the shared oauth2-proxy client (IAM-003) |
| `_FILE` keys | `infra/secret-file-support.json` records every Terrakube `_FILE` key as unsupported (Spring reads plain environment values), so the mounted secret files are probably not read today |
| HOME mng-pg | Role and database `terrakube` from `init_users_dbs.sql`, password through mng-pg-init; `test_mng_pg_init_sql` lists it |
| HOME mng-valkey | Login with `terrakube_valkey_password`, but `render-acl.sh` has no terrakube user, so the login cannot succeed |
| HOME SeaweedFS | Bucket `tfstate` from `seaweedfs-buckets`; identity `terrakube` with Read, Write and List on `tfstate` |
| Observability and backup | No Prometheus, Gatus or Alloy target and no Restic set |
| Pinned elsewhere | Root `docker-compose.yml` include, networks and secrets; Traefik `terrakube_ui_ingress_net`; update ledger rows, `verification.json`, `release-lookups.json`, a stale `terrakube-ui:2.33.2` lookup in `image-source-lookups.json`; `tech-stack.versions.json`; `check-all-hardening.sh` tier 09 loop; `test_infra_tier_layout`, `test_p02_service_contracts`, `test_compose_baseline_gates`, `test_mng_pg_init_sql`; `.env.example`; READMEs; GDE, POL and RUN 0069 with 0060, 0063, 0082, 0021, 0099, 0079, 0024, 0028 cross-references; POL-0006; POL-0078 `iac` and inventory rows; the m0021 service inventory |

#### Move file set

Following the Open WebUI move (`3fc3f3399`), the move change would touch:
`labs/terrakube/` (Compose, README, `promotion.yaml`, an entrypoint that
exports the secret files as environment values), `labs/README.md`,
`labs/.env.example`, the root Compose include, networks and secrets, Traefik's
UI network, the update ledger (`historical_lab_entries`), `verification.json`,
`release-lookups.json`, `tech-stack.versions.json`, `secret-file-support.json`,
the OpenBao catalog rows (new `LAB-0xx` rows and `secrets/labs/terrakube/`
copies), `check-all-hardening.sh` and the LAB test tuples, the HOME tests
listed above, GDE, POL and RUN 0069 moved to `15-labs` with their
cross-references, POL-0006, POL-0078, ADR-0062 and the m0021 inventory.

### Blockers and Decisions

The move waits for these owner choices:

| No. | Choice | Options | Note |
| --- | --- | --- | --- |
| 1 | Executor Docker socket | Drop it, or record a LAB exception | `lab.py check` refuses it as is |
| 2 | HOME data stores | Keep mng-pg, mng-valkey and SeaweedFS as required endpoints like the SonarQube LAB, or give the LAB its own stores | A LAB joins no HOME network, so the endpoint path must be chosen |
| 3 | Valkey | Add a terrakube ACL role, drop Valkey, or use a LAB-local Redis | Broken today |
| 4 | OIDC and routes | Own client (`home-terrakube` per the Compose comment) or none; keep or drop gateway routes | ADR-0062 item 7 lists Terrakube behind the chain, but LABs normally have no route; the executor needs an API URL |
| 5 | HOME leftovers | Keep or retire the `terrakube` role and database, the `tfstate` bucket and identity, and the five secrets | Any existing state needs export or retention first |
| 6 | Runtime cleanup | Containers, DNS and Keycloak entries | A separately approved runtime step |

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 1, 3 | W9 | method=review; tool=git grep, graphify; command=read-only census of Terrakube sources, references and HOME dependencies | `main` `350d52d1f`, 2026-11-26 | PASS | Inventory and file set above; the Docker socket bind and the `_FILE` support records were read at their sources | required | - |

### Resolution Links

None: no row resolves another.

## Acceptance Decision

### Criterion Decisions

None: each criterion already carries its one decision (1, 2, 4 and 6
accepted in TSK-0001; 3 not-required in TSK-0003; 5 and 7 not-required in
TSK-0001; 8 not-required in TSK-0002). This Task adds evidence for the
Terrakube move and decides no criterion.

### Remaining Conditions

The owner choices under Blockers and Decisions, then the move change itself,
whose LAB, secret, catalog, hardening, render, document and hosted checks
become this Task's evidence.

## Handoff

### Promotion Receipt

None: this Task records a plan and promotes no long-lived rule.

### Next Owner

@buenhyden makes the choices above and starts the move change, which records
its work and evidence here.
