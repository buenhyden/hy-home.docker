---
title: "Release Management Runbook"
version: "1.2.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0009"
parent_ids: []
created: "2026-06-04"
---

# Release Management Runbook

## Overview

이 런북은 `hy-home.docker`의 수동 release/tag readiness, evidence capture, rollback evidence 확인 절차를 정의한다. 이 문서는 release/tag 준비 절차와 `main-current` 채널 태그 운영을 설명한다. GitHub branch protection, Docker runtime, secret, `.env`, port의 변경 권한은 부여하지 않는다.

> 범위: Release Management Runbook의 실행 절차

### Purpose

- Release Management Runbook 작업을 반복 가능하고 검증 가능한 절차로 수행한다.
- 실행 전후 evidence, rollback 또는 escalation 기준을 명확히 남긴다.

**`main-current` 채널 태그**

`main` push가 완료되면 `.github/workflows/ci-quality.yml`의 `main-security`가 병합된 SHA에서 Zizmor SARIF를 생성한다. 이 작업이 성공한 경우에만 종속 작업 `update-main-current`가 `bash scripts/operations/update-main-current-tag.sh`를 실행한다. 스크립트는 원격 `main`이 감사한 `GITHUB_SHA`와 일치하는지 확인하고, 기존 태그에 lease를 걸어 경량 `refs/tags/main-current`만 갱신한다. 원격 `main`이 앞서갔거나 태그가 주석 태그이거나 다른 실행이 먼저 태그를 바꿨다면 실패하며 태그를 강제로 덮어쓰지 않는다. 기존 릴리스 태그와 수동 릴리스 절차는 별도로 유지한다.

실패 시에는 GitHub Actions의 `main-security`와 `update-main-current` 상태, 원격 `refs/heads/main` 및 `refs/tags/main-current`의 SHA를 확인한다. 재실행은 해당 SHA의 보안 검사가 성공했고 원격 `main`이 여전히 그 SHA일 때만 허용한다. 태그를 수동으로 이동하기 전에 실패 원인과 승인 범위를 Task에 기록한다.

## When to Use

- Release 또는 tag 생성 전에 local documentation, validation, changelog readiness를 확인해야 할 때.
- PR 또는 local branch가 release candidate로 승격되기 전에 어떤 evidence를 남겨야 하는지 확인할 때.
- Rollback 가능성을 주장하기 전에 실제로 남겨야 할 local evidence를 확인해야 할 때.

## Procedure

### Checklist

- [ ] 관련 policy, guide, runbook handoff를 확인한다.
- [ ] 현재 상태와 변경 범위를 기록한다.

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

3. candidate에 해당하는 문서·검증 gate를 선택한다. 먼저 명령이 읽는 입력과 side effect를 확인한다. 문서 작업 승인은 환경·secret 읽기 승인이 아니다.

   ```bash
   python3 scripts/validation/run-ci-gate.py --profile changed
   python3 scripts/validation/check-document-links.py --mode traceability
   ```

