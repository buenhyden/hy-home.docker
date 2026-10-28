---
title: "OpenBao Prometheus Metrics Credential"
version: "0.4.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-28"
layer: "operations"
artifact_id: "RUN-0104"
parent_ids:
- "POL-0085"
created: "2026-10-28"
---

# OpenBao Prometheus Metrics Credential

## Overview

이 런북은 Prometheus가 OpenBao `sys/metrics`를 읽는 전용 token의 발급·검증·회전·폐기를 다룬다. 공통 운영은 [RUN-0085](0085-openbao.md)가 소유한다.

## Trigger

metrics token을 처음 발급하거나, 만료 전에 회전하거나, 이미 만료된 token을 교체할 때 사용한다. 만료된 경우는 아래 `만료된 이전 token` 분기를 따른다.

## Prerequisites

승인이 OpenBao policy/token 변경과 Prometheus 재생성을 정확한 대상으로 명시해야 한다. 명령은 [hy-home.k8s integration runbook](../10-platform-and-backup/0096-k8s-integration.md)의 throwaway client와 그 임시 root 세션 안에서 실행한다.

## Procedure

### Prometheus Metrics Credential

이 절차는 승인이 OpenBao policy/token 변경과 Prometheus 재생성을 정확한 대상으로 명시한
경우에만 사용한다.

#### Scripted Rotation

기본 경로다. `owner-window.sh metrics-rotate`가 아래 수동 1–5단계와 만료 분기를
한 번에 실행한다. root는 [RUN-0105](0105-openbao-maintenance-window.md) W1 source bootstrap과
W1 ceremony로 얻고, W7 `revoke-root`로 폐기한다. 이 경로에서는 throwaway client와 수동
generate-root가 필요 없다. 저장소 루트에서 다음 순서로 실행한다.

```bash
# 0. RUN-0105의 W1 source bootstrap 블록을 승인된 commit(P01_APPROVED_COMMIT)으로 실행한다.
bash "$P01_SCRIPT_DIR/owner-window.sh" token w1        # OIDC 로그인 후 Copy token
bash "$P01_SCRIPT_DIR/owner-window.sh" check-token w1  # policy·TTL과 attempt started:false
bash "$P01_SCRIPT_DIR/owner-window.sh" w1              # unseal share 2개 숨김 입력, root는 custody로
bash "$P01_SCRIPT_DIR/owner-window.sh" metrics-rotate
bash "$P01_SCRIPT_DIR/owner-window.sh" metrics-revoke  # metrics-rotate가 확인하지 못한 것이 있을 때만
bash "$P01_SCRIPT_DIR/owner-window.sh" token w7        # 새 OIDC 로그인
bash "$P01_SCRIPT_DIR/owner-window.sh" revoke-root
bash "$P01_SCRIPT_DIR/owner-window.sh" cleanup
```

W1 뒤에는 RUN-0105 W7 절의 이전 root 정리 블록도 매 window 실행한다. `metrics-rotate`는
다음을 순서대로 한다. token과 accessor는 stdin으로만 넘기며 출력하거나 인자로 넘기지 않는다.

1. bootstrap 사본의 `prometheus.hcl`을 쓰고 `token/` mount 최대 TTL을 `8760h`로 tune한다.
2. 1년 token을 발급하고 정책·orphan·갱신 불가·명시 최댓값을 확인한 뒤 `sys/metrics` 허용과
   `policy list` 거부를 확인한다.
3. 이전 token을 판정한다. 기준은 배포된 파일이다.
   - 배포된 token 조회가 성공하고 그 accessor와 정책이 custody와 같으면 `valid`다. 다르면
     custody가 오래된 것이므로 멈춘다.
   - 배포된 token이 `bad token`이고 custody accessor가 `invalid accessor`이며, root 조회와
     unsealed 상태(양성 대조)가 확인되면 `expired`다.
   - 그 밖은 `INDETERMINATE`로 멈춘다.
4. 배포 파일을 mode `0640`과 기존 group으로 교체하고 Prometheus만 재생성한다. 재생성 시각
   이후에 scrape한 `up{job="openbao"} == 1` 표본이 나올 때까지 최대 2분 기다린다. 표본 시각은
   `timestamp()`로 확인하므로 재시작 전 WAL에서 되살아난 표본은 통과하지 못한다.
5. custody를 새 accessor·만료일로 교체한다.
6. `valid`였으면 accessor로 폐기하고, 조회가 `invalid accessor`이며 양성 대조가 통과해야
   `old: revoked`로 출력한다. 작업 파일을 지운다.

기대 출력은 `metrics: allowed`, `policy list: denied`, `old token: valid|expired`,
`target: openbao up`, `new: expires <날짜>`, `old: revoked` 또는 `old: expired (<날짜>)`이다.

