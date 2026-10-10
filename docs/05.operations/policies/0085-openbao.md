---
title: "OpenBao Policy"
version: "0.5.3"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0085"
parent_ids:
- "AD-0003"
created: "2026-09-19"
---

# OpenBao Policy

## Overview

HOME secret control plane이다. 레거시 Vault는 2026-09-25 폐기되었으므로 현재 마이그레이션·복구 소스로 취급하지 않는다.

## Scope

`infra/03-security/openbao`와 `core / dev / local / security / secrets` 프로필 아래의 서비스
`openbao openbao-agent`.

## Rules

unseal/recovery 자료는 오프라인으로 유지한다. token, role_id, secret_id 또는 렌더링된
파일을 절대 로깅하지 않는다. 현재 서버 health는 unsealed 상태만 허용한다. Agent
health만으로는 새 인증·출력 갱신과 secret 전달을 증명할 수 없다. 기존 애플리케이션 Docker Secret은 Agent
출력으로 자동 대체되지 않는다.

사람이 하는 일반 관리 작업은 Keycloak을 backend로 하는 OpenBao native OIDC를 통해
발급된 non-root OpenBao 토큰을 사용해야 한다. 승인된 HOME 바인딩은 Keycloak 그룹
`/openbao-admins`, role `home-admin`, OpenBao OIDC client `home-openbao`, OpenBao
operator policy `hy-home-operator`다. 사람 토큰의 policy TTL은 유한해야 한다. OpenBao
UI 앞의 Gateway SSO는 HTTP 접근 제어일 뿐이며 OpenBao native OIDC 인가를 대체하지
않는다.

### Prometheus Metrics Credential

Prometheus는 전용 service token으로 `sys/metrics`에 인증해야 하며, 그 유일한 service
policy는 추적되는 `infra/03-security/openbao/config/policies/prometheus.hcl`이다. 이
policy는 `sys/metrics`에 대한 `read`만 부여한다. 토큰은 수동으로 발급해
`secrets/security/openbao/openbao_token.txt`에 저장하고 Prometheus만 마운트하며 유한한 만료
전에 회전한다. 인증 없는 metrics를 활성화하거나 root, human operator, renderer AppRole,
renderer sink 토큰을 재사용하지 않는다.

policy 적용, 토큰 발급/폐기, 파일 작성, Prometheus 재생성은 별도로 승인된 유지보수
기록이 필요한 실제 credential/runtime 변경이다. 추적되는 policy, Compose, scrape 설정은
소스 계약만 증명한다.

### hy-home.k8s Kubernetes Auth

hy-home.k8s 클러스터는 `kubernetes` auth method로 인증한다. External Secrets service
account (`external-secrets`, namespace `external-secrets`, audience `vault`)만 role
`eso-read-platform`을 통해 로그인할 수 있으며, 그 policy는 `secret/platform/{argocd,postgres-app,notifications,prometheus-api,grafana-api}`의
정확한 KV v2 data/metadata 경로만 읽는다. wildcard, list, create/update/delete/sudo를
부여하지 않는다. 클러스터 부트스트랩 토큰은 오직
`k8s-bootstrap` 토큰 role에서 나온다: orphan, 2시간 TTL, policy `k8s-bootstrap`
(`platform/argocd` 읽기). OIDC operator는 클러스터 재구축마다 `auth/kubernetes/config`를
갱신하고 이 토큰을 발급할 수 있다. method 활성화, policy/role 작성, KV 항목 작성에는
승인된 root 세션이 필요하다. 클러스터가 도달할 수 있도록 OpenBao Traefik route는 SSO나
IP allowlist 없이 유지한다.

