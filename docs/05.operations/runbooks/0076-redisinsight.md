---
title: "RedisInsight Recovery Runbook"
version: "1.2.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "operations"
artifact_id: "RUN-0076"
parent_ids:
- "GDE-0076"
created: "2026-05-17"
---

# RedisInsight Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

gateway 로그인 실패, 설정 손실·손상, 대상 인증 실패, 자격 증명 노출, 설정 복원
또는 업그레이드에 사용한다.

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

### Procedure

1. 루트에서 validate하고 점검한다.

   ```bash
   docker compose --profile admin-data config --quiet
   docker compose --profile admin-data ps redisinsight
   docker compose --profile admin-data logs --tail=200 redisinsight
   ```

2. gateway/CIDR, RedisInsight settings, target database 증상을 구분한다. UI health
   (`/api/health/`)와 DB 접속은 따로 본다. DB 접속은 컨테이너 안에서 사전 등록
   연결의 info를 호출해 확인한다. 기동 직후 첫 요청은 시간 초과될 수 있으므로 한 번
   더 시도한다.

   ```bash
   docker exec redisinsight wget -qO- http://10.250.18.3:5540/api/health/
   docker exec redisinsight node -e 'fetch("http://10.250.18.3:5540/api/databases/1/info").then(r=>console.log(r.status))'
   ```

   `1`은 `DEV / dev-valkey`, `2`는 `MNG / mng-valkey`다. 424는 대상 Valkey 중단이나
   inspector 인증 실패이며, 대상 쪽에서 inspector `PING`과 `ACL LOG`를 확인한다.
   administrator target credential로 테스트하지 않는다.
3. 저장된 credential이 노출되었을 수 있으면 RedisInsight를 중지하고, 각 target에서
   rotate하고, 복구 후 connection definition을 제거/재추가하고, sanitized evidence만
   보존한다.
4. `/data` ownership/free-space와 gateway control이 통과한 후에만 재시작한다.

### Inspector 비밀 회전

1. `secrets/db/dev-valkey/inspector_password.txt`(또는 MNG의 같은 파일)를 같은
   소유자·`640`으로 새 값으로 바꾼다. 값은 출력하지 않는다.
2. 대상 Valkey를 다시 만들어 ACL을 렌더링한다:
   `docker compose --profile dev-data up -d --no-deps --force-recreate dev-valkey`
   (MNG는 `--profile mng ... mng-valkey`이며 공유 소비자가 몇 초간 재접속한다).
3. 이전 비밀이 `WRONGPASS`, 새 비밀이 `PONG`인지 확인한다.
4. RedisInsight를 다시 만든다:
   `docker compose --profile admin up -d --no-deps --force-recreate redisinsight`.
   사전 등록 연결이 새 비밀로 다시 저장되고 info가 200인지 본다.

### 기존 `/data`의 암호화 전환

`encryption` 동의가 꺼진 채 만든 `/data`에는 연결 비밀번호가 평문으로 남는다.

1. RedisInsight를 중지하고 `/data`를 소유자만 읽는 위치로 복사한다.
2. 시작한 뒤 `PATCH /api/settings`로 `{"agreements":{"encryption":true}}`를 보내고
   다시 시작한다. 사전 등록 연결은 키로 다시 암호화된다.
3. 관리자 계정으로 수동 추가한 연결은 `DELETE /api/databases/<id>`로 지운다. 이전
   평문 값은 복호화되지 않으므로 다시 넣지 않는다.
4. RedisInsight를 중지하고 `redisinsight.db`에 `VACUUM`을 실행해 지운 행의 잔여
   페이지를 없앤 뒤 `pragma integrity_check`가 `ok`인지 본다. 관리자·inspector
   secret 값이 파일에 남지 않았는지 개수로만 확인한다.
5. `/data`를 `700`, `redisinsight.db`를 `600`으로 둔다. 1단계의 사본은 평문
   자격 증명을 담으므로 확인 뒤 폐기 시점을 정해 기록한다.

### Settings restore and upgrade

1. RedisInsight를 중지하고 `/data` 전체를 protected storage로 복사한다. checksum과
   source commit을 기록하고 credential-bearing material로 보호한다.
2. production target network가 차단된 isolated instance로 복원한다. source
   deployment의 `RI_ENCRYPTION_KEY`(`redisinsight_encryption_key`)와 같은 key를
   사용한다. key가 다르면 저장된 비밀번호를 복호화하지 못한다.
3. live target에 연결하지 않고 settings/log count와 UI access를 확인한다.
4. upgrade 시에는 release/license note를 검토하고, 복사된 settings에서 target image를
   테스트하고, gateway access와 disposable test database connection을 확인한다.

### 승인된 사용·설정 보존·업그레이드

`docker compose --profile admin-data config --quiet`로 검증한다. 게이트웨이
인증/CIDR를 확인한 다음 사전 등록된 inspector 연결만 쓴다. 다른 연결을 수동으로 추가하지 않는다. Workbench의
파괴적 명령은 대상 소유자 승인이 필요하다. ForwardAuth는 Redis 권한을 제한하지
않는다.

`/data`를 복사하기 전에 RedisInsight를 중지한다. 백업은 credential을 담은
자료로 보고 보호한다. UI 설정 백업은 대상 데이터베이스 백업이 아니다. 먼저 프로덕션
Redis/Valkey에 접근할 수 없는 격리된 RedisInsight로 복원하고 같은 암호화 키를
사용한다. 업그레이드 전에는 release와 라이선스 약관을
검토하고 저장된 연결/history를 테스트한다. 여기서는 백업/복원을 실행하지 않았다.

## Verification

### Evidence

종료 코드·source 커밋·설정 checksum/개수·gateway/CIDR 판정·자격 증명 회전 근거·
대상 계정 범위와 최종 상태를 기록한다. password,
key, query history, data 값은 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

settings restore와 upgrade rehearsal은 **계획되었으나 미실행** 상태이다. target
Redis/Valkey data의 restore는 target engine runbook 소관이다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

credential exposure, encrypted data의 encryption key 누락, 알 수 없는 target
authority, settings corruption, license 모호성, restore rehearsal 중 production
target reachability가 있으면 중단한다.

### 직접 접근 제한

listener는 `redisinsight_ingress_net`의 `10.250.18.3`에만 열린다. 데이터 망 peer에서
`nc -z <redisinsight 데이터망 주소> 5540`이, 호스트에서
`curl --max-time 4 http://10.250.18.3:5540/api/health/`가 실패하는지 확인한다. 열려 있으면
`RI_APP_HOST`가 빠졌거나 바뀐 것이므로 중단하고 보고한다. CIDR·SSO 성공만으로
안전한 배포나 복구 완료를 선언하지 않는다. 노출을 확대하거나 저장된 credential을
진단 출력으로 사용하지 않는다.

### Traceability

- [Guide](../guides/0076-redisinsight.md) (`GDE-0076`)
- [Policy](../policies/0076-redisinsight.md) (`POL-0076`)
- [RedisInsight Compose](../../../infra/04-data/redisinsight/docker-compose.yml)

## Related Documents

- [RedisInsight configuration](https://redis.io/docs/latest/operate/redisinsight/configuration/)
