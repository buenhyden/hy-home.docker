---
status: active
artifact_id: prd-025
artifact_type: prd
parent_ids: []
created: 2026-07-19
updated: 2026-08-10
---
# Operational Readiness Closure Product Requirements

## Overview

이 문서는 정적 문서·구성 검증만으로 남아 있는 Compose runtime,
infrastructure recovery, software supply chain, deployment/release engineering
격차를 안전한 로컬 실행 evidence로 전환하기 위한 제품 요구사항을 정의한다.

목표는 운영 환경이나 원격 control plane을 변경하는 것이 아니다. 저장소가
소유한 sample artifact와 synthetic state를 사용하여 startup, readiness,
backup/restore, supply-chain verification, promotion, rollback을 재현 가능하게
검증하고, 실제로 검증한 범위와 여전히 승인 대기 중인 범위를 분리하는 것이
핵심 성과다.

## Problem and Stakeholders

현재 정본 감사와 Specs 124-127은 Compose startup/readiness, representative
state recovery, SBOM/provenance/signing, deployment promotion/rollback을 실제로
관찰한 evidence가 부족하다고 분류한다. 정적 Compose rendering, 문서 존재,
CI build 성공, vulnerability audit 일부 실행은 중요한 선행 evidence지만
runtime readiness, recoverability, artifact trust, deployability를 증명하지
않는다.

주요 이해관계자는 다음과 같다.

- **Repository maintainer**: 미구현 격차와 구현 완료 범위를 명확히 구분하고
  독립적으로 검토 가능한 evidence를 필요로 한다.
- **Infrastructure and operations owner**: 로컬 rehearsal이 다른 Docker
  workload, 운영 데이터, secret, remote target에 영향을 주지 않아야 한다.
- **Security reviewer**: SBOM, vulnerability policy, provenance, signature가
  같은 immutable artifact identity에 결합되어야 한다.
- **Release owner**: 검증된 artifact만 promotion되고 실패 시 이전 digest로
  되돌아가는 경로를 확인해야 한다.
- **AI agent and reviewer**: 실행 권한, stop condition, evidence promotion,
  승인 대기 범위를 machine-checkable contract로 소비해야 한다.

주요 use case는 다음과 같다.

- Maintainer가 격리된 `core` Compose service set의 실제 readiness와 teardown을
  재현한다.
- Operations owner가 synthetic PostgreSQL state를 이전 버전에서 새 버전으로
  논리 이관하고 backup/restore 무결성을 검증한다.
- Security reviewer가 `examples/sample-web-service` image의 SBOM, vulnerability
  verdict, provenance, signature를 동일 digest에 대해 검증한다.
- Release owner가 sample service의 local canary, promotion, health verification,
  rollback을 실제로 rehearsal한다.
- Reviewer가 원격 Scorecard read-only 결과와 deterministic local CI gate를
  구분하여 해석한다.

## Requirements

### Functional requirements

- **REQ-ORC-001**: 시스템은 격리된 Compose project에서 정확히 승인된 `core`
  service set을 시작하고 observed health/readiness, timeout, failure recovery,
  teardown 결과를 기록해야 한다.
- **REQ-ORC-002**: runtime rehearsal은 synthetic secret과 전용 임시 network,
  volume, project identity를 사용하고 다른 Docker project를 변경하지 않아야
  한다.
- **REQ-ORC-003**: 시스템은 synthetic PostgreSQL state에 대해 logical backup,
  restore, representative major-version upgrade, integrity comparison, rollback
  decision을 검증해야 한다.
- **REQ-ORC-004**: `examples/sample-web-service` image에 대해 digest-bound SBOM,
  vulnerability policy verdict, provenance statement, signature verification을
  생성하고 tamper 또는 identity mismatch를 거부해야 한다.
- **REQ-ORC-005**: 공급망 도구는 호스트 전역 설치 없이 version과 container
  image digest가 고정된 wrapper를 통해 실행해야 한다.
- **REQ-ORC-006**: OpenSSF Scorecard 실제 저장소 평가는 read-only advisory로
  실행하고, CI 차단 판정은 versioned local policy와 deterministic fixture로
  수행해야 한다.
- **REQ-ORC-007**: sample service deployment rehearsal은 verified digest를
  baseline과 canary로 분리하고 health gate 통과 후에만 local stable target으로
  promotion해야 한다.
- **REQ-ORC-008**: canary 또는 promotion 후 failure 발생 시 이전 verified
  digest로 rollback하고 post-rollback health를 검증해야 한다.
- **REQ-ORC-009**: 각 실행 Wave는 승인된 Spec, prospective Plan, active Task,
  targeted validation, independent review, logical commit을 가져야 한다.
- **REQ-ORC-010**: raw runtime output은 ignored repo-support staging에만 일시
  보관하고, 장기 evidence에는 non-secret command/result summary, immutable
  identifiers, checksums, exit status만 승격해야 한다.

### Non-functional requirements

- **REQ-ORC-NFR-001 — Isolation**: 모든 runtime resource는 task-scoped identity와
  labels로 식별되어야 하며 cleanup은 그 resource에만 적용되어야 한다.
- **REQ-ORC-NFR-002 — Security**: secret value, private key, token, raw auth log,
  production data는 tracked docs와 `_workspace`에 저장되어서는 안 된다.
- **REQ-ORC-NFR-003 — Determinism**: network-independent gates는 pinned inputs와
  fixtures로 동일 pass/fail 결과를 재현해야 한다.
