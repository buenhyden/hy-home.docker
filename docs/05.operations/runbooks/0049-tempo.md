---
title: "Tempo Readiness and Recovery Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0049"
parent_ids:
- "GDE-0049"
created: "2026-05-17"
---

# Tempo Readiness and Recovery Runbook

## Overview

> Scope: Tempo 준비 상태, OTLP 입력 진단, SeaweedFS 저장소 증거, metrics generator 검증, 재시작과 WAL 증상 보고.

이 런북은 Tempo trace ingestion failure, SeaweedFS-backed storage error, metrics generator failure, query latency, and WAL corruption symptom을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `infra-tempo`의 상태를 확인하고 Alloy → Tempo → SeaweedFS → Prometheus remote write 경로를 검증하며, 데이터 손실 가능성이 있는 WAL or bucket 조치를 별도 승인으로 격리하도록 돕는다.

## When to Use

- Grafana Tempo datasource에서 최근 trace가 검색되지 않을 때.
- Alloy는 trace를 수신하지만 Tempo에 trace가 도착하지 않는다고 의심될 때.
- Tempo log에 S3, bucket, access denied, compaction, WAL 관련 오류가 보일 때.
- Service graph or span metrics가 Prometheus/Grafana에서 보이지 않을 때.
- Config 변경 후 readiness, route, storage, remote write evidence가 필요할 때.

## Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Service lifecycle prerequisites

`tempo` 최초 기동의 `seaweedfs-buckets` 완료 의존성은 bucket provision을 실행할 수 있다. Bucket·정책·secret 준비는 RUN-0024가 소유한다. Monolithic 구성에는 Kafka를 추가하지 않는다. 요구 retention 미선언 상태를 수용 완료로 표시하지 않고, 입력을 중지하고 WAL·object store 복구 시점이 일치하는지 확인한 뒤 변경을 승인한다.

### Checklist

- [ ] `tempo` service, `infra-tempo` container, and `tempo-data` volume 상태를 확인한다.
- [ ] Secret values를 열람하지 않는다. `seaweedfs_s3_tempo_secret_key` ID만 evidence에 기록한다.
- [ ] 문제 유형을 readiness, ingestion, storage, metrics generator, query, WAL symptom 중 하나로 분류한다.
- [ ] WAL deletion, bucket mutation, retention change, or secret rotation이 필요해 보이면 중단하고 repository owner @buenhyden approval을 받는다.

### Steps

1. 현재 service 상태, ready endpoint, 최근 로그를 캡처한다.

   ```bash
   docker compose --profile obs ps tempo
   docker logs --tail=200 infra-tempo
   docker exec infra-tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready
   ```

2. Compose and config boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-stateful-high|image: hy/tempo:|container_name: infra-tempo|user: .10001:10001.|tempo-data|TEMPO_PORT|seaweedfs_s3_tempo_secret_key|tempo.middlewares' infra/06-observability/docker-compose.yml
   rg -n 'endpoint: 0.0.0.0:4317|endpoint: 0.0.0.0:4318|metrics_generator:|remote_write:|url: http://prometheus:9090/api/v1/write|bucket: tempo-bucket|endpoint: seaweedfs-s3:8333|secret_key: \\$\\{S3_SECRET_KEY\\}' infra/06-observability/tempo/config/tempo.yaml
   ```

3. Alloy exporter가 Tempo endpoint를 가리키는지 확인한다.

   ```bash
   rg -n 'otelcol.exporter.otlp "tempo"|endpoint = "tempo:4317"|traces  = \\[otelcol.exporter.otlp.tempo.input\\]' infra/06-observability/alloy/config/config.alloy
   ```

4. Storage or secret symptom은 로그 문구와 bucket/config boundary만 캡처한다. Secret value를 출력하지 않는다.

   ```bash
   docker logs --tail=500 infra-tempo | grep -Ei 's3|bucket|tempo-bucket|seaweedfs|access denied|secret|wal|compact|block'
   ```

5. Metrics generator failure가 의심되면 Tempo config의 `remote_write` endpoint와 Prometheus readiness를 확인한다.

   ```bash
   rg -n 'metrics_generator:|span_metrics:|service_graphs:|remote_write:|url: http://prometheus:9090/api/v1/write' infra/06-observability/tempo/config/tempo.yaml
   docker exec infra-prometheus wget -qO- http://localhost:9090/-/healthy
   ```

6. Readiness or ingestion state가 config와 맞지만 회복되지 않으면 Tempo를 재시작한다. Alloy exporter state도 함께 의심될 때만 Alloy를 같이 재시작한다.

   ```bash
   docker compose --profile obs restart tempo
   docker compose --profile obs restart tempo alloy
   ```

7. WAL corruption or local-block corruption이 의심되면 삭제하지 말고 evidence만 수집한다.

   ```bash
   docker logs --tail=500 infra-tempo | grep -Ei 'wal|corrupt|local block|compactor|failed to replay'
   rg -n 'tempo-data|/var/tempo|tempo-bucket' infra/06-observability/docker-compose.yml infra/06-observability/tempo/config/tempo.yaml
   ```

   이 런북은 WAL 삭제, bucket mutation, or volume file mutation을 검증된 복구 절차로 제공하지 않는다. 데이터 손실 가능성이 있는 조치는 별도 incident/task approval과 backup evidence가 필요하다.

### Retention enforcement gap

[POL-0048](../policies/0048-telemetry-retention.md)은 block 24h, compacted block 1h를 요구하지만 현재 설정에는 둘 다 없다. 선언된 Tempo 기본값은 336h/1h이므로 24h 준수가 입증되지 않는다. Bucket/receiver에 일치한 `rg`를 retention 검증으로 간주하지 않는다. 별도로 확인하고 누락은 통제 실패로 기록한다. 버전에 맞는 별도 구현 수정이 필요하다. Tempo 3은 backend scheduler/worker compaction 설정을 사용하므로 Tempo 2의 `compactor` 블록을 복사하지 않는다. 소스 검증은 실제 삭제나 trace 복원 증거가 아니다.

### Approved LAN integration boundary

Traefik hostname에는 TLS/SSO middleware를 유지한다. 별도로 [POL-0096](../policies/0096-k8s-integration.md#controls)의 기존 k3d 예외에 따라 Tempo HTTP `3200`을 `HOST_LAN_BIND_IP`(공개 기본값 `192.168.0.13`)에 gateway 인증·서비스 TLS 없이 게시한다. 완료된 SPEC-0188 Task의 2026-09-29 owner 승인에 따른 것으로 W5가 만든 예외가 아니다. Loki `auth_enabled: false`는 사용자 인증이 아니며 Tempo에도 native 인증 계층이 없다. Gateway middleware는 직접 포트를 보호하지 않는다.

예외는 지정 cluster 통합 목적과 설정된 LAN 인터페이스로 한정한다. 소스에는 k3d만 식별하는 인증이 없으며 비공개 override, bind 성공, routing/firewall과 실제 도달성은 관찰하지 않았다. 사람은 보호된 hostname을, 기계 검증은 [GDE-0096](../guides/0096-k8s-integration.md)을 따른다. 실제 log/trace payload 대신 상태와 시험 ID만 남긴다. 재바인딩·제거·인증/TLS 추가·노출 확대는 통합 소유자와 조정한 별도 승인 변경이다.

### Verification Steps

- [ ] `docker exec infra-tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready`가 성공한다.
- [ ] Grafana Tempo datasource에서 최근 trace가 조회된다.
- [ ] Service graph or span metrics가 필요한 경우 Prometheus remote write와 Grafana dashboard timestamp가 갱신된다.
- [ ] Storage symptom이면 `tempo-bucket`, SeaweedFS endpoint, secret reference boundary가 policy와 일치한다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 infra-tempo`
- **Health**: Tempo `/ready`, Grafana Tempo datasource, Grafana service graph dashboards
- **Config**: `tempo.yaml`, Alloy Tempo exporter, Prometheus `/-/healthy`
- **Storage**: `tempo-bucket` 경계와 SeaweedFS endpoint `seaweedfs-s3:8333`, `tempo-data` volume
- **Evidence to Capture**: 실패 증상, secret을 제거한 로그, 영향받은 경로·endpoint, 재시작 시각, 최종 복구 또는 보고 상태

