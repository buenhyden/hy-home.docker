# Gateway Tier Runbooks

# Gateway Runbooks

> Immediate operational procedures and recovery steps for Gateway infrastructure (01-gateway).

## Overview

이 디렉토리는 `01-gateway` 계층(Traefik, Nginx)의 운영 이슈 발생 시 즉시 실행 가능한 런북을 관리한다. 설정 리로드, 인증 문제 해결, 파일 업로드 최적화, 그리고 상태 진단을 위한 단계별 절차를 제공한다.

## Audience

이 README의 주요 독자:

- Operators
- SRE / DevOps Engineers
- AI Agents

## Scope

### In Scope

- Step-by-step recovery procedures
- Configuration reload checklists
- Healthcheck failure diagnostic steps

### Out of Scope

- General system guides (handled in `docs/07.guides`)
- Governance and approval standards (handled in `docs/08.operations`)

## Structure

```text
01-gateway/
├── nginx.md       # [Nginx](nginx.md): Nginx Gateway runbook.
├── traefik.md     # [Traefik](traefik.md): Traefik Edge Router runbook.
└── README.md       # This file
```

## Related Documents

- [01-gateway Root README](../../../infra/01-gateway/README.md)
- [Gateway Operations](../../08.operations/01-gateway/README.md)
- [Incident Records](../../10.incidents/README.md)

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
