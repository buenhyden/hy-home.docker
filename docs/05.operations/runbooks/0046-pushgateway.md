---
title: "Pushgateway Metrics Buffer Recovery Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0046"
parent_ids:
- "GDE-0046"
created: "2026-05-17"
---

# Pushgateway Metrics Buffer Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

> Scope: 오래된 지표 정리, Pushgateway 준비 상태, 메모리 버퍼 초기화.

이 런북은 Pushgateway 운영 중 발생할 수 있는 stale metric, metric group contamination, memory pressure, and push failure를 복구하기 위한 실행 절차를 정의한다.

### Purpose

Pushgateway의 안정적인 메트릭 버퍼 상태를 유지하고, 비정상적인 메트릭 데이터를 정제하여 가시성 품질을 확보한다.

### When to Use

- 특정 batch or CI job metric이 갱신되지 않고 stale value를 유지할 때.
- Pushgateway metric group이 오염되었거나 high-cardinality label이 잘못 push되었을 때.
- Pushgateway ready endpoint, Traefik route, or internal service endpoint가 실패할 때.
- Prometheus target에서 Pushgateway scrape 상태를 확인해야 하지만 scrape job 존재 여부가 불명확할 때.
- Pushgateway memory usage가 비정상적으로 높고 stale group cleanup만으로 회복되지 않을 때.

## Procedure

### Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Service lifecycle prerequisites

`pushgateway`를 기동하면 건강한 `prometheus`·`grafana` 의존성을 요구한다. `batch-metrics`도 선택 경로지만 HOME 편입 근거가 아니다. 정지·재시작은 모든 메모리 지표를 잃으므로 producer 소유자가 손실을 승인하고 현재 관측만 제한적으로 다시 보낸다. 업무 배치를 재실행해 지표를 복구하지 않는다.

### Checklist

- [ ] 영향받은 `job` and optional `instance` label을 확인한다.
- [ ] Pushgateway container 상태를 확인한다.
- [ ] 내부 ready endpoint와 protected external route 중 최소 하나의 도달성을 확인한다.
- [ ] Prometheus scrape job 존재 여부를 확인하고, 없으면 scrape failure가 아니라 integration gap으로 분류한다.
- [ ] 삭제 대상 metric group이 운영자가 승인한 stale or contaminated group인지 확인한다.

내부 HTTP 명령은 기존 승인된 `obs_net` client에서 실행하며 host DNS를 가정하지 않는다. Gateway 인증 redirect는 backend readiness 성공이 아니다. 현재 두 Prometheus config에 Pushgateway job이 없으므로 실패 target이 아닌 별도 integration gap으로 기록한다.

### Steps

1. 현재 상태와 로그를 캡처한다.

   ```bash
   docker compose --profile obs ps pushgateway
   docker logs --tail=100 pushgateway
   curl -I http://pushgateway:9091/-/ready
   ```

2. Prometheus scrape integration이 필요한 장애인지 확인한다.

   ```bash
   rg -n 'job_name: "pushgateway"|pushgateway:9091|honor_labels' infra/06-observability/prometheus/config/prometheus.yml
   ```

   Match가 없으면 Prometheus target failure로 처리하지 말고, Pushgateway scrape job 추가를 별도 runtime configuration task로 기록한다.

3. 현재 metric group을 조회한다.

   ```bash
   curl -s http://pushgateway:9091/metrics | grep -E 'push_time_seconds|<job_name>'
   ```

4. 오염/stale 판정과 producer 조정 뒤 승인된 정확한 grouping key 하나만 삭제한다. 아래 두 경로는 대안이며 연속 실행하지 않는다. Job-only 삭제는 instance group을 cascade 삭제하지 않는다.

   ```bash
   curl -X DELETE http://pushgateway:9091/metrics/job/stale_batch_job
   curl -X DELETE http://pushgateway:9091/metrics/job/stale_batch_job/instance/worker-01
   ```

5. 상태가 매우 불안정하거나 메모리 임계치에 도달한 경우 Pushgateway를 재시작하여 in-memory buffer를 초기화한다. 현재 Compose는 persistence option을 선언하지 않으므로 process restart는 보관 중인 metric을 잃는다. Producer/alert 영향과 repush 계획이 승인되지 않으면 중단한다.

   ```bash
   docker compose --profile obs restart pushgateway
   ```