4. 해당 작업에서 입력과 임시 파일 생성까지 승인한 경우에만 Compose readiness를 점검한다. preflight는 실제 `.env`를 source하고 일반 검증도 dummy 입력을 만들 수 있다. [RUN-0086](0086-dependency-version-management.md#static-configuration-validation)의 범위를 먼저 확인한다.

   ```bash
   bash scripts/validation/validate-docker-compose.sh --preflight
   bash scripts/validation/validate-docker-compose.sh
   ```

   격리된 five-service runtime harness는 별도 operator 작업이다. preflight는
   service를 시작하지 않지만 입력·도구 사용 범위는 확인한다. scenario는 Task별
   runtime 승인이 필요하며 validation profile이 자동 선택하지 않는다.

   ```bash
   bash scripts/operations/check-compose-core-readiness.sh --preflight
   ```

5. 추적된 release 소스에서 changelog와 tag 준비 상태를 확인한다.

   ```bash
   git log --oneline --decorate -n 20
   git tag --list
   ```

   `v*.*.*` tag를 push하기 전에 `CHANGELOG.md`에 정확한 tag 문자열이 있는지
   확인한다. `.github/workflows/generate-changelog.yml`은 문자열이 없으면
   실패한다. 아래 placeholder를 승인된 tag로 바꾸고 fixed-string으로 검사한다.

   ```bash
   rg -n -F "vX.Y.Z" CHANGELOG.md
   ```

6. release 또는 deploy 준비 완료를 선언하기 전에 다음 항목을 확인한다.

   - 영향을 받는 각 stateful surface의 backup 증거 또는 명시적인 N/A 근거.
   - 변경한 각 service·workflow·deployment의 rollback/recovery runbook 링크.
   - 차단·실패·rollback한 release 판단의 incident 기록 경로 또는 escalation 채널.
   - branch protection·required check·release workflow의 현재 강제를 주장할 때 remote gate 검증 증거.

7. 실행 Task 또는 PR 설명에 준비 상태와 증거를 남긴다. secret·`.env` 값, credential이 있는 원문 로그, shell history, deployment token을 붙여넣지 않는다.

8. `sample-web-service`의 local promotion/rollback 계약을 확인할 때는 먼저
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

9. 정적 delivery 계약은 다음 operation-owned 예제 세 개로 검증한다.
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

10. 실제 rehearsal의 positive/negative 순서와 횟수는 해당 실행 Task에서
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

### Steps

1. 이 runbook의 trigger와 checklist를 확인한다.
2. 기존 절차가 문서에 포함되어 있으면 그 순서대로 수행한다.
3. 실행 중 생성된 명령 출력과 판단 근거를 evidence로 남긴다.
4. 검증 실패, secret exposure 위험, 파괴적 변경 필요 시 즉시 중단하고 `## Escalation`으로 이동한다.

### Verification Steps

- [ ] 관련 validation script 또는 수동 확인을 실행한다.
- [ ] 변경 결과가 policy, guide, runbook handoff와 충돌하지 않는지 확인한다.

### Observability and Evidence Sources

- **Signals**: 명령 결과, 검증 로그, service 상태, 문서 diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 runbook 범위를 벗어난 별도 승인 절차로 분리한다.

## Evidence

- 현재 branch와 clean/예상된 작업 트리 상태.
- 정확한 base/candidate SHA, 두 commit 사이 diff 요약과 `git diff --check` 결과.
- 선택한 저장소 계약·문서 traceability 검사와 승인 범위에 해당하는 Compose 검증 결과. 등록에서 폐기된 surface의 freshness를 현재 gate로 요구하지 않는다.
- release/tag 판단에 사용한 changelog의 정확한 tag 문자열과 commit 범위 증거.
- release/deploy 주장이 의존하는 backup/N/A, rollback/recovery 링크, incident 경로, remote gate 증거.
- 별도 승인하여 실제 실행한 runtime 배포·secret 값·`.env` sync·port·permission·remote branch-protection 변경과 실행하지 않은 범위의 구분.
- Local delivery evidence에는 revision, digest/verdict reference, project,
  full portable identity tuple의 concise fields, marker presence, decision,
  `data_impact=none`, cleanup, schema-v4 record hash만 기록한다. HTTP body,
  runtime log, secret, credential, token은 기록하지 않는다.
- Local-delivery record의 현재 verdict와 교체 전후 hash/inode는 해당 실행
  Task의 실제 증거에서 확인한다. 과거 문서 서술은 현재 실행 결과가 아니다.

## Rollback or Recovery

- 해당 service·workflow·deployment에 문서화된 rollback/recovery 절차만 사용한다.
- 모든 Compose service에 적용되는 일반 rollback 명령은 N/A다. 서비스별 data migration과 backup 복구 경계를 따른다.
- release/tag 판단이 차단되거나 rollback 증거가 불완전하면 판단을 중단하고 위 증거로 에스컬레이션한다.
- Local delivery cleanup의 project/resource ownership query가 누락되거나
  ambiguous하면 broad cleanup을 시도하지 말고 class `60`으로 중단한다.
- In-process cleanup은 exact all-versus-owned container/network ID, 단일
  cardinality, zero volume을 확인한 뒤 그 ID만 직접 제거한다. Standalone
  cleanup은 pair가 absent/incomplete/additional/nonmatching이면 destructive
  call 없이 class `60`으로 중단한다.

## Escalation

- tag 생성, release branch push, branch protection/required check 변경, 배포, runtime 변경은 해당 승인을 확인하고 저장소 소유자 또는 담당 operator에게 handoff한다.
- secret 노출 징후, 값 변경이 필요한 `.env` drift, 추적 문서로 입증할 수 없는 rollback 증거가 있으면 즉시 중단·에스컬레이션한다.

## Traceability

- 현재 정책: [Documentation Protocol](../../../.agents/governance/documentation-protocol.md); external release evidence 소유권을 포함한다.
- 과거 구현 증거: [Workspace Revalidation Outcome](../../98.archive/completed/03.specs/0097-home-docker-revalidation-deferred-follow-up/spec.md) (`SPEC-0097`). 완료된 기록은 현재 실행 권한이 아니다.
- 같은 번호 `0009`의 Guide/Policy는 없다.

## Related Documents

- [Operations index](../README.md)
- [Runbooks index](../README.md)
- [Co-located Plans and Tasks](../../03.specs/README.md)
- [Current Spec Package selection](../../03.specs/README.md)
