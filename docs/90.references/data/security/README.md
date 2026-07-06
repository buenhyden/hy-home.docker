---
status: active
---

<!-- Target: docs/90.references/data/security/README.md -->

# Security Reference Data

> generated security automation readiness data and security-control interpretation context

## Overview

`docs/90.references/data/security`는 보안 자동화 준비 상태와 supply-chain
security gap을 안정적인 reference data로 정리합니다. 이 폴더의 문서는
보안 policy, CI workflow, branch protection, runtime hardening, incident
procedure를 대체하지 않습니다.

## Category Role

이 category는 Stage 90 security audit과 future Stage 03/04 security
automation planning을 보조합니다. 실제 보안 통제는 `docs/00.agent-governance/`,
`.github/workflows/**`, `.github/SECURITY.md`, `scripts/`, `infra/`, 그리고
approved Stage 04 task evidence가 담당합니다.

## Audience

이 README의 주요 독자:

- Security Reviewers
- QA Engineers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Generated security automation readiness snapshots
- Repo-local evidence mapping for vulnerability gates, SBOM, attestation,
  Scorecard, workflow security, secret scanning, Dependabot, and hardening
- Security maturity audit support data

### Out of Scope

- Active security policy or incident procedure
- Live vulnerability scan results, SBOM artifacts, signatures, attestations, or
  release assets
- Remote GitHub setting assertions, registry lookups, runtime state, secret
  values, credentials, tokens, private keys, shell history, raw logs, or `.env`
  values

## Structure

```text
security/
├── README.md                         # This file
└── security-automation-readiness.md  # Generated security automation readiness snapshot
```

## Current References

- [security-automation-readiness.md](./security-automation-readiness.md) -
  generated security automation readiness snapshot for vulnerability gate,
  SBOM, provenance/attestation, Scorecard, workflow security, secret scanning,
  Dependabot, and hardening coverage

## How to Work in This Area

1. Regenerate security readiness data with
   `bash scripts/validation/generate-security-automation-readiness.sh`.
2. Check freshness with
   `bash scripts/validation/generate-security-automation-readiness.sh --check`.
3. Keep generated security data as planning evidence only.
4. Route new security controls to Stage 03 specs and Stage 04 plans/tasks before
   changing CI, scanners, SBOM generation, signing, attestation, branch
   protection, or remote GitHub state.

## Related Documents

- [reference data index](../README.md)
- [security automation readiness](./security-automation-readiness.md)
- [security framework maturity audit](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)
- [security governance research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md)
- [reference template](../../../99.templates/templates/common/reference.template.md)
