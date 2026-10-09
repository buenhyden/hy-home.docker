---
title: "Alloy Readiness and Pipeline Recovery Runbook"
version: "1.0.6"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0040"
parent_ids:
- "GDE-0040"
created: "2026-05-17"
---

# Alloy Readiness and Pipeline Recovery Runbook

## Overview

이 런북은 Grafana Alloy의 준비 상태 점검, Docker discovery 증거, OTLP 입력 진단, downstream exporter 검증, 재시작과 설정 rollback을 다룬다. 설명은 [GDE-0040](../guides/0040-alloy.md)과 [POL-0040](../policies/0040-alloy.md)에 두고, 여기서는 실행 가능한 진단, 안전한 restart, evidence 수집, escalation 기준만 둔다.

## Trigger and Preconditions

다음 경우에 사용한다.

- Alloy UI 또는 `/-/healthy` endpoint가 실패할 때.
- Docker 로그, metric, trace가 backend에 도착하지 않을 때.
- OTLP trace client가 `alloy:4317` 또는 `alloy:4318`로 보내지 못할 때. 이 두 port는 trace만 전달하며 여기에 보낸 metric은 오류 없이 버려진다.
- k6 품질 metric(`k6_*`)이 Prometheus에 없을 때. 품질 metric은 `config.home.alloy`의 인증 수신기 `alloy:4319`로만 들어온다(SPEC-0214).
- 특정 backend exporter에서 connection refused나 timeout이 보일 때.
- 설정 변경 후 component graph, label, exporter 상태 검증이 필요할 때.

사전 조건은 다음과 같다.

- `alloy` service, `alloy` container, `alloy-data` volume, 읽기 전용 Docker mount 상태를 확인한다.
- 문제를 readiness, Docker discovery/logs, OTLP ingress, downstream exporter, relabel/label drift, config regression 중 하나로 분류한다.
- Docker socket/container mount를 read-write로 바꾸거나 exporter endpoint, port를 바꿔야 해 보이면 중단하고 @buenhyden의 승인을 받는다.
- secret이 담긴 label이나 high-cardinality label을 발견해도 원문 값을 기록하지 않는다.
- `alloy`의 `required: false` backend는 없어도 기동된다. 선택한 설정과 필요한 Loki, Tempo, Pyroscope endpoint를 확인한 뒤 신호별 수신을 검증한다.
- 중지나 재생성 전에 position/state와 로그 유실, 중복 허용 범위를 기록한다. 설정 선택 변경에는 재생성이 필요하며 reload 지원 여부를 임의로 가정하지 않는다.

## Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 쓰고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단, memory/queue 손실, 부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

log를 보존하기 전에 payload, credential, header/cookie, private path를 제거하고 명령, 시각, 상태, 제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패, 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. 설정 rollback은 data/schema 복구가 아니다. 전체 기동과 중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 절차를 쓴다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 쓰는 자격 증명과 상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

비공개 환경을 출력하지 않고 `ALLOY_CONFIG_FILE`의 선택 이름을 확인한 뒤 해당 tracked 파일과 지원 대안을 읽는다. 아래 예시는 `config.alloy`이며 실제로 `config.home.alloy`를 선택했다면 파일 이름을 바꾼다. reload로 mount/port를 바꿀 수 없고 inode가 바뀐 파일에는 재시작이나 재생성 결정이 필요하다. 상태 경로를 바꾸기 전에 [GDE-0040](../guides/0040-alloy.md)의 positions 손실 이력을 확인한다.

### Steps

1. 현재 service 상태, 최근 로그, route/health signal을 캡처한다.

   ```bash
   docker compose --profile obs ps alloy
   docker logs --tail=200 alloy
   docker exec alloy bash -lc 'exec 3<>/dev/tcp/localhost/12345; printf "HEAD /-/healthy HTTP/1.1\r\nHost: localhost\r\n\r\n" >&3; timeout 2 head -1 <&3'
   ```