- **REQ-ORC-NFR-004 — Fail closed**: target ambiguity, digest mismatch, integrity
  mismatch, missing cleanup, unapproved scope expansion은 성공 또는 skip으로
  처리해서는 안 된다.
- **REQ-ORC-NFR-005 — Traceability**: PRD, Architecture Description, ADR, Specs 124-127, Plans, Tasks,
  validation evidence 사이에 stable artifact ID 기반 추적성이 유지되어야
  한다.
- **REQ-ORC-NFR-006 — Honest lifecycle**: 로컬 범위가 완료되어도 remote 또는
  live acceptance criteria가 남아 있으면 해당 Spec을 완료로 표시해서는 안
  된다.

요구사항의 근거는 2026-07-05 canonical research/audit pack, 최신 audit
implementation matrix, 사용자 승인된 2026-07-19 설계 경계다. 외부 guidance는
구현 선택의 근거이며 repository acceptance evidence를 대신하지 않는다.

## Acceptance and Verification

다음 조건이 모두 확인되면 이 PRD의 로컬 구현 목표를 충족한다.

- **VAL-ORC-001**: approved `core` service set이 isolated project에서 ready 또는
  명확한 bounded failure로 수렴하고 teardown 결과가 검증된다.
- **VAL-ORC-002**: synthetic PostgreSQL fixture의 backup, restore, logical
  upgrade 후 schema, row count, digest, constraints, representative query가
  일치한다.
- **VAL-ORC-003**: sample service의 SBOM, scan verdict, provenance, signature가
  동일 image digest에 결합되고 tampered fixture가 거부된다.
- **VAL-ORC-004**: local canary와 promotion이 required gates를 소비하고 injected
  failure 후 이전 digest rollback과 health recovery가 확인된다.
- **VAL-ORC-005**: Scorecard remote read-only 결과가 advisory로 기록되고
  network-independent policy fixture가 CI decision을 결정한다.
- **VAL-ORC-006**: metadata, lifecycle, traceability, implementation alignment,
  repository contract, targeted tests, controlled all-files QA가 통과한다.
- **VAL-ORC-007**: Task evidence에는 명령, 종료 코드, tool/image identity,
  artifact digest, result summary, review, commit, deferred remote work가
  기록되고 secret/raw log는 포함되지 않는다.

성공은 실제 운영 배포나 broad infrastructure maturity를 의미하지 않는다.
성공 지표는 네 bounded local lanes의 reproducible pass/fail evidence, scope
escape 0건, secret exposure 0건, unowned Docker resource mutation 0건이다.

## Scope and Non-goals

### In scope

- Local-isolated Compose runtime acceptance for the `core` five-service set.
- Representative PostgreSQL logical backup, restore, and major-version upgrade.
- Supply-chain verification of `examples/sample-web-service`.
- Local sample-service canary, promotion, and rollback.
- Read-only Scorecard observation plus deterministic local policy fixtures.
- Required SDLC, validation, review, and evidence harness changes.

### Out of scope and non-goals

- Production or shared-host service mutation.
- Live data migration, production backup, disaster recovery declaration, or
  organization RTO/RPO commitment.
- Registry push, artifact publication, keyless OIDC signing, GitHub settings,
  rulesets, Environments, Releases, branch protection, or remote deployment.
- Secret-value inspection, credential modification, private-key retention, or
  tracked raw logs.
- Exhaustive rehearsal of all 25 Compose profiles and all services.
- SLSA conformance-level claim, broad security maturity claim, or release event
  claim based only on local evidence.

## Risks and Dependencies

- Core services may require additional synthetic configuration or resources;
  architecture review must approve any test-only overlay before execution.
- Container-image pulls and Scorecard observation depend on network
  availability. Deterministic gates must not convert that dependency into a
  flaky CI decision.
- Vulnerability databases change over time. Policy fixtures own deterministic
  enforcement while live scans record tool/database freshness.
- Logical PostgreSQL upgrade is representative evidence, not proof for every
  vendor image, extension, physical backup, or HA topology.
- Local canary without production traffic routing proves orchestration and
  rollback mechanics only.
- Docker availability, sufficient local resources, current pinned tool images,
  and an initially clean isolated worktree are implementation dependencies.

## AI Agent Requirements

- Agents must load Stage 00 governance, the active Spec/Plan/Task chain, exact
  runtime scope, and rollback/cleanup rules before execution.
- Each logical task uses a fresh implementation agent followed by separate
  specification-compliance and quality/security reviews.
- Agents may operate only on task-owned local resources. Runtime or target
  expansion requires new approval and Task evidence.
- Agents must stop on secret exposure, target ambiguity, integrity mismatch,
  unowned resources, cleanup failure, or unexpected changed paths.
- Agents must not run `pre-commit run --all-files` directly. The final approved
  gate uses `scripts/validation/run-agent-precommit-all-files.sh` from a clean
  linked worktree.
- Read-only Scorecard observation is permitted; remote mutation, publication,
  deployment, or credential use remains separately approval-gated.

## Related Documents

- **Architecture Description**: [Operational readiness closure architecture](../02.architecture/descriptions/ad-0028-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md)
- **Compose Spec**: Spec 124
- **Infrastructure Spec**: Spec 125
- **Supply-chain Spec**: Spec 126
- **Deployment Spec**: Spec 127
- **Canonical audit matrix**: [Audit implementation matrix](../90.references/data/governance/audit-implementation-matrix.md)
- **Docker startup-order guidance**: [Control startup order](https://docs.docker.com/compose/how-tos/startup-order/)
- **SLSA provenance model**: [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)
