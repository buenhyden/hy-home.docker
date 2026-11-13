---
title: "Traefik Static Configuration"
version: "1.0.4"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Traefik Static Configuration

이 폴더는 Traefik의 정적 설정을 담고 있습니다.

- **traefik.yml**: 주 설정 파일입니다. entrypoint(80, 443, 8082), Docker provider, `/dynamic/`의 동적 설정을 위한 file provider를 정의합니다.

---

## Purpose

### Service Role

#### Overview

`infra/01-gateway/traefik/config`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며 기존 본문과 실제 디렉터리 구조를 함께 기준으로 삼는다.

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers

#### Scope

##### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

##### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

#### Structure

```text
infra/01-gateway/traefik/config/
├── README.md  # 이 파일
└── traefik.yml  # 구성 파일
```

### Supported Environment

정적 설정 파일 `traefik.yml` 하나만 두며, Compose와 Dockerfile은 없다. 상위 `traefik/docker-compose.yml`의 `traefik` 서비스가 이 파일을 `/etc/traefik/traefik.yml`에 읽기 전용으로 마운트한다.

## Interfaces

### Inputs and Outputs

`traefik.yml`은 진입점 `:80`, `:443`과 메트릭 진입점 `10.250.46.2:8082`를 선언하며, `ping`과 Prometheus 메트릭은 메트릭 진입점으로 제공한다.

### Security Boundary

`api.insecure`는 `false`이며 메트릭 진입점은 전용 내부 주소에만 바인딩된다. 이 폴더에는 인증서나 secret 값이 없고, 인증서는 상위 Compose가 `/certs/`로 주입한다.

## Development

### Local Workflow

#### Usage

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

### Checks

없음: 이 폴더는 자체 테스트나 검증 스크립트를 두지 않는다. 구성 검증은 `infra/README.md`가 기술한 루트 Compose 검증 경로를 따른다.

## Operations

### Runbook Links

#### Related Documents

- [infra/README.md](../../../README.md)
- [Traefik 서비스 README](../README.md)
- 게이트웨이 운영 가이드 (`docs/05.operations/guides/README.md`)
- [문서 인덱스](../../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [curated 버전 투영](../../../tech-stack.versions.json)으로 drift를 검증합니다.

### Observability and Recovery

`traefik.yml`의 `ping`은 메트릭 진입점으로 연결되며, 상위 Compose의 헬스체크가 `traefik healthcheck --ping`으로 이를 사용한다.
