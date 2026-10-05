---
title: "Alloy Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0040"
parent_ids:
- "POL-0040"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - alloy
created: "2026-05-10"
---

# Alloy Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Overview

이 가이드는 `06-observability` 계층의 Grafana Alloy 사용 맥락과 설정 확인 방법을 설명한다. Alloy는 선택된 설정에서 Docker 로그를 Loki로, OTLP trace를 Tempo로, pprof profile을 Pyroscope로 전달한다. Prometheus는 Alloy 자체 지표를 직접 수집하며 현재 두 설정에는 자체 remote-write 경로가 없다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- SRE
- AI Agent

### Purpose

- Alloy compose service, Docker discovery, relabeling, exporter endpoint, and OTLP ingress boundary를 빠르게 파악한다.
- Logs, metrics, traces, and profiling writer pipeline이 어떤 backend로 향하는지 확인한다.
- 복구, restart, endpoint 장애 대응, config rollback은 runbook으로 넘긴다.

### Prerequisites

- `config.alloy` HCL 설정 문법과 OTLP 기본 개념.
- Docker container label and network metadata 확인 권한.
- Alloy UI `https://alloy.${DEFAULT_URL}` 접근 권한.
- Docker socket and container log mount는 read-only로 유지한다.

### Step-by-step Instructions

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-infra-med|image: grafana/alloy:|container_name: infra-alloy|ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|/-/healthy|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

2. Pipeline component boundary를 확인한다.

   ```bash
   rg -n 'discovery.docker|hy-home-infra|loki.source.docker|loki.write|pyroscope.scrape|otelcol.receiver.otlp|otelcol.processor.batch|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy
   ```

3. 현재 pipeline 구조를 이해한다. `ALLOY_CONFIG_FILE`이 두 독립 파일 중 하나를
   `/etc/alloy/config.alloy`로 mount한다. 두 파일은 합쳐 읽히지 않으므로 각각 따로
   검사한다(`alloy fmt <file>`).

   | 파일 | Source selector | Pipelines |
   | --- | --- | --- |
   | `config.home.alloy` | 공개 `.env.example`의 선택값 | Docker 로그·OTLP trace·pprof 수집과 전송 |
   | `config.alloy` | 미지정 시 Compose 기본 선택 | 현재 pipeline은 같지만 파일 선택은 별개 |

   비공개 실행 환경의 선택값은 관찰하지 않았다. 두 파일 모두 Compose project가 `hy-home-infra`인 컨테이너만 유지하고 service/container/project/env/scope를 재표기해 Loki로 로그를 보낸다. 과거 network-name filter와는 다른 경계다. OTLP gRPC/HTTP는 Tempo로 전달한다. 자체 metric은 Prometheus job `alloy`가 한 번 scrape하며 내부 self remote-write는 없다. `pyroscope.scrape "go_services"`는 10개 대상을, 별도 SeaweedFS source는 지원되지 않는 block/mutex를 제외한 profile을 수집해 Pyroscope로 보낸다. 설정이나 collector health만으로 전달 성공을 판정하지 않는다. k3d OTLP 진입은 [POL-0096](../policies/0096-k8s-integration.md)이 관장한다.

4. 애플리케이션 instrumentation은 가능한 OTLP endpoint를 사용한다.

   - gRPC: `alloy:4317`
   - HTTP: `alloy:4318`

5. Pipeline debugging은 Alloy UI에서 수행한다.

   - `https://alloy.${DEFAULT_URL}`에 접속한다.
   - **Graph View**에서 component 연결과 error state를 확인한다.
   - **Component Details**에서 target, receiver, exporter 상태를 확인한다.

### Common Pitfalls

- **Relabeling regex**: `service_name` 또는 `scope` label이 잘못 지정되면 logs/metrics/profile query가 분산된다.
- **Discovery filter**: Docker discovery는 Compose project `hy-home-infra`만 유지한다. 이 프로젝트 밖 컨테이너는 network 이름과 관계없이 의도적으로 제외한다.
- **Exporter assumption**: Downstream backend가 unhealthy이면 Alloy pipeline이 정상이어도 telemetry가 보이지 않을 수 있다.
- **Profiling assumption**: `pyroscope.write` endpoint가 있다고 해서 profile source가 자동으로 수집되는 것은 아니다. SPEC-0193부터 `go_services`의 10개 대상과 별도 SeaweedFS source가 선언된 11개 pprof 대상을 수집한다. eBPF는 쓰지 않는다.
- **Config file selection**: `ALLOY_CONFIG_FILE`은 파일 하나를 선택한다. 공개 기본값으로 비공개 runtime 선택을 단정할 수 없다. 지원하는 두 파일을 검토하고 RUN-0040에서 승인한 선택 설정만 적용한다.
- **Self metrics**: Alloy 자체 metric은 Prometheus job `alloy`가 직접 수집한다. Alloy 안에서 self remote-write를 두면 같은 series가 `integrations/self`로 한 번 더 들어온다.
- **Docker socket boundary**: Docker socket and container log mounts는 read-only여야 한다.

