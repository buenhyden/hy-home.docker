---
title: "D11 v9 Legacy and Temporary Cleanup Task"
version: "0.1.2"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0126"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-28"
---

# D11 v9 Legacy and Temporary Cleanup Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion183/W199 in the [Spec](../spec.md) and [Plan](../plan.md). Apply
D11 of the v9 task prompts: retire the cleanup targets the earlier prompts
handed to D11, only by exact identifier, after a consumer check, keeping
HOME data, backups and evidence.

##### Inputs and Authority

On 2026-11-28 the user directly requested D11 from
`_workspace/workspace_task_prompts_20261127_progress_v9/` (prompt
`11_legacy_secret_temp_cleanup.md`), limited to that prompt's scope, with
commit, push, PR and merge after checks. Asked in this chat, the owner
approved deleting the six superseded `sec01-n8n` candidate images, the two
superseded inner sandbox images, the probe workflow `d06e12CodeRunner01`,
the 188 empty dangling anonymous volumes and the four retired Kafka Connect
and Schema Registry topics. Work ran in the primary checkout on branch
`docs/d11-v9-cleanup` from `main` `f11c0350a`; brief `d11-v9` bound this Task
and the Spec and Plan rows. No secret value was read or printed. Direct user
authorization is authority; this record is not.

#### Execution Log

##### Work Performed

###### Candidates

| Candidate | Handed by | Runtime finding | Disposition |
| --- | --- | --- | --- |
| `sec01-n8n` candidate images 2.42.6 (three tags), 2.43.6 (`03892eb1a9a4`, `cd628778fccb`) and the replaced 2.49.7 `a92e6afbd3dd` | D09 (TSK-0052) | No container used them; about 12.5 GB | Removed by tag; the current reviewed candidate `2.49.7-opsflow-099418ca2fb4` stays |
| Inner sandbox images 1.15.0 (`008efc5a496e`, `sha256:d5084349…`) and 1.8.1 (`00daa6a14b72`, `sha256:b397f4b5…`) in `n8n-sandbox-runner-1` | D06 (TSK-0123) | No inner container; inner data root 25.9 GB | Removed by ID; only the pinned 1.16.0 `sha256:4b48ced7…` stays, data root 11.3 GB, runner and API healthy |
| n8n workflow `d06e12CodeRunner01` | D06 (TSK-0118), D09 (TSK-0052) | Inactive, not published, 3 nodes; D09 accepted the native runner replacement on 2.49.7 | Exported to `/home/hyunyoun/storage/volumes/backups/cleanup-20261128/d06e12CodeRunner01.json`, then one row deleted in a transaction (`DELETE 1`); workflows 13 to 12 |
| Kafka topics `_connect-configs`, `_connect-offsets`, `_connect-status`, `_schemas` | D08 (TSK-0046) | Kafka Connect and Schema Registry are no longer in HOME Compose; no consumer group exists | Deleted; `infra-events`, `application-logs` and `__consumer_offsets` stay, `kafka-1` healthy |
| 242 dangling anonymous volumes (created 2026-09-22 to 2026-11-09) | This census | 188 have no entries; 54 hold data: 28 PostgreSQL 18 directories (1.56 GB), Kafka logs, a SeaweedFS filer store, MongoDB and a Pyroscope store | The owner first approved removing the 188, then on 2026-11-28 the 54 as well. Each of the 54 was archived to `/home/hyunyoun/storage/volumes/backups/cleanup-20261128/vol-<id>.tgz` (gzip test passes for all); the ID lists are `empty-anonymous-volumes.txt` and `data-anonymous-volumes.txt` there. The native deny rule refused `docker volume rm` to the agent both times, so the owner runs the removal |
| `hy-home-infra_open-webui` volume | This census | 265 MB of Open WebUI data (`webui.db`, uploads, vector store, its secret key file); no container uses it, and Open WebUI runs only as a LAB | The owner approved its removal on 2026-11-28; archived to `/home/hyunyoun/storage/volumes/backups/cleanup-20261128/vol-hy-home-infra_open-webui.tgz` and listed in `data-anonymous-volumes.txt`; the owner runs the removal |
| `/tmp/hyhome-retained-n8n-2.49.7-attempt1-cc76d6c8` | D09 (TSK-0052) | Already absent | Nothing to do |
| Retired OpenBao KV values `hy-home/08-ai/open-webui`, `hy-home/12-analytics/superset` | D07 (TSK-0116) | Already deleted: TSK-0116 E27 records `Success! Data deleted` for both metadata paths with root on 2026-11-25, and E26 records the narrowed `renderer` policy write (`RENDERER_ROLES_APPLIED`) in the same window. Its Next Owner text and D11 row, which still name both as open, are stale; this row is the correction, since TSK-0116 is terminal | Nothing to do; not re-verified live because a read needs a token |

