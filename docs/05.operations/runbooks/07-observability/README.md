---
title: "관측 런북"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "operations"
---

# 관측 런북

## Overview

관측의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Alertmanager Notification Recovery Runbook](0039-alertmanager.md) | `RUN-0039` | Alertmanager readiness, Prometheus 전달, 렌더링 설정과 알림 경로를 진단·복구한다. |
| [Alloy Readiness and Pipeline Recovery Runbook](0040-alloy.md) | `RUN-0040` | Alloy readiness, Docker discovery, OTLP 입력과 downstream exporter를 진단·복구한다. |
| [Grafana Provisioning and Access Recovery Runbook](0041-grafana.md) | `RUN-0041` | Grafana readiness, OAuth 역할 매핑, datasource·provisioning을 진단·복구한다. |
| [Loki Readiness and Storage Recovery Runbook](0043-loki.md) | `RUN-0043` | Loki readiness, Alloy 입력, SeaweedFS 저장·retention을 진단하고 재시작·rollback한다. |
| [06-Observability Optimization Hardening Runbook](0044-observability-optimization-hardening.md) | `RUN-0044` | 관측 hardening 회귀(middleware, 의존성, 이미지, 검사)를 진단하고 rollback한다. |
| [Prometheus Readiness and Recovery Runbook](0045-prometheus.md) | `RUN-0045` | Prometheus readiness, config·rule 검증, reload, scrape target과 TSDB 증상을 다룬다. |
| [Pushgateway Metrics Buffer Recovery Runbook](0046-pushgateway.md) | `RUN-0046` | Pushgateway의 stale·오염 metric group 정리, readiness와 메모리 버퍼 초기화를 다룬다. |
| [Pyroscope Readiness and Recovery Runbook](0047-pyroscope.md) | `RUN-0047` | Pyroscope readiness, profile 입력, 로컬 저장소와 용량 문제를 진단한다. |
| [Tempo Readiness and Recovery Runbook](0049-tempo.md) | `RUN-0049` | Tempo readiness, OTLP 수집, SeaweedFS 저장, metrics generator와 WAL 증상을 다룬다. |
| [Dozzle Recovery Runbook](0072-dozzle.md) | `RUN-0072` | Dozzle의 OIDC/CIDR 거부, 로그 스트림, socket 오류, 설정 손실과 업그레이드를 다룬다. |
| [Gatus Runbook](0087-gatus.md) | `RUN-0087` | Gatus readiness, 승인된 배포, SQLite 백업·복구와 native OIDC 운영을 다룬다. |

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
