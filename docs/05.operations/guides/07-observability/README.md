---
title: "관측 가이드"
version: "0.1.3"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
---

# 관측 가이드

## Stage Responsibility

### Purpose and Readers

관측의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

### Inputs and Outputs

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Contents

### Current Items

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Alertmanager Usage Guide](0039-alertmanager.md) | `GDE-0039` | Alertmanager의 route·receiver·inhibition·silence와 secret 렌더링 경계를 설명한다. |
| [Alloy Usage Guide](0040-alloy.md) | `GDE-0040` | Alloy의 두 설정 파일, log·trace·profile·품질 metric 파이프라인과 구현 경계를 설명한다. |
| [Grafana Usage Guide](0041-grafana.md) | `GDE-0041` | Grafana의 datasource·dashboard provisioning, Keycloak OAuth와 신호 연결을 설명한다. |
| [LGTM Stack Usage Guide](0042-lgtm-stack.md) | `GDE-0042` | 관측 tier 전체 서비스, 신호별 data path와 storage 경계를 한눈에 연결한다. |
| [Loki Usage Guide](0043-loki.md) | `GDE-0043` | Loki의 SeaweedFS 저장, retention, label cardinality, Alloy 수집과 LogQL 조회를 설명한다. |
| [06-Observability Optimization Hardening Usage Guide](0044-observability-optimization-hardening.md) | `GDE-0044` | 관측 tier의 gateway·SSO 정렬, health 의존성, 커스텀 이미지 하드닝과 cAdvisor 경계를 설명한다. |
| [Prometheus Usage Guide](0045-prometheus.md) | `GDE-0045` | Prometheus의 선택 config, scrape job, alert rule, TSDB와 host·GPU exporter 경계를 설명한다. |
| [Pushgateway Usage Guide](0046-pushgateway.md) | `GDE-0046` | Pushgateway의 batch metric push·삭제와 현재 없는 Prometheus scrape 연동을 설명한다. |
| [Pyroscope Usage Guide](0047-pyroscope.md) | `GDE-0047` | Pyroscope의 local filesystem 저장, 입력 제한, Alloy profile source와 readiness를 설명한다. |
| [Tempo Usage Guide](0049-tempo.md) | `GDE-0049` | Tempo의 OTLP 수신, SeaweedFS 저장, metrics generator와 retention gap을 설명한다. |
| [Dozzle Usage Guide](0072-dozzle.md) | `GDE-0072` | OPTIONAL admin 로그 뷰어 Dozzle의 native OIDC·CIDR·Docker socket 경계를 설명한다. |
| [Gatus Guide](0087-gatus.md) | `GDE-0087` | Gatus의 native OIDC status UI, SQLite probe history와 수명 주기를 설명한다. |

### Classification

이 폴더의 문서는 모두 가이드 역할이며 `GDE-NNNN` 식별자를 쓴다. 같은 subject의 다른 역할 문서는 있는 경우 같은 번호와 slug로 다른 역할 폴더에 있다.

## Workflow

### Create and Review

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

### Transition and Exit

문서는 `operational-policy` 수명주기(draft, in-review, active, deprecated, superseded, retired)를 따른다. 종료 상태에 이른 문서는 남아야 할 내용을 소유 문서에 요약한 뒤 삭제하고, 번호를 Registry `reserved_history`에 추가하며, 이 목록의 행과 링크를 같은 변경에서 제거한다.

## Related Documents

### Upstream and Downstream

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)

### Policy and Templates

- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
- [README 템플릿](../../../99.templates/templates/common/readme-stage.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다
