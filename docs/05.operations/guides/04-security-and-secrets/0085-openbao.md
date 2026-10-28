---
title: "OpenBao Guide"
version: "0.7.2"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-28"
layer: "operations"
artifact_id: "GDE-0085"
parent_ids:
- "POL-0085"
implementation_services:
  infra/03-security/openbao/docker-compose.yml:
  - openbao
  - openbao-agent
created: "2026-09-19"
---

# OpenBao Guide

## Overview

OpenBao는 HOME secret control plane이다. 레거시 Vault runtime/data는 2026-09-25 폐기된 역사적 대상이며 현재 migration/rollback 입력으로 사용할 수 없다.

## Scope

### Audience and Goal

대상은 OpenBao를 운영하거나 secret 소비 경로를 연결하는 보안·인프라 운영자다. 구성과 persistent input, 사람 관리자 접근(Keycloak native OIDC), credential 경계를 이해하고, 실행 절차가 필요하면 Runbook으로 넘어가는 것이 목표다.

## Concepts

구현 소스는 [infra/03-security/openbao/docker-compose.yml](../../../../infra/03-security/openbao/docker-compose.yml)이다.

Profile: `core / dev / local / security / secrets`. Service: `openbao openbao-agent`. root
Compose가 포함 여부를 관장한다.

Raft data, AppRole bootstrap material, 렌더링된 출력은 별도의 bind volume을
사용한다. agent config는 command path에 마운트되어야 하며, 렌더링된 파일은
/openbao/out 아래에 있어야 한다. VAULT_ADDR은 HCL server 주소를 override한다.

[Implementation](../../../../infra/03-security/openbao/docker-compose.yml)과
[version projection](../../../../infra/tech-stack.versions.json)이 runtime pin을
관장한다.

## Usage

### Service behavior and persistent inputs

`openbao`와 `openbao-agent`는 모두 HOME이며 `core`/`dev`/`local`/`security`/
`secrets`에서 선택된다. 두 서비스는 Compose image를 직접 사용하며 build는 없다.
server command는 `server`, Agent는 `agent -config=/openbao/config/agent.hcl`이다.
server의 `BAO_LOCAL_CONFIG`가 단일 노드 Raft와 내부 native TLS listener를 정의한다.
`OPENBAO_PORT`/`OPENBAO_CLUSTER_PORT`, `DEFAULT_SECURITY_DIR`, public route의
`DEFAULT_URL`이 입력이다. host port는 없으며 외부 TLS와 검증된 내부 TLS를 모두 사용한다.
서버는 `edge_net`/`secrets_net`/`obs_net`, Agent는 `secrets_net`과 `obs_net`을 사용한다.
Agent의 유일한 listener는 `metrics_only` 역할의 8100 HTTP이며(SPEC-0239)
`/agent/v1/metrics`만 응답하고 API proxy·cache·quit 경로는 없다. 인증이 없으므로
host port는 열지 않는다. Prometheus `openbao-agent` job이 `bao_agent_auth_failure`를
수집한다. template 렌더링은 metric이 없어 staleness는 Docker healthcheck로만 드러난다.

| 서비스 | mount·인증·정상 신호와 한계 |
| --- | --- |
| `openbao` | `openbao-data`는 host의 `${DEFAULT_SECURITY_DIR}/openbao/data`를 Raft 상태로 사용한다. OIDC·AppRole·Kubernetes auth/policy는 승인된 bootstrap으로 설치하며 Compose가 자동 생성하지 않는다. `/sys/metrics`는 전용 token을 요구한다. |
| `openbao-agent` | `agent.hcl`과 templates는 읽기 전용, `openbao-agent-data`와 `openbao-agent-out`은 각각 host의 agent/out 경로다. AppRole RoleID/SecretID로 로그인하고 token sink와 version 파일은 0600, 소비자가 읽는 `.txt` 출력은 0640(group 1000)으로 쓴다. secret rotation이나 소비자 mount 전환을 자동 수행하지 않는다. |

