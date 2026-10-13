---
title: "OpenBao Runbook"
version: "0.7.10"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "operations"
artifact_id: "RUN-0085"
parent_ids:
- "POL-0085"
created: "2026-09-19"
---

# OpenBao Runbook

## Overview

이 런북은 OpenBao(`openbao`, `openbao-agent`)의 상태 점검, 승인된 대상 기동·중지, initial bootstrap, Renderer SecretID 전달, 복구를 다룬다. OpenBao는 재시작 뒤 owner가 직접 하는 수동 Shamir unseal이 필요하다. 이 문서의 어떤 단계도 unseal share를 대신 입력하거나 자동화하지 않는다.

## Trigger and Preconditions

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

기존2026-09-22 custody 결정과 단일 파일 위험·미기록 종료 조건은
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
표준 default policy가 token 자체 갱신을 제공한다. Agent token은 갱신되다가 최대 수명에서
끝나며, SecretID TTL은 10분, 사용 횟수는 1회로 설정한다. 고정 버전의 만료 결함은 아래 Known Runtime Residual을 확인한다. Agent는 SecretID 파일을 읽은 뒤
삭제하므로, token이 끝나면 새 SecretID를 전달해야 한다(아래 Renderer SecretID Delivery). 기존 Docker Secret 소비자는 현재 파일을 계속 사용하며, 렌더링된 출력이 자동으로
애플리케이션 mount를 전환하지는 않는다.

### Renderer SecretID Delivery

현재 source는 60초 wrapping, issuer/cleanup 분리, 영속 journal을 함께 사용한다.
`operator`는 renderer SecretID를 직접 만들 수 없다. 두 token role은 각각 정확한 policy만
허용하며 5분·비갱신·default policy 없음·explicit max TTL 5분을 요구한다.
[issuer role](../../../../infra/03-security/openbao/config/renderer-issuer-token-role.json),
[cleanup role](../../../../infra/03-security/openbao/config/renderer-cleanup-token-role.json),
[issuer policy](../../../../infra/03-security/openbao/config/policies/renderer-issuer.hcl),
[cleanup policy](../../../../infra/03-security/openbao/config/policies/renderer-cleanup.hcl)를
승인된 관리 신원이 먼저 적용한다. HOME 적용 여부는 별도이며 source를 배포 증거로 쓰지 않는다.
cleanup의 자원 권한은 해당 renderer accessor 목록·조회·폐기뿐이다. 두 token의
`lookup-self`는 정확한 policy·TTL·비갱신 신원을 검사하며 다른 KV나 AppRole을 열지 않는다.

1. TLS·unseal·두 제한 KV/version·정확한 Agent named volume과 RoleID를 준비한다.
   기존 Agent 자동 재시작이나 sink 존재를 준비 완료로 판단하지 않는다. 운영자가 지정한
   journal 디렉터리는 Agent data/out volume 밖에 영속 보관하고 owner mode 0700을 요구한다.
   journal과 completion anchor를 따로 삭제·초기화하지 않는다. 값·token·accessor는 기록하지 않는다.
2. 검토한 전체 commit SHA로 host helper를 operator-private 디렉터리에 설치한다.
   source checkout의 group-writable 경로는 token을 받는 실행 경로로 신뢰하지 않는다.
   installer는 정확한 Git blob 두 개만 읽고 mode 0500/0400과 공개 hash receipt를 남긴다.
   기존 목적지와 symlink를 덮어쓰지 않는다. 부모 디렉터리는 운영자가 소유한 0700이어야 한다.

   ```bash
   # 아래 경로와 commit은 owning Task에서 확정한 운영자 입력이다.
   test -n "$issuer_repository" && test -n "$issuer_commit" && test -n "$operator_tools" || exit 1
   set -o pipefail
   /usr/bin/git -C "$issuer_repository" show \
     "$issuer_commit:infra/03-security/openbao/scripts/install-renderer-issuer.sh" | \
     /bin/sh -s -- "$issuer_repository" "$issuer_commit" "$operator_tools/$issuer_commit" || exit 1
   ```

   승인 SHA는 checkout의 현재 HEAD와 별개로 owning Task에서 검토한 full commit이다.
   installer도 해당 commit blob에서만 읽는다. 쓰기 가능한 checkout의 installer를 직접 실행하지 않는다.

