---
title: "게이트웨이와 네트워크 정책"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 게이트웨이와 네트워크 정책

## Overview

게이트웨이와 네트워크의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [01-Gateway Nginx Operations Policy](0011-nginx.md) | `POL-0011` | 이 문서는 `01-gateway`의 Nginx 운영 정책을 정의한다. Nginx는 특수 경로(`/oauth2/`, `/keycloak/`, `/cdn/`) 프록시 역할을 수행하며, `Balanced` 하드닝 기준을 준수한다. |
| [01-Gateway Traefik Operations Policy](0013-traefik.md) | `POL-0013` | 이 문서는 `01-gateway`의 Traefik 운영 정책을 정의한다. 런타임 모델은 `Traefik Primary`이며, 표준 하드닝 강도는 `Balanced`다. |
| [Compose Network Membership Operations Policy](0077-ip-address-management.md) | `POL-0077` | 이 문서는 `hy-home.docker` 시스템의 Docker network 소속과 주소 할당 정책을 정의한다. IP 충돌 방지 및 일관성 유지를 위한 통제 기준을 제공한다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 정책 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
