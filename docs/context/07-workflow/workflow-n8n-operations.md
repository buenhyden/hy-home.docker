---
layer: infra
---
# n8n Workflow Operations Tracking
n**Overview (KR):** n8n 워크플로우의 실행 실패 추적 및 워커 관리 운영 지침입니다.

> This document serves as the permanent, historical record for production events, scaling efforts, and stability metrics related to the distributed `n8n` workflow orchestration system.

## Golden Rules

- **Mandatory Tracking**: Any execution freeze or webhook delivery failure MUST be documented here with links to `runbooks/incidents/`.
- **Performance Budget**: Log whenever the `n8n-worker` queue surpasses 1,000 backlog items or takes longer than 15 minutes to clear.

## Operations History

### 2026-02-23: Distributed Queue Implementation

**Status**: Stable / High Performance
**Context**: We migrated n8n from an embedded process to a robust distributed `Queue Mode` utilizing `Valkey` as the message broker.
**Observed Metrics**:

- Main (Webhook receiver) can comfortably process 300+ req/s.
- `n8n-worker` instances scale cleanly without race conditions.

---
*End of current logs*
