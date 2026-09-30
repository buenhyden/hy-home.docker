---
title: "OpenBao Runbook"
version: "0.6.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "operations"
artifact_id: "RUN-0085"
parent_ids:
- "POL-0085"
created: "2026-09-19"
---

# OpenBao Runbook

## When to Use

`openbao openbao-agent` readiness 점검과 승인된 대상 지정 배포 또는 복구에 사용한다. 저장소
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
4. 배포가 승인되면 이 서비스들만 명시하고 initialization job과 daemon readiness를 별도로
   검증한다. 예상치 못한 mount나 실패한 점검이 있으면 중단하고, 전체 stack으로 범위를
   넓히지 않는다.

[Implementation](../../../infra/03-security/openbao/docker-compose.yml)과 [version projection](../../../infra/tech-stack.versions.json)이 런타임 고정 버전을 소유한다.

### Initial Bootstrap and Credential Recovery

owner가 승인한 initial bootstrap은 threshold 2의 Shamir unseal share 3개를 사용한다.
임시 전달 후 share는 서로 분리된 오프라인 custody에 보관한다. 모든 share를 담은 단일
파일은 custody 분리가 아니다. initialization 출력은 절대 출력하지 않고, credential을
명령 인자에 넣지 않으며, 복구 자료를 commit하지 않는다. 초기 root credential은 human
OIDC 로그인, 기대되는 non-root policy, 인증된 recovery, Agent 인증/렌더링, 보호된 Raft
스냅샷이 모두 성공한 뒤에만 폐기해야 한다. setup이 실패하면 운영자 복구를 위해 보호된
복구 자료를 유지한다.

Owner 결정(2026-09-22): 세 share는 `secrets/security/openbao_unseal_keys.txt`
(SEC-003, share 한 줄당 하나, `0600`, Git-ignored, 컨테이너에 절대 mount하지 않음)에
함께 보관한다. 이 결정은 분리 custody의 명시적 예외다. 그 파일을 읽을 수 있는 사람은 누구나
OpenBao를 unseal할 수 있다. 대화형 터미널에서 unseal하고
(`docker compose exec openbao bao operator unseal`) 숨겨진 프롬프트에 share 하나를
붙여넣는다. share를 절대 인자로 전달하지 않는다. 비공개 registry는 SEC-003의 placeholder만
보관하며, 그 파일이 유일한 사본이다. 레거시 Vault 파일로는 OpenBao를 unseal할 수 없다.
2026-09-25 SPEC-0182 W5가 그 파일들(`secrets/.retired/2026-09-23/security/`의
`vault_token.txt`와 `vault_unseal_keys.legacy.txt`), 보존된 Vault 트리
`${DEFAULT_MOUNT_VOLUME_PATH}/security/vault`, 레거시 `hashicorp/vault` 이미지를
폐기했다. 데이터가 사라졌으므로 레거시 Vault root token은 의미가 없다.

`hy-home-renderer` AppRole은
[renderer policy](../../../infra/03-security/openbao/config/policies/renderer.hcl)를
사용한다. 구성된 두 KV v2 데이터 경로만 read하며, write/list/admin 권한은 부여하지 않는다.
표준 default policy가 token 자체 갱신을 제공한다. Agent token은 갱신되다가 최대 수명에서
끝나며, SecretID는 10분 후 만료되고 1회만 사용할 수 있다. Agent는 SecretID 파일을 읽은 뒤
삭제하므로, token이 끝나면 새 SecretID를 전달해야 한다(아래 Renderer SecretID Delivery). 기존 Docker Secret 소비자는 현재 파일을 계속 사용하며, 렌더링된 출력이 자동으로
애플리케이션 mount를 전환하지는 않는다.

### Renderer SecretID Delivery

Agent는 `/openbao/agent/role_id`(volume `openbao-agent-data`에 남아 있다)와
`/openbao/agent/secret_id`로 AppRole `hy-home-renderer`에 로그인하고, 읽은
`secret_id` 파일을 지운다([agent.hcl](../../../infra/03-security/openbao/config/agent.hcl)).
SecretID는 1회용이므로 Agent가 다시 로그인해야 할 때마다 새 SecretID를 전달한다.
다시 로그인해야 하는 경우는 다음과 같다.

- OpenBao 재시작과 unseal 뒤([RUN-0098](0098-cold-start-and-reboot.md) 6단계).
- Agent token이 최대 수명에 닿은 뒤. 2026-09-24 09:57Z에 로그인한 token은
  2026-09-25까지 갱신된 뒤 2026-09-26 16:51Z에 `lifetime watcher done`으로
  끝났고, Agent는 그 뒤로 로그인하지 못했다.
