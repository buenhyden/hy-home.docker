---
title: "hy-home.k8s Integration Usage Guide"
version: "1.3.1"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0096"
parent_ids:
- "POL-0096"
created: "2026-09-23"
---

# hy-home.k8s Integration Usage Guide

## Usage

### Purpose

hy-home.k8s 저장소는 같은 호스트에서 k3d 클러스터(`hyhome`)를 실행한다.
k3d 제거 이후로는 어떤 Compose 서비스도 이와 Docker 네트워크를 공유하지
않는다. 클러스터는 호스트 주소 `192.168.0.13`을 통해서만 이 스택에
도달하며, OpenBao도 같은 방식으로 클러스터 API에 도달한다. 이 가이드는
그 계약을 설명하고 [runbook](../runbooks/0096-k8s-integration.md)은 계약을 설정하고 클러스터를
재구축할 때마다 반복하는 전체 절차다.

### Contract

| Consumer in the cluster | Endpoint | Authentication | Owner here |
| --- | --- | --- | --- |
| External Secrets Operator | `https://openbao.hy.home.arpa` (Traefik `192.168.0.13:443`) | OpenBao Kubernetes 인증, 역할 `eso-read-platform` | [OpenBao](0085-openbao.md) |
| 클러스터 부트스트랩(ESO 이전) | 동일 | `k8s-bootstrap` 토큰, 2시간 | OpenBao |
| Alloy 메트릭(remote write), Argo Rollouts 분석 | `https://prometheus.hy.home.arpa/api/v1/write`, `/api/v1/query*` | OpenBao `secret/platform/prometheus-api`의 Basic Auth (출처 `PROMETHEUS_API_USERNAME`, `OBS-013`) | [Prometheus](0045-prometheus.md) |
| Kiali 쿼리 | `https://prometheus.hy.home.arpa` (`/api/v1/`만 통과) | 동일 | Prometheus |
| Kiali Grafana 링크 | `https://grafana.hy.home.arpa` | Viewer 서비스 계정 `k8s-kiali`의 bearer 토큰, OpenBao `secret/platform/grafana-api`에서 발급 | [Grafana](0041-grafana.md) |
| Alloy 로그 | `http://192.168.0.13:3100` (Loki push) | 없음 | Loki |
| 트레이스 | `http://192.168.0.13:3200` (Tempo) | 없음 | Tempo |
| Argo CD 캐시 | `192.168.0.13:26379` (`mng-valkey`) | Valkey 비밀번호(`CACHE-007`, OpenBao `platform/argocd`를 통해 전달) | [Management database](0028-management-database.md) |
| PostgreSQL이 필요한 앱(옵션) | `192.168.0.13:15432` 쓰기, `15433` 읽기 | OpenBao `platform/postgres-app`을 통한 데이터베이스 자격 증명 | `postgres-ha` 프로파일 |
| OpenBao에서 클러스터로 | `https://192.168.0.13:6550` (k3d API) | `auth/kubernetes/config`의 클러스터 CA | OpenBao |

제공하지 않는 것: 호스트 포트나 익명 접근을 통한 Grafana(오너 결정;
Kiali는 대신 Viewer 토큰을 사용), `4317/4318`의 Alloy OTLP(HOME Alloy
설정에는 OTLP 수신자가 없음). Traefik에는 `*.k8s.hy.home.arpa` 라우트가
없다. 네이티브 k3s NodePort로 가는 인증 없는 catch-all은 지난 7일간
요청이 없어 2026-09-24에 제거했다.

### What hy-home.k8s needs from this side

| Item | Where it lives | How it is handed over |
| --- | --- | --- |
| Gateway CA | `secrets/certs/rootCA.pem` (mkcert root, public) | 복사 |
| Prometheus API 자격 증명 | OpenBao `secret/platform/prometheus-api` (`username`, `password`), `.env`의 `PROMETHEUS_API_USERNAME`과 `secrets/observability/prometheus_api_password.txt`에서 | ESO 동기화; 수동 복사 없음 |
| Kiali Grafana 토큰 | OpenBao `secret/platform/grafana-api` (`token`), runbook이 90일로 발급 | ESO 동기화; 수동 복사 없음 |
| 부트스트랩 토큰 | `/tmp/bao-k8s/k8s-bootstrap.token` (runbook이 생성) | 보호된 채널, 2시간 이내 사용 |
| 이름 해석 | `openbao.hy.home.arpa`, `prometheus.hy.home.arpa`, `grafana.hy.home.arpa` → `192.168.0.13` | 클러스터 DNS 항목 |

클러스터 쪽은 이 밖에도 ESO 서비스 계정을 위한 `system:auth-delegator`
ClusterRoleBinding, `192.168.0.13`의 443, 3100, 3200, 26379 포트로의
egress, remote write된 시리즈의 `cluster` 외부 레이블을 보유한다.

### Common Pitfalls

- 단일 파일 Docker secret은 컨테이너가 생성될 때의 inode를 유지한다.
  시크릿 파일을 재생성했다면 그 소비자도 재생성해야 한다
  (`INFRA-007`의 경우 Traefik).
- 이름이 해석되지 않으면 호스트에서 실행한 `curl`은 `000`을 반환한다. 호스트
  `/etc/hosts`에는 `hy.home.arpa` 이름이 몇 개뿐이므로 `--resolve`를
  사용한다.
- zsh에서는 여러 `curl` 옵션을 담은 변수가 분할되지 않으므로 옵션을
  풀어서 쓴다.
- 새 Prometheus API 비밀번호는 OpenBao
  `secret/platform/prometheus-api`에도 반영해야 한다. 반영하지 않으면
  클러스터의 remote write가 `401`을 받는다. runbook의 교체 섹션이 세
  곳을 모두 함께 처리한다.

## Common Checks

- `bash scripts/operations/gen-secrets.sh --sync-metadata-check` (종료 코드 0)
- `bash scripts/hardening/check-all-hardening.sh` (라우트, 정책, 미들웨어 고정)
- `docker network inspect k3d-hyhome --format '{{range .Containers}}{{.Name}} {{end}}'`는 `k3d-hyhome-*` 컨테이너만 나열

## Runbook Handoff

최초 설정, 클러스터 재구축, 자격 증명 교체는
[runbook](../runbooks/0096-k8s-integration.md)을 따른다.

## Traceability

- [Policy](../policies/0096-k8s-integration.md) (`POL-0096`)
- [Runbook](../runbooks/0096-k8s-integration.md) (`RUN-0096`)
- [Compose network segmentation architecture](../../02.architecture/descriptions/0026-standardize-infra-net.md)

## Related Documents

- [OpenBao runbook](../runbooks/0085-openbao.md)
- [Prometheus policy](../policies/0045-prometheus.md)
- [Traefik guide](0013-traefik.md)