3. 새 발급 전에 Agent를 중지한다. 현재 operator 인증을 통해
   `auth/token/create/renderer-issuer`와 `auth/token/create/renderer-cleanup`에서
   token을 별도로 발급한다. JSON 입력의 `policies`는 각각 정확한 policy 문자열이며,
   `ttl="5m"`, `explicit_max_ttl="5m"`, `renewable=false`, `no_default_policy=true`를
   함께 요구한다. 발급 응답을 출력하지 않고 보호된 stdin/custody로 처리한다.
   root·renderer·application token을 helper 입력으로 사용하지 않는다.

   ```bash
   set +x
   docker stop openbao-agent || exit 1
   read -rsp 'Enter short issuer credential> ' SEC01_ISSUER_TOKEN; printf '\n'
   read -rsp 'Enter short cleanup credential> ' SEC01_CLEANUP_TOKEN; printf '\n'
   printf '%s\n%s\n' "$SEC01_ISSUER_TOKEN" "$SEC01_CLEANUP_TOKEN" | \
     sh "$operator_tools/$issuer_commit/issue-renderer-secret-id.sh" \
       openbao "$agent_volume" \
       openbao/openbao:2.7.1@sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf openbao-agent "$issuance_journal" "$issuer_commit" # <!-- runtime-version-exception: compatibility — helper requires the exact image; docker-compose.yml owns the pin -->
   sec01_issue_result=$?
   unset SEC01_ISSUER_TOKEN SEC01_CLEANUP_TOKEN
   test "$sec01_issue_result" -eq 0 || exit 1
   ```

   `agent_volume`와 `issuance_journal`은 Task에 확정한 실제 대상이다. helper는 이미지의
   amd64 manifest·server·Agent volume binding·entrypoint를 확인한다. API 호출 전에
   secret-free version-derived record를 journal에 atomic/fsync 저장한다.
   Docker socket은 host helper만 사용하며 Agent에 주지 않는다. 전달 helper container는
   network none·pull never·UID100·cap drop·read-only를 유지한다.
4. helper가 Agent를 시작하고 새 `StartedAt`·TLS·unsealed·제한 fetch/render와 KV version
   sentinel을 검증한다. 전달 성공만으로 journal을 없애지 않는다. 같은 nonce·생성 시간의
   accessor 소비/폐기와 부재를 확인한 후만 completion witness를 기록한다.
   전체 작업 budget은 240초이며 token 만료 전 여유를 남긴다. consumer 적용은 별도 증거다.
5. SIGTERM/SIGKILL·reboot 후 같은 journal로 재실행하면 먼저 이전 발급을 정합화하고
   그 실행에서는 새 SecretID를 만들지 않는다. 정확한 단일 accessor만 폐기한다.
   전달 후 시작 전에는 stopped 상태를, 시작 후 기록 전에는 발급 이후의 새 generation과
   기능 readiness를 증명한다. 불명확·복수 결과·시간/nonce 불일치·sealed·권한 거부·journal
   유실은 실패로 유지하고 새 발급을 차단한다. 자동으로 journal을 지우거나 광범위 accessor를
   폐기하지 않는다. 해당 상태는 승인된 관리 신원의 custody/API 대조 복구가 필요하다.

새 발급 journal은 `schema_version: 2`, `issuance_id`, 기존 `nonce`를 함께 보관하며 두
identity 값은 같아야 한다. 실제 accessor metadata도 `issuance_schema: "2"`,
`issuance_id`, `sec01_nonce`를 모두 포함한다. v1 journal과 anchor는 version 필드 없이
기존 형태로 보존한다. 정합화 시 journal과 활성 anchor의 version·identity가
정확히 일치하고, accessor metadata가 해당 journal version에서 유도한 전체 metadata와
정확히 일치해야 한다. completion witness는 중단된 정리의 복구를 허용하는 별도 기록이다.
v1/v2 혼합, alias 불일치, 복수 accessor가 있으면 어느 accessor도 폐기하지 말고 중단한다.
이전 발급을 정합화한 같은 실행에서는 새 SecretID를 발급하지 않는다.

이 프로토콜은 아직 HOME에서 수행하지 않았다. 운영 실패 시 journal·completion witness·
보호된 snapshot과 관리 인증을 보존한다. 재시작을 반복하거나 오래된 sink를 PASS로 처리하지 않는다.

### Prometheus Metrics Credential

이 절차는 승인이 OpenBao policy/token 변경과 Prometheus 재생성을 정확한 대상으로 명시한
경우에만 사용한다.

1. OpenBao가 initialized/unsealed 상태이고, 검토된 `prometheus.hcl`이 `sys/metrics`에
   대한 `read`만 포함하며, 승인된 관리자가 대기 중이고, rollback이 현재 configuration
   commit을 사용함을 확인한다. Prometheus credential로 renderer AppRole, renderer sink
   token, human operator token, root token을 사용하지 않는다.
2. policy를 적용하고 default policy가 없는 새 orphan service token을 발급한다. 유효 시스템
   최댓값 이내의 유한한 TTL을 부여하고, 만료 시각과 accessor를 보호된 custody에 기록하고,
   token 값만 mode `0640`, group `SECRETS_GID`로 `secrets/security/openbao/openbao_token.txt`에
   전달한다(Prometheus는 `group_add`를 통해 `nobody`로 이를 읽는다). 출력하거나 인자로
   전달하지 않는다. 아래 명령의 owner-only 세션 디렉터리만 스테이징으로 허용되며 이후
   삭제한다.
3. 보호된 입력을 통해 새 token이 `sys/metrics`를 읽을 수 있고 관련 없는 secret 경로와
   관리 경로에서는 거부됨을 검증한다. boolean allow/deny 결과와 유효 TTL만 기록하고,
   token이나 원본 응답은 절대 기록하지 않는다.
