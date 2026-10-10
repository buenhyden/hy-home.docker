---
title: "Release Management Runbook"
version: "1.3.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0009"
created: "2026-06-04"
---

# Release Management Runbook

## Overview

main 대상 릴리스 준비 PR과 승인된 SemVer 게시 절차를 소유한다. 일반 후보
QA는 PR의 changed-profile 한 번으로 검증하며 릴리스에서 다시 전체 QA를
실행하지 않는다. 배포·secret·HOME 복구 수용은 해당 운영 Task의 별도 작업이다.

## Trigger and Preconditions

- main 대상 준비 PR에서 `CHANGELOG.md`의 실제 변경을 작성한다. 개발 push마다
  자동 생성하거나 이미 게시된 릴리스 이력을 덮어쓰지 않는다.
- `.cz.toml`의 Commitizen 문법과 [Git 정책](../../../.agents/governance/git-workflow.md)을 따른다.
- 최종 후보의 원격 QA, 독립 리뷰, 실제 main 통합과 revision을 확인한다.
- 게시할 정확한 SemVer와 main commit, 대상 저장소, 승인 및 실패 복구 소유자를
  실행 Task에 기록한다. 이 런북의 명령 예시는 실행 승인이 아니다.
- 기존 `main-current`와 과거 릴리스 ref는 역사로 보존한다. moving tag 생산자는
  폐기하며, 소비자는 main의 immutable SHA 또는 SemVer Release를 사용한다.

## Procedure

1. release candidate branch와 비교할 base를 확인하고 정확한 두 commit SHA를 기록한다.

   ```bash
   git status --short --branch
   git branch --show-current
   ```

2. release/tag 판단 전에 기록한 base/candidate 사이의 전체 변경을 확인한다. 작업 트리 diff만으로 이미 commit된 변경을 누락하지 않는다.

   ```bash
   # RELEASE_BASE와 RELEASE_CANDIDATE에는 앞에서 확인한 commit SHA를 지정한다.
   git diff --stat "$RELEASE_BASE" "$RELEASE_CANDIDATE"
   git diff --check "$RELEASE_BASE" "$RELEASE_CANDIDATE"
   git diff --check
   ```

3. 선택된 검사와 필요한 도구·예산을 확인한다. 집중 authoring 검사와 원격
   후보 aggregate 결과는 서로 다른 목적이다. 같은 입력의 leaf를 다시 실행하지
   않고 Task의 실제 PR base/head/merge revision과 결과를 확인한다.

   ```bash
   python3 scripts/validation/run-ci-gate.py --profile changed --explain
   ```

4. 준비 PR에서 Keep a Changelog의 dated SemVer heading과 실질적인 변경 내용을
   작성한다. 버전 문자열이 본문 어딘가에 있다는 이유만으로 수용하지 않는다.
   선택된 후보 검사에 포함되면 다음 read-only 검사를 별도로 반복하지 않는다.

   ```bash
   python3 scripts/operations/release.py validate --changelog CHANGELOG.md
   ```

5. PR과 승인된 코드가 main에 통합되면 정확한 commit과 아직 존재하지 않는
   `v` + SemVer를 확인한다. `generate-changelog.yml`의 main-only 수동 dispatch가
   유일한 태그·Release 생산자다. 태그를 따로 push하거나 다른 writer를 추가하지
   않는다. 실제 dispatch에는 정확한 version·repository·commit의 별도 승인이 필요하다.

6. 생산자는 main ancestry와 CHANGELOG를 확인한 후 create-only tag를 만든다.
   draft Release에 `CHANGELOG.md`, `SOURCE_REVISION.txt`, `SHA256SUMS`를 붙이고
   tag SHA와 업로드 manifest를 확인한 후 게시한다. 필요 자산을 모두 올린 뒤
   Release를 게시한다. immutable 설정을 사용하는 경우에도 이 순서를 지키고,
   실제 게시 후 draft 여부·tag SHA·자산 digest·immutable 상태를 read-back한다.
   설정 활성화는 별도 승인 대상이며 소스만으로 적용됐다고 표시하지 않는다. GitHub 공식
   [릴리스 관리](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)와
   [immutable release 계약](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)을 따른다.

7. 실패하면 재시도·force update·태그 삭제를 자동으로 하지 않는다. 생성된 tag나
   draft가 있다면 그 정확한 대상과 자산 상태를 Task에 남기고 소유자에게 복구를
   요청한다. 이미 게시된 버전은 수정하지 않는다. 실제 배포·backup·rollback 수용은
   해당 service Task에 별도로 기록하며 Release 게시를 배포 성공으로 표현하지 않는다.

### Optional Compose service observation

