---
title: "게이트웨이와 네트워크 런북"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 게이트웨이와 네트워크 런북

## Overview

게이트웨이와 네트워크의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [01-Gateway Nginx Runbook](0011-nginx.md) | `RUN-0011` | 이 런북은 Nginx readonly/tmpfs 전환 이후 발생 가능한 장애, `nginx -t` 실패, `/ping` 헬스체크 실패 상황의 복구 절차를 정의한다. > Scope: Nginx Special-path Proxy Recovery 목적은 r |
| [01-Gateway Traefik Runbook](0013-traefik.md) | `RUN-0013` | 이 런북은 Traefik 미들웨어 회귀, dashboard 접근 장애, 라우팅 이상 상황에서 복구 절차를 정의한다. > Scope: Traefik Primary Gateway Recovery 목적은 `gateway-standard-chain` 회귀 시 |
| [Compose Network Membership Runbook](0077-ip-address-management.md) | `RUN-0077` | Compose 서비스의 network membership과 고정 주소를 변경하거나 DNS/IP 충돌을 진단하는 절차다. |

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
