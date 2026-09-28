---
title: "hy-home.k8s Integration Operations Policy"
version: "1.2.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0096"
parent_ids:
- "AD-0026"
created: "2026-09-23"
---

# hy-home.k8s Integration Operations Policy

## Overview

hy-home.k8s 클러스터는 host 주소상의 고정된 엔드포인트 집합과 두 개의
OpenBao 인증 경로를 사용한다. 이 정책은 그 집합, 인증 방식, 두 저장소 사이에
오가는 자격 증명 처리 방식을 고정한다.

## Policy Scope

클러스터가 호출할 수 있는 엔드포인트, OpenBao Kubernetes 인증과 bootstrap
토큰, Prometheus HTTP API 자격 증명, 저장소 경계를 넘는 값 전달.

## Controls

- 클러스터는 `192.168.0.13`을 통해서만 이 스택에 도달한다. 어떤 Compose
  서비스도 다시 k3d 네트워크에 참여하지 않으며, 클러스터를 위해 고정 주소를
  예약하지도 않는다.
- OpenBao는 SSO나 IP allowlist 없이 Traefik 라우트를 통해 도달한다(ESO는
  클러스터에서 로그인한다). OpenBao의 authorization이 통제 대상이다. ESO
  role은 audience `vault`로 `external-secrets/external-secrets`에만
  바인딩되며 `secret/platform/*`만 읽는다.
- bootstrap 토큰은 `k8s-bootstrap` 토큰 role에서만 나온다. orphan이며,
  정책은 `k8s-bootstrap`, 수명은 최대 두 시간이고 발급마다 명시적으로
  요청한다. 더 오래 사는 토큰은 발견 즉시 폐기한다.
- OIDC operator는 `auth/kubernetes/config`를 업데이트하고 bootstrap 토큰을
  발급할 수 있으며, 자격 증명 회전을 위해 `secret/platform/prometheus-api`를,
  토큰 재발급을 위해 `secret/platform/grafana-api`를, Slack 토큰 교체를
  위해 `secret/platform/notifications`를 업데이트할 수 있다. 인증 방식
  활성화, 정책과 role 작성, `secret/platform/*` 쓰기는 폐기로 끝나는 승인된
  임시 root 세션이 필요하다.
- Prometheus는 클러스터에서 Basic Auth(`INFRA-007`)로 `/api/v1/`을 통해서만
  도달 가능하다. 클러스터는 자격 증명을 OpenBao `secret/platform/prometheus-api`
  로만 받으며, 이는 `OBS-013`, `INFRA-007`과 같은 회전에서 함께 바뀐다.
  Prometheus host 포트는 게시하지 않으며 UI는 SSO를 유지한다. Grafana는
  host 포트도 익명 접근도 없다. Kiali는 `secret/platform/grafana-api`의
  Viewer 서비스 계정 `k8s-kiali`(90일) 토큰으로 읽는다.
- Loki `3100`, Tempo `3200`, `mng-valkey` `26379`는 gateway 인증 없이 모든
  host interface에 게시된 상태를 유지한다(Valkey는 비밀번호를 유지한다).
  이는 클러스터에 대해 허용된 LAN 노출이며, 범위를 좁히려면 엔드포인트
  추가와 같은 수준의 검토가 필요하다.
- 값은 저장소 경계를 파일이나 보호된 채널을 통해서만 넘긴다. chat, issue
  텍스트, 명령줄 인자, 로그로는 절대 넘기지 않는다. 증거는 이름, boolean,
  비밀이 아닌 필드만 기록한다.

## Exceptions

없음. 새 엔드포인트, 다른 인증 방식, 더 긴 토큰 수명은 이 정책과 가이드의
contract 표에 대한 검토된 변경이 필요하다.

## Verification

- Hardening이 Prometheus API 라우트, 그 middleware, `usersFile`을 고정하고
  두 k8s OpenBao 정책을 읽기 전용이며 wildcard 없는 상태로 유지한다.
- 런북의 확인 항목은 Prometheus 자격 증명 없이 401, 있을 때 200, role과
  config 읽기, bootstrap 토큰의 정책, orphan 플래그와 TTL, allow/deny
  읽기이다.

## Review Cadence

consumer를 추가하는 모든 hy-home.k8s 변경 시, OpenBao나 Traefik 업그레이드
시, 자격 증명이 회전할 때마다 검토한다.

## Traceability

- [가이드](../guides/0096-k8s-integration.md) (`GDE-0096`)
- [런북](../runbooks/0096-k8s-integration.md) (`RUN-0096`)
- [OpenBao policy](0085-openbao.md)

## Related Documents

- [OpenBao ESO read policy](../../../infra/03-security/openbao/config/policies/eso-read-platform.hcl)
- [OpenBao operator policy](../../../infra/03-security/openbao/config/policies/operator.hcl)
- [Prometheus policy](0045-prometheus.md)
