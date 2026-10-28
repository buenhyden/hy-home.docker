---
title: "OpenBao Runbook"
version: "0.13.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-28"
layer: "operations"
artifact_id: "RUN-0085"
parent_ids:
- "POL-0085"
created: "2026-09-19"
---

# OpenBao Runbook

## Overview

이 런북은 OpenBao(`openbao`, `openbao-agent`)의 상태 점검, 승인된 대상 기동·중지, initial bootstrap, 사람 로그인과 root 복구, break-glass, 복구를 다룬다. Renderer SecretID 전달은 [RUN-0103](0103-openbao-renderer-delivery.md), metrics credential은 [RUN-0104](0104-openbao-metrics-credential.md), 유지보수 window는 [RUN-0105](0105-openbao-maintenance-window.md), 소비자 이관과 secret catalog는 [RUN-0106](0106-openbao-consumer-catalog.md)이 소유한다. OpenBao는 재시작 뒤 owner가 직접 하는 수동 Shamir unseal이 필요하다. 이 문서의 어떤 단계도 unseal share를 대신 입력하거나 자동화하지 않는다.

## Trigger

`openbao openbao-agent` readiness 점검과 승인된 대상 지정 배포 또는 복구에 사용한다.

## Prerequisites

### Trigger and Preconditions

저장소
루트에서 작업한다. 런타임 변경 전에 configuration commit, 이미지 source, 기존 데이터 위치,
보호된 backup을 확인한다.

## Procedure

1. 기존 Compose validator로 선택한 profile을 검증한다. 비공개 렌더링 모델은 절대 출력하지
   않는다.
2. 다음의 한정된 read-only 점검을 실행한다.

   ```bash
   docker compose exec -T openbao bao status
   ```

3. initialized/unsealed 상태를 별도로 확인한 뒤, 내용을 읽지 않고 destination 존재 여부와
   권한을 검증한다. AppRole provisioning과 unseal은 owner-controlled credential 절차가
   필요하다.
4. 배포가 승인되면 이 서비스들만 명시하고 수동 initialization/unseal과 daemon readiness를 별도로
   검증한다. 예상치 못한 mount나 실패한 점검이 있으면 중단하고, 전체 stack으로 범위를
   넓히지 않는다.

[Implementation](../../../../infra/03-security/openbao/docker-compose.yml)과 [version projection](../../../../infra/tech-stack.versions.json)이 런타임 고정 버전을 소유한다.

### Lifecycle and maintenance boundary

`openbao`와 `openbao-agent`만 대상으로 하며 기본 `security` 선택을 사용한다.
기존 local image와 root network, bind 경로의 소유권·용량, 보존된 Raft identity,
승인된 unseal 관리자가 준비되지 않았다면 시작/중지를 진행하지 않는다.

```bash
HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh
# 이후 명령은 대상 runtime 변경이 승인된 경우에만 실행한다.
docker compose --profile security up -d --no-deps --no-build --pull never openbao
```

`bao status`의 exit0은 unsealed, exit2는 sealed, 그 밖은 오류다. 현재 Compose
health는 0만 허용하며 sealed(2)는 `unhealthy`다. 새 Compose 기동의 Agent health 의존성은
unseal 이후에 통과한다. Docker daemon의 기존 Agent 자동 재시작에는 이 의존성이 적용되지 않는다. 이미 initialize된 저장소를 다시 initialize하지 않는다.
위 initial/bootstrap 또는 승인된 unseal 뒤 실제 `Sealed false`를 확인하고, 새로
필요한 SecretID를 아래 절차로 전달한 후 Agent만 시작한다.

```bash
docker compose --profile security up -d --no-deps --no-build --pull never openbao-agent
# 승인된 중지는 Agent부터 수행하며 secret 출력 갱신이 멈춘다.
docker compose stop openbao-agent
docker compose stop openbao
```