실패 시 동작은 다음과 같다. 폐기 확인 기준은 새 token은 값 조회의 `bad token`, 이전 token은
accessor 조회의 `invalid accessor`와 양성 대조이다.

- **교체 전 실패.** 새 token을 값으로 폐기하고 멈춘다.
- **target이 올라오지 않음, 이전 token 만료.** 만료된 token으로 되돌려도 소용없으므로 검증된 새
  token을 배포한 채 custody에 기록하고 exit 1로 멈춘다. Prometheus를 점검한다.
- **target이 올라오지 않음, 이전 token 유효.** 이전 파일과 Prometheus를 되돌리고 새 token을
  폐기한다. Prometheus만 다시 올라오지 않으면 `restored file; Prometheus not up`을 출력한다.
  파일 되돌리기가 실패하면 `RESTORE FAILED`를 출력하고, 배포된 새 token을 custody에 기록하며,
  아직 유효한 이전 token을 폐기 대상으로 남긴다.
- **이전 token 폐기를 확인하지 못함.** custody는 이미 새 token이다. `NOT confirmed revoked`로
  멈춘다.

확인하지 못한 폐기나 custody 쓰기가 있으면 작업 디렉터리 `$XDG_RUNTIME_DIR/p01-metrics.*`에
`new.unrevoked`, `old.unrevoked` 또는 `custody.unwritten` 표시가 남고 `cleanup`이 지우기를
거부한다. 이 token을 폐기할 수 있는 것은 root뿐이므로 W7 `revoke-root` **전에**
`metrics-revoke`로 같은 확인을 다시 실행한다. 해결되면 작업 디렉터리를 지운다. root를 이미
폐기했다면 다음 window의 W1 root로 `metrics-revoke`를 실행하고, 그 전에는
`cleanup --discard-metrics`로 지우지 않는다. 변경은 policy(같은 내용), tune, 새 token뿐이며 accessor
폐기와 tune 원복으로 되돌릴 수 있으므로 Raft snapshot은 만들지 않는다.

#### Manual Procedure

아래 수동 절차는 스크립트를 쓸 수 없을 때의 기준이다. 스크립트는 같은 판정과 양성 대조를 하고, 이전 token을 accessor뿐 아니라 배포된 파일로도 확인한다.

1. OpenBao가 initialized/unsealed 상태이고, 검토된 `prometheus.hcl`이 `sys/metrics`에
   대한 `read`만 포함하며, 승인된 관리자가 대기 중이고, rollback이 현재 configuration
   commit을 사용함을 확인한다. Prometheus credential로 renderer AppRole, renderer sink
   token, human operator token, root token을 사용하지 않는다.
2. policy를 적용하고 default policy가 없는 새 orphan service token을 발급한다. TTL은
   1년(`8760h`)이다(2026-10-28 owner 결정. 이전 `720h`는 경고 없이 만료되었다). 기본
   token mount 최댓값(768h)을 넘으므로 같은 root 세션에서 `token/` mount의 최대 TTL을 먼저
   `8760h`로 tune한다. 이 token은 `sys/metrics` read만 가진다. 만료 30일 전부터
   `owner-window.sh status`가 경고한다. 만료가 없는 일반 service token은 만들 수 없다.
   TTL을 지정하지 않으면 mount 기본 TTL을 받고, period token도 갱신하지 않으면 만료된다.
   tune은 최댓값만 바꾸며 TTL을 지정하지 않은 다른 token은 계속 기본 TTL을 받는다. 다만 tune은
   영구적이다. `auth/token/create*`를 쓸 수 있는 호출자는 명시 TTL로 최대 1년짜리 token을 받을
   수 있고, 명시 최댓값이 없는 갱신 가능 token은 1년까지 갱신된다. 이 잔여 위험은 owning
   Task에 기록한다. 새 token은 `-explicit-max-ttl`과 `-renewable=false`로 스스로 묶는다. 발급한 뒤 만료 시각과
   accessor를 보호된 custody에 기록하고,
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

#### Minimal Client

아래 policy 발급·검증·회전 명령은 [hy-home.k8s integration runbook](../10-platform-and-backup/0096-k8s-integration.md)의
throwaway 클라이언트(5.2, `/s/k8s`는 host의 owner-only `/tmp/bao-k8s`)에서, 그
임시 root 세션(5.4, `R`이 명령마다 root를 전달) 안에서 실행한다. operator policy는
`prometheus` policy를 가진 token을 발급할 수 없다.