- `openbao-agent` 컨테이너를 새로 만든 뒤.

**판별.** healthcheck(`test -s /openbao/agent/token`)는 남아 있는 옛 token
파일만 보므로, Agent가 로그인하지 못해도 `healthy`다. 아래 개수가 0보다 크면
전달이 필요하다.

```bash
docker logs --since 1h openbao-agent 2>&1 | grep -c 'error getting path or data from method'
```

**전제 조건.**

- `bao status`가 `Sealed false`다.
- `role_id`가 있고 `secret_id`가 없다(내용은 읽지 않는다).
- 이 절차는 SecretID를 CLI 세션에서 발급해 Agent volume으로 바로 흘려보내므로, UI
  OIDC 로그인만으로는 부족하다. 호스트에는 `bao` CLI가 없으므로
  [RUN-0096](0096-k8s-integration.md) 5.2와 같은 일회용 client 컨테이너를 쓴다.
- 브라우저가 다른 기기에서 실행되면 먼저 `ssh -L 8250:localhost:8250 <host>`로 OIDC
  callback 포트를 포워딩한다.

```bash
docker compose exec -T openbao bao status | grep Sealed
docker exec openbao-agent sh -c 'test -s /openbao/agent/role_id && echo role_id-ok; test -e /openbao/agent/secret_id && echo secret_id-present || echo secret_id-absent'
```

기대 결과: `Sealed false`, `role_id-ok`, `secret_id-absent`.

**절차.** 저장소 루트에서 한 셸로 실행한다. `B`는 token을 호스트의 `0700` 임시
디렉터리(`$T/.vault-token`)에만 저장한다.

1. client를 정의하고 OIDC로 로그인한다. token은 출력되지 않는다. 이 단계에서는 SecretID의
   10분이 아직 흐르지 않는다.

   ```bash
   T=$(mktemp -d); IMG=$(docker compose config --images openbao)
   B() { docker run --rm -i --network host --user "$(id -u):$(id -g)" -e HOME=/h -v "$T:/h" \
     -e BAO_ADDR=https://openbao.hy.home.arpa -e BAO_CACERT=/ca.pem \
     -v "$PWD/secrets/certs/rootCA.pem:/ca.pem:ro" --entrypoint bao "$IMG" "$@"; }
   B login -no-print -method=oidc -path=oidc role=home-admin
   B token lookup -format=json | grep -c '"hy-home-operator"'
   ```

   기대 결과: 브라우저 로그인 성공, 개수 `1` 이상. `0`이면 `/openbao-admins` 멤버십과
   role을 확인한다(OIDC Configuration Contract).

2. SecretID를 발급하고 같은 파이프로 Agent volume에 쓴다. 값은 화면, 명령 인자, shell
   history에 남지 않는다. `-field`는 끝 줄바꿈 없이 값만 내보낸다. 임시 파일에 먼저 쓰고
   비어 있지 않을 때만 `mv`로 바꾸므로, Agent가 반쯤 쓴 파일을 읽지 않는다. 발급 시점부터
   10분 안에 3단계까지 끝낸다.

   ```bash
   B write -f -field=secret_id auth/approle/role/hy-home-renderer/secret-id \
     | docker exec -i openbao-agent sh -c 'umask 077 && cat > /openbao/agent/secret_id.new && test -s /openbao/agent/secret_id.new && mv /openbao/agent/secret_id.new /openbao/agent/secret_id' \
     && echo delivered || docker exec openbao-agent rm -f /openbao/agent/secret_id.new
   ```

   기대 결과: `delivered`. `docker exec`는 Agent와 같은 uid 100으로 쓰므로 Agent가 파일을
   읽을 수 있다.

3. Agent가 바로 읽게 재시작한다. 재시작하지 않으면 Agent는 다음 재시도(backoff 약 4~5분)에
   읽는다.

   ```bash
   docker restart openbao-agent
   docker logs --since 2m openbao-agent 2>&1 | grep -c 'authentication successful'
   docker exec openbao-agent sh -c 'test -e /openbao/agent/secret_id && echo not-consumed || echo consumed; stat -c %y /openbao/agent/token'
   ```

   기대 결과: 개수 `1` 이상, `consumed`, token 파일 시각이 방금이다.

4. 세션을 정리한다.

   ```bash
   B token revoke -self; rm -f "$T/.vault-token"; rmdir "$T"
   ```

   기대 결과: `rmdir`가 성공한다. 실패하면 `$T`에 남은 파일을 확인한다.

