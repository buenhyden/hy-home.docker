---
profile_id: architecture-description
status: active
artifact_id: AD-0028
artifact_type: architecture-description
parent_ids:
  - REQ-0025
created: 2026-07-19
updated: 2026-08-10
---
# Operational Readiness Closure Architecture Description

## Context and Stakeholders

이 Architecture Description는 PRD 025의 네 로컬 실행 lane을 하나의 격리·evidence architecture로
정렬한다. 각 lane의 요구사항 소유권은 Specs 124-127에 남으며, 이 문서는
공통 runtime boundary, artifact flow, evidence promotion, failure containment를
정의한다.

Architecture의 핵심은 tracked source와 transient runtime material을 분리하는
것이다. tracked scripts, policies, schemas, fixtures, Specs/Plans/Tasks가 실행을
정의하고, `_workspace/repo-support/<task-id>/`는 ignored non-secret scratch만
일시 staging한다. Secret, private key, token, raw auth/log는 `/tmp` 또는
process-local environment에만 존재하며 durable evidence로 승격되지 않는다.

## Stakeholders and Concerns

요구사항 소유자, 구현자와 운영자는 이 절과 후속 뷰에 기록된 관심사를 공유한다. 여기서는 기존 문서에서 확인되는 관심사만 다룬다.

| Stakeholder | Primary concern | Architecture response |
| --- | --- | --- |
| Repository maintainer | 완료 claim과 실제 evidence 일치 | stable IDs, Task evidence, validation ladder, honest lifecycle |
| Infrastructure owner | 다른 Docker workload 및 state 보호 | unique project identity, labels, bounded volumes, scoped cleanup |
| Operations/data owner | representative recovery의 무결성 | synthetic state, explicit source/target versions, integrity oracle |
| Security reviewer | artifact identity와 trust evidence 결합 | digest-bound SBOM, policy, provenance, signature, negative fixtures |
| Release owner | gate를 통과한 artifact만 promotion | immutable digest, canary isolation, health gate, previous-digest rollback |
| AI agent/reviewer | 권한·stop rule·검증 경계 명확성 | active Spec/Plan/Task input, fail-closed wrappers, separate reviews |

## System Boundaries

이 절은 현재 문서가 이미 기록한 시스템 경계, 소비 관계, non-goal과 제약을 보존한다.

- **Owned boundary**: repository-local, task-scoped Docker runtime and tracked
  harness changes required by Specs 124-127.
- **Runtime boundary**: `core` five-service Compose set plus a separate
  representative PostgreSQL path and sample-service deployment path.
- **Artifact boundary**: `examples/sample-web-service` image and derived
  digest-bound SBOM, scan verdict, provenance statement, signature bundle.
- **State boundary**: synthetic PostgreSQL fixture and task-owned temporary
  backup/restore volumes only.
- **Remote boundary**: OpenSSF Scorecard read-only observation only. Registry,
  GitHub, deployment, publication, identity, credential, and settings mutation
  remain outside this architecture.
- **Evidence boundary**: tracked definitions and concise Task summaries are
  durable; raw generated artifacts remain ignored or CI-retained according to
  the Plan.
- **Cleanup boundary**: scripts may remove only resources matching the exact
  task project identity and labels they created.

This Architecture Description does not authorize commands by itself. Each runtime lane requires an
active Spec, approved Plan, active Task, exact command envelope, rollback, and
human approval evidence.

## Quality Attributes

### Quality Scenarios

품질 시나리오는 아래 속성이 적용되는 기존 구성, 실패 경계와 연결된 검증 기대를 가리킨다. 구체적인 실행 증거는 관련 Spec과 Operations 문서가 소유한다.

- **Isolation**: no shared project name, implicit default profile, host-global
  tool installation, or unscoped Docker cleanup.
- **Reliability**: startup and health converge within explicit timeouts;
  failures produce stable codes and deterministic cleanup attempts.
- **Security**: least privilege, no durable private key or secret, digest-bound
  verification, fail-closed mismatches, redacted evidence.
- **Reproducibility**: pinned tool/image identities, versioned policies,
  synthetic fixtures, idempotent wrappers, declared prerequisites.
- **Observability**: each lane emits scenario ID, subject identity, timing,
  state transition, exit status, cleanup result, and concise error class.
- **Recoverability**: configuration rollback and data recovery are separate;
  unknown state stops automatic cleanup or promotion.
- **Maintainability**: common wrapper primitives are shared, while requirement
  and evidence ownership remains in the four canonical Specs.

## Components

### Viewpoints and Views

이 절의 컨텍스트, 구성 요소 또는 배치 표현을 해당 관심사의 뷰로 사용한다.

### Control view

```text
PRD 025
  -> Architecture Description 0028
    -> ADR 0028
      -> Spec 124 -> Compose acceptance result
      -> Spec 126 -> artifact verification verdict
      -> Spec 125 -> state recovery result
      -> Spec 127 -> promotion/rollback result
        -> Stage 04 Task evidence and validation closure
```

