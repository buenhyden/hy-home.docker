# docs/ 문서 체계 안내

## 목적

이 디렉터리는 프로젝트의 모든 요구사항, 아키텍처, 결정 사항, 운영 절차 등을 통합 관리하는 표준 공간입니다.

이 체계는 다음 세 가지 핵심 가치를 지향합니다.

1. **추적성**: 모든 기술적 결정은 명확히 기록되어 언제든 이유를 확인할 수 있어야 합니다.
2. **검증 가능성**: TDD 원칙에 따라 검증 가능한 구현 단위와 작업을 관리합니다.
3. **AI 통합**: 에이전트가 문서를 통해 맥락을 파악하고 협업할 수 있도록 구조화합니다.

## 문서 흐름

기본적인 문서 작업 흐름은 다음과 같습니다.

`01.prd → 02.ard → 03.adr → 04.specs → 05.plans → 06.tasks → 07.guides / 08.operations / 09.runbooks → 10.incidents → 11.postmortems`

도움이 되는 보조 문서는 다음과 같습니다.

- `99.templates`: 모든 문서의 표준 템플릿 모음
- `00.agent-governance`: AI 에이전트 전용 실행 지침 (토큰 절약을 위한 Lazy Loading 구조)

## 작성 원칙

1. **상단 요약 제공**: 모든 문서는 최상단에 한국어 요약(Overview (KR))을 배치하여 빠르게 내용을 파악할 수 있게 합니다.
2. **이원화 언어 정책**:
   - **에이전트 전용 문서** (`docs/00.agent-governance/`, `AGENTS.md` 등): 토큰 효율과 분석 정확도를 위해 **영어(English)** 작성을 원칙으로 합니다.
   - **인간 전용 문서** (README, 가이드, 리포트 등): 사용자의 가독성을 위해 **한국어(Korean)**로 작성합니다.
3. **AI 에이전트 응답 정책**:
   - 에이전트는 모든 답변, 요약, 알림을 반드시 **한국어**로 수행해야 합니다.
   - 내부적인 사고(Thinking)나 기술적 분석은 영어를 사용할 수 있으나, 최종 결과물은 한국어여야 합니다.
4. **Markdown 표준**: 모든 문서는 상대 경로를 사용하며 Markdown 형식을 준수합니다. (절대 경로 및 `file://` 사용 금지)
5. **명확한 위치 설정**: 결정 사항은 ADR에, 상세 설계는 Spec에, 작업 절차는 Runbook에 기록하여 파편화를 방지합니다.

## 하위 폴더별 README 필수 항목

각 하위 폴더의 `README.md`는 다음 내용을 포함해야 합니다. (모두 **한국어** 작성)

- 해당 단계가 프로젝트에서 갖는 의미와 역할
- 권장되는 파일명 명명 규칙 및 하위 구조
- 참조할 표준 템플릿 링크

---

## 디렉터리 상세 역할

### [01.prd](01.prd/README.md)

제품 요구사항 정의 (Vision, Use Case, Requirements)

### [02.ard](02.ard/README.md)

아키텍처 참조 모델 및 품질 속성 정의

### [03.adr](03.adr/README.md)

기술적 의사결정 기록 (Decision, Status, Context, Consequence)

### [04.specs](04.specs/README.md)

컴포넌트/기능별 상세 설계 명세 (Data, API, Logic, Agent-Design)

### [05.plans](05.plans/README.md)

실행 계획 및 마일스톤 (Work Breakdown, Risks)

### [06.tasks](06.tasks/README.md)

실제 구현 및 검증 작업 단위 (Task Table, Evidence)

### [08.operations](08.operations/README.md)

시스템 운영 정책 및 거버넌스

### [09.runbooks](09.runbooks/README.md)

반복적 운영 작업의 실행 지침 (Step-by-step)

### [10.incidents](10.incidents/README.md)

발생한 사고의 사실 기록 (Timeline, Mitigation)

### [11.postmortems](11.postmortems/README.md)

사고 구조 분석 및 재발 방지 대책