4. 승인된 재생성 전에 Compose와 Prometheus 구성을 검증한다. Prometheus만 재생성하고
   구성 로드/reload가 성공했음을 확인한 뒤, 원본 target 응답이나 로그를 기록하지 않고
   `openbao` target이 `UP`을 보고할 것을 요구한다.
5. 먼저 교체본을 생성하고 검증한 뒤, consumer용 `0640`/`SECRETS_GID` 파일을 원자적으로 교체하고 Prometheus만
   재생성하고 새 target을 확인하고 accessor로 이전 token을 폐기해 회전시킨다.
   레거시 Vault root token 권한이나 scrape job을 절대 복원하지 않는다.

policy 적용, token validation, 구성 로드, 또는 target health가 실패하면 이전
source/runtime 구성을 계속 사용 가능하게 유지하고, accessor로 새 token을 폐기하고,
승인된 credential 처리 범위 내에서만 local 파일을 제거한다. 검토된 rollback commit에서
Prometheus만 재생성한다. source rollback은 `vault_token`을 다시 도입해서는 안 된다.
전용 credential 경로가 복구될 때까지 OpenBao metrics는 비활성 상태로 둔다.

아래 policy 발급·검증·회전 명령은 [hy-home.k8s integration runbook](../10-platform-and-backup/0096-k8s-integration.md)의
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
install -m 640 -g "$(stat -c %g secrets/security/openbao/openbao_token.txt)" /tmp/bao-k8s/metrics.token secrets/security/.openbao_token.new
mv secrets/security/.openbao_token.new secrets/security/openbao/openbao_token.txt
rm -f /tmp/bao-k8s/metrics.token
docker compose --profile obs up -d --no-deps --force-recreate --wait prometheus
sleep 45   # one scrape interval after the recreate
docker exec prometheus wget -qO- 'http://localhost:9090/api/v1/query?query=up%7Bjob%3D%22openbao%22%7D' | grep -o '"value":\[[^]]*\]'
```

예상 결과: 값 `"1"`. Prometheus는 host port를 게시하지 않으므로 점검은 컨테이너 내부에서
실행한다. custody 파일은 `accessor=`, `expires=`, `issued=`, `policy=` 줄을 담는다.
기존 파일을 컨테이너용으로 준비하고 root 세션에서 그 파일로 폐기한 뒤, 같은 형식으로 새
파일을 작성한다.

```bash
install -m 600 secrets/security/openbao/openbao_metrics_token.custody /tmp/bao-k8s/old.custody
```

다음은 한 줄씩 실행하고 결과를 확인한다. 처음 두 검사는 accessor가 정확히 한 개이고
비어 있지 않음을 요구한다. 폐기 전 조회와 폐기 요청이 모두 성공하지 않으면 즉시
중단한다. 원본 응답은 보호된 세션 디렉터리에만 보관하며 출력하거나 증거에 복사하지 않는다.

```sh
umask 077
test "$(grep -c '^accessor=' /s/k8s/old.custody)" -eq 1
OLD_ACCESSOR=$(sed -n 's/^accessor=//p' /s/k8s/old.custody)
test -n "$OLD_ACCESSOR"
R token lookup -accessor -format=json "$OLD_ACCESSOR" >/s/k8s/old-before.json 2>/s/k8s/old-before.err
R token revoke -accessor "$OLD_ACCESSOR" >/s/k8s/old-revoke.out 2>/s/k8s/old-revoke.err
R token lookup -accessor -format=json "$OLD_ACCESSOR" >/s/k8s/old-after.json 2>/s/k8s/old-after.err
R token lookup -format=json >/s/k8s/caller-control.json 2>/s/k8s/caller-control.err
bao status -format=json >/s/k8s/server-control.json 2>/s/k8s/server-control.err
```

[공식 CLI](https://openbao.org/docs/commands/token/lookup/)의 형식은
`token lookup -accessor`이다. 폐기 전 같은 accessor 조회와 폐기 요청의 성공,
이후 관리 호출자의 유효 권한과 unsealed 서버 상태, 같은 accessor에 대한 서버의
명시적인 invalid-accessor 응답을 모두 확인해야 `old: revoked`로 기록한다.
폐기 후 조회가 성공하면 `STILL VALID`이다. 일반403·DNS·TLS·timeout·sealed·CLI·
응답 해석 실패는 `INDETERMINATE`이며 폐기 증거가 아니다. 이 경우 아래 custody
교체·정리를 실행하지 말고 보호된 응답과 관리 세션을 보존하여 원인을 확인한다.
폐기가 확인된 경우에만 다음 단계로 진행한다.

```bash
umask 077
A=$(sed -n 's/.*"accessor": *"\([^"]*\)".*/\1/p' /tmp/bao-k8s/metrics.custody)
E=$(sed -n 's/.*"expire_time": *"\([^"]*\)".*/\1/p' /tmp/bao-k8s/metrics.custody)
[ -n "$A" ] && [ -n "$E" ] && printf 'accessor=%s\nexpires=%s\nissued=%s\npolicy=prometheus\n' "$A" "$E" "$(date -u +%FT%TZ)" >secrets/security/.openbao_metrics_token.custody.new
test -s secrets/security/.openbao_metrics_token.custody.new && mv secrets/security/.openbao_metrics_token.custody.new secrets/security/openbao/openbao_metrics_token.custody
unset A E; sed -n 's/^expires=//p' secrets/security/openbao/openbao_metrics_token.custody
rm -f /tmp/bao-k8s/old.custody /tmp/bao-k8s/metrics.custody
```

예상 결과: `old: revoked`, 그다음 새 만료일(secret이 아니므로 기록한다). 그런 다음 통합
runbook의 root 폐기 단계로 root 세션을 종료한다. `Started false`는 발급 시도 종료일
뿐 root 폐기 증거가 아니다. root 폐기도 해당 절차의 서버 응답과 양성 대조로
확인한 후, 이 단계에서 만든 보호된 응답 파일과 `OLD_ACCESSOR`를 정리한다.

Agent 재시작 전에 승인된 운영자는 보호된 채널을 통해 새 SecretID를 전달해야 한다.
RoleID/SecretID 파일(0600, 컨테이너 UID 100/GID 1000)을 배치하는 동안 Agent만 중단한
뒤 시작한다. Agent가 소비하기 전에 같은 일회용 SecretID로 test-login하지 않는다.
server를 재시작하면 unseal ceremony가 필요하고 Agent token을 잃거나 만료되어도 새 AppRole
credential이 필요하다. 발급에는 승인된 운영자 신원이 필요하다. 아직 수립되지 않았다면
아래의 별도로 승인된 loopback recovery 절차를 사용한다. 일반 generate-root도 현재 API에서
인증된 권한이 필요하다. quorum key만으로는 그 endpoint를 승인할 수 없다. 자동화 지름길로
활성 영구 root token을 저장하지 않는다.

### Renderer delivery from an existing integration session

기존 RUN-0096 세션을 사용할 때도 위 Renderer SecretID Delivery와 같은 제한 발급자와
response wrapping을 사용한다. raw `-field=secret_id` 전달과 root UID로 volume을 고치는
옛 대안은 현재 경로가 아니다. wrapping helper 하나만 사용하고 중복 발급하지 않는다.
기존 세션·root 폐기·integration receipt는 과거 관찰이며 새 P01 결과가 아니다.

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

### Native TLS, Audit and Recovery Gate

`OPENBAO_PORT`가 내부 listener/API·Agent·Prometheus target·Gatus URL·Traefik backend의
공통 port 입력이다. HCL에 별도 address를 고정하지 않는다. CA/server certificate/key는
공유 `${DEFAULT_CERT_DIR}` 밖의 전용 경로를 사용해 다른 컨테이너에 server key가 노출되지 않게 합니다.
OpenBao 외부 custody에서 `${DEFAULT_SECURITY_DIR}/openbao/tls/{ca.pem,server.pem,server-key.pem}`에
준비한다. 이 경로는 신규 source 계약이며 실제 파일 존재나 발급을 증명하지 않는다.
서버 SAN `DNS:openbao`와 `IP:127.0.0.1`, 유효 기간·chain·key 일치와 UID 100 읽기 권한을 검증한 후만
적용한다. 시작 전 아래 read-only preflight를 실행한다. stdout은 check label과 PASS/FAIL만 출력한다.

```bash
sh infra/03-security/openbao/scripts/check-tls-material.sh "$DEFAULT_SECURITY_DIR/openbao/tls" openbao/openbao:2.7.1@sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf # <!-- runtime-version-exception: compatibility — preflight requires the exact image; docker-compose.yml owns the pin -->
```

명령은 만료·CA chain·정확한 SAN·cert/key 일치와 UID100:GID1000의 읽기를 검증한다.
마지막 읽기 검사는 pull 없는 network-none 임시 컨테이너와 exact-file readonly bind만 사용한다.
TLS 자료는 HOME source 경로에 준비되었고 공개 인증서 검사는 통과했다(TLS_PREPARED / NOT_DEPLOYED, server 재시작 없음). 다만 이 명령 자체를 HOME에서 실행한 기록은 없다. CLI는 `BAO_CACERT`/`BAO_TLS_SERVER_NAME`, Agent는 `VAULT_CACERT`, metrics는
CA/server_name, Traefik은 `openbao-tls@file`로 검증한다. 잘못된 CA/SAN/만료는 차단하며
`skip_verify`를 정상 경로로 사용하지 않는다. 외부 gateway 인증서와 내부 backend 신뢰는
별개다. 최초 key/CA를 그 OpenBao Agent가 발급하는 순환은 금지한다.

현재 candidate 2.7.1에는 config-owned `p01-file` audit backend를 선언한다. 로그는 별도
`openbao-audit` bind에 0600으로 보관하고 stdout으로 보내지 않는다. `log_raw=false`,
`hmac_accessor=true`, `unsafe_allow_api_audit_creation=false`를 유지한다. HMAC은 주로
JSON string을 보호하며 숫자·boolean·일부 metadata까지 모두 비밀화하는 보장은 아니다.
민감 값은 string으로 전달하고 raw auth/audit 로그는 출력하거나 채팅에 전달하지 않는다.

file backend에는 자체 rotation이 없다. 운영자는 실제 audit filesystem·남은 용량과
증가율을 측정해 보존 기간·rotation size·schedule을 정하고 기존 host logrotate에
rename/create(0600, UID 100/GID 1000)와 대상 OpenBao `SIGHUP` reopen을 등록한다.
`copytruncate`로 손실을 감추거나 audit device를 제거하지 않는다. `/` 용량 알림은 실제
mountpoint가 `/`라는 관찰이 있어야 audit 용량 증거로 인정한다. 아직 해당 HOME 관찰과
rotation 등록은 미실행이다. 임시 용량 장애 시험은 실제 host 용량 최적값이 아니다.

현재 한 backend의 쓰기가 실패하면 audited 요청은 실패하고 blocking writer라면
응답이 지연될 수 있다. `/sys/health` 같은 비감사 경로가 200이어도 정상 업무를 뜻하지
않는다. audit 실패·scrape 실패·Agent 기능 실패를 각각 확인하고 공간/권한/backend를
복구한다. 요청 성공만을 위해 audit를 disable하거나 `skip_test`/discard로 바꾸지 않는다.

snapshot은 [기존 정책/절차](../10-platform-and-backup/0021-backup-and-restore.md)를 재사용한다.
token 누락·갱신 실패·빈 snapshot·sealed는 backup unit 실패다. 복구는 선택한
barrier-encrypted snapshot, 원본 unseal shares, 독립 보관된 offsite key와 빈 대상의
identity·용량·network·rollback을 묶어 별도로 검토한다. Git revert는 data 복구가 아니다.
격리 시험의 init/share/snapshot은 합성 자료이며 HOME 독립 custody를 대신하지 않는다.
`OpenBaoAuditFailure`는 실제 격리 시험에서 관찰한 request/response failure counter의 최근 5분 증가를 평가한다. 누적값 자체로 영구 경보하지 않는다.
알림 수신·회복은 HOME에서 별도 검증해야 한다. 모든 audit backend가 막히면 metrics 요청도 실패할 수 있으므로
`up==0` 신호를 함께 사용한다. scrape 실패는 원인을 특정하지 않으며 health 성공도 audit 정상 증거가 아니다.

#### Current candidate and preserved residual

이전 2.6.2의 만료된 미사용 SecretID 수용과 abandoned issuance 정리 결함은 보존된 P01
Task의 역사 증거다. [공식 release notes](https://openbao.org/community/release-notes/2-6-0/#v264)가
보안 수정 범위를 소유한다. SEC01 candidate는 2.7.1이며 Raft·Shamir·TLS·config-owned
file audit를 보존한다. 2.7의 제거된 file **storage** backend와 file **audit** backend를
혼동하지 않는다. Agent와 snapshot CLI는 같은 server image 묶음으로 정렬한다.

격리 합성 시험에서 expired-unused SecretID 거부·잘못된 CA 거부·제한 token role·
snapshot 빈 환경 복원·audit 용량 실패 차단을 확인했다. 이는 실제 HOME custody·cold boot·
이관·복구나 모든 malformed 입력 안전성의 증거가 아니다. 실제 host 적용 전에는 최신
공급자 channel·같은 플랫폼 SBOM/scan·서명·pre-upgrade snapshot·독립 custody·빈 이전
버전 환경 복원과 이후 candidate upgrade를 검증한다. 2.7 데이터에 이전 image를 붙이는
것은 rollback이 아니다. 운영자가 고른 30분 cutover 목표와 60분 maintenance window
안에 restore/unseal/검증까지 가능한지 측정한다. 두 값은 계획 추정치이며 관측한
RTO가 아니다. 목표를 넘거나 복구 자료가 없으면 HOME만 보류한다. P06 확대도 HOME gate 전에는
진행하지 않는다.

HOME 적용 전 source-only rollback은 검토된 revert다. 적용 후에는 TLS·audit 선언과 로그 custody를 유지하는
검토된 override 또는 fix-forward만 사용한다. client도 검증된 endpoint로만 전환하며 HTTP나 audit 제거로 되돌리지 않는다.

P06 확대는 실제 HOME cold boot·custody·복구 gate가 통과할 때까지 보류한다.

#### HOME 적용 입력과 승인 순서

값은 기록하지 않는다. 각 단계는 앞 단계가 끝난 뒤에만 진행하며, 괄호 안 승인이 따로 필요하다.

1. SEC01이 현재 candidate image의 서명·SBOM·CVE 결과를 수용한다(SEC01 담당자).
2. 보존된 attempt 대상과 container의 처리를 정한다(삭제는 명시 승인). attempt 03·04·chown container와 `-03` 대상은 2026-10-13에 owner가 삭제했다. 같은 날 owner 결정으로 빈 기본 restore 대상과 `-04` 대상도 삭제했고, 기존 업그레이드 전 snapshot 파일은 새 snapshot이 생길 때까지 rollback 지점으로 보존한다.
3. snapshot 전용으로 제한한 identity와 token을 발급한다(credential 발급 승인). operator policy는 `sys/policies/acl` 쓰기와 orphan token 발급을 허용하지 않으므로(2026-10-13 HTTP 403) 복구 share ceremony로 만든 임시 root가 필요하다. owner 결정으로 8단계 업그레이드 window의 같은 ceremony에서 발급하며, 그 전까지 일일 backup의 OpenBao snapshot은 recovery gap으로 계속 실패한다.
4. 그 token이 일반 secret을 읽지 못하고 갱신되는지 확인한 뒤, 쓰기를 멈춘 상태에서 새 업그레이드 전 snapshot을 만든다(backup 실행 승인).
5. unseal share·offsite key·CA key의 off-host 독립 보관을 값 없이 확인한다(owner 확인). 2026-10-13 owner 확인 결과 아직 분리 보관이 없으므로 미실행이며, P01은 계속 차단된다.
6. 새 attempt 식별자로 빈 대상에 의미 있는 restore를 하고 canary 읽기와 renderer 재인증을 확인한다(독립 READY 검토 후 사용자 승인). 이전 attempt 04의 도구는 추적되지 않으므로 이 단계에는 추적되거나 새로 검토한 도구가 필요하다.
7. audit 용량을 측정하고 logrotate를 등록한다(sudo가 필요한 host 변경 승인). 현재 HOME server에는 audit mount가 없으므로 8단계 업그레이드 window로 미룬다.
8. maintenance window 안에서 server 업그레이드, 지정 운영자의 수동 unseal, wrapped 재발급을 포함한 Agent 업그레이드를 진행한다(승인된 runtime 변경 의도의 새 검토).
9. HOME cold boot를 한다(별도 승인).
10. 현재 버전 인증과 consumer 읽기를 위한 consumer와 ACL을 고른다(P06 담당자 선택).

Agent staleness와 인증 실패를 알리는 Prometheus 규칙이 아직 없고, 변조된 HMAC의 audit 검증도 미실행이다. `openbao-agent`는 metric을 노출하지 않는다(`agent.hcl`에 telemetry·listener가 없고 Prometheus도 scrape하지 않는다). Docker healthcheck가 token lookup·KV 읽기·렌더 bytes 일치를 확인하므로 staleness·인증 실패는 Docker `unhealthy`로만 드러나고 알림은 없다. 2026-10-13 owner 결정으로 이 gap을 기록해 두고, Agent telemetry·scrape·alert는 IaC 검토를 거치는 별도 Spec에서 추가한다.

### HOME 유지보수 창 계획

2026-10-13 owner 결정으로 남은 HOME 단계를 한 번의 maintenance window로 묶는다. 이
계획은 문서일 뿐 실행 증거가 아니다. 모든 값(share·OTP·token·key)은 숨겨진 prompt나
stdin으로만 다루고, 명령 인자·터미널 기록·채팅에 남기지 않는다. 각 단계의 결과는
SPEC-0204 TSK-0006 Evidence에 값 없이 기록한다.

**전제 조건(위 5단계).** unseal share·offsite key·CA key가 서로 분리된 off-host 보관에
있다는 owner 확인이 값 없이 기록되어야 한다. 확인이 없으면 window를 열지 않는다.

| 순서 | 단계 | 목표 시간 | 승인 |
| --- | --- | --- | --- |
| W0 | 사전 점검 | window 전 | SEC01 담당자, owner |
| W1 | root ceremony | 10분 | owner(share 보유자 2명) |
| W2 | snapshot token 발급과 확인 | 5분 | owner(credential 발급) |
| W3 | 새 업그레이드 전 snapshot | 5분 | owner(backup 실행) |
| W4 | server 업그레이드와 수동 unseal | 10분 | owner(runtime 변경) |
| W5 | Agent 업그레이드와 재발급 | 5분 | owner(runtime 변경) |
| W6 | audit·logrotate | 10분 | owner(sudo host 변경) |
| W7 | 사후 점검과 root 폐기 | 10분 | owner |
| W8 | cold boot | 별도 window | owner(별도 승인) |

W1부터 W5까지가 운영자가 고른 30분 cutover 목표이고, W7까지 60분 window 안에 끝나야
한다. 두 값은 계획 추정치다. 30분을 넘거나 어떤 중단 조건이 생기면 아래 rollback으로
돌아가고 남은 단계는 다음 window로 넘긴다.

**W0 사전 점검.**

```bash
HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh
docker compose exec -T openbao bao status
docker compose --profile security config --images | grep '^openbao/openbao' | sort -u |
  xargs docker image inspect --format '{{.Id}}'   # 없으면 오류로 끝난다
