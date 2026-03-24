# docs/ 문서 체계 안내

## 목적

이 디렉터리는 요구, 아키텍처, 결정, 명세, 계획, 작업,
운영, 절차, 사고, 사분석을 통합 관리하는 표준 공간이다.

이 체계는 다음 세 가지를 만족하도록 설계한다.

1. 모든 기술 결정은 명시적으로 기록되고 추적 가능해야 한다.
2. TDD 기반의 검증 가능한 구현과 작업 단위를 관리한다.
3. AI Agent 설계와 운영을 표준 문서 체계 안에 통합한다.

## 문서 흐름

기본 흐름은 아래와 같다.

`01.prd → 02.ard → 03.adr → 04.specs → 05.plans → 06.tasks → 07.guides / 08.operations / 09.runbooks → 10.incidents → 11.postmortems`

보조 문서는 다음과 같다.

- `99.templates`: 모든 문서의 표준 템플릿
- `00.agent`: AI Agent 전용 실행 지침 (Lazy Loading 전용)

## 작성 원칙

1. 한국어 기술 요약(Overview (KR))을 문서 상단에 배치한다.
2. 영어와 한국어를 혼용하여 아키텍처적 의도를 명확히 한다.
3. 모든 문서는 Markdown 형식을 따르며, 상대 경로를 사용한다.
4. Placeholder는 저장 전에 모두 제거한다.
5. 결정은 ADR에, 상세 설계는 Spec에, 절차는 Runbook에 둔다.
6. 사고 기록은 사실에, 사후 분석은 학습에 집중한다.
7. AI Agent 변경은 설계, 계획, 평가, 운영까지 연결되어야 한다.

## README에 반드시 들어가야 하는 내용

각 하위 폴더의 `README.md`는 다음 내용을 포함해야 한다.

- 해당 단계의 정의와 역할
- 권장 하위 구조 및 파일명 규칙
- 사용할 표준 템플릿 링크

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
