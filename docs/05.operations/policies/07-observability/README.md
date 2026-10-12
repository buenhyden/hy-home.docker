---
title: "관측 정책"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 관측 정책

## Overview

관측의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Alertmanager Operations Policy](0039-alertmanager.md) | `POL-0039` | 이 정책은 Alertmanager notification routing, grouping, inhibition, receiver, silence, secret boundary를 정의한다. 사용 흐름은 Alertmanager guide가, 장애 대응 절 |
| [Alloy Operations Policy](0040-alloy.md) | `POL-0040` | 이 정책은 Grafana Alloy collector의 telemetry ingestion, discovery, relabeling, exporter, route, health, 설정 경계를 정의한다. 사용 흐름은 GDE-0040이, 장애 대응 절차는 |
| [Grafana Operations Policy](0041-grafana.md) | `POL-0041` | 이 정책은 Grafana visualization hub의 dashboard provisioning, datasource provisioning, Keycloak role mapping, secret boundary, protected route를 정 |
| [Loki Operations Policy](0043-loki.md) | `POL-0043` | 이 정책은 Loki log aggregation service의 retention, SeaweedFS storage, cardinality, compactor, resource, secret boundary를 정의한다. 사용 흐름은 Loki guide |
| [Observability Optimization Hardening Policy](0044-observability-optimization-hardening.md) | `POL-0044` | 이 문서는 `06-observability` 계층의 최적화/하드닝 운영 정책을 정의한다. 게이트웨이 경계 보안, health 기반 의존성, 커스텀 이미지 런타임 하드닝, CI 기준선 검증, 카탈로그 확장 승인 조건을 통제한다. |
| [Prometheus Operations Policy](0045-prometheus.md) | `POL-0045` | 이 정책은 scrape target registration, alerting rule management, TSDB persistence, lifecycle reload, secret file reference, protected access에 대한  |
| [Pushgateway Operations Policy](0046-pushgateway.md) | `POL-0046` | 이 문서는 `06-observability` 계층의 Pushgateway 운영 정책을 정의한다. Pushgateway는 Prometheus pull 모델이 직접 적용되기 어려운 단기 실행 작업과 배치 작업의 메트릭을 임시로 받는 버퍼이며, 장기 저장소 |
| [Pyroscope Operations Policy](0047-pyroscope.md) | `POL-0047` | 이 정책은 Pyroscope continuous profiling service의 ingestion, filesystem storage, capacity boundary, label/cardinality, route, health 기준을 정의한다. 사 |
| [Retention and Performance Policies](0048-telemetry-retention.md) | `POL-0048` | 이 정책은 `06-observability` tier의 metrics, logs, traces, profiles 보관 경계와 performance guardrail을 정의한다. 현재 storage 구현과 요구되는 retention을 구분하며, exte |
| [Tempo Operations Policy](0049-tempo.md) | `POL-0049` | 이 정책은 Tempo distributed tracing backend의 trace ingestion, SeaweedFS S3 storage, block retention, metrics generator, secret boundary, protect |
| [Dozzle Operations Policy](0072-dozzle.md) | `POL-0072` | Dozzle은 OPTIONAL 특권 관리자 뷰어다. 네이티브 OIDC와 CIDR 제한은 직접적인 Docker API 접근을 보완하는 필수 통제다. |
| [Gatus Policy](0087-gatus.md) | `POL-0087` | Gatus는 native OIDC와 지속적인 probe history를 가진 HOME availability monitor다. |

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