이 runbook만 수행할 때는 RUN-0096의 throwaway client 대신 아래 최소 권한 client를 쓴다.
RUN-0096 명령은 Valkey 비밀번호, Prometheus API 비밀번호와 `.env`의 사용자 이름도 mount하지만,
metrics 회전에는 CA, policy 디렉터리와 owner 전용 작업 디렉터리만 필요하다. RUN-0096의
snapshot, 임시 root, root 폐기 단계는 그대로 따른다.

```bash
K8S_WORK=/tmp/bao-k8s; install -d -m 0700 "$K8S_WORK" && [ -O "$K8S_WORK" ] && [ "$(stat -c %a "$K8S_WORK")" = 700 ] || { echo STOP; exit 1; }
IMG=$(docker compose config --images openbao)
docker run --rm -it --network host --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -e BAO_ADDR=https://openbao.hy.home.arpa -e BAO_CACERT=/ca.pem \
  -v "$PWD/secrets/certs/rootCA.pem:/ca.pem:ro" \
  -v "$PWD/infra/03-security/openbao/config/policies:/policies:ro" \
  -v "$K8S_WORK:/s/k8s" --entrypoint sh "$IMG"
```

#### Issue and Verify the New Token

```sh
R policy write prometheus /policies/prometheus.hcl
R auth tune -max-lease-ttl=8760h token/
R token create -orphan -no-default-policy -policy=prometheus -ttl=8760h -explicit-max-ttl=8760h -renewable=false -field=token >/s/k8s/metrics.token
R write -format=json auth/token/lookup token=@/s/k8s/metrics.token | grep -E '"(accessor|expire_time)"' >/s/k8s/metrics.custody
grep -c . /s/k8s/metrics.custody
BAO_TOKEN="$(cat /s/k8s/metrics.token)" bao read sys/metrics >/dev/null 2>&1 && echo "metrics: allowed" || echo "metrics: DENIED"
BAO_TOKEN="$(cat /s/k8s/metrics.token)" bao policy list >/dev/null 2>&1 && echo "policy list: LEAK" || echo "policy list: denied"
```

예상 결과: `2`(custody 줄 수, 개수만 세고 절대 표시하지 않음), `metrics: allowed`,
`policy list: denied`. token은 자기 자신을 lookup할 수 없다. 유일한 policy가
`sys/metrics`이므로 root로 lookup한다. root 세션은 열어 둔다. host에서 같은
mode와 group으로 파일을 교체하고, Prometheus만 재생성하고 target을 기다린다.

#### Swap the Deployed File

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

#### Revoke a Valid Old Token

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

#### Expired Old Token

custody의 `expires=`가 이미 지났다면 위 폐기 요청을 보내지 않는다.
폐기 전 조회가 실패하는 것이 정상이므로, 위 순서대로 하면 첫 조회에서 중단되고 custody가
교체되지 않는다. 만료 여부는 custody만 믿지 않고 실제 배포된 token으로도 확인한다. custody가
오래되었으면 accessor는 무효여도 배포된 token은 유효할 수 있기 때문이다. 따라서 위 파일 교체
**전에** host에서 배포된 이전 token을 세션 디렉터리에 복사해 둔다.

```bash
install -m 600 secrets/security/openbao/openbao_token.txt /tmp/bao-k8s/old.token
```

파일 교체 뒤 같은 root 세션에서 다음만 실행한다. 각 검사는 결과를 출력하며 `STOP`이 하나라도
나오면 중단한다.

```sh
umask 077
[ "$(grep -c '^accessor=' /s/k8s/old.custody)" -eq 1 ] && echo "accessor: one" || echo STOP
OLD_ACCESSOR=$(sed -n 's/^accessor=//p' /s/k8s/old.custody)
[ -n "$OLD_ACCESSOR" ] && echo "accessor: set" || echo STOP
R token lookup -accessor -format=json "$OLD_ACCESSOR" >/s/k8s/old-expired.json 2>/s/k8s/old-expired.err; echo "accessor lookup rc=$?"
grep -c 'invalid accessor' /s/k8s/old-expired.err
R write -format=json auth/token/lookup token=@/s/k8s/old.token >/s/k8s/old-token.json 2>/s/k8s/old-token.err; echo "token lookup rc=$?"
grep -c 'bad token' /s/k8s/old-token.err
R token lookup -format=json >/s/k8s/caller-control.json 2>/s/k8s/caller-control.err; echo "caller rc=$?"
bao status -format=json >/s/k8s/server-control.json 2>/s/k8s/server-control.err; echo "status rc=$?"
```

다음 조건이 모두 맞을 때만 `old: expired (<custody expires 값>)`로 기록하고, 폐기 없이 아래
custody 교체로 넘어간 뒤 `/s/k8s/old.token`을 지운다.

