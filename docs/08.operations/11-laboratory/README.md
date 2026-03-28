# Laboratory (11-laboratory) Operations Policy

> 실험 및 관리 서비스 노출/인증/권한/감사 정책 인덱스.

## Overview (KR)

이 문서는 `11-laboratory` 계층의 운영 통제 정책을 정의한다. 관리 UI를 안전 경계 뒤에 유지하고, 실험성 서비스의 예외/권한/감사 절차를 표준화한다.

## Policy Index

- [Optimization Hardening Policy](./optimization-hardening.md): gateway+allowlist+SSO, 최소권한, CI 게이트, 카탈로그 확장 승인 조건
- [Portainer Policy](./portainer.md)
- [RedisInsight Policy](./redisinsight.md)
- [Dozzle Policy](./dozzle.md)
- [Dashboard Policy](./dashboard.md)

## Applies To

- **Systems**: dashboard, dozzle, portainer, redisinsight
- **Agents**: Infra/DevOps/Operations agents
- **Environments**: Local, Dev, Stage, Production-like management plane

## Review Cadence

- 월 1회 정책 점검
- 접근권한/노출 정책 변경 시 즉시 리뷰

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.ard/0025-laboratory-optimization-hardening-architecture.md](../../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/11-laboratory/spec.md](../../04.specs/11-laboratory/spec.md)
- **Plan**: [../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/11-laboratory/optimization-hardening.md](../../07.guides/11-laboratory/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/11-laboratory/optimization-hardening.md](../../09.runbooks/11-laboratory/optimization-hardening.md)