**실패 처리.**

- 2단계가 `permission denied`로 실패하면 로그인한 token에 `hy-home-operator`가 없다는
  뜻이다. 1단계의 policy 확인으로 돌아간다.
- 10분이 지나 3단계의 개수가 `0`이고 `invalid secret id`가 기록되면 2단계부터 새로
  발급한다. 쓰이지 않은 SecretID는 만료되면 사라진다.
- `secret_id.new`가 남아 있으면 지운 뒤 2단계를 다시 실행한다.

**증거.** 발급 시각, `delivered`, 인증 성공 개수, `consumed`, token 파일 시각만
현재 Task에 기록한다. SecretID, role_id, token 값은 기록하지 않는다.

**알려진 한계.** SecretID가 1회용이고 읽은 뒤 지워지므로, Agent는 token이 최대 수명에
닿으면 사람의 전달 없이 다시 로그인하지 못한다. 위 판별 명령으로 주기적으로 확인한다.
자동 재로그인(주기 token, 재사용 가능한 SecretID와 CIDR 바인딩 등)은 보안 설계를
바꾸므로 Spec으로 결정한다.

### Prometheus Metrics Credential

이 절차는 승인이 OpenBao policy/token 변경과 Prometheus 재생성을 정확한 대상으로 명시한
경우에만 사용한다.

1. OpenBao가 initialized/unsealed 상태이고, 검토된 `prometheus.hcl`이 `sys/metrics`에
   대한 `read`만 포함하며, 승인된 관리자가 대기 중이고, rollback이 현재 configuration
   commit을 사용함을 확인한다. Prometheus credential로 renderer AppRole, renderer sink
   token, human operator token, root token을 사용하지 않는다.
2. policy를 적용하고 default policy가 없는 새 orphan service token을 발급한다. 유효 시스템
   최댓값 이내의 유한한 TTL을 부여하고, 만료 시각과 accessor를 보호된 custody에 기록하고,
   token 값만 mode `0640`, group `SECRETS_GID`로 `secrets/security/openbao_token.txt`에
   전달한다(Prometheus는 `group_add`를 통해 `nobody`로 이를 읽는다). 출력하거나 인자로
   전달하지 않는다. 아래 명령의 owner-only 세션 디렉터리만 스테이징으로 허용되며 이후
   삭제한다.
3. 보호된 입력을 통해 새 token이 `sys/metrics`를 읽을 수 있고 관련 없는 secret 경로와
   관리 경로에서는 거부됨을 검증한다. boolean allow/deny 결과와 유효 TTL만 기록하고,
   token이나 원본 응답은 절대 기록하지 않는다.
4. 승인된 재생성 전에 Compose와 Prometheus 구성을 검증한다. Prometheus만 재생성하고
   구성 로드/reload가 성공했음을 확인한 뒤, 원본 target 응답이나 로그를 기록하지 않고
   `openbao` target이 `UP`을 보고할 것을 요구한다.
5. 먼저 교체본을 생성하고 검증한 뒤, `0600` 파일을 원자적으로 교체하고 Prometheus만
   재생성하고 새 target을 확인하고 accessor로 이전 token을 폐기해 회전시킨다.
   레거시 Vault root token 권한이나 scrape job을 절대 복원하지 않는다.

policy 적용, token validation, 구성 로드, 또는 target health가 실패하면 이전
source/runtime 구성을 계속 사용 가능하게 유지하고, accessor로 새 token을 폐기하고,
승인된 credential 처리 범위 내에서만 local 파일을 제거한다. 검토된 rollback commit에서
Prometheus만 재생성한다. source rollback은 `vault_token`을 다시 도입해서는 안 된다.
전용 credential 경로가 복구될 때까지 OpenBao metrics는 비활성 상태로 둔다.

5단계 명령은 [hy-home.k8s integration runbook](0096-k8s-integration.md)의
throwaway 클라이언트(5.2, `/s/k8s`는 host의 owner-only `/tmp/bao-k8s`)에서, 그
임시 root 세션(5.4, `R`이 명령마다 root를 전달) 안에서 실행한다. operator policy는
`prometheus` policy를 가진 token을 발급할 수 없다.

