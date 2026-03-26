# Gateway Tier Operations

> Governance and control rules for the edge routing infrastructure.

## Overview

This directory defines the operational policies for the `01-gateway` tier. It regulates security controls, availability standards, and change management processes for the ingress traffic paths of the `hy-home.docker` ecosystem.

## Overview (KR)

이 디렉토리는 `01-gateway` 티어의 운영 정책을 정의한다. 트래픽 인입 경로의 보안성, 가용성, 그리고 변경 관리 프로세스에 대한 통제 기준을 규정한다.

## Audience

이 문서의 주요 독자:

- Operators
- SREs
- Security Auditors
- AI Agents

## Policy Table

## Scope

### In Scope

- SSO enforcement policies
- Traffic management standards
- Configuration compliance rules for gateway components

### Out of Scope

- Step-by-step recovery procedures (handled in `docs/09.runbooks`)
- How-to guides (handled in `docs/07.guides`)

## Structure

```text
01-gateway/
├──- [Nginx](nginx.md): Nginx Gateway operations policy.
- [Traefik](traefik.md): Traefik Edge Router operations policy.
└── README.md       # This file
```

## Related Documents

- [01-gateway Root README](../../../infra/01-gateway/README.md)
- [Gateway Runbooks](../../09.runbooks/01-gateway/README.md)
- [Incident Records](../../10.incidents/README.md)

---

## AI Agent Guidance

1. Follow the `operation.template.md` for any new policy document.
2. Link policies to their corresponding ARDs and Runbooks.
3. Do not create redundant policy documents if a higher-level policy already covers the scope.
