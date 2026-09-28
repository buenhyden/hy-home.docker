---
title: "SonarQube Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0066"
parent_ids:
- "GDE-0066"
created: "2026-05-17"
---

# SonarQube Runbook

## When to Use

health failure, DB connection failure, background-task backlog, search index
failure, token/auth incident, database restore, 또는 승인된 upgrade에 사용한다.

## Procedure

1. 저장소 루트에서 validate하고 bounded state를 캡처한다.

   ```bash
   docker compose --profile sast config --quiet
   docker compose --profile sast ps sonarqube
   docker compose --profile sast logs --tail=200 sonarqube
   ```

2. gateway auth, SonarQube app auth/token, DB connectivity, compute engine queue,
   search-index 증상을 구분한다. user/source/token data는 redact한다.
3. management PostgreSQL service와 여유 공간을 owner를 통해 확인한다. image가 해당
   client를 선언하지 않으므로 SonarQube 내부에서 `psql`을 실행하지 않는다.
4. DB/storage 점검 후 SonarQube만 재시작한다. system health, gateway entry,
   SonarQube permission, 대표 background task 하나를 확인한다.
5. token compromise 시에는 SonarQube에서 token을 revoke하고, 소유 CI secret을
   rotate하고, 이전 token이 거부되는지 확인한다. IdP account 비활성화만으로는
   충분하지 않다.

### Database restore and index recovery

1. SonarQube를 중지하고 DB write가 발생하지 않도록 중지 상태를 유지한다.
2. 검증된 database-native backup을 isolated PostgreSQL target으로 복원한다. source
   DB를 보존하고 backup/checksum/schema/source version을 기록한다.
3. 복원된 DB에 대해 일치하는 version의 isolated SonarQube instance를 fresh/empty
   local search-index path로 시작한다. 진단 목적으로 active production index를
   삭제하지 않는다.
4. reindexing을 허용한 뒤 project/settings/user count, permission, 대표 검색,
   analysis 하나를 확인한다. 승인 후에만 promote한다.

### Upgrade and rollback

1. pre-upgrade DB backup과 plugin/config inventory를 확인하고, 모든 release note와
   prerequisite를 검토한다. 측정된 DB disk를 기준으로 migration headroom을 확보한다.
2. reindex와 scanner 호환성을 포함해 isolated restored DB에 대해 target image를
   테스트한다.
3. rollback 승인이 있을 때만 active instance를 upgrade한다. 실패 시 중지하고,
   pre-upgrade DB를 복원하고, 이전 image를 시작한다. target release가 이미 migrate한
   DB에 이전 image를 연결하지 않는다.

## Evidence

command exit, image/source commit, DB backup/checksum/schema, project와 task
count, health/index status, plugin inventory, 최종 상태를 기록한다. DB 내용,
source code, personal data, token은 절대 기록하지 않는다.

## Rollback or Recovery

database restore/reindex와 upgrade rehearsal은 **계획되었으나 미실행** 상태이다.
검증된 database recovery point 없이 search index를 삭제하는 것은 금지된다.

## Escalation

DB backup이 없거나 미검증이거나, migration이 모호하거나, DB가 corruption되었거나,
plugin 호환성을 알 수 없거나, queue/index failure가 지속되거나, authorization bypass가
있으면 중단한다.

## Traceability

- [Guide](../guides/0066-sonarqube.md) (`GDE-0066`)
- [Policy](../policies/0066-sonarqube.md) (`POL-0066`)
- [SonarQube Compose](../../../infra/09-tooling/sonarqube/docker-compose.yml)

## Related Documents

- [SonarQube backup/restore](https://docs.sonarsource.com/sonarqube-server/9.9/instance-administration/backup-and-restore)
- [SonarQube upgrade](https://docs.sonarsource.com/sonarqube-server/9.8/setup-and-upgrade/upgrade-the-server/upgrade-guide)