### Source-backed operating contract

- **목적·분류·구현 소유권**: `alloy`는 `HOME` telemetry collector이며 `obs`, `logs`, `tracing`, `profiling`으로 선택한다. [Compose](../../../infra/06-observability/docker-compose.yml)와 [Alloy config](../../../infra/06-observability/alloy/config/config.alloy)가 구현을 소유한다.
- **흐름·의존성**: 읽기 전용 Docker socket/container log는 Loki로, OTLP 4317/4318 입력은 Tempo로 전달된다. Prometheus는 Alloy 자체 metric을 scrape하며, 선택 가능한 두 config 모두 pprof source와 Pyroscope writer를 선언한다. source 선언만으로 profile 수신이 입증되지는 않는다. backend depends_on 항목은 선택적이므로(`required: false`) 일부 구성만 선택하면 모든 backend 없이도 시작될 수 있다. Docker와 선언된 network는 여전히 전제 조건이다.
- **상태·보안**: config·host log mount는 읽기 전용이며 Docker socket 접근은 민감하다. `alloy-data:/var/lib/alloy`와 선언된 storage path, UID/GID를 유지한다. State와 전송 중인 telemetry의 복구 가능 범위를 구분하며 유실·중복을 승인 없이 완전 복구로 처리하지 않는다. 현재 변경 절차는 [RUN-0040](../runbooks/0040-alloy.md)을 따른다. 파일 교체로 bind inode가 달라졌거나 port·mount·Compose 설정이 바뀌면 단순 restart로 적용을 보장하지 않으며 승인된 recreate와 state 보존 검토가 필요하다.

> Historical evidence (not current authority; source: Git history):
> Source commit: `22475253cacfa452f92fb7f917585e634ea6253f`; path: `docs/05.operations/guides/0040-alloy.md`.
>
> - **State/security**: config and host log mounts are read-only; Docker socket access is security-sensitive. `alloy-data:/var/lib/alloy` is mounted and the command now passes `--storage.path=/var/lib/alloy/data`; the previous command override had dropped the image default, so positions and WAL lived in the container layer and were lost on recreate. The container runs as the image's `alloy` user (UID 473) with the host docker group (`DOCKER_GID`) because root without capabilities cannot write the 473-owned state directory; the first attempt as root crash-looped on `mkdir /var/lib/alloy/data: permission denied` on 2026-09-21 and was rolled back within about three minutes. The first recreate with the fix starts without the old positions, which can re-send or skip recent Docker log lines; Loki may reject out-of-order duplicates. Config edits apply through `POST /-/reload` only when the mounted file inode is unchanged; editors that replace the file need a container restart. Changing ports or mounts needs a recreate. In-flight telemetry can be lost and is not a guaranteed recovery asset.

- **자원·정상 사용**: source의 CPU/memory limit은 여유 용량을 뜻하지 않는다. 저장소 root에서 `docker compose --profile obs config --quiet`로 렌더링하고 Alloy config를 검증한 뒤, downstream 쓰기와 범위를 제한한 retry/WAL 신호를 확인한다.
- **수명 주기**: config와 component별로 검증된 state를 보존한다. 전송을 drain하거나 문서화된 전송 중 손실을 허용하고, 고정된 version을 하나씩 update한다. component 호환성을 검증한 뒤 log/trace/metric을 확인하며, source가 있을 때만 profiling이 이루어진다고 주장한다.
- **공식 문서·license**: 공식 [Alloy 동작 방식](https://grafana.com/docs/alloy/latest/introduction/how-alloy-works/)과 [remote_write/WAL](https://grafana.com/docs/alloy/latest/reference/components/prometheus/prometheus.remote_write/) 문서를 따른다. Grafana Alloy에는 Apache-2.0 license가 적용된다.

### Common Checks

- `docker compose --profile obs ps alloy`
- `docker logs --tail=100 infra-alloy`
- `rg -n 'discovery.docker|loki.source.docker|pyroscope.scrape|otelcol.receiver.otlp|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy`
- `rg -n 'ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0040-alloy.md)을 따른다.

### Traceability

- Declared parent: [Alloy Operations Policy](../policies/0040-alloy.md) (`POL-0040`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](../policies/0040-alloy.md) (`POL-0040`), [Runbook](../runbooks/0040-alloy.md) (`RUN-0040`)

## Related Documents

- [Runtime image declarations](../../../infra/06-observability/docker-compose.yml)
- [Operations index](../README.md)
- [Operations policy](../policies/0040-alloy.md)
- [Recovery runbook](../runbooks/0040-alloy.md)
