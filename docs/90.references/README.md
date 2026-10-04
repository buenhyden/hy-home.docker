---
title: "References"
version: "1.0.3"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "references"
---

# References

## Overview

`docs/90.references/`는 세 가지 package 범주로 보조 증거를 저장합니다. 활성
lifecycle stage가 사실을 평가하도록 돕지만 공통 Agent 거버넌스
정책, Stage 01 요구사항, Stage 02 아키텍처, Stage 03 명세, Stage 05 운영을
대체하지 않습니다.

## Scope

- `research/`: 외부 증거와 출처 기반 분석(`RES-####`).
- `audits/`: 특정 시점의 gap과 conformance 평가(`AUD-####`).
- `data/`: 저장소 인벤토리와 구조화된 참고 데이터(`DATA-####`).

## Structure

```text
docs/90.references/
├── README.md
├── research/####-<slug>/
├── audits/####-<slug>/
└── data/####-<slug>/
```

Package 경로는 번호만 사용하며 접두사와 날짜를 포함하지 않습니다. 안정 ID는
frontmatter에 남습니다. 관찰 날짜는 `observed_at`에 남고, 생성된 Data
package는 `generated_by` provenance를 유지합니다.

### Authority Boundary

Stage 90은 비규범적입니다. 증거가 현재 owner와 충돌하면 현재 공통
거버넌스와 Stage 01/02/03/05 문서를 따르고 reference package를 갱신하거나
supersede합니다. 실행 가능한 OpenAPI, GraphQL, Proto 계약은 해당 Stage 03
Spec Package에 남습니다.

[공통 Agent 거버넌스 작성 정책](../../.agents/governance/documentation-protocol.md#role-specific-authoring)이
출처, 한계, 소비자, 신선도 기대치를 소유합니다. Diátaxis의 technical
reference는 독자의 필요를 설명할 뿐이며 이것만으로 문서가 Stage 90 증거가
되지는 않습니다. 생성된 데이터는 등록된 generator가 새로고침하며 손으로
고쳐 현재 버전이나 runtime 권위로 만들지 않습니다.

폐기된 redirect, 호환 사본, `learning/`, `llm-wiki/`는 현재 범주가
아닙니다. 학습 자료는 의미에 따라 Stage 05 Guide 또는 Research package로
분류됩니다.

### Lifecycle and Naming

- Stage 99의 `research`, `audit`, `data` profile과 그 템플릿을 사용합니다.
- 발급된 ID를 재사용하지 않습니다.
- lifecycle 이력에는 `status`, `supersedes`, `superseded_by`를 사용합니다.
- 날짜는 package 이름이 아니라 frontmatter에 저장합니다.
- 인용, 외부 관찰 날짜, 한계를 보존합니다.

### Current Categories

- [Research packages](./research/README.md)
- [Audit packages](./audits/README.md)
- [Data packages](./data/README.md)

## Usage

1. 파일 형식이 아니라 목적으로 증거 범주를 선택합니다.
2. 매핑된 Stage 99 템플릿을 복사하고 다음 등록 안정 ID를 발급합니다.
3. Traceability에 활성 owner를 연결하고 규범적 지시는 그곳에 둡니다.
4. metadata, 링크, reference-package, generator 신선도 검증을 실행합니다.

## Related Documents

- [Documentation protocol](../../.agents/governance/documentation-protocol.md)
- [Stage authoring matrix](../../.agents/governance/stage-authoring-matrix.md)
- [Stage 99 registry](../99.templates/registry.json)
- [Research template](../99.templates/templates/references/research-pack.template.md)
- [Audit template](../99.templates/templates/references/audit-pack.template.md)
- [Data template](../99.templates/templates/references/data-pack.template.md)
