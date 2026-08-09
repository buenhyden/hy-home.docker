---
status: active
artifact_id: adr-0028
artifact_type: adr
parent_ids:
  - ad-0028
created: 2026-07-19
updated: 2026-08-10
---
# ADR-0028: Local-Isolated Readiness Evidence Strategy

## Context and Decision Drivers

Specs 124-127 define genuine gaps that static documentation and CI rendering do
not close: observed Compose readiness, representative state recovery,
digest-bound supply-chain verification, and deployment promotion/rollback.
Their earlier draft state intentionally left runtime target, toolchain, artifact,
state, and evidence boundaries unresolved.

The chosen strategy must satisfy the following drivers.

- Produce real execution evidence without changing production, shared runtime,
  remote control planes, registries, or credentials.
- Bind every supply-chain and delivery verdict to an immutable artifact digest.
- Use synthetic state and task-owned resources so failure injection and cleanup
  have bounded blast radius.
- Keep network-dependent security observations useful but prevent them from
  making CI nondeterministic.
- Preserve canonical requirement ownership in Specs 124-127 instead of adding
  a duplicate umbrella specification.
- Support fresh implementation and independent review agents with concise,
  non-secret Task evidence and logical commits.

The user approved the staged full program, local-isolated completion depth,
progressive `core` plus PostgreSQL runtime scope, `examples/sample-web-service`
as the supply-chain/delivery artifact, digest-pinned containerized tools, and
read-only remote Scorecard observation on 2026-07-19.

## Considered Options

### Option 1: Contract-first vertical slices in local isolation

Resolve the shared PRD/Architecture Description/ADR chain, then complete Spec 124, Spec 126, Spec
125, and Spec 127 as independently reviewed vertical slices. Use task-owned
Compose projects, synthetic fixtures, digest-pinned tool containers, and local
promotion/rollback.

- Advantages: smallest blast radius, honest evidence, clear dependency order,
  independent rollback and review, no remote mutation.
- Trade-offs: does not prove production topology, full profile coverage, remote
  release controls, or live recovery objectives.

### Option 2: Parallel domain implementation

Implement all four domains concurrently after a lightweight shared contract.

- Advantages: shorter apparent elapsed time and less sequential waiting.
- Trade-offs: competing evidence formats, duplicated wrappers, incompatible
  artifact/state identities, and larger integration/review risk.

### Option 3: Remote control-plane and deployment-first validation

Configure registries, GitHub Environments/Releases, branch rules, deployment
targets, signing identity, and live recovery paths in the first program.

- Advantages: stronger production realism and direct remote control evidence.
- Trade-offs: credential and secret handling, irreversible or broad mutation,
  availability risk, non-deterministic external state, and authority beyond the
  approved local scope.

## Decision

Adopt **Option 1: contract-first vertical slices in local isolation**.

The execution order is:

1. Reconcile the Stage 01-04 chain and current audit evidence.
2. Implement Spec 124 for an exact `core` five-service set in a uniquely named
   Compose project with synthetic configuration, readiness observation,
   bounded failure injection, and owned teardown.
3. Implement Spec 126 for `examples/sample-web-service` using digest-pinned
   Syft, Grype, and Cosign containers; create digest-bound SBOM, vulnerability
   verdict, SLSA/in-toto-style provenance, local blob signature, verification,
   and negative fixtures.
4. Implement Spec 125 with synthetic PostgreSQL state, logical backup/restore,
   representative major-version upgrade, integrity comparison, and recovery
   failure paths.
5. Implement Spec 127 with separate local baseline and canary projects,
   required readiness and supply-chain gates, promotion by verified digest,
   injected failure, and previous-digest rollback.
6. Reconcile Task evidence and lifecycle state, then run the complete
   validation ladder and controlled all-files wrapper from a clean worktree.

OpenSSF Scorecard may perform a read-only remote observation. Its live result is
advisory evidence; versioned local policy and fixtures own deterministic CI
pass/fail behavior. No registry push, artifact publication, keyless OIDC
signing, GitHub setting change, deployment, or credential modification is
authorized.

