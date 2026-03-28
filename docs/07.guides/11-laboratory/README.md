# Laboratory (11-laboratory) Guide

> 실험 및 관리 서비스(Laboratory tier) 사용/구성/하드닝 적용 가이드 모음.

## Overview (KR)

이 문서는 `11-laboratory` 계층의 운영자 UI(dashboard, dozzle, portainer, redisinsight)를 안전하게 사용하고 유지하기 위한 가이드 인덱스다. 기본 사용 가이드와 최적화/하드닝 가이드를 함께 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Operator (인프라 관리)
- DevOps Engineer
- Security Reviewer
- AI Agent

## Guide Index

- [Optimization Hardening Guide](./optimization-hardening.md): gateway+allowlist+SSO 경계, 최소권한, 정책 게이트 적용 절차
- [Portainer Guide](./portainer.md): 컨테이너 관리 UI 사용
- [RedisInsight Guide](./redisinsight.md): Redis 데이터 시각화/분석
- [Dozzle Guide](./dozzle.md): Docker 로그 모니터링
- [Dashboard Guide](./dashboard.md): Homer 서비스 대시보드 구성

## Common Pitfalls

- allowlist CIDR 미설정으로 운영자 접근이 차단됨
- dashboard `ports` 재노출로 인증 우회 경로가 생김
- dozzle docker.sock 쓰기 권한으로 최소권한 원칙이 깨짐
- 문서 인덱스/링크를 업데이트하지 않아 추적성이 깨짐

## Related Documents

- **Infra Source**: [../../../infra/11-laboratory/README.md](../../../infra/11-laboratory/README.md)
- **PRD**: [../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.ard/0025-laboratory-optimization-hardening-architecture.md](../../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/11-laboratory/spec.md](../../04.specs/11-laboratory/spec.md)
- **Plan**: [../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Operations**: [../../08.operations/11-laboratory/optimization-hardening.md](../../08.operations/11-laboratory/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/11-laboratory/optimization-hardening.md](../../09.runbooks/11-laboratory/optimization-hardening.md)