이 runbook은 다음 기존 운영 명령의 수동 실행 경계를 유지한다. 일반 Release의
추가 필수 gate가 아니다. 입력·환경·권한은 해당 service Task에서 먼저 승인한다.
준비 파일만 확인하는 경로는 다음과 같다.

```bash
bash scripts/validation/validate-docker-compose.sh --preflight
bash scripts/operations/check-compose-core-readiness.sh --preflight
```

승인된 Task가 구조 렌더나 선택한 daemon의 실제 관측을 요구할 때만 기본 경로를
실행한다. 렌더는 임시 환경·dummy secret을 만들 수 있고 readiness는 live
Docker 관측이므로 같은 결과나 승인으로 취급하지 않는다. 각각의 결과와 입력을
해당 Task에 남기며 구조 PASS를 배포·복구 수용으로 승격하지 않는다.

```bash
bash scripts/validation/validate-docker-compose.sh
bash scripts/operations/check-compose-core-readiness.sh
```

### Optional service delivery rehearsal

아래 재사용 가능한 Docker 운영 예제는 해당 service의 승인된 변경에만 적용한다.
문서·commit·일반 릴리스의 필수 gate가 아니며 후보 QA와 live 운영 수용을 합치지 않는다.

1. `sample-web-service`의 local promotion/rollback 계약을 확인할 때는 먼저
   Docker를 시작하지 않는 fixture-only preflight를 실행한다.

   ```bash
   bash scripts/operations/rehearse-sample-service-delivery.sh preflight --task-id sample-delivery --baseline-verdict examples/operations/sample-service-delivery/verdict.baseline.accepted.json --candidate-verdict examples/operations/sample-service-delivery/verdict.candidate.accepted.json
   ```

   `evidence=fixture-contract-only`, `readiness=passed`,
   `recovery_boundary=passed`, `compose=passed`, `ports=18080,18081`이 모두
   있어야 한다. Fixture verdict는 실제 실행 승인이 아니다.

   supply-chain 준비는 fail-closed를 유지한다. 기본 점검은 fixture-only 또는
   preflight이며 network를 쓰는 Grype seed는 추적된 별도 승인 범위에서만 실행한다.

   ```bash
   bash scripts/security/verify-sample-service-supply-chain.sh --fixture-only
   bash scripts/security/verify-sample-service-supply-chain.sh --preflight
   bash scripts/security/seed-grype-db-cache.sh --preflight
   ```

   secret 생성도 명시적인 operator 작업이다. 인자 없는 write 전에 `--check`의
   입력·범위를 확인한다. 이 점검은 `--sync-metadata-check`와 다른 계약이다.

   ```bash
   bash scripts/operations/gen-secrets.sh --check
   ```

2. 정적 delivery 계약은 다음 operation-owned 예제 세 개로 검증한다.
   verdict schema v2와 pair schema/generation v3의 형식을 설명하는 fixture이며,
   실제 local rehearsal 입력이나 실행 승인은 아니다.

   ```text
   examples/operations/sample-service-delivery/verdict.baseline.accepted.json
   examples/operations/sample-service-delivery/verdict.candidate.accepted.json
   examples/operations/sample-service-delivery/verification-verdict.pair.json
   ```

   Verdict v2는 OCI manifest/config/archive, deterministic Docker-load archive,
   deterministic local image reference, runtime image ID/kind의 전체 tuple을
   포함한다. Pair v3 (`hyhome-verification-verdict-pair-v3`)는 두 verdict의
   exact byte hash와 role별 전체 tuple을 고정한다. 하나라도 없거나 legacy,
   stale, mixed, substituted이면 class `10`에서 중단하며 Docker/Compose 호출,
   project, record를 만들지 않는다. 위 경로의 파일 존재와 pair 수락 여부는
   승인된 실행 때 다시 검증한다. 현재 project, timestamp, record hash/inode,
   cleanup 증거는 해당 변경의 실제 Task가 소유하며 이 런북이 실행 성공을
   선언하지 않는다.

3. 실제 rehearsal의 positive/negative 순서와 횟수는 해당 실행 Task에서
    승인한다. Baseline/canary는
    `hyhome-dre-20260719-<decimal-pid>-baseline|canary`, loopback
    `18080`/`18081`, exact ownership labels로 제한된다. Canary 실패 시 previous
    runtime image ID와 baseline health를 확인한 뒤 in-process cleanup한다.
    시작 전 deterministic local ref의 `.Id`와 role label을 verdict의 값과
    비교하고, 시작 후 container `.Image`를 같은 runtime ID와 비교한다. Merged
    topology에는 build path가 없고 `pull_policy: never`, `--pull never`,
    `--no-build`가 필수다. 각 run은 cleanup 후 schema-v4 record를 publish한다.
    Canonical record가 하나이므로 positive record hash/요약 필드를 먼저 Task에
    기록한 다음 negative run의 교체 결과를 별도로 기록한다. Standalone `cleanup --task-id`는
    interrupted/partial exact owned pair를 위한 rescue-only 명령이며 성공 run
    후에는 실행하지 않는다. 이미 cleanup된 상태에서는 의도대로 class `60`을
    반환한다. Stateful impact는 해당 서비스의 승인된 recovery 절차로
    handoff한다. 이 런북은 실행이나 재실행을 승인하지 않는다. 필요하면 owning Spec에
    co-located Plan과 Task 승인/evidence 계약을 먼저 작성한다.