Specs 124 and 126 may execute after the common architecture and task gates are
ready. Spec 125 consumes Spec 124 readiness for its PostgreSQL rehearsal. Spec
127 consumes the verified artifact verdict from Spec 126, runtime readiness
from Spec 124, and recovery boundary from Spec 125.

### Runtime view

| Lane | Isolated runtime | Primary subject | Result consumer |
| --- | --- | --- | --- |
| Compose acceptance | Unique Compose project and synthetic overlay | `core` five-service set | Spec 125 and Spec 127 readiness gates |
| Supply chain | Digest-pinned tool containers | sample-service image digest | Spec 127 promotion gate |
| Recovery | Separate old/new PostgreSQL projects and volumes | synthetic schema/data fixture | Spec 127 rollback decision |
| Delivery | Baseline and canary sample-service projects | verified sample-service digest | Local stable target and Task evidence |

### Failure-containment view

Every wrapper follows `preflight -> allocate -> execute -> verify -> summarize ->
cleanup`. A failure skips no required verification, records a stable class,
attempts only owned cleanup, and exits non-zero. Cleanup ambiguity or evidence
redaction failure is itself a blocking failure.

## Data Flow

### Data and Control Flows

데이터 및 제어 흐름은 이 절과 기존 인프라·배치 설명에 명시된 상호작용만 포함한다.

### Durable tracked data

- tool and image version/digest registry;
- policy, schema, exception format, deterministic positive/negative fixtures;
- harness scripts and tests;
- Spec, Plan, Task, review, commit, and validation summaries.

### Transient data

- Compose logs, generated SBOM and scan output, vulnerability database/cache;
- provenance/signature working files and ephemeral key material;
- PostgreSQL data volumes, dump/restore files, local container state;
- Scorecard raw output and local deployment runtime artifacts.

Non-secret transient output may use ignored
`_workspace/repo-support/<task-id>/`. Secret-bearing or raw authentication
material must use `/tmp` or process-local memory and be removed by the owning
process. Task evidence records only redacted summaries and hashes needed to
corroborate results.

The architecture prefers digest-pinned containerized Syft, Grype, Cosign, and
Scorecard execution so the host requires Docker but no global installation.
Network-independent policy fixtures remain the CI decision owner. Live
vulnerability and Scorecard observations include freshness metadata and never
silently replace deterministic gates.

## Traceability

| PRD requirement set | Architecture owner | Decision/spec consumer |
| --- | --- | --- |
| `REQ-0025-FR-0001`–`REQ-0025-FR-0002` | Isolated Compose runtime boundary | ADR 0028, Spec 124 |
| `REQ-0025-FR-0003` | Representative state and recovery boundary | ADR 0028, Spec 125 |
| `REQ-0025-FR-0004`–`REQ-0025-FR-0006` | Digest-bound supply-chain boundary | ADR 0028, Spec 126 |
| `REQ-0025-FR-0007`–`REQ-0025-FR-0008` | Local delivery and rollback boundary | ADR 0028, Spec 127 |
| `REQ-0025-FR-0009`–`REQ-0025-FR-0010` | SDLC and evidence-promotion boundary | Specs 124-127 and Stage 04 |

ADR 0028 records the selected local-isolated strategy. Specs own detailed
interfaces, failure modes, and acceptance criteria. Plans own prospective
commands and sequencing. Tasks alone own actual results.

## AI Agent Architecture

- A fresh implementation agent receives one task-owned lane, exact allowed
  paths, runtime identities, command envelope, and stop conditions.
- A specification reviewer verifies requirement and scope compliance before a
  quality/security reviewer evaluates implementation and tests.
- Agents exchange only non-secret transient handoff files through
  `_workspace/repo-support/` and promote durable outcomes to the Task.
- Runtime wrappers must expose dry-run or preflight behavior where meaningful,
  unique project identity, timeout, cleanup status, and stable exit classes.
- Direct all-files pre-commit execution is prohibited. The final clean-worktree
  gate uses the controlled repository wrapper and records reviewed evidence.
- No model or provider receives broader runtime, secret, remote, or deployment
  authority through this architecture.

## Deployment View

Existing architecture details above remain authoritative for this view.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/0025-operational-readiness-closure.md)
- **ADR**: [ADR-0028 local-isolated readiness evidence](../decisions/0028-local-isolated-readiness-evidence.md)
- **Compose Spec**: Spec 124
- **Infrastructure Spec**: Spec 125
- **Supply-chain Spec**: Spec 126
- **Deployment Spec**: Spec 127
- **Workspace support contract**: [`_workspace`](../../../_workspace/README.md)
- **Docker Compose readiness guidance**: [Startup order](https://docs.docker.com/compose/how-tos/startup-order/)
- **Sigstore verification guidance**: [Verifying signatures](https://docs.sigstore.dev/cosign/verifying/verify/)
