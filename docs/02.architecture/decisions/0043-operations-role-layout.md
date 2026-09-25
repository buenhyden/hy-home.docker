---
title: "Operations Role Layout"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0043"
parent_ids:
- "AD-0030"
created: "2026-09-26"
---

# ADR-0043: Operations Role Layout

## Context

2026-08-13 SPEC-0158과 MIG-0002는 Stage 05를 domain 우선 catalog로 수렴시켰다.
문서는 `docs/05.operations/catalog/<domain>/####-<subject>/{guide,policy,runbook}.md`에
있고, 13개 domain README와 catalog README가 탐색을 소유한다. 그때의 운영 검증기는
`guides/`, `policies/`, `runbooks/` 경로를 "retired root"로 거부한다.

2026-09-26 owner는 Stage 05를 현재 워크스페이스를 안전하게 운영하는 사람 중심
계층으로 다시 정의했다. 사람은 먼저 "이해가 필요한가, 허용 여부가 필요한가, 실행할
명령이 필요한가"로 문서를 찾는다. catalog 구조에서는 같은 질문에 답하려면 13개
domain을 모두 열어야 하고, 세 역할을 채우려는 압력이 subject 폴더 단위로 생긴다.

기준점 `0deb430ea`의 사실:

- 역할 문서 225개(Guide 77, Policy 75, Runbook 73), domain README 13개.
- 모든 `GDE`/`POL`/`RUN` 번호는 subject 폴더 번호와 같고, 하나만 다르다:
  `0051-airflow-dag-lifecycle/policy.md`는 MIG-0002의 병합 결과로 `POL-0052`다.
- `optimization-hardening` slug는 7개 domain에서 반복된다.

## Decision Drivers

- 사람이 역할(이해, 통제, 실행)로 먼저 찾는다.
- 발급된 ID를 바꾸지 않는다(documentation protocol 작성 규칙 5).
- 두 탐색 체계를 병행하지 않는다.
- Stage 98 frozen body와 sealed record는 다시 쓰지 않는다.

## Options Considered

1. **catalog 유지**: 변경 비용이 없지만 owner가 목표와 충돌한다고 명시한 구조를
   남긴다.
2. **catalog 유지 + 역할별 인덱스 추가**: 두 탐색 체계가 영구히 병행한다.
   README가 "역할별 병렬 인덱스를 발행하지 않는다"고 금지한 바로 그 상태다.
3. **역할 우선 경로로 전환(채택)**: `guides/`, `policies/`, `runbooks/`,
   `incidents/`가 역할을 소유하고 domain은 인덱스 분류로 남는다.

## Decision

- 경로: `docs/05.operations/` 아래 `guides/####-<slug>.md`,
  `policies/####-<slug>.md`, `runbooks/####-<slug>.md`. Incident와 Postmortem
  경로는 바꾸지 않는다.
- 파일 번호는 문서 자신의 artifact 번호다(`identity_relation: direct`). 기존 ID는
  그대로 두므로 `POL-0052`는 `policies/0052-airflow-dag-lifecycle.md`가 된다.
- subject는 slug다. 같은 slug는 역할 디렉터리를 넘어 같은 subject를 가리키고,
  한 역할 디렉터리 안에서 slug는 유일하다. 반복되는 `optimization-hardening`은
  domain 단어를 앞에 붙인다(예: `data-optimization-hardening`).
- 새 subject 번호는 지금처럼 subject당 하나를 발급해 그 subject의 역할 문서가
  공유한다.
- 각 역할 디렉터리의 `README.md`가 구성원을 domain별로 묶어 한 번씩 나열한다.
  `catalog/`, domain README, `operations-domain-readme` profile과 template은
  제거한다. 어떤 Stage 98 보존 문서도 그 profile을 쓰지 않으므로 historical-only
  profile은 두지 않는다.
- 운영 검증기는 `catalog`를 retired root로, 현재 문서의 catalog 경로 언급을
  active reference 위반으로 거부한다.
- 외부 저장소 소비자에게는 MIG-0005가 이동 범위와 현재 owner를 알린다.

## Consequences

- 긍정: 역할로 바로 찾는다. 역할을 채우려는 빈 문서가 생길 구조적 이유가 없다.
- 부정: 한 subject의 세 문서가 한 폴더에 모이지 않는다. 역할 인덱스와 같은
  slug가 그 관계를 보여 준다.
- 다른 저장소의 catalog 링크는 끊긴다. 이 저장소는 그것을 고치지 않고 인계한다.
- Stage 98 기록과 MIG-0002는 catalog 경로를 역사 사실로 계속 담는다.

## Traceability

- 상위 architecture: [AD-0030](../descriptions/0030-document-lifecycle-governance.md)
- 대체되는 구조 결정: SPEC-0158과 MIG-0002의 catalog 수렴(Stage 98 보존 기록)
- 실행: [SPEC-0183](../../03.specs/0183-operations-role-layout/spec.md)

## Compliance

`scripts/validation/check-operations-catalog.py`, Registry의 taxonomy 검사, 그리고
`check-document-links.py --mode all`이 이 결정을 강제한다.

## Follow-up

- `inc-2026-0002`의 해결 검증은 이 결정과 무관하며 SPEC-0183 Task가 인계 항목으로
  추적한다.
- 다른 저장소의 링크 수정은 해당 저장소 owner가 수행한다.
