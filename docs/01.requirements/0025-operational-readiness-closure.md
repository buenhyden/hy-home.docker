---
title: Operational Readiness Closure Requirements
type: sdlc/requirement
layer: requirements
status: active
owner: "@buenhyden"
artifact_id: REQ-0025
parent_ids: []
created: 2026-07-19
updated: 2026-09-01
---
# Operational Readiness Closure Requirements

## Problem and Goals

정적 문서와 Compose rendering만으로는 startup/readiness, 데이터 복구,
artifact trust, promotion/rollback 동작을 증명할 수 없다. 이 요구사항은
저장소가 소유한 sample artifact와 synthetic state를 사용해 네 동작을
로컬 격리 환경에서 재현하고, 실제로 검증한 범위를 과장 없이 기록한다.

## Stakeholders and User Needs

- Maintainer는 구현된 readiness 동작과 미승인 원격 작업을 구분해야 한다.
- Operator는 rehearsal이 다른 Docker project나 실제 데이터를 변경하지
  않는다는 보장이 필요하다.
- Security reviewer는 supply-chain 판정이 동일 image digest에 결합되었는지
  확인해야 한다.
- Release reviewer는 실패한 canary가 promotion되지 않고 이전 digest로
  rollback되는지 재현해야 한다.

## Functional Requirements

- **REQ-0025-FR-0001**: 승인된 `core` service set은 고유한 Compose project에서
  시작되어 bounded readiness 결과와 teardown 결과를 제공해야 한다.
- **REQ-0025-FR-0002**: runtime rehearsal은 synthetic configuration과 task-owned
  network·volume·project identity를 사용해야 한다.
- **REQ-0025-FR-0003**: PostgreSQL rehearsal은 synthetic state의 logical backup,
  restore, representative major-version upgrade와 integrity comparison을
  수행해야 한다.
- **REQ-0025-FR-0004**: `examples/sample-web-service`의 SBOM, vulnerability
  verdict, provenance, signature verification은 동일 image digest에 결합되고
  tamper와 identity mismatch를 거부해야 한다.
- **REQ-0025-FR-0005**: supply-chain 도구는 저장소가 선언한 version과 container
  image identity를 사용하며 host-global 설치를 요구해서는 안 된다.
- **REQ-0025-FR-0006**: network-dependent security observation은 advisory로
  구분하고 deterministic local policy와 fixture가 CI 판정을 소유해야 한다.
- **REQ-0025-FR-0007**: delivery rehearsal은 verified digest만 canary로
  배치하고 health gate를 통과한 경우에만 local stable target으로 promotion해야
  한다.
- **REQ-0025-FR-0008**: canary 또는 promotion 후 실패하면 이전 verified
  digest로 rollback하고 post-rollback health를 확인해야 한다.
- **REQ-0025-FR-0009**: 실행 결과는 active Spec Package의 current Task에
  command, scope, result, cleanup, review를 기록하고 lifecycle 상태와 일치해야
  한다.
- **REQ-0025-FR-0010**: raw runtime output은 ignored 또는 process-local 임시
  저장소에만 두고 durable evidence에는 비밀이 제거된 요약과 immutable subject
  identity만 남겨야 한다.

## Non-functional Requirements

- **REQ-0025-NFR-0011 — Isolation**: 모든 resource는 task-owned identity로
  식별되며 cleanup은 그 resource에만 적용되어야 한다.
- **REQ-0025-NFR-0012 — Security**: secret, private key, token, raw auth log,
  production data는 tracked evidence에 저장되어서는 안 된다.
- **REQ-0025-NFR-0013 — Determinism**: blocking Gate는 versioned inputs와
  fixtures로 network 없이 같은 pass/fail 결과를 재현해야 한다.
- **REQ-0025-NFR-0014 — Fail closed**: target ambiguity, digest 또는 integrity
  mismatch, cleanup failure는 성공이나 skip으로 처리해서는 안 된다.
- **REQ-0025-NFR-0015 — Traceability**: 이 Requirement, AD-0028, ADR-0028,
  구현 스크립트, Operations 절차, current Task 결과의 추적성이 유지되어야
  한다.
- **REQ-0025-NFR-0016 — Honest scope**: 로컬 rehearsal 성공은 production
  readiness, 전체 profile, live recovery, remote release 완료로 확대 해석해서는
  안 된다.

## Constraints

- 범위는 로컬 격리 Compose readiness, synthetic PostgreSQL logical recovery,
  sample-service supply chain 및 local promotion/rollback으로 제한한다.
- Production/shared runtime, 실제 데이터, registry publication, OIDC signing,
  remote GitHub 설정과 deployment는 범위 밖이다.
- 자동 cleanup은 정확히 식별된 task-owned resource에만 허용한다.

## Acceptance Criteria

- `run-compose-core-readiness.sh`가 readiness, timeout, cleanup 경계를 검증한다.
- `rehearse-postgres-logical-upgrade.sh`가 synthetic state의 backup/restore와
  integrity oracle을 검증한다.
- `verify-sample-service-supply-chain.sh`와
  `check-supply-chain-policy.py`가 digest-bound positive/negative 판정을
  검증한다.
- `rehearse-sample-service-delivery.sh`가 canary, promotion, injected failure,
  rollback을 검증한다.
- 관련 focused tests와 등록된 full profile이 통과하고 Task evidence에 비밀이나
  raw runtime log가 없다.

## Traceability

- **Architecture Description**: [AD-0028 Operational Readiness Closure](../02.architecture/descriptions/0028-operational-readiness-closure.md)
- **Decision**: [ADR-0028 Local-Isolated Readiness Evidence](../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- **Implementation**: `scripts/validation/run-compose-core-readiness.sh`,
  `scripts/lib/ops/rehearse-postgres-logical-upgrade.sh`,
  `scripts/security/verify-sample-service-supply-chain.sh`,
  `scripts/validation/check-supply-chain-policy.py`,
  `scripts/operations/rehearse-sample-service-delivery.sh`
- **Sample artifact**: `examples/sample-web-service/`
