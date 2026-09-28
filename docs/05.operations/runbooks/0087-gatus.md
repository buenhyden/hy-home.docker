---
title: "Gatus Runbook"
version: "0.2.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0087"
parent_ids:
- "POL-0087"
created: "2026-09-19"
---

# Gatus Runbook

## When to Use

Gatus 준비 상태, 프로브 결과 누락 또는 승인된 배포와 복구에 사용한다. 저장소
루트에서 작업한다. 런타임 변경 전에 설정 커밋, 실제 마운트된 데이터 경로,
백업 대상을 기록한다.

## Procedure

1. 렌더링된 환경을 출력하지 않고 공개 설정을 검증한다.

```bash
docker compose --env-file .env.example --profile availability config --quiet
docker compose --profile availability ps gatus
docker compose --profile availability exec -T gatus sh -ec 'wget -q -O /dev/null "http://127.0.0.1:${PORT}/health"'
```

1. 상태 경로가 인증을 요구하는지 확인하고, 승인된 세션을 통해 프로브 상태를
   검토한다. 응답 본문, 토큰, 엔드포인트 크리덴셜을 증거에 복사하지 않는다.
2. 승인된 배포의 경우, 검토된 Compose 선택으로 `gatus`만 빌드하고 교체한다.
   컨테이너 헬스, UI 인증, 예상 프로브 이름을 별도로 검증한다. 예상치 못한
   마운트, 권한, 이미지 식별자를 발견하면 중단한다.

### Native OIDC operation

실행 중인 서비스는 소유자 로그인 승인 이후 네이티브 OIDC와 함께
`config.oidc.yaml`을 사용한다. 라우터는 표준 게이트웨이 체인만 유지하며
metrics 접두사는 제외한다. 원본 `config.yaml`은 설정 롤백을 위해 보존된다.
실행 중인 바인드 마운트 파일을 변경하면 실행 중인 서비스에 즉시 영향을 줄 수
있다. 승인되지 않은 전환을 준비하기 위해 실행 중인 파일을 편집하지 않는다.
현재 롤아웃 상태는
[Task 0004](../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0004-native-oidc-service-migration.md)에
속한다.

클라이언트는 `home-gatus`이며, 정확한 콜백은
`https://status.${DEFAULT_URL}/authorization-code/callback`, confidential
code flow와 S256을 사용한다. 클라이언트 시크릿은 Docker Secret이며, 서비스는
UID 1000으로 실행되고 UID-1000이 소유한 mode 0600 파일을 요구한다.
`GATUS_OIDC_ALLOWED_SUBJECT`는 이메일이나 표시 이름이 아닌 정확한 Keycloak
사용자 `sub`이다. 빈 allowlist는 시작 단계에 도달해서는 안 된다. 로컬 CA는
공개 루트와 결합될 뿐 이를 대체하지 않으며, TLS 검증은 계속 활성화되어 있다.

고정된 소스 빌드에는 Secure/HttpOnly 쿠키, S256 PKCE, 임시 상태 정리, 대소문자
구분 subject 매칭에 대한 검토된 패치가 포함되어 있다. 재빌드 시 소스 아카이브
체크섬을 검증하고, 패치를 fuzz 없이 적용하고, Go 보안 테스트를 통과해야 한다.
업스트림 핀이 변경되면 패치 검토를 다시 수행해야 한다.

이후 승인된 롤아웃에서는 기존 이미지를 롤백용으로 보존하고, SQLite를 일관되게
백업하며, 동일한 데이터 볼륨으로 Gatus만 교체한다. 향후 마이그레이션이나
롤백에서 임시 게이트웨이가 필요한 경우, allowed-subject 로그인과
denied/invalid-session 검사를 통과할 때까지 유지한다. 현재 승인된 런타임은 그
임시 게이트웨이를 제거한 상태다. 쿠키 플래그와 네이티브 세션 만료는 컨테이너
헬스와 별개로 검증한다. Gatus의 로컬 세션은 현재 설정에서 1시간 TTL을 가지며,
Keycloak 로그아웃만으로는 로컬 세션이 폐기되었음을 증명하지 못한다. 별도의
관찰 테스트 없이 애플리케이션 간 단일 로그아웃을 주장하지 않는다.

### Planned isolated restore rehearsal

상태: **계획됨, 미실행**. 성공적인 Gatus SQLite 복원은 주장되지 않는다.

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

## Evidence

현재 Task에 날짜, 커밋, 서비스 이름, 종료 코드, 정제된 health/프로브 결과를
기록한다. 소스 검증만으로는 런타임 준비 상태나 복원된 이력을 입증하지
못한다.

## Rollback or Recovery

일관된 SQLite 백업에는 조율된 스냅샷 또는 승인된 quiescence가 필요하다.
실행 중인 데이터베이스 파일만 복사하면 WAL 상태가 누락될 수 있다. 승인된
셧다운 이후 소유권을 보존한 채 전체 데이터 디렉터리의 보호된 백업을 확보한다.
격리된 저장소로 복원하고 프로덕션 데이터 교체를 승인하기 전에 이력과 새
프로브를 검증한다. 설정과 이미지는 독립적으로 롤백하며, 문제 해결의 기본
수단으로 볼륨을 삭제하지 않는다.

## Escalation

백업 누락, 인증 실패, 알 수 없는 데이터 경로 또는 파괴적 교체가 발생하면
중단하고 @buenhyden에게 연락한다. 배포와 셧다운에는 구체적으로 승인된
대상이 필요하다.

[Compose](../../../infra/06-observability/docker-compose.yml)가 활성화, 마운트,
라우팅을 소유한다. [Dockerfile](../../../infra/06-observability/gatus/Dockerfile)이
업스트림 빌드 핀을 소유하며, 로컬 이미지 이름은 업스트림 버전이 아니다.

## Traceability

- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)
- [Guide](../guides/0087-gatus.md), [Policy](../policies/0087-gatus.md), [Runbook](0087-gatus.md)

## Related Documents

- 런타임 핀은 Compose/Dockerfile 선언이 소유하며,
  [파생 Compose 이미지 프로젝션](../../../infra/tech-stack.versions.json)이
  드리프트를 검증한다.

- [운영 인덱스](../README.md)
- [공식 Gatus 설정, 저장소, 인증](https://github.com/TwiN/gatus)
