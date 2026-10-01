---
title: "Terrakube Operations Policy"
version: "1.1.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0069"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# Terrakube Operations Policy

## Overview

Terrakube는 명시적인 `iac` 컨트롤 플레인이다. Apache-2.0 프로젝트 라이선스가
이 단일 호스트 배포의 지원, SLA, 엔터프라이즈 기능, HA를 보장하지는
않는다.

## Policy Scope

API/UI/executor 활성화, 네이티브/gateway 인증, Docker 소켓 및 provider 권한,
PostgreSQL/SeaweedFS/Valkey 데이터, 협조된 복구, 업그레이드, 제거.

## Controls

- **Activation:** `iac`에서는 이름이 지정된 세 가지 Terrakube 서비스만 시작하고
  정확한 의존성은 별도로 선택한다. HOME/tooling에서는 제외한다.
- **Authentication:** 추적 중인 gateway 미들웨어와 애플리케이션 OIDC 동작을 모두
  검증한다. 환경 변수 레이블만으로 네이티브 OIDC나 그룹 권한 부여를 주장하지
  않는다.
- **Execution:** executor의 Docker 소켓 접근과 provider 자격 증명은 특권이다.
  plan과 apply는 리포지토리/ref, workspace, 계정, 예상 리소스, 승인자를
  명시한다. apply/destroy는 별도 승인을 받아야 한다.
- **Secrets:** 선언된 시크릿 파일만 사용한다. 로그, 스크린샷, Task, 지원 번들에
  시크릿/상태/plan 출력이 포함되어서는 안 된다.
- **Data:** PostgreSQL 메타데이터와 SeaweedFS `tfstate`는 공동으로 권위를
  갖는다. Valkey는 조정 상태다. 보존 정책은 일관된 복구 지점을 포함해야 한다.
- **Backup/recovery:** 스케줄링/실행을 정지하고, PostgreSQL과 SeaweedFS를
  일관되게 캡처하며, config/client/custody 메타데이터를 보존하고, 외부 실행을
  비활성화한 상태로 리허설한다. 단일 저장소 복구는 불완전하다.
- **Resources/availability:** 단일 호스트, 단일 replica DEV 배포로
  취급한다. 컨테이너 재시작을 HA나 재해 복구로 묘사하지 않는다.
- **Upgrade:** 복원된 사본에서 마이그레이션을 테스트하고 API/UI/executor를
  호환 세트로 함께 이동한다. 호환되지 않는 다운그레이드에는 데이터베이스/상태
  롤백이 동반된다.
- **Removal:** 승인된 후속 시스템이 소유하기 전까지 workspace, run, 상태, 출력,
  VCS 매핑, 복구 보관을 유지한다. 컨테이너 삭제만으로는 충분하지 않다.

## Exceptions

예외는 provider/apply 승인, Docker 소켓 검토, 시크릿 취급, 협조된 백업을
우회할 수 없다. 만료 시점과 복구 담당자를 기록한다.

## Verification

정적 Compose와 컴포넌트 헬스는 부분적인 신호다. 엔드투엔드 증거에는
로그인/권한 부여, DB/객체 접근 가능성, executor 등록, 그리고 검토된
비적용(non-applying) plan이 필요하다. 복구는 리허설하기 전까지 검증되지
않은 상태로 남는다.

## Review Cadence

각 릴리스, 인증 변경, 저장소/백엔드 변경, Docker 소켓 권한 변경 전에
검토한다.

### 현재 실행 경로의 제한

추적되는 Compose와 README는 cookie 기반 ForwardAuth가 Terraform CLI/API 토큰
요청 및 공개 API URL을 사용하는 executor 요청을 막는 상태임을 명시한다. 전용
`home-terrakube` client/audience와 RBAC 활성화는 별도 승인된 구현 변경이 필요하다.
현재 gateway 통제는 유지하며 로그인·health 성공을 실행 가능 증거로 기록하지 않는다.
인증 오류를 우회하거나 실제 plan/apply를 재시도하지 말고 `@buenhyden`에게 보고한다.

## Traceability

- [가이드](../guides/0069-terrakube.md) (`GDE-0069`)
- [런북](../runbooks/0069-terrakube.md) (`RUN-0069`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Terrakube Compose 소스](../../../infra/09-platform-ops/terrakube/docker-compose.yml)
- [Terrakube 문서](https://docs.terrakube.io/)
- [Terrakube 라이선스](https://github.com/terrakube-io/terrakube/blob/main/LICENSE)
- [운영 인덱스](../README.md)
