---
status: draft
---
<!-- Target: docs/02.architecture/requirements/####-<system-or-domain>.md -->

# [System or Domain Name] Architecture Reference Document (ARD)

> Use this template for `docs/02.architecture/requirements/####-<system-or-domain>.md`.
>
> Rules:
>
> - Keep ARD architectural.
> - File-level implementation detail belongs in the Spec.
> - Use one `Overview` summary near the top.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.
> - Replace example links with real target-relative links, or delete unused examples before saving.
>
> Target-relative examples from `docs/02.architecture/requirements/####-<system-or-domain>.md`:
>
> - PRD: `../../01.requirements/YYYY-MM-DD-feature-or-system.md`
> - ADR: `../decisions/####-short-title.md`
> - Spec: `../../03.specs/feature-id/spec.md`
> - Plan: `../../04.execution/plans/YYYY-MM-DD-feature.md`
> - Task: `../../04.execution/tasks/YYYY-MM-DD-feature-or-stream.md`
> - Operations: `../../05.operations/README.md`

---

## Overview

이 문서는 [시스템 또는 도메인명]의 참조 아키텍처와 품질 속성을 정의한다. 시스템 경계, 책임, 데이터 흐름, 운영 관점을 정리하는 기준 문서다.

## Summary

[What this system owns and why.]

## Boundaries & Non-goals

- **Owns**:
- **Consumes**:
- **Does Not Own**:
- **Non-goals**:

## Quality Attributes

- **Performance**:
- **Security**:
- **Reliability**:
- **Scalability**:
- **Observability**:
- **Operability**:

## System Overview & Context

[High-level architecture and context.]

## Data Architecture

- **Key Entities / Flows**:
- **Storage Strategy**:
- **Data Boundaries**:

## Infrastructure & Deployment

- **Runtime / Platform**:
- **Deployment Model**:
- **Operational Evidence**:

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**:
- **Tooling Boundary**:
- **Memory & Context Strategy**:
- **Guardrail Boundary**:
- **Latency / Cost Budget**:

## Related Documents

- **PRD**: [../../01.requirements/YYYY-MM-DD-<feature-or-system>.md](../../01.requirements/YYYY-MM-DD-<feature-or-system>.md)
- **Spec**: [../../03.specs/<feature-id>/spec.md](../../03.specs/<feature-id>/spec.md)
- **Plan**: [../../04.execution/plans/YYYY-MM-DD-<feature>.md](../../04.execution/plans/YYYY-MM-DD-<feature>.md)
- **Task**: [../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md](../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md)
- **ADR**: [../decisions/####-<short-title>.md](../decisions/####-<short-title>.md)
- **Operations**: [../../05.operations/README.md](../../05.operations/README.md)
