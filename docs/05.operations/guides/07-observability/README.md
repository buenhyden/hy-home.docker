---
title: "관측 가이드"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "operations"
---

# 관측 가이드

## Overview

관측의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Alertmanager Usage Guide](0039-alertmanager.md) | `GDE-0039` | 이 가이드는 `06-observability` 계층의 Alertmanager 사용 맥락과 설정 확인 방법을 설명한다. Alertmanager는 Prometheus가 보낸 알림을 grouping, deduplication, inhibition, sile |
| [Alloy Usage Guide](0040-alloy.md) | `GDE-0040` | Grafana Alloy는 HOME 관측 계층의 telemetry collector다. 서비스 `alloy`는 `obs`, `logs`, `tracing`, `profiling` profile로 선택하며 Compose가 구현을 소유한다. Alloy는  |
| [Grafana Usage Guide](0041-grafana.md) | `GDE-0041` | 이 가이드는 `06-observability` 계층의 Grafana 사용 맥락과 설정 확인 방법을 설명한다. Grafana는 grafana/grafana image declaration으로 실행되는 visualization hub이며 provision |
| [LGTM Stack Usage Guide](0042-lgtm-stack.md) | `GDE-0042` | 이 가이드는 `hy-home.docker`의 `06-observability` tier가 제공하는 통합 관측성 stack을 설명한다. 현재 stack은 Prometheus, Loki, Tempo, Grafana에 Alloy, Alertmanager,  |
| [Loki Usage Guide](0043-loki.md) | `GDE-0043` | 이 가이드는 `06-observability` 계층의 Loki 사용 맥락과 설정 확인 방법을 설명한다. Loki는 Alloy가 수집한 Docker 로그를 `http://loki:3100/loki/api/v1/push`로 수신하고, SeaweedFS S |
| [06-Observability Optimization Hardening Usage Guide](0044-observability-optimization-hardening.md) | `GDE-0044` | 이 문서는 `06-observability` 계층의 최적화/하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. gateway 체인+SSO 정렬, health 기반 의존성, 커스텀 이미지 하드닝, CI 검증 절차를 제공한다. |
| [Prometheus Usage Guide](0045-prometheus.md) | `GDE-0045` | 이 가이드는 `06-observability` 계층의 Prometheus 사용 맥락과 설정 확인 방법을 설명한다. Prometheus는 `infra/06-observability/prometheus/config/prometheus.yml`의 scrap |
| [Pushgateway Usage Guide](0046-pushgateway.md) | `GDE-0046` | 이 문서는 Pushgateway의 역할과 기본 사용법을 설명한다. Pushgateway는 Prometheus pull 모델이 직접 적용되기 어려운 단기 실행·배치 작업의 metric을 일시적으로 받아 두는 버퍼다. 장기 실행 서비스의 일반 metric |
| [Pyroscope Usage Guide](0047-pyroscope.md) | `GDE-0047` | 이 가이드는 `06-observability` 계층의 Pyroscope 사용 맥락과 설정 확인 방법을 설명한다. Pyroscope는 profile 데이터를 로컬 filesystem backend `/var/lib/pyroscope`에 저장하고, Gra |
| [Tempo Usage Guide](0049-tempo.md) | `GDE-0049` | 이 가이드는 `06-observability` 계층의 Tempo 사용 맥락과 설정 확인 방법을 설명한다. |
| [Dozzle Usage Guide](0072-dozzle.md) | `GDE-0072` | 이 가이드는 OPTIONAL admin 로그 뷰어 Dozzle의 구성, 인증 경계, 일반 사용 방법을 설명한다. `admin`과 `admin-logs` profile에서만 선택된다. |
| [Gatus Guide](0087-gatus.md) | `GDE-0087` | Gatus는 `obs`, `availability`, `dev`가 선택하는 상시 실행 HOME availability monitor이다. native Keycloak OIDC로 보호되는 status UI와 SQLite probe history를 제공한 |

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
