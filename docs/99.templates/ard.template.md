<!-- Target: docs/02.ard/####-<system-or-domain-name>.md -->
# [System or Domain Name] Architecture Reference Document (ARD)

> Use this template for `docs/02.ard/####-<system-or-domain-name>.md`.
>
> Rules:
>
> - Keep ARD architectural.
> - File-level implementation detail belongs in the Spec.
> - Use one `Overview (KR)` summary near the top.

---

# [System or Domain Name] Architecture Reference Document

## Overview (KR)

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

- **PRD**: `[../01.prd/YYYY-MM-DD-<feature-or-system>.md]`
- **Spec**: `[../04.specs/<feature-id>/spec.md]`
- **Plan**: `[../05.plans/YYYY-MM-DD-feature.md]`
- **ADR**: `[../03.adr/####-<short-title>.md]`
