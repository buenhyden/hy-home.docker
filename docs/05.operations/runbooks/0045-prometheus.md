---
title: "Prometheus Readiness and Recovery Runbook"
version: "1.2.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0045"
parent_ids:
- "GDE-0045"
created: "2026-05-17"
---

# Prometheus Readiness and Recovery Runbook

## Overview

이 런북은 Prometheus 준비 상태, 설정·rule 검증, lifecycle reload, scrape target 진단, 재시작, TSDB 증상 보고를 다룬다. 장애, scrape target 실패, alert rule 평가 실패, reload, TSDB 손상 증상에 대응한다.

운영자가 `prometheus` 상태를 안전하게 확인하고, config/rule 변경을 검증한 뒤 reload나 restart를 수행하게 한다. 데이터 손실 가능성이 있는 TSDB 조치는 별도 승인으로 격리한다. 정책과 가이드의 설명은 반복하지 않고 실행 가능한 확인 절차와 증거 기준만 둔다.

## Trigger and Preconditions

다음 중 하나일 때 사용한다.

- Prometheus UI나 `/-/healthy` endpoint가 실패한다.
- Grafana dashboard에서 metrics가 비어 있거나 오래된 값으로 보인다.
- 특정 scrape target이 `DOWN`이거나 `PrometheusAllTargetsMissing` 계열 alert가 발생한다.
- `PrometheusRuleEvaluationFailures`나 rule loading error가 발생한다.
- `prometheus.yml`이나 `alert_rules/`를 바꾼 뒤 reload가 필요하다.
- TSDB 손상, compaction 실패, WAL 관련 로그가 보인다.

시작 전에 다음을 확인한다.

- [ ] 변경 전 `prometheus.yml`, alert rule files, compose service boundary를 확인한다.
- [ ] Secret values를 열람하지 않는다. Secret ID and file reference만 evidence에 기록한다.
- [ ] 문제 유형을 readiness, config/rule, scrape target, route, storage/TSDB 중 하나로 분류한다.
- [ ] 데이터 삭제, WAL 제거, volume mutation이 필요해 보이면 즉시 중단하고 repository owner @buenhyden approval을 받는다.

### Service lifecycle prerequisites

`prometheus`의 선택 config, rule 파일과 세 secret mount가 준비되어야 한다. `node-exporter`의 textfile host 경로는 자동 생성되지 않으며 `dcgm-exporter`는 호환되는 GPU runtime이 필요하다. DCGM에는 Compose healthcheck가 없으므로 수집 target과 지원 metric을 확인한다. 두 exporter는 자체 데이터 백업이나 별도 사용자 자격 증명 회전 대상이 아니다. exporter 교체·중지는 관측 공백과 label 연속성을 검토하고 Prometheus TSDB 복구와 구분한다.

## Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Host and GPU exporter boundary

