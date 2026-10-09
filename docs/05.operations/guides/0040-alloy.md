---
title: "Alloy Usage Guide"
version: "1.1.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
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

Grafana Alloy는 HOME 관측 계층의 telemetry collector다. 서비스 `alloy`는 `obs`, `logs`, `tracing`, `profiling` profile로 선택하며 [Compose](../../../infra/06-observability/docker-compose.yml)가 구현을 소유한다.

Alloy는 세 가지 신호를 전달한다.

- Docker 로그는 Loki로 보낸다.
- OTLP trace는 Tempo로 보낸다.
- pprof profile은 Pyroscope로 보낸다.

Alloy 자체 지표는 Prometheus job `alloy`가 직접 scrape한다. 두 설정 파일 모두 Alloy 안에 자체 remote-write를 두지 않는다. 같은 series가 `integrations/self`로 한 번 더 들어오기 때문이다(SPEC-0193).

## Audience and Goal

대상 독자는 개발자, 운영자, SRE, AI Agent다. 이 가이드로 다음을 빠르게 파악한다.

- Alloy 서비스 경계, Docker discovery, relabel, OTLP 입력 경계.
- 로그, trace, profile이 어느 backend로 가는지.
- 어떤 설정 파일이 어떤 역할을 하는지.

복구, restart, endpoint 장애 대응, 설정 rollback은 [RUN-0040](../runbooks/0040-alloy.md)이 맡는다.

## Usage

### 설정 파일의 역할

`ALLOY_CONFIG_FILE`이 두 파일 중 하나를 `/etc/alloy/config.alloy`로 mount한다. 값이 없으면 Compose 기본값 `config.alloy`를 쓰고, 공개 `.env.example`은 `config.home.alloy`를 선택한다. 두 파일은 합쳐 읽히지 않으므로 각각 따로 검사한다(`alloy fmt <file>`). 비공개 실행 환경의 선택값은 관찰하지 않았다(미검증).

| 파일 | 역할 |
| --- | --- |
| [`config.alloy`](../../../infra/06-observability/alloy/config/config.alloy) | 기본 파이프라인이다. Docker 로그를 Loki로, OTLP trace를 Tempo로, pprof를 Pyroscope로 보낸다. 품질 metric 수신기는 없다. |
| [`config.home.alloy`](../../../infra/06-observability/alloy/config/config.home.alloy) | 기본 파이프라인에 품질 OTLP metric 전용 경로를 더한 HOME 설정이다. 인증 수신기(HTTP 4319, host 비공개, secret `quality_otlp_token`)가 받은 metric을 속성 제한, delta-to-cumulative 변환, label 제한을 거쳐 Prometheus로 remote write한다(SPEC-0214). |

두 파일이 공유하는 동작은 다음과 같다.

- 로그: Compose project가 `hy-home-infra`인 컨테이너만 유지하고 `service_name`, `container_name`, `compose_project`, `env`, `scope`를 다시 표기해 Loki로 보낸다.
- trace: OTLP gRPC 4317과 HTTP 4318을 받아 Tempo로 전달한다. 이 두 port는 trace만 처리하며 metric은 버려진다.
- profile: `pyroscope.scrape "go_services"`가 10개 대상을, 별도 `pyroscope.scrape "seaweedfs"`가 지원되지 않는 block/mutex를 제외한 profile을 수집해 Pyroscope로 보낸다. eBPF는 쓰지 않는다.

`config.home.alloy`의 OTLP trace 수신 주석에 따르면 hy-home.k8s의 Istio가 `192.168.0.13:4317`로 보낸다. k3d OTLP 진입은 [POL-0096](../policies/0096-k8s-integration.md)이 관장한다.

### 정상 사용

- 애플리케이션 instrumentation은 가능한 OTLP endpoint를 쓴다. gRPC는 `alloy:4317`, HTTP는 `alloy:4318`이다.
- Pipeline debugging은 Alloy UI `https://alloy.${DEFAULT_URL}`에서 한다. **Graph View**에서 component 연결과 error state를, **Component Details**에서 target, receiver, exporter 상태를 본다.
- 설정이나 collector health만으로 전달 성공을 판정하지 않는다. backend에서 실제 수신을 확인한다.

### 구현 경계

