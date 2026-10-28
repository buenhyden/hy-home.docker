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

승인이 OpenBao policy/token 변경과 Prometheus 재생성을 정확한 대상으로 명시해야 한다. root는 [RUN-0105](0105-openbao-maintenance-window.md) W1 ceremony가 custody에 남긴 임시 root를 쓰고 W7 `revoke-root`로 폐기한다. operator policy는 `prometheus` policy를 가진 token을 발급할 수 없다.

## Procedure

### Prometheus Metrics Credential

이 절차는 승인이 OpenBao policy/token 변경과 Prometheus 재생성을 정확한 대상으로 명시한
경우에만 사용한다.

#### Rotation Rules

회전은 다음 규칙을 따르며, 아래 `metrics-rotate`가 이 규칙을 그대로 실행한다.

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
   전달하지 않는다. `metrics-rotate`의 owner 전용 tmpfs 작업 디렉터리만 스테이징으로 허용되며
   끝나면 지운다.
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
source/runtime 구성을 계속 사용 가능하게 유지하고, 새 token을 폐기하고,
승인된 credential 처리 범위 내에서만 local 파일을 제거한다. 검토된 rollback commit에서
Prometheus만 재생성한다. source rollback은 `vault_token`을 다시 도입해서는 안 된다.
전용 credential 경로가 복구될 때까지 OpenBao metrics는 비활성 상태로 둔다.

#### Rotation Steps

`owner-window.sh metrics-rotate`가 위 규칙의 발급·교체·이전 token 처리를 한 번에 실행한다. root는
[RUN-0105](0105-openbao-maintenance-window.md) W1 source bootstrap과 W1 ceremony로 얻고, W7
`revoke-root`로 폐기한다. throwaway client와 수동 generate-root는 필요 없다.
`bash --noprofile --norc` 셸 하나에서 저장소 루트로 이동해 다음 순서로 실행한다.
`p01_run`은 [RUN-0085 Reviewed Script Runner](0085-openbao.md#reviewed-script-runner)의 함수이고,
`P01_APPROVED_COMMIT`은 이 script를 담은 검토된 전체 commit이다.

```bash
bash infra/03-security/openbao/scripts/owner-window.sh preflight
p01_run "$P01_APPROVED_COMMIT" infra/03-security/openbao/scripts/p01-bootstrap.sh "$P01_APPROVED_COMMIT"
. "$XDG_RUNTIME_DIR/p01-window.vars"
bash "$P01_SCRIPT_DIR/owner-window.sh" token w1        # OIDC 로그인 후 Copy token
bash "$P01_SCRIPT_DIR/owner-window.sh" check-token w1  # policy·TTL과 attempt started:false
bash "$P01_SCRIPT_DIR/owner-window.sh" w1              # unseal share 2개 숨김 입력, root는 custody로
bash "$P01_SCRIPT_DIR/owner-window.sh" root-sweep      # 이전 root 정리(매 window): revoked=<n>, remaining=0
bash "$P01_SCRIPT_DIR/owner-window.sh" metrics-rotate
bash "$P01_SCRIPT_DIR/owner-window.sh" metrics-revoke  # metrics-rotate가 확인하지 못한 것이 있을 때만
bash "$P01_SCRIPT_DIR/owner-window.sh" token w7        # 새 OIDC 로그인
bash "$P01_SCRIPT_DIR/owner-window.sh" revoke-root
bash "$P01_SCRIPT_DIR/owner-window.sh" cleanup
```

`root-sweep`은 RUN-0105의 이전 root 정리 규칙이다. `metrics-rotate`는
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

실패 시 동작은 [Rotation Steps](#rotation-steps)의 실패 목록을 따른다. 이전 token이 유효하면 이전 파일과 Prometheus를 되돌리고 새 token을 폐기한다. 이전 token이 이미 만료됐으면 검증된 새 token을 배포한 채 custody에 기록하고 Prometheus를 점검한다. 확인하지 못한 폐기는 W7 `revoke-root` 전에 `metrics-revoke`로 다시 확인한다. source rollback은 `vault_token`을 다시 도입하지 않는다.

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