6. 작업 노드와 external route에서 도달성을 다시 확인한다.

   ```bash
   curl -I http://pushgateway:9091/-/ready
   curl -I https://pushgateway.${DEFAULT_URL}/-/ready
   ```

### Verification Steps

- [ ] `curl -s http://pushgateway:9091/metrics` 출력에서 삭제 대상 `job` group이 사라졌는지 확인한다.
- [ ] `curl -I http://pushgateway:9091/-/ready`가 successful HTTP status를 반환한다.
- [ ] Prometheus scrape job이 존재하는 환경에서는 Prometheus UI `Targets`에서 `pushgateway` target이 `UP`인지 확인한다.
- [ ] Scrape job이 없는 환경에서는 관련 task or gap evidence에 `prometheus.yml` integration gap을 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=100 pushgateway`
- **Metrics**: `pushgateway_http_requests_total`, `process_resident_memory_bytes`, `push_time_seconds` (Prometheus가 수집할 때)
- **Evidence to Capture**: 상태 명령, 삭제한 지표 group 경로, 전후 `/metrics` 발췌, 수집 job 점검 결과

### Safe Rollback or Recovery Procedure

- 삭제한 metric group은 Git rollback으로 복원되지 않는다. 승인된 producer가 현재 유효한 관측만 repush한다. Metric 복구만을 위해 업무 batch를 재실행하거나 과거 success payload를 replay하지 않는다.
- Restart 후 Pushgateway가 올라오지 않으면 `docker compose --profile obs up -d pushgateway`를 실행하고 healthcheck를 재확인한다.
- Push 실패가 계속되면 batch job log와 network path를 확인하고, 추가 config 변경 전 escalation한다.

### Planned isolated recovery rehearsal

**project 이름만 바꾸어서는 실행할 수 없다.** rehearsal 전에 고정된 container-name,
host port, bind-path, external-network와 route의 충돌을 제거하고 운영 환경으로의
알림 전송과 workflow egress를 차단하는 별도 Compose 정의와 storage 구성을 승인받는다.
이 격리 구성과 해당 subject의 backup 계약을 검토하기 전까지 계획은 NOT_RUN으로
유지한다. 임시 project에 운영 volume을 연결하거나 credential을 복사하지 않는다.

상태: **계획됨, 미실행**. Pushgateway에는 복구할 영속 service state가 없다.

1. image/config identity, producer 목록, grouping-key/metric 계약, Prometheus target label과 현재 optional runtime 관찰을 기록한다. 메모리 내용을 신뢰할 backup으로 내보내지 않는다.
2. test Prometheus가 있는 격리된 project/network에서 추적 중인 Compose를 사용해 다시 생성한다. 통제된 producer에서 합성한 현재 metric만 push한다.
3. health, push/delete 의미, scrape label, 오래된 group 정리와 재시작 시 예상되는 손실을 검증한다. volume이나 `--persistence.file`이 추가되지 않았는지 확인한다.
4. 불일치가 있으면 격리된 optional service를 중지하고 config/image를 되돌린다. 운영 환경에서의 활성화나 producer 변경은 별도로 승인받는다.

## Verification

### Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- 삭제한 metric group path와 삭제 전후 `/metrics` evidence를 기록한다.
- Prometheus scrape job check 결과를 기록한다.
- 실패한 check, 관찰된 증상, 최종 recovery or escalation 상태를 관련 task or incident evidence에 남긴다.

## Rollback and Escalation

### Rollback or Recovery

이 런북에 명시된 cleanup, restart, repush 절차만 사용한다. 이 범위를 벗어난 persistence option, scrape job 추가, route 변경, image 변경은 별도 task와 approval이 필요한 runtime configuration change다. 관찰된 실패가 절차와 다르면 변경을 중단하고 evidence를 보존한 뒤 `## Escalation`으로 이동한다.

### Escalation

verification이 실패하거나, secret exposure risk가 보이거나, metric 삭제 범위가 불명확하거나, runtime config 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 repository owner @buenhyden에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

### Traceability

- Declared parent: [Pushgateway Usage Guide](../guides/0046-pushgateway.md) (`GDE-0046`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0046-pushgateway.md) (`GDE-0046`), [Policy](../policies/0046-pushgateway.md) (`POL-0046`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0046-pushgateway.md)
- [Operations policy](../policies/0046-pushgateway.md)