실제로 선택된 template은 `agent.hcl`의 19개다. Keycloak·Grafana 관리자 비밀번호와 8개 OIDC client
secret의 `.txt` 10개, KV 경로마다 하나인 `*_version.ctmpl` 9개(Grafana 두 값은 한 경로)이며 소비자마다
`out` 아래 디렉터리 하나를 쓴다. 같은 디렉터리의 나머지 template는
mount되어 있어도 `agent.hcl`에서 선택하지 않으며 renderer ACL을 확장하지 않는다.
서버 health는 `bao status`의 0(unsealed)만 허용한다. sealed(2) 상태에서는
새 Compose 기동에서 `openbao-agent`의 `service_healthy` 의존성이 대기한다. Docker daemon의 기존 컨테이너 자동 재시작은 이를 재평가하지 않는다. Agent는 새 프로세스에서 옛 sink를 제거하고 token validity·두 제한 fetch·정확한
render 일치를 요구한다. KV/render version과 실제 consumer 적용은 따로 검증한다. 근거는 [선언 릴리스 계열 status](https://openbao.org/docs/2.6.x/commands/status/)와
[Agent AppRole](https://openbao.org/docs/2.6.x/agent-and-proxy/autoauth/methods/approle/)이다.

두 서비스 모두 `template-stateful-med`의 CPU1/512 MiB를 상속한다. Raft 디스크
여유·sealed 지속·Agent 재인증 실패·OOM·전용 metrics 수집을 관찰하되 원문 로그나
렌더링 내용을 증거에 넣지 않는다. single-node Raft는 HA가 아니다. 공통 자원·선택·
기동 흐름은 [System Guide](../01-common/0099-system-operations.md)를 따른다. 버전 변경은
[공식 해당 계열 release notes](https://openbao.org/community/release-notes/2-6-0/#v262)와
[RUN-0086](../../runbooks/10-platform-and-backup/0086-dependency-version-management.md)를 대조한다.

**Administrator access.** 사람 관리자 접근은 UI 앞단의 gateway SSO session이
아니라 Keycloak 기반 OpenBao native OIDC이다. Keycloak이나 OAuth2 Proxy가
HTTP route를 보호할 수는 있지만 브라우저 사용자가 OpenBao policy가 적용된
OpenBao token을 받기 전에 OpenBao에는 여전히 자체 `jwt/oidc` auth method가
필요하다. OpenBao OIDC 문서에 따르면 OpenBao와 OIDC provider의 redirect URI가
일치해야 한다. UI callback 형태는
`/ui/vault/auth/{path}/oidc/callback`이다. 확인일: 2026-09-19. 출처:
<https://openbao.org/docs/auth/jwt/>.

구성된 HOME identity mapping은 다음과 같다.

| Field | Value | Purpose |
| --- | --- | --- |
| Realm | `hy-home.realm` | 사람 identity를 관장하는 Keycloak realm. |
| Client | `home-openbao` | OpenBao native OIDC용 Keycloak OIDC client. |
| Group | `/openbao-admins` | admin policy를 요청할 수 있는 사람 운영자 group. |
| OpenBao OIDC role | `home-admin` | 정확한 Keycloak group claim에 바인딩된 OpenBao role. |
| OpenBao policy | `hy-home-operator` | 최소 권한 non-root 운영자 policy. |
| Current user | `hyunyoun` | 전용 운영자 group에 배정된 기존 user. |

`https://openbao.hy.home.arpa/ui/`에서 OpenBao UI를 열고 **OIDC**를 선택한
후, 프롬프트가 뜨면 role `home-admin`을 입력하고 기존 Keycloak account로
로그인한다. 초기 root token과 임시 recovery root token은 모두 revoke되었으며
둘 다 login credential이 아니다. 사람의 password는 새 local OpenBao
account가 아니라 Keycloak에 속한다. 이 guide에는 password나 token을 전혀
기록하지 않는다. owner는 OIDC 로그인 성공을 확인했으며 server-side
metadata는 해당 session에 `default`와 `hy-home-operator` policy만 있음을
확인했다.

HOME host에는 `bao` CLI가 없다. 평소에는 OpenBao UI에서 OIDC로 로그인한다. HOME domain을
resolve하고 그 CA를 신뢰하는 다른 host에 CLI가 있으면 다음처럼 로그인할 수 있다:

```bash
export BAO_ADDR=https://openbao.hy.home.arpa
bao login -no-print -method=oidc -path=oidc role=home-admin
```

그 CLI는 token helper로 OpenBao token을 local 파일에 저장하므로 그 파일을 보호한다. 유지보수
window에서는 token helper를 쓰지 않는다. UI에서 받은 token을 숨김 입력으로 tmpfs의 0600 파일에
넣고 보호된 FD나 명령 하나에만 붙는 환경 변수로만 넘긴다([POL-0085](../../policies/04-security-and-secrets/0085-openbao.md#maintenance-window-credential-handling),
RUN-0085). gateway browser SSO는 public route에서 non-browser API access를
막을 수 있다. gateway 인증이나 TLS 검증을 우회하지 말고 승인된 API transport를
사용한다. 구성된 callback은 정확한 UI path인
`https://openbao.hy.home.arpa/ui/vault/auth/oidc/oidc/callback`와 CLI
callback인 `http://localhost:8250/oidc/callback`이다. client는 S256 PKCE를
요구한다.

[operator policy](../../../../infra/03-security/openbao/config/policies/operator.hcl)는
Keycloak과 Grafana KV 값만 읽기/갱신, renderer SecretID 발급, Raft snapshot
읽기, 인증된 quorum root recovery 시작/취소, 그리고
`auth/kubernetes/config` 갱신, `k8s-bootstrap` role을 통한 token 생성,
Prometheus API credential의 `secret/platform/prometheus-api`, Kiali Grafana token의
`secret/platform/grafana-api`, notification credential의 `secret/platform/notifications`에
대한 create/read/update와 해당 metadata read를 현재 source가 허용한다. ESO의
read-only 주체와 이 사람 운영자 권한은 별개다. source ACL은 배포된 권한의 증거가 아니다.
ESO는 이 사람 operator와 달리 `secret/platform/{argocd,postgres-app,notifications,prometheus-api,grafana-api}`의
정확한 data/metadata read만 받는다. 다섯 항목이 한 ESO 주체에 묶이므로 해당 주체
침해의 범위도 함께 검토한다. 승인 provenance와 Kubernetes 바인딩은
[Policy](../../policies/04-security-and-secrets/0085-openbao.md#hy-homek8s-kubernetes-auth)가 소유한다.
root 권한, secret 삭제, 임의 secret access, policy 변경, 그 밖의 auth 설정
변경은 부여하지 않는다. OIDC token TTL은 1시간이며 최대 lifetime은
4시간이다. 넓은 list 권한이 없으므로 모든 secret이 list에 나타날 것으로
기대하지 말고 알려진 secret path로 직접 이동한다.

root token, unseal key, OIDC client secret, AppRole `role_id`, AppRole
`secret_id`, wrapping token, 렌더링된 secret은 절대 command line, guide,
shell history에 두지 않는다.

**Credential boundaries.** unseal key, root token, OIDC 사람 user, AppRole
credential, OIDC client secret은 서로 다른 통제 수단이다.

| Material | Holder | Use | Normal lifetime |
| --- | --- | --- | --- |
| Unseal key share | Quorum holder | 재시작 후 OpenBao unseal 및 quorum 작업 승인. | 장기 custody 자료이며 UI login에는 사용하지 않는다. 현재 단일 파일 예외는 아래 Policy 참조. |
| Root token | Break-glass 운영자 | 초기 bootstrap 또는 비상 복구 전용. | 짧은 수명; 검증된 사람 admin과 recovery path 확보 후 revoke. |
| OIDC user session | 사람 운영자 | `hy-home-operator`를 통한 일반 OpenBao UI/CLI 관리. | OpenBao role이 정한 유한한 사람 TTL. |
| AppRole `role_id`와 `secret_id` | Renderer 또는 automation | 선언된 path에 대해서만 machine access. | 별도 TTL/사용 제한 policy; 사람 admin으로 절대 사용 안 함. |
| Keycloak client secret | OpenBao OIDC backend | OpenBao를 Keycloak OIDC client로 신뢰. | secret material로 저장; 노출 시 회전. |

server의 기존 bootstrap 기록은 threshold2, Shamir share3개다. 현재 custody의
2026-09-22 단일 host 파일 예외와 단일 confidentiality/availability 위험은
[Policy Exceptions](../../policies/04-security-and-secrets/0085-openbao.md#exceptions)가 소유한다. 분리 custody와
만료·종료 조건은 충족된 것으로 보지 않는다. 사람 OIDC 수용, renderer
확인, 수정된 recovery 절차는
[보존된 follow-up Task](../../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0002-openbao-access-and-env-convergence.md)에
기록되어 있다. snapshot 생성과 server 재시작/unseal은 검증되었으며, 격리된
restore와 share의 오프라인 전달은 별도의 운영자 책임으로 남아 있다.

### Maintenance window

server와 Agent 업그레이드는 120분 유지보수 window 하나에서 순서대로 진행한다(SPEC-0243).
W0 사전 점검 뒤 W1 임시 root, W1c renderer 정책, W2 snapshot token, W3 새 snapshot, W3b R2 보관,
W3a 격리 복원 시험(한 번만), W4 server 업그레이드와 수동 unseal(목표상 OpenBao가 약 10분 멈추며, window를 넘기면 다음 window까지 sealed로 남을 수 있다),
W5 Agent 업그레이드와 재발급, W6 audit 확인, W7 root 폐기 순서다. 정해진 시각까지 단계가 시작되지
않으면 멈추고, 어디서 멈추든 같은 정리를 한다. Keycloak과 Grafana는 이미 렌더된 값으로 계속
동작한다. 명령과 멈춤 기준은 [runbook](../../runbooks/04-security-and-secrets/0085-openbao.md)이,
credential 규칙과 받아들인 잔여 위험은 [policy](../../policies/04-security-and-secrets/0085-openbao.md)가
소유한다.

### Runbook Handoff

[Runbook](../../runbooks/04-security-and-secrets/0085-openbao.md)이 command, 예상 결과, recovery를
관장한다. [Policy](../../policies/04-security-and-secrets/0085-openbao.md)가 control을 관장한다.

### Traceability

- Governing architecture: [AD-0003](../../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](0085-openbao.md), [Policy](../../policies/04-security-and-secrets/0085-openbao.md), [Runbook](../../runbooks/04-security-and-secrets/0085-openbao.md)
- Official OpenBao OIDC auth method: <https://openbao.org/docs/auth/jwt/>
- Official OpenBao token model: <https://openbao.org/docs/concepts/tokens/>
- Official OpenBao seal/unseal model: <https://openbao.org/docs/concepts/seal/>
- Official OpenBao AppRole auth method: <https://openbao.org/docs/auth/approle/>
- Official Keycloak reverse proxy guidance: <https://www.keycloak.org/server/reverseproxy>

### P01 Trust and Bootstrap States

현재 source는 native HTTPS와 외부 CA 검증을 요구한다. Agent의 HCL address hardcoding은
없으며 `OPENBAO_PORT`의 Compose endpoint를 사용한다. source 등록은 HOME 적용 증거가
아니다. 새 프로세스는 이전 sink를 제거하고 60초 response-wrapped SecretID를 요구한다.
server unsealed, 제한 role fetch/KV version, rendered version, 실제 consumer 적용을
나누어 확인한다. 최초 TLS key/CA와 unseal/offsite 복구 자료는 그 OpenBao와 독립적으로
보관해야 한다. 기존 Keycloak/DB Docker Secret bootstrap은 P01에서 바꾸지 않아 OIDC와
render 사이의 순환을 피한다. 실제 consumer 전환은 P06 gate 이후의 별도 작업이다.

한 config-owned file audit의 용량/권한 장애는 audited 요청을 막을 수 있으며 system
health가 성공해도 audit 성공을 뜻하지 않는다. 값·raw audit/auth 로그 대신 status와
KV version/결과만 전달한다. 정확한 실행·복구는 [Runbook](../../runbooks/04-security-and-secrets/0085-openbao.md)의
Native TLS, Audit and Recovery Gate를 따른다. HOME custody·cold boot·실제 복구는
현재 미검증이며 격리 synthetic PASS를 복사하지 않는다.

### P01 versioned issuance journal

새 renderer 발급은 journal에 `schema_version: 2`와 `issuance_id`를 남긴다.
`issuance_id`는 기존 `nonce`의 동일한 호환 별칭이다. accessor metadata에는 문자열
`issuance_schema: "2"`, `issuance_id`, 기존 `sec01_nonce`가 함께 있으며 두 identity 값은
같아야 한다. 반면 과거 v1 journal과 anchor는 version 필드 없이 기존 정확한 문서 형태를
그대로 유지한다.

재실행은 journal과 활성 anchor의 version·identity, 그리고 실제 accessor metadata와 그
journal version에서 유도한 전체 metadata가 정확할 때만 이전 발급을 정합화한다. completion
witness는 중단된 정리 복구를 허용하는 별도 기록이다. v1/v2 혼합, 별칭 불일치, 중복 accessor는
폐기 전에 중단하며, 이전 발급을 정합화한 같은 실행은 새 SecretID를 발급하지 않는다. 이 계약은
source와 합성 검증의 범위이고, HOME 대상·custody·복원 입력이 미확정인 현재 상태를 실제 적용
증거로 바꾸지 않는다.

### P02 공개 catalog와 staging view

공개 분류의 단일 원천은 `infra/03-security/openbao/secret-catalog.json`과 같은 디렉터리의
`secret-catalog.schema.json`이다. 이 계약은 secret 값·값의 hash·token·실제 KV payload를
담지 않는다. 각 ID의 `owner`, `action`, `evidence_ref`, `source_recorded_at`을 유지한다.
마지막 날짜는 원 공개 기록의 날짜이며 검토·rotation·운영 관찰 날짜가 아니다.

분류는 `kv_static`, `stable_crypto`, `bootstrap_external`, `public_configuration`,
`derived_runtime`, `unused_delete`, `lab_excluded`이다. 현재 destination plan의
mount·field·UID/GID·mode는 null이고 ACL·delivery·reload·restart·rotation은
`BLOCKED_P01`이다. 실제 KV destination, 소비자 권한, 전달·reload와 RPO/RTO는 후속
담당자가 정확한 대상과 증거로 수용해야 한다. catalog 등록만으로 승인되지 않는다.

선언과 실제 관찰을 구분하기 위해 lifecycle은 declared, observed, imported, delivered,
consumed, rotated, recovered, retired의 여덟 lane을 둔다. declared 이외 일곱 lane에는
nullable runtime-evidence pointer가 있으며 `CONFIRMED`일 때 대응 pointer가 필요하다.
이 구조적 조건이나 pointer의 존재는 실제 소비·이관·복구 수용을 증명하지 않는다.
`UNKNOWN_BLOCKED`도 소비자가 없다는 판정이 아니다.

네 공개 입력은 catalog, schema, `secrets/SENSITIVE_ENV_VARS.md.example`,
`infra/secret-file-support.json`이다. CLI는 이 입력만 대조하고 승인된 ignored staging
경로 `.agent-work/p02-views`에 공개 예시, 값 없는 local view, JSON summary, README를 만든다.
local view는 기존 공개 표의 10-cell 형식을 유지한다. 상위 `.agent-work/README.md`와
경로의 소유권·regular/single-link·no-follow 조건을 먼저 확인해야 한다.
정확한 명령·출력·거절 조건은 [Runbook](../../runbooks/04-security-and-secrets/0106-openbao-consumer-catalog.md#p02-public-catalog-checks)을 따른다.

canonical SMTP 항목은 `COMM-002`이고 `COMM-003`은 그 항목을 가리키는 source-retired
alias이다. 별도 값·KV entry나 재발급 대상이 아니며, 이 표시가 실제 파일 삭제 완료를
뜻하지 않는다. 실제 COMM-003 폐기는 SMTP01이 소유한다. P06은 catalog API로 합성 binding을
검사할 수 있지만 실제 pilot은 발급된 대상 ID·KV path·ACL·delivery와 P01 인증·복구,
P03 소비자 신원, P04 실제 DEV/S3 수용을 기다린다. opsflow ID나 ACL을 임의로 만들지 않는다.

## Troubleshooting

### Common Checks

사용 전에 선택된 service, 선언된 mount, 공개된 interface, container 상태를
확인한다. readiness와 data recovery는 runbook evidence를 수집하기 전까지
검증되지 않은 상태다.

## Related Documents

- [Operations index](../../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
