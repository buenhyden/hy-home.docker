---
title: "게이트웨이와 네트워크 가이드"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "operations"
---

# 게이트웨이와 네트워크 가이드

## Overview

게이트웨이와 네트워크의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [01-Gateway Nginx Usage Guide](0011-nginx.md) | `GDE-0011` | 이 문서는 01-gateway의 Nginx 특수 경로 프록시 구성과 하드닝 포인트를 설명한다. Nginx의 lifecycle class는 **OPTIONAL** alternative gateway다. readonly/tmpfs 운영, timeout/f |
| [Edge Routing Stack Operations](0012-edge-routing-stack.md) | `GDE-0012` | 이 문서는 `01-gateway` 티어의 초기 설정 및 검증 가이드이다. |
| [01-Gateway Traefik Usage Guide](0013-traefik.md) | `GDE-0013` | 이 문서는 `Traefik Primary` 모델에서 01-gateway 소유 라우터를 운영하는 방법을 설명한다. Traefik의 lifecycle class는 **HOME**이다. 표준 미들웨어 체인 적용과 검증 흐름을 중심으로 다룬다. |
| [Compose Network Membership Usage Guide](0077-ip-address-management.md) | `GDE-0077` | 이 가이드는 Compose 서비스의 Docker network 소속과 고정 주소 사용 기준을 설명한다. |

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
