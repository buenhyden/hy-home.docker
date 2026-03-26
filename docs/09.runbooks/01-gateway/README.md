# Gateway Tier Runbooks

: Gateway Tier Maintenance & Recovery

> Step-by-step procedures for managing and troubleshooting the gateway infrastructure.

## Overview

This directory houses the runbooks for the `01-gateway` tier. It provides infrastructure operators and AI agents with clear, executable instructions for routine maintenance and emergency recovery of the Traefik and Nginx stack.

## Overview (KR)

이 디렉토리는 `01-gateway` 티어의 유지보수 및 즉각적인 장애 대응을 위한 실행 절차(런북)를 포함한다. 서비스 재시작, 로그 분석, 상태 점검 절차 등 운영자가 즉시 따라 할 수 있는 가이드를 제공한다.

## Audience

이 문서의 주요 독자:

- Operators
- On-call Engineers
- AI Agents

## Runbook Table


| [README.md](./README.md) | Tier-level maintenance summary and daily checks |
| [traefik.md](./traefik.md) | Specific procedures for Traefik routing and TLS management |
| [nginx.md](./nginx.md) | Specific procedures for Nginx proxying and SSO integration |

## Usage Instructions

1. Identify the operational problem (e.g., 502 error, SSL expiry).
2. Locate the corresponding runbook in the table above.
3. Follow the **Procedure** steps sequentially.
4. Execute **Verification Steps** to confirm the fix.

## Verification and Monitoring

- **Signals**: Traefik dashboard, Grafana (Traefik metrics).
- **Daily Check**: Verify container health and log consistency.
- **Recovery**: Refer to the "Safe Rollback" section in each runbook if a procedure fails.

## Related References

- **Ops Policy**: [../../08.operations/01-gateway/README.md](../../08.operations/01-gateway/README.md)
- **Setup Guide**: [../../07.guides/01-gateway/01.setup.md](../../07.guides/01-gateway/01.setup.md)
- **Incident Records**: [../../10.incidents/README.md](../../10.incidents/README.md)

---

## AI Agent Guidance

1. Always use the `runbook.template.md` for new entries.
2. Ensure all commands are formatted in code blocks for direct execution.
3. Link each runbook to its corresponding Operation Policy.
