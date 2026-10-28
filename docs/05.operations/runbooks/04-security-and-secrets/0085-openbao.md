---
title: "OpenBao Runbook"
version: "0.12.50"
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

이 런북은 OpenBao(`openbao`, `openbao-agent`)의 상태 점검, 승인된 대상 기동·중지, initial bootstrap, Renderer SecretID 전달, 복구를 다룬다. OpenBao는 재시작 뒤 owner가 직접 하는 수동 Shamir unseal이 필요하다. 이 문서의 어떤 단계도 unseal share를 대신 입력하거나 자동화하지 않는다.

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

이 HOME은 1인 관리자 결정(SPEC-0242)으로 share를 host에 두며 아래 [1인 관리자 custody 절차](#1인-관리자-custody-절차)를 따른다. 기존2026-09-22 custody 결정과 단일 파일 위험·미기록 종료 조건은
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
window의 W1c가 root로 먼저 적용한다. HOME 적용 여부는 별도이며 source를 배포 증거로 쓰지 않는다.
cleanup의 자원 권한은 해당 renderer accessor 목록·조회·폐기뿐이다. 두 token의
`lookup-self`는 정확한 policy·TTL·비갱신 신원을 검사하며 다른 KV나 AppRole을 열지 않는다.

1. TLS·unseal·두 제한 KV/version·정확한 Agent named volume과 RoleID를 준비한다.
   기존 Agent 자동 재시작이나 sink 존재를 준비 완료로 판단하지 않는다. 운영자가 지정한
   journal 디렉터리는 Agent data/out volume 밖에 영속 보관하고 owner mode 0700을 요구한다.
   journal과 completion anchor를 따로 삭제·초기화하지 않는다. 값·token·accessor는 기록하지 않는다.
2. 검토한 전체 commit SHA로 host helper를 operator-private 디렉터리에 설치한다.
   source checkout의 group-writable 경로는 token을 받는 실행 경로로 신뢰하지 않는다.
   installer는 wrapper·Python helper·request shell의 Git blob 세 개만 읽고 mode 0500/0400과 공개 hash receipt를 남긴다.
   기존 목적지와 symlink를 덮어쓰지 않는다. 부모 디렉터리는 운영자가 소유한 0700이어야 한다.

   ```bash
   # 아래 경로와 commit은 owning Task에서 확정한 운영자 입력이다.
   unset LD_PRELOAD LD_LIBRARY_PATH PYTHONHOME PYTHONPATH
   test -n "$issuer_repository" && test -n "$issuer_commit" && test -n "$operator_tools" || exit 1
   /usr/bin/env -i PATH=/usr/bin:/bin /usr/bin/python3 -I -S - \
     "$issuer_repository" "$issuer_commit" "$operator_tools/$issuer_commit" <<'P01_ISSUER_BOOTSTRAP'
   import hashlib, os, re, stat, subprocess, sys
   from pathlib import Path

   def bootstrap():
       repository, revision, target = sys.argv[1:]
       repo = Path(repository)
       git = repo / ".git"
       def binding():
           if str(repo) != "/home/hyunyoun/data/hy-home.docker" or repo.resolve() != repo or git.is_symlink():
               raise ValueError()
           root_info, git_info = repo.stat(), git.stat()
           if ((root_info.st_dev, root_info.st_ino, root_info.st_uid) != (64512, 4338469, 1000)
                   or (git_info.st_dev, git_info.st_ino, git_info.st_uid) != (64512, 4338470, 1000)
                   or not stat.S_ISDIR(root_info.st_mode) or not stat.S_ISDIR(git_info.st_mode)):
               raise ValueError()
       binding()
       if re.fullmatch(r"[a-f0-9]{40}", revision) is None:
           raise ValueError()
       environment = {"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1",
                      "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_NO_REPLACE_OBJECTS": "1"}
       def read(*arguments):
           result = subprocess.run(["/usr/bin/git", "--no-pager", "--git-dir=" + str(git), *arguments],
                                   env=environment, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, check=True, timeout=10)
           return result.stdout
       if read("rev-parse", "--verify", revision + "^{commit}").strip().decode("ascii") != revision:
           raise ValueError()
       source = read("show", "--no-textconv", revision + ":infra/03-security/openbao/scripts/install-renderer-issuer.sh")
       binding()
       if len(source) > 100000 or hashlib.sha256(source).hexdigest() != "27a097f133ced7bc1d3657c401a16fa923d464878a10b38d69d5e0e7033343c9":
           raise ValueError()
       subprocess.run(["/bin/sh", "-s", "--", repository, revision, target], input=source,
                      env=environment, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                      check=True, timeout=60)
   try:
       bootstrap()
   except Exception:
       raise SystemExit(1)
   P01_ISSUER_BOOTSTRAP
   test "$?" = 0 || exit 1
   ```

   승인 SHA는 checkout의 현재 HEAD와 별개로 owning Task에서 검토한 full commit이다.
   installer 자체도 환경·replacement를 차단한 full commit에서 읽고 고정 공개 hash와 대조한 메모리 bytes로 실행한다. installer가 검증한 request shell도 token 입력 전에 같은 bytes로 고정한다. 쓰기 가능한 checkout 경로를 다시 열어 실행하지 않는다.

3. 새 발급 전에 Agent를 중지한다. 현재 operator 인증을 통해
   `auth/token/create/renderer-issuer`와 `auth/token/create/renderer-cleanup`에서
   token을 별도로 발급한다. JSON 입력의 `policies`는 각각 정확한 policy 문자열이며,
   `ttl="5m"`, `explicit_max_ttl="5m"`, `renewable=false`, `no_default_policy=true`를
   함께 요구한다. 발급 응답을 출력하지 않고 보호된 stdin/custody로 처리한다.
   root·renderer·application token을 helper 입력으로 사용하지 않는다. 운영자 token만 숨김
   입력으로 받고, 두 짧은 token은 server 안의 CLI가 만들어 변수로 바로 받으므로 화면에
   나오지 않는다. CLI의 `policies=…`는 문자열로 보내져 operator 정책의 허용 형식과 맞는다.

   W0의 셸 규칙대로 `bash --noprofile --norc` 셸에서 실행한다.

   [window script](../../../../infra/03-security/openbao/scripts/owner-window.sh)의 `agent-restart`가
   이 순서를 실행한다. operator credential을 숨김 입력으로 받아 `hy-home-operator` 정책인지 먼저
   확인하고(아니면 Agent를 멈추지 않는다), Agent 중지 → 두 token 발급 → 설치된
   `issue-renderer-secret-id.sh`에 stdin으로 전달한다. image 인자는 OpenBao Compose 파일의 고정
   image 한 줄(두 service가 같아야 함)에서 읽는다. 끝나면 `issue rc`, 최대 90초 기다린 Docker
   health, `out` 아래 파일의 mode와 이름만 출력한다. 중간에 실패하면 Agent가 멈춰 있을 수 있다고
   알리며, 원인을 고친 뒤 다시 실행한다.

   script는 mutable checkout이 아니라 검토한 commit 객체에서 읽는다. 아래 `p01_run`은 W1
   bootstrap과 같은 Git 격리로 전체 40자리 SHA를 확인하고 blob을 tmpfs 파일로 꺼내 실행한다.
   그 commit에 script가 없으면(이 script를 담은 PR이 병합되기 전) 실행하지 않고 실패한다.

   ```bash
   p01_run() {  # p01_run <40자리 commit> <저장소 경로> <인자…>
     local c f r
     case "$1" in *[!0-9a-f]*) return 1 ;; esac; [ "${#1}" = 40 ] || return 1
     c="$(/usr/bin/env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_REPLACE_OBJECTS=1 \
       /usr/bin/git --git-dir=/home/hyunyoun/data/hy-home.docker/.git rev-parse --verify "$1^{commit}")" && [ "$c" = "$1" ] || return 1
     f="$(umask 077; /usr/bin/mktemp "${XDG_RUNTIME_DIR:?}/p01-run.XXXXXX")" || return 1
     /usr/bin/env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_REPLACE_OBJECTS=1 \
       /usr/bin/git --git-dir=/home/hyunyoun/data/hy-home.docker/.git show --no-textconv "$1:$2" >"$f" && [ -s "$f" ] &&
       bash "$f" "${@:3}"; r=$?
     rm -f "$f"; return "$r"
   }
   issuer_commit=… operator_tools=… agent_volume=… issuance_journal=… \
     p01_run <검토한 40자리 commit> infra/03-security/openbao/scripts/owner-window.sh agent-restart
   ```

   window 안이면 같은 입력을 앞에 붙여
   `issuer_commit=… operator_tools=… agent_volume=… issuance_journal=… bash "$P01_SCRIPT_DIR/owner-window.sh" agent-restart`로
   실행한다. 입력은 Task에 기록한 값이며 셸 변수로만 두면 script가 보지 못한다.

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
sh infra/03-security/openbao/scripts/check-tls-material.sh "$DEFAULT_SECURITY_DIR/openbao/tls" hy-home/openbao:2.7.1-go1.27.3-net0.60.0-r1@sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8 # <!-- runtime-version-exception: compatibility — preflight requires the exact owned image; docker-compose.yml owns the pin -->
```

명령은 만료·CA chain·정확한 SAN·cert/key 일치와 UID100:GID1000의 읽기를 검증한다.
마지막 읽기 검사는 pull 없는 network-none 임시 컨테이너와 exact-file readonly bind만 사용한다.
TLS_PREPARED / NOT_DEPLOYED는 초기 준비 기록이다. 이후 SPEC-0243의 2026-10-22 12:30
window에서 TLS·config-owned audit와 Agent가 HOME에 적용되었다(REPOSITORY_REPORTED,
원시 운영 영수증은 이번 세션에 미제공). 같은 Task는 W0 preflight 12초 PASS를 기록한다.
이 세션의 새 실행 증거로 해석하지 않는다. CLI는 `BAO_CACERT`/`BAO_TLS_SERVER_NAME`, Agent는 `VAULT_CACERT`, metrics는
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
mountpoint가 `/`라는 관찰이 있어야 audit 용량 증거로 인정한다. 2026-10-15 owner가 rotation
규칙과 시간 단위 drop-in을 설치했다(SPEC-0243). 이후 HOME audit 파일 성장과 mount 적용은
2026-10-22 Task에 기록됐다. 첫 자연 회전·회전 inode와 HOME 용량 추세는 아직 미확보다. 임시 용량 장애 시험은 실제 host 용량 최적값이 아니다.

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
공급자 channel·아래 W4/W5 SEC01 gate·pre-upgrade snapshot·5단계 custody 기록(SPEC-0242)·빈 이전
버전 환경 복원과 이후 candidate upgrade를 검증한다. 2.7 데이터에 이전 image를 붙이는
것은 rollback이 아니다. 아래 120분 maintenance window 시간표
안에 restore/unseal/검증까지 가능한지 측정한다. 두 값은 계획 추정치이며 관측한
RTO가 아니다. 목표를 넘거나 복구 자료가 없으면 HOME만 보류한다. P06 확대도 HOME gate 전에는
진행하지 않는다.

HOME 적용 전 source-only rollback은 검토된 revert다. 적용 후에는 TLS·audit 선언과 로그 custody를 유지하는
검토된 override 또는 fix-forward만 사용한다. client도 검증된 endpoint로만 전환하며 HTTP나 audit 제거로 되돌리지 않는다.

P06 확대는 실제 HOME cold boot·5단계 custody 기록(SPEC-0242)·복구 gate가 통과할 때까지 보류한다.

#### HOME 적용 입력과 승인 순서

값은 기록하지 않는다. 각 단계는 앞 단계가 끝난 뒤에만 진행하며, 괄호 안 승인이 따로 필요하다.

1. 아래 W4/W5의 SEC01 gate(image 잔여 위험 수용과 7일 안의 stable 조회)가 기록돼 있다(owner).
2. 보존된 attempt 대상과 container의 처리를 정한다(삭제는 명시 승인). attempt 03·04·chown container와 `-03` 대상은 2026-10-13에 owner가 삭제했다. 같은 날 owner 결정으로 빈 기본 restore 대상과 `-04` 대상도 삭제했고, 기존 업그레이드 전 snapshot 파일은 새 snapshot이 생길 때까지 rollback 지점으로 보존한다.
3. snapshot 전용으로 제한한 identity와 token을 발급한다(credential 발급 승인). operator policy는 `sys/policies/acl` 쓰기와 orphan token 발급을 허용하지 않으므로(2026-10-13 HTTP 403) 복구 share ceremony로 만든 임시 root가 필요하다. owner 결정으로 8단계 업그레이드 window의 같은 ceremony에서 발급하며, 그 전까지 일일 backup의 OpenBao snapshot은 recovery gap으로 계속 실패한다.
4. 그 token이 일반 secret을 읽지 못하고 갱신되는지 확인한 뒤, 쓰기를 멈춘 상태에서 새 업그레이드 전 snapshot을 만든다(backup 실행 승인).
5. BKP-003·R2 자격 증명·BKP-002·Cloudflare 계정 접근의 off-host 보관과 share·CA key의 host 보조 사본을 값 없이 확인한다(owner 확인). 확인 전까지 미실행이며, P01은 계속 차단된다. 배치와 확인은 아래 [1인 관리자 custody 절차](#1인-관리자-custody-절차)를 따른다.
6. 새 attempt 식별자로 빈 대상에 의미 있는 restore를 하고 canary 읽기와 renderer 재인증을 확인한다(독립 READY 검토 후 사용자 승인). 이전 attempt 04의 도구는 추적되지 않았다. 지금은 추적되는 `protected-semantic-restore.py`가 있고, SPEC-0243이 합성 자원에서 전체 `perform()`을 native로 리허설했다. HOME의 실제 restore와 canary는 아직 실행되지 않았다.
7. audit 용량을 측정하고 logrotate를 등록한다(sudo가 필요한 host 변경 승인). 규칙과 drop-in은 2026-10-15에 설치됐다. 현재 HOME server에는 audit mount가 없으므로 용량 측정은 8단계 업그레이드 window로 미룬다.
8. maintenance window 안에서 server 업그레이드, 지정 운영자의 수동 unseal, wrapped 재발급을 포함한 Agent 업그레이드를 진행한다(승인된 runtime 변경 의도의 새 검토).
9. HOME cold boot를 한다(별도 승인).
10. 현재 버전 인증과 consumer 읽기를 위한 consumer와 ACL을 고른다(P06 담당자 선택).

변조된 HMAC의 audit 검증은 미실행이다. Agent 인증 실패 alert는 SPEC-0239(PR #463, #466)로 source에 들어왔다. `agent.hcl`이 `metrics_only` listener(8100)로 `/agent/v1/metrics`를 열고, Prometheus job `openbao-agent`가 scrape하며, `OpenBaoAgentMetricsScrapeFailing`과 `OpenBaoAgentAuthFailure`가 알린다. 아직 배포되지 않았다. 실행 중인 server와 Agent는 Compose가 고정한 image보다 이전 버전이므로, Agent만 다시 만들면 server보다 먼저 업그레이드된다. 그래서 2026-10-14 owner 결정으로 유지보수 창의 W5(Agent 업그레이드와 wrapped 재발급)에서 함께 배포하고 이어서 Prometheus를 다시 만든다. 인증은 되는데 렌더만 낡는 경우는 metric이 없어서 배포 뒤에도 Docker healthcheck(token lookup·KV 읽기·렌더 bytes 일치)의 `unhealthy`로만 드러나고 알림은 없다.

#### 1인 관리자 custody 절차

이 절차는 owner가 직접 수행한다. agent는 값을 읽거나 옮기지 않고, 값이 없는 owner 진술만
SPEC-0204 TSK-0006에 기록한다. 값은 화면 공유·채팅·명령 인자·터미널 기록·이 저장소
어디에도 남기지 않는다. Claude Code의 `!` 명령 출력은 대화 기록에 남으므로 값을 다루는
명령은 기록되지 않는 별도 터미널에서만 실행한다.

2026-10-14 owner 결정(SPEC-0242)으로 관리자가 1명인 이 HOME은 share를 host에 두고 host
백업에 포함한다. off-host로는 백업과 원격 저장소를 여는 key만 둔다. 장소 A는 owner가 관리하는 host 밖 장소로,
비밀번호 관리자 계정이나 owner의 별도 데스크탑이다. 2026-10-14 기준 백업·R2 값은 별도
데스크탑에, Cloudflare 계정 접근은 비밀번호 관리자 계정에 있다. 이 배치는 장소 분리로
threshold를 지키지 않는다. 그 대신 host를 잃어도 R2 사본에서 모두 복구할 수 있게 하려는
것이다. 아직 R2 원격 복구를 실행하지 않았고 OpenBao 일일 snapshot도 실패 중이므로(위
복구 gap) 현재 보장된 상태는 아니다.

**배치.**

| 항목 | 내용 | 둘 곳 | 노출되면 |
| --- | --- | --- | --- |
| unseal share 파일 | OpenBao Shamir share 3개(threshold 2), `secrets/security/openbao/openbao_unseal_keys.txt` | host `secrets/`, host Restic 백업(local·R2) | 한 주체가 unseal과 root ceremony를 할 수 있음 |
| CA key | 내부 TLS 공용 root CA 개인키(`secrets/certs/`), OpenBao 전용이 아님 | host `secrets/`, host Restic 백업 | 그 CA를 믿는 모든 내부 TLS endpoint를 사칭할 수 있음 |
| host 보조 사본 | 위 두 항목을 포함한 owner의 사본, `/home/hyunyoun/data/hy-home.secrets`(root 0700) | 같은 system disk | 실수로 지운 경우만 막음. host·disk를 잃으면 함께 잃음 |
| BKP-003 offsite key | R2 원격 Restic 저장소 암호 | host 밖 장소 A | R2 읽기 권한과 합쳐지면 R2 사본의 모든 secret과 share |
| R2 자격 증명 | BKP-004·005 R2 API token(객체 읽기·쓰기) | host 밖 장소 A | BKP-003과 합쳐지면 R2 사본을 읽음 |
| BKP-002 local key | local host Restic 저장소 암호 | host 밖 장소 A | local 저장소에 접근하면 그 안의 모든 secret과 share |
| Cloudflare 계정 접근 | 로그인·2FA 복구 코드 | host 밖 장소 A | R2 자격 증명을 다시 발급하고 bucket과 lock 규칙을 바꾸거나 지울 수 있음 |
| R2 account ID·bucket 이름 | `.env`의 `BACKUP_OFFSITE_R2_ACCOUNT_ID`·`BACKUP_OFFSITE_R2_BUCKET`(secret 아님) | host 밖 장소 A | 단독으로는 접근을 주지 않음. host를 잃으면 `.env`가 R2 사본 안에 있으므로 따로 필요함 |

BKP-001(pgBackRest)은 host `secrets/`에 있어 host 백업으로 함께 복구된다. host 보조 사본은
host 백업 범위 밖이며 off-host 보관이 아니다.

**받아들인 노출.** 장소 A 하나가 뚫리면 BKP-003과 R2 자격 증명으로 R2 사본을 열어 모든
secret과 share를 얻는다. 같은 계정의 Cloudflare 접근과 쓰기 가능한 R2 token으로 bucket lock
규칙이나 bucket을 지우고 lock이 없는 `locks/`·`index/`를 바꿔 유일한 off-host 사본을 망가뜨릴
수도 있다. host를 읽는 한 주체는 share 3개를 모두 가진다. 둘 다
[POL-0085 Exceptions](../../policies/04-security-and-secrets/0085-openbao.md#existing-custody-decision-and-missing-closure)의
예외로 남고, 이 절차로 닫히지 않는다. 장소 A는 비밀번호 관리자 계정이면 강한 마스터 비밀번호와 2FA로, 별도 데스크탑이면 로그인과
디스크 암호화로 보호하고,
그 복구 수단(emergency kit·복구 코드)과 2FA 요소(TOTP seed 등)를 같은 계정이나 host에 두지
않는다. 복구 수단은 host와 장소 A 없이 닿는 오프라인 장소에 두고, 장소 A의 2FA가 그 안에
저장된 Cloudflare 로그인에 기대지 않게 한다. Claude Code `!` 명령이나 agent 세션처럼 저장소
UID로 도는 process도 host를 읽는 주체에 들어간다.

**절차.**

1. BKP-003, R2 자격 증명, BKP-002, Cloudflare 계정 접근, R2 account ID와 bucket 이름을 계정
   A로 **복사**한다. 원본은
   지우지 않는다. clipboard 기록·동기화가 꺼진 상태에서 한 번에 하나씩 옮긴다.
2. host 보조 사본을 갱신한다. share와 CA key가 바뀔 때마다 다시 맞춘다. sudo로 맞출 때도 값을
   명령 인자·기록에 남기지 않는다.
3. host가 아닌 장치에서 장소 A를 열어 항목을 꺼낼 수 있는지 확인한다. 값이 맞는지는 장소 A에서
   꺼낸 BKP-003·R2 자격 증명·account ID·bucket을 숨김 입력으로 넣어 읽기 전용 R2 snapshot
   목록을 받아 확인한다. 값은 출력하지 않는다. 6단계 restore는 host의 사본을 쓰므로 장소 A의
   값을 증명하지 못한다.
4. 아래 기록을 값 없이 채워 agent에 전달한다.

| 항목 | 둔 곳 | host 밖인가 | 꺼낼 수 있음을 확인한 날 |
| --- | --- | --- | --- |
| BKP-003 offsite key | | | |
| R2 자격 증명 | | | |
| BKP-002 local key | | | |
| Cloudflare 계정 접근 | | | |
| R2 account ID·bucket 이름 | | | |
| 장소 A의 값으로 받은 R2 snapshot 목록 | | 해당 없음 | |
| unseal share 파일과 CA key의 host 보조 사본 | | 해당 없음 | |
| 장소 A의 복구 수단이 장소 A와 host 밖에 있는가 | | | |

**판정.** 모든 칸이 채워지고 장소 A의 다섯 행이 "host 밖 = 예"이며 R2 목록을 받은 날이 있고
마지막 행이 "예"일 때만
agent가 5단계를 기록한다. Evidence 결과는 `PASS`이고 Check는 "owner-attested"로 시작한다.
칸이 비면 `NOT_RUN`, "아니오"가 하나라도 있으면 `FAIL`이다. 둘 다 유지보수 창을 열지
않는다. owner 진술일 뿐이며 저장소는 보관 사실을 인증하지 못한다.

### Maintenance Window Plan

현행 상태(2026-10-22): SPEC-0243은 `-06` semantic restore accepted와 W4/W5의 HOME
2.7.1·TLS·audit·Agent 적용, 수동 backup 성공을 보고한다. 아래의 2.6.2→2.7.1 window <!-- runtime-version-exception: history — SPEC-0243의 2026-10-22 실행 기록과 이전 window 입력 -->
블록과 승인 commit은 그 실행의 역사적 입력이다. 다음 창에는 새 현재 버전·빈 attempt·
source pin/검토·창별 승인을 먼저 확정하며, 이미 끝난 업그레이드를 다시 실행하지 않는다.

2026-10-13 owner 결정으로 남은 HOME 단계를 한 번의 maintenance window로 묶는다. 이
계획은 문서일 뿐 실행 증거가 아니다. 모든 값(share·OTP·token·key)은
[POL-0085](../../policies/04-security-and-secrets/0085-openbao.md#maintenance-window-credential-handling)의
경로(숨김 입력, stdin, 보호된 FD, tmpfs 0600 파일, 명령 하나에만 붙는 환경 변수)로만 다루고, 명령
인자·터미널 기록·채팅에 남기지 않는다. 각 단계의 결과는
SPEC-0204 TSK-0006 Evidence에 값 없이 기록한다.

**전제 조건(위 5단계).** BKP-003·R2 자격 증명·BKP-002·Cloudflare 계정 접근이 1인 관리자 custody 절차에 맞는 off-host 보관에
있다는 owner 확인이 값 없이 기록되어야 한다. 확인이 없으면 window를 열지 않는다.

| 순서 | 단계 | 목표 시간 | 승인 |
| --- | --- | --- | --- |
| W0 | 사전 점검 | window 전 | owner(runtime 재생성, host sudo) |
| W1 | root ceremony | 10분 | buenhyden(서로 다른 share 2개 수동 입력) |
| W1c | renderer 정책·token role 적용(plan·apply) | 10분 | owner(root 사용, credential 정책 변경) |
| W2 | snapshot token 발급과 확인 | 5분 | owner(credential 발급) |
| W3 | writer 정지, lease, 새 업그레이드 전 snapshot | 10분 | owner(backup 실행) |
| W3b | R2 artifact 보관(W3 직후, W3a 전) | 10분 | owner(off-host 전송) |
| W3a | 입력 준비와 격리 semantic restore | 25분(성공한 restore는 최대 약 16분) | 정확한 새 artifact·빈 대상의 독립 검토와 owner |
| W4 | server 업그레이드와 수동 unseal | 10분 | owner(runtime 변경) |
| W5 | Agent 업그레이드, 재발급, Prometheus·Gatus 재생성 | 15분 | owner(runtime 변경) |
| W6 | audit 쓰기·mode·성장 확인(회전은 사후) | 5분 | owner |
| W7 | 사후 점검과 root 폐기(다음 backup은 사후) | 10분 | owner |
| W8 | cold boot | 별도 window | owner(별도 승인) |

window는 120분이다(2026-10-14 owner 결정, SPEC-0243). 위 목표의 합은 110분이며 나머지 10분은
여유다. W3b는 W3 산출물만 쓰므로 W3a보다 먼저 한다. W4부터 W7까지 40분이 걸리므로 시작
시각을 T로 두고 시각으로 멈춘다: T+15까지 W1이 끝나지 않으면 window를 닫는다. T+45까지
W3b가 시작되지 않으면 W3b 이후를 다음 window로 넘긴다. T+55까지 W3a가 시작되지 않으면
W3a를 시작하지 않는다(단발 attempt를 쓰지 않는다). T+80까지 W4가 시작되지 않으면 HOME
server를 바꾸지 않고 멈춘다.

어느 지점에서 멈추든 같은 정리를 한다: W0에서 멈춘 `hyhome-backup.timer`를 다시 켠다.
silence는 window 동안 발생한 경보를 기록한 뒤 지운다. W3에서 멈춘 hy-home.k8s 로그인 주체를
다시 켠다. W3에서 멈춘 Agent는 다시 켜지 않는다. 일회용 SecretID를 이미 소비해 인증하지
못하므로, consumer는 렌더된 파일로 계속 동작하고 Agent는 다음 window의 W5에서 새 SecretID로
올린다(2026-10-15 owner 결정). 그동안 나는 Agent 경보는 알려진 상태로 기록한다. W2가 끝난
뒤 멈췄으면 설치된 snapshot token은 일일 backup이 쓰므로 그대로 두고, 다음 window는 그 token이
갱신되는지 확인한 뒤 W2를 건너뛴다. 임시 root는 server가 unsealed이고 operator token이
있으면 아래 W7의 `revoke-root`로 폐기한다. W1c rollback 판단이 열려 있어도 버리며, rollback이
필요하면 다음 window의 새 root로 한다. server가 sealed라 폐기할 수 없을 때만 아래 이전 root
정리 규칙을 따른다(unsealed인데 OIDC가 안 되면 아래 `cleanup --keep-root` 규칙). W0·W1·W3a·W5·W7의 operator token은 각자 `revoke-self`로 폐기한다. server가
sealed라 폐기할 수 없는 token은 OIDC 최대 TTL(4시간) 안에 만료되며, 그 사실을 값 없이 기록한다.
server가 unsealed이면 root와 마지막 operator token을 버리기 전에 UI에서 새 OIDC 로그인을 해
W0 방식으로 `$XDG_RUNTIME_DIR/p01-op-proof.token`에 받고
`BAO_TOKEN="$(cat "$XDG_RUNTIME_DIR/p01-op-proof.token")" docker compose exec -T -e BAO_TOKEN openbao bao read -field=policies auth/token/lookup-self`가
`[hy-home-operator]`를 돌려주는지 본 뒤, 같은 형식의 `bao token revoke -self`로 그 token도 폐기한다.
안 되면(gateway나 OIDC 장애) root와 custody를 지우지 않고 OIDC 접근부터 복구한다. 복구 수단 없이
관리 접근을 모두 버리지 않는다. 이때 아래 `cleanup`에 `--keep-root`를 붙여 W1 custody, `p01-op-*.token`과
`p01-window.vars`를 남기고, root로 OIDC를 고친 뒤 `--keep-root` 없이 이 정리를 처음부터
다시 한다(`--keep-w2`는 kept W2 custody가 있는 동안 계속 붙이는 반면 이 옵션은 다시 뺀다). 보존은
owner가 맡으며 재부팅 전까지, 최대 다음 window까지이고 그 기한 날짜를 값 없이 Task에 기록한다.
보존 동안에도 Linger나 로그인 세션을 유지해 logind가 custody를 지우지 않게 한다. server가 sealed면 이 확인은 할 수 없고 root도 unseal 전까지 쓸 수
없으므로, custody는 그대로 지우고 다음 window W1 뒤의 이전 root 정리에 맡긴다.

exit2(INDETERMINATE)가 남았으면 그 단계의 복구가 정리보다 먼저다. W1 exit2는 OTP가 함께 있는
custody 파일을 열지 않고, window 안이든 다음 window의 W1 전이든 operator token으로
같은 형식의 `bao read sys/generate-root-token/attempt`로 started·progress와 nonce가 있는지만 값 없이 기록한 뒤
`BAO_TOKEN="$(cat "$XDG_RUNTIME_DIR/p01-op-w1.token")" docker compose exec -T -e BAO_TOKEN openbao bao delete sys/generate-root-token/attempt`를
실행해 남은 attempt를 취소하고(operator 정책이 허용한다) `cleanup --discard-root`로 W1 custody를 지운다. 이 경우 생겼을 수
있는 root는 다음 window W1 뒤의 이전 root 정리가 찾는다. W2 exit2가 window 안에서 해결되지
않았으면 W2 custody(`p01-token.*`)와 대상의 `.snapshot_token.txt.issuance-lock`은 남기고 아래
`cleanup`에 `--keep-w2`를 붙인다. 그 안의 token은 snapshot 전용 권한에 최대 720시간이며 tmpfs라
재부팅 때 사라진다. W2 helper는 lock이 있으면 멈추므로 다음 window의 W2와 W3는 검토된 W2 복구
절차가 생길 때까지 **BLOCKED**다([POL-0085](../../policies/04-security-and-secrets/0085-openbao.md#maintenance-window-residuals)가
받아들인 잔여 위험). kept W2 custody가 있는 동안은 이후 모든 정리에서도
`--keep-w2`를 붙인다. sealed server에서 root custody를 지우면(`--discard-root`) OIDC 확인 없이 관리 접근을 모두
버리는 것이며, 이는 [POL-0085](../../policies/04-security-and-secrets/0085-openbao.md#maintenance-window-residuals)가 2026-12-15까지 받아들인 잔여 위험이다(복구는 share 2개로 unseal한 뒤
OIDC operator와 W1 절차).

지우기 전에 credential이 없는 증거, 곧 W1c의 `prior-state.json`·`state.json`(`p01-roles.*`,
`p01-roles-plan.*`), W1·W2·W7의 `state.json`, W1c·W2·W7의 `operation-intent.json`과 `$P01_INPUTS`의
contract·lease·receipt를 owner 전용 영구 저장소(tmpfs·문서 밖)에 복사한다. 그다음 secret 파일을
모두 지운다. root는 `root.token`만이
아니라 `initialization.json`의 OTP와 `update-2.json`의 encoded token으로도 다시 만들 수 있으므로
custody 디렉터리 전체를 지운다:

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" evidence "$HOME/p01-evidence/<날짜>-<작업>"
bash "$P01_SCRIPT_DIR/owner-window.sh" cleanup
```

bootstrap 셸이 아니면 먼저 `. "$XDG_RUNTIME_DIR/p01-window.vars"`로 `P01_SCRIPT_DIR`를 읽는다.
`evidence`는 위 receipt를 tmpfs·저장소 밖 0700 디렉터리로 복사하고 각 `state.json`의 상태만
출력한다. `cleanup`은 남은 `p01-op-*.token`을 `revoke -self`로 폐기한 뒤 custody·share·token
파일을 `shred -u`로 지우고 `p01-window.vars`를 지운다. 옵션은 `--keep-root`·`--keep-w2`이며 위
규칙대로 해당 custody를 남긴다(환경변수는 읽지 않는다). W1 custody에 `root.token`이 있는데 W7의
`ROOT_REVOKED_OPERATOR_HEALTHY` receipt가 없으면 아무것도 지우지 않고 멈춘다. W7을 하지 않고
root custody를 버리는 경우(W1 exit2, sealed server)에만 `--discard-root`를 붙인다. `evidence`는
K8s writer state(`p01-k8s.*`의 원래 UID·replica·selector, 변경 목록, Finish 시각)도 복사하지만
`$P01_INPUTS`의 contract·lease·receipt는 복사하지 않으므로 W3a를 연 window면 그것은 따로 복사한다.
끝에 남은 `p01-*` 항목을 출력하며 `p01-client.*`(secret 없는 helper 사본)와, W3a를 연 window면
`p01-inputs.*`, K8s writer를 멈춘 window면 `p01-k8s.*`만 남아야 한다.

변수가 아닌 고정 glob이라 셸을 다시 열어 변수가 비어도 `/` 아래를 지우지 않는다. 멈춘 시각,
남은 단계와 폐기하지 못한 token을 값 없이 Task에 기록한다. W3a는 attempt와 대상이 고정된
단발 실행이라, 다음 window에서 다시 하려면 새 attempt를 정하는 별도 변경이 먼저
필요하다. W6의 실제 회전·`SIGHUP` 재개방과 W7의 다음 backup 성공은 window 안에서 볼 수
없으므로 window 뒤 관찰로 기록한다. W1b rekey는 이 window에 없습니다(SPEC-0242). W1 직후
W1c, 그다음 W2·W3를 엽니다. 새 snapshot의 semantic restore를 끝낸 다음 W4 cutover를
엽니다. 중단 조건이 생기면 HOME 변경을 시작하지 않고 남은 단계는 다음 window로 넘깁니다.

Compose는 두 OpenBao service 모두 자체 빌드 image(manifest `a58fb110`, Go 1.27.3)를 고정한다. <!-- runtime-version-exception: history — 현재 고정 image의 builder Go 버전이며 build-inputs.json이 pin을 소유함 -->
W4/W5의 SEC01 gate는 두 가지다(2026-10-14 owner 결정): owner가 이 image의 잔여 위험(서명 없음,
CVE-2025-60876, GO-2026-5932 처분)을 수용한 기록(2026-10-21 교체 승인, POL-0085)과, window 시작 7일 안의 최신 stable
조회다. fix-forward라 image는 window 뒤에도 실행되므로 이 수용은 window가 아니라 SEC01 기준
15가 수용되거나 image가 교체될 때까지 유효하다. 조회에서 현재 image의 OpenBao에 영향을 주는 보안 수정이 든
새 stable·Go·x/net·x/crypto가 나왔으면 gate는 실패다. SEC01 기준 15 전체는 다른 gate까지
포함하므로 W4 조건이 아니다. 둘 중 하나라도 없거나 실패면 W4/W5를 실행하지 않는다. 실제 scan·플랫폼 적용 판단은
[SEC01 Task](../../../03.specs/0204-service-integration-security-and-operations/tasks/tsk-0009-sec01-stable-security-integration.md)가
소유합니다. 아래 명령의 준비 여부와 실제 실행은 별도이며, 지정 운영자의 서로 다른 share 2개·5단계 custody 기록(SPEC-0242)과
W3a 복구 gate도 계속 필요합니다.

**W0 사전 점검.**

```bash
HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh
docker compose exec -T openbao bao status
docker compose --profile security config --images | grep '^hy-home/openbao' | sort -u |
  xargs docker image inspect --format '{{.Id}}'   # 없으면 오류로 끝난다
df -h /home
systemctl show hyhome-backup.service -p Result,ExecMainExitTimestamp
docker info -f '{{.Debug}}'   # false여야 한다. true면 exec 환경의 token이 dockerd 로그에 남는다
command -v jq                  # 이전 root 정리에 필요하다
loginctl show-user "$USER" -p Linger   # yes가 아니면 window 동안 다른 로그인 세션을 유지한다
docker compose --profile backup run --rm --no-deps restic-offsite cmd snapshots --no-lock --compact | tail -4   # W3b가 쓸 R2 저장소
docker compose --profile backup run --rm --no-deps restic-offsite cmd stats --no-lock --mode debug 2>&1 | grep -A2 '^File Type: data'
: >"$XDG_RUNTIME_DIR/p01-window.vars"   # 이 window의 경로 변수 기록을 비운다
```

window 전체를 `bash --noprofile --norc`로 연 셸 하나에서 `unset HISTFILE`과
`cd /home/hyunyoun/data/hy-home.docker` 뒤에 실행한다(상대 경로와 `.env`가 main checkout을
가리킨다). 기본 셸 zsh의 `read -p`는 coprocess 읽기라 숨김 입력이 되지 않는다. 블록의
`|| exit 1`은 그 셸을 닫으므로, 값이 아닌 경로 변수(`P01_RUNTIME_DIR`·`P01_SCRIPT_DIR`·
`P01_CUSTODY_DIR`·`P01_TOKEN_CUSTODY_DIR`·`P01_INPUTS`·`P01_SNAPSHOT_DIRECTORY` 등)는 만들 때마다
`declare -p <이름> >>"$XDG_RUNTIME_DIR/p01-window.vars"`로 남기고(W0 시작에
`: >"$XDG_RUNTIME_DIR/p01-window.vars"`로 비운다. 정리는 이 파일 없이 고정 glob으로 한다), 셸이 닫히면 같은 규칙의 새
셸에서 `. "$XDG_RUNTIME_DIR/p01-window.vars"`로 되살린 뒤 정리나 재시도를 한다. 값·token은 이
파일에 넣지 않는다. 마지막 로그인 세션이 끝나면 logind가 W1 custody가 있는
`$XDG_RUNTIME_DIR`를 지우므로 Linger나 별도 세션으로 막는다.

기대: compose 검증 통과, `Sealed false`, compose가 고정한 candidate image가 local에
있음, 남은 용량 확인, 마지막 backup 결과 확인. 위 SEC01 gate(image 잔여 위험 수용과 7일 안의
stable 조회)가 기록돼 있고 위 TLS preflight가 PASS여야 한다. 하나라도 아니면 중단한다.
R2 줄은 exit 0이고 저장소 `f6973d0274`의 state·host snapshot 이력을 보여야 한다(2026-10-20
owner 승인으로 비운 bucket에 재초기화하고 첫 copy·check가 통과했다. SPEC-0204 TSK-0009). 저장된 byte에
W3 snapshot·receipt 크기의 1.05배를 더한 값이 `offsite.sh`의 상한(9,000,000,000 byte, owner의
10 GB 절대 상한) 안이어야 한다. 둘 중 하나라도 아니면 window를 열지 않는다. W3b는 W1·W1c·W2·W3
뒤에 있으므로 거기서 멈추면 root 절차와 Agent의 일회용 SecretID를 이미 쓴 뒤다. 저장소가 없다고
나와도 `restic-offsite init`으로 고치지 않는다. 새 key와 ID가 생기고 기존 data는 lock 아래에 남아
열 수 없게 된다. owner가 계정·bucket·credential·`config`/`keys` object를 읽기 전용으로 먼저 확인한다
(2026-10-20 13:12의 `repository does not exist`는 owner가 bucket을 비운 결과였다. SPEC-0204 TSK-0009).
image가 없으면 registry에서 받을 수 없으므로, 별도 승인으로 검토된 OCI archive를 다시 import해 같은 digest인지 확인한다(SPEC-0204 TSK-0009).

W0에서는 audit 디렉터리와 rotation 계약도 server 재생성 전에 준비합니다. 실제 audit
경로 `/home/hyunyoun/storage/volumes/security/openbao/audit`는 2026-10-14에 독립 IaC
검토 후 생성됐습니다: device2064/inode115609395, UID100/GID1000, mode0700,
해당 filesystem 가용 공간 약2.5TiB. 전용 rotation 규칙은 2026-10-15에 등록됐고, audit
volume·file과 server mount는 아직 없습니다. W6는 사후 쓰기·reopen 검증 단계이며 audit 디렉터리의 최초 준비를
그때까지 미루지 않습니다. 매 실행 전 같은 path/device/inode·권한과 실제 mount 용량을
다시 확인하고, 원본 데이터 volume `hy-home-infra_openbao-data`의 bind device
`/home/hyunyoun/storage/volumes/security/openbao/data`와 device2064/inode115612005를
보존합니다. audit를 준비하려고 데이터 권한을 재귀 변경하지 않습니다.

[전용 rotation 규칙](../../../../infra/03-security/openbao/config/logrotate/openbao)은
이 HOME의 UID100=`dhcpcd`, GID1000=`hyunyoun` 매핑을 사용합니다. host의 `dhcpcd` 계정은
OpenBao와 같은 UID라 `audit.json`, TLS server key, Raft data, Agent token sink, `role_id`와
렌더된 Keycloak·Grafana admin password, SecretID 파일, 그리고 `docker compose exec` 동안 container
안 `bao` process의 환경에 있는 root·operator token을 읽을 수 있습니다(`${DEFAULT_SECURITY_DIR}/openbao` 아래 UID 100
소유 경로). dhcpcd의 권한 분리
process는 chroot되어 위험이 작으며 [POL-0085](../../policies/04-security-and-secrets/0085-openbao.md#maintenance-window-residuals)가 2026-12-15까지 받아들인 잔여 위험입니다. host swap(`/swap.img`)은 암호화되지
않아 tmpfs의 custody·token 파일 page가 disk로 나갈 수 있고, `shred`는 그 사본을 지우지 못합니다.
이것도 [POL-0085](../../policies/04-security-and-secrets/0085-openbao.md#maintenance-window-residuals)가 받아들인 잔여 위험입니다. 최초 숫자 group
표기는 실제 격리 parser에서 거부돼 이름으로 수정했습니다. rename/create0600,
`nocopytruncate`, `compress`/`delaycompress`와 고정 container ID의 상태·Compose 라벨
검증 뒤 같은 ID에만 `SIGHUP`을 보내는 계약입니다. 성장률 미측정으로 `maxsize256M`,
`rotate14`는 초기값이며 14개 파일을 뜻합니다. 14일 보존이나 최대 파일 크기의 엄격한
상한을 보장하지 않습니다.

2026-10-14 재확인에서 host logrotate3.21.0, 공용 config와 활성 일 단위 timer가
관측됐습니다. 이전 부재 점검 뒤 파일 ctime09:40:51 KST에 상태가 바뀌었으며 설치 주체는
확인되지 않았습니다. 격리된 서명 검증 APK의 logrotate3.22.0 debug parser는 규칙을
수용했지만 실제 host debug는 권한 전환 EPERM으로 종료됐고 비대화형 sudo도 실패했습니다.
host 등록·권한 있는 parser·실제 rotation 성공을 뜻하지 않습니다.

W4 전에 root-owned0644 `/etc/logrotate.d/openbao`의 정확한 source hash, 실제 NSS
매핑과 host parser를 검증하고, 같은 공용 config·state·lock을 쓰는 시간 단위 호출을
준비해야 합니다. 시간 단위 호출은 기존 `logrotate.timer`의 일정만 바꾸는
[drop-in](../../../../infra/03-security/openbao/config/systemd/logrotate-hourly.conf)입니다.
owner가 `sudo install -D -o root -g root -m 0644` 로
`/etc/systemd/system/logrotate.timer.d/hourly.conf`에 설치하고 `sudo systemctl daemon-reload`
뒤 `systemctl list-timers logrotate.timer`의 다음 실행이 한 시간 안인지 확인합니다.
`daily`·`weekly` 규칙은 날짜 기준이라 계속 한 번만 회전합니다. 다만 `size`·`minsize`나
`hourly` 규칙은 최대 24배 자주 회전해 같은 `rotate N`으로 보존 기간이 줄고, 전역 `dateext`가
켜져 있으면 같은 날 두 번째 회전은 이미 있는 파일명 때문에 건너뛴다. 설치 전에
`grep -rnE '^\s*(hourly|size|minsize|maxsize|dateext)' /etc/logrotate.conf /etc/logrotate.d`로
해당 규칙을 확인하고 영향을 받아들일지 owner가 정한다. 되돌리기는 drop-in을 지우고
`sudo systemctl daemon-reload`이다. 실제 동작은 회전할 것이 있을 때
`sudo systemctl start logrotate.service`와 `journalctl -u logrotate`로 확인한다. 직접
`logrotate -f`는 unit hardening과 전역 config를 거치지 않으므로 증거로 쓰지 않는다. 기존 일 단위 timer에서는 `maxsize`도 하루 한 번만 검사합니다.
별도 state를 사용하는 중복 scheduler를 만들지 않습니다. source만 복사한 상태나
신호 전달만으로 등록·재개방을 완료했다고 보지 않으며, host 권한·등록·schedule 입력이
준비되지 않으면 W0에서 중단합니다. W6는 실제 inode 변경과 후속 audit 성장·실패 알림을
검증하고, 그 결과로 보존 개수·간격·용량 reserve를 조정합니다.

Traefik의 내부 OpenBao CA mount는 2026-10-15 Compose 고정 재생성으로 배포됐고,
Prometheus·Gatus의 mount는 아직 미배포입니다. 검토된 동일
서비스 image를 유지하는 scoped override 또는 해당 image의 SEC01 수용이 있어야
재생성합니다. Traefik은 backend CA/transport를 먼저 준비하고 public gateway를 확인합니다.
Prometheus/Gatus의 HTTPS-only OpenBao target 전환은 server의 내부 TLS가 실제 동작한
뒤 수행합니다. 준비되지 않은 monitoring을 먼저 바꾸거나 전체 스택을 재시작하지 않습니다.

W0의 추가 선행 조건(SPEC-0243). 하나라도 없으면 window를 열지 않는다.

- **백업 timer.** `hyhome-backup.timer`(매일 03:30 KST)가 W3 정지 범위와 W4 sealed 구간에
  돌지 않게 window 동안 멈추거나 window를 03:30부터 무작위 지연 최대 30분과 실행
  시간을 더한 구간과 떨어뜨린다. timer는 system unit이라
  멈추고 다시 켜는 것은 owner의 sudo 작업이다. timer를 멈춰도 이미 도는 실행은 멈추지
  않으므로 `systemctl is-active hyhome-backup.service`가 `inactive`인지 먼저 확인한다(일요일
  실행은 최대 4시간). timer는 `Persistent=true`라 다시 켜는 즉시 놓친 실행이 시작되므로
  W7이 끝난 뒤에만 다시 켠다.
- **checkout과 입력.** 모든 재생성과 `./scripts` bind는 main checkout의 작업 트리를 쓰므로,
  그 checkout이 깨끗하고 `HEAD`가 `P01_APPROVED_COMMIT`이며 `COMPOSE_FILE`이나 추적되지 않은
  `docker-compose.override.yml`이 없는지 확인한다. renderer helper를 [Renderer SecretID
  Delivery](#renderer-secretid-delivery) 2단계로 `$operator_tools/$P01_COMMIT`에 설치하고,
  `P01_APPROVED_COMMIT`·`operator_tools`·`issuer_commit`(=`P01_COMMIT`)·`agent_volume`·
  `issuance_journal`·`P01_SNAPSHOT_DIRECTORY`를 값 없이 Task에 기록한다.
- **operator credential.** host에는 `bao` CLI가 없으므로 OIDC 로그인은 OpenBao UI에서 하고
  token을 복사한다. token helper 파일(홈 디렉터리, 영구 disk)에는 저장하지 않는다. 쓰는 단계마다
  새로 로그인해 `umask 077`에서
  `IFS= read -rsp 'operator token> ' v </dev/tty; printf '\n'; printf '%s' "$v" >"$XDG_RUNTIME_DIR/p01-op-<단계>.token"; unset v`로
  tmpfs 0600 파일에 받는다(W1 블록의 `set -C` 뒤라 다시 받을 때는 먼저 `shred -u`로 지운다.
`<단계>`는 `w0`·`w1`·`w3a`·`w5`·`w7`). W1 source bootstrap 뒤에는
  `bash "$P01_SCRIPT_DIR/owner-window.sh" token <단계>`가 같은 일을 하고(기존 파일은 먼저 지운다)
  0600·single-link를 확인한다. UI에서 로그아웃하면 그 token이 폐기되므로 단계가 끝날 때까지
  로그인 상태로 둔다. `check-token <단계>`는 helper가 요구하는 policy·TTL·path·meta와
  generate-root attempt 상태만 값 없이 출력한다. 이후에는 FD나
  `"$(cat …)"`로만 넘긴다. W5의 숨김 prompt 대신 `BAO_TOKEN="$(cat "$XDG_RUNTIME_DIR/p01-op-w5.token")"`를
  써도 된다. token과 share는 화면에 띄우지 않고 clipboard 기록·동기화를 끈 상태에서 붙여 넣으며,
  붙여 넣은 뒤 clipboard를 비운다. 이 token은 window 끝이나 중단 때 위 정리대로 폐기하고 지운다.
- **기준선.** 실행 중 `openbao` image ID가 restore의 이전 image(`11fd73a2…`)와 같고,
  `openbao-agent`가 `healthy`이며(W1c health 정지의 기준; 이전 window가 W3 뒤 멈춰 Agent가 그때부터
  정지 상태로 기록돼 있으면 정지를 기준으로 하고, W1c는 health 대신 렌더 파일이 그대로인지만
  본다), `/dev/shm`이 `noexec` 없는
  tmpfs인지 본다. 이 2.6.2 기준은 2026-10-22 W4 이전의 역사적 입력이다. HOME은 이후 <!-- runtime-version-exception: history — SPEC-0243의 2026-10-22 실행 기록과 이전 window 입력 -->
  2.7.1+hyhome으로 올라갔고 Agent는 healthy로 보고됐다. `p01-restore-20261022-06`은 <!-- runtime-version-exception: history — SPEC-0243의 2026-10-22 실행 기록과 이전 window 입력 -->
  accepted된 사용 완료 대상이다. 다음 restore는 새 attempt/빈 대상·부모 identity와 source
  상수를 먼저 검토해야 하며 이 이전 window 블록을 그대로 실행하지 않는다.
- **HOME audit·mount 목록.** 격리 restore server는 tmpfs의 `p01-file` audit만 만들 수 있다.
  HOME의 `bao audit list -format=json`과 `bao secrets list -format=json`·`bao auth list
  -format=json`의 path·type만 값 없이 Task에 기록한다. restore가 열 수 없는 audit device나
  plugin mount가 있으면 W3a를 열지 않고 검토로 돌린다. `hy-home-operator`에는
  `sys/audit`·`sys/mounts`·`sys/auth` 읽기가 없어 W0에서는 403이다(2026-10-21 관측). 2026-10-21
  owner 결정대로 이 확인은 W1 직후, W1c 전에 W1 custody의 root로 한다:
  `bash "$P01_SCRIPT_DIR/owner-window.sh" audit-list`가 audit·secrets·auth의 이름과 type만 출력한다
  (실패하면 `<종류>: rc=1`로 멈춘다). 성공한 빈 목록만 "없음"으로 기록한다. 이 목록은 W3a gate이므로
  W1·W1c·W2·W3의 진행 조건이 아니다.
- **이전 operator token.** host에 남은 `p01-operator.token`은 W7 입력으로 쓰지 않는다.
  2026-10-14 owner 결정대로 owner가 그 token으로 `revoke-self`한 뒤 파일을 지운다. 값은
  변수로만 넘겨 argv에 이름만 남게 하고, 정책이 `hy-home-operator`인지 먼저 보고, 폐기가
  성공하고 그 token의 조회가 거부될 때만 파일을 지운다. 결과는 값 없이 Task에 기록한다:

  ```bash
  p01_run "$P01_APPROVED_COMMIT" infra/03-security/openbao/scripts/owner-window.sh retire-token <path>/p01-operator.token
  ```

  `p01_run`은 아래 [Renderer SecretID Delivery](#renderer-secretid-delivery) 3단계에 있다. 인자는 0600
  single-link 일반 파일이어야 하고, 정책이 `[hy-home-operator]`가 아니면 멈춘다. 첫 조회를 server가
  거부하면(403·`permission denied`) token은 이미 만료됐으므로 폐기 없이 지우고 `already expired; file
  removed`를 출력한다. 그 밖의 실패(sealed, container 정지, 연결 오류)는 파일을 남기고 exit1로
  멈춘다. 결과를 그대로 기록한다.

- **Traefik CA mount(W4 전).** 새 `openbao` label은 https와 `openbao-tls@file` transport를
  쓰므로 Traefik 안에 `/openbao-ca/ca.pem`이 있어야 한다. 없으면 W4 뒤 gateway를 거치는
  OIDC 로그인과 W7 `revoke-root`가 끊긴다. 2026-10-15 owner가 아래 명령으로 다시 만들었고,
  실행 image `575fa15b`와 그 파일이 확인됐다(SPEC-0243). W0에서는 같은 두 가지와 아래 차이
  비교(재생성 전 비교는 관찰되지 않았다)를 다시 본다. 다시 만들어야 하면 SEC01 수용(SPEC-0204
  TSK-0009)에 따라 별도 owner 승인으로
  `docker compose --profile core up -d --no-deps --no-build --pull never --force-recreate traefik`을
  쓴다. 기대: 실행 중 image ID가 Compose 고정 digest와 같고,
  container 안에 `/openbao-ca/ca.pem`이 있으며, gateway 경유 로그인과 대시보드 인증이 된다.
  되돌리기는 이전 image를 유지하는
  [Traefik window overlay](../../../../infra/01-gateway/traefik/compose.window-ca.override.yml)로
  `docker compose -f docker-compose.yml -f infra/01-gateway/traefik/compose.window-ca.override.yml --profile core up -d --no-deps --no-build --pull never --force-recreate traefik`이다.
  실행 중 Traefik이 Compose 고정이 아니면 W4를 열지 않는다. Prometheus는 window 전에 다시 만들지
  않는다. 지금 설정은 OpenBao scrape를 HTTPS로 바꾸므로 W4 전에는 scrape 경보만 낸다.
- **실행 중 설정과 디스크의 차이.** Prometheus·Gatus·Traefik의 실행 중 image·mount·설정을
  Compose 선언과 비교한다. 차이가 있으면 재생성이 다른 변경까지 배포하므로 먼저 검토한다.
  명령은 worktree가 아니라 `.env`가 있는 main checkout에서 실행한다. 서비스마다
  `docker inspect`의 `.Mounts`(source·destination·RW), `.NetworkSettings.Networks` 이름,
  `.HostConfig`의 memory·CPU·pids와
  `docker compose config --format json <service>`의 volumes·networks·자원을 나란히 비교한다.
  image는 Compose 고정과 비교한다. Traefik은 이미 그 image로 실행 중이고, Prometheus는 W5에서
  그 image로 올라간다. 실행 중 `Config.Image`는 tag만 담으므로 image는
  ID로 비교하고 config hash는 쓰지 않는다. 단일 파일 bind는 재생성 때 지금 파일 내용이
  들어가므로 그 파일의 최근 변경도 함께 본다. override가 고정한 참조가 로컬에서 풀리는지
  `docker image inspect --format '{{.Id}}' <override의 image>`로 두 서비스 모두 확인한다.
  2026-10-15 SEC01 수용으로 Traefik·Prometheus는 Compose 고정으로 올리며, 두 override는 이전
  image로 되돌릴 때만 쓴다. 두 서비스가 Compose 고정으로 안정되면 override를 지운다.
- **경보.** W3에서 Agent를 멈추는 순간부터 Prometheus·Gatus를 다시 만들 때까지 OpenBao·Agent
  경보가 난다. 2026-10-14 owner 결정대로 W3 시작에 Alertmanager silence를 하나 만든다. 범위는
  예상되는 경보 `alertname=~"OpenBao(Sealed|MetricsScrapeFailing|AgentMetricsScrapeFailing|AgentAuthFailure)"`로
  한정해 `OpenBaoAuditFailure`·`OpenBaoTooManyInfinityTokens`·`OpenBaoTooManyPendingTokens`는
  계속 알리고, 종료 시각은 window 끝(T+120)으로 둔다. ID를 Task에 기록하고, W7 끝이나 어떤
  중단 경로에서든 지우기 전에 Prometheus에서 window 동안의 `ALERTS{alertname=~"OpenBao.*"}`를
  조회해 발생한 경보를 값 없이 기록한다.

**W1 root ceremony.** 위 [Human Login and Normal Root Recovery](#human-login-and-normal-root-recovery)의
보호된 인증 API 절차를 사용한다. Share·OTP·token은 검토된 클라이언트의 숨겨진
입력 또는 보호된 stdin/custody로만 다루고 argv·터미널·일반 로그로 전달하지 않는다.

현재 [CLI 계약](https://openbao.org/docs/commands/operator/generate-root/)의 OTP
option은 문자열 인자이며 encoded token의 stdin 입력과 별개다. Container 안 shell이
실행 중인 server나 다른 process·runtime metadata에서 인자를 숨긴다고 가정하지 않는다.
이전 window의 OTP 인자 명령은 실행 절차에서 제거했다.

[보호 client](../../../../infra/03-security/openbao/scripts/protected-maintenance.py)는
고정 gateway와 numeric IP, 사전 검토된 공개 CA hash를 사용합니다. CA bytes를 검증한 뒤에만
OIDC operator token과 두 share를 보호된 FD로 받습니다(아래 블록: token은 W0의 tmpfs 파일, share는
`/dev/tty` 숨김 입력으로 만든 tmpfs 파일). 입력값은 서로
달라야 하며, 현재 cluster·Shamir 2-of-3·operator 권한을 확인합니다. API는 root ceremony와
lookup만 허용하고 proxy·redirect·환경 token을 사용하지 않습니다. root를 디코딩한 뒤 새
root credential로 `lookup-self`를 수행해 root-only·orphan·비만료 identity를 확인해야
`DELIVERED`가 됩니다. 이 client는 snapshot token 발급·root 폐기·upgrade를 실행하지 않습니다.

operator의 `entity_id`는 명시적인 비어 있지 않은 문자열이어야 합니다. 또한 token `meta`는 정확히
OIDC role `home-admin` 하나이고 `identity_policies`는 없거나 비어 있어야 합니다. 2026-10-27 owner가 직접
실행한 읽기 전용 lookup은 이 모양과 entity의 단일 `oidc`(`auth/oidc/`) alias를 보였습니다. entity alias와
mount accessor 대조는 이 도구의 API 허용 목록을 넓혀야 하고 operator는 auth mount 목록을 읽을 수 없으므로
검사하지 않습니다. 변경된 helper는 다음 window에서 새 `P01_APPROVED_COMMIT` 승인과 설치 검증이 필요합니다.

독립 code/security 검토와 합성 TLS·중단 회귀시험은 통과했습니다. 지정 운영자 `buenhyden`은
2026-10-14 최신 답변에서 unseal share와 보관 준비를 확인했습니다. 이는 5단계 기록이 아닌 운영자 확인이며
실제 인증·발급·복구가 실행됐다는 증거는 아닙니다. 실제 W1의 현재 OIDC 인증과 서로 다른
share 2개는 보호 client로 입력합니다. 보관 위치 참조와 복구 계약도 값 없이 기록합니다.
아직 ceremony는 **NOT_RUN**이며 실제 값은 채팅으로 보내지 않습니다.

운영자는 CI와 독립 검토를 통과한 정확한 commit을 `P01_APPROVED_COMMIT`에 지정합니다.
아래 명령은 고정 HOME 저장소 identity와 전체 commit OID를 확인한 뒤 해당 blob을 운영자
전용 runtime 디렉터리에 복사하고 source hash를 검사합니다. Git 환경과 replacement object를
차단하고 stdlib-only helper는 시스템 Python의 isolated/no-site 모드로 실행합니다.
mutable checkout의 helper를 그대로 실행하지 않습니다. `XDG_RUNTIME_DIR`은
현재 운영자의 0700 runtime 디렉터리여야 하며, 해당 mount가 tmpfs인지 먼저 확인합니다.
매번 새 custody를 만들고 이전 attempt를 덮어쓰거나 재사용하지 않습니다.

```bash
unset LD_PRELOAD LD_LIBRARY_PATH PYTHONHOME PYTHONPATH
readonly P01_HOME_ROOT=/home/hyunyoun/data/hy-home.docker
test "$P01_HOME_ROOT" = "$(/usr/bin/realpath -e -- "$P01_HOME_ROOT")" || exit 1
test "$(/usr/bin/stat -c '%d:%i:%u' -- "$P01_HOME_ROOT")" = 64512:4338469:1000 || exit 1
test ! -L "$P01_HOME_ROOT/.git" || exit 1
test "$(/usr/bin/stat -c '%d:%i:%u' -- "$P01_HOME_ROOT/.git")" = 64512:4338470:1000 || exit 1
case "${P01_APPROVED_COMMIT:?}" in *[!0-9a-f]*) exit 1 ;; esac
test "${#P01_APPROVED_COMMIT}" = 40 || exit 1
P01_COMMIT="$(/usr/bin/env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 \
  GIT_CONFIG_GLOBAL=/dev/null GIT_NO_REPLACE_OBJECTS=1 /usr/bin/git \
  --git-dir="$P01_HOME_ROOT/.git" rev-parse --verify "$P01_APPROVED_COMMIT^{commit}")" || exit 1
test "$P01_COMMIT" = "$P01_APPROVED_COMMIT" || exit 1
readonly P01_COMMIT
readonly P01_RUNTIME_DIR="${XDG_RUNTIME_DIR:?}"
test -d "$P01_RUNTIME_DIR" || exit 1
test ! -L "$P01_RUNTIME_DIR" || exit 1
test "$P01_RUNTIME_DIR" = "$(/usr/bin/realpath -e -- "$P01_RUNTIME_DIR")" || exit 1
test "$(/usr/bin/stat -c '%u:%a' -- "$P01_RUNTIME_DIR")" = "$(/usr/bin/id -u):700" || exit 1
test "$(/usr/bin/findmnt -n -T "$P01_RUNTIME_DIR" -o FSTYPE)" = tmpfs || exit 1
P01_CLIENT_DIR="$(/usr/bin/mktemp -d "$P01_RUNTIME_DIR/p01-client.XXXXXX")" || exit 1
declare -p P01_CLIENT_DIR >>"$XDG_RUNTIME_DIR/p01-window.vars"
P01_SCRIPT_DIR="$P01_CLIENT_DIR/infra/03-security/openbao/scripts"
declare -p P01_RUNTIME_DIR P01_COMMIT P01_SCRIPT_DIR >>"$XDG_RUNTIME_DIR/p01-window.vars"
/usr/bin/install -d -m 0700 "$P01_SCRIPT_DIR" "$P01_CLIENT_DIR/infra/03-security/openbao/config/policies" || exit 1
set -C  # 기존 source 파일을 덮어쓰지 않습니다.
while read -r P01_SOURCE_HASH P01_SOURCE_PATH; do
  /usr/bin/env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null \
    GIT_NO_REPLACE_OBJECTS=1 /usr/bin/git --git-dir="$P01_HOME_ROOT/.git" \
    show --no-textconv "$P01_COMMIT:$P01_SOURCE_PATH" > "$P01_CLIENT_DIR/$P01_SOURCE_PATH" || exit 1
  printf '%s  %s\n' "$P01_SOURCE_HASH" "$P01_CLIENT_DIR/$P01_SOURCE_PATH" | /usr/bin/sha256sum -c - || exit 1
  /usr/bin/chmod 0400 "$P01_CLIENT_DIR/$P01_SOURCE_PATH" || exit 1
done <<'P01_SOURCE_MANIFEST'
b6b820b6561558020842376a06729f7663de3410188a544a6662024c4575568c infra/03-security/openbao/scripts/protected-maintenance.py
1ffe30c089361c7a7129bcce2407d08418222722aad2cba6e90804213b7c433b infra/03-security/openbao/scripts/protected-token-operations.py
05be43d5e2b9e8f067c2b81d4872666e89a1300fd2d21ecfee12db13e8aa5853 infra/03-security/openbao/scripts/protected-raft-snapshot.py
48ff7d0e0ee6e39b00c5105df5fa20891b70ac5e0e820715aad0b675ab028868 infra/03-security/openbao/scripts/protected-snapshot-archive.py
fd266cdd46d950cc8d6cc8704497fd1454bd51c47f1c4b071b24cfbf79bba724 infra/03-security/openbao/scripts/protected-snapshot-custody.py
32412b2a6f4d28f6e6105066dafd61d876443cd3160bb4feb120d7e175e3c6ef infra/03-security/openbao/scripts/protected-semantic-restore.py
b5aa92bdf528eb92993fc46061ead65b72bf71efe30182cca7cc5b5706ab396e infra/03-security/openbao/scripts/protected-semantic-execution.py
1aa658e05aee76127c7961abd218020fe6a319fd26253c78ecefb3ae99d4b622 infra/03-security/openbao/config/policies/backup-snapshot.hcl
52f47d119920ca8942a9d8a3f4ab352dbc05898a7fecabe8c02af0ec1a0e8cba infra/03-security/openbao/scripts/protected-renderer-roles.py
3a24759ae95ac6363353c9d5d28de787c75bb3c60e1af6bc4bbe34b103799a4e infra/03-security/openbao/config/policies/renderer.hcl
0ab86b526e0506b658184e0be20a9713a737262f921f1019f2f38609c394d3e5 infra/03-security/openbao/config/policies/renderer-issuer.hcl
a42f0b23de31acbeaf3c88761ebc2ba5a696fbdfcfe6667062ed864e9998a7a5 infra/03-security/openbao/config/policies/renderer-cleanup.hcl
fd277c7e09cd9a9ade1f1067664dafb39b6d91be524f285d6851919f2144847b infra/03-security/openbao/config/policies/operator.hcl
1693e2326f4aa74f5134490e6a1af8d2ed4727e11fb9d6167fec2634d4a493d4 infra/03-security/openbao/scripts/protected-restore-inputs.py
4a1052b4e888e5e0c5b025db7f6447f4719264343abc8f67e0c17fc3269e3a0f infra/03-security/openbao/config/renderer-issuer-token-role.json
bceb1e97853f173b5011f1af34033d01c07309e582137d0e67f85ae33b9eb17e infra/03-security/openbao/config/renderer-cleanup-token-role.json
e0dafc929bd037ef7910c04ee5ec343566ef7000ed7172032be3bfd95cabeb11 infra/03-security/openbao/config/renderer-role.json
ac23a2fa7dc72552d08f9232035f851b739a749745786046598b16475303b228 infra/03-security/openbao/scripts/owner-window.sh
152754095d8051fd6018ddb352b83ebb8d15ad2eb1599788ea6da28f2bf6dfaf infra/03-security/openbao/scripts/k8s-writers.sh
P01_SOURCE_MANIFEST
```

같은 셸에서 W1을 실행한다. 아래 단계는 모두 위 manifest로 복사·검증한
[window script](../../../../infra/03-security/openbao/scripts/owner-window.sh)를 쓰며, 실패하면
script만 끝나고 셸은 남는다. 단계 사이의 경로는 `$XDG_RUNTIME_DIR/p01-window.vars`에서 읽는다.

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" token w1        # OIDC 로그인 후 Copy token, UI 로그아웃 금지
bash "$P01_SCRIPT_DIR/owner-window.sh" check-token w1  # policy·TTL·path·meta와 attempt started:false 확인
bash "$P01_SCRIPT_DIR/owner-window.sh" w1              # share 2개 숨김 입력, 끝나면 share 파일 삭제
```

W1이 끝나면 W1c 전에 아래 W7 절의 이전 root 정리 블록을 실행한다(매 window).

각 setup 명령이 exit0인지 확인한 뒤 다음 명령으로 진행합니다. source hash 실패, CA 변경,
cluster 변경 또는 기존 attempt가 있으면 중단합니다. gateway 공개 CA hash와 IP는 이 HOME
대상의 2026-10-14 검증 입력이며, 내부 backend CA와 혼동하지 않습니다. 다른 host·CA에는
그 대상의 검토된 공개 입력을 다시 고정합니다. hash는 공개 인증서와 source만 대상으로 하고
secret hash는 기록하지 않습니다.

기대: exit0/`DELIVERED`, custody의 `root.token`은 0600이며 새 root로 인증됨. OTP/nonce,
encoded 응답과 root는 custody에 먼저 fsync되고 일반 출력에는 상태만 나옵니다.
operator token과 share 둘은 세 개의 보호된 0600 regular file FD로 넘깁니다. share는 숨김으로
읽어 tmpfs 파일로 열고 실행 뒤 지웁니다. secret-bearing 파일·FD·custody를 출력하지 않습니다.

중단: exit1/`BLOCKED`는 완료를 주장하지 않습니다. exit2/`INDETERMINATE`는 생성·완료 여부가
불확실하므로 custody를 그대로 보존하고 동일 attempt 상태부터 확인합니다. 새 ceremony나
재시작으로 덮지 않습니다. 미완료 attempt는 client가 보존한 자신의 nonce와 일치할 때만
취소하며, 완료·취소 불확실 응답은 운영자 복구로 넘깁니다. 다른 운영자가 동시에 ceremony를
실행하지 않아야 합니다. 메모리 소거, prompt 대기나 fsync 시간 상한은 보장하지 않습니다.
root를 읽어 채팅에 보내지 말고 W1c·W2·W7의 보호된 관리 입력으로만 전달합니다.

**W1c renderer 정책과 token role.** W1 root로 W3 전에 수행해 W3 snapshot이 이 설정을 담게
한다. W3a 격리 restore와 W5 helper는 HOME에 `renderer-issuer`·`renderer-cleanup` 정책과
token role이 있다고 가정한다. `operator.hcl`에는 `sys/policies/acl` 쓰기가 없어 root가
필요하고, W7이 root를 폐기하기 전에 끝나야 한다.
[renderer role helper](../../../../infra/03-security/openbao/scripts/protected-renderer-roles.py)는
위 manifest로 받은 고정 파일만 쓴다. 대상은 정책 `renderer`·`renderer-issuer`·
`renderer-cleanup`·`hy-home-operator`, token role `renderer-issuer`·`renderer-cleanup`,
AppRole `hy-home-renderer`이며 이 순서로 한 번씩 쓴다. role 읽기가 돌려주는 나머지
필드도 모두 기본값으로 함께 써서 남은 설정이 살아남지 않게 한다. 예외는 role 생성 때
정해지는 AppRole `local_secret_ids`뿐이다.
쓰기 전에 모든 대상의 현재 값을 읽어 custody의 `prior-state.json`에 남기고, 각 쓰기 직후
읽어 같은지 비교한다. 배포된 Agent가 RoleID를 쥐고 있으므로 AppRole이 없으면 쓰기 전에
멈춘다. credential을 만들거나 출력하지 않는다.

먼저 `plan`으로 같은 읽기만 하고 아무것도 쓰지 않는다. 그 `state.json`이 대상별 변경 여부를
보여 준다. `hy-home-operator`·`renderer`·AppRole이 바뀌면 `prior-state.json`의 현재 값과
고정 파일을 비교해 그 차이를 owner가 받아들인다고 Task에 기록한 뒤에만 `apply`한다.
이 정책들은 실행 중인 OIDC 세션과 현재 Agent token에 즉시 적용된다.

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" roles-plan   # 대상별 {path, changed}
bash "$P01_SCRIPT_DIR/owner-window.sh" roles-diff   # 바뀌는 정책의 HOME 원문(<)과 승인 파일(>) 차이
```

차이를 받아들였다면 `apply`한다.

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" roles-apply
```

`apply`는 `plan`과 따로 이전 값을 읽으므로, script가 두 `state.json`의 `prior_sha256`을
비교해 `prior:same`을 출력하고, 이어서 Agent health와 `.version` 파일 시각을 출력한다. `prior:DIFFERENT`면 exit1이며 plan과 apply 사이에 누군가 값을 바꾼 것이므로 owner가 그 차이를
다시 판단한다.

기대: `plan`은 exit0/`RENDERER_ROLES_PLANNED`, `apply`는 exit0/`RENDERER_ROLES_APPLIED`.
custody의 `state.json`은 값 없는 receipt이며 대상마다 경로, 이전·적용 값의 SHA-256, 변경
여부만 담는다. `prior-state.json`은 credential이 없지만 HOME의 정책 원문이므로, window를
닫기 전에 owner 전용 영구 저장소(tmpfs 밖, 문서 밖)에 복사한다. `renderer`나 AppRole이
바뀌었다면 바로 `docker inspect -f '{{.State.Health.Status}}' openbao-agent`가 `healthy`이고
렌더 결과가 그대로인지 확인한다(W0 기준선이 정지 상태면 렌더 결과만 본다). 아니면 W2로 가지 않고 window를 멈추며,
`prior-state.json`으로 되돌릴지는 아래 rollback 판단으로 넘긴다. W1c 뒤 window를 멈추면 W5 재발급까지 Agent가 낡은 결과를
유지하고 `OpenBaoAgentAuthFailure`가 날 수 있음을 받아들인다.

중단: exit1/`BLOCKED`는 쓰기 전이다. `plan`의 exit2는 읽기 실패이며 아무것도 쓰지
않았으므로 새 디렉터리로 다시 실행할 수 있다. `apply`의 exit2/`INDETERMINATE`는 일부
대상만 바뀌었을 수 있다.
custody를 보존하고 같은 명령을 다시 실행하지 않는다. `state.json`이
`RENDERER_ROLES_APPLIED`가 아니면 W2·W3를 시작하지 않는다. 되돌릴지 그대로 둘지는 root를
폐기하기 전에 정한다. 정책 복원과 새 token role 삭제에는 root가 필요하며, 검토된 rollback
명령이 없으므로 rollback은 **BLOCKED**이고 root는 window 안에서 그 결정까지 보존한다.
window가 멈추면 위 정리 규칙대로 server가 unsealed인 한 root를 폐기한다. 이 실행 결과는
HOME 증거이며 source 검증이 이를 대신하지 않는다.

**W1b unseal rekey는 하지 않는다.** 2026-10-14 owner 결정(SPEC-0242)으로 share를 host
백업에 포함하므로, rekey해도 새 share가 다시 백업에 들어가 노출이 줄지 않는다. 그래서 이
window에서 rekey와 그 PGP 준비를 하지 않는다. share 유출이 의심되면 별도 Spec과 별도
승인으로 rekey한다. 그때는 rekey가 이전 Raft snapshot을 여는 옛 share를 바꾸지 못한다는
점과 새 share를 host 파일과 보조 사본에 함께 반영하는 순서를 정한다.

**W2 snapshot token.** 위에서 검증한
[token helper](../../../../infra/03-security/openbao/scripts/protected-token-operations.py)를
사용합니다. 실제 root는 W1 custody의 보호된 FD로만 전달하며 argv에 넣지 않습니다.
고정 대상 `secrets/backup/openbao`는 2026-10-14 metadata 점검에서 UID/GID1000,
mode0700, device64512/inode5260267이었고 token과 issuance lock은 모두 없었습니다.
HOME root의 사전 기록은 device64512/inode4338469입니다. 실행 직전에 같은 대상을 다시
확인하며, 기대 identity를 임의의 다른 경로에서 계산해 이 인자에 넣지 않습니다.

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" w2
```

기대: exit0/`SNAPSHOT_TOKEN_DELIVERED`, 기존 파일을 덮지 않고 0600 single-link token이
고정 대상에 생성됩니다. helper가 root identity, 정확한 정책·capability, no-default-policy
720-hour orphan service token, 일반 secret403과 갱신·후속 lookup을 확인합니다.
정책이 없거나 알려진 이전 정책 또는 정확한 새 정책일 때만 진행합니다. 다른 정책,
기존 token/lock, 경로·권한·cluster 불일치에서는 중단합니다. exit2/`INDETERMINATE`는
응답·custody·lock을 보존하며 재발급하거나 파일을 지우지 않습니다. 단순 로컬 파일 삭제는
발급된 credential의 폐기가 아니므로 별도 실제 identity 확인 없이 보상 폐기를 하지 않습니다.

**W3 새 업그레이드 전 snapshot.** OpenBao에는 쓰기 정지 기능이 없으므로 승인된
Agent·관리 writer의 정지 범위, 정확한 container ID와 정지 전 상태를 먼저 기록합니다.
writer는 `openbao-agent`(`docker stop openbao-agent`), OIDC 운영자 로그인, hy-home.k8s의
OpenBao 로그인(External Secrets 등 Kubernetes auth)이다. 운영자는 W3 시작부터 W3a가 끝날
때까지 새로 로그인하지 않는다. W3a의 HOME 읽기 token은 W3 전에 받아 두고(restore는 시작할
때만 읽으므로 그때 유효하면 된다. `owner-window.sh token w3a`), W5·W7의 새 OIDC credential은 W3a 뒤에 만든다. hy-home.k8s
쪽 로그인 주체를 멈춘 방법과 확인을 값 없이 Task에 기록하며, 멈출 방법이 없으면 W3를 열지
않는다. 2026-10-21 관측에서 그 주체는 External Secrets controller 하나다(ClusterSecretStore
`vault-backend`, ExternalSecret 6개; POL-0085의 `eso-read-platform`). 그 Deployment는 Argo CD
Application `platform-external-secrets-operator`가, 그 위를 `root-platform`·`platform-cluster-config`와
ApplicationSet `apps-generator`가 관리하며 모두 `selfHeal`이 켜져 있다. 2026-10-22 window에서
Application의 자동 sync를 patch로 끄는 방법은 상위 관리자가 곧 되돌려 실패했다(ESO가 replica 1로
돌아옴). 다음 정지는 Docker 에이전트가 실행하지 않는다. 별도 클러스터 운영자가 창별 승인 뒤,
`k3d-hyhome`의 API endpoint·cluster identity·권한과 위 상위 관리자를 대조한다.
전체 GitOps 조정이 멈추며 기존 Kubernetes Secret은 남고 갱신만 멈춘다. 과거 축소의
unreviewed-step/실행으로 승인 기록은 과거 사실이며 다음 창의 검토·권한이 아니다.
현재 replica를 1/1/1로 가정하지 않는다.

아래 [K8s writer script](../../../../infra/03-security/openbao/scripts/k8s-writers.sh)는 실행 권한이 있는 외부 운영자용이다. 새 owner 전용 0700 증거 디렉터리를 사용하고,
세 대상의 UID·원래 desired/current/ready·selector를 저장한 뒤에만 정지한다. 원래 상태가
불안정하거나 selector에 matchExpressions가 있으면 임의 변환하지 않고 중단·검토한다.
`P01_K8S_WINDOW_APPROVED`는 그 창의 승인 참조이며 변수 설정 자체가 승인 증거는 아니다. `stop`이 출력한
`P01_K8S_STATE`는 이후 `check`·`restore`·`finish` 단계에 환경으로 넘긴다(W1 bootstrap 셸이면
`p01-window.vars`에도 남는다).

```bash
P01_K8S_WINDOW_APPROVED=<승인 참조> P01_EXPECTED_ES=<여섯 대상 JSON> P01_ES_SET_APPROVAL=<승인 참조> \
  bash "$P01_SCRIPT_DIR/k8s-writers.sh" stop     # P01_K8S_STATE=<경로>와 WRITERS_ZERO를 출력
```

두 Argo controller → ESO 순서다. snapshot **직전**에도 `k8s-writers.sh check`를 다시 실행하고
0일 때만 W3를 계속한다. 조회 오류·nonzero·UID 변경·pod 재등장 시 다음 쓰기를 멈추고
`k8s-writers.sh restore`로 실제 변경 요청을 보낸 대상만 ESO → ApplicationSet → Application
Controller 순서로 복구한다. 복구 함수의 nonzero를 별도 실패로 Task에 남기고 원래
UID/replica·남은 pod·담당자·수동 재개 조건을 기록한다. 자동 재축소·무한 대기는 금지한다.
셸 단절 때도 보존한 state와 변경 목록으로 같은 복구 순서를 사용한다. state/변경 목록을
창의 보호 기록에 보존하기 전 셸을 종료하지 않는다. Finish에서도 같은 복구 함수를 사용한다.
Agent와 해당 writer가 정지했음을 확인한 뒤 아래
[보호 snapshot helper](../../../../infra/03-security/openbao/scripts/protected-raft-snapshot.py)를
사용합니다. helper 자체는 writer를 정지하지 않습니다. 중단 시 writer 재개 여부는
기록된 window 상태와 복구 판단에 따르며 자동 재시도하지 않습니다.

`P01_SNAPSHOT_DIRECTORY`는 사전 선택한 새 절대 경로입니다. 기존 attempt, token 보관
디렉터리, HOME data 또는 source 디렉터리를 재사용하지 않습니다. 생성 명령은 기존 경로에서
실패해야 하며 helper가 canonical 경로·UID·0700·alias와 모든 산출물 이름을 다시 검사합니다.
아래 expected-version은 W0에 기록한 업그레이드 전 HOME 검사값이며 새 image pin이 아닙니다.
`w3`는 환경이나 `p01-window.vars`에 `P01_K8S_STATE`가 있으면 `k8s-writers.sh check`를 먼저
실행하고, 없으면 외부 운영자가 방금 `check`한 것을 확인한 뒤 셋째 인자 `--writers-checked`를
붙여야 실행한다. 이때 확인한 사람과 시각을 Task에 기록한다.

writer가 멈춘 것을 확인한 즉시, snapshot 전에
[restore input producer](../../../../infra/03-security/openbao/scripts/protected-restore-inputs.py)로
quiescence lease의 시작 시각을 남긴다. lease 디렉터리는 새 0700 경로이며 W3a가 끝날
때까지 보존한다.

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" lease-start
```

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" w3 <새 절대 경로> 2.6.2 # <!-- runtime-version-exception: migration — fixed observed pre-upgrade HOME version check -->
```

기대: exit0/`SAVED`, barrier-encrypted `raft-pre-upgrade.snap`과 값 없는
`raft-pre-upgrade.snap.receipt.json`, 모두 0600 single-link. helper는 보유 FD의 token을
검증·갱신하고 현재 cluster/version·TTL, bounded archive 구조·checksum·최종 inode를
확인합니다. snapshot과 receipt는 Linux `renameat2(RENAME_NOREPLACE)`로 게시하며
기존 파일을 덮지 않습니다. 해당 syscall이 없거나 저장 후 상태가 불확실하면 exit2/
`INDETERMINATE`로 남기고 lock·partial·final을 그대로 보존합니다. exit1/`BLOCKED`도
완료를 주장하지 않습니다. snapshot token·archive 내용·secret hash는 출력하지 않습니다.

helper receipt는 UTC·cluster/version·암호화 artifact SHA256·크기·파일 identity를 증명합니다.
원본 image와 data volume identity, writer 정지 구간, 독립 offsite 전달 결과는 별도 실제
window 증거로 붙입니다. 이 helper는 Restic 또는 offsite 전송을 실행하지 않습니다.
전체 backup은 [RUN-0021](../10-platform-and-backup/0021-backup-and-restore.md)의 기존 flow를
따릅니다. `latest`나 과거 snapshot을 새 성공으로 대체하지 않으며, 2026-10-13 snapshot은
새 artifact와 semantic restore 수용 전까지 보존합니다.

`SAVED` 뒤 같은 producer로 lease를 snapshot에 결속한다. lease는 운영자가 writer를 멈췄다고
확인한 시각을 기록할 뿐 정지를 스스로 증명하지 않는다. 시작이 receipt의 `saved_at_utc`보다
늦거나 30분 넘게 이르면 거부한다. 만료는 bind부터 세며 90분을 넘지 않는다. 출력의 lease
ID와 SHA-256은 contract가 쓴다.

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" lease-bind
```

**W3a 격리 semantic restore.** W4 전에 새 W3 artifact를 실제 빈 대상에서 복원하고
원본 cluster·canary 읽기·제한 권한 거부·renderer 재인증을 확인합니다. 먼저 이전 버전
image에 복원하고, 그 격리 대상만 candidate로 올려 두 share의 수동 unseal과 같은 검사를
반복합니다. 대상은 HOME data mount와 분리하고 edge/obs/egress를 연결하지 않습니다.
실제 artifact identity와 새 attempt·빈 대상 device/inode·소유권·용량·network·담당자·
시간/공간 한도·보존/정리 경계를 정한 stateful recovery contract가 필요합니다.
이전 attempt04의 FILE_USABILITY는 이 검사를 통과한 것이 아닙니다. 운영 도구·exact target이
준비되지 않았던 상태는 보존합니다. SPEC-0243의 2026-10-22 기록에서 `-05`는
INDETERMINATE, 후속 `-06`은 실제 semantic restore accepted다. 현재 소스 변경은 그
영수증을 새 hash에 승계하지 않는다. 다음 attempt의 실제 복구는 **NOT_RUN**이다. 합성 native rehearsal
또는 Git revert는 이 단계의 대체 증거가 아닙니다.

2026-10-15 독립 검토가 Agent 단계의 입력 chown 결함을 찾았고 native로
재현됐다. 그 수정 뒤 전체 `perform()` native 리허설이 결함 넷(sealed 상태의 login, 빈 token
생성 요청, 본문 없는 revoke 응답, Agent 파일 회수)을 더 찾았고, 고친 뒤 두 image에서
`accepted`로 끝났다. 그 수정의 재검토가 umask 077에서 읽을 수 없는 `tls/`와 실패 경로의
Agent 파일 잔여를 찾아 다시 고쳤고, 리허설은 restore를 umask 077에서 실행한다. 이 수정과 그 뒤
보완의 독립 IaC·보안 재검토가 통과했다(SPEC-0243). 이제 W3a 도구는 준비됐고, 실행은 W3
산출물·lease·W0의 HOME audit·mount 기록과 owner 승인을 기다린다. SPEC-0243 W2에서 client의 결함 다섯 가지를 고쳤다. server를
`/bin/bao`로 `-config` 없이 시작하던 것(D3), TTY 없이 거부되는 `operator unseal`과 인자 없는
`login`, 없는 `/usr/bin/stat`, capability 없는 root로 읽을 수 없던 0400 snapshot이다. 이제
image entrypoint와 `/openbao/config`·`/tmp` tmpfs, `write sys/unseal key=-`, `login -`,
`/bin/stat`, server 사용자와 0440 snapshot을 쓰며, 외래 share 확인은 threshold 미만 첫 share가
sealed로 남고 둘째 share가 `invalid key`로 실패해야 통과한다. 두 image 모두 합성 대상에서 init·unseal·
login·snapshot restore가 통과했다. SPEC-0243 W4가 네 입력의 producer를 더했다(아래).
W4 rehearsal은 preflight가 multi-arch 이전 image의 platform manifest ID를 비교해 W3a를 항상
멈추는 결함도 찾았고, 이제 local image ID와 `linux/amd64`를 비교한다. W3a는 W3 산출물·lease와 owner 승인이 있어야 연다.

입력 준비. renderer helper는 위 [Renderer SecretID Delivery](#renderer-secretid-delivery) 2단계의
installer로 `$operator_tools/$issuer_commit`에 먼저 설치한다. bundle·보안 receipt·candidate는
같은 승인 commit에서 만들므로 `$issuer_commit`과 `$P01_COMMIT`은 같아야 한다. producer는 Git을
보유 descriptor로 읽고 `^{commit}`을 확인하며, candidate는 그 commit의 Compose가 고정한 owned
image 하나다. `contract`는 snapshot archive를 검증하고 W3 receipt·lease·두 receipt의 revision과
대조한 뒤 restore client의 schema 검사를 통과해야만 파일을 남긴다.

```bash
issuer_commit=… operator_tools=… bash "$P01_SCRIPT_DIR/owner-window.sh" w3a-inputs
```

기대: `BUNDLE_WRITTEN`·`SECURITY_RECEIPT`·`CONTRACT_WRITTEN <sha256>`. exit1/`BLOCKED`는 기존
파일을 덮지 않는다. `w3a-inputs`를 다시 실행하면 이미 있는 bundle과 보안 receipt는 그대로 두고
contract만 다시 만든다(거부된 contract는 producer가 지운다). bundle이나 보안 receipt가 중간에
실패해 일부가 남았으면 그 경로를 지우지 말고 새 `lease-start`부터 새 attempt로 간다.
`$P01_INPUTS/quiescence-lease.json`은 그대로 둔다. lease가 만료됐거나 lease가 더는 이 snapshot을 덮지 못하면 새 W3 attempt(새 snapshot
디렉터리·새 W3b)로 간다. restore는 lease 만료보다 최소 17분 전에 시작한다(900초 실행과
60초 정리, 입력 시간). 그보다 늦으면 시작하지 않는다. 실패한 restore는 token 폐기·Agent
정지·확인·정리·재회수가 단계마다 별도 60초 시계로 돌아 최대 약 9분이 더 걸린다. lease는 시작 뒤
다시 보지 않고, 실패하면 W4를 열지 않으므로 시간표에는 영향이 없다. `$P01_INPUTS`의 contract·lease·
`lease.pending.json`·두 receipt는 credential이 없지만 W4 gate와 INDETERMINATE 분석의 증거이므로,
window를 닫기 전에 owner 전용 영구 저장소(tmpfs 밖, 문서 밖)에 복사한다.

2026-10-14에 고른 `p01-restore-20261014-05`는 2026-10-22 W3a에서 `INDETERMINATE`로 끝나
대상과 ledger를 보존했으므로 다시 쓰지 않는다. 원인은 렌더 값 비교였다. 템플릿은 값을
그대로 쓰는데 client가 끝의 줄바꿈을 지워, 줄바꿈으로 끝나는 canary가 일치하지 않았다.
후속 `/home/hyunyoun/storage/volumes/security/openbao/p01-restore-20261022-06`은
2026-10-22 12:40–12:42 accepted로 사용 완료됐다. `-05`와 `-06` 모두 재사용하지 않는다.
다음 실행은 새 attempt·빈 대상·정확한 부모 identity와 도구 상수를 변경·검토하고 새 승인
commit/manifest를 설치하기 전까지 BLOCKED다. 기존 숫자와 경로는 역사 증거로 남긴다.

검토된 [보호 복구 client](../../../../infra/03-security/openbao/scripts/protected-semantic-restore.py)는
위 W1 manifest의 두 복구 모듈을 같은 private 경로에 설치해 사용합니다. 공개 contract는
이 attempt·부모 identity·새 W3 snapshot/receipt의 정확한 SHA256과 파일 identity,
유효한 quiescence lease의 ID/바이트 SHA256, 승인된 candidate reference와 실제 Docker ID,
승인 commit에서 설치한 renderer 3파일·인접 receipt·bundle의 경로/해시와 보안 receipt의
해시를 결속합니다. contract와 실제 snapshot이 없으면 아래 호출을 실행하지 않습니다.
writer 정지 확인은 W3 저장 전부터 W3a 종료까지 별도로 유지해야 합니다.

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" w3a   # 성공(RESTORE_ACCEPTED)이면 w4 gate 표시를 남긴다
```

HOME 읽기 token은 W3 시작 전에 `bash "$P01_SCRIPT_DIR/owner-window.sh" token w3a`로 받아 둔다.

HOME 읽기용 현재 관리자 token·임시 root·서로 다른 원본 share 둘은 네 개의 서로 다른
보호 FD로 넘긴다. 임시 root는 W1 custody 파일에만 있어 숨김 prompt로 입력하려면 먼저 화면에
보여야 하므로 prompt 방식은 쓰지 않는다. HOME 읽기 token은 W3 전에 받은 tmpfs 파일(`p01-op-w3a.token`)에서 열고 정리 때 지운다. share 둘은
숨김으로 읽어 tmpfs의 0600 파일로 열고 실행 뒤 지운다. 값·capability·복구된 canary는 일반 로그에 남기지 않습니다.
effects 생성부터 공통 절대 900초 deadline을 세고 subprocess runner가 이를 강제합니다.
입력 prompt와 이전 관리자 lookup은 시계 시작 전입니다. 이후 로컬 syscall·canary GET은
runner가 중단시키지 않지만 경과 시간은 같은 예산을 소비하며 GET에는 별도 20초 abort가
있습니다. cleanup은 별도 시계를 사용합니다. 약 1초 간격 watcher가 64개 entry/1GiB를 감시하며
filesystem quota가 아닙니다. cleanup·token 폐기·Agent 파일 회수는 단계마다 별도 60초 안에서 돌며, cleanup은 성공적으로 확보한 정확한 생성
ID만 정리합니다. 이름·label은 ID를 확보하지 못한 create의 운영자 대조 자료이며 자동
cleanup 선택자가 아닙니다.
2026-10-26 source는 정확한 생성 ID를 제거할 때 `--volumes`로 이미지가 자동 생성한
익명 volume도 함께 제거합니다. 이 옵션은 명시적으로 연결한 named volume과 bind를
삭제하지 않으므로 복원된 Raft 대상·audit·Agent 경로의 기존 보존 계약은 유지됩니다.
격리 시험은 생성 직후 실제 `.Mounts`의 `Type=volume`인 `Name`을 기록하고, 모든
container와 시험이 직접 만든 named volume을 정리한 뒤 각 이름을 한 번씩 조회해
부재를 확인합니다. daemon·권한·불명확한 조회 오류는 부재로 인정하지 않습니다.
이 source 변경은 기존 승인 commit이나 설치된 도구를 바꾸지 않으며, 다음 운영 창은
새 해시 manifest와 정확한 `P01_APPROVED_COMMIT` 검토·승인·설치가 필요합니다.
`RESTORE_ACCEPTED`/exit0만 성공이며 `INDETERMINATE`/exit2에서는 대상·ledger를 보존하고
다시 실행하지 않습니다. exit가 0이 아니거나 실행이 끊기면(kill, 터미널 닫힘, 전원) `RESIDUE` 줄이
없어도 ledger 상태와 `/dev/shm/p01-restore-20261022-06-*`를 보고,
`docker ps -a`·`docker volume ls`·`docker network ls`를 `--filter label=hy-home.attempt=p01-restore-20261022-06`로
조회해 남은 container·volume·network를 값 없이 기록합니다. 익명 volume에는 이 label이
없으므로 label 조회만으로 정리 완료를 판단하지 않습니다. 끊긴 실행은 unseal된
`-candidate`와 계속 렌더하는 `-agent`를 남길 수 있습니다. 소유권을 확인한 정확한 생성
ID와 그 container의 실제 volume mount 이름을 보존한 뒤, 그 ID만
`docker rm --force --volumes`로 먼저 지우고 기록한 volume 이름마다 부재를 확인합니다.
생성 ID나 mount 기록이 없으면 이름을 추정해 지우지 않고 owner가 정합화합니다.
stderr에 `RESIDUE: /dev/shm attempt directory retained`가 나오면
`/dev/shm/<ATTEMPT>-*`에 복원 key·snapshot 사본이나 렌더 값이 남았을 수 있습니다. 지우지
말고 그대로 두며, owner가 `sudo ls -laR`로 이름·소유자·크기만(내용은 보지 않음) 값 없이
Task에 기록한 뒤 `sudo rm -r`로 지웁니다. 재부팅해도 `/dev/shm`은 비워집니다. 이전 버전 복원 후 candidate와 Agent를 같은 격리 data에 연결하며
HOME root 폐기나 HOME server 교체는 이 client가 수행하지 않습니다.

**W3b 정확한 artifact의 독립 보관.** W3 snapshot과 그 receipt를 선택한 독립 off-host
대상으로 전달하고, 양쪽에서 두 파일의 정확한 bytes·hash와 보관 위치 참조를
값 없는 receipt로 결속합니다. share와 CA key는 host와 host 백업에, BKP-003은 장소 A에
있다는 1인 관리자 custody 기록(5단계)도 확인합니다. 준비됐다는 운영자 확인만으로 이 전달을 완료 처리하지 않습니다.
standalone helper와 RUN-0021의 별도 full backup은 이 W3 경로를 자동으로 복사하지 않습니다.
운영자는 기존 Cloudflare R2 Restic 저장소를 이번 snapshot·receipt 보관 대상으로 선택했다.
[offsite entrypoint](../../../../infra/09-platform-ops/restic/offsite.sh)의 `artifact`는 두
파일만 tag `hy-home-openbao-w3`, host `hy-home-openbao-window`로 R2에 저장하고, 곧바로 R2에서
두 파일을 다시 읽어 SHA-256을 로컬과 비교한다. 지우거나 다시 시도하지 않는다. 먼저 읽기
전용 `snapshots --no-lock`(lock 파일도 쓰지 않음)으로 저장소에 닿는지 확인한다.

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" w3b
```

기대: 마지막 줄이 `{"state":"W3B_STORED","snapshot_id":...,"files":[...]}`이고 두 파일의
`sha256`이 W3 receipt와 같다. 이 줄이 값 없는 W3b receipt이며 Task에 그대로 남긴다.
중단: exit64는 입력 누락이나 symlink, exit65는 R2 저장소 문제·snapshot ID 없음·바이트
불일치다. exit66은 R2 상한 거부로 아무것도 올리지 않았다는 뜻이다. 다시 시도하지 않고 W3b와
이후 단계를 다음 window로 넘긴다. 이때 stdout 마지막 줄은 receipt가 아니라
`R2 repository size: N bytes`다. `restic backup` 자체가 실패하면 restic의 종료 코드(1·3·10-12 등)로 끝난다. 0이
아닌 종료는 모두 W4를 막는다. R2에 남은 배타 lock이 있으면 `cmd unlock`은 거부되므로 W3b를
멈추고 다음 window로 넘긴다. 불일치 뒤 다시 실행하면 새 snapshot이 하나 더
생길 뿐 이전 것은 지워지지 않는다. 전체 repository copy를 이번 두 산출물의 전달 성공으로
대체하지 않는다. `artifact`는 snapshot의 SHA-256이 W3 receipt에 적힌 값과 다르거나 입력이
비어 있으면 exit64로 멈춘다. 이 snapshot은 자기 host·tag 묶음에 혼자 있어 월간
`forget-prune`이 지우지 않으므로, W4 수용 뒤 R2에서 언제 지울지는 owner가 따로 정한다.
W4는 W3a semantic restore와 이 W3b receipt가 모두 수용된 뒤에만 실행합니다.

**W4 server 업그레이드와 수동 unseal.**

중단 gate: 이번 W3 snapshot/receipt identity에 결속된 독립 off-host 보관 receipt와 W3a
semantic restore 중 하나라도 없으면 아래 server 재생성 명령을 실행하지 않습니다. 재생성
전후에 `docker inspect openbao`의 `/openbao/data` mount 이름·source와 server 안에서 본 그 mount의
`stat -c '%d/%i'`(기록값 device2064/inode115612005)로 실제 Raft mount identity를 기록하고, Compose가 volume 설정이 달라 다시 만들지 묻는 prompt에는 절대 동의하지
않고 중단합니다.

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" w4 2064/115612005   # 기록값과 전후 identity 비교, share 두 번 숨김 입력, bao status
```

`w4`는 `w3a`의 수용 표시와 `w3b`가 남긴 W3b receipt(`$P01_INPUTS/w3b-receipt.json`)가 없으면
시작하지 않는다. 재생성 전 identity가 인자와 다르거나 재생성 전후가 다르면 멈춘다. 인자는 W0에
`docker exec openbao /bin/stat -c '%d/%i' /openbao/data`로 server 안에서 다시 확인한 값이며,
host source의 기록값과 다르면 W4를 열지 않고 검토한다.

기대: 새 image로 재생성, Raft mount identity 불변, threshold 뒤 `Sealed false`.
중단: mount identity 변경, unseal 실패, cluster ID 변경, audit backend 실패.
rollback 규칙은 fix-forward다(2026-10-14 owner 결정, SPEC-0243 W6). 새 버전 데이터에 이전
image를 붙이지 않는다(in-place Raft downgrade 금지). W4가 실패하면 새 owned image에서 원인을 고친다.
window 안에 끝나지 않으면 server를 sealed 또는 정지 상태로 두고, consumer는 이미 렌더된
파일로 계속 동작하며, 남은 단계는 다음 window로 넘긴다. 유일한 예외는 Raft 데이터 손상처럼
새 owned image에서 고칠 수 없는 경우다. 그때만 HOME을 보류하고 @buenhyden에게 반환하며, 별도 승인으로
W3 snapshot을 이전 버전 image의 빈 대상에 복원하는 경로를 연다(아래 Rollback or Recovery).
지금의 restore 도구는 격리 target-05에 고정돼 있으므로, HOME을 복원된 volume으로 바꾸는
절차는 그때 따로 검토한다.

**W5 Agent 업그레이드와 재발급.** server가 unsealed이고 health가 통과한 뒤에만
`owner-window.sh w5-create`로
컨테이너만 만든다(journal이 없을 때 helper는 Agent가 멈춰 있기를 요구한다). 그다음 위 [Renderer SecretID Delivery](#renderer-secretid-delivery)로 wrapped
SecretID를 다시 전달한다. 기대: Agent `healthy`, 렌더 bytes와 version 일치. 중단:
재인증 실패, health 실패. Agent는 server보다 앞서 rollback하지 않는다.

이 재생성으로 SPEC-0239 Agent telemetry도 배포된다(2026-10-14 owner 결정). Compose와
`agent.hcl`이 이미 `metrics_only` listener(8100)와 `obs_net`을 담고 있으므로 따로 바꿀 것은
없다. Agent가 `healthy`가 된 뒤 Prometheus의 `openbao-agent` scrape를 확인한다.
Prometheus는 2026-10-20 SEC01 rollout에서 Compose 고정 image(`v3.15.0`, digest `efd719c9`)로 이미 <!-- runtime-version-exception: history — 2026-10-20 rollout에서 관찰한 Prometheus image 버전이며 Compose가 pin을 소유함 -->
다시 만들어져 `/etc/prometheus/openbao-ca.pem` mount를 갖고 있다(SPEC-0245 TSK-0001). W0에서
`docker inspect prometheus`로 image가 Compose pin과 같고 그 mount가 있는지만 확인하며, 이 단계에서
Prometheus를 다시 만들지 않는다. 이전 image로 되돌리는 overlay는 v3.15.0이 쓴 TSDB를 낮은 버전으로
여는 다운그레이드가 되므로 두지 않는다. 확인이 어긋나면 이 부분은 **BLOCKED**다. 기대: `up{job="openbao-agent"}`이 1, `OpenBaoAgentMetricsScrapeFailing`과
`OpenBaoAgentAuthFailure`가 조용하다. 중단: scrape 실패가 이어지면 Agent listener와 `obs_net`
연결을 먼저 확인한다. Prometheus를 다시 만들거나 되돌리는 것은 Agent 재인증과 무관하다.

Gatus도 W4 뒤 OpenBao를 HTTPS로 보고 내부 CA를 요구하므로 CA mount가 없으면 W4 이후에도
계속 경보를 낸다. Compose는 이미 Gatus의 CA mount를 선언한다. Gatus image는 digest 고정이 아닌
local build tag `hy/gatus:local`이므로, 실행 중 컨테이너의 image ID가 지금의 `hy/gatus:local`
ID와 같고(2026-10-14 관측에서 같았다) 다른 설정 차이가 없을 때만
`docker compose --profile obs up -d --no-deps --no-build --pull never --force-recreate gatus`로
다시 만든다. 다르면 Gatus override는 없으므로 이 부분은 **BLOCKED**이며 그때까지의 Gatus
경보는 W0에서 정한 대로 처리한다.

**W6 audit와 logrotate 검증.** W0에서 등록·parser 검증을 끝낸 규칙을 사용합니다.
window 안에서는 새 server의 `openbao-audit` mount와 `audit.json`(0600, UID100/GID1000), 정확한
device·inode·용량, 실제 audit 요청 전후 크기 성장만 확인합니다. 새 파일은 `daily`·`maxsize`
조건 때문에 첫 확인에서 회전하지 않고 `logrotate -f`는 증거가 아니므로, 첫 자연 회전 뒤
새 inode의 성장과 회전된 inode가 더 커지지 않는지는 window 뒤 관찰로 확인하고 Task에
기록합니다. `SIGHUP` 전달 성공만으로
재개방을 완료했다고 보지 않습니다. 실패하면 audit device를 끄거나 `copytruncate`로
바꾸지 않고 공간·권한과 재개방을 복구합니다. 이전 파일을 계속 쓰는 상태에서는 다음
rotation을 성공으로 처리하지 않습니다.

**W7 사후 점검과 root 폐기.** renderer 재인증, consumer 읽기(Keycloak·Grafana 렌더 결과
일치), `OpenBaoSealed` 등 기존 경보가 조용한지, `up{job="openbao"}`를 확인합니다. 다음
backup 단위의 OpenBao snapshot 성공은 window 뒤 관찰입니다. W7 뒤 backup timer와
hy-home.k8s 로그인 주체를 아래 Finish대로 복구·검증하고, 경보를 기록한 뒤 silence를 지웁니다.

**Finish — writer 복구와 ESO 수용.** W3의 저장된 UID/replica와 변경 목록으로
`k8s-writers.sh finish`가 writer를 복구하고 nonzero면 Finish FAIL로 남긴다. 원래 0이던 대상은
0으로 유지한다. Store Ready·실제 refresh·Application 상태까지 통과해야 완료다.
2026-10-22 12:54–12:56의 ESO lookup/read403 원인은 UNKNOWN이며 cache/token 재사용은
검증되지 않은 가설이다. W5 typed-JSON403과 별개다. 복원 뒤 대부분 회복했으나
`argocd-external-valkey`는 13:02:54 force refresh 뒤 회복했다는 Task 기록을 재사용한다.

현재 정확한 여섯 namespace/name은 이 저장소 기록만으로 확정할 수 없다. 외부 운영자는
읽기 전용 discovery로 Store binding·refreshPolicy/refreshInterval과 설치 ESO/Argo CD
버전·cache 옵션·auth role/SA/namespace/audience를 확인한다. 아래 출력에는 Secret data가 없다.
latest 공식 문서는 참고이며 설치 버전의 지원 증거가 아니다.
cache/auth의 세부 launch 값은 보호된 운영자 preflight에서 확인하고 값 없는 판정만 기록한다.

```bash
bash "$P01_SCRIPT_DIR/k8s-writers.sh" discover
```

discovery를 자동 승인 목록으로 사용하지 않는다. 운영자가 의도된 **정확히 여섯**
namespace/name·`ClusterSecretStore/vault-backend` 연결을 검토해 `P01_EXPECTED_ES`의 보호된
JSON 배열로 확정하고 창별 승인 참조를 남긴다. 각 행 형식은
`{"namespace":"확인한 namespace","name":"확인한 name","store":{"kind":"ClusterSecretStore","name":"vault-backend"}}`다.
누락·중복·집합 변경 또는 여섯 이름 미확보는 W3/Finish만 BLOCKED이며 이름을 만들지 않는다.

`finish`는 writer 복구 전에 Finish 기준시각을 state에 저장하고, 복구한 뒤 gate를 한 번 실행한다. query 실패는
즉시 실패이며 stale Ready는 통과시키지 않는다. 원래 0 replica이거나 설치된 정책이 새
refresh를 허용하지 않으면 그 자원의 복구 판정을 별도로 인계하고 성공으로 표시하지 않는다.

```bash
P01_K8S_STATE=… P01_EXPECTED_ES=… P01_ES_SET_APPROVAL=… bash "$P01_SCRIPT_DIR/k8s-writers.sh" finish   # ESO_GATE_PASS 또는 exit1
```

첫 gate 실패는 조사 대상이다. API/Store/controller 실패와 ES stale/오류를 구분한다.
원문 요청의 원인 미확정 시 동일 Store의 전체 여섯 대상 강제 갱신과 아래 현행
실패 대상 한정 절차는 동등한 수용조건으로 입증되지 않았다. 외부 ESO 운영자는
정확한 여섯 대상, 각 `refreshPolicy`와 설치 CRD·버전의 지원, 현재 갱신 신선도,
불필요한 재동기화의 영향·비용을 확인한 뒤 전체 여섯 대상 또는 실패 대상 한정 중
허용할 범위를 결정하고 기록한다. 그 결정 전에는 아래 명령의 기본 대상 집합을
넓히지 않으며, 대상 집합 결정이 실제 annotation 실행 승인을 대신하지 않는다.
Store와 writer rollout이 정상이고 **설치 버전**의 manual refresh·각 대상 refreshPolicy가
지원됨을 확인한 경우에만, 외부 운영자의 별도 forced-refresh 승인으로 실패한 기대 대상
하나씩 다음 명령을 실행한다. `CreatedOnce`, Periodic의 0간격, 미지원 정책/버전은 중단한다.
권한 확대·Secret 삭제·전체 accessor 폐기는 이 fallback에 포함하지 않는다.

```bash
P01_FORCE_REFRESH_APPROVAL=<승인 참조> P01_K8S_STATE=… P01_EXPECTED_ES=… P01_ES_SET_APPROVAL=… \
  bash "$P01_SCRIPT_DIR/k8s-writers.sh" force-refresh <namespace> <name>   # 대상당 한 번만, finish의 writer 복구 성공 뒤에만
```

강제 갱신은 대상당 최대 1회다. 승인된 실패 대상의 annotation이 끝난 뒤 다음으로
동일 gate를 최대 6회·10초 간격·180초 deadline 안에서 재확인한다. API 오류(exit2)는
즉시 중단하고 Ready/시각/집합 불일치(exit1)만 유한 재확인한다.

```bash
P01_K8S_STATE=… P01_EXPECTED_ES=… P01_ES_SET_APPROVAL=… bash "$P01_SCRIPT_DIR/k8s-writers.sh" finish-wait   # ESO_GATE_PASS
```

 annotation 성공은 인수가 아니다. timeout·계속된403·
집합 변경·stale refreshTime은 Finish FAIL로 남기고, 실패한 namespace/name·Store·조건·
시각·실행자·다음 검토 입력을 Task에 값 없이 기록한다. 새 축소·무한 재시도는 하지 않는다.
이 runbook의 command syntax/합성 gate 확인은 실제 cluster recovery나 ESO 원인 재현이 아니다.
독립 throwaway Kubernetes/TokenReview·합성 SA/KV를 갖춘 재시작 대 snapshot restore 비교 환경이
없으므로 실제 ESO/provider cache 재현은 NOT_RUN이다.

[ESO ExternalSecret/manual refresh](https://external-secrets.io/latest/api/externalsecret/),
[refreshTime 판정](https://external-secrets.io/latest/introduction/faq/),
[Argo 자동 sync의 상위 관리자 영향](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)와
[Kubernetes bounded rollout](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_status/)을
2026-10-22 확인했다. 실제 설치 버전 일치는 외부 운영자가 창 전에 확인한다.

server가 sealed라 window가 root를 폐기하지 못하고 끝나면 만료 없는 root가 OpenBao에 남는다
(unsealed인데 OIDC가 안 되면 위 `cleanup --keep-root` 규칙을 따른다). W1 custody는 `$XDG_RUNTIME_DIR`
tmpfs에 있고 Linger나 남은 로그인 세션 때문에 재부팅 전까지 남으며, 저장소 UID로 도는 모든 process가 읽을 수 있다. 값은 영구 저장소로
옮기지 않는다(backup 대상인 `secrets/` 포함). 위 정리 명령으로 모든 custody·secret 파일을
`shred -u`해 값을 아무도 갖지 않게 하고, 폐기하지 못한 사실만 값 없이 Task에 남긴다. accessor도
기록하지 않는다. 모든 window는 W1 직후, W1c·W3 전에 아래로 이전 root를 찾아 폐기한다(W1 exit2로
누구도 갖지 않은 root가 생겼을 수도 있으므로 기록과 상관없이 매번 한다. W1의 10분 안에 들어가며,
W3 뒤에는 쓰기라 하지 않는다). accessor 하나마다 `docker compose exec`가 한 번 돌아 시간은
accessor 수에 비례하며 아직 측정하지 않았으므로, T+15 멈춤 기준은 그대로 적용한다. W0에서
`command -v jq`를 확인한다. 이 정리 블록이 실패하면 오류를 보고 T+15 전까지 한 번 다시 실행해도
된다(이미 폐기한 accessor는 없는 것으로 넘어가며, 두 실행의 `revoked` 수를 더해 기록한다). 폐기한 개수와 다시 센 나머지
root 수(0이어야 한다)를 값 없이 Task에 기록한다. 새 root를 helper가 아닌
CLI에 넘기는 유일한 예외이며, 값은 변수로만 넘겨 argv에는 이름만 남고 출력은 화면에만 둔다:

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" root-sweep   # revoked=<n>, remaining=0
```

server가 sealed면 이전 root는 unseal 전까지 쓸 수 없다. 임시 root는 이 예외 외에는 W1c·W2·W7의
보호된 관리 입력으로만 사용합니다. W4 수동 unseal에는 지정된 두 share가 필요합니다.

window 안에서 W1c rollback 판단이 열려 있는 동안은 root를 폐기하지 않습니다(W1c 참조). window가
멈추면 위 정리 규칙이 우선합니다.
W7의 `revoke-root`는 root FD와 별도의 현재 OIDC operator FD를 요구합니다. 운영자는
승인된 로그인 절차로 새 OIDC credential을 받아 `owner-window.sh token w7`로
`$XDG_RUNTIME_DIR/p01-op-w7.token`(0600·single-link)에 둡니다(정리 glob에 들어간다). 이 파일은
tmpfs 안에 있고, W7이 끝나거나 중단되면 window 정리의 `cleanup`이 그 token을 `revoke -self`로
폐기한 뒤 `shred -u`로 지웁니다. 결과는 값 없이 Task에 기록합니다.
이전 W1의 성공 기록을 현재 관리자 접근 확인으로
대체하지 않으며, auth 파일을 자동 검색하거나 값을 출력하지 않습니다.

```bash
bash "$P01_SCRIPT_DIR/owner-window.sh" token w7
bash "$P01_SCRIPT_DIR/owner-window.sh" check-token w7   # renewable, ttl 600초 이상
bash "$P01_SCRIPT_DIR/owner-window.sh" revoke-root
```

기대: exit0/`ROOT_REVOKED_OPERATOR_HEALTHY`만 완료입니다. helper가 서로 다른 실제
FD inode와 token bytes, 정확한 renewable service OIDC 정책과 600초 이상 TTL을 폐기
직전과 직후에 확인하고 root lookup403을 확인합니다. 관리자 접근이 준비되지 않으면
POST 전에 중단합니다. 폐기 후 확인이 불확실하면 exit2이며 custody를 보존하고 같은
mutation을 재시도하지 않습니다. 더 이른 단계에서 window를 접을 때도 먼저 현재 복구
접근을 확인한 뒤 이 절차로 폐기합니다.

**W8 cold boot.** 별도 승인과 별도 window에서 host를 재시작하고, 수동 unseal, Agent
재인증, 위 W7 점검을 반복한다. cold start 시뮬레이션은 실제 재부팅 증거가 아니다.

**window 뒤에 남는 것.**

- W3a는 window 뒤 잔여가 아니라 W4 전 필수 gate입니다. 도구는 리허설·검토를 마쳤고, 새
  attempt의 W3 산출물·빈 대상 입력이 없으면 HOME upgrade는 계속 미실행입니다.
- consumer와 ACL 선택(위 10단계, P06).

### P06 Consumer Migration Boundary

이 Runbook은 [copy runtime](../../../../scripts/lib/ops/openbao_consumer_migration.py)과
[HTTPS transport](../../../../scripts/lib/ops/_openbao_copy_transport.py)의 운영 실행 경계를 소유합니다.
두 모듈은 controller가 현재 trusted user 또는 native authorization origin을 확인하고
고정 P02·P01·P03·P04 입력에 결속한 뒤에만 실행하는 runtime primitive입니다.
직접 library를 호출했다는 사실은 실행 승인이 아닙니다. 공개
`scripts/operations/openbao-consumer-migration.py` CLI는 validate-only이며 production catalog
adapter·controller factory·runtime copy CLI는 아직 제공하지 않습니다. 실제 private/native copy,
consumer 렌더·pilot·authority 전환·복구·삭제·회전은
[P06 Task](../../../03.specs/0204-service-integration-security-and-operations/tasks/tsk-0014-p06-openbao-consumer-migration.md)의
별도 입력·검토·수용 전까지 **NOT_RUN**입니다. source/unit 통과로 이 경계를 완료 처리하지 않습니다.

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

## Failure and Recovery

### Rollback or Recovery

maintenance window의 W4 실패는 fix-forward가 규칙이다([W4](#maintenance-window-plan)의 rollback
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

- [운영 인덱스](../../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