2. Compose service boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-infra-med|image: grafana/alloy:|container_name: alloy|ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|/-/healthy|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   rg -n '/var/lib/docker/containers:/var/lib/docker/containers:ro|/var/run/docker.sock:/var/run/docker.sock:ro|alloy-data:/var/lib/alloy:rw' infra/06-observability/docker-compose.yml
   ```

3. Pipeline config boundary를 확인한다.

   ```bash
   rg -n 'discovery.docker|hy-home-infra|loki.source.docker|loki.write|pyroscope.scrape|otelcol.receiver.otlp|otelcol.processor.batch|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy
   ```

4. Downstream exporter failure가 의심되면 현재 선택한 backend만 확인한다. Optional dependency가 없어도 collector는 시작할 수 있으며 health는 delivery 증거가 아니다.

   ```bash
   docker exec prometheus wget -qO- http://localhost:9090/-/healthy
   docker exec loki wget -qO- http://127.0.0.1:3100/ready
   docker exec tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready
   docker exec pyroscope profilecli ready --url=http://localhost:4040
   ```

5. OTLP ingress 장애가 의심되면 Compose port binding과 Alloy config를 확인한다.

   ```bash
   rg -n 'ALLOY_OTLP_GRPC_HOST_PORT|ALLOY_OTLP_HTTP_HOST_PORT|4317|4318' infra/06-observability/docker-compose.yml infra/06-observability/alloy/config/config.alloy
   ```

   k6 품질 metric이 없으면 `config.home.alloy`가 선택되었는지, `alloy`에 secret
   `quality_otlp_token`이 부여되었는지, run별 `metrics-ingress` relay가 같은 token으로
   `alloy:4319`에 보내는지 확인한다. relay와 Alloy는 둘 다 internal network
   `quality_otlp_net`에 있어야 한다. Alloy가 이 network에 없으면 Alloy를 다시 만든다. token 파일이 비어 있으면 Alloy는 요청을 받지 않고
   연결을 끊으므로, HOME Alloy를 다시 만들기 전에 파일이 비어 있지 않은지 확인한다. 값은
   출력하지 않는다.

   ```bash
   rg -n 'quality_otlp_token|4319|otelcol.auth.bearer' infra/06-observability/docker-compose.yml infra/06-observability/alloy/config/config.home.alloy
   test -s secrets/observability/alloy/quality_otlp_token.txt && echo non-empty
   docker network inspect quality_otlp_net --format '{{range .Containers}}{{.Name}} {{end}}'
   ```

6. Label drift or discovery gap이 의심되면 relabel rules와 Compose project filter를 확인한다.

   ```bash
   rg -n 'target_label  = "service_name"|target_label  = "container_name"|target_label = "scope"|regex         = "hy-home-infra"|replacement   = "infra"' infra/06-observability/alloy/config/config.alloy
   ```

7. Config가 현재 정책과 일치하지만 runtime state가 회복되지 않으면 Alloy를 재시작한다.

   ```bash
   docker compose --profile obs restart alloy
   ```

8. `config.alloy`의 bind-mounted 내용만 바뀌었으면 아래 `git diff`로 후보를 확인하고 승인된 정상 revision의 해당 파일만 복원한다. `git diff`는 복원 명령이 아니다. 기존 컨테이너가 같은 bind의 복원 내용을 읽는지 확인한 경우에만 아래 restart를 사용한다. Compose의 config 선택·환경변수·mount·image나 secret bind 또는 파일 inode가 바뀌면 이 분기를 중단하고 [RUN-0086](0086-dependency-version-management.md)의 이전 image/선언 복원과 승인된 recreate 계획으로 넘긴다. Secret 유지보수는 [RUN-0085](0085-openbao.md)를 따른다. `ALLOY_CONFIG_FILE`로 실제 선택된 파일에만 적용하며 `config.home.alloy`를 선택했다면 아래 diff 대상도 그 파일로 바꾼다.

   ```bash
   git diff -- infra/06-observability/alloy/config/config.alloy
   docker compose --profile obs restart alloy
   docker logs --tail=100 alloy
   ```

   이 런북은 mount permission relaxation, Docker socket read-write access, exporter endpoint change, OTLP port change, or high-cardinality relabel expansion을 검증된 복구 절차로 제공하지 않는다. 해당 변경은 별도 approval과 rollback evidence가 필요하다.

#### Planned isolated recovery rehearsal

**project 이름만 바꾸어서는 실행할 수 없다.** rehearsal 전에 고정된 container-name,
host port, bind-path, external-network와 route의 충돌을 제거하고 운영 환경으로의
알림 전송과 workflow egress를 차단하는 별도 Compose 정의와 storage 구성을 승인받는다.
이 격리 구성과 해당 subject의 backup 계약을 검토하기 전까지 계획은 NOT_RUN으로
유지한다. 임시 project에 운영 volume을 연결하거나 credential을 복사하지 않는다.

상태: **계획됨, 미실행**. 전송 중이던 telemetry를 정확히 복구할 수 있다고 주장하지 않는다.

1. image/config digest, 활성 component, downstream endpoint, queue/WAL metric과 `/var/lib/alloy`를 실제로 사용하는 component가 있는지 기록한다. 가능한 경우 test producer의 전송을 일시 중단한다.
2. test Loki/Tempo/Prometheus/Pyroscope endpoint에 연결된 별도 project/network에 추적 중인 config와 검증된 component state만 복구한다. host/Docker 접근은 필요한 최소한의 읽기 전용으로 유지한다.
3. config를 검증하고 Alloy를 시작한 뒤, label을 붙인 test log/trace/metric 입력을 주입한다. 구성된 각 downstream과 retry/WAL 동작을 검증한다. profile은 source component를 확인한 후에만 test한다.
4. 불일치가 있으면 격리된 collector를 중지하고 log를 보존한다. config/image를 rollback하고, 운영 환경을 변경하기 전에 허용한 전송 중 data 손실을 기록한다.

## Verification

- [ ] `docker compose --profile obs ps alloy`에서 `alloy` service가 running이다.
- [ ] Alloy UI `https://alloy.${DEFAULT_URL}`의 pipeline graph에 failed component가 없다.
- [ ] 영향받은 경로에서 로그는 Loki에, Alloy 자체 metric은 Prometheus에, OTLP trace는 Tempo에 나타난다.
- [ ] k6 품질 metric이 영향 범위라면 Prometheus에 해당 `instance=<run_id>-a<attempt>`의 `k6_*` series가 있고, token 없는 요청은 4319에서 401을 받는다.
- [ ] Pyroscope writer endpoint는 설정된 상태이며, profile 수집은 source가 명시적으로 연결된 경우에만 주장한다.
- [ ] 문서나 config만 바꿨다면 관련 repository validation을 실행하고 evidence에 기록한다.