```sh
R policy write prometheus /policies/prometheus.hcl
R token create -orphan -no-default-policy -policy=prometheus -ttl=720h -field=token >/s/k8s/metrics.token
R write -format=json auth/token/lookup token=@/s/k8s/metrics.token | grep -E '"(accessor|expire_time)"' >/s/k8s/metrics.custody
grep -c . /s/k8s/metrics.custody
BAO_TOKEN="$(cat /s/k8s/metrics.token)" bao read sys/metrics >/dev/null 2>&1 && echo "metrics: allowed" || echo "metrics: DENIED"
BAO_TOKEN="$(cat /s/k8s/metrics.token)" bao policy list >/dev/null 2>&1 && echo "policy list: LEAK" || echo "policy list: denied"
```

예상 결과: `2`(custody 줄 수, 개수만 세고 절대 표시하지 않음), `metrics: allowed`,
`policy list: denied`. token은 자기 자신을 lookup할 수 없다. 유일한 policy가
`sys/metrics`이므로 root로 lookup한다. root 세션은 열어 둔다. host에서 같은
mode와 group으로 파일을 교체하고, Prometheus만 재생성하고 target을 기다린다.

```bash
install -m 640 -g "$(stat -c %g secrets/security/openbao_token.txt)" /tmp/bao-k8s/metrics.token secrets/security/.openbao_token.new
mv secrets/security/.openbao_token.new secrets/security/openbao_token.txt
rm -f /tmp/bao-k8s/metrics.token
docker compose --profile obs up -d --no-deps --force-recreate --wait prometheus
sleep 45   # one scrape interval after the recreate
docker exec infra-prometheus wget -qO- 'http://localhost:9090/api/v1/query?query=up%7Bjob%3D%22openbao%22%7D' | grep -o '"value":\[[^]]*\]'
```

예상 결과: 값 `"1"`. Prometheus는 host port를 게시하지 않으므로 점검은 컨테이너 내부에서
실행한다. custody 파일은 `accessor=`, `expires=`, `issued=`, `policy=` 줄을 담는다.
기존 파일을 컨테이너용으로 준비하고 root 세션에서 그 파일로 폐기한 뒤, 같은 형식으로 새
파일을 작성한다.

```bash
install -m 600 secrets/security/openbao_metrics_token.custody /tmp/bao-k8s/old.custody
```

```sh
R token revoke -accessor "$(sed -n 's/^accessor=//p' /s/k8s/old.custody)"
R token lookup-accessor "$(sed -n 's/^accessor=//p' /s/k8s/old.custody)" >/dev/null 2>&1 && echo "old: STILL VALID" || echo "old: revoked"
```

```bash
umask 077
A=$(sed -n 's/.*"accessor": *"\([^"]*\)".*/\1/p' /tmp/bao-k8s/metrics.custody)
E=$(sed -n 's/.*"expire_time": *"\([^"]*\)".*/\1/p' /tmp/bao-k8s/metrics.custody)
[ -n "$A" ] && [ -n "$E" ] && printf 'accessor=%s\nexpires=%s\nissued=%s\npolicy=prometheus\n' "$A" "$E" "$(date -u +%FT%TZ)" >secrets/security/.openbao_metrics_token.custody.new
test -s secrets/security/.openbao_metrics_token.custody.new && mv secrets/security/.openbao_metrics_token.custody.new secrets/security/openbao_metrics_token.custody
unset A E; sed -n 's/^expires=//p' secrets/security/openbao_metrics_token.custody
rm -f /tmp/bao-k8s/old.custody /tmp/bao-k8s/metrics.custody
```

예상 결과: `old: revoked`, 그다음 새 만료일(secret이 아니므로 기록한다). 그런 다음 통합
runbook의 root 폐기 단계(`root revoked`, `Started false`)로 root 세션을 종료한다.

Agent 재시작 전에 승인된 운영자는 보호된 채널을 통해 새 SecretID를 전달해야 한다.
RoleID/SecretID 파일(0600, 컨테이너 UID 100/GID 1000)을 배치하는 동안 Agent만 중단한
뒤 시작한다. Agent가 소비하기 전에 같은 일회용 SecretID로 test-login하지 않는다.
server를 재시작하면 unseal ceremony가 필요하고 Agent token을 잃거나 만료되어도 새 AppRole
credential이 필요하다. 발급에는 승인된 운영자 신원이 필요하다. 아직 수립되지 않았다면
아래의 별도로 승인된 loopback recovery 절차를 사용한다. 일반 generate-root도 현재 API에서
인증된 권한이 필요하다. quorum key만으로는 그 endpoint를 승인할 수 없다. 자동화 지름길로
활성 영구 root token을 저장하지 않는다.

전달 명령. OIDC 운영자가 SecretID를 발급할 수 있다(통합 runbook의 5.2 클라이언트와 5.3
로그인, root 불필요).

