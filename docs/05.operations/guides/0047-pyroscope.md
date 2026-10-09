---
title: "Pyroscope Usage Guide"
version: "1.0.6"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0047"
parent_ids:
- "POL-0047"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - pyroscope
created: "2026-05-10"
---

# Pyroscope Usage Guide

## Overview

이 가이드는 `06-observability` 계층의 Pyroscope 사용 맥락과 설정 확인 방법을 설명한다. Pyroscope는 profile 데이터를 로컬 filesystem backend `/var/lib/pyroscope`에 저장하고, Grafana Pyroscope datasource와 Alloy `pyroscope.write` endpoint를 통해 flamegraph 분석 경로를 제공한다.

## Audience and Goal

대상 독자: 개발자, SRE, 운영자, AI Agent.

- Pyroscope 서비스, 설정, storage, ingestion limit, Grafana/Alloy 연동 경계를 빠르게 파악한다.
- Grafana에서 flamegraph, diff view, profile label을 확인하는 진입점을 안내한다.
- 복구, restart, 용량 압박, storage 변경 판단은 [RUN-0047](../runbooks/0047-pyroscope.md)로 넘긴다.

## Usage

사용 전에 다음을 확인한다.

- [Grafana Alloy](0040-alloy.md)에 `pyroscope.write "local_pyroscope"` endpoint `http://pyroscope:4040`이 있어야 한다.
- [Grafana](0041-grafana.md)에 Pyroscope datasource URL `http://pyroscope:4040`이 provisioning되어 있어야 한다.
- Profile labels에는 request ID, user ID, token, credential 같은 high-cardinality 또는 secret-bearing 값을 넣지 않는다.

일반 순서는 다음과 같다.

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-infra-med|image: grafana/pyroscope:|container_name: pyroscope|pyroscope-data|PYROSCOPE_PORT|/ready|pyroscope.middlewares' infra/06-observability/docker-compose.yml
   ```

2. Pyroscope config의 storage, ingestion limit, privacy boundary를 확인한다.

   ```bash
   rg -n 'http_listen_port: 4040|reporting_enabled: false|data_dir: /var/lib/pyroscope/compactor|ingestion_rate_mb: 16|ingestion_burst_size_mb: 32|max_label_names_per_series: 30|multitenancy_enabled: false|backend: filesystem|dir: /var/lib/pyroscope|disable_push: true' infra/06-observability/pyroscope/config/pyroscope.yaml
   ```

3. Alloy와 Grafana가 Pyroscope endpoint를 가리키는지 확인한다.

   ```bash
   rg -n 'pyroscope.write "local_pyroscope"|url = "http://pyroscope:4040"|type: grafana-pyroscope-datasource|url: http://pyroscope:4040' infra/06-observability/alloy/config/config.alloy infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

4. Grafana의 `Explore` 메뉴에서 `Pyroscope` datasource를 선택하고 `Application` 또는 service label 기준으로 최근 profile을 조회한다.

5. Flamegraph에서 CPU hot path 또는 allocation-heavy path를 확인한다. 성능 저하 전후를 비교해야 하면 Grafana diff view를 사용한다.

### Source-backed operating contract

- **목적/분류/출처**: `pyroscope`는 `obs`/`profiling`이 선택하는 `HOME` continuous-profile store다. [Compose](../../../infra/06-observability/docker-compose.yml)와 [Pyroscope config](../../../infra/06-observability/pyroscope/config/pyroscope.yaml)가 authoritative하다.
- **Flow/dependencies/security**: client 또는 Alloy profile source가 profile을 write하고 Grafana가 query한다. 두 Alloy config는 Go/SeaweedFS scrape sources와 write sink를 선언한다. 소스 선언만으로 실제 profile 수신이 증명되지는 않는다. Traefik이 route를 보호하며, Grafana, producer, storage와 선언된 network가 dependency다.
- **State/resources**: single-node filesystem state는 `pyroscope-data:/var/lib/pyroscope` 아래에 있고, service Docker Secret은 없다. Source의 resource 값은 limit이지 측정된 headroom이 아니다.
- **Normal use**: root에서 render하고, `profilecli ready`로 readiness를 확인하고, 승인된 client에서만 labeled test profile을 ingest해 Pyroscope/Grafana에서 query한다.
- **Lifecycle**: write를 중지하고 consistent stopped filesystem snapshot을 만든다. Config와 producer label을 보존한다. Storage-format 가이드에 따라 upgrade한 뒤 historical/new profile query와 producer 호환성을 검증한다.
- **Upstream/license**: 공식 [storage](https://grafana.com/docs/pyroscope/latest/configure-server/storage/)와 [deployment modes](https://grafana.com/docs/pyroscope/latest/reference-pyroscope-v2-architecture/deployment-modes/) 가이드를 따른다. Pyroscope는 AGPL-3.0 라이선스다.

### Profile storage and source limits

이 항목은 [POL-0047](../policies/0047-pyroscope.md#profile-storage-and-source-limits)이 소유한다. 요약: Alloy의 Go/SeaweedFS pprof source는 writer/receiver readiness만으로 수신을 증명하지 않는다. Pyroscope에는 고정 retention이 없고 기본값이나 disk pressure 정리가 무기한 보존을 보장하지 않는다. readiness는 `wget` 대신 선언된 `profilecli ready` probe를 쓴다.

### 운영 시 주의점

- **Profiling overhead**: 수집 빈도와 profile type은 애플리케이션 성능에 영향을 줄 수 있다. 고빈도 profiling은 policy approval과 rollback note가 필요하다.
- **Label cardinality**: request ID, user ID, random run ID를 label로 올리면 index와 storage pressure가 커진다.
- **Storage assumption**: 현재 backend는 local filesystem이다. 오래된 profile data 삭제나 retention 변경은 guide 범위가 아니라 runbook escalation 대상이다.
- **Language support**: 언어와 runtime에 따라 CPU, memory, goroutine, mutex, block profile 지원 범위가 다르다.

### Common Checks

- `docker compose --profile obs ps pyroscope`
- `docker logs --tail=100 pyroscope`
- `docker compose --profile profiling exec -T pyroscope /usr/bin/profilecli ready --url=http://127.0.0.1:${PYROSCOPE_PORT:-4040}`
- `rg -n 'ingestion_rate_mb: 16|ingestion_burst_size_mb: 32|max_label_names_per_series: 30|backend: filesystem|dir: /var/lib/pyroscope|disable_push: true' infra/06-observability/pyroscope/config/pyroscope.yaml`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0047-pyroscope.md)을 따른다.

### Traceability

- Declared parent: [Pyroscope Operations Policy](../policies/0047-pyroscope.md) (`POL-0047`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](../policies/0047-pyroscope.md) (`POL-0047`), [Runbook](../runbooks/0047-pyroscope.md) (`RUN-0047`)

## Related Documents

- [Observability Compose](../../../infra/06-observability/docker-compose.yml)
- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.
- [Operations index](../README.md)
- [Operations policy](../policies/0047-pyroscope.md)
- [Recovery runbook](../runbooks/0047-pyroscope.md)
