---
title: "메시징과 CDC 런북"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 메시징과 CDC 런북

## Overview

메시징과 CDC의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Kafka Runbook](0036-kafka.md) | `RUN-0036` | 이 런북은 Kafka family의 정적 진단, CDC connector 수명주기, 계획된 백업·복제 캡처, 격리 복원 절차를 다룬다. 정상 대상은 단일 broker이고, 다중 broker LAB은 별도 실행 계약을 따른다. |
| [05-Messaging Optimization Hardening Runbook](0037-messaging-optimization-hardening.md) | `RUN-0037` | 이 런북은 Kafka family hardening baseline을 컨테이너를 시작하지 않고 정적으로 점검하는 절차를 다룬다. |

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
