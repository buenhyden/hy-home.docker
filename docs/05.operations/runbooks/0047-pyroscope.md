---
title: "Pyroscope Readiness and Recovery Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0047"
parent_ids:
- "GDE-0047"
created: "2026-05-17"
---

# Pyroscope Readiness and Recovery Runbook

## Overview

> Scope: Pyroscope 준비 상태, profile 입력 진단, 로컬 저장소 증거, 재시작과 용량 문제 보고.

이 런북은 Pyroscope profile ingestion gap, Grafana datasource failure, local filesystem storage pressure, high CPU overhead, and config regression을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `infra-pyroscope` 상태를 확인하고 Alloy/Grafana 연결, ingestion limits, local storage boundary를 검증하며, 데이터 삭제나 retention/capacity 변경 같은 위험 조치를 별도 승인으로 격리하도록 돕는다.

## When to Use

- Grafana Pyroscope datasource에서 최근 profile이 보이지 않을 때.
- Alloy `pyroscope.write` endpoint는 선언되어 있지만 profile ingestion gap이 의심될 때.
- `infra-pyroscope` 로그에 storage, ingestion limit, label cardinality, or ready failure 관련 오류가 보일 때.
- Profile ingestion으로 host or container CPU usage가 비정상적으로 높을 때.
- `pyroscope.yaml` 변경 후 readiness, storage, ingestion limit evidence가 필요할 때.

## Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

## Procedure

### Service lifecycle prerequisites

`pyroscope`의 filesystem volume과 선택 Alloy source를 먼저 확인한다. `profiling`은 승인된 HOME 선택에 포함되며 실제 source 수신은 별도 검증한다. 교체·중지 전 입력을 멈추고 일관된 local data를 보존한다. 기간 미선언을 무기한 보존 계약으로 취급하지 않는다.


### Checklist

- [ ] `pyroscope` service, `infra-pyroscope` container, and `pyroscope-data` volume 상태를 확인한다.
- [ ] Profile labels에 high-cardinality or secret-bearing values가 들어갔는지 의심되면 ingestion source를 먼저 식별한다.
- [ ] 문제 유형을 readiness, ingestion, Grafana datasource, storage/capacity, CPU overhead, config regression 중 하나로 분류한다.
- [ ] Data deletion, retention change, storage backend change, or ingestion limit change가 필요해 보이면 중단하고 repository owner @buenhyden approval을 받는다.

### Steps

1. 현재 service 상태, ready endpoint, 최근 로그를 캡처한다.

   ```bash
   docker compose --profile obs ps pyroscope
   docker logs --tail=200 infra-pyroscope
   docker compose --profile profiling exec -T pyroscope /usr/bin/profilecli ready --url=http://127.0.0.1:${PYROSCOPE_PORT:-4040}
   ```

2. Compose and config boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-infra-med|image: grafana/pyroscope:|container_name: infra-pyroscope|pyroscope-data|PYROSCOPE_PORT|/ready|pyroscope.middlewares' infra/06-observability/docker-compose.yml
   rg -n 'http_listen_port: 4040|reporting_enabled: false|data_dir: /var/lib/pyroscope/compactor|ingestion_rate_mb: 16|ingestion_burst_size_mb: 32|max_label_names_per_series: 30|multitenancy_enabled: false|backend: filesystem|dir: /var/lib/pyroscope|disable_push: true' infra/06-observability/pyroscope/config/pyroscope.yaml
   ```

3. Alloy writer와 Grafana datasource가 Pyroscope endpoint를 가리키는지 확인한다.

   ```bash
   rg -n 'pyroscope.write "local_pyroscope"|url = "http://pyroscope:4040"|type: grafana-pyroscope-datasource|url: http://pyroscope:4040' infra/06-observability/alloy/config/config.alloy infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

4. Storage or cardinality symptom은 로그와 capacity evidence를 캡처한다. Profile data를 삭제하지 않는다.

   ```bash
   docker logs --tail=500 infra-pyroscope | grep -Ei 'storage|filesystem|label|cardinality|ingestion|limit|error|warn'
   docker stats --no-stream infra-pyroscope
   rg -n 'pyroscope-data|/var/lib/pyroscope' infra/06-observability/docker-compose.yml infra/06-observability/pyroscope/config/pyroscope.yaml
   ```

5. Readiness or ingestion state가 config와 맞지만 회복되지 않으면 Pyroscope를 재시작한다. Alloy writer state도 함께 의심될 때만 Alloy를 같이 재시작한다.

   ```bash
   docker compose --profile obs restart pyroscope
   docker compose --profile obs restart pyroscope alloy
   ```

6. `pyroscope.yaml`의 bind-mounted 내용만 바뀌었으면 아래 `git diff`로 후보를 확인하고 승인된 정상 revision의 해당 파일만 복원한다. `git diff`는 복원 명령이 아니다. 기존 컨테이너가 같은 bind의 복원 내용을 읽는지 확인한 경우에만 아래 restart를 사용한다. Compose의 config 선택·환경변수·mount·image나 secret bind 또는 파일 inode가 바뀌면 이 분기를 중단하고 [RUN-0086](0086-dependency-version-management.md)의 이전 image/선언 복원과 승인된 recreate 계획으로 넘긴다. Secret 유지보수는 [RUN-0085](0085-openbao.md)를 따른다.

   ```bash
   git diff -- infra/06-observability/pyroscope/config/pyroscope.yaml
   docker compose --profile obs restart pyroscope
   docker compose --profile profiling exec -T pyroscope /usr/bin/profilecli ready --url=http://127.0.0.1:${PYROSCOPE_PORT:-4040}
   ```

   이 런북은 profile data deletion, filesystem mutation, retention change, or ingestion limit change를 검증된 복구 절차로 제공하지 않는다. 데이터 손실 가능성이 있거나 운영 기준을 바꾸는 조치는 별도 incident/task approval과 rollback evidence가 필요하다.

