---
title: "관측 정책"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
---

# 관측 정책

## Stage Responsibility

### Purpose and Readers

관측의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

### Inputs and Outputs

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Contents

### Current Items

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Alertmanager Operations Policy](0039-alertmanager.md) | `POL-0039` | Alertmanager routing·grouping·inhibition·receiver·silence와 secret 렌더링 통제를 정한다. |
| [Alloy Operations Policy](0040-alloy.md) | `POL-0040` | Alloy 설정 선택, discovery·relabel·exporter·route와 품질 metric 수신 통제를 정한다. |
| [Grafana Operations Policy](0041-grafana.md) | `POL-0041` | Grafana provisioning, datasource UID, Keycloak role mapping, secret과 route 통제를 정한다. |
| [Loki Operations Policy](0043-loki.md) | `POL-0043` | Loki retention, SeaweedFS storage, cardinality, compactor, resource와 LAN 예외 통제를 정한다. |
| [Observability Optimization Hardening Policy](0044-observability-optimization-hardening.md) | `POL-0044` | 관측 tier의 gateway 경계, health 의존성, 커스텀 이미지 하드닝과 확장 승인 조건을 정한다. |
| [Prometheus Operations Policy](0045-prometheus.md) | `POL-0045` | Prometheus scrape·rule·TSDB·lifecycle·secret·API route와 host·GPU exporter 통제를 정한다. |
| [Pushgateway Operations Policy](0046-pushgateway.md) | `POL-0046` | Pushgateway의 사용 범위, label·stale group 관리와 Prometheus scrape 연동 요구를 정한다. |
| [Pyroscope Operations Policy](0047-pyroscope.md) | `POL-0047` | Pyroscope ingestion 제한, filesystem storage, label cardinality, route와 health 통제를 정한다. |
| [Retention and Performance Policies](0048-telemetry-retention.md) | `POL-0048` | metrics·logs·traces·profiles의 보존 요구와 현재 구현의 미준수 경계를 정한다. |
| [Tempo Operations Policy](0049-tempo.md) | `POL-0049` | Tempo ingestion, SeaweedFS storage, metrics generator, retention gap과 LAN 예외 통제를 정한다. |
| [Dozzle Operations Policy](0072-dozzle.md) | `POL-0072` | OPTIONAL 특권 뷰어 Dozzle의 OIDC·CIDR·socket·로그 프라이버시 통제를 정한다. |
| [Gatus Policy](0087-gatus.md) | `POL-0087` | Gatus의 native OIDC, metrics 경계, SQLite 상태와 업그레이드 통제를 정한다. |

### Classification

이 폴더의 문서는 모두 정책 역할이며 `POL-NNNN` 식별자를 쓴다. 같은 subject의 다른 역할 문서는 있는 경우 같은 번호와 slug로 다른 역할 폴더에 있다.

## Workflow

### Create and Review

1. 식별자와 문서 제목으로 대상을 고른다.
2. 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

### Transition and Exit

문서는 `operational-policy` 수명주기(draft, in-review, active, deprecated, superseded, retired)를 따른다. superseded 또는 retired에 이른 문서는 [은퇴 전제 조건](../../../../.agents/governance/documentation-protocol.md#retirement-preconditions)을 모두 충족할 때에만 남아야 할 내용을 소유 문서에 요약한 뒤 삭제하고, 번호를 Registry `reserved_history`에 추가하며, 이 목록의 행과 링크를 같은 변경에서 제거한다.

## Related Documents

### Upstream and Downstream

- [상위 정책 분류](../README.md)
- [운영 문서](../../README.md)

### Policy and Templates

- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
- [README 템플릿](../../../99.templates/templates/common/readme-stage.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다
