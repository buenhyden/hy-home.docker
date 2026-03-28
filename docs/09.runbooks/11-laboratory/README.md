# Laboratory (11-laboratory) Runbook

> 관리 UI 계층의 회귀 대응 및 복구 절차 인덱스.

## Overview (KR)

이 런북 인덱스는 `11-laboratory` 계층에서 발생하는 접근 경계 회귀, 설정 드리프트, UI 장애를 빠르게 복구하기 위한 절차 문서를 모은다.

## Runbook Index

- [Optimization Hardening Runbook](./optimization-hardening.md): middleware/allowlist/network/socket/direct exposure 회귀 복구
- [Portainer Runbook](./portainer.md): 관리자 계정/서비스 복구
- [RedisInsight Runbook](./redisinsight.md): 데이터 UI 연결/설정 복구
- [Dozzle Runbook](./dozzle.md): 로그 스트림/서비스 복구
- [Dashboard Runbook](./dashboard.md): Homer 설정/렌더링 복구

## When to Use

- `laboratory-hardening` CI 실패
- 관리 UI 접근 실패(403/401/라우팅 실패)
- 실수로 direct 노출/권한 확대가 반영된 경우
- compose 경계(`infra_net`) 또는 하드닝 계약이 깨진 경우

## Related Operational Documents

- **PRD**: [../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.ard/0025-laboratory-optimization-hardening-architecture.md](../../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/11-laboratory/spec.md](../../04.specs/11-laboratory/spec.md)
- **Plan**: [../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/11-laboratory/optimization-hardening.md](../../07.guides/11-laboratory/optimization-hardening.md)
- **Operations**: [../../08.operations/11-laboratory/optimization-hardening.md](../../08.operations/11-laboratory/optimization-hardening.md)
