---
title: "06-Observability Optimization Hardening Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0044"
parent_ids:
- "GDE-0044"
created: "2026-05-17"
---

# 06-Observability Optimization Hardening Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

> Scope: 관측 gateway·SSO middleware, Compose 상태 의존성, 커스텀 이미지 보안 강화, 검사, 재시작과 Git 기반 rollback 증거.

이 런북은 `06-observability` hardening regression을 복구하기 위한 실행 절차를 제공한다. Gateway/SSO middleware 누락, health dependency 회귀, custom image runtime hardening 누락, Pyroscope route availability 회귀, cAdvisor healthcheck 회귀, and CI hardening baseline failure를 중심으로 점검/복구한다.

### Purpose

운영자가 observability management route, compose dependency, healthcheck, custom image, and hardening validation boundary를 확인하고, runtime/security policy 변경이 필요한 경우 별도 승인으로 격리하도록 돕는다.

### When to Use

- `infrastructure-hardening` CI가 실패할 때.
- 관측성 UI/API가 Traefik 경유로 비정상 응답할 때.
- 스택 부팅 시 Alloy/Grafana dependency 또는 service health race가 반복될 때.
- Loki/Tempo custom image runtime hardening이 깨졌을 때.
- Pyroscope or cAdvisor route/healthcheck availability가 회귀했을 때.
- hardening script, Compose, Dockerfile, or operations docs 변경 후 rollback 가능성을 확인해야 할 때.

## Procedure

### Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Service lifecycle prerequisites

`cadvisor`는 host mount·device·privileged 접근의 승인을 먼저 확인한다. 기동 후 `/healthz`와 실제 container series를 별도로 확인한다. 중지·image 교체는 관측 공백을 만들지만 자체 애플리케이션 데이터 복원은 없다. node-exporter·DCGM 실행은 RUN-0045와 RUN-0055의 소유 경계를 따른다.

### Checklist

- [ ] 실패 항목을 middleware, depends_on, healthcheck, image, script, workflow, or docs 중 하나로 분류한다.
- [ ] 최근 변경 커밋과 영향 범위를 확인한다.
- [ ] telemetry collection, query, alerting, profiling, and UI route 영향도를 평가한다.
- [ ] Secret value, token, or credential payload는 기록하지 않는다.
- [ ] Route/middleware, resource cap, secret reference, workflow gate, or runtime hardening rule을 변경해야 해 보이면 중단하고 repository owner @buenhyden approval을 받는다.

### Steps

1. 정적 구성과 hardening baseline을 캡처한다.

   ```bash
   HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh
   bash scripts/hardening/check-all-hardening.sh 06-observability
   ```

