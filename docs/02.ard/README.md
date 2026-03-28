# 02. ARD (Architecture Reference Document)

> 시스템의 구조적 경계, 품질 속성 및 참조 모델을 정의하는 문서 저장소

## Overview

`docs/02.ard/` 경로는 `hy-home.docker` 에코시스템의 기술적 뼈대를 정의하는 아키텍처 참조 문서들을 관리한다. 각 문서는 특정 시스템이나 도메인이 맡은 책임 범위, 타 시스템과의 상호작용 방식, 그리고 달성해야 할 핵심 품질 속성(성능, 보안, 확장성 등)을 아키텍처 관점에서 기술한다.

## Audience

이 README의 주요 독자:

- Software Architects
- Senior Developers
- Infrastructure Engineers
- AI Agents (Architectural guardrails & context)

## Scope

### In Scope

- 시스템/도메인별 참조 아키텍처 모델 (`####-<name>.md`)
- 시스템 경계 및 책임 (Owns / Consumes)
- 품질 속성 요구사항 (Performance, Security, etc.)
- 인프라 배포 모델 및 데이터 흐름도

### Out of Scope

- 비즈니스 요구사항 정의 (-> `01.prd/`)
- 구체적인 개별 기술 결정의 배경 (-> `03.adr/`)
- 함수/클래스 수준의 상세 설계 (-> `04.specs/`)
- 운영 매뉴얼 및 절차 (-> `09.runbooks/`)

## Structure

```text
02.ard/
├── 0010-communication-architecture.md
├── 0011-laboratory-architecture.md
├── 0013-open-webui-architecture.md
├── 0014-auth-optimization-hardening-architecture.md
├── 0018-security-optimization-hardening-architecture.md
├── 0019-data-optimization-hardening-architecture.md
├── 0020-messaging-optimization-hardening-architecture.md
├── 0021-observability-optimization-hardening-architecture.md
├── 0022-workflow-optimization-hardening-architecture.md
├── 2026-03-26-10-communication-standardization.md # Communication 문서 표준화 계획
├── 2026-03-26-11-laboratory-standardization.md # Laboratory 문서 표준화 계획
└── README.md                                 # This file
```

## How to Work in This Area

1. 시스템 아키텍처를 설계하거나 변경할 때 `docs/99.templates/ard.template.md`를 사용한다.
2. 파일명은 `####-<system-name>.md` 순차 번호 형식을 권장한다.
3. PRD의 요구사항이 어떻게 아키텍처적으로 해결되는지 매핑한다.
4. 변경 시 관련된 ADR 및 Spec 문서의 링크를 최신 상태로 유지한다.

## Documentation Standards

- 파일 단위의 세부 구현보다는 시스템 수준의 경계와 흐름에 집중한다.
- 상단에 `Overview (KR)` 요약을 포함한다.
- Mermaid 등을 활용한 시각적 다이어그램 포함을 지향한다 (권장).

## Related References

- [01.prd (Requirements)](../01.prd/README.md)
- [03.adr (Decisions)](../03.adr/README.md)
- [07-workflow Spec](../04.specs/07-workflow/spec.md)
- [11-laboratory Spec](../04.specs/11-laboratory/spec.md)
- [04.specs (Specifications)](../04.specs/README.md)
- [99.templates (Templates)](../99.templates/README.md)

---
*Maintained by Engineering Architecture Team*
