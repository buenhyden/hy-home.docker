---
title: "Gatus Runbook"
version: "0.2.2"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0087"
parent_ids:
- "POL-0087"
created: "2026-09-19"
---

# Gatus Runbook

## Overview

이 런북은 Gatus(`gatus`)의 준비 상태 점검, 승인된 대상 배포, SQLite 백업·복구, native OIDC 운영을 다룬다.

[Compose](../../../infra/06-observability/docker-compose.yml)가 활성화, 마운트,
라우팅을 소유한다. [Dockerfile](../../../infra/06-observability/gatus/Dockerfile)이
업스트림 빌드 핀을 소유하며, 로컬 이미지 이름은 업스트림 버전이 아니다.

## Trigger and Preconditions

Gatus 준비 상태, 프로브 결과 누락 또는 승인된 배포와 복구에 사용한다. 저장소
루트에서 작업한다. 런타임 변경 전에 설정 커밋, 실제 마운트된 데이터 경로,
백업 대상을 기록한다.

## Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Service lifecycle prerequisites

`gatus`는 승인된 source/patch build 결과, 선택 OIDC config, subject allowlist, client secret과 CA, sqlite volume 권한을 확인한 뒤 기동한다. Dockerfile의 test 선언은 실행 증거가 아니다. 교체·중지 전 sqlite 일관성을 확보하고 Keycloak·CA 유지보수는 공통 소유자에게 넘긴다.

1. 렌더링된 환경을 출력하지 않고 공개 설정을 검증한다.

```bash
docker compose --env-file .env.example --profile availability config --quiet
docker compose --profile availability ps gatus
docker compose --profile availability exec -T gatus sh -ec 'wget -q -O /dev/null "http://127.0.0.1:${PORT}/health"'
```

1. Public health/bootstrap와 protected status/history API를 구분해 인증을 확인하고, 승인된 세션을 통해 프로브 상태를
   검토한다. 응답 본문, 토큰, 엔드포인트 크리덴셜을 증거에 복사하지 않는다.
2. 승인된 배포의 경우, 검토된 Compose 선택으로 `gatus`만 빌드하고 교체한다.
   컨테이너 헬스, UI 인증, 예상 프로브 이름을 별도로 검증한다. 예상치 못한
   마운트, 권한, 이미지 식별자를 발견하면 중단한다.

### Native OIDC operation

기록된 owner 승인 rollout은 네이티브 OIDC로 전환되었고 현재 source는
`config.oidc.yaml`을 사용한다. 라우터는 표준 게이트웨이 체인만 유지하며
metrics 접두사는 제외한다. 설정 롤백에 대비해 원본 `config.yaml`을 보존한다.
실행 중인 바인드 마운트 파일을 고치면 서비스에 즉시 영향을 줄 수
있다. 승인되지 않은 전환을 준비하기 위해 실행 중인 파일을 편집하지 않는다.
현재 롤아웃 상태는
[Task 0004](../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0004-native-oidc-service-migration.md)에
속한다.

클라이언트는 `home-gatus`이며, 정확한 콜백은
`https://status.${DEFAULT_URL}/authorization-code/callback`, confidential
code flow와 S256을 사용한다. 클라이언트 시크릿은 Docker Secret이며, 서비스는
Compose-selected non-root UID/GID (default 1000)로 실행된다. Mode 0600 secret의 소유자는 선택 UID여야 한다; 기본값을 실제 private 선택으로 단정하지 않는다.
`GATUS_OIDC_ALLOWED_SUBJECT`는 이메일이나 표시 이름이 아닌 정확한 Keycloak
사용자 `sub`이다. 빈 allowlist는 시작 단계에 도달해서는 안 된다. 로컬 CA는
공개 루트와 결합될 뿐 이를 대체하지 않으며, TLS 검증은 계속 활성화되어 있다.

고정된 소스 빌드에는 Secure/HttpOnly 쿠키, S256 PKCE, 임시 상태 정리, 대소문자
구분 subject 매칭에 대한 검토를 거친 패치가 들어 있다. 재빌드 시 소스 아카이브
체크섬을 검증하고, 패치를 fuzz 없이 적용하고, Go 보안 테스트를 통과해야 한다.
업스트림 핀이 바뀌면 패치를 다시 검토해야 한다.