### Safe Rollback or Recovery Procedure

- Git-managed `tempo.yaml`, Alloy exporter, or Compose 변경이 원인이면 직전 Git diff 단위로 되돌리고 readiness를 다시 확인한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- WAL deletion, bucket deletion, object mutation, retention change, or secret rotation은 이 런북의 안전 롤백 범위를 벗어난다.

### Planned isolated restore rehearsal

**project 이름만 바꾸어서는 실행할 수 없다.** rehearsal 전에 고정된 container-name,
host port, bind-path, external-network와 route의 충돌을 제거하고 운영 환경으로의
알림 전송과 workflow egress를 차단하는 별도 Compose 정의와 storage 구성을 승인받는다.
이 격리 구성과 해당 subject의 backup 계약을 검토하기 전까지 계획은 NOT_RUN으로
유지한다. 임시 project에 운영 volume을 연결하거나 credential을 복사하지 않는다.

상태: **계획됨, 미실행**. Tempo bucket/WAL 복구에 성공했다고 주장하지 않는다.

1. image/config digest, block/WAL 시간 범위, tenant/trace 기준값, bucket 목록, local-state identity와 checksum을 기록한다. Alloy/producer의 trace 입력을 일시 중단하고, 일관된 `tempo-bucket` snapshot과 정지 상태의 `tempo-data` 복사본을 함께 확보하도록 조율한다.
2. test credential을 사용하고 운영 route가 없는 별도 project/network의 새 bucket/prefix와 local path에 복구한다.
3. Tempo를 시작하고 readiness/WAL replay를 검증한다. 과거 trace를 조회하고 격리된 Alloy를 통해 새 label을 붙인 trace를 전송·조회한 뒤 Grafana와 metrics-generator 동작을 검증한다.
4. 불일치가 있으면 격리된 project를 중지하고 evidence를 보존한다. 수정하지 않은 object/local backup으로 돌아간다. 운영 bucket/path/route 교체는 별도로 승인받는다.

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret values는 기록하지 않는다.
- Trace ingestion 장애는 Alloy exporter check, Tempo ready state, Grafana datasource result를 함께 기록한다.
- Storage/WAL symptom은 로그 발췌, `tempo-data` volume 경계, approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, restart, and Git-managed config rollback만 사용한다. 데이터 손실 가능성이 있는 WAL, bucket, object, retention 조치는 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, destructive data change가 필요하거나, WAL/bucket/object mutation이 필요하거나, 관찰된 상태가 예상 절차와 다르면 repository owner @buenhyden에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Traceability

- Declared parent: [Tempo Usage Guide](../guides/0049-tempo.md) (`GDE-0049`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0049-tempo.md) (`GDE-0049`), [Policy](../policies/0049-tempo.md) (`POL-0049`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0049-tempo.md)
- [Operations policy](../policies/0049-tempo.md)
