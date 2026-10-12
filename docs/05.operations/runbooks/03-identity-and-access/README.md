---
title: "인증과 접근 런북"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 인증과 접근 런북

## Overview

인증과 접근의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [02-Auth Keycloak Runbook](0014-keycloak.md) | `RUN-0014` | 이 런북은 Keycloak readiness 실패, DB 연결 오류, issuer/redirect 불일치, proxy header 오류, 시크릿 회전 후 인증 장애 상황의 복구 절차를 정의한다. 값이 필요한 점검은 secret 값을 출력하지 않는 방식 |
| [02-Auth OAuth2 Proxy Runbook](0015-oauth2-proxy.md) | `RUN-0015` | 이 런북은 OAuth2 Proxy 인증 루프, OIDC 장애, CA/issuer/callback 불일치, Redis/Valkey session 장애, logout 경계 혼동, readonly/tmpfs 관련 오류, 설정 검증 실패 상황에 대한 복구 절 |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 런북 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