- `accessor: one`과 `accessor: set`이 출력되고 `STOP`이 없다.
- accessor 조회가 0이 아닌 코드로 끝나고, 오류에 `invalid accessor`가 정확히 한 번 나온다.
- 배포된 token 조회가 0이 아닌 코드로 끝나고, 오류에 `bad token`이 정확히 한 번 나온다.
- 관리 호출자 조회와 server 상태 조회가 0으로 끝난다.

어느 조회든 성공하면 token이 아직 유효하므로 위 폐기 순서를 따른다. 배포된 token이 유효하고
accessor만 다르면 custody가 오래된 것이므로 중단하고 원인을 확인한다. 그 밖의 결과(403, DNS,
TLS, timeout, sealed, 파싱 실패)는 `INDETERMINATE`이며 위와 같이 중단한다.

#### Write the New Custody

```bash
umask 077
A=$(sed -n 's/.*"accessor": *"\([^"]*\)".*/\1/p' /tmp/bao-k8s/metrics.custody)
E=$(sed -n 's/.*"expire_time": *"\([^"]*\)".*/\1/p' /tmp/bao-k8s/metrics.custody)
[ -n "$A" ] && [ -n "$E" ] && printf 'accessor=%s\nexpires=%s\nissued=%s\npolicy=prometheus\n' "$A" "$E" "$(date -u +%FT%TZ)" >secrets/security/.openbao_metrics_token.custody.new
test -s secrets/security/.openbao_metrics_token.custody.new && mv secrets/security/.openbao_metrics_token.custody.new secrets/security/openbao/openbao_metrics_token.custody
unset A E; sed -n 's/^expires=//p' secrets/security/openbao/openbao_metrics_token.custody
rm -f /tmp/bao-k8s/old.custody /tmp/bao-k8s/metrics.custody
```

예상 결과: `old: revoked` 또는 `old: expired (<날짜>)`, 그다음 새 만료일(secret이 아니므로 기록한다). 그런 다음 통합
runbook의 root 폐기 단계로 root 세션을 종료한다. `Started false`는 발급 시도 종료일
뿐 root 폐기 증거가 아니다. root 폐기도 해당 절차의 서버 응답과 양성 대조로
확인한 후, 이 단계에서 만든 보호된 응답 파일과 `OLD_ACCESSOR`를 정리한다.

#### Agent and Root Boundary

Agent 재시작 전에 승인된 운영자는 보호된 채널을 통해 새 SecretID를 전달해야 한다([RUN-0103](0103-openbao-renderer-delivery.md#renderer-secretid-delivery)).
RoleID/SecretID 파일(0600, 컨테이너 UID 100/GID 1000)을 배치하는 동안 Agent만 중단한
뒤 시작한다. Agent가 소비하기 전에 같은 일회용 SecretID로 test-login하지 않는다.
server를 재시작하면 unseal ceremony가 필요하고 Agent token을 잃거나 만료되어도 새 AppRole
credential이 필요하다. 발급에는 승인된 운영자 신원이 필요하다. 아직 수립되지 않았다면
[RUN-0085 break-glass](0085-openbao.md#no-administrative-identity-explicit-break-glass-recovery)의 별도로 승인된 loopback recovery 절차를 사용한다. 일반 generate-root도 현재 API에서
인증된 권한이 필요하다. quorum key만으로는 그 endpoint를 승인할 수 없다. 자동화 지름길로
활성 영구 root token을 저장하지 않는다.

## Verification

`metrics: allowed`, `policy list: denied`, `up{job="openbao"}` 값 1, 이전 token의 `old: revoked` 또는 `old: expired (<날짜>)`와 새 만료일을 값 없이 Task에 기록한다.

## Failure and Recovery

### Rollback or Recovery

policy 적용, token 검증, 구성 로드, target health가 실패하면 이전 구성을 유지하고 새 token을 accessor로 폐기한다. source rollback은 `vault_token`을 다시 도입하지 않는다.

### Escalation

credential, 파괴적 스토리지 변경, remote 변경, 또는 backup 부재로 안전한 진행이 불가능하면
중단하고 @buenhyden에게 연락한다.

## Related Documents

### Traceability

- 공통 OpenBao 운영: [RUN-0085](0085-openbao.md)
- [Implementation](../../../../infra/03-security/openbao/docker-compose.yml)과 [version projection](../../../../infra/tech-stack.versions.json)이 런타임 고정 버전을 소유한다.
- [Guide](../../guides/04-security-and-secrets/0085-openbao.md), [Policy](../../policies/04-security-and-secrets/0085-openbao.md)
- 관장 architecture: [AD-0003](../../../02.architecture/descriptions/0003-security-architecture.md)

- [운영 인덱스](../../README.md)