- **흐름·의존성**: 읽기 전용 Docker socket과 container log를 Loki로, OTLP 입력을 Tempo로 보낸다. `depends_on`의 Prometheus, Loki, Tempo는 `required: false`이므로 일부 구성만 선택해도 시작된다. Docker와 선언된 network는 여전히 전제 조건이다.
- **네트워크**: `edge_net`, `obs_net`, `quality_otlp_net`에 붙는다. OTLP 4317/4318은 `${HOST_LAN_BIND_IP:-192.168.0.13}`에 publish한다. Alloy UI는 Traefik 경로(`gateway-standard-chain@file,sso-errors@file,sso-auth@file`)로 노출한다.
- **node-exporter 접근**: SPEC-0225 이후 node-exporter는 host network namespace에서 `obs_net` gateway에 bind한다. Alloy는 `extra_hosts`로 `node-exporter:10.250.5.1`을 선언해 pprof 대상 이름을 그대로 유지한다.
- **상태·보안**: config와 host log mount는 읽기 전용이다. Docker socket 접근은 민감하다. `alloy-data:/var/lib/alloy`와 `--storage.path=/var/lib/alloy/data`, UID/GID `473:473`을 유지한다. 전송 중 telemetry는 복구 자산이 아니다. 파일 inode가 바뀌었거나 port, mount, Compose 설정이 바뀌면 restart만으로 적용을 보장하지 않으며 승인된 recreate와 state 보존 검토가 필요하다.

> Historical evidence (not current authority; source: Git history):
> Source commit: `22475253cacfa452f92fb7f917585e634ea6253f`; path: `docs/05.operations/guides/0040-alloy.md`.
>
> - **State/security**: config and host log mounts are read-only; Docker socket access is security-sensitive. `alloy-data:/var/lib/alloy` is mounted and the command now passes `--storage.path=/var/lib/alloy/data`; the previous command override had dropped the image default, so positions and WAL lived in the container layer and were lost on recreate. The container runs as the image's `alloy` user (UID 473) with the host docker group (`DOCKER_GID`) because root without capabilities cannot write the 473-owned state directory; the first attempt as root crash-looped on `mkdir /var/lib/alloy/data: permission denied` on 2026-09-21 and was rolled back within about three minutes. The first recreate with the fix starts without the old positions, which can re-send or skip recent Docker log lines; Loki may reject out-of-order duplicates. Config edits apply through `POST /-/reload` only when the mounted file inode is unchanged; editors that replace the file need a container restart. Changing ports or mounts needs a recreate. In-flight telemetry can be lost and is not a guaranteed recovery asset.

- **자원·정상 사용**: Compose의 CPU/memory limit은 여유 용량을 뜻하지 않는다. 저장소 root에서 `docker compose --profile obs config --quiet`로 렌더링하고 Alloy config를 검증한 뒤, downstream 쓰기와 retry/WAL 신호를 확인한다.
- **수명 주기**: config와 component별로 검증된 state를 보존한다. 전송을 drain하거나 문서화된 전송 중 손실을 허용하고, 고정된 version을 하나씩 update한다. component 호환성을 검증한 뒤 log/trace/metric을 확인한다.
- **공식 문서·license**: 공식 [Alloy 동작 방식](https://grafana.com/docs/alloy/latest/introduction/how-alloy-works/)과 [remote_write/WAL](https://grafana.com/docs/alloy/latest/reference/components/prometheus/prometheus.remote_write/) 문서를 따른다. Grafana Alloy에는 Apache-2.0 license가 적용된다.

### Common Checks

- `docker compose --profile obs ps alloy`
- `docker logs --tail=100 alloy`
- Compose 경계: `rg -n 'service: template-infra-med|image: grafana/alloy:|container_name: alloy|ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|/-/healthy|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml`
- Pipeline 경계: `rg -n 'discovery.docker|hy-home-infra|loki.source.docker|loki.write|pyroscope.scrape|otelcol.receiver.otlp|otelcol.processor.batch|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy`
- 품질 metric 수신기: `rg -n 'quality_otlp_token|otelcol.auth.bearer|0.0.0.0:4319|labelkeep' infra/06-observability/alloy/config/config.home.alloy`

주의할 점은 다음과 같다.

- `service_name` 또는 `scope` relabel regex가 틀리면 log, profile 조회가 갈라진다.
- Docker discovery는 Compose project `hy-home-infra`만 유지한다. 이 밖의 컨테이너는 network 이름과 관계없이 의도적으로 제외한다.
- backend가 unhealthy이면 pipeline이 정상이어도 telemetry가 보이지 않을 수 있다.
- `pyroscope.write` endpoint가 있다고 profile이 자동 수집되지는 않는다. 선언된 pprof 대상(10개 + SeaweedFS 1개)만 수집한다.
- `ALLOY_CONFIG_FILE` 공개 기본값으로 비공개 runtime 선택을 단정하지 않는다. 지원하는 두 파일을 검토하고 RUN-0040에서 승인한 선택 설정만 적용한다.

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback, escalation은 [RUN-0040 절차](../runbooks/0040-alloy.md#procedure)를 따른다.

### Traceability

- Declared parent: [Alloy Operations Policy](../policies/0040-alloy.md) (`POL-0040`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](../policies/0040-alloy.md) (`POL-0040`), [Runbook](../runbooks/0040-alloy.md) (`RUN-0040`)

## Related Documents

- [Runtime image declarations](../../../infra/06-observability/docker-compose.yml)
- [Operations index](../README.md)
- [Operations policy](../policies/0040-alloy.md)
- [Recovery runbook](../runbooks/0040-alloy.md)
