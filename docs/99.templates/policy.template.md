---
status: draft
---
<!-- Target: docs/05.operations/policies/<tier>/<topic>.md -->

# {Topic Name} Policy

> Use this template for `docs/05.operations/policies/<tier>/<topic>.md`.
>
> Rules:
>
> - This document is an operations policy and must contain `## Policy Scope`, `## Controls`, and `## Review Cadence`.
> - This document is not a step-by-step guide or recovery procedure. If the primary purpose is how-to usage or recovery, write a Guide or Runbook instead.
> - Target-relative links are calculated from the copied target path, not from `docs/99.templates/`.

---

## Overview (KR)

{이 문서가 규정하는 정책의 목적과 대상, 언제 이 정책을 적용해야 하는지 설명한다.}

## Policy Scope

{List systems, configs, agents, environments, or workflows governed by this policy.}

## Controls

- **Required**: {Required state}
- **Allowed**: {Allowed variation}
- **Disallowed**: {Forbidden state}

## Exceptions

{State who may approve exceptions and what evidence must be recorded.}

## Verification

{State the checks that prove compliance.}

## Review Cadence

{Monthly, quarterly, per release, or on material change.}

---

## Related Documents

Use only links that apply to the copied target path. Delete unused examples before committing.

Domain-depth examples (two levels deep):

- [Operations index](../../README.md)
- [Usage guide](../../guides/<tier>/<topic>.md)
- [Recovery runbook](../../runbooks/<tier>/<topic>.md)

Nested-depth examples (three levels deep):

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/<tier>/<subdomain>/<topic>.md)
- [Recovery runbook](../../../runbooks/<tier>/<subdomain>/<topic>.md)