수집할 evidence는 다음과 같다.

- 실행한 명령, timestamp, 운영자나 agent의 조치.
- 실패한 component 이름, backend endpoint, log excerpt, 영향받은 telemetry 신호, 재시작 시각, 최종 복구 또는 보고 상태.
- Alloy `/-/healthy`, Alloy UI graph, `docker logs --tail=200 alloy`.
- mount나 endpoint 변경이 필요해 보이면 승인 상태.
- secret이 담긴 label이나 payload가 의심되면 원문 값은 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

- Git으로 관리하는 설정, Compose, downstream endpoint 변경이 원인이면 직전 Git diff 단위로 되돌리고 Alloy를 재시작한다.
- Runtime restart는 `obs` profile compose 명령만 쓴다.
- Docker mount 권한 완화, exporter endpoint 변경, OTLP port 변경, relabel cardinality 확대는 이 런북의 안전 롤백 범위를 벗어나므로 Escalation으로 넘긴다.

### Escalation

verification이 실패하거나, secret 노출 위험이 보이거나, Docker mount/endpoint/port 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 repository owner @buenhyden에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

### Traceability

- Declared parent: [Alloy Usage Guide](../guides/0040-alloy.md) (`GDE-0040`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0040-alloy.md) (`GDE-0040`), [Policy](../policies/0040-alloy.md) (`POL-0040`)

- [Runtime image declarations](../../../infra/06-observability/docker-compose.yml)
- [Operations index](../README.md)
- [Usage guide](../guides/0040-alloy.md)
- [Operations policy](../policies/0040-alloy.md)
