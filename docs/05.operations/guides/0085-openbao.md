---
title: "OpenBao Guide"
version: "0.5.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
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

## Usage

### Implementation Sources

- [infra/03-security/openbao/docker-compose.yml](../../../infra/03-security/openbao/docker-compose.yml)

HOME secret control plane이다. 레거시 Vault runtime/data는 2026-09-25 폐기된 역사적 대상이며 현재 migration/rollback 입력으로 사용할 수 없다.

Profile: `core / dev / local / security / secrets`. Service: `openbao openbao-agent`. root
Compose가 포함 여부를 관장한다.

Raft data, AppRole bootstrap material, 렌더링된 출력은 별도의 bind volume을
사용한다. agent config는 command path에 마운트되어야 하며, 렌더링된 파일은
/openbao/out 아래에 있어야 한다. VAULT_ADDR은 HCL server 주소를 override한다.

[Implementation](../../../infra/03-security/openbao/docker-compose.yml)과
[version projection](../../../infra/tech-stack.versions.json)이 runtime pin을
관장한다.

### Service behavior and persistent inputs

`openbao`와 `openbao-agent`는 모두 HOME이며 `core`/`dev`/`local`/`security`/
`secrets`에서 선택된다. 두 서비스는 Compose image를 직접 사용하며 build는 없다.
server command는 `server`, Agent는 `agent -config=/openbao/config/agent.hcl`이다.
server의 `BAO_LOCAL_CONFIG`가 단일 노드 Raft와 내부 HTTP listener를 정의한다.
`OPENBAO_PORT`/`OPENBAO_CLUSTER_PORT`, `DEFAULT_SECURITY_DIR`, public route의
`DEFAULT_URL`이 입력이다. host port는 없고 TLS는 Traefik에서 종료한다.
서버는 `edge_net`/`secrets_net`/`obs_net`, Agent는 `secrets_net`만 사용한다.
Agent에는 HTTP listener나 자체 metrics endpoint가 선언되어 있지 않다.

| 서비스 | mount·인증·정상 신호와 한계 |
| --- | --- |
| `openbao` | `openbao-data`는 host의 `${DEFAULT_SECURITY_DIR}/openbao/data`를 Raft 상태로 사용한다. OIDC·AppRole·Kubernetes auth/policy는 승인된 bootstrap으로 설치하며 Compose가 자동 생성하지 않는다. `/sys/metrics`는 전용 token을 요구한다. |
| `openbao-agent` | `agent.hcl`과 templates는 읽기 전용, `openbao-agent-data`와 `openbao-agent-out`은 각각 host의 agent/out 경로다. AppRole RoleID/SecretID로 로그인하고 token sink와 두 출력 파일을0600으로 쓴다. secret rotation이나 소비자 mount 전환을 자동 수행하지 않는다. |

실제로 선택된 template은 `keycloak_admin_password.ctmpl`,
`grafana_admin_password.ctmpl` 두 개뿐이다. 같은 디렉터리의 나머지 template는
mount되어 있어도 `agent.hcl`에서 선택하지 않으며 renderer ACL을 확장하지 않는다.
서버 health는 `bao status`의0과2(sealed)를 모두 허용한다. Agent의
`service_healthy` dependency도 unseal을 기다리지 않으며 자체 health는 옛 token
파일이 남아 있어도 통과한다. 실제 unsealed·인증 성공·갱신·읽기/거부·출력 갱신을
따로 검증한다. 근거는 [선언 릴리스 계열 status](https://openbao.org/docs/2.6.x/commands/status/)와
[Agent AppRole](https://openbao.org/docs/2.6.x/agent-and-proxy/autoauth/methods/approle/)이다.

두 서비스 모두 `template-stateful-med`의 CPU1/512 MiB를 상속한다. Raft 디스크
여유·sealed 지속·Agent 재인증 실패·OOM·전용 metrics 수집을 관찰하되 원문 로그나
렌더링 내용을 증거에 넣지 않는다. single-node Raft는 HA가 아니다. 공통 자원·선택·
기동 흐름은 [System Guide](0099-system-operations.md)를 따른다. 버전 변경은
[공식 해당 계열 release notes](https://openbao.org/community/release-notes/2-6-0/#v262)와
[RUN-0086](../runbooks/0086-dependency-version-management.md)를 대조한다.

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

HOME domain을 resolve하고 그 CA를 신뢰하는 host에서 CLI access를 하려면:

```bash
export BAO_ADDR=https://openbao.hy.home.arpa
bao login -no-print -method=oidc -path=oidc role=home-admin
```

CLI는 token helper로 OpenBao token을 저장한다. 그 local 파일을
보호한다. gateway browser SSO는 public route에서 non-browser API access를
막을 수 있다. gateway 인증이나 TLS 검증을 우회하지 말고 승인된 API transport를
사용한다. 구성된 callback은 정확한 UI path인
`https://openbao.hy.home.arpa/ui/vault/auth/oidc/oidc/callback`와 CLI
callback인 `http://localhost:8250/oidc/callback`이다. client는 S256 PKCE를
요구한다.

[operator policy](../../../infra/03-security/openbao/config/policies/operator.hcl)는
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
[Policy](../policies/0085-openbao.md#hy-homek8s-kubernetes-auth)가 소유한다.
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
[Policy Exceptions](../policies/0085-openbao.md#exceptions)가 소유한다. 분리 custody와
만료·종료 조건은 충족된 것으로 보지 않는다. 사람 OIDC 수용, renderer
확인, 수정된 recovery 절차는
[보존된 follow-up Task](../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0002-openbao-access-and-env-convergence.md)에
기록되어 있다. snapshot 생성과 server 재시작/unseal은 검증되었으며, 격리된
restore와 share의 오프라인 전달은 별도의 운영자 책임으로 남아 있다.

## Common Checks

사용 전에 선택된 service, 선언된 mount, 공개된 interface, container 상태를
확인한다. readiness와 data recovery는 runbook evidence를 수집하기 전까지
검증되지 않은 상태다.

## Runbook Handoff

[Runbook](../runbooks/0085-openbao.md)이 command, 예상 결과, recovery를
관장한다. [Policy](../policies/0085-openbao.md)가 control을 관장한다.

## Traceability

- Governing architecture: [AD-0003](../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](0085-openbao.md), [Policy](../policies/0085-openbao.md), [Runbook](../runbooks/0085-openbao.md)
- Official OpenBao OIDC auth method: <https://openbao.org/docs/auth/jwt/>
- Official OpenBao token model: <https://openbao.org/docs/concepts/tokens/>
- Official OpenBao seal/unseal model: <https://openbao.org/docs/concepts/seal/>
- Official OpenBao AppRole auth method: <https://openbao.org/docs/auth/approle/>
- Official Keycloak reverse proxy guidance: <https://www.keycloak.org/server/reverseproxy>

## Related Documents

- [Operations index](../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
