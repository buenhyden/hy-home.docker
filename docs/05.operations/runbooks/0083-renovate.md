---
title: "Renovate Runbook"
version: "0.1.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0083"
parent_ids:
- "POL-0083"
created: "2026-09-19"
---

# Renovate Runbook

## When to Use

정적 readiness 점검, 구체적으로 승인된 live job, 또는 잘못된 Renovate 변경의 복구에
사용한다. 저장소 루트에서 작업한다.

## Procedure

1. remote 저장소에 접근하지 않고 검증한다.

   ```bash
   renovate-config-validator --strict --no-global renovate.json5
   renovate-config-validator --strict infra/09-tooling/renovate/config/config.js
   bash scripts/operations/sync-tech-stack-versions.sh --check
   ```

2. dry-run/discovery 출력, 저장소 scope, token owner, branch protection, 승인 여부를
   검토한다. 1단계 결과만으로 remote readiness를 추론하지 않는다.
3. remote write가 승인된 경우에만 job을 실행한다.

   ```bash
   docker compose --profile dependency-update run --rm renovate
   ```

4. 정제된 exit status를 기록하고 생성된 remote 변경 사항을 열거한다. 각 branch/PR를 검토한다.
   이 실행 승인 범위에서는 merge나 close를 하지 않는다.

## Evidence

승인 여부, config commit, 이미지 선언, 대상 저장소, exit status, 정제된 job 요약, 생성된
모든 branch/PR을 기록한다. token, 원본 환경 값, 저장소 credential은 기록하지 않는다.

## Rollback or Recovery

1. 활성 실행이 원치 않는 변경을 만들고 있다면 해당 컨테이너를 중단한다.
2. 잘못된 local policy를 Git에서 복원하고 strict validation을 다시 실행한다.
3. remote branch/PR을 개별적으로 검토한다. 명시적 승인이 있을 때만 close 또는 revert하고
   audit trail을 보존한다.
4. token이 노출됐을 가능성이 있으면 job을 비활성화하고 secret owner에게 rotate/revoke를
   요청한다. 현재 token을 복사하거나 표시하지 않는다.
5. 캐시 손상은 job이 실행 중이지 않을 때 폐기 가능한 캐시를 재생성하여 복구한다. remote
   저장소 상태는 절대 그 캐시에서 복원하지 않는다.

### Verification and Status

Renovate job이 실행 중이지 않고, config가 검증되고, remote 변경 사항이 파악되고, token
처리 상태가 확인되면 복구가 완료된 것이다. 이 복구 단계는 2026-09-20 수정 때 문서로만
남겼고 실행하지 않았다. remote 저장소 변경이나 token validation은 주장하지 않는다.

## Escalation

알 수 없는 remote write, 과도한 token 권한, token 노출 의심, 인식되지 않는 허용 명령, 또는
한 번에 하나씩 안전하게 조정할 수 없는 remote 상태는 에스컬레이션한다.

## Traceability

- 관장 architecture: [AD-0009](../../02.architecture/descriptions/0009-tooling-architecture.md)
- 대상 peer 문서: [Guide](../guides/0083-renovate.md), [Policy](../policies/0083-renovate.md)

## Related Documents

- [Renovate Compose source](../../../infra/09-tooling/renovate/docker-compose.yml)
- [Derived Compose image projection](../../../infra/tech-stack.versions.json)
- [Renovate self-hosted configuration](https://docs.renovatebot.com/self-hosted-configuration/)
- [운영 인덱스](../README.md)
