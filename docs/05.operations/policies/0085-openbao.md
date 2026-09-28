---
title: "OpenBao Policy"
version: "0.4.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0085"
parent_ids:
- "AD-0003"
created: "2026-09-19"
---

# OpenBao Policy

## Overview

HOME secret control plane이며, Vault는 별도의 마이그레이션 소스로 남는다.

## Policy Scope

`infra/03-security/openbao`와 `core / security / secrets` 프로필 아래의 서비스
`openbao openbao-agent`.

## Controls

unseal/recovery 자료는 오프라인으로 유지한다. token, role_id, secret_id 또는 렌더링된
파일을 절대 로깅하지 않는다. 현재 상태 health는 sealed 상태를 허용한다. 컨테이너
health만으로는 secret 전달을 증명하지 않는다. 기존 애플리케이션 Docker Secret은 Agent
출력으로 자동 대체되지 않는다.

일반적인 사람의 관리 작업은 Keycloak을 backend로 하는 OpenBao native OIDC를 통해
발급된 non-root OpenBao 토큰을 사용해야 한다. 승인된 HOME 바인딩은 Keycloak 그룹
`/openbao-admins`, role `home-admin`, OpenBao OIDC client `home-openbao`, OpenBao
operator policy `hy-home-operator`다. 사람 토큰의 policy TTL은 유한해야 한다. OpenBao
UI 앞의 Gateway SSO는 HTTP 접근 제어일 뿐이며 OpenBao native OIDC 인가를 대체하지
않는다.

### Prometheus Metrics Credential

Prometheus는 전용 service token으로 `sys/metrics`에 인증해야 하며, 그 유일한 service
policy는 추적되는 `infra/03-security/openbao/config/policies/prometheus.hcl`이다. 이
policy는 `sys/metrics`에 대한 `read`만 부여한다. 토큰은 수동으로 발급되어
`secrets/security/openbao_token.txt`에 저장되고, Prometheus만 마운트하며, 유한한 만료
전에 회전한다. 인증 없는 metrics를 활성화하거나 root, human operator, renderer AppRole,
renderer sink 토큰을 재사용하지 않는다.

policy 적용, 토큰 발급/폐기, 파일 작성, Prometheus 재생성은 별도로 승인된 유지보수
기록이 필요한 실제 credential/runtime 변경이다. 추적되는 policy, Compose, scrape 설정은
소스 계약만 증명한다.

### hy-home.k8s Kubernetes Auth

hy-home.k8s 클러스터는 `kubernetes` auth method로 인증한다. External Secrets service
account (`external-secrets`, namespace `external-secrets`, audience `vault`)만 role
`eso-read-platform`을 통해 로그인할 수 있으며, 그 policy는 `secret/platform/argocd`,
`postgres-app`, `notifications` 항목만 읽는다. 클러스터 부트스트랩 토큰은 오직
`k8s-bootstrap` 토큰 role에서 나온다: orphan, 2시간 TTL, policy `k8s-bootstrap`
(`platform/argocd` 읽기). OIDC operator는 클러스터 재구축마다 `auth/kubernetes/config`를
갱신하고 이 토큰을 발급할 수 있다. method 활성화, policy/role 작성, KV 항목 작성에는
승인된 root 세션이 필요하다. 클러스터가 도달할 수 있도록 OpenBao Traefik route는 SSO나
IP allowlist 없이 유지한다.

Root 토큰은 bootstrap과 break-glass 용도로만 사용한다. 다음 사항이 모두 동일한 유지보수
기록 안에서 검증되기 전에는 마지막으로 사용 가능한 root 토큰을 폐기하지 않는다: human
OIDC 로그인이 성공한다, 결과로 나온 OpenBao 토큰이 기대한 non-root policy를 가진다,
AppRole renderer 접근이 여전히 선언된 두 KV 경로만 읽는다, 배포된 OpenBao 버전의 root
recovery 방법이 문서화되어 있다, root 토큰 폐기가 관찰되었다.

Traceability에 문서화된 upstream OpenBao 릴리스 라인은 `operator generate-root`에
대해 인증된 `/sys/generate-root-token` 엔드포인트를 사용한다. 권한 있는 사람이나 root
토큰이 남아 있지 않을 때, Agent read-only 토큰을 root-generation 엔드포인트 호출로
승격시켜서는 안 된다. deprecated된 인증 없는 `/sys/generate-root/*` 엔드포인트는 2.5.3부터
기본적으로 비활성화되어 있으며 <!-- runtime-version-exception: history — unauthenticated root generation was disabled upstream to close a recovery-path security exposure --> 임시 loopback 전용
listener에서 명시적으로 승인된 break-glass 예외로만 다시 활성화될 수 있다. 이 예외는
동일한 데이터 볼륨과 seal 설정을 유지해야 하고, 기본적으로 스냅샷을 restore해서는 안
되며, native OIDC 관리가 검증된 직후 즉시 제거되어야 하고, 복구된 root 토큰의 폐기로
끝나야 한다.

[Implementation](../../../infra/03-security/openbao/docker-compose.yml)과
[version projection](../../../infra/tech-stack.versions.json)이 런타임 고정값을 소유한다.

## Exceptions

owner @buenhyden은 모든 편차 전에 범위, 위험, 만료, 종료 조건을 기록해야 한다. 정적
설정은 실제 backup이나 recovery의 증거가 아니다.

임시 인증 없는 generate-root recovery로 승인되는 유일한 형태는, 대체 root 토큰을
생성하고 정상적인 OIDC administrator 경로를 확립하는 데 필요한 기간 동안
`disable_unauthed_generate_root_endpoints = false`로 설정된 loopback 전용 listener다.
이 설정은 public이나 gateway listener에서는 금지되며 steady-state 설정에 남아 있을 수
없다.

## Verification

Compose/profile 검증과 [runbook](../runbooks/0085-openbao.md)이 별도의 정적/런타임 증거를
제공한다. 예상치 못한 서비스, 마운트, 인증, readiness 상태에서 중단한다.

## Review Cadence

매월, 그리고 이미지, persistence, 인증, 노출이 변경되기 전에 검토한다.

## Traceability

- Governing architecture: [AD-0003](../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](../guides/0085-openbao.md), [Policy](0085-openbao.md), [Runbook](../runbooks/0085-openbao.md)
- Official OpenBao TCP listener parameters: <https://openbao.org/docs/configuration/listener/tcp/>
- Official OpenBao authenticated root generation API: <https://openbao.org/docs/api/system/generate-root-token/>
- Official OpenBao deprecated legacy root generation API: <https://openbao.org/docs/api/system/generate-root/>
- Official OpenBao deprecation note for unauthenticated generate-root: <https://openbao.org/community/deprecation/unauthed-generate-root/>
- Official OpenBao release notes for authenticated root generation: <https://openbao.org/community/release-notes/2-6-0/>

## Related Documents

- [Operations index](../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
- [OpenBao unauthenticated generate-root deprecation](https://openbao.org/community/deprecation/unauthed-generate-root/)
</content>
