# Operations Knowledge Base

> 운영 정책, 사용 절차, 복구 절차를 하나의 canonical stage에서 관리한다.

## Overview

`docs/07.operations`는 기존 guide, policy, procedure stage를 통합한 운영 지식 베이스다. 각 문서는 사용 맥락, 운영 통제, 실행 절차, 검증 기준을 한 위치에서 제공한다.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- SREs
- Security Officers
- AI Agents

## Scope

### In Scope

- 서비스별 사용 방법과 운영 절차
- 운영 정책, 통제 기준, 예외 처리 기준
- 장애 복구, 정기 점검, 검증 절차
- 운영 자동화 스크립트 실행 기준
- AI Agent가 참조할 canonical operations context

### Out of Scope

- 제품 요구사항과 사용자 가치 정의 (`01.prd` 담당)
- 아키텍처 참조 모델과 결정 기록 (`02.ard`, `03.adr` 담당)
- 상세 기술 명세 (`04.specs` 담당)
- 구현 계획과 작업 증거 (`05.plans`, `06.tasks` 담당)
- 실제 사고 기록과 사후 분석 (`10.incidents` 담당)

## Structure

```text
docs/07.operations/
├── 01-gateway/
├── 02-auth/
├── 03-security/
├── 04-data/
├── 05-messaging/
├── 06-observability/
├── 07-workflow/
├── 08-ai/
├── 09-tooling/
├── 10-communication/
├── 11-laboratory/
├── 12-infra-service-optimization-catalog.md
├── standardize-infra-net.md
├── harness-agent-first-engineering.md
├── harness-agent-first-engineering-validation.md
└── README.md
```

## How to Work in This Area

1. 새 운영 문서는 `../99.templates/operation.template.md`를 사용한다.
2. 한 문서 안에서 `Usage`, `Controls`, `Procedure`, `Validation`, `Related Documents`를 필요한 만큼 작성한다.
3. 운영 변경 후 `scripts/check-doc-traceability.sh`와 `scripts/check-repo-contracts.sh`를 실행한다.
4. 반복 실행 절차는 명령, 기대 결과, 실패 시 중단 기준을 함께 둔다.

## Documentation Standards

- `docs/07.operations`가 운영 지식의 canonical stage다.
- 기존 guide, policy, procedure 역할은 별도 top-level stage가 아니라 문서 내부 섹션으로 표현한다.
- 상위 계획과 하위 실행 증거 간 추적성을 유지한다.
- 사고 기록과 사후 분석은 `docs/10.incidents`에만 둔다.

## AI Agent Guidance

1. 운영·복구·사용 절차가 필요하면 이 README와 관련 service 문서를 먼저 확인한다.
2. 운영 지식의 canonical target은 항상 `docs/07.operations`다.
3. 새 문서를 만들 때는 parent README와 관련 plan/spec/task 링크를 함께 갱신한다.

## Related References

- **Docs Index**: [../README.md](../README.md)
- **Plans**: [../05.plans/README.md](../05.plans/README.md)
- **Tasks**: [../06.tasks/README.md](../06.tasks/README.md)
- **Incidents**: [../10.incidents/README.md](../10.incidents/README.md)
- **Templates**: [../99.templates/README.md](../99.templates/README.md)
