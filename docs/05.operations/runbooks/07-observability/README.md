---
title: "관측 런북"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
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
| [Alertmanager Notification Recovery Runbook](0039-alertmanager.md) | `RUN-0039` | > Scope: Alertmanager 준비 상태, Prometheus 전달 증거, secret으로 렌더링한 설정, 알림 경로 진단, 재시작과 설정 rollback. 이 런북은 Alertmanager UI와 readiness 실패, Prometheus |
| [Alloy Readiness and Pipeline Recovery Runbook](0040-alloy.md) | `RUN-0040` | 이 런북은 Grafana Alloy의 준비 상태 점검, Docker discovery 증거, OTLP 입력 진단, downstream exporter 검증, 재시작과 설정 rollback을 다룬다. 설명은 GDE-0040과 POL-0040에 두고, 여 |
| [Grafana Provisioning and Access Recovery Runbook](0041-grafana.md) | `RUN-0041` | > Scope: Grafana 준비 상태, OAuth 역할 매핑 진단, datasource·provisioning 증거, dashboard 다시 읽기, 재시작과 설정 rollback. 이 런북은 Grafana readiness 실패, OAuth 로그인 |
| [Loki Readiness and Storage Recovery Runbook](0043-loki.md) | `RUN-0043` | > Scope: Loki 준비 상태, Alloy 입력 증거, SeaweedFS 저장소·retention 검증, 재시작과 설정 rollback. 이 런북은 Loki readiness 실패, Grafana의 "no logs found", Alloy ing |
| [06-Observability Optimization Hardening Runbook](0044-observability-optimization-hardening.md) | `RUN-0044` | > Scope: 관측 gateway·SSO middleware, Compose 상태 의존성, 커스텀 이미지 보안 강화, 검사, 재시작과 Git 기반 rollback 증거. 이 런북은 `06-observability` hardening 회귀를 복구하는  |
| [Prometheus Readiness and Recovery Runbook](0045-prometheus.md) | `RUN-0045` | 이 런북은 Prometheus 준비 상태, 설정·rule 검증, lifecycle reload, scrape target 진단, 재시작, TSDB 증상 보고를 다룬다. 장애, scrape target 실패, alert rule 평가 실패, reload |
| [Pushgateway Metrics Buffer Recovery Runbook](0046-pushgateway.md) | `RUN-0046` | 이 런북은 Pushgateway 운영 중 생기는 stale metric, metric group 오염, 메모리 압박, push 실패를 복구하는 실행 절차를 정의한다. 범위는 오래된 지표 정리, 준비 상태 확인, 메모리 버퍼 초기화다. Pushgatew |
| [Pyroscope Readiness and Recovery Runbook](0047-pyroscope.md) | `RUN-0047` | > Scope: Pyroscope 준비 상태, profile 입력 진단, 로컬 저장소 증거, 재시작과 용량 문제 보고. 이 런북은 Pyroscope profile ingestion 누락, Grafana datasource 실패, 로컬 filesyste |
| [Tempo Readiness and Recovery Runbook](0049-tempo.md) | `RUN-0049` | 이 런북은 Tempo 장애 대응 절차를 정의한다. 범위는 준비 상태, OTLP 수집, SeaweedFS S3 저장, metrics generator, WAL 증상 진단과 재시작이다. 데이터 손실 가능성이 있는 WAL·bucket 조치는 별도 승인으로  |
| [Dozzle Recovery Runbook](0072-dozzle.md) | `RUN-0072` | 이 런북은 Dozzle의 OIDC/CIDR 거부, 로그 스트림 누락, socket 오류, 설정 손실, 침해 의심과 승인된 업그레이드를 다루는 절차를 정의한다. |
| [Gatus Runbook](0087-gatus.md) | `RUN-0087` | 이 런북은 Gatus(`gatus`)의 준비 상태 점검, 승인된 대상 배포, SQLite 백업·복구, native OIDC 운영을 다룬다. Compose가 활성화, 마운트, 라우팅을 소유한다. Dockerfile이 업스트림 빌드 핀을 소유하며, 로컬  |

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