```sh
bao write -f -field=secret_id auth/approle/role/hy-home-renderer/secret-id >/s/k8s/secret_id
```

SecretID는 10분간 유효하다. host에서 그 시간 내에 실행한다.

```bash
docker stop openbao-agent
T=$(date -u +%FT%TZ)
docker run --rm --user 0 -v hy-home-infra_openbao-agent-data:/a -v /tmp/bao-k8s:/s:ro --entrypoint install "$(docker inspect openbao-agent --format '{{.Config.Image}}')" -m 600 -o 100 -g 1000 /s/secret_id /a/secret_id
rm -f /tmp/bao-k8s/secret_id
docker start openbao-agent
sleep 20
docker logs --since "$T" openbao-agent 2>&1 | grep -c 'authentication successful'
docker logs --since "$T" openbao-agent 2>&1 | grep -ciE 'no known secret ID|permission denied|invalid'
```

예상 결과: 최소 `1`, 그다음 `0`. 여기서는 health와 사라진 `secret_id` 파일만으로는 아무것도
증명하지 못한다. volume은 이전 token 파일을 유지하고, Agent는 로그인 성공 전에 SecretID를
읽자마자 삭제한다.

unsealed 상태, Agent health, 주기적 token 갱신 능력, 정확한 read/deny 능력, 두 출력
파일(0600) 모두를 검증한다. 출력 바이트를 승인된 source와 비공개로 비교하고 boolean
결과만 기록한다. 원본 Docker Secret 값을 보존한다. backup 생성만으로는 restore
readiness를 증명할 수 없다.

### OIDC Configuration Contract

| Surface | Required setting |
| --- | --- |
| Keycloak realm/client | `hy-home.realm` / `home-openbao`, confidential client-secret authentication |
| Flows | Authorization Code enabled; S256 PKCE required; implicit/password/service-account flows disabled |
| Claim mapper | `oidc-group-membership-mapper`; claim `groups`; full group paths in ID token |
| Membership | Existing operator `hyunyoun` belongs to `/openbao-admins`; no automatic grant to all realm users |
| OpenBao mount/role | `oidc` / `home-admin`, role type `oidc`, user claim `sub`, groups claim `groups` |
| Binding | Exact `bound_claims.groups=["/openbao-admins"]`, audience `home-openbao` |
| Issuer | `https://keycloak.hy.home.arpa/realms/hy-home.realm`; verified CA supplied through `oidc_discovery_ca_pem` |
| UI callback | `https://openbao.hy.home.arpa/ui/vault/auth/oidc/oidc/callback` |
| CLI callback | `http://localhost:8250/oidc/callback` |
| Human token | `hy-home-operator` plus standard `default`; TTL 1h, max TTL 4h; no root or periodic token |

위 hostname은 현재 HOME default다. 도메인이 바뀌면 issuer, 인증서, 정확한 redirect를 함께
갱신하며, wildcard redirect는 도입하지 않는다. Keycloak은 자신의 client secret을 저장하고
OpenBao는 구성된 사본을 보호된 backend 상태에 저장하므로, 새로운 평문 `.env` client-secret
키는 필요 없다. [Official Keycloak integration](https://openbao.org/docs/auth/jwt/oidc-providers/keycloak/)이
provider 설정 맥락을 제공한다. 이 contract는 인증된 모든 사용자에게 admin 접근을 부여하는
대신 의도적으로 정확한 callback과 group binding을 사용한다.

### Human Login and Normal Root Recovery

1. [guide](../guides/0085-openbao.md)를 사용해 OIDC를 통해 role `home-admin`으로 로그인한다.
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
[hy-home.k8s integration runbook](0096-k8s-integration.md)(OpenBao는 phase 5)에
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

## Evidence

날짜, configuration commit, 서비스 이름, exit status, 정제된 health/resource 결과를 현재
Task에 기록한다. secret 값, 원본 환경, state, token 파일, 메시지/database 콘텐츠는 캡처하지
않는다. 날짜가 기록된 런타임 결과와 recovery-custody 전달은 현재 Task에 속한다.

## Rollback or Recovery

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

## Escalation

credential, 파괴적 스토리지 변경, remote 변경, 또는 backup 부재로 안전한 진행이 불가능하면
중단하고 @buenhyden에게 연락한다.

## Traceability

- 관장 architecture: [AD-0003](../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](../guides/0085-openbao.md), [Policy](../policies/0085-openbao.md), [Runbook](0085-openbao.md)

## Related Documents

- [운영 인덱스](../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
