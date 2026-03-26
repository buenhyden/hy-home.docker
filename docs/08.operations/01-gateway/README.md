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

| [README.md](./README.md) | Tier-level operational overview and global controls |
| [traefik.md](./traefik.md) | Specific operational policy for the Traefik router |
| [nginx.md](./nginx.md) | Specific operational policy for the Nginx secondary proxy |

## Usage Instructions

This area contains governance documents. Before making infrastructure changes in `infra/01-gateway`, verify that the proposed changes comply with the policies defined here.

## Verification and Monitoring

- **Status Check**: Use the [Traefik Dashboard](https://dashboard.${DEFAULT_URL}) for real-time routing status.
- **Security Check**: Verify TLS termination and certificate validity regularly.
- **Runbooks**: Refer to [09.runbooks/01-gateway/README.md](../../09.runbooks/01-gateway/README.md) for execution steps during deviations.

## Related References

- **ARD**: [../../02.ard/README.md](../../02.ard/README.md)
- **Guides**: [../../07.guides/01-gateway/README.md](../../07.guides/01-gateway/README.md)
- **Runbooks**: [../../09.runbooks/01-gateway/README.md](../../09.runbooks/01-gateway/README.md)

---

## AI Agent Guidance

1. Follow the `operation.template.md` for any new policy document.
2. Link policies to their corresponding ARDs and Runbooks.
3. Do not create redundant policy documents if a higher-level policy already covers the scope.
