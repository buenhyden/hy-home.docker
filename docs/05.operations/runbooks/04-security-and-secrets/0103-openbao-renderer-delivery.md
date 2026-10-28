---
title: "OpenBao Renderer SecretID Delivery"
version: "0.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-28"
layer: "operations"
artifact_id: "RUN-0103"
parent_ids:
- "POL-0085"
created: "2026-10-28"
---

# OpenBao Renderer SecretID Delivery

## Overview

이 런북은 OpenBao Agent의 renderer AppRole SecretID를 wrapping으로 다시 전달하고 Agent를 다시 시작하는 절차를 다룬다. `agent.hcl` 변경 반영, Agent token 유실, W5 재발급에 쓴다. 공통 상태 점검과 기동·중지는 [RUN-0085](0085-openbao.md)가 소유한다.

## Trigger

Agent 설정이 바뀌어 다시 시작해야 하거나, Agent가 재인증하지 못하거나, maintenance window의 W5에서 SecretID를 다시 전달할 때 사용한다.

## Prerequisites

OpenBao가 initialized·unsealed이고, 승인된 issuer helper가 operator 전용 디렉터리에 설치돼 있으며, 현재 OIDC operator credential을 받을 수 있어야 한다. issuance journal이 `complete`가 아니면 새로 발급하지 않는다.

## Procedure

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

### Renderer delivery from an existing integration session

기존 RUN-0096 세션을 사용할 때도 위 Renderer SecretID Delivery와 같은 제한 발급자와
response wrapping을 사용한다. raw `-field=secret_id` 전달과 root UID로 volume을 고치는
옛 대안은 현재 경로가 아니다. wrapping helper 하나만 사용하고 중복 발급하지 않는다.
기존 세션·root 폐기·integration receipt는 과거 관찰이며 새 P01 결과가 아니다.

## Verification

`issue rc=0`, Agent `healthy`, 렌더 파일의 mode와 KV version 일치, journal `complete`를 확인하고 값 없이 Task에 기록한다.

## Failure and Recovery

### Rollback or Recovery

전달이 실패하면 journal·completion witness·보호된 snapshot과 관리 인증을 보존한다. 재시작을 반복하거나 오래된 sink를 성공으로 처리하지 않고, 같은 journal로 정합화한 뒤에만 다시 발급한다.

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
