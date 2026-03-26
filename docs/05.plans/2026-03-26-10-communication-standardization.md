<!-- Target: docs/05.plans/2026-03-26-10-communication-standardization.md -->

# Implementation Plan - 10-communication Standardization

## Goal Description
`10-communication` 계층의 문서 체계를 "Thin Root" 아키텍처 및 "Golden 5" 택소노미에 맞춰 표준화한다. 

## Proposed Changes

### Documentation Layer
#### [NEW] [2026-03-26-10-communication.md](../../01.prd/2026-03-26-10-communication.md)
#### [NEW] [0010-communication-architecture.md](../../02.ard/0010-communication-architecture.md)
#### [NEW] [0010-communication-services.md](../../03.adr/0010-communication-services.md)
#### [NEW] [spec.md](../../04.specs/10-communication/spec.md)
#### [NEW] [2026-03-26-10-communication-tasks.md](../../06.tasks/2026-03-26-10-communication-tasks.md)

### Infrastructure Layer
#### [MODIFY] [README.md](../../../infra/10-communication/README.md)
- "Golden 5" 패턴(Overview, Architecture, Integration, Operations, Governance)으로 리팩토링.

## Verification Plan
### Automated Tests
- `markdownlint`를 통한 문서 규격 검증.
- 모든 상대 경로 링크의 유효성 점검.

### Manual Verification
- AI Agent 브레인(`task.md`)과의 일관성 확인.
