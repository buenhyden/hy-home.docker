---
title: "Dozzle Usage Guide"
version: "1.1.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0072"
parent_ids:
- "POL-0072"
implementation_services:
  infra/06-observability/dozzle/docker-compose.yml:
  - dozzle
created: "2026-05-10"
---

# Dozzle Usage Guide

## Overview

이 가이드는 OPTIONAL admin 로그 뷰어 Dozzle의 구성, 인증 경계, 일반 사용 방법을 설명한다. `admin`과 `admin-logs` profile에서만 선택된다.

## Audience and Goal

대상 독자는 컨테이너 로그를 조회하거나 Dozzle 구성을 바꾸는 운영자다. 목표는 Dozzle이 로그 아카이브가 아니라는 점, Docker socket과 OIDC 경계가 어디에 있는지 이해하고 안전하게 조회하는 것이다. 장애와 복구 절차는 [RUN-0072](../runbooks/0072-dozzle.md)가 소유한다.

## Usage

### 목적과 분류

Dozzle은 `admin`과 `admin-logs` 하위의 OPTIONAL admin 로그 뷰어이다. 로그 아카이브가
아니다. 컨테이너 로그는 여전히 Docker/로깅 백엔드가 소유한다. Dozzle은
`${DEFAULT_MANAGEMENT_DIR}/dozzle`에 UI/사용자 설정을 영속화하지만, 조회한 로그의
두 번째 권위 사본을 보관하지는 않는다.

### 현재 구현과 위험

- [Dozzle Compose](../../../infra/06-observability/dozzle/docker-compose.yml)가
  profile, OIDC, 라우트, IP 허용목록, secret, health, 마운트를 정의한다.
- `DOZZLE_AUTH_*`와 `dozzle_client_secret`을 통해 Keycloak에 대한 네이티브 OIDC를
  사용한다. Traefik은 OAuth2 Proxy ForwardAuth가 아니라 게이트웨이 표준 체인과
  admin CIDR 허용목록을 적용한다.
- Docker socket은 `:ro`로 마운트되지만, 업스트림은 읽기 전용 파일 모드가 Docker
  API 메서드를 제한하지 않는다고 경고한다. 침해되면 root와 동등해질 수 있다.
  현재 소스는 socket proxy를 선언하지 않는다.
- `/data`는 설정을 영속화한다. CA 파일은 issuer 신뢰를 지원한다. health 명령은
  OIDC, socket 인가, 로그 커버리지가 아니라 Dozzle 프로세스 health만 증명한다.

### 정상 사용과 준비 조건

운영자는 허용된 계정으로 로그인한 뒤 필요한 컨테이너·시간 범위만 조회한다. 화면과
증거에 비밀·개인정보가 섞이지 않도록 범위를 제한한다. `edge_net`에 연결되지만
호스트 포트는 없고 별도 Compose 의존성 대기는 없다. Keycloak·CA·gateway·Docker
socket 준비는 따로 확인한다. 자원 상한은 선언된 템플릿을 따르며 로그 지연과 CPU·메모리
증가를 함께 관찰한다. TLS/OIDC secret 변경은 공통 인증 소유자와 조정한다.

### Common Checks

- `docker compose --profile admin-logs config --quiet`
- `bash scripts/hardening/check-all-hardening.sh 06-observability`

### Runbook Handoff

OIDC, socket, 로그 스트림, 설정, 업그레이드 복구에는
[runbook](../runbooks/0072-dozzle.md)을 사용한다. 사용·설정 보존·업그레이드 순서는 런북의 `Settings recovery and upgrade`와 `승인된 사용` 절차를 따르며, 데이터와 권한 경계는 [정책](../policies/0072-dozzle.md)을 유지한다.

### Traceability

- [Policy](../policies/0072-dozzle.md) (`POL-0072`)
- [Runbook](../runbooks/0072-dozzle.md) (`RUN-0072`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Dozzle authentication and socket security](https://dozzle.dev/guide/authentication)
- [Dozzle getting started](https://dozzle.dev/guide/getting-started)
- [Dozzle MIT license](https://github.com/amir20/dozzle#license)
