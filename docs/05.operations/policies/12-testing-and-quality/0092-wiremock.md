---
title: "WireMock Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0092"
parent_ids:
- "AD-0009"
created: "2026-09-23"
next_review_at: "2027-05-13"
---

# WireMock Operations Policy

## Purpose and Scope

### Objective

WireMock은 추적되는 stub으로 HTTP 요청에 응답한다. 기능 모드는 bounded request
journal을 기록하고, load override 모드는 journal을 기록하지 않는다. admin API에는
인증이 없으므로 노출과 stub 내용이 곧 control이다.

#### Authority

- [Platform Operations·Quality 아키텍처](../../../02.architecture/descriptions/0009-tooling-architecture.md)
- [WireMock Compose source](../../../../infra/11-quality/wiremock/docker-compose.yml)

### Applies To

기능·부하 모드 선택, 네트워크 노출, stub 내용, request journal, 제거.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0092-R1 | 기능 모드 선택 시 | 필수: `api-mock`만 선택한다 | none | none |
| POL-0092-R2 | 부하 모드 선택 시 | 필수: root Compose와 `wiremock.load.yml` override를 함께 사용해 같은 `api-mock`을 선택한다 | none | none |
| POL-0092-R3 | 항상 | 금지: 기능 모드와 부하 모드의 동시 선택 | none | none |
| POL-0092-R4 | 항상 | 금지: HOME·도메인 profile에 추가 | none | none |
| POL-0092-R5 | 기능 모드 | 필수: host 포트는 `127.0.0.1`에만 게시한다 | none | none |
| POL-0092-R6 | 항상 | 금지: Traefik route 추가 | none | none |
| POL-0092-R7 | 부하 모드 | 필수: host port를 게시하지 않는다 | 격리된 실행에서 host port 없음 확인 | none |
| POL-0092-R8 | 부하 모드 | 필수: `--admin-api-require-https`로 HTTP admin을 거부한다 | none | none |
| POL-0092-R9 | HTTPS listener 추가 시 | 필수: 인증·노출을 검토한 별도 변경으로 추가한다 | 수동 | none |
| POL-0092-R10 | 부하 모드에 named consumer 추가 시 | 필수: 별도 제한 네트워크와 HTTPS listener 부재를 확인한다 | 수동 | none |
| POL-0092-R11 | 항상 | 필수: 추적되는 mapping만 지속적인 stub으로 쓴다 | none | none |
| POL-0092-R12 | 항상 | 필수: stub body는 합성 데이터로 한다 | none | none |
| POL-0092-R13 | 항상 | 금지: 캡처된 운영 response·credential·토큰·개인 데이터 사용 | none | none |
| POL-0092-R14 | 항상 | 금지: 실제 upstream 대상 recording이나 proxying | read-only mount(recording 저장만 차단, admin API의 recording 시작/`proxyBaseUrl` stub 생성은 차단하지 않음) | none |
| POL-0092-R15 | 기능 모드 | 필수: request journal을 제한된 상태로 유지한다 | 격리된 실행에서 bounded journal/reset 확인 | none |
| POL-0092-R16 | 기능 모드 | 필수: 각 승인된 실행 전에 journal을 reset한다 | 격리된 실행에서 bounded journal/reset 확인 | none |
| POL-0092-R17 | 부하 모드 | 필수: `--no-request-journal`을 유지한다 | 격리된 실행에서 `--no-request-journal` 확인 | none |
| POL-0092-R18 | 항상 | 금지: journal reset이나 조회를 성능 증거로 사용 | none | none |
| POL-0092-R19 | 기능 모드 | 필수: journal 개수 한도와 컨테이너 자원 제한을 유지한다 | none | none |
| POL-0092-R20 | 항상 | 금지: 민감한 요청을 보존 근거로 복제 | none | none |
| POL-0092-R21 | mapping·이미지 변경 시 | 필수: 합성 canary와 검토된 rollback 원본을 확보하고 적용한다 | 수동 | none |

- 기능 모드는 `api-mock`만 선택한다. 부하 모드는 root Compose와
  `wiremock.load.yml` override를 함께 사용해 같은 `api-mock`을 선택한다.
  두 모드는 같은 service state를 공유하므로 동시에 선택하거나 HOME·도메인 profile에
  추가하지 않는다.