### Profile storage and source limits

두 Alloy 설정에는 Go와 별도 SeaweedFS pprof source가 있다. 선택 파일·target과 제한된 profile query로 수신을 확인하며 writer/receiver readiness만으로 판정하지 않는다. Pyroscope는 선언 volume의 로컬 filesystem과 ingestion/cardinality 한도를 사용한다. 고정 retention은 없고 기본값·disk pressure 정리가 무기한 보존을 보장하지 않는다. 기간 요구는 별도 승인된 설정·용량 검토가 필요하다. wget 존재를 가정하지 않고 선언된 `profilecli ready` probe를 쓴다. Profile/config를 일관되게 보존하고 삭제는 POL-0048을 따른다.

### Verification Steps

- [ ] `profilecli ready` command above exits successfully.
- [ ] Grafana Pyroscope datasource에서 최근 profile이 조회된다.
- [ ] `docker stats --no-stream infra-pyroscope`에서 CPU/memory 사용량이 정상 범위로 돌아온다.
- [ ] Storage symptom이면 `pyroscope-data`, `/var/lib/pyroscope`, and filesystem backend boundary가 policy와 일치한다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 infra-pyroscope`, `docker logs --tail=200 infra-alloy`
- **Health**: Pyroscope `/ready`, Grafana Pyroscope datasource
- **Config**: `pyroscope.yaml`, Alloy `pyroscope.scrape "go_services"`, `pyroscope.scrape "seaweedfs"`(block·mutex profile off: SeaweedFS가 scrape timeout 뒤에야 응답한다)와 `pyroscope.write`(HOME은 `config.home.alloy`), Grafana datasource provisioning(UID `Pyroscope`)
- **Profile sources**: `service_name` label 값을 조회해 수집 중인 서비스를 확인한다. 2026-09-30 기준 11개(alertmanager, alloy, grafana, loki, mng-pg-exporter, node-exporter, prometheus, pyroscope, registry, seaweedfs-s3, tempo)다.

  ```bash
  docker exec infra-grafana sh -c "wget -qO- --header 'Content-Type: application/json' --post-data '{\"name\":\"service_name\",\"start\":$(( ($(date +%s)-600)*1000 )),\"end\":$(( $(date +%s)*1000 ))}' http://pyroscope:4040/querier.v1.QuerierService/LabelValues"
  ```

- **Runtime**: `docker stats --no-stream infra-pyroscope`, `pyroscope-data` volume 경계
- **Evidence to Capture**: 실패 증상, 로그 발췌, 영향받은 profile source·label, 재시작 시각, 최종 복구 또는 보고 상태

### Safe Rollback or Recovery Procedure

- Git-managed `pyroscope.yaml`, Alloy writer, Grafana datasource, or Compose 변경이 원인이면 직전 Git diff 단위로 되돌리고 readiness를 다시 확인한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- Profile data deletion, filesystem mutation, retention change, storage backend change, and ingestion limit change는 이 런북의 안전 롤백 범위를 벗어난다.

### Planned isolated restore rehearsal

**project 이름만 바꾸어서는 실행할 수 없다.** rehearsal 전에 고정된 container-name,
host port, bind-path, external-network와 route의 충돌을 제거하고 운영 환경으로의
알림 전송과 workflow egress를 차단하는 별도 Compose 정의와 storage 구성을 승인받는다.
이 격리 구성과 해당 subject의 backup 계약을 검토하기 전까지 계획은 NOT_RUN으로
유지한다. 임시 project에 운영 volume을 연결하거나 credential을 복사하지 않는다.


상태: **계획됨, 미실행**. Pyroscope 복구에 성공했다고 주장하지 않는다.

1. image/config digest, storage 시간 범위, producer/label 목록과 backup checksum을 기록한다. profile 쓰기와 Pyroscope를 중지한 뒤, 일관된 상태의 `pyroscope-data` snapshot을 생성한다.
2. 운영 route가 없고 통제된 test producer만 있는 별도 project/network의 새 path에 복구한다.
3. Pyroscope를 시작하고 `profilecli ready`를 실행한다. 과거 기준값을 조회하고 label을 붙인 test profile 1개를 수집·조회한 뒤 Grafana 연동을 검증한다. Alloy가 수집한다고 주장하기 전에 실제 source를 확인한다.
4. 불일치가 있으면 격리된 project를 중지하고 evidence를 보존한다. 수정하지 않은 backup으로 돌아간다. 운영 state/route 변경은 별도로 승인받는다.


## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Profile label or payload에 secret-bearing value가 의심되면 원문 값을 기록하지 않는다.
- Ingestion 장애는 Alloy writer check, Pyroscope ready state, Grafana datasource result를 함께 기록한다.
- Storage/capacity symptom은 로그 발췌, `pyroscope-data` volume 경계, approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, restart, and Git-managed config rollback만 사용한다. 데이터 손실 가능성이 있는 profile data deletion, filesystem mutation, retention/storage/ingestion-limit change는 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, destructive data change가 필요하거나, storage/capacity 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 repository owner @buenhyden에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Traceability

- Declared parent: [Pyroscope Usage Guide](../guides/0047-pyroscope.md) (`GDE-0047`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0047-pyroscope.md) (`GDE-0047`), [Policy](../policies/0047-pyroscope.md) (`POL-0047`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0047-pyroscope.md)
- [Operations policy](../policies/0047-pyroscope.md)
