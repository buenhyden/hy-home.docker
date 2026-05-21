---
status: draft
---
<!-- Target: docs/90.references/<category>/<item>.md -->

# Reference: {Item Name}

> Use this template for non-README reference docs under `docs/90.references/<category>/<item>.md`.
>
> Rules:
>
> - Reference docs provide stable context; they do not define active policy, plans, runbooks, incidents, or runtime truth.
> - Use target-relative Markdown links for repo-local sources and Related Documents.
> - Use direct links for external sources.
> - Summarize what each source supports; do not paste long external content.
> - Do not include secret values, credentials, tokens, private keys, shell history, or raw secret logs.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.

---

## Overview (KR)

이 문서는 [주제]에 대한 참고 문서다. 느리게 변하는 기준 정보, 용어, 외부 표준 요약을 정리한다.

## Purpose

[Why this reference exists and which active docs it supports.]

## Repository Role

[How this reference supports the repository, which active docs may use it, and what it must not replace.]

## Scope

### In Scope

- [What is covered]

### Out of Scope

- [What is not covered]
- Active policy, runbook, incident timeline, runtime config source of truth

## Definitions / Facts

- **Term / Fact 1**:
- **Term / Fact 2**:

## Source Rules

- Prefer primary external sources or repo-local canonical files.
- Include a short note on what each source supports.
- Re-check external facts before using them for current decisions.

## Sources

- [Docs-local source](../../02.architecture/requirements/####-<system-or-domain-name>.md) - {What this docs-local source supports}
- [Repo-root source](../../../README.md) - {What this repo-root source supports}
- [External source](https://example.com/source) - {What this source supports}

## Maintenance

- **Owner**:
- **Review Cadence**:
- **Update Trigger**:

## Related Documents

- **Architecture**: [../../02.architecture/requirements/####-<system-or-domain-name>.md](../../02.architecture/requirements/####-<system-or-domain-name>.md)
- **Spec**: [../../03.specs/<feature-id>/spec.md](../../03.specs/<feature-id>/spec.md)
- **Operations**: [../../05.operations/README.md](../../05.operations/README.md)
