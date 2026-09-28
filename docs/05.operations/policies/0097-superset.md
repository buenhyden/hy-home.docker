---
title: "Superset Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0097"
parent_ids:
- "AD-0004"
created: "2026-09-23"
---

# Superset Operations Policy

## Overview

Superset는 자체 로그인, 메타데이터 데이터베이스, lakehouse 데이터 접근
권한을 가진 라우팅되는 웹 애플리케이션이다. 인증, role 부여, 자격 증명
처리가 통제 대상이다.

## Policy Scope

선택, 로그인, role, secret, 메타데이터 데이터베이스, 데이터 연결, 업그레이드.

## Controls

- `bi`를 통해서만 선택한다. HOME에는 절대 추가하지 않는다.
- 로그인은 PKCE를 사용하는 native Keycloak OIDC다. router는
  `gateway-standard-chain@file`만 사용하며 OAuth2 Proxy ForwardAuth는 절대
  쓰지 않는다. form 로그인은 제공하지 않는다.
- self-registration은 `Gamma`만 부여한다. Admin과 데이터 role은 Admin이
  이름이 명시된 Keycloak 사용자에게 부여하며, 누가 왜 부여했는지를 Task에
  기록한다.
- signing key, 데이터베이스 비밀번호, client secret은 Docker secret 파일에서
  가져온다. 어느 것도 환경 변수, 명령줄 인자, 설정 안의 평문 URI로 두지
  않는다.
- 메타데이터 데이터베이스는 `mng-pg`에서 feature-owned로 존재하며
  `mng_data_net`에서만 도달 가능하다. host 포트는 없다.
- UI에서 추가한 데이터 연결은 범위가 한정된 identity를 사용한다. 어떤
  것도 관리자 로그인을 쓰지 않는다.

## Exceptions

없음. Superset는 native OIDC를 사용하므로 OAuth2 Proxy `/admins` allowlist는
적용되지 않는다. 어떤 realm 사용자든 `Gamma`(데이터 접근 없음)로 로그인할
수 있고 Admin이 role을 부여한다. 소유자는 realm이 사용자 한 명뿐인
2026-09-24 시점에 이를 유지하기로 했다.

## Verification

Compose 렌더링, hardening 고정값, 그리고 예행연습: 프로비저닝, idempotent
마이그레이션, 등록된 `lakehouse` 데이터베이스, `/health`, 익명 API `401`,
Keycloak 로그인 옵션, 컨테이너 환경 변수에 자격 증명이 없음.

## Review Cadence

Superset 또는 Flask-AppBuilder 업그레이드, Keycloak client 변경, 새 데이터
연결이 생길 때마다 검토한다.

## Traceability

- [가이드](../guides/0097-superset.md) (`GDE-0097`)
- [런북](../runbooks/0097-superset.md) (`RUN-0097`)
- [Application auth integration policy](0079-application-auth-integration.md)

## Related Documents

- [Superset Compose source](../../../infra/04-data/analytics/superset/docker-compose.yml) and [derived version projection](../../../infra/tech-stack.versions.json)
- [Compose profile vocabulary](0078-compose-profile-vocabulary.md)
