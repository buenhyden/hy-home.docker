---
profile_id: spec
status: completed
artifact_id: SPEC-0094
artifact_type: spec
parent_ids:
  - AD-0027
created: 2026-07-05
updated: 2026-09-01
---
# Harness and Agent-first Engineering Outcome

## Overview

This completed change aligned repository Agent behavior, provider projections,
hooks, and validation with one canonical governance model.

## Boundaries and Inputs

The change covered repository-local Agent instructions and harness mechanics.
It did not authorize user-global configuration, credential access, deployment,
or runtime mutation.

## Behavior Contract

- Stage 00 policies, roles, skills, and Provider Registry are canonical.
- .agents/, .claude/, and .codex/ are projections or native runtime mechanics.
- Active repository work loads its governing Spec Package and current Task.
- Hooks route policy decisions and cannot create new policy.

## Technical Approach

Canonical Markdown sources are rendered into provider-native surfaces and
checked for source, name, scope, and content parity. Focused validators and the
registered public suites report drift.

## Interfaces and Data

The durable interfaces are Stage 00, Provider Registry, provider adapters,
hook configuration, and the script manifest. Generated projections remain
consumers of canonical sources.

## Failure Modes and Guardrails

Projection drift, a missing canonical source, an unsupported provider surface,
or a broadened permission boundary fails closed. This completed Spec is not a
provider policy source.

## Acceptance Contract

Provider projections identify their canonical source, Stage 00 and Stage 99
have separate authority, and current governance gates validate the tracked
surface without historical fixtures.

## Traceability

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0029](../../02.architecture/decisions/0029-workspace-governance-authority.md)
- [Harness Operations](../../05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/guide.md)
