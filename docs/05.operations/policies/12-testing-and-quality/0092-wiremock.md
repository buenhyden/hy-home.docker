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
| POL-0092-R1 | 모드 선택 | 필수: 기능 모드는 `api-mock`만 선택하고 부하 모드는 root Compose와 `wiremock.load.yml` override로 같은 `api-mock`을 선택하며 두 모드를 동시에 선택하거나 HOME·도메인 profile에 추가하지 않는다 | 각 모드 Compose 렌더링 / 운영 catalog 검사 | none |
| POL-0092-R2 | 노출 경계 | 필수: 기능 모드 host 포트는 `127.0.0.1`에만 게시하고 Traefik route를 추가하지 않으며 부하 모드는 포트 미게시와 `--admin-api-require-https`를 유지한다 | Compose 렌더링 / 격리 실행의 host port 없음 확인 | none |
| POL-0092-R3 | 네트워크 admin 권한 | 필수: 기능 모드의 기본 네트워크 컨테이너는 admin 권한을 가지며 부하 모드에 named consumer를 추가하면 별도 제한 네트워크와 HTTPS listener 부재를 확인한다 | 수동 | none |
| POL-0092-R4 | stub 관리 | 필수: 추적되는 mapping만 지속 stub으로 쓰고 stub body는 합성 데이터로 하며 운영 response·credential·토큰·개인 데이터를 쓰지 않는다 | 추적되는 stub 확인 | none |
| POL-0092-R5 | recording/proxying | 금지: 실제 upstream 대상 recording/proxying(admin API로 막히지는 않음) | read-only mount는 recording 저장만 차단 | none |
| POL-0092-R6 | request journal | 필수: 기능 모드 journal을 제한된 상태로 유지하고 각 실행 전 reset하며 부하 모드는 `--no-request-journal`을 유지하고 journal을 성능 증거로 쓰지 않는다 | 격리 실행에서 bounded journal/reset / `--no-request-journal` 확인 | none |
| POL-0092-R7 | 소유권과 자원 | 필수: 기능 모드 journal 개수 한도와 컨테이너 자원 제한을 유지하고 mapping·이미지 변경은 합성 canary와 rollback 원본을 확보한 뒤 적용한다 | Compose 렌더링 / non-root user / read-only root filesystem 확인 | none |

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

다음은 정책이 이름 있는 검사의 한계를 밝히는 부분이다.

- 실제 upstream recording/proxying 금지는 정책일 뿐이며 admin API로 recording을 시작하거나 `proxyBaseUrl` stub을 만드는 것은 기술적으로 막혀 있지 않다.
- 기능 모드에서는 프로젝트 기본 네트워크의 컨테이너가 admin 권한을 가지며 stub에 보낸 요청의 테스트 credential은 실행 중 admin API로 읽을 수 있다.
- 새 consumer와 HTTPS listener 추가는 검토된 변경에 의존하고 메모리 자료는 복구 약속 대상이 아니다.
- mapping·이미지 변경의 canary와 rollback 확보는 이름 있는 검사 없이 검토에 의존한다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- [Guide](../../guides/12-testing-and-quality/0092-wiremock.md) (`GDE-0092`)
- [Runbook](../../runbooks/12-testing-and-quality/0092-wiremock.md) (`RUN-0092`)
- [Compose profile vocabulary](../01-common/0078-compose-profile-vocabulary.md)
