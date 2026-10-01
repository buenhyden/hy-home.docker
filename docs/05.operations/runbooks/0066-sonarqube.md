---
title: "SonarQube Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0066"
parent_ids:
- "GDE-0066"
created: "2026-05-17"
---

# SonarQube Runbook

## When to Use

health·DB 연결 실패, 백그라운드 작업 지연, 검색 인덱스 실패, 토큰·인증 사고,
DB 복원 또는 승인된 업그레이드에 사용한다.

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

1. 저장소 루트에서 validate하고 bounded state를 캡처한다.

   ```bash
   docker compose --profile sast config --quiet
   docker compose --profile sast ps sonarqube
   docker compose --profile sast logs --tail=200 sonarqube
   ```

2. gateway 인증·SonarQube 앱 인증/token·DB 연결·compute engine 대기열·검색
   인덱스 증상을 구분한다. user/source/token data는 redact한다.
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

### 보존 대상과 사전 검토

데이터베이스가 백업 권한을 갖는다. 공식 가이드는 데이터베이스 네이티브 백업을
사용하고 복원 후 Elasticsearch 인덱스를 재구축한다. 일관되게 복구하려면 추적되는 설정,
DB secret 보관, 여기 표현되지 않은 외부 설치 plugin/config도 보존해야 한다.
격리된 DB로 복원하고, 로컬 인덱스가 없는 상태로 SonarQube를 시작하여 재인덱싱을
허용한 다음, 프로젝트/설정/사용자와 대표 스캔을 검증한다. 활성 인덱스 삭제는
절대 1차 복구 방법으로 삼지 않는다.

업그레이드 전에는 DB를 백업/검증하고, 모든 release/업그레이드 노트를 읽고, DB와
호스트 전제 조건을 확인하고, plugin 인벤토리를 작성하고, 복원된 사본에서
테스트한다. 롤백에는 이전 이미지와 업그레이드 이전 데이터베이스가 모두 필요하다.
이미지 롤백만으로는 스키마 마이그레이션을 되돌릴 수 없다. 여기서는 백업/복원/
업그레이드를 실행하지 않았다.

## Evidence

command exit, image/source commit, DB backup/checksum/schema, project와 task
count, health/index status, plugin inventory, 최종 상태를 기록한다. DB 내용,
source code, personal data, token은 절대 기록하지 않는다.

## Rollback or Recovery

database restore/reindex와 upgrade rehearsal은 **계획되었으나 미실행** 상태이다.
검증된 database recovery point 없이 search index를 삭제해서는 안 된다.

## Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

DB backup이 없거나 미검증이거나, migration이 모호하거나, DB가 corruption되었거나,
plugin 호환성을 알 수 없거나, queue/index failure가 지속되거나, authorization bypass가
있으면 중단한다.

### 버전 적용 한계

아래의 Server 9.8/9.9 링크는 과거 참고 자료이며 현재 Compose가 선택하는 Community
Build의 실행 절차를 보증하지 않는다. 현재 선언과 일치하는 release·DB·plugin 지원
근거를 확보하기 전에는 업그레이드와 재인덱싱 복구를 진행하지 않는다. 과거 명령을
현재 이미지에 그대로 적용하지 않고 `@buenhyden`에게 호환성 확인을 요청한다.

## Traceability

- [Guide](../guides/0066-sonarqube.md) (`GDE-0066`)
- [Policy](../policies/0066-sonarqube.md) (`POL-0066`)
- [SonarQube Compose](../../../infra/11-quality/sonarqube/docker-compose.yml)

## Related Documents

- [SonarQube backup/restore](https://docs.sonarsource.com/sonarqube-server/9.9/instance-administration/backup-and-restore)
- [SonarQube upgrade](https://docs.sonarsource.com/sonarqube-server/9.8/setup-and-upgrade/upgrade-the-server/upgrade-guide)
