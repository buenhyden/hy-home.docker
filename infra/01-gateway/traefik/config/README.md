---
title: "Traefik Static Configuration"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# Traefik Static Configuration

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

이 폴더는 Traefik의 정적 설정을 담고 있습니다.

- **traefik.yml**: 주 설정 파일입니다. entrypoint(80, 443, 8082), Docker provider, `/dynamic/`의 동적 설정을 위한 file provider를 정의합니다.

---

#### Service

##### Purpose

###### Overview
<!-- core-payload-level:4 -->

`infra/01-gateway/traefik/config`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며 기존 본문과 실제 디렉터리 구조를 함께 기준으로 삼는다.

###### Audience
<!-- core-payload-level:4 -->

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers

###### Scope
<!-- core-payload-level:4 -->

###### In Scope
<!-- core-payload-level:5 -->

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

###### Out of Scope
<!-- core-payload-level:5 -->

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

###### Structure
<!-- core-payload-level:4 -->

```text
infra/01-gateway/traefik/config/
├── README.md  # 이 파일
└── traefik.yml  # 구성 파일
```

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| `:80`, `:443` 진입점 | `traefik.yml`을 읽는 Traefik | 이 README는 소비자를 기록하지 않는다. | `traefik.yml`이 선언하는 Traefik 진입점이며 인증서는 상위 Compose가 `/certs/`로 주입한다. | 이 README는 실패 처리를 기록하지 않는다. |
| 메트릭 진입점 `10.250.46.2:8082` | `traefik.yml`을 읽는 Traefik | 상위 Compose 헬스체크(`traefik healthcheck --ping`) | `ping`과 Prometheus 메트릭을 전용 내부 주소에서만 제공하며 `api.insecure`는 `false`이다. | 상위 Compose 헬스체크가 `traefik healthcheck --ping`으로 `ping`을 검사한다. |
| `traefik.yml` 정적 설정 파일 | 이 폴더(`infra/01-gateway/traefik/config`) | 상위 `traefik/docker-compose.yml`의 `traefik` 서비스 | `/etc/traefik/traefik.yml`에 읽기 전용으로 마운트되는 Traefik 정적 설정이다. | 이 README는 실패 처리를 기록하지 않는다. |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

`traefik.yml`은 진입점 `:80`, `:443`과 메트릭 진입점 `10.250.46.2:8082`를 선언하며, `ping`과 Prometheus 메트릭은 메트릭 진입점으로 제공한다.

###### Security Boundary
<!-- core-payload-level:4 -->

`api.insecure`는 `false`이며 메트릭 진입점은 전용 내부 주소에만 바인딩된다. 이 폴더에는 인증서나 secret 값이 없고, 인증서는 상위 Compose가 `/certs/`로 주입한다.

#### Usage

##### Prerequisites

정적 설정 파일 `traefik.yml` 하나만 두며, Compose와 Dockerfile은 없다. 상위 `traefik/docker-compose.yml`의 `traefik` 서비스가 이 파일을 `/etc/traefik/traefik.yml`에 읽기 전용으로 마운트한다.

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

#### Checks

##### Readiness

없음: 이 폴더는 자체 테스트나 검증 스크립트를 두지 않는다. 구성 검증은 `infra/README.md`가 기술한 루트 Compose 검증 경로를 따른다.

##### Failure Handling

###### Related Documents
<!-- core-payload-level:4 -->

- [infra/README.md](../../../README.md)
- [Traefik 서비스 README](../README.md)
- 게이트웨이 운영 가이드 (`docs/05.operations/01.guides/README.md`)
- [문서 인덱스](../../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [curated 버전 투영](../../../tech-stack.versions.json)으로 drift를 검증합니다.

###### Observability and Recovery
<!-- core-payload-level:4 -->

`traefik.yml`의 `ping`은 메트릭 진입점으로 연결되며, 상위 Compose의 헬스체크가 `traefik healthcheck --ping`으로 이를 사용한다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
