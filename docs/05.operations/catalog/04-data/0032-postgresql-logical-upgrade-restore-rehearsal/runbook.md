---
profile_id: runbook
status: active
artifact_id: runbook-0032
artifact_type: runbook
parent_ids: []
created: 2026-07-22
updated: 2026-08-11
---

# PostgreSQL Logical Upgrade and Restore Rehearsal Runbook

## Overview

이 런북은 repository-owned synthetic fixture를 PostgreSQL 17.6에서 custom-format logical backup으로 캡처하고 PostgreSQL 18.4 isolated target에 복원한 뒤 metadata-only oracle을 비교하는 로컬 rehearsal 절차다. 이 결과는 rollback boundary evidence이며 production recovery, live Supabase/Spilo data, physical backup, PITR, HA, retention, remote storage 또는 조직 RTO/RPO를 증명하지 않는다.

이 문서는 `infra/04-data/relational`의 새 service를 설명하지 않는다. 실제 구현은 repository validation wrapper와 `tests/fixtures/postgres-logical-upgrade/`에 있는 task-scoped non-service harness이며, 문서 구현 정렬 validator도 이 정확한 stem 하나만 `NON_SERVICE_STEMS`로 분류한다.

## When to Use

- PostgreSQL source/target image pin, fixture, oracle, wrapper, or recovery boundary가 바뀐 뒤 local representative evidence를 갱신할 때
- Backup capture와 restore/integrity를 별도 gate로 검증해야 할 때
- Checksum mismatch, partial state, bad target major, 또는 timeout cleanup 동작을 재검증할 때

## Trigger and Preconditions

| Trigger | Prerequisites | Safety conditions |
| --- | --- | --- |
| PostgreSQL pin 또는 logical recovery wrapper 변경 후 representative rehearsal | Docker Compose와 exact Plan/Task approval | Synthetic SQL only; exact 17.6/18.4 image pins; no host port, bind mount, external network, named/shared volume, `${DEFAULT_DATA_DIR}`, raw log, row, password, or dump evidence |

Task 2의 local runtime handoff SHA-256 `7b95d095764ede50585e8aa267483539c39e652e94a911bdc84fabb416ee6edf`는 readiness semantics boundary를 설명하는 upstream evidence일 뿐 이 데이터 복구 rehearsal의 operational prerequisite가 아니다. 이 런북은 그 handoff의 존재 또는 내용에 의존하지 않는다.

## Procedure

| Step order | Procedure step | Expected result |
| --- | --- | --- |
| 1 | `python3 -m unittest tests.lib.ops.test_postgres_logical_upgrade_rehearsal -v` | Fixture, shell contract, negative cases, cleanup, redaction, and verdict tests pass. |
| 2 | `bash scripts/lib/ops/rehearse-postgres-logical-upgrade.sh --check` | Full machine-readable Compose render, exact pins, anonymous approved targets, fixture SHA-256, exclusive UID/mode/device/inode evidence ownership, 360-second operation budget, and 60-second cleanup reserve pass inside one 420-second deadline without starting a database. |
| 3 | `bash scripts/lib/ops/rehearse-postgres-logical-upgrade.sh` | Source and target each prove the same authenticated postmaster identity over TCP `127.0.0.1:5432` twice, two seconds apart, while the container remains running and healthy; separate exact-project renders then pass backup, restore, oracle comparison, cleanup, and atomic canonical publication. |
| 4 | Run `--negative-case checksum-mismatch`, `partial-state`, `bad-target-major`, and `timeout` separately. | Stable nonzero class `50`, `50`, `10`, and `20`; cleanup passes; canonical handoff is absent after each negative. |
| 5 | Run the normal command twice consecutively after negative cases when readiness behavior changes. | Both runs pass stable authenticated readiness; the second fresh exact 12-key canonical handoff is published only after verified cleanup. |

## Verification Record

| Verification environment | Command or procedure | Result | Evidence location |
| --- | --- | --- | --- |
| Local isolated Docker, 2026-07-22 | Exact focused suite and `--check` | Historical RED 7/31 and 1/1; second-review RED 13 assertions across 7 methods; terminal-review RED 8 direct-control subcases; final 41/41 passed; fixture SHA-256 `b8d5421bba8fb32a1be3d485660f7d0cc018405e1cf7f2564f653bf0dd725460` | Infrastructure Task |
| Local isolated Docker, 2026-07-22 | Single approved final-state normal rehearsal after reviewer invalidation | Project `hyhome-ior-20260719-229164-source/target` passed authenticated TCP readiness, integrity, cleanup, and redaction; fixture SHA-256 `b8d5421bba8fb32a1be3d485660f7d0cc018405e1cf7f2564f653bf0dd725460`; retained dump SHA-256 `090b92324621b40e87355d705483e2ac66c027ac3fed2940b588a525cdaae6f3`, 4,484 bytes; backup 1s; restore 0s; zero owned resources | Ignored exact 12-key, mode-0600 canonical `recovery-verdict.json`, SHA-256 `c5f9e3a135d032e480c4484a5c545486f461562fc327923c9e4a3887f2883899`; schema 1; scope `synthetic-local`; integrity, cleanup, and redaction passed; no later canonical-mutating command |
| Local isolated Docker, 2026-07-22 | Four negative commands | Expected classes `50/50/10/20`; cleanup passed; no canonical remained | Infrastructure Task |

## Evidence

기록 가능한 evidence는 image pins, fixture/dump SHA-256, dump byte size, aggregate oracle status, observed local timing, stable exit class, cleanup/redaction status, project identity, commit, and review verdict로 제한한다. Password, environment value, SQL row, raw dump, raw database/Compose log, query output 또는 remote location은 기록하지 않는다.

## Rollback or Recovery

실패 시 wrapper가 정확한 task project와 labeled dump client, anonymous volumes, exclusively created PID-scoped `/tmp`만 제거한다. `/tmp`가 사전에 존재하거나 symlink이거나 retained UID/mode/device/inode identity가 달라지면 그 경로를 읽거나 변경하지 않고 canonical을 게시하지 않는다. Cleanup은 client, target, source, network, volume, temporary artifact를 독립적으로 끝까지 시도하고 실패를 누적하며, 남은 deadline 안에서 exact owner만 idempotent retry할 수 있다. 구현 rollback은 logical commit revert로 제한하며 live/shared database를 삭제하거나 `docker system prune`을 실행하지 않는다.

## Escalation

Image pin drift, project collision, unexpected target, integrity mismatch, partial state, cleanup failure, secret/raw-payload exposure, live/shared path 발견 시 즉시 중단하고 data owner와 operations/security reviewer에게 에스컬레이션한다. Production recovery 또는 physical/PITR/HA/remote scope가 필요하면 새 Stage 01-04 승인 chain을 만든다.

## Automation Handoff

| Automation candidate or invocation | Human or operator judgment boundary |
| --- | --- |
| `scripts/lib/ops/rehearse-postgres-logical-upgrade.sh` normal/check/negative envelope | Canonical verdict는 local synthetic rollback boundary일 뿐 deployment gate가 아니다. Pin, data class, storage, cleanup, remote, or live target 변경은 새 승인 없이 자동화하지 않는다. |

## Related Documents

- Spec 125
- Infrastructure Plan
- Infrastructure Task
- [Rehearsal wrapper](../../../../../scripts/lib/ops/rehearse-postgres-logical-upgrade.sh)
- [Synthetic Compose fixture](../../../../../tests/fixtures/postgres-logical-upgrade/docker-compose.yml)
- [Relational runbook index](../README.md)
- [HA cluster triage runbook](../0031-postgresql-cluster/runbook.md)
