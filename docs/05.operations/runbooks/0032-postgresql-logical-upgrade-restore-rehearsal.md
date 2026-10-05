---
title: "PostgreSQL Logical Upgrade and Restore Rehearsal Runbook"
version: "1.0.5"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0032"
created: "2026-07-22"
---

# PostgreSQL Logical Upgrade and Restore Rehearsal Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

이 런북은 repository-owned synthetic fixture를 source PostgreSQL image에서 custom-format logical backup으로 캡처하고 target-major isolated image에 복원한 뒤 metadata-only oracle을 비교하는 로컬 rehearsal 절차다. 이 결과는 rollback boundary evidence이며 production recovery, live Supabase/Spilo data, physical backup, PITR, HA, retention, remote storage 또는 조직 RTO/RPO를 증명하지 않는다.

이 문서는 `infra/04-data`의 새 service를 설명하지 않는다. 실제 구현은 repository operation entrypoint와 `examples/operations/postgres-logical-upgrade/`에 있는 reusable non-service harness다.

### When to Use

- PostgreSQL source/target image pin, fixture, oracle, wrapper, or recovery boundary가 바뀐 뒤 local representative evidence를 갱신할 때
- Backup capture와 restore/integrity를 별도 gate로 검증해야 할 때
- Checksum mismatch, partial state, bad target major, 또는 timeout cleanup 동작을 재검증할 때

### Trigger and Preconditions

| 실행 계기 | 전제 조건 | 안전 조건 |
| --- | --- | --- |
| PostgreSQL pin 또는 logical recovery wrapper 변경 후 representative rehearsal | Docker Compose와 exact Plan/Task approval | synthetic SQL만 사용; source/target image pin은 연결된 harness source가 소유함; host port, bind mount, external network, named/shared volume, `${DEFAULT_DATA_DIR}`, raw log, row, 비밀번호, dump evidence 없음 |

Task 2의 local runtime handoff SHA-256 `7b95d095764ede50585e8aa267483539c39e652e94a911bdc84fabb416ee6edf`는 readiness semantics boundary를 설명하는 upstream evidence일 뿐 이 데이터 복구 rehearsal의 operational prerequisite가 아니다. 이 런북은 그 handoff의 존재 또는 내용에 의존하지 않는다.

### Scope separation from actual HA recovery

이 harness는 `examples/`의 digest-pinned PostgreSQL17.11→18.4와 fixture 한 DB만 다룬다. `--no-owner --no-acl`이며 globals/전체 DB/extension inventory/Patroni/etcd/pg-router를 복원하지 않는다. [RUN-0031](0031-postgresql-cluster.md)의 실제 HA 계약을 만족시키거나 HOME restore를 승인하지 않는다. 아래2026-07-22 기록은 그 날짜의 synthetic evidence이며 현재 source pin에 대한 새 runtime 관측이 아니다. 이미 검증된 exact-owner cleanup만 wrapper가 소유하고, 일반 실패 target 자동 삭제로 범위를 확장하지 않는다.

## Procedure

### Procedure

| 단계 순서 | 실행 절차 | 기대 결과 |
| --- | --- | --- |
| 1 | `python3 -m unittest tests.validation.test_postgres_logical_upgrade_rehearsal -v` | fixture, shell contract, negative case, cleanup, redaction, verdict 테스트가 통과한다. |
| 2 | `bash scripts/operations/rehearse-postgres-logical-upgrade.sh --check-config-only` | 완전히 기계 판독 가능한 Compose render, 정확한 pin, anonymous approved target, fixture SHA-256, 배타적 UID/mode/device/inode evidence ownership, 360초 operation budget, 60초 cleanup reserve가 database를 시작하지 않고 하나의 420초 deadline 안에서 통과한다. |
| 3 | `bash scripts/operations/rehearse-postgres-logical-upgrade.sh` | source와 target 각각이 TCP `127.0.0.1:5432`에서 동일한 인증된 postmaster identity를 2초 간격으로 두 번 증명하는 동안 컨테이너가 계속 실행되고 healthy 상태를 유지하며, 별도의 정확한 project render가 이어서 backup, restore, oracle 비교, cleanup, atomic canonical publication을 통과한다. |
| 4 | `--negative-case checksum-mismatch`, `partial-state`, `bad-target-major`, `timeout`을 각각 실행한다. | 안정적인 nonzero class `50`, `50`, `10`, `20`; cleanup 통과; 각 negative 이후 canonical handoff가 존재하지 않는다. |
| 5 | readiness 동작이 바뀌면 negative case 이후 정상 명령을 연속으로 두 번 실행한다. | 두 실행 모두 안정적인 인증된 readiness를 통과하며, 검증된 cleanup 이후에만 두 번째의 새로운 정확한 12-key canonical handoff가 게시된다. |

