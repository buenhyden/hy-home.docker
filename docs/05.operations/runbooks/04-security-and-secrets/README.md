---
title: "보안과 비밀값 런북"
version: "0.2.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-28"
layer: "operations"
---

# 보안과 비밀값 런북

## Overview

보안과 비밀값의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [OpenBao Runbook](0085-openbao.md) | `RUN-0085` | OpenBao 상태 점검, 기동·중지, initial bootstrap, 사람 로그인과 root 복구, break-glass, 복구 |
| [OpenBao Renderer SecretID Delivery](0103-openbao-renderer-delivery.md) | `RUN-0103` | renderer SecretID wrapping 전달과 Agent 재시작 |
| [OpenBao Prometheus Metrics Credential](0104-openbao-metrics-credential.md) | `RUN-0104` | Prometheus `sys/metrics` token 발급·검증·회전·폐기 |
| [OpenBao Maintenance Window](0105-openbao-maintenance-window.md) | `RUN-0105` | 업그레이드·정책 변경용 W0–W8·Finish, TLS·audit gate, 1인 custody |
| [OpenBao Consumer Migration and Secret Catalog](0106-openbao-consumer-catalog.md) | `RUN-0106` | P06 소비자 이관 운영 경계와 P02 secret catalog 점검 |

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
