---
title: "Canonical Agent Governance Home"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-06"
layer: "architecture"
artifact_id: "ADR-0032"
parent_ids:
- "AD-0027"
supersedes:
- "ADR-0029"
created: "2026-09-06"
---

# ADR-0032: Canonical Agent Governance Home

## Context

ADR-0029는 공통 규범, 문서 machine contract, 실행기, native adapter의 책임을
분리했다. 이 책임 분리는 유지하면서 사용자가 공통 정본을 저장소 소유
`.agents/`로 이전하고 옛 거버넌스 디렉터리를 제거하도록 명시적으로 요청했다.
현재의 비권위·빈 디렉터리 계약은 이 변경의 대상이다.

이 문서는 명시적인 사용자 이전 요청과 Task의 독립 설계 검토에 따라
위치·로딩 결정을 대체한다. 구현 검증의 남은 항목은 Task가 소유한다.
사람 서명, 승인 시각, native 실행 결과를 소급 작성하지 않는다.

## Decision Drivers

- 공통 의미와 변경 가능한 목록마다 정본을 하나만 둔다.
- Codex의 저장소 스킬 탐색과 실제 소유 경로를 일치시킨다.
- native 형식과 제공자별 지원 차이, 기존 승인·보안 경계를 유지한다.
- 77개 원본의 내용을 검토해 처분하며, 역할 14개와 스킬 23개의 식별자를 유지한다.
- 문서 검증·CI·위키가 숨김 정본을 누락하지 않아야 한다.
- archived Task와 이미 frozen인 본문을 경로 정리를 이유로 수정하지 않는다.

## Options Considered

| 대안 | 효과와 비용 | 판단 |
| --- | --- | --- |
| 검토한 정본을 `.agents`로 이전 | 네이티브 스킬 탐색과 소유권 일치; 모든 소비자 전환 필요 | 요청 목표에 부합 |
| 현재 문서 Stage에 정본 유지 | 기존 명시적 읽기 유지; 요청한 정본 위치·탐색 목표 미충족 | 이번 요청에서 미채택 |
| 전체 복제 또는 루트 symlink | 중복 권위, 형식 혼합, 출력/입력 순환과 경계 위험 | 미채택 |

## Decision

독립 설계 검토를 거친 다음 위치 모델을 채택한다.

- `.agents/governance/`는 공통 정책과 규범적 SDLC를 소유한다.
- `.agents/roles/`는 기존 책임·입출력·권한·위임 계약을 소유한다.
- `.agents/skills/<name>/SKILL.md`는 실제 호출형 절차를 소유한다. 기존 metadata는
  표준 native envelope 안에 보존하며 양 제공자의 명시 호출 제어를 적용한다.
- 제공자 공통 매핑은 governance/providers Registry가 소유한다. 도구별 authored
  설명은 `.claude/provider.md`·`.codex/provider.md`, 생성 README와 역할/스킬
  어댑터는 기존 native 위치를 사용한다. 생성 출력은 입력 정본이 아니다.
- Stage 99는 문서 경로·profile·ID·section·lifecycle·traceability·template의
  유일한 machine authority다. 기존 scripts가 실행 검증과 변환을 소유한다.
- 여섯 suite와 두 profile, workflow의 실행 구성, script manifest의 inventory
  책임을 유지한다. 이번 위치 변경은 운영 입력에 접근할 실행 승인을 부여하지 않는다.
- 상세 Requirement·Architecture·Spec/Plan/Task·Operations는 기존 docs에 둔다.
  Stage 90은 비권위 증거, Stage 98은 ADR-0031에 따른 보존 기록이다. Git 이력은
  보존 본문의 복구·동일성 근거이며 Task 본문의 대체물이 아니다.
- 옛 공통 디렉터리는 현행 읽기·생성·링크·fallback 대상에서 제거한다. frozen
  기록의 옛 경로와 재발 방지 테스트 문자열은 역사/부정 사례로 분류한다.

## Consequences

- 공통 스킬은 native 탐색 대상이 되므로 묵시적 실행 확대를 막는 제어와
  실제 discovery 결과를 별도로 검사해야 한다. metadata는 승인 게이트가 아니다.
- canonical 입력은 생성·격리·삭제 대상이 아니다. 예상 밖 파일은 보존하고 실패한다.
- 경로 변경은 Registry/schema/template/validator/test와 상대 링크를 함께 바꾼다.
- 새로운 plugin, 서버, memory, `.codex/config.toml`, 추가 공통 디렉터리를
  형식적 대칭을 위해 만들지 않는다. 모델·권한·hook trust를 변경하지 않는다.
- 로컬 문법/계약 성공, native 발견, 호출, 권한 강제, 실제 hook 수신은 서로 다른 증거다.

## Traceability

- [Agent governance requirement](../../01.requirements/0024-agent-governance-standardization.md)
- [Canonical adapter architecture](../descriptions/0027-agent-governance-canonical-adapter.md)
- Predecessor authority decision
- Preserved-record decision
- [Owning specification](../../03.specs/0173-governance-qa-surface-convergence/spec.md)
- [Current plan](../../03.specs/0173-governance-qa-surface-convergence/plan.md)

## Compliance

승인 출처는 현재 대화의 명시적 이전 요청과 Task에 기록하는 실제 독립 검토다.
커밋·원격·운영·비밀값·전역 설정 변경은 승인되지 않았다. 보호 경로 쓰기는
대상과 행위가 한정된 정상 승인 절차로만 수행한다.

## Follow-up

ADR-0029의 reciprocal supersession metadata와 최초 보존 직전의 합법적인
lifecycle metadata만 변경한다. 결정 본문은 수정하지 않고 Stage 98에 보존한다.
이미 frozen인 ADR-0027과 다른 기록은 그대로 둔다. 필수 정적 검사와 보호 경로
승인 상태, 네이티브 검증 보류는 현재 Task에서 계속 추적한다.