###### Owner command

```bash
cd /home/hyunyoun/storage/volumes/backups/cleanup-20261128
cat empty-anonymous-volumes.txt data-anonymous-volumes.txt \
  | grep -xF -f <(docker volume ls -q -f dangling=true) | xargs docker volume rm
```

The `grep` keeps only IDs that are still unattached; `docker volume rm` also
refuses a volume a container uses. A volume is restored with `docker volume
create <name>` and `tar -xzf vol-<name>.tgz` into it.

##### Blockers and Decisions

The agent could not remove any volume because the native deny rule covers
`docker volume rm`; the command above is the owner step for all 243 (188
empty, 54 data-bearing anonymous, Open WebUI). The two OpenBao KV values need
no step.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 183 | W199 | method=observation; tool=docker, psql, kafka-topics; command=container, image, volume and topic census; read-only alpine mount of the dangling volumes listing names and sizes only | HOME, 2026-11-28 | PASS | Candidates table | required | - |
| E02 | 183 | W199 | method=automated; tool=docker; command=docker image rm by tag; docker exec n8n-sandbox-runner-1 docker image rm by ID | Owner approval in this chat | PASS | Six host images and two inner images removed; current candidate and pinned 1.16.0 kept; runner and API healthy | required | - |
| E03 | 183 | W199 | method=automated; tool=n8n CLI, psql; command=n8n export:workflow; DELETE FROM workflow_entity in a transaction | Owner approval in this chat | PASS | Export saved; `DELETE 1`; 0 rows left for the ID; 12 workflows | required | - |
| E04 | 183 | W199 | method=automated; tool=kafka-topics; command=kafka-topics --delete for four topics | Owner approval in this chat | PASS | Topics gone, no consumer group, broker healthy | required | - |
| E05 | 183 | W199 | method=automated; tool=docker; command=docker volume rm of the 188 empty dangling volumes | Owner approval in this chat | NOT_RUN | Denied to the agent by the native deny rule; ID list written for the owner | required | - |
| E06 | 183 | W199 | method=automated; tool=docker, tar, gzip; command=read-only alpine mount and tar -czf of each of the 55 data-bearing volumes; gzip -t of each archive | Owner approval on 2026-11-28 | PASS | 55 archives, 513 MB, 0 corrupt | required | - |
| E07 | 183 | W199 | method=automated; tool=docker; command=docker volume rm of the 243 listed unattached volumes | Owner approval on 2026-11-28 | NOT_RUN | Denied again by the native deny rule; owner command above | required | - |
| E08 | 183 | W199 | method=automated; tool=docker; command=docker volume rm of the 188 empty dangling volumes | Owner run, observed 2026-11-28 | PASS | 0 of the 188 listed IDs remain; the 55 archived volumes are still present | required | E05 |

##### Resolution Links

E08 resolves E05: the owner removed the 188 empty volumes. E07 is resolved when the owner runs the command above for the 55 archived volumes and a new row records
the remaining dangling volume count.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 183 | pending | E01,E02,E03,E04,E05,E06,E07,E08 | Awaiting the owner volume removal and acceptance | @buenhyden |

##### Remaining Conditions

- The owner removes the 55 archived volumes with the command above; this Task
  then records it.
- 38 named dangling volumes outside both lists (stopped HOME services such as
  `kafka-2`/`kafka-3` and `open-notebook`, the pre-upgrade copies
  `grafana-data-pre-13.3.0` and `owui-prerollout-226`, and labs data) are not
  D11 targets and stay.

#### Handoff

##### Promotion Receipt

None: this Task records cleanup and routing only.

##### Next Owner

The owner runs the volume command and decides criterion183.
D12 runs next; no other prompt is started automatically.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
