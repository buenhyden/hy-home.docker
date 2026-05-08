# Laboratory (11-laboratory) Operations

> 실험 및 관리 서비스 계층의 노출, 인증, 권한, 감사 정책 인덱스.

## Overview

이 디렉터리는 `11-laboratory` 계층의 운영 통제 정책을 정의한다. 관리 UI와 실험성 서비스는 편의성이 높지만 권한, 네트워크 노출, Docker socket, secret, 데이터 볼륨 위험이 크므로 서비스별 허용/금지 기준을 명확히 관리한다.

## Audience

이 README의 주요 독자:

- Operators
- DevOps Engineers
- Security Reviewers
- AI Agents

## Scope

### In Scope

- `11-laboratory` 서비스별 운영 통제 정책
- gateway, SSO, allowlist, secret, volume, audit 기준
- 정책과 guide/runbook 간 추적성

### Out of Scope

- 사용자를 위한 튜토리얼 절차
- 실시간 장애 복구 절차
- incident timeline 또는 postmortem
- secret 값, token, credential 원문

## Structure

```text
11-laboratory/
├── dashboard.md              # Homer dashboard operations policy
├── dozzle.md                 # Dozzle log access policy
├── open-notebook.md          # Open Notebook operations policy
├── optimization-hardening.md # Laboratory hardening policy
├── portainer.md              # Portainer operations policy
├── redisinsight.md           # RedisInsight operations policy
└── README.md                 # This file
```

## Policy Index

- [Optimization Hardening Policy](./optimization-hardening.md): gateway+allowlist+SSO, 최소권한, CI 게이트, 카탈로그 확장 승인 조건
- [Open Notebook Policy](./open-notebook.md): Open Notebook, SurrealDB, secret, volume, Traefik 노출 정책
- [Portainer Policy](./portainer.md)
- [RedisInsight Policy](./redisinsight.md)
- [Dozzle Policy](./dozzle.md)
- [Dashboard Policy](./dashboard.md)

## Applies To

- **Systems**: dashboard, dozzle, open-notebook, portainer, redisinsight
- **Agents**: Infra/DevOps/Operations agents
- **Environments**: Local, Dev, Stage, Production-like management plane

## Review Cadence

- 월 1회 정책 점검
- 접근권한/노출 정책 변경 시 즉시 리뷰

## How to Work in This Area

1. 정책을 추가하기 전에 관련 guide, runbook, Compose service definition을 확인한다.
2. 새 정책 문서는 `docs/99.templates/operation.template.md`를 기준으로 작성한다.
3. Required/Allowed/Disallowed controls를 구분하고, 예외 승인 경로를 명시한다.
4. 문서 추가/삭제 후 이 README의 `Structure`와 `Policy Index`를 갱신한다.

## Related References

- **PRD**: [../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.ard/0025-laboratory-optimization-hardening-architecture.md](../../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/11-laboratory/spec.md](../../04.specs/11-laboratory/spec.md)
- **Guide Index**: [../../07.guides/11-laboratory/README.md](../../07.guides/11-laboratory/README.md)
- **Runbook Index**: [../../09.runbooks/11-laboratory/README.md](../../09.runbooks/11-laboratory/README.md)
- **Template**: [../../99.templates/operation.template.md](../../99.templates/operation.template.md)