`node-exporter`는 `obs`/`obs-host`/`dev`로 선택하는 HOME host 관측기다. 통제는 [POL-0045](../policies/0045-prometheus.md#host-and-gpu-exporter-boundary)가 소유하고, 이 절은 운영 전제만 둔다.

- 제한된 collector를 유지하고 기본 collector에 `processes`, `tcpstat`을 추가한다. Network·socket collector가 host를 보도록 host network namespace에서 실행하며, listener는 `obs_net`의 host 쪽 주소(기본 gateway `10.250.5.1:9100`)에만 묶는다. 기본적으로 LAN에서 route되지 않지만, LAN host가 직접 route를 추가하면 닿을 수 있고 internal이 아닌 bridge network의 container도 닿는다.
- Host network 서비스에는 Compose가 network를 만들지 않는다. `obs_net`이 없으면 bind가 실패해 재시작을 반복한다. `obs`/`obs-host`/`dev` profile에서는 Prometheus나 cAdvisor가 `obs_net`을 먼저 만든다.
- Prometheus와 Alloy는 `extra_hosts`로 이 주소를 `node-exporter` 이름에 연결하므로 scrape target과 `instance` label은 바뀌지 않는다. `obs_net`을 다른 subnet으로 다시 만들면 listen 주소와 두 서비스의 `extra_hosts`를 함께 바꾼다.
- Backup textfile 경로는 `create_host_path: false`여서 소유자가 미리 준비해야 한다. HTTP probe와 Prometheus target은 따로 확인한다.
- `dcgm-exporter`는 `obs-gpu` 전용이며 Compose healthcheck가 없다. GPU, DCGM metric, scrape 상태를 구분하고, GPU 유지보수는 [RUN-0055](../runbooks/0055-gpu-recovery.md)가 맡는다.

### Diagnosis and reload

1. 현재 service 상태와 최근 로그를 캡처한다.

   ```bash
   docker compose --profile obs ps prometheus
   docker logs --tail=200 prometheus
   docker exec prometheus wget -qO- http://localhost:9090/-/healthy
   ```

2. Config와 rule syntax를 검증한다.

   ```bash
   docker exec prometheus promtool check config /etc/prometheus/prometheus.yml
   docker exec prometheus /bin/sh -c 'promtool check rules /etc/prometheus/alert_rules/*.yml'
   ```

   두 번째 명령은 container 내부 `/bin/sh`가 rule glob을 확장하도록 shell program을 따옴표로 감싼다. `/run/secrets/openbao_token` 미준비로 config 검사가 멈추면 그 전제를 별도 실패로 기록한다. Rule 검사는 문법 증거일 뿐 credential이나 scrape readiness를 증명하지 않는다.

3. Scrape target 장애는 Prometheus `Targets` page에서 failing job을 확인하고, Prometheus container에서 target endpoint를 직접 확인한다.

   ```bash
   docker exec prometheus wget -qO- http://<target-service-name>:<metrics-port>/metrics
   ```

   Target이 `/metrics`가 아닌 custom path를 사용하면 `prometheus.yml`의 `metrics_path`를 기준으로 endpoint를 바꾼다.

4. Config or rule 변경이 검증을 통과했고 service가 healthy하면 lifecycle reload를 수행한다.

   ```bash
   docker exec prometheus wget -qO- --post-data='' http://localhost:9090/-/reload
   ```

5. Reload 후에도 service가 unhealthy하거나 runtime state가 회복되지 않으면 profile 포함 compose 명령으로 restart한다.

   ```bash
   docker compose --profile obs restart prometheus
   ```

6. TSDB corruption, compaction failure, WAL 관련 로그가 보이면 삭제 조치를 하지 말고 evidence를 수집한다.

   ```bash
   docker logs --tail=500 prometheus | grep -Ei 'tsdb|wal|compact|corrupt|block'
   rg -n 'prometheus-data|/prometheus|web.enable-(lifecycle|admin-api)' infra/06-observability/docker-compose.yml
   ```

   이 런북은 WAL 삭제나 TSDB file mutation을 검증된 복구 절차로 제공하지 않는다. 데이터 손실 가능성이 있는 조치는 별도 incident/task approval과 backup evidence가 필요하다.

### Datastore observation alerts

`up`은 scrape 연결만 뜻한다. DB 접속은 `pg_up`·`redis_up`, 수집 권한은
`pg_scrape_collector_success`·`redis_exporter_last_scrape_error`로 따로 본다.
MNG·DEV 고유 경보는 각 DB runbook이 다룬다.

| 경보 | 먼저 볼 것 |
| --- | --- |
| `DatastoreScrapeTargetMissing` | 네 datastore job 중 대상이 사라짐. DEV 대상이면 `/etc/prometheus/targets/`가 렌더링됐는지, `PROMETHEUS_DEV_DATA_EXPECTED`가 `on`/`off`인지(그 밖의 값이면 Prometheus가 시작하지 않는다) |
| `DatastoreCollectorFailed` | PostgreSQL에는 접속했지만 collector 일부가 실패함. monitor role에서 `pg_read_all_stats`, `pg_read_all_settings`, `pg_ls_waldir()` 실행 권한이 빠졌으면 provision job을 다시 실행한다. Valkey exporter에는 collector별 신호가 없고 접속 실패는 `redis_up`이 알린다 |
| `DatastoreScrapeSlow` | 수집이 5초 넘게 걸림(기본 제한 10초). DB 부하와 monitor role의 `statement_timeout`(10초) 근접 여부 |

## Verification

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret values는 기록하지 않는다.
- Target 장애는 job name, endpoint, observed error, final `UP/DOWN` state를 기록한다.
- TSDB symptom은 로그 발췌, volume 경계, approval state를 기록한다.

### Verification Steps

- [ ] `docker exec prometheus wget -qO- http://localhost:9090/-/healthy`가 healthy response를 반환한다.
- [ ] Prometheus `Targets` page에서 affected critical target이 `UP`이다.
- [ ] `promtool check config` and `promtool check rules`가 성공한다.
- [ ] Grafana dashboard에서 새 metrics timestamp가 갱신된다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Evidence sources

- **Logs**: `docker logs --tail=200 prometheus`
- **Health**: `/-/healthy`, Prometheus UI `Targets`, Grafana dashboards
- **Validation**: `promtool check config`, `promtool check rules`
- **Metrics**: `prometheus_rule_evaluation_failures_total`, `prometheus_tsdb_compactions_failed_total`, target `up`
- **Evidence to Capture**: 실패한 job 이름과 target, 명령 출력 요약, reload·재시작 시각, 최종 복구 또는 보고 상태

## Rollback and Escalation

### Rollback or Recovery

이 런북에 명시된 validation, reload, restart, Git으로 관리하는 config rollback만 사용한다. 데이터 손실 가능성이 있는 TSDB/WAL 조치는 검증된 안전 복구 절차가 아니므로 Escalation으로 넘긴다.

#### Safe rollback

- Git-managed `prometheus.yml` or alert rule 변경이 원인이면 직전 Git diff 단위로 되돌리고 `promtool` 검증 후 lifecycle reload를 다시 수행한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- TSDB/WAL 삭제, volume file mutation, retention flag change는 이 런북의 안전 롤백 범위를 벗어난다. 별도 approval, backup evidence, incident/task 기록 없이 수행하지 않는다.

#### Planned isolated restore rehearsal

**project 이름만 바꾸어서는 실행할 수 없다.** rehearsal 전에 고정된 container-name,
host port, bind-path, external-network와 route의 충돌을 제거하고 운영 환경으로의
알림 전송과 workflow egress를 차단하는 별도 Compose 정의와 storage 구성을 승인받는다.
이 격리 구성과 해당 subject의 backup 계약을 검토하기 전까지 계획은 NOT_RUN으로
유지한다. 임시 project에 운영 volume을 연결하거나 credential을 복사하지 않는다.

상태: **계획됨, 미실행**. Prometheus TSDB 복구에 성공했다고 주장하지 않는다.

1. image/config/rule digest, TSDB 시간 범위, target/rule 기준값, retention flag와 backup checksum을 기록한다. Prometheus를 정지시키고, 승인된 방식으로 정지 상태의 일관된 `prometheus-data` 복사본 또는 storage snapshot을 생성한다. 현재 source에서는 admin snapshot API를 사용할 수 없다.
2. 알림 전송과 remote-write client를 비활성화하거나 test endpoint로 돌린 별도 project/network의 새 path에 복구한다.
3. Prometheus를 시작하고 WAL replay/readiness, 범위를 제한한 과거·현재 조회, target label, rule health, 통제된 Alertmanager 전송과, 사용 중인 경우 remote-write receiver 동작을 검증한다.
4. 불일치가 있으면 격리된 service를 중지하고 log/checksum을 보존한다. 수정하지 않은 backup으로 돌아간다. 운영 TSDB 교체는 별도로 승인받는다.

### Escalation

verification이 실패하거나, secret exposure risk가 보이거나, destructive data change가 필요하거나, TSDB/WAL 조치가 필요하거나, 관찰된 상태가 예상 절차와 다르면 repository owner @buenhyden에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0045-prometheus.md)
- [Operations policy](../policies/0045-prometheus.md)

### Traceability

- Declared parent: [Prometheus Usage Guide](../guides/0045-prometheus.md) (`GDE-0045`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0045-prometheus.md) (`GDE-0045`), [Policy](../policies/0045-prometheus.md) (`POL-0045`)