df -h /home
systemctl show hyhome-backup.service -p Result,ExecMainExitTimestamp
```

기대: compose 검증 통과, `Sealed false`, compose가 고정한 candidate image가 local에
있음, 남은 용량 확인, 마지막 backup 결과 확인. SEC01이 candidate image의 서명·SBOM·
CVE 결과를 수용했고(위 1단계) 위 TLS preflight가 PASS여야 한다. 하나라도 아니면 중단한다.
image가 없으면 별도 승인으로 같은 digest만 pull한다.

**W1 root ceremony.** 위 [Human Login and Normal Root Recovery](#human-login-and-normal-root-recovery)의
보호된 인증 API 절차를 사용한다. Share·OTP·token은 검토된 클라이언트의 숨겨진
입력 또는 보호된 stdin/custody로만 다루고 argv·터미널·일반 로그로 전달하지 않는다.

현재 [CLI 계약](https://openbao.org/docs/commands/operator/generate-root/)의 OTP
option은 문자열 인자이며 encoded token의 stdin 입력과 별개다. Container 안 shell이
실행 중인 server나 다른 process·runtime metadata에서 인자를 숨긴다고 가정하지 않는다.
이전 window의 OTP 인자 명령은 실행 절차에서 제거했다.

W1은 보호된 [인증 API](https://openbao.org/docs/api/system/generate-root-token/)를
사용하는 클라이언트의 입력·출력·디코딩·중단 처리가 검토되고, 정확한 대상·권한·
복구와 독립 custody가 확인되기 전까지 **BLOCKED / NOT_RUN**이다. 이 문서 수정은
클라이언트 구현, root 발급이나 승인 증거가 아니다. API 응답의 OTP/nonce와 encoded
응답은 보호된 custody에 먼저 보존하고, 디코딩한 root를 승인된 다음 단계로만 전달한다.

기대: 검토된 절차로 새 root token 하나가 생성되고 정상 관리 인증을 보존한다.
중단: share 불일치, 진행 정체, 입력·출력 보호 실패, 디코딩 실패. 미완료 attempt는
같은 보호된 클라이언트의 승인된 취소 경로로 정리하고 실제 잔여 상태를 확인한다.
값은 기록하지 않으며, 취소가 수행되지 않았다면 성공으로 보고하지 않는다.

**W2 snapshot token.** [RUN-0021](../10-platform-and-backup/0021-backup-and-restore.md)의
OpenBao token 블록을 별도 터미널에서 실행하고, `OpenBao admin token:` prompt에 임시
root를 입력한다. 기대: `snapshot token ready`. 그 token으로 일반 secret 경로 읽기가
거부되고 `bao token renew`가 성공하는지 값 없이 확인한다. 중단: 403, 빈 파일, 확인 실패.
실패하면 `$out.new`를 지우고 token을 폐기한다.

**W3 새 업그레이드 전 snapshot.** OpenBao에는 쓰기 정지 기능이 없으므로 쓰기 주체를
멈춘다. Agent를 먼저 멈추고(`docker compose stop openbao-agent`), 승인된 관리 작업이
없음을 확인한 뒤 새 token으로 snapshot을 받는다.

```bash
docker compose exec openbao bao operator raft snapshot save /tmp/pre-upgrade.snap
```

container 안 임시 파일은 RUN-0021 경로로 옮기고 sha256과 크기를 기록한 뒤 container에서
지운다. 기대: 0이 아닌 크기와 checksum. 중단: 빈 파일, sealed, timeout. 이 snapshot이
생기면 보존해 둔 이전 업그레이드 전 snapshot은 다음 정리 결정의 대상이 된다.

**W4 server 업그레이드와 수동 unseal.**

```bash
docker compose --profile security up -d --no-deps --no-build --pull never openbao
docker compose exec openbao bao operator unseal   # 숨겨진 prompt, 지정 운영자가 share 입력
docker compose exec openbao bao operator unseal   # 두 번째 share
docker compose exec -T openbao bao status
```

기대: 새 image로 재생성, Raft mount identity 불변, threshold 뒤 `Sealed false`.
중단: mount identity 변경, unseal 실패, cluster ID 변경, audit backend 실패.
rollback: 새 버전 데이터에 이전 image를 붙이지 않는다(in-place Raft downgrade 금지).
업그레이드가 실패하면 W3 snapshot을 이전 버전 image의 빈 대상에 복원하는 검토된 절차로
간다(위 Rollback or Recovery). 이 경우 HOME은 보류하고 @buenhyden에게 반환한다.

**W5 Agent 업그레이드와 재발급.** server가 unsealed이고 health가 통과한 뒤에만
`docker compose --profile security up -d --no-deps --no-build --pull never openbao-agent`를
실행하고, 위 [Renderer SecretID Delivery](#renderer-secretid-delivery)로 wrapped
SecretID를 다시 전달한다. 기대: Agent `healthy`, 렌더 bytes와 version 일치. 중단:
재인증 실패, health 실패. Agent는 server보다 앞서 rollback하지 않는다.

**W6 audit와 logrotate.** 새 server에 `openbao-audit` mount와 `audit.json`(0600, UID
100)이 생겼는지 확인하고, 용량과 증가율을 잰 뒤 위 Native TLS, Audit and Recovery Gate의
규칙대로 host logrotate(rename/create 0600, UID 100/GID 1000, `SIGHUP` reopen)를
sudo로 등록한다. `copytruncate`는 쓰지 않는다. 기대: rotation 시험 뒤 audit 쓰기 지속.
중단: audit 쓰기 실패. 이때 audit device를 끄지 않고 공간과 권한을 복구한다.

**W7 사후 점검과 root 폐기.** renderer 재인증, consumer 읽기(Keycloak·Grafana 렌더 결과
일치), `OpenBaoSealed` 등 기존 경보가 조용한지, `up{job="openbao"}`, 다음 backup 단위의
OpenBao snapshot 성공을 확인한다. 임시 root는 W2·W4에서만 필요하다. W7 끝에서
`bao token revoke -self`로 폐기하고 같은 token의 lookup이 거부되는지, OIDC 로그인이
여전히 되는지 확인한다. 더 이른 단계가 실패해 window를 접을 때도 root를 먼저 폐기한다.

**W8 cold boot.** 별도 승인과 별도 window에서 host를 재시작하고, 수동 unseal, Agent
재인증, 위 W7 점검을 반복한다. cold start 시뮬레이션은 실제 재부팅 증거가 아니다.

**window 뒤에 남는 것.**

- 새 attempt로 빈 대상에 의미 있는 restore와 canary 읽기(위 6단계). `.agent-work/`가
  삭제되므로 추적되거나 새로 검토한 도구가 필요하다.
- consumer와 ACL 선택(위 10단계, P06).
- Agent telemetry·scrape·alert를 추가하는 별도 Spec.

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

### P02 Public Catalog Checks

이 절차는 검토된 checkout의 공개 metadata와 staging view만 확인한다. OpenBao API,
private metadata·환경·credential 파일, HOME 서비스에 접속하지 않는다. 저장소 루트의
물리적 절대 경로에서 검증 의존성이 설치된 Python으로 실행하며, symlink 경로나 다른
checkout을 `--root`로 지정하지 않는다. 먼저 읽기 전용 검사를 실행한다.

```bash
rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check
```

네 입력은 catalog, schema, `secrets/SENSITIVE_ENV_VARS.md.example`,
`infra/secret-file-support.json`이다. 형식·분류·원본 표 일치가 유효하면 JSON의
`result`는 `P02_METADATA_VALID`, `entries`와 `aliases`는 실제 입력의 개수이며 exit 0이다.
`P02_METADATA_BLOCKED`와 exit 2는 형식·원본·경로·의존성 등 검사 실패이므로 중단한다.
이 결과는 credential 값 또는 권리·운영 상태를 검사한 결과가 아니다.

staging이 필요한 경우에만 operator-owned `.agent-work`와 그 안의 regular, single-link,
동일 소유자 `README.md`를 먼저 확인한다. 기존 타 작업자의 경로를 교체하거나 symlink,
공유 inode, 다른 소유자의 파일 권한을 고쳐서 통과시키지 않는다. 새 경로를 준비할 때는
소유자가 확인된 전용 checkout에서만 만들고 그 목적을 README에 기록한다.

```bash
rtk python3 scripts/operations/secret-catalog.py --root "$PWD" render
rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check-views
```

`render`는 `.agent-work/p02-views`에 정확히 네 공개 출력 파일을 만들며
`STAGING_RENDERED`와 파일명 목록, exit 0을 반환한다. `check-views`는 네 입력에서 유도한
bytes와 모두 일치할 때만 `P02_VIEWS_MATCH`, exit 0이다. 불일치는 `P02_VIEW_DRIFT`,
exit 2다. 경로·소유권 등 안전 검사 실패는 `P02_METADATA_BLOCKED`, exit 2다.
파일별 교체는 전체 네 파일의 원자적 transaction을 뜻하지 않는다. 실패 후 부분 결과를
소비하지 말고 원인과 공개 입력을 검토한 뒤 동일 전용 staging을 다시 생성·검사한다.
private 파일 삭제나 runtime rollback을 이 절차의 정리로 수행하지 않는다.

아래 두 거절 probe는 각각 독립적으로 실행한다. `check-generation`은 생성 적격성만
검사하며 secret을 발급하지 않는다. 두 명령 모두 `P02_GENERATION_BLOCKED`, exit 2가
정상 예상 결과이며, 일반 shell의 실패 코드와 구별해 기록한다.

```bash
rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check-generation COMM-002
rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check-generation COMM-003
```

거절 대신 성공하거나 예상 출력과 다르면 중단하고 P02 catalog 담당자와 검토한다.
alias COMM-003은 실제 폐기 완료가 아니며 별도 credential/KV 대상을 만들 수 없다.
다른 crypto/bootstrap/recovery/LAB/unknown/migrated/retired 항목과 observed/consumed 항목도
guard가 거부해야 한다. 공개 staging만으로 실제 발급·수집·이관·delivery·reload·rotation·
복구를 수용하지 않는다. ACL/delivery mapping은 `BLOCKED_P01`, 실제 pilot은 대상 ID·KV
path·P01 인증/복구·P03 신원·P04 DEV/S3 증거가 있어야 한다. 현재 HOME/P06 hold를 유지한다.

## Rollback and Escalation

### Rollback or Recovery

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

- [운영 인덱스](../../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