이후 승인된 롤아웃에서는 기존 이미지를 롤백용으로 보존하고, SQLite를 일관되게
백업하며, 동일한 데이터 볼륨으로 Gatus만 교체한다. 향후 마이그레이션이나
롤백에서 임시 게이트웨이가 필요한 경우, allowed-subject 로그인과
denied/invalid-session 검사를 통과할 때까지 유지한다. 인용된 rollout 기록에서는 그 임시 게이트웨이가 제거되었다. 현재 runtime 상태는
별도 관찰 없이 재확인되었다고 주장하지 않는다. 쿠키 플래그와 네이티브 세션 만료는 컨테이너
헬스와 별개로 검증한다. Gatus의 로컬 세션은 현재 설정에서 1시간 TTL을 가지며,
Keycloak 로그아웃만으로는 로컬 세션이 폐기되었음을 증명하지 못한다. 별도의
관찰 테스트 없이 애플리케이션 간 단일 로그아웃을 주장하지 않는다.

### Planned isolated restore rehearsal

**Project 이름만 바꿔서는 실행할 수 없다.** Rehearsal 전에 고정 container name, host port, bind path, external network와 route 충돌을 제거하고 production 통지·workflow egress를 차단한 별도 Compose/storage 정의를 승인한다. 격리와 대상 backup 계약을 검토하기 전에는 NOT_RUN으로 유지한다. 임의 project에 production volume이나 credential을 연결하지 않는다.

상태: **계획됨, 미실행**. Gatus SQLite 복원에 성공했다고 주장하지 않는다.

1. 이미지/패치/설정 digest, 데이터베이스 스키마/이력 개수, 엔드포인트
   인벤토리, 체크섬을 기록한다. 검사를 일시 중단하고 Gatus를 정지한 뒤,
   설정과 시크릿 참조를 포함한 전체 `gatus-data` 세트의 SQLite 일관 백업을
   생성한다.
2. 테스트 엔드포인트 크리덴셜, 테스트 Keycloak 클라이언트를 사용하고 프로덕션
   경로가 없는 별도 프로젝트/네트워크의 새 경로로 복원한다.
3. Gatus를 시작하고 마이그레이션/준비 상태, 이력 개수, 대표 엔드포인트 상태,
   네이티브 OIDC/root-CA 검증, 세션 만료 동작, metrics 스크레이핑을 검증한다.
4. 불일치 시 격리된 프로젝트를 중지하고 로그/체크섬을 보존한다. 손대지 않은
   백업으로 되돌린다. 프로덕션 상태/클라이언트/경로 교체는 별도 승인이
   필요하다.

## Verification

현재 Task에 날짜, 커밋, 서비스 이름, 종료 코드, 정제된 health/프로브 결과를
기록한다. 소스 검증만으로는 런타임 준비 상태나 복원된 이력을 입증하지
못한다.

## Rollback and Escalation

### Rollback or Recovery

일관된 SQLite 백업에는 조율된 스냅샷 또는 승인된 quiescence가 필요하다.
실행 중인 데이터베이스 파일만 복사하면 WAL 상태가 누락될 수 있다. 승인된
셧다운 이후 소유권을 보존한 채 전체 데이터 디렉터리의 보호된 백업을 확보한다.
격리된 저장소로 복원하고 프로덕션 데이터 교체를 승인하기 전에 이력과 새
프로브를 검증한다. 설정과 이미지는 독립적으로 롤백하며, 문제 해결의 기본
수단으로 볼륨을 삭제하지 않는다.

### Escalation

백업 누락, 인증 실패, 알 수 없는 데이터 경로 또는 파괴적 교체가 발생하면
중단하고 @buenhyden에게 연락한다. 배포와 셧다운에는 구체적으로 승인된
대상이 필요하다.

## Related Documents

### Traceability

- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)
- [Guide](../guides/0087-gatus.md), [Policy](../policies/0087-gatus.md), [Runbook](0087-gatus.md)

- 런타임 핀은 Compose/Dockerfile 선언이 소유하며,
  [파생 Compose 이미지 프로젝션](../../../infra/tech-stack.versions.json)이
  드리프트를 검증한다.

- [운영 인덱스](../README.md)
- [공식 Gatus 설정, 저장소, 인증](https://github.com/TwiN/gatus)
