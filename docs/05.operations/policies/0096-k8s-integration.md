---
title: "hy-home.k8s Integration Operations Policy"
version: "1.3.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0096"
parent_ids:
- "AD-0026"
created: "2026-09-23"
---

# hy-home.k8s Integration Operations Policy

## Overview

### Overview

hy-home.k8s 클러스터는 host 주소상의 고정된 엔드포인트 집합과 두 개의
OpenBao 인증 경로를 사용한다. 이 정책은 그 집합과 인증 방식, 두 저장소 사이를
오가는 자격 증명의 처리 방식을 고정한다.

## Scope

### Policy Scope

클러스터가 호출할 수 있는 엔드포인트, OpenBao Kubernetes 인증과 bootstrap
토큰, Prometheus HTTP API 자격 증명, 저장소 경계를 넘는 값 전달.

### Traceability

- [가이드](../guides/0096-k8s-integration.md) (`GDE-0096`)
- [런북](../runbooks/0096-k8s-integration.md) (`RUN-0096`)
- [OpenBao policy](0085-openbao.md)

## Rules

### Controls

- 클러스터는 승인된 `HOST_LAN_BIND_IP`(기본값 `192.168.0.13`)를 통해 이 스택에 도달한다. 어떤 Compose
  서비스도 다시 k3d 네트워크에 참여하지 않으며, 클러스터를 위해 고정 주소를
  예약하지도 않는다.
- OpenBao는 SSO나 IP allowlist 없이 Traefik 라우트를 통해 도달한다(ESO는
  클러스터에서 로그인한다). OpenBao의 authorization이 통제 대상이다. ESO
  role은 audience `vault`로 `external-secrets/external-secrets`에만
  바인딩되며 HCL에 명시된 다섯 항목 `argocd`, `postgres-app`,
  `notifications`, `prometheus-api`, `grafana-api`의 data/metadata만 읽는다.
  `secret/platform/*` wildcard 권한을 부여하지 않는다.
- bootstrap 토큰은 `k8s-bootstrap` 토큰 role에서만 나온다. orphan이며,
  정책은 `k8s-bootstrap`, 수명은 최대 두 시간이고 발급마다 명시적으로
  요청한다. `secret/data/platform/argocd`만 읽으며 더 오래 사는 토큰은 발견 즉시 폐기한다. 폐기 확인 후 role 상한을 수정·검증하기 전에는 재발급하지 않는다.
- OIDC operator는 `auth/kubernetes/config`를 업데이트하고 bootstrap 토큰을
  발급할 수 있으며, 자격 증명 회전을 위해 `secret/platform/prometheus-api`를,
  토큰 재발급을 위해 `secret/platform/grafana-api`를, Slack 토큰 교체를
  위해 `secret/platform/notifications`를 업데이트할 수 있다. 인증 방식
  활성화, 정책과 role 작성, operator에 허용되지 않은 platform 초기 쓰기는
  폐기로 끝나는 승인된 임시 root 세션이 필요하다. operator의 허용된 세 KV 경로
  쓰기와 auth config 갱신을 root 전용으로 확대 해석하지 않는다.
- Prometheus는 클러스터에서 Basic Auth(`INFRA-007`)로 `/api/v1/`을 통해서만
  도달 가능하다. 클러스터는 자격 증명을 OpenBao `secret/platform/prometheus-api`
  로만 받으며 이 자격 증명은 `OBS-013`, `INFRA-007`과 같은 회전에서 함께 바뀐다.
  Prometheus host 포트는 게시하지 않으며 UI는 SSO를 유지한다. Grafana는
  host 포트도 익명 접근도 없다. Kiali는 `secret/platform/grafana-api`의
  Viewer 서비스 계정 `k8s-kiali`(90일) 토큰으로 읽는다.
- Loki `3100`, Tempo `3200`, `mng-valkey` `26379`, `alloy` `4317`/`4318`,
  `pg-router` `15432`/`15433`는 gateway 인증 없이 `HOST_LAN_BIND_IP`
  (기본값 `192.168.0.13`) 호스트 LAN 주소에만 게시된 상태를 유지한다
  (Valkey는 비밀번호를 유지한다). 클러스터를 위해 허용한 LAN 노출이며
  범위를 좁히려면 엔드포인트 추가와 같은 수준의 검토가 필요하다. 같은
  주소에 게시되는 gateway 80/443을 빼면, 나머지 host 포트는 `127.0.0.1`에만
  게시된다.
- 값은 저장소 경계를 파일이나 보호된 채널을 통해서만 넘긴다. chat, issue
  텍스트, 명령줄 인자, 로그로는 절대 넘기지 않는다. 증거는 이름, boolean,
  비밀이 아닌 필드만 기록한다.

이 정책은 현재 source의 회전 결함에 맞춰 통제를 낮추지 않는다. `OBS-013`,
`INFRA-007`, OpenBao 값의 일관성과 새 값 증명이 필요하며, 이를 만들지 못하는
절차는 `BLOCKED`로 중단한다. 명령 실패만으로 인증 거절·폐기 성공을 판정하지
않으며 transport/서버 상태/구문 오류는 `INDETERMINATE`로 처리한다.

### Verification

- Hardening이 Prometheus API 라우트, 그 middleware, `usersFile`을 고정하고
  두 k8s OpenBao 정책을 읽기 전용이며 wildcard 없는 상태로 유지한다.
- 런북의 확인 항목은 잘못된 Basic401, 유효한 Basic200, header 없는 API/UI의
  SSO302, role/config, bootstrap의 정확한 정책·orphan·TTL과 허용 읽기 전후의
  금지 읽기403이다. 서버 건강·unsealed와 동일 token으로 확인하며 다른 오류는
  거절 증거가 아니다. root/bootstrap의 로컬 파일 삭제는 서버 token 폐기가 아니다.
- 클러스터 재구축 뒤 CA 갱신 이후의 새 ESO 인증과 소비자별 기능 결과를 확인한다.
  Tempo3200 조회/API와 Alloy4317/4318 trace 수집을 구분한다.

### Review Cadence

책임 소유자는 @buenhyden이다. consumer를 추가하는 모든 hy-home.k8s 변경 시, OpenBao나 Traefik 업그레이드
시, 자격 증명이 회전할 때마다 검토한다.

## Exceptions

### Exceptions

없음. 새 엔드포인트, 다른 인증 방식, 더 긴 토큰 수명은 이 정책과 가이드의
contract 표에 대한 검토된 변경이 필요하다.

## Related Documents

- [OpenBao ESO read policy](../../../infra/03-security/openbao/config/policies/eso-read-platform.hcl)
- [OpenBao operator policy](../../../infra/03-security/openbao/config/policies/operator.hcl)
- [Prometheus policy](0045-prometheus.md)
