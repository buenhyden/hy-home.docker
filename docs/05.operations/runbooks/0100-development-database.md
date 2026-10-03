---
title: "Development Database Source Preflight Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "RUN-0100"
parent_ids:
- "GDE-0100"
created: "2026-10-03"
---

# Development Database Source Preflight Runbook

## When to Use

`dev-db` source change를 검토하거나 runtime execution request를 준비할 때 사용한다.
현재 완료 범위는 소스 통합·정적 검증, 신규 dev/LAB 비밀 파일 20개 발급과
합성 격리 엔진의 기동·권한·오프라인 백업·별도 볼륨 복원이다(SPEC-0202-TSK-0002).
HOME 배포·기동·정지·재시작, 외부 프로젝트 계정 발급, 실데이터 이관,
운영 백업 검증·복원은 `NOT_RUN`이며 각각 별도 구체적 승인이 필요하다.

## Procedure

저장소 root에서 working tree와 intended source를 확인한다. private `.env`, secret value,
rendered private Compose와 database content는 출력하지 않는다.

```bash
docker compose --env-file .env.example --profile dev-data config --quiet
python3 -m unittest tests.validation.test_dev_pg_provision tests.validation.test_dev_valkey_acl tests.validation.test_dev_data_boundary
```

두 명령이 exit 0이면 source profile, secret reference, static project grant/ACL contract가
일관됨을 기록한다. 이미지 빌드·컨테이너 health·확장 로드·격리 복원은 별도
SPEC-0202-TSK-0002 증거를 따른다. 이 정적 명령만으로 HOME 도달성, WAL archive,
운영 복원 성공을 주장하지 않는다.

runtime request가 있으면 실행 전에 승인된 Docker context, project name, ports, networks,
volumes, bind paths, UID/GID, resource budget, exact cleanup 대상과 rollback target을
읽기 전용으로 재확인한다. `down -v`, volume prune, 기존 management state 재연결, retention
축소, credential rotation은 이 runbook의 source-only 단계에서 금지한다.

외부 project provision은 manifest의 `project_id`, explicit DB/role, Valkey ACL prefix,
secret reference, quota와 approval state가 승인된 뒤에만 별도 task에서 실행한다. 앱 migration은
외부 workspace가 소유한다.

## Evidence

Task에는 source SHA, changed paths, 명령, exit code, 실행 시각, 정적·격리 결과와
운영 `NOT_RUN` 경계를 각각 기록한다. secret 값, private file 내용, raw log, DB row,
resolved mount path는 기록하지 않는다.

## Rollback or Recovery

source 문제는 runtime mutation 전에 source patch를 되돌려 static checks를 재실행한다.
runtime activation 뒤의 rollback은 해당 승인 task의 preserved volume, compatible image,
consumer impact와 recovery point를 사용한다. source rollback은 schema, data, ACL 또는
credential rollback을 보장하지 않는다.

## Escalation

Compose render failure, ambiguous project identity, secret/mount ownership drift, host port/network
collision, insufficient resource evidence, unsupported image/extension/backup compatibility,
grant isolation failure, current management dependency 발견 시 중단하고 @buenhyden에게
target, source SHA, failure signal, proposed approval boundary를 전달한다.

## Traceability

- Artifact: `RUN-0100`; parent guide: `GDE-0100`.
- Governing source contract: `SPEC-0202`.
- Static implementation authority: `infra/04-data/dev-db/docker-compose.yml`.

## Related Documents

- [Development database guide](../guides/0100-development-database.md)
- [Development database policy](../policies/0100-development-database.md)
- [Backup and restore runbook](0021-backup-and-restore.md)
