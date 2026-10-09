---
title: "Gatus Guide"
version: "0.2.2"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0087"
parent_ids:
- "POL-0087"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - gatus
created: "2026-09-19"
---

# Gatus Guide

## Overview

Gatus는 `obs`, `availability`, `dev`가 선택하는 상시 실행 HOME availability monitor이다. native Keycloak OIDC로 보호되는 status UI와 SQLite probe history를 제공한다.

## Audience and Goal

대상은 observability와 availability probe를 운영하는 @buenhyden과 기여자다. Gatus의 구성, 인증 경계, 상태 저장 방식을 이해하고, 승인이 필요한 진단·재시작·복구는 Runbook으로 넘기는 것이 목표다.

## Usage

Gatus는 `obs`, `availability`, `dev`가 선택하는 상시 실행 HOME availability
monitor이다. root Compose가 포함 여부를 관장하며,
[observability Compose source](../../../infra/06-observability/docker-compose.yml)가
local build, UID/GID, `GATUS_PORT`, read-only 설정, healthcheck, network,
`gatus-data` mount, Traefik label을 관장한다.

활성 mount는 `config.oidc.yaml`이다. Gatus는 confidential한 `home-gatus`
Keycloak authorization-code client로 인증하며 구성된 subject만 허용한다. UI
route는 TLS와 `gateway-standard-chain@file`을 사용하며 `sso-auth@file`은
사용하지 않는다. router는 `/metrics`를 제외하므로 metrics는 인증된 브라우저
UI가 아니라 내부 monitoring 경계이다. Gatus session은 local에서 1시간으로
설정되어 있다. Keycloak logout이 Gatus session revocation으로 즉시
이어지는지는 관찰한 테스트가 없어 확인되지 않았다.

SQLite history는 `gatus-data`를 통해 `/data/gatus.db`에 저장된다. probe
결과는 운영 data이다. 설정과 database는 probe 대상 application이 완전히
수용되었음을 증명하지 않으며, 선언된 endpoint check만 기록한다.

### Selected source and readiness

Linked Dockerfile은 고정 upstream commit archive와 checksum을 확인하고 로컬 OIDC patch를 zero-fuzz로 적용한 뒤 module 일치·API/security test와 binary build를 수행하도록 선언한다. 최종 Alpine stage는 binary와 secret/CA entrypoint를 COPY한다. Compose는 Gatus directory context를 쓰고 args/target은 없으며 config는 runtime bind다. Local tag는 checksum/test나 배포 bytes를 증명하지 않는다. 이 문서 감사에서는 build·runtime 검사를 실행하지 않았다.

Health·bootstrap/auth는 의도적으로 공개되고 status/history API는 native OIDC로 보호한다. Metrics는 내부에 열려 있지만 public router에서 제외된다. Wrapper는 비어 있지 않은 정확한 subject와 읽을 수 있는 secret/CA를 요구하고 CA bundle을 만든 뒤 Gatus를 실행한다. 선택 non-root UID/GID가 secret/data 소유권과 맞아야 한다. Health로 OIDC·probe 전달을 증명하지 않는다. Keycloak·gateway·CA/state·probe 대상마다 readiness를 확인하며 설정 한도는 실측 여유가 아니다.

### Normal operation and lifecycle

승인된 UI session에서 probe 이름과 상태 결과를 검토한다. 응답 본문,
credential, token은 evidence에 넣지 않는다. local image를 upgrade하려면
먼저 Dockerfile의 upstream source와 patch를 검토하고, 이전 image와 설정을
보존한 뒤, runtime 승인 후 [runbook](../runbooks/0087-gatus.md)을 사용한다.
[repository](https://github.com/TwiN/gatus)에 따르면 Gatus는 Apache-2.0
upstream license를 사용한다. local image 이름에서 기능을 추론하기보다 새
source release와 patch 호환성을 검증한다.

SQLite backup에는 조율된 quiescence나 engine이 지원하는 consistent snapshot이
필요하다. live database 파일만 복사하면 WAL 상태가 누락될 수 있다. 먼저
격리된 storage로 restore하고 예상 history와 새 probe를 검증한 뒤 교체 전에
승인을 받는다. 중앙 [backup policy](../policies/0021-backup-and-restore.md)가
공유 retention과 custody control을 관장한다.

### Source-backed operating contract

- **Purpose/classification/source**: `gatus`는 `obs`/`availability`/`dev`가
  선택하는 `HOME` availability dashboard이다.
  [Compose](../../../infra/06-observability/docker-compose.yml),
  [local Dockerfile](../../../infra/06-observability/gatus/Dockerfile), entrypoint,
  OIDC 설정이 authoritative하다.
- **Flow/dependencies/security**: Gatus는 선언된 endpoint check를 실행하고
  UI/metrics를 공개한다. native Keycloak OIDC가 `gatus_oidc_client_secret`과
  마운트된 root CA를 사용해 UI를 보호한다. session TTL은 1시간이다. metrics
  endpoint는 현재 source에서 독립적으로 gateway-routed되어 있지 않다.
- **State/resources**: `gatus-data:/data`에는 SQLite `gatus.db`와 application
  상태가 들어 있다. source limit은 여유 공간이 아니다. endpoint 설정에는
  민감한 topology가 포함될 수 있으므로 token이나 private 응답 본문을 log에
  남기지 않는다.
- **Normal use/lifecycle**: root에서 render하고 설정을 validate한 뒤 health,
  OIDC login, 예상 endpoint 결과, Prometheus scrape path를 확인한다. backup
  전에 Gatus를 멈추거나 SQLite-native consistency를 사용한다. 설정, database,
  OIDC secret reference, root CA를 보존한다.
- **Upgrade**: pinned local image/patch를 의도적으로 재빌드하고, schema/OIDC
  호환성을 검토하며, 격리된 상태에서 restore/test한 뒤 history, endpoint
  check, login, session, metrics를 검증한다.
- **Upstream/license**: 공식
  [Gatus repository/release](https://github.com/TwiN/gatus)를 따른다. Gatus는
  Apache-2.0 license이며 patch provenance를 보존한다.

### Common Checks

- [Observability Compose](../../../infra/06-observability/docker-compose.yml)에서
  native OIDC, `/metrics` router 제외, healthcheck를 점검한다.
- 승인된 upgrade 전에 source와 SQLite custody를 검토한다. health는 login이나
  probe coverage를 증명하지 않는다.

### Runbook Handoff

승인 게이트가 걸린 진단, 재시작, recovery에는
[Gatus Runbook](../runbooks/0087-gatus.md)을 사용한다.

### Traceability

- [Policy](../policies/0087-gatus.md), [Runbook](../runbooks/0087-gatus.md)
- [Gatus configuration reference](https://github.com/TwiN/gatus#configuration)

## Related Documents

- [Observability Compose](../../../infra/06-observability/docker-compose.yml)
