---
status: draft
artifact_id: <artifact-id>
artifact_type: release
parent_ids: [<parent-artifact-id>]
---
<!-- Release Target: docs/05.operations/releases/YYYY-MM-DD-release-name.md -->

# Release: [Release Name]

> Use this template only after a real release event has executable evidence.
>
> Rules:
>
> - Write the human-facing release record in Korean. Preserve version strings,
>   artifact identifiers, commands, paths, timestamps, and evidence labels.
> - A changelog, release-readiness review, plan, or task is input evidence; it
>   is not proof that a release was executed.
> - Record only verified artifacts, approvals, validation, rollout, rollback,
>   and outcomes. Mark unknown or unavailable evidence explicitly.
> - Do not treat this document as deployment runtime authority. Deployment
>   targets, promotion, CD behavior, and runtime rollback remain owned by Spec
>   127 or a later approved runtime chain.
> - Never include secret values, credentials, tokens, private keys, raw logs,
>   or shell history.
> - Target-relative links are calculated from the copied release path, not
>   from `docs/99.templates/`.

## Release Identity and Scope

- **Release name / version**: [검증된 이름 또는 버전]
- **Release date and time**: [YYYY-MM-DD HH:MM TZ]
- **Release owner**: [승인된 소유자 또는 팀]
- **Environment / target**: [검증된 대상]
- **Scope**: [이번 릴리스에 포함된 범위]
- **Out of scope**: [포함되지 않은 범위]

## Included Changes

| Change / Work Item | Version / Commit | User or Operator Impact | Source Evidence |
| --- | --- | --- | --- |
| [변경 항목] | [버전 또는 커밋] | [영향] | [Spec, Plan, Task, PR 또는 변경 기록 링크] |

## Release Artifacts

| Artifact | Immutable Identifier | Provenance / Location | Verification |
| --- | --- | --- | --- |
| [이미지, 패키지, 구성 또는 문서] | [digest, version, commit] | [비밀이 없는 위치] | [검증 결과] |

## Validation Evidence

| Gate | Command / Check | Result | Evidence |
| --- | --- | --- | --- |
| [검증 게이트] | `[명령 또는 검사 이름]` | [PASS / FAIL / N/A] | [요약 또는 링크] |

## Approvals

| Approval | Approver / Authority | Decision | Evidence |
| --- | --- | --- | --- |
| [릴리스 또는 변경 승인] | [역할 또는 승인 주체] | [Approved / Rejected] | [승인 기록] |

## Rollout and Rollback

- **Executed rollout**: [실제로 수행된 순서와 시각]
- **Observed checkpoints**: [검증된 상태와 지표]
- **Rollback trigger**: [승인된 기준]
- **Verified rollback procedure**: [실행된 절차 또는 승인된 runbook 링크]
- **Rollback outcome**: [수행하지 않음 / 성공 / 실패와 근거]

## Outcome

- **Final state**: [Completed / Rolled back / Partially completed]
- **Completion time**: [YYYY-MM-DD HH:MM TZ]
- **Observed impact**: [검증된 사용자 또는 운영 영향]
- **Follow-up**: [후속 Task, Incident 또는 Runbook]

## Known Issues

| Issue | Impact | Mitigation / Owner | Tracking Evidence |
| --- | --- | --- | --- |
| [알려진 문제 또는 None] | [영향] | [완화책과 담당] | [Task 또는 Incident 링크] |

## Related Documents

- **Parent Spec**: [Spec](../../03.specs/NNN-feature-id/spec.md)
- **Execution Plan**: [Plan](../../04.execution/plans/YYYY-MM-DD-feature.md)
- **Execution Task**: [Task](../../04.execution/tasks/YYYY-MM-DD-feature-or-stream.md)
- **Deployment runtime owner**: [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
- **Rollback Runbook**: [Runbook](../runbooks/tier/topic.md)