Generated runtime material stays ignored under the approved repo-support
boundary or process-local temporary storage. Durable Task evidence contains
only commands, exit status, tool/image identity, subject digest, concise result,
review, commit, and deferred-work disposition.

## Consequences

### Positive consequences

- The four audit gap groups gain reproducible execution evidence without
  conflating static validation with observed behavior.
- Each lane has an immutable subject, explicit consumer, negative path, and
  cleanup boundary.
- Supply-chain and delivery checks share one sample artifact while keeping
  requirement ownership separate.
- Remote availability cannot make the blocking CI gate flaky.
- Task evidence can distinguish locally completed requirements from remote or
  live follow-up work.

### Trade-offs and limitations

- The `core` five-service rehearsal does not represent all profiles or services.
- Logical PostgreSQL upgrade does not prove every extension, vendor image,
  physical backup, HA topology, or production RTO/RPO.
- Local blob signing proves subject binding and verifier behavior but not
  remote registry attachment, OIDC identity, transparency-log, or release trust.
- Local canary and rollback prove orchestration mechanics but not production
  traffic management, GitHub Environment protection, or a real Release event.
- Vulnerability and Scorecard live observations remain time-sensitive and
  require recorded freshness and later revalidation.

## Confirmation

The decision is confirmed only when all of the following hold.

- PRD 025, Architecture Description 0028, this ADR, and Specs 124-127 have valid typed metadata and
  traceability.
- Each implementation lane has an approved Plan, active Task, exact runtime
  scope, cleanup, rollback, and evidence contract before executing commands.
- Targeted deterministic tests cover success, mismatch/tamper, timeout,
  integrity failure, cleanup, and rollback paths.
- Docker resources created by a rehearsal are identified and removed without
  affecting other projects.
- Metadata, lifecycle, traceability, implementation alignment, repository
  contracts, diff hygiene, and the controlled clean-worktree all-files gate pass.
- Separate spec-compliance, quality/security, and final whole-branch reviews
  report no unresolved blocking findings.

Completion of local acceptance does not automatically complete a Spec whose
remote or live criteria remain unresolved. Those items stay active and receive
a separately approved follow-up artifact.

## Follow-up Decisions

- Select and pin exact container image digests and policy schema versions in the
  implementation Plan after verifying current official releases.
- Approve any test-only Compose overlay, healthcheck, port, resource, or
  initialization change before runtime execution.
- Define whether later registry publication uses keyless identity, managed key,
  or another trust model in a separate security ADR.
- Define production backup formats, encryption, retention, HA recovery, and
  RTO/RPO commitments in a separate infrastructure decision.
- Define remote deployment environments, separation of duties, release
  publication, traffic strategy, and GitHub controls in a separate delivery ADR.

## Related Documents

- **PRD**: [Operational readiness closure](../../01.requirements/prd-025-operational-readiness-closure.md)
- **Architecture Description**: [Operational readiness closure architecture](../descriptions/ad-0028-operational-readiness-closure.md)
- **Compose Spec**: [Spec 124](../../98.archive/03.specs/124-compose-runtime-readiness-remediation/spec.md)
- **Infrastructure Spec**: [Spec 125](../../98.archive/03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- **Supply-chain Spec**: [Spec 126](../../98.archive/03.specs/126-security-supply-chain-remediation/spec.md)
- **Deployment Spec**: [Spec 127](../../98.archive/03.specs/127-deployment-release-engineering-remediation/spec.md)
- **Audit matrix**: [Canonical implementation matrix](../../90.references/data/governance/audit-implementation-matrix.md)
- **Docker Compose**: [Startup order](https://docs.docker.com/compose/how-tos/startup-order/)
- **Syft**: [SBOM generator](https://github.com/anchore/syft)
- **Grype**: [Vulnerability scanner](https://github.com/anchore/grype)
- **Cosign**: [Signing and verification](https://github.com/sigstore/cosign)
- **OpenSSF Scorecard**: [Security health metrics](https://github.com/ossf/scorecard)
- **SLSA**: [Provenance v1.2](https://slsa.dev/spec/v1.2/provenance)