## Verification

- 현재 branch와 clean/예상된 작업 트리 상태.
- 정확한 base/candidate SHA, 두 commit 사이 diff 요약과 `git diff --check` 결과.
- 선택한 저장소 계약·문서 traceability 검사와 승인 범위에 해당하는 Compose 검증 결과. 등록에서 폐기된 surface의 freshness를 현재 gate로 요구하지 않는다.
- main 준비 PR의 dated CHANGELOG heading, 정확한 SemVer와 commit, draft 자산 hash 및 실제 게시/미실행 구분.
- release/deploy 주장이 의존하는 backup/N/A, rollback/recovery 링크, incident 경로, remote gate 증거.
- 별도 승인하여 실제 실행한 runtime 배포·secret 값·`.env` sync·port·permission·remote branch-protection 변경과 실행하지 않은 범위의 구분.
- Local delivery evidence에는 revision, digest/verdict reference, project,
  full portable identity tuple의 concise fields, marker presence, decision,
  `data_impact=none`, cleanup, schema-v4 record hash만 기록한다. HTTP body,
  runtime log, secret, credential, token은 기록하지 않는다.
- Local-delivery record의 현재 verdict와 교체 전후 hash/inode는 해당 실행
  Task의 실제 증거에서 확인한다. 과거 문서 서술은 현재 실행 결과가 아니다.

## Rollback and Escalation

### Rollback or Recovery

- 해당 service·workflow·deployment에 문서화된 rollback/recovery 절차만 사용한다.
- 모든 Compose service에 적용되는 일반 rollback 명령은 N/A다. 서비스별 data migration과 backup 복구 경계를 따른다.
- release/tag 판단이 차단되거나 rollback 증거가 불완전하면 판단을 중단하고 위 증거로 에스컬레이션한다.
- Local delivery cleanup의 project/resource ownership query가 누락되거나
  ambiguous하면 broad cleanup을 시도하지 말고 class `60`으로 중단한다.
- In-process cleanup은 exact all-versus-owned container/network ID, 단일
  cardinality, zero volume을 확인한 뒤 그 ID만 직접 제거한다. Standalone
  cleanup은 pair가 absent/incomplete/additional/nonmatching이면 destructive
  call 없이 class `60`으로 중단한다.
- 실패한 문서 변경은 직전 diff 단위로 되돌린다.

### Escalation

- tag 생성, release branch push, branch protection/required check 변경, 배포, runtime 변경은 해당 승인을 확인하고 저장소 소유자 또는 담당 operator에게 handoff한다.
- secret 노출 징후, 값 변경이 필요한 `.env` drift, 추적 문서로 입증할 수 없는 rollback 증거가 있으면 즉시 중단·에스컬레이션한다.

### 검증된 미사용 자료의 정확한 폐기

`python3 scripts/operations/retire-materials.py --root <운영자-체크아웃> --manifest <검토된-manifest>`는 기본적으로 계획만 검사한다. `--apply`는 총괄 통합 순서에 따른 별도 운영 단계이며, 현재 CLN01 source 검증은 실제 삭제 승인이 아니다. 추적 파일은 이 helper가 거부하므로 해당 owning commit에서 정확한 `git rm -- PATH...`를 사용한다. 빈 디렉터리는 별도 확인 후 `rmdir`만 사용한다.

manifest는 checkout 밖 운영자 소유 0700 디렉터리의 0600 regular single-link 파일이며 `entries`에 공개 material `id`, 정확한 path, scope, kind, owner, 1시간 이내 검토 시각, file/parent identity를 둔다. 각 소비 축의 `checked`와 `evidence`, 빈 `consumers`, `recovery_required: false`, 명시적 delete 판정이 필요하다. 유지보수 근거에도 owner, 1시간 이내 검토 시각과 모든 writer 중단 근거를 둔다. `source/runtime/jobs/backup_restore/external` 검사에는 초기화, 수동 운영, 인증 재공급, rollback과 과거 snapshot 복구를 포함한다. true 필드나 profile 비활성만으로 소비자 부재를 증명하지 않는다. 실제 운영 근거는 owning Task에서 확인하고 manifest 원문·비밀값·비밀 hash·inode metadata는 Git과 채팅에 남기지 않는다.