- 기능 모드 host 포트는 `127.0.0.1`에만 게시하고 Traefik route를 추가하지 않는다.
  부하 모드는 host port를 게시하지 않고 `--admin-api-require-https`로 HTTP admin을
  거부한다. HTTPS listener를 추가하려면 인증·노출을 검토한 별도 변경이 필요하다.
- 기능 모드에서는 프로젝트 기본 네트워크의 컨테이너가 admin 권한을 가진다.
  부하 모드의 HTTP admin은 거부되지만 named consumer가 추가되면 별도 제한
  네트워크와 HTTPS listener 부재를 확인한다.
- 추적되는 mapping만이 지속적인 stub이다. stub body는 합성 데이터다. 캡처된 운영
  response, credential, 토큰, 개인 데이터는 사용하지 않는다.
- 실제 upstream을 대상으로 한 recording이나 proxying은 정책으로 금지한다. read-only
  mount는 recording 저장만 막는다. admin API로 recording을 시작하거나
  `proxyBaseUrl`을 가진 stub을 만드는 일은 기술적으로 막혀 있지 않다.
- 기능 모드 request journal은 제한된 상태로 유지하고 각 승인된 실행 전에 reset한다.
  stub에 보낸 요청에는 테스트 credential이 들어 있을 수 있고 실행 중에는 admin API로
  읽을 수 있다. 부하 모드는 `--no-request-journal`을 유지하며 journal reset이나
  조회를 성능 증거로 사용하지 않는다.

#### 소유권과 자원

책임자는 `@buenhyden`이다. 기능 모드의 journal 개수 한도와 컨테이너 자원 제한을
유지한다. 삭제·재시작으로 사라지는 메모리 자료는 복구 약속 대상이 아니며 민감한
요청을 보존 근거로 복제해서는 안 된다. mapping·이미지 변경은 합성 canary와 검토된
rollback 원본을 확보하고 적용한다.

### Exceptions

#### Exception Conditions

현재 승인된 예외는 없다. 새로운 consumer의 네트워크 연결은 범위와 admin API
권한을 검토한 변경이어야 한다. host binding이나 기본 네트워크 참여를 자동으로 넓히지 않는다.

#### Approval and Review

WireMock major 업그레이드, 신규 consumer, loopback을 넘는 노출이 제안될 때마다
검토한다.

## Enforcement

### Mechanisms

각 모드의 Compose 렌더링, 운영 catalog 검사, 추적되는 stub, non-root user,
read-only root filesystem을 확인한다. 기능 모드는 bounded journal/reset, load 모드는
host port 없음과 `--no-request-journal`을 격리된 실행에서 별도로 확인한다.

### Limits

다음 규칙은 정책이 이름 있는 자동 검사를 연결하지 않았다.

- 이름 있는 검사 없음(모드 선택): `POL-0092-R1`, `POL-0092-R2`, `POL-0092-R3`, `POL-0092-R4`
- 이름 있는 검사 없음(노출): `POL-0092-R5`, `POL-0092-R6`, `POL-0092-R8`
- 이름 있는 검사 없음(stub): `POL-0092-R11`, `POL-0092-R12`, `POL-0092-R13`
- 이름 있는 검사 없음(journal): `POL-0092-R18`
- 이름 있는 검사 없음(자원): `POL-0092-R19`, `POL-0092-R20`
- 수동 검토·승인에 의존(노출): `POL-0092-R9`
- 수동 검토·승인에 의존(네트워크): `POL-0092-R10`
- 수동 검토·승인에 의존(자원): `POL-0092-R21`
- 정책이 스스로 밝힌 한계: 실제 upstream recording/proxying 금지는 정책이며 admin API로 recording을 시작하거나 `proxyBaseUrl` stub을 만드는 일은 기술적으로 막혀 있지 않다.
- 기능 모드에서는 프로젝트 기본 네트워크의 컨테이너가 admin 권한을 가지며 stub에 보낸 요청의 테스트 credential은 실행 중 admin API로 읽을 수 있다.
- 삭제·재시작으로 사라지는 메모리 자료는 복구 약속 대상이 아니다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- [Guide](../../guides/12-testing-and-quality/0092-wiremock.md) (`GDE-0092`)
- [Runbook](../../runbooks/12-testing-and-quality/0092-wiremock.md) (`RUN-0092`)
- [Compose profile vocabulary](../01-common/0078-compose-profile-vocabulary.md)