## Verification

### Verification Record

| 검증 환경 | 명령 또는 절차 | 결과 | 증거 위치 |
| --- | --- | --- | --- |
| Local isolated Docker, 2026-07-22 | 정확한 focused suite와 `--check` | historical RED 7/31 및 1/1; second-review RED 7개 method에 걸친 13개 assertion; terminal-review RED 8개 direct-control subcase; 최종 41/41 통과; fixture SHA-256 `b8d5421bba8fb32a1be3d485660f7d0cc018405e1cf7f2564f653bf0dd725460` | Infrastructure Task |
| Local isolated Docker, 2026-07-22 | reviewer invalidation 이후 단일 승인된 final-state 정상 rehearsal | project `hyhome-ior-20260719-229164-source/target`가 인증된 TCP readiness, integrity, cleanup, redaction을 통과함; fixture SHA-256 `b8d5421bba8fb32a1be3d485660f7d0cc018405e1cf7f2564f653bf0dd725460`; 보존된 dump SHA-256 `090b92324621b40e87355d705483e2ac66c027ac3fed2940b588a525cdaae6f3`, 4,484 bytes; backup 1s; restore 0s; owned resource 없음 | 무시된 정확한 12-key, mode-0600 canonical `recovery-verdict.json`, SHA-256 `c5f9e3a135d032e480c4484a5c545486f461562fc327923c9e4a3887f2883899`; schema 1; scope `synthetic-local`; integrity, cleanup, redaction 통과; 이후 canonical-mutating 명령 없음 |
| Local isolated Docker, 2026-07-22 | 네 개의 negative 명령 | 기대 class `50/50/10/20`; cleanup 통과; canonical 잔존 없음 | Infrastructure Task |

### Evidence

기록 가능한 evidence는 image pins, fixture/dump SHA-256, dump byte size, aggregate oracle status, observed local timing, stable exit class, cleanup/redaction status, project identity, commit, and review verdict로 제한한다. Password, environment value, SQL row, raw dump, raw database/Compose log, query output 또는 remote location은 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

실패 시 wrapper가 정확한 task project와 labeled dump client, anonymous volumes, exclusively created PID-scoped `/tmp`만 제거한다. `/tmp`가 사전에 존재하거나 symlink이거나 retained UID/mode/device/inode identity가 달라지면 그 경로를 읽거나 변경하지 않고 canonical을 게시하지 않는다. Cleanup은 client, target, source, network, volume, temporary artifact를 독립적으로 끝까지 시도하고 실패를 누적하며, 남은 deadline 안에서 exact owner만 idempotent retry할 수 있다. 구현 rollback은 logical commit revert로 제한하며 live/shared database를 삭제하거나 `docker system prune`을 실행하지 않는다.

### Escalation

Image pin drift, project collision, unexpected target, integrity mismatch, partial state, cleanup failure, secret/raw-payload exposure, live/shared path 발견 시 즉시 중단하고 data owner와 operations/security reviewer에게 에스컬레이션한다. Production recovery 또는 physical/PITR/HA/remote scope가 필요하면 새 Stage 01-04 승인 chain을 만든다.

### Automation Handoff

| 자동화 후보 또는 호출 | 사람·운영자가 판단할 경계 |
| --- | --- |
| `scripts/operations/rehearse-postgres-logical-upgrade.sh` normal/check-config-only/negative envelope | canonical verdict는 local synthetic rollback boundary일 뿐 deployment gate가 아니다. pin, data class, storage, cleanup, remote, live target 변경은 새 승인 없이 자동화하지 않는다. |

### Traceability

- Governing authority: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peer: 없음 — 번호 `0032`를 공유하는 Guide나 Policy가 없다.

## Related Documents

- Runtime pin: Compose/Dockerfile 선언이 authoritative이며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

- Spec 125
- Infrastructure Plan
- Infrastructure Task
- [Rehearsal operation](../../../scripts/operations/rehearse-postgres-logical-upgrade.sh)
- [Synthetic Compose example](../../../examples/operations/postgres-logical-upgrade/docker-compose.yml)
- [Relational runbook index](README.md)
- [HA cluster triage runbook](0031-postgresql-cluster.md)
