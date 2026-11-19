---
title: "Dozzle Operations Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0072"
parent_ids:
- "AD-0011"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Dozzle Operations Policy

## Purpose and Scope

### Objective

Dozzle은 OPTIONAL 특권 관리자 뷰어다. 네이티브 OIDC와 CIDR 제한은 직접적인 Docker API 접근을 보완하는 필수 통제다.

#### Authority

- [Laboratory 아키텍처](../../../02.architecture/01.descriptions/0011-laboratory-architecture.md)

- [Dozzle Compose 소스](../../../../infra/06-observability/dozzle/docker-compose.yml)

### Applies To

활성화, OIDC/CIDR, Docker 소켓 권한, 로그 프라이버시, 설정 데이터, 업그레이드,
백업, 제거.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0072-R1 | 항상 | 필수: `admin`/`admin-logs` profile만 사용 | none | none |
| POL-0072-R2 | 항상 | 필수: Dozzle을 HOME 밖에 유지 | none | none |
| POL-0072-R3 | 항상 | 필수: 네이티브 OIDC/시크릿 파일 전달/TLS issuer 신뢰/관리자 CIDR allowlist 보존 | none | none |
| POL-0072-R4 | 항상 | 필수: 역할/필터 검증(로그인만으로 최소 권한이 되지 않음) | none | none |
| POL-0072-R5 | 항상 | 필수: `:ro`여도 소켓을 root와 동등한 것으로 취급 | none | none |
| POL-0072-R6 | 승인된 요구사항과 소켓 제한 설계가 달리 정하지 않을 때 | 필수: shell/actions를 꺼진 상태로 유지 | none | none |
| POL-0072-R7 | 항상 | 금지: Dozzle을 보존(retention) 용도로 사용 | none | none |
| POL-0072-R8 | 자격 증명/개인 데이터/비공개 요청을 포함할 수 있는 로그 | 필수: 마스킹과 최소 접근 적용 | 수동 | none |
| POL-0072-R9 | `/data` 백업/복구 전 | 필수: Dozzle 중지 | 수동 | none |
| POL-0072-R10 | 복구 테스트 시 | 필수: 격리된/비프로덕션 Docker 엔드포인트 사용 | none | none |
| POL-0072-R11 | 업그레이드 전 | 필수: upstream 권고와 OIDC 동작 검토 | 수동 | none |
| POL-0072-R12 | 폐기 시 | 필수: 설정을 삭제하기 전에 소켓 제거 | 수동 | none |
| POL-0072-R13 | 폐기 시 | 필수: OIDC 클라이언트/시크릿 폐기 | 수동 | none |

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

### Exceptions

#### Exception Conditions

책임자는 `@buenhyden`이다. Dozzle의 네이티브 OIDC는 승인된 인증 방식이며
ForwardAuth를 중복 추가하는 일반 절차를 적용하지 않는다. 이 예외가 CIDR·issuer
신뢰·socket 권한 통제를 면제하지 않는다. 선언된 자원 상한을 바꿀 때는 관찰된 로그
처리량과 호스트 용량을 근거로 검토한다.

인증/CIDR 통제 없이 Dozzle을 노출하거나 읽기 전용 소켓 마운트를 Docker API
권한 부여로 취급하는 예외는 없다.

#### Approval and Review

이미지/보안 권고 OIDC/CIDR, 소켓, 설정 변경 시 검토한다.

## Enforcement

### Mechanisms

헬스, OIDC claim/역할, CIDR 거부, 예상 컨테이너 가시성, 승인되지 않은
shell/actions의 부재를 검증한다. 런타임 증거는 별도로 남는다.

### Limits

정책 본문이 이름 붙인 검사로 강제하는 규칙은 일부이며 아래 항목은 기계적으로 강제되지 않는다.

- 노출/권한 통제: `POL-0072-R1`, `POL-0072-R2`, `POL-0072-R3`, `POL-0072-R4`, `POL-0072-R5`, `POL-0072-R6`는 이름 붙은 검사가 지정되지 않았다.
- 로그 프라이버시: `POL-0072-R7`는 이름 붙은 검사가 지정되지 않았다.
- 로그 프라이버시: `POL-0072-R8`는 승인/검토 등 수동 절차에 의존한다.
- 수명주기: `POL-0072-R9`, `POL-0072-R11`, `POL-0072-R12`, `POL-0072-R13`는 승인/검토 등 수동 절차에 의존한다.
- 수명주기: `POL-0072-R10`는 이름 붙은 검사가 지정되지 않았다.
- 정책은 이름 붙은 검사 명령이나 스크립트를 지정하지 않으며 구체 check와 런타임 증거는 이 문서에 기록되어 있지 않다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter `owner`에 기록된 @buenhyden이다.

### Review Triggers

- [가이드](../../01.guides/07.observability/0072-dozzle.md) (`GDE-0072`)
- [런북](../../03.runbooks/07.observability/0072-dozzle.md) (`RUN-0072`)

- [Dozzle 보안 고려사항](https://dozzle.dev/guide/authentication#security-considerations)
