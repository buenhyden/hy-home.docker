---
title: "공통 운영 런북"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 공통 운영 런북

## Overview

공통 운영의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Harness / Agent-first Engineering Runbook](0004-harness-agent-first-engineering.md) | `RUN-0004` | 이 런북은 `hy-home.docker`의 하네스 엔지니어링과 Agent-first Engineering 계약이 계속 유효한지 반복 검증하는 절차를 제공한다. |
| [Cold Start and Reboot Runbook](0098-cold-start-and-reboot.md) | `RUN-0098` | 이 런북은 호스트 재부팅 전후에 HOME Docker Compose 스택과 hy-home.k8s(k3d) 컨테이너를 안전한 순서로 다시 세우고, 단계 사이의 health gate를 확인하는 절차를 제공한다. |
| [System Operations Diagnostic Runbook](0099-system-operations.md) | `RUN-0099` | 이 런북은 여러 앱의 접속·로그인·작업·저장이 함께 실패할 때 공유 의존성 후보를 좁히고 기존 서비스 Runbook으로 전달하는 읽기 전용 진단 절차를 제공한다. |

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