이 다섯 경로는 [추적 ACL](../../../infra/03-security/openbao/config/policies/eso-read-platform.hcl)의
범위이며 사람이 쓰는 operator의 create/update 권한과 구분한다. 기존 세 경로 설명
이후 owner-authored 변경 `e3d811870`과 `5fb725b2a`(2026-09-23)가 Prometheus와
Kiali Grafana 읽기를 추가했고, [완료된 Task 0008](../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0008-storage-security-lakehouse-convergence.md)의
해당 경로·통합/merge 기록과 [2026-09-24 owner 완료 결정](../../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md#completion-basis-owner-decision-2026-09-24)이
그 제한된 추가의 역사적 근거다. 이 교정은 임의 권한 확대를 허용하지 않는다.
ESO 주체가 침해되면 이 다섯 항목에 대한 읽기가 함께 영향을 받으므로 exact
service-account/namespace/audience 바인딩을 유지한다. 실제 설치된 정책·role과
경로 밖 거부는 별도 검증하며 source나 문자열 하드닝 통과로 증명하지 않는다.

Root 토큰은 bootstrap과 break-glass 용도로만 사용한다. 다음 사항이 모두 동일한 유지보수
기록 안에서 검증되기 전에는 마지막으로 사용 가능한 root 토큰을 폐기하지 않는다: human
OIDC 로그인이 성공한다, 결과로 나온 OpenBao 토큰이 기대한 non-root policy를 가진다,
AppRole renderer 접근이 여전히 선언된 두 KV data와 해당 metadata 경로만 읽는다, 배포된 OpenBao 버전의 root
recovery 방법이 문서화되어 있다. 그 뒤 root를 폐기하고 거부 결과를 같은 기록에 남긴다.

Traceability에 문서화된 upstream OpenBao 릴리스 라인은 `operator generate-root`에
대해 인증된 `/sys/generate-root-token` 엔드포인트를 사용한다. 권한 있는 사람이나 root
토큰이 남아 있지 않을 때, Agent read-only 토큰을 root-generation 엔드포인트 호출로
승격해서는 안 된다. deprecated된 인증 없는 `/sys/generate-root/*` 엔드포인트는 2.5.3부터
기본적으로 비활성화되어 있으며 <!-- runtime-version-exception: history — unauthenticated root generation was disabled upstream to close a recovery-path security exposure --> 임시 loopback 전용
listener에서 명시적으로 승인된 break-glass 예외로만 다시 활성화할 수 있다. 이 예외는
동일한 데이터 볼륨과 seal 설정을 유지해야 하고 기본적으로 스냅샷을 restore해서는 안
되며 native OIDC 관리가 검증되면 즉시 제거해야 하고 복구된 root 토큰의 폐기로
끝나야 한다.

[Implementation](../../../infra/03-security/openbao/docker-compose.yml)과
[version projection](../../../infra/tech-stack.versions.json)이 런타임 고정값을 소유한다.

### Persistence, limits and removal

두 서비스의 공통 자원 상한·변경 적용은 [POL-0006](0006-infrastructure-optimization-governance.md),
버전 변경은 [POL-0086](0086-dependency-version-management.md)을 적용한다.
Raft 상태와 Agent bootstrap/output, offline custody는 서로 다른 보호 입력이며
[POL-0021](0021-backup-and-restore.md)의 OpenBao state-owner retention·암호화·복구
기준을 함께 적용한다. renderer는 선언된 두 KV data 경로만 read하며 unused template가
있다는 이유로 권한을 넓히지 않는다. Agent 재생성은 secret authority 복원이 아니다.

Raft upgrade 전 backup과 독립 stateful recovery 계약 검토가 필요하다. 승인된
격리 복원 없이 data rollback을 준비됐다고 표시하지 않는다. 마지막 관리 접근이나
unseal/custody 자료를 검증 전에 폐기하지 않는다. 서비스·Agent 제거는 소비자 이관,
credential 폐기와 보호 자료 보존을 각각 승인받아 수행하며 `down -v`로 대체하지 않는다.

## Exceptions

owner @buenhyden은 모든 편차 전에 범위, 위험, 만료, 종료 조건을 기록해야 한다. 정적
설정은 실제 backup이나 recovery의 증거가 아니다.

임시 인증 없는 generate-root recovery로 승인되는 유일한 형태는 대체 root 토큰을
생성하고 정상적인 OIDC administrator 경로를 확립하는 데 필요한 기간 동안
`disable_unauthed_generate_root_endpoints = false`로 설정된 loopback 전용 listener다.
이 설정은 public이나 gateway listener에서는 금지되며 steady-state 설정에 남아 있을 수
없다.

### Existing custody decision and missing closure

기존 owner 결정(2026-09-22)은 share3개를 `secrets/security/openbao/openbao_unseal_keys.txt`
한 파일에 함께 보관한다. 파일은0600, Git-ignored, 컨테이너에 mount하지 않으며
private registry는 SEC-003 placeholder만 보관하고 이 파일이 유일한 사본이다.
이는 분리 custody의 기존 명시적 예외다. 파일을 읽는 한 주체가 unseal threshold를
충족할 수 있고 파일 손실이 복구 자료 가용성을 잃게 할 수 있다. 이 문서는 기존
결정을 이동해 보존할 뿐 새 credential 처리나 예외 확대를 승인하지 않는다.
기존 기록에는 **만료와 종료 조건이 없다**. 위 Exceptions의 필수 항목을 충족했다고
표시하지 않으며 @buenhyden의 후속 결정이 필요하다. 파일을 읽거나 이동하거나
share를 재발급해 이 문서 불일치를 자동 해결하지 않는다.

### Verification

Compose/profile 검증과 [runbook](../runbooks/0085-openbao.md)이 별도의 정적/런타임 증거를
제공한다. 예상치 못한 서비스, 마운트, 인증, readiness 상태가 보이면 중단한다.

### P01 Native Trust and Audit Gate

정상 경로는 내부 native TLS와 검증된 CA/SAN이다. bootstrap key/CA trust는 해당
OpenBao에만 의존하지 않는다. wrapping SecretID의 creation path·짧은 TTL·1회 사용과
제한 role fetch/render version을 검증하며 sink 존재는 readiness가 아니다. Agent에
Docker socket을 주거나 무제한 restart로 인증 실패를 숨기지 않는다.

config-owned HMAC file audit를 유지하며 모든 필수 backend 실패 시 업무 요청의
실패/지연을 수용한다. health 응답은 audit 증거가 아니며 audit 비활성화로 성공시키지
않는다. 실제 filesystem 용량, rotation owner/schedule/보존, 실패 알림을 HOME에서
검증해야 한다. 기존 single-file custody 예외는 미해결 상태로 보존한다. P01 격리 시험은
그 예외를 종료하거나 HOME 복구 자료를 만들어내지 않는다. P06 확대는 실제 cold boot·
독립 unseal/offsite custody·선정 snapshot 복구 수용 이후만 허용한다.

### Review Cadence

매월, 그리고 이미지, persistence, 인증, 노출이 변경되기 전에 검토한다.

### Traceability

- Governing architecture: [AD-0003](../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](../guides/0085-openbao.md), [Policy](0085-openbao.md), [Runbook](../runbooks/0085-openbao.md)
- OpenBao 공식 TCP listener 파라미터: <https://openbao.org/docs/configuration/listener/tcp/>
- OpenBao 공식 authenticated root generation API: <https://openbao.org/docs/api/system/generate-root-token/>
- OpenBao 공식 deprecated legacy root generation API: <https://openbao.org/docs/api/system/generate-root/>
- unauthenticated generate-root를 다루는 OpenBao 공식 deprecation note: <https://openbao.org/community/deprecation/unauthed-generate-root/>
- authenticated root generation을 다루는 OpenBao 공식 release notes: <https://openbao.org/community/release-notes/2-6-0/>

## Related Documents

- [Operations index](../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
- [OpenBao unauthenticated generate-root deprecation](https://openbao.org/community/deprecation/unauthed-generate-root/)

고정 runtime의 미사용 SecretID 만료 결함(GHSA-7m59-mp95-w6ph)은 TTL·wrapping·1회 사용 선언으로
해결됐다고 간주하지 않는다. 수정 버전 검증과 HOME gate 전에는 배포·P06 확대를 보류하며,
미사용 발급의 명시적 폐기와 거부를 별도로 확인한다. 상세 근거는 RUN-0085의 Known Runtime Residual을 따른다.
