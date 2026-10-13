---
title: "인증과 접근 가이드"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "operations"
---

# 인증과 접근 가이드

## Overview

인증과 접근의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [02-Auth Keycloak Usage Guide](0014-keycloak.md) | `GDE-0014` | 이 문서는 `02-auth`의 Keycloak 운영 구성과 OIDC 발급자 계약을 설명한다. Keycloak의 lifecycle class는 **HOME**이다. DB/관리자 시크릿 주입, hostname/proxy header, health endp |
| [02-Auth OAuth2 Proxy Usage Guide](0015-oauth2-proxy.md) | `GDE-0015` | 이 문서는 OAuth2 Proxy를 Traefik `ForwardAuth` 표준으로 운영하는 방법을 설명한다. |
| [Application Authentication Integration Guide](0079-application-auth-integration.md) | `GDE-0079` | Keycloak, OAuth2 Proxy, Traefik, Kafbat UI, Airflow를 중복 인증 없이 연결하고 서비스별 authorization model을 유지하는 방법을 설명한다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