2. Native and proxy gateway boundaries를 각각 확인한다.

   ```bash
   rg -n 'traefik.http.routers.(grafana|gatus).middlewares: gateway-standard-chain@file|GF_AUTH_GENERIC_OAUTH_ENABLED|GATUS_OIDC_CLIENT_ID' infra/06-observability/docker-compose.yml
   rg -n 'traefik.http.routers.(prometheus|alloy|alertmanager|pushgateway|loki|tempo|pyroscope|cadvisor).middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

3. Health dependency and healthcheck boundary를 확인한다.

   ```bash
   rg -n 'condition: service_healthy|/healthz|/api/health|/-/healthy|/ready|/-/ready' infra/06-observability/docker-compose.yml
   ```

4. Custom image hardening boundary를 확인한다.

   ```bash
   rg -n 'USER 10001:10001|S3_SECRET_KEY_FILE|S3_SECRET_KEY|exec /usr/bin/(loki|tempo)' infra/06-observability/loki/Dockerfile infra/06-observability/loki/docker-entrypoint.sh infra/06-observability/tempo/Dockerfile infra/06-observability/tempo/docker-entrypoint.sh
   ```

5. Pyroscope and cAdvisor route availability boundary를 확인한다.

   ```bash
   rg -n 'pyroscope:|cadvisor:|traefik.http.routers.pyroscope|traefik.http.services.pyroscope.loadbalancer.server.port|traefik.http.routers.cadvisor|traefik.http.services.cadvisor.loadbalancer.server.port|PYROSCOPE_PORT|CADVISOR_PORT' infra/06-observability/docker-compose.yml
   ```

6. 증상별 Git-managed rollback 후보를 확인한다.

   ```bash
   git diff -- infra/06-observability/docker-compose.yml infra/06-observability/loki/Dockerfile infra/06-observability/loki/docker-entrypoint.sh infra/06-observability/tempo/Dockerfile infra/06-observability/tempo/docker-entrypoint.sh scripts/hardening/check-all-hardening.sh .github/workflows/ci-quality.yml
   ```

7. Hardening script·workflow 파일 문제는 승인된 이전 revision의 해당 파일만 복원한 뒤 정적 검증한다. Compose·Dockerfile·내장 entrypoint 변경은 source 복원이나 restart만으로 기존 컨테이너에 반영되지 않는다. [RUN-0086](0086-dependency-version-management.md)에서 이전 image/build와 선언을 복원하는 승인된 recreate 계획으로 넘기고, 각 서비스 Runbook의 backup·marker·schema·secret 중단 조건을 먼저 충족한다. `git diff`는 후보 확인이며 복원 명령이 아니다.

   ```bash
   HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh
   bash scripts/hardening/check-all-hardening.sh 06-observability
   python3 scripts/validation/check-document-links.py --mode traceability
   ```

   이 런북은 route/middleware policy change, resource cap change, secret rotation, workflow gate redesign, or runtime security relaxation을 검증된 복구 절차로 제공하지 않는다. 해당 변경은 별도 approval과 rollback evidence가 필요하다.

### cAdvisor and static-check limits

cAdvisor는 읽기 전용 filesystem/device mount와 `/dev/kmsg`를 사용하는 privileged 관측기다. 공통 template이 capability를 제거한다고 격리를 보장하지 않는다. Disk metric 등 제외 collector, container label/cardinality와 보호 route를 유지한다. Health는 process 응답만 확인하므로 Prometheus target과 예상 container series를 따로 검증한다. 자체 애플리케이션 데이터나 Docker Secret은 없고 복구 대상은 승인된 image/config와 telemetry 기준이다.

관측 hardening 함수는 일부 문자열·파일만 검사하며 모든 Dockerfile, retention 시행, 인증 거부, 전달, host 호환성이나 용량을 증명하지 않는다. Loki/Tempo LAN 접근은 POL-0096의 기존 예외이고 retention 결함은 POL-0048에 남는다. Grafana/Gatus native 인증에 일괄 proxy SSO를 붙이지 않는다. 검사 통과만으로 통제를 완료하거나 privileged 권한 확대를 승인하지 않는다.

### Verification Steps

- [ ] `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh`가 통과한다.
- [ ] `bash scripts/hardening/check-all-hardening.sh 06-observability` 실패가 0건이다.
- [ ] `python3 scripts/validation/check-document-links.py --mode traceability`가 통과한다.
- [ ] Observability route middleware, health dependencies, custom image hardening, Pyroscope/cAdvisor availability checks가 현재 policy와 일치한다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Signals**: CI `infrastructure-hardening` 상태, Traefik router labels, container health, hardening script output
- **Evidence to Capture**: 보안 강화 검사 전후 출력, Compose 검증 결과, 영향받은 router·서비스, 관련 diff, 최종 복구 또는 보고 상태

### Safe Rollback or Recovery Procedure

- Git-managed Compose, Dockerfile, entrypoint, hardening script, workflow, or operations doc change가 원인이면 직전 Git diff 단위로 되돌린다.
- Runtime restart는 affected service의 documented runbook을 따른다.
- Route/middleware policy, resource cap, secret reference, workflow gate, or runtime security relaxation은 이 런북의 안전 롤백 범위를 벗어난다.

### Planned isolated recovery rehearsal

**Project 이름만 바꿔서는 실행할 수 없다.** Rehearsal 전에 고정 container name, host port, bind path, external network와 route 충돌을 제거하고 production 통지·workflow egress를 차단한 별도 Compose/storage 정의를 승인한다. 격리와 대상 backup 계약을 검토하기 전에는 NOT_RUN으로 유지한다. 임의 project에 production volume이나 credential을 연결하지 않는다.

상태: **계획됨·미실행**. 이 무상태 exporter들은 자체 데이터 복원 대상이 없다.

1. 고정한 이미지, 마운트·namespace 권한, 지표 endpoint 기준값, Prometheus target label, 의존하는 rule·dashboard 목록을 기록한다.
2. 동등한 읽기 전용 호스트 입력을 안전하게 제공할 수 있는 격리된 시험 호스트·프로젝트에서 추적되는 Compose로 exporter를 재생성한다. 호스트 파일을 서비스 백업으로 복사하지 않는다.
3. 상태, 예상 호스트·컨테이너 시계열, label 연속성, 수집 시간·cardinality, 보호된 cAdvisor 경로를 확인하고 예상하지 않은 쓰기 가능 마운트나 secret이 없는지 점검한다.
4. 불일치하면 격리 서비스를 중지하고 이미지·설정을 되돌린다. 운영 권한이나 마운트 변경은 별도 보안 승인이 필요하다.

## Verification

### Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret 값, token, credential payload 원문은 기록하지 않는다.
- Hardening 장애는 failed check name, affected service/router, before/after command output, relevant redacted diff, and recovery/escalation state를 함께 기록한다.
- Route/resource/secret/workflow/security policy 변경 필요성이 보이면 approval state를 기록한다.

## Rollback and Escalation

### Rollback or Recovery

이 런북에 명시된 validation, evidence capture, and Git-managed rollback만 사용한다. Route/middleware policy, resource cap, secret reference, workflow gate, runtime security relaxation, or external service 변경은 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

### Escalation

verification이 실패하거나, secret exposure risk가 보이거나, route/resource/secret/workflow/security 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 repository owner @buenhyden에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

### Traceability

- Declared parent: [06-Observability Optimization Hardening Usage Guide](../guides/0044-observability-optimization-hardening.md) (`GDE-0044`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0044-observability-optimization-hardening.md) (`GDE-0044`), [Policy](../policies/0044-observability-optimization-hardening.md) (`POL-0044`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0044-observability-optimization-hardening.md)
- [Operations policy](../policies/0044-observability-optimization-hardening.md)
