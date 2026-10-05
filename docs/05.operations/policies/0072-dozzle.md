---
title: "Dozzle Operations Policy"
version: "1.1.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0072"
parent_ids:
- "AD-0011"
created: "2026-05-17"
---

# Dozzle Operations Policy

## Overview

### Overview

Dozzle는 OPTIONAL 특권 관리자 뷰어다. 네이티브 OIDC와 CIDR 제한은 직접적인
Docker API 접근을 보완하는 필수 통제다.

## Scope

### Policy Scope

활성화, OIDC/CIDR, Docker 소켓 권한, 로그 프라이버시, 설정 데이터, 업그레이드,
백업, 제거.

### Traceability

- [가이드](../guides/0072-dozzle.md) (`GDE-0072`)
- [런북](../runbooks/0072-dozzle.md) (`RUN-0072`)
- [Laboratory 아키텍처](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Rules

### Controls

- `admin`/`admin-logs`만 사용한다. Dozzle을 HOME 밖에 유지한다.
- 네이티브 OIDC, 시크릿 파일 전달, TLS issuer 신뢰, 관리자 CIDR allowlist를
  보존한다. 역할/필터를 검증한다. 로그인만으로 최소 권한이 되지는 않는다.
- `:ro`여도 소켓을 root와 동등한 것으로 취급한다. 승인된
  요구사항과 소켓 제한 설계가 달리 정하지 않는 한 shell/actions는 꺼진
  상태를 유지한다.
- Dozzle을 보존(retention) 용도로 사용하지 않는다. 자격 증명, 개인 데이터,
  비공개 요청을 포함할 수 있는 로그에는 마스킹과 최소 접근을 적용한다.
- `/data` 백업/복구 전에 Dozzle을 중지한다. 복구 테스트에는 격리된/비프로덕션
  Docker 엔드포인트를 사용한다.
- 업그레이드 전에 upstream 권고와 OIDC 동작을 검토한다. 폐기 시 설정을
  삭제하기 전에 소켓을 제거하고 OIDC 클라이언트/시크릿을 폐기한다.

### Verification

헬스, OIDC claim/역할, CIDR 거부, 예상 컨테이너 가시성, 승인되지 않은
shell/actions의 부재를 검증한다. 런타임 증거는 별도로 남는다.

### Review Cadence

이미지/보안 권고 OIDC/CIDR, 소켓, 설정 변경 시 검토한다.

### 책임과 예외 구분

책임자는 `@buenhyden`이다. Dozzle의 네이티브 OIDC는 승인된 인증 방식이며
ForwardAuth를 중복 추가하는 일반 절차를 적용하지 않는다. 이 예외가 CIDR·issuer
신뢰·socket 권한 통제를 면제하지 않는다. 선언된 자원 상한을 바꿀 때는 관찰된 로그
처리량과 호스트 용량을 근거로 검토한다.

## Exceptions

### Exceptions

인증/CIDR 통제 없이 Dozzle을 노출하거나 읽기 전용 소켓 마운트를 Docker API
권한 부여로 취급하는 예외는 없다.

## Related Documents

- [Dozzle Compose 소스](../../../infra/06-observability/dozzle/docker-compose.yml)
- [Dozzle 보안 고려사항](https://dozzle.dev/guide/authentication#security-considerations)