canonical SMTP, LAB, OpenBao·CA·backup key, 현행 암호화 identity, history/audit 원문은 보호한다. 일반 helper는 COMM-002·복구용 PG-020뿐 아니라 COMM-003과 정확한 `secrets/communication/supabase/supabase_smtp_password.txt` 경로도 override 없이 거부한다. Supabase 중복 파일은 SMTP01의 source·운영 참조 전환, 재생성 방지와 5축 검사를 마친 뒤 총괄이 지정한 단일 실행 경로에서만 다룬다. SMTP01의 metadata proof는 CLN01 manifest의 true 값으로 자동 변환하지 않는다. 공유 inode와 불명확한 소비·복구 의존성은 차단한다. 총괄 담당이 정확한 host/path, 효과, 검증, 복구 경계와 동시 writer 중단을 확인한 유지보수 구간에서만 apply한다. `retirement_lock`을 생성기에도 연결해야 하며, lock은 이를 사용하지 않는 hostile writer를 차단하지 못한다. 따라서 총괄 담당은 한 executor, fresh receipt와 통합 route를 지정하고 user-integration hold를 해제하기 전에는 private apply를 하지 않는다.

manifest 필드 계약은 아래와 같다. 이것은 값 없는 입력 계약이며 실제 검사 결과를 채운 운영 manifest가 아니다. 예시 값을 true로 채워 운영 근거를 대체하지 않는다. 현재 Task는 운영 디렉터리를 `/tmp/cln01-<run>/`로 제한하며, helper의 기술적 허용 범위인 다른 외부 0700 디렉터리를 자동 승인하지 않는다.

| 필드 | 필수 조건 |
| --- | --- |
| `entries[].id` | 공개 catalog ID 형식. 보호 ID를 바꿔도 보호 경로는 계속 거부 |
| `path`, `scope`, `kind` | 정확한 상대 경로, `root`, `legacy-secret`·`duplicate-secret`·`optional-material` 중 하나 |
| `decision`, `consumers`, `recovery_required` | `delete`, 빈 배열, `false`; 실제 조사 후에만 기록 |
| `owner`, `evidence_ref`, `reviewed_at` | 담당자·owning Task 근거·timezone 포함 1시간 이내 시각 |
| `checked`, `evidence` | 다섯 축 각각 실제 확인된 boolean과 비어 있지 않은 근거 참조 |
| `identity` | `dev`, `ino`, `size`, `mtime_ns`, `ctime_ns`, `mode`, `nlink`; `identity()`로 현재 파일을 관측 |
| `parents` | `parent_identities()`의 부모 경로·identity 배열; 출력은 private manifest에만 보관 |
| `maintenance` | `writers_stopped`, `owner`, `evidence_ref`, `reviewed_at` 필수. 실제 writer 배제 근거와 1시간 이내 시각 |

`maintenance`는 manifest 최상위 또는 개별 entry에 둘 수 있다. `writers_stopped`는 실제 확인 후에만 true이며, 일반 flock 확보가 다른 writer 중단의 증거가 되지 않는다. 일반 helper의 COMM-003 거부는 유지된다. 해당 후보는 SMTP01의 `smtp_contract --retire`를 제안된 단일 실행자로 두고, 총괄 승인·lock/receipt 통합 전까지 실행하지 않는다. generator는 재생성 방지를 소유하며 후보를 중복 unlink하지 않는다.

helper는 전체 preflight 후 각 파일을 즉시 재검증한다. 부분 실패는 exit 2와 처리됨·이미 없음·실패·미시도 상태를 남긴다. unlink 뒤 fsync 실패는 `deleted-durability-unknown`, identity 확인 실패는 `deleted-identity-unconfirmed`로 보고하므로 파일이 그대로 있다고 가정하지 않는다. 먼저 실제 상태를 재관측하고 검토된 근거를 갱신한 뒤 재실행한다. private 원본을 새 retired/backup 평문 폴더에 복제하지 않는다. Git revert는 추적 source만 복구하며 private 파일의 복구는 이미 존재하는 암호화 복구 자료나 검증된 재발급 경로에 한정한다.

## Related Documents

- [Operations index](../README.md)
- [Runbooks index](../README.md)
- [Co-located Plans and Tasks](../../03.specs/README.md)
- [Current Spec Package selection](../../03.specs/README.md)

### Traceability

- 현재 정책: [Documentation Protocol](../../../.agents/governance/documentation-protocol.md); external release evidence 소유권을 포함한다.
- 과거 구현 증거: [Workspace Revalidation Outcome](../../98.archive/completed/03.specs/0097-home-docker-revalidation-deferred-follow-up/spec.md) (`SPEC-0097`). 완료된 기록은 현재 실행 권한이 아니다.
- 같은 번호 `0009`의 Guide/Policy는 없다.