stop은 volume이나 credential을 지우지 않는다. server restart는 다시 unseal을,
Agent restart는 유효한 AppRole 재인증 입력을 요구할 수 있다. `agent.hcl` 단일 파일
변경은 [POL-0006](../../policies/01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의
대상 재생성·hash 검사를 따른다. Compose의 server 환경 변경도 재생성이 필요하다.
재생성 전후 Raft mount identity가 바뀌면 중단한다. 자동 bootstrap job은 없으며
이 절차의 daemon health를 초기화 완료로 표시하지 않는다.

upgrade는 [RUN-0086](../10-platform-and-backup/0086-dependency-version-management.md), backup·retention은
[POL-0021](../../policies/10-platform-and-backup/0021-backup-and-restore.md)을 적용한다. 아래 격리 restore는
계획이지 검증된 실행 명령이 아니다. artifact·custody·격리 target·승인·독립 검토가
없으면 복구는 BLOCKED이며 @buenhyden에게 반환한다. in-place Raft downgrade,
기존 volume restore, 마지막 관리 credential 삭제는 금지한다. 제거/cleanup은
consumer와 보호 자료 disposition이 별도 승인된 뒤에만 수행하며 명령을 추정하지 않는다.

### Initial Bootstrap and Credential Recovery

owner가 승인한 initial bootstrap은 threshold 2의 Shamir unseal share 3개를 사용한다.
임시 전달 후 share는 서로 분리된 오프라인 custody에 보관한다. 모든 share를 담은 단일
파일은 custody 분리가 아니다. initialization 출력은 절대 출력하지 않고, credential을
명령 인자에 넣지 않으며, 복구 자료를 commit하지 않는다. 초기 root credential은 human
OIDC 로그인, 기대되는 non-root policy, 인증된 recovery, Agent 인증/렌더링, 보호된 Raft
스냅샷이 모두 성공한 뒤에만 폐기해야 한다. setup이 실패하면 운영자 복구를 위해 보호된
복구 자료를 유지한다.

이 HOME은 1인 관리자 결정(SPEC-0242)으로 share를 host에 두며 아래 [1인 관리자 custody 절차](0105-openbao-maintenance-window.md#1인-관리자-custody-절차)를 따른다. 기존2026-09-22 custody 결정과 단일 파일 위험·미기록 종료 조건은
[POL-0085 Exceptions](../../policies/04-security-and-secrets/0085-openbao.md#existing-custody-decision-and-missing-closure)가
소유한다. 이 예외는 share 분리 검증을 뜻하지 않는다. 승인된 운영자는 대화형
`docker compose exec openbao bao operator unseal`의 숨겨진 prompt로 share를 하나씩
전달한다. 인자로 전달하지 않으며 레거시 Vault share로 OpenBao를 unseal할 수 없다.
2026-09-25 SPEC-0182 W5가 그 파일들(`secrets/.retired/2026-09-23/security/`의
`vault_token.txt`와 `vault_unseal_keys.legacy.txt`), 보존된 Vault 트리
`${DEFAULT_MOUNT_VOLUME_PATH}/security/vault`, 레거시 `hashicorp/vault` 이미지를
폐기했다. 데이터가 사라졌으므로 레거시 Vault root token은 의미가 없다.

`hy-home-renderer` AppRole은
[renderer policy](../../../../infra/03-security/openbao/config/policies/renderer.hcl)를
사용한다. 구성된 두 KV v2 data 경로와 각각의 metadata 경로만 read하며, write/list/admin 권한은 부여하지 않는다.
표준 default policy가 token 자체 갱신을 제공한다. 현재 역할의 `token_period=24h`,
`token_ttl=0`, `token_max_ttl=0`과 발급 token의 `explicit_max_ttl=0`에서 24시간은
갱신 주기다. 갱신이 계속되면 총수명 상한이 없다([공식 token 수명](https://openbao.org/docs/concepts/tokens/)).
SecretID TTL은 10분, 사용 횟수는 1회다. sink 복사본도 갱신 가능하고 W5는 이전 Agent token을
폐기하지 않는다. 두 KV 읽기·sink0600과 2026-12-15까지의 기존 예외를 유지한다.
유한수명이나 이전 세대 폐기는 아래 인계와 POL-0085의 별도 결정이 필요하다. Agent는 SecretID 파일을 읽은 뒤
삭제하므로, token이 끝나면 새 SecretID를 전달해야 한다([RUN-0103](0103-openbao-renderer-delivery.md#renderer-secretid-delivery)). 기존 Docker Secret 소비자는 현재 파일을 계속 사용하며, 렌더링된 출력이 자동으로
애플리케이션 mount를 전환하지는 않는다.

### OIDC Configuration Contract

| Surface | Required setting |
| --- | --- |
| Keycloak realm/client | `hy-home.realm` / `home-openbao`, confidential client-secret 인증 |
| Flow | Authorization Code 활성화; S256 PKCE 필수; implicit/password/service-account flow 비활성화 |
| Claim mapper | `oidc-group-membership-mapper`; claim은 `groups`; ID token에 전체 group 경로 포함 |
| Membership | 기존 운영자 `hyunyoun`은 `/openbao-admins`에 속함; 모든 realm 사용자에게 자동 권한 부여하지 않음 |
| OpenBao mount/role | `oidc` / `home-admin`, role type은 `oidc`, user claim은 `sub`, groups claim은 `groups` |
| Binding | 정확한 `bound_claims.groups=["/openbao-admins"]`, audience는 `home-openbao` |
| Issuer | `https://keycloak.hy.home.arpa/realms/hy-home.realm`; 검증된 CA를 `oidc_discovery_ca_pem`으로 제공 |
| UI callback | `https://openbao.hy.home.arpa/ui/vault/auth/oidc/oidc/callback` |
| CLI callback | `http://localhost:8250/oidc/callback` |
| 사용자 token | `hy-home-operator`와 기본 `default`; TTL 1h, 최대 TTL 4h; root 또는 periodic token 아님 |

위 hostname은 현재 HOME default다. 도메인이 바뀌면 issuer, 인증서, 정확한 redirect를 함께
갱신하며, wildcard redirect는 도입하지 않는다. Keycloak은 자신의 client secret을 저장하고
OpenBao는 구성된 사본을 보호된 backend 상태에 저장하므로, 새로운 평문 `.env` client-secret
키는 필요 없다. [Official Keycloak integration](https://openbao.org/docs/auth/jwt/oidc-providers/keycloak/)이
provider 설정 맥락을 제공한다. 이 contract는 인증된 모든 사용자에게 admin 접근을 부여하는
대신 의도적으로 정확한 callback과 group binding을 사용한다.

### Human Login and Normal Root Recovery

1. [guide](../../guides/04-security-and-secrets/0085-openbao.md)를 사용해 OIDC를 통해 role `home-admin`으로 로그인한다.
   결과 policy가 `default`와 `hy-home-operator`이며 절대 `root`가 아님을 확인한다.
2. operator policy는 quorum ceremony에서만 인증된 `/sys/generate-root-token/attempt`와
   `/sys/generate-root-token/update`를 허용한다. attempt를 시작하면 민감한 OTP/nonce
   자료가 반환되므로 터미널이나 chat이 아니라 보호된 custody로 바로 캡처한다. 서로 다른
   share 2개를 보호된 입력 채널로 제공한다. share나 OTP를 인자로 전달하지 않는다.
3. 보호된 프로세스 내부에서 원본 OTP로 반환된 인코딩 token을 디코드한다. Base64 출력은
   padding을 생략할 수 있으므로 지원되는 클라이언트나 검증된 디코더를 사용한다. 디코딩
   실패로 새로 발급된 root token을 잃지 않도록 인코딩된 응답을 디코딩 전에 보존한다.
4. root는 승인된 작업에만 사용한다. 일반 OIDC 접근이 여전히 동작하는지 확인하고, 미완료
   attempt를 취소하고, 임시 root를 폐기하고, 그 lookup이 거부됨을 확인한다. 마지막으로
   남은 정상 작동하는 관리 경로를 일찍 폐기하지 않는다.

현재 CLI `bao operator generate-root`는 인증된 API를 사용한다.
[official command reference](https://openbao.org/docs/commands/operator/generate-root/)와
[authenticated API](https://openbao.org/docs/api/system/generate-root-token/)가 이
호환성 경계를 설명한다. 일상적인 unseal은 로그인과 별개이며 관리자 승인과 혼동해서는 안
된다.

### hy-home.k8s Kubernetes Auth

Kubernetes auth 방식, `eso-read-platform`과 `k8s-bootstrap` policy/role,
`secret/platform/*`, rebuild별 구성과 bootstrap token은 hy-home.k8s 통합의 한
단계다. 저장소 준비부터 cluster에서의 검증까지 이어지는 end-to-end 절차는
[hy-home.k8s integration runbook](../10-platform-and-backup/0096-k8s-integration.md)(OpenBao는 phase 5)에
있다. 위 규칙은 그대로 적용된다. 임시 root는 승인된 세션에서만 사용하고 폐기로 끝낸다.

### No Administrative Identity: Explicit Break-glass Recovery

이 절차는 데이터와 quorum share가 보존된 상태에서 확인된 lockout에만 사용한다. 정확한
재시작과 임시 listener에 대해 명시적 승인을 받는다. 다시 initialize하거나, volume을
교체하거나, 실제 데이터 위에 스냅샷을 복원하거나, 기존 network listener를 약화시키지
않는다.

1. 이미지 ID, cluster ID, 기존의 모든 mount 식별자를 기록한다. 가능하면 보호된 스냅샷을
   보존한다. 동일한 이미지, 스토리지, seal 구성을 유지한다.
2. 임시 Compose override에서 `disable_unauthed_generate_root_endpoints=false`로 설정한
   container-loopback listener를 `127.0.0.1:18200`에만 추가한다. 일반 listener에서는 그
   플래그를 명시적으로 true로 유지한다. 추가 port는 게시하지 않는다.
3. `--no-deps --pull never --no-build`로 OpenBao만 재생성한 뒤 같은 cluster를 unseal한다.
   `docker exec`와 보호된 stdin을 통해 레거시 `/sys/generate-root/attempt`와
   `/sys/generate-root/update` API를 quorum과 함께 사용한다. 일반 generate-root CLI는
   다른 인증 API를 대상으로 한다.
4. 응답과 디코드된 rescue token을 바로 0600 파일로 저장한다. root가 복구되는 즉시 임시
   override를 제거하고, OpenBao만 재생성하고, 다시 unseal한다. 보조 listener가 사라졌고,
   일반 레거시 endpoint가 인증되지 않은 접근을 거부하며, mount/cluster 식별자가 일치함을
   확인한다.
5. 승인된 native OIDC client, 정확한 group-bound role, operator policy를 구성한다. issuer
   CA를 신뢰하고, TLS 검사를 절대 비활성화하지 않는다. client나 group 멤버십을 바꾸기 전에
   대상 지정 Keycloak rollback 영수증을 기록한다.
6. 실제 human OIDC 로그인을 요구하고 non-root policy임을 확인한다. 그 policy로 capability
   거부, 스냅샷 읽기, share를 제출하지 않는 인증된 root recovery start/cancel을 테스트한다.
   Agent 렌더링을 다시 확인한다.
7. 새 보호된 스냅샷을 만들고, rescue root를 폐기하고, 거부됨을 검증한다. human 승인이
   실패하면 rescue custody를 보호된 상태로 유지하며 접근을 복구하고, 대기 중 loopback
   listener를 활성 상태로 두지 않는다.

이 절차는 [deprecated API](https://openbao.org/docs/api/system/generate-root/)를 명시적으로
승인된 복구 창에서만 사용한다. 일반 운영에서는
[listener contract](https://openbao.org/docs/configuration/listener/tcp/)가 요구하는 대로
계속 비활성 상태로 유지해야 한다.

## Verification

### Exact policy validation

Kubernetes auth의 ESO 허용 범위는 [POL-0085](../../policies/04-security-and-secrets/0085-openbao.md#hy-homek8s-kubernetes-auth)의
기존 승인된 다섯 data/metadata 항목 read로 제한한다. 정적 hardening은 일부 금지
capability를 검사하지만 정확한 전체 path set이나 실제 설치 role을 증명하지 않는다.
renderer 두 data와 해당 metadata 경로 read와 사람 operator의 platform credential create/update는 별개다.
승인된 변경 후에는 exact binding과 경로 밖 read/list/write 거부를 비밀값 없는
결과로 확인하며 불일치 시 중단한다.

### 증거 기록

날짜, configuration commit, 서비스 이름, exit status, 정제된 health/resource 결과를 현재
Task에 기록한다. secret 값, 원본 환경, state, token 파일, 메시지/database 콘텐츠는 캡처하지
않는다. 날짜가 기록된 런타임 결과와 recovery-custody 전달은 현재 Task에 속한다.

## Failure and Recovery

### Rollback or Recovery

maintenance window의 W4 실패는 fix-forward가 규칙이다([W4](0105-openbao-maintenance-window.md#maintenance-window-plan)의 rollback
규칙). 아래 snapshot 복원은 새 owned image에서 고칠 수 없는 손상에 대한 별도 승인 경로다.

non-root operator 신원으로 보호된 Raft 스냅샷을 캡처하고, checksum, cluster ID, 이미지
선언, seal 구성, custody 영수증을 기록한 뒤, network egress와 consumer가 비활성화된 새
데이터 volume에서 복원을 리허설한다. 지원되는 이미지를 복원된 volume에 대해서만 시작하고,
threshold unseal ceremony를 완료하고, secret 값을 공개하지 않고 cluster ID, mount, policy,
auth 방식, Agent 인증/렌더링, denial 테스트를 검증한다. 증거가 승인된 후 격리 사본을
파기한다. 실제 Raft 데이터 위에는 절대 복원하지 않는다. 이 격리 restore는 계획된 채로
남아 있으며 2026-09-20 수정 중에는 실행되지 않았다.

스냅샷은 캡처 시점의 token 상태를 담는다. root 폐기 이전에 캡처한 스냅샷을 복원하면
그 credential 상태가 복원될 수 있다. 격리 recovery validation 중 복원된 bootstrap/recovery
token을 재확인하고 폐기한다. 임시 root가 폐기된 후 operator 신원으로 일상적인 backup을
수행한다. 기존 Raft 데이터 위에 initialize하거나 스토리지를 제자리에서 다운그레이드하지
않는다.

### Escalation

credential, 파괴적 스토리지 변경, remote 변경, 또는 backup 부재로 안전한 진행이 불가능하면
중단하고 @buenhyden에게 연락한다.

## Related Documents

### Traceability

- 관장 architecture: [AD-0003](../../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](../../guides/04-security-and-secrets/0085-openbao.md), [Policy](../../policies/04-security-and-secrets/0085-openbao.md), [Runbook](0085-openbao.md)
- 분리된 런북: [RUN-0103](0103-openbao-renderer-delivery.md), [RUN-0104](0104-openbao-metrics-credential.md), [RUN-0105](0105-openbao-maintenance-window.md), [RUN-0106](0106-openbao-consumer-catalog.md)

- [운영 인덱스](../../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
