---
title: "OpenSearch"
version: "1.0.8"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2025-11-12"
---

# OpenSearch

## Overview

이 패키지는 정상 root Compose의 선택형 단일 OpenSearch와 해당
OpenSearch Dashboards를 소유합니다. 검색 API와 Dashboard는 기존 Traefik
라우트를 사용합니다. 소스 변경만으로 실행 중인 서비스가 바뀌지는 않습니다.

## Audience

검색 서비스의 developer, operator, 보안 검토자를 대상으로 합니다.

## Scope

`docker-compose.yml`의 `opensearch` profile은 `opensearch`와
`opensearch-dashboards`만 선택합니다. API는 HTTPS와 관리자 secret 기반
healthcheck를 사용하고 Dashboard는 `200` 또는 `401` 상태를 준비 신호로
받습니다. 두 서비스는 `edge_net`을 공유하고 OpenSearch는 관측 연결을
위해 `obs_net`도 사용합니다. 호스트 포트는 게시하지 않습니다.

관리자, Dashboard, exporter, cookie, OAuth client secret은 기존 root의
Docker secret 이름을 사용합니다. `${DEFAULT_CERT_DIR}`의 인증서와 보안
설정은 읽기 전용으로 mount합니다. 정상 영속 경로 `opensearch-data`와
`opensearch-dashboards-data`는 변경하지 않습니다. API와 Dashboard는
`opensearch.${DEFAULT_URL}` 및 `opensearch-dashboard.${DEFAULT_URL}`의
기존 gateway route를 유지합니다. 인증서와 실제 접근 권한은 소스 선언만으로
확인되지 않습니다.

Dockerfile은 OpenSearch를 기반으로 하지만 prometheus-exporter plugin의 선언 버전과
호환되는지 확인되지 않았습니다.
이미지 빌드, plugin 로드, 실제 readiness와 백업·복구는 확인 전이며 이
소스 변경으로 통과했다고 보지 않습니다.

## Structure

- `docker-compose.yml`: 정상 단일 엔진, Dashboard, 네트워크, 인증,
  영속 경로와 healthcheck.
- `Dockerfile`: 커스텀 엔진 이미지와 plugin 설치.
- `opensearch/`: 엔진 보안 설정, 사전, secret 기반 사용자 렌더러.
- `opensearch-dashboards/`: 정상 Dashboard의 HTTPS/OIDC 설정.

## Tech Stack

[Dockerfile](Dockerfile)과 [Compose](docker-compose.yml)가 단일 OpenSearch, Dashboards, exporter plugin을 선언합니다.

## Configuration

`opensearch` profile, `edge_net`·`obs_net`, 기존 영속 경로와 secret·인증서 bind를 사용합니다. 서비스별 실제 참조는 Compose가 소유합니다.

## Validation

아래 Compose 렌더를 정적으로 확인합니다. 이미지 빌드와 인증·readiness·복구는 별도 실행 결과가 필요합니다.

## How to Work in This Area

저장소 루트에서 정상 구성만 정적으로 확인합니다.

```bash
docker compose --profile opensearch config --quiet
docker compose --profile opensearch config --services
```

기동·재기동·인덱스 변경·백업·복구에는 별도의 구체적 승인이 필요합니다.
빌드 호환성, 비밀·인증서, 실제 consumer, host 용량, 복구 지점을 먼저
확인합니다. runtime 검사를 수행하지 않았다면 `NOT_RUN`으로 기록합니다.

## Related Documents

[문서 진입점](../../../docs/README.md)에서 OpenSearch 운영 정책·가이드·런북을
찾습니다. 공식 [Docker 설치](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/)와
[스냅샷 복구](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
문서를 참고합니다. 빌드 선언은 [Dockerfile](Dockerfile)이 소유하며 이미지
투영은 [tech-stack.versions.json](../../tech-stack.versions.json)에서 확인합니다.
