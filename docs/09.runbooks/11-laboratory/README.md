# Laboratory (11-laboratory) Runbooks

> 관리 UI 계층의 회귀 대응 및 복구 절차 인덱스.

## Overview

이 디렉터리는 `11-laboratory` 계층에서 발생하는 접근 경계 회귀, 설정 드리프트, UI 장애, 데이터 의존성 장애를 빠르게 복구하기 위한 절차 문서를 모은다. 정책 판단은 `docs/08.operations/11-laboratory/`를 따르고, 사용자 사용법은 `docs/07.guides/11-laboratory/`를 따른다.

## Audience

이 README의 주요 독자:

- Operators
- DevOps Engineers
- Incident Responders
- AI Agents

## Scope

### In Scope

- `11-laboratory` 서비스별 장애 대응 절차
- 복구 전 점검, 검증, rollback 기준
- 운영 정책과 guide 문서 연결

### Out of Scope

- 장기 운영 정책 정의
- 일반 사용 튜토리얼
- postmortem 또는 incident timeline 원문
- 사용자의 승인 없는 destructive cleanup

## Structure

```text
11-laboratory/
├── dashboard.md              # Homer dashboard recovery
├── dozzle.md                 # Dozzle recovery
├── open-notebook.md          # Open Notebook and SurrealDB recovery
├── optimization-hardening.md # Laboratory hardening regression recovery
├── portainer.md              # Portainer recovery
├── redisinsight.md           # RedisInsight recovery
└── README.md                 # This file
```

## Runbook Index

- [Optimization Hardening Runbook](./optimization-hardening.md): middleware/allowlist/network/socket/direct exposure 회귀 복구
- [Open Notebook Runbook](./open-notebook.md): Open Notebook UI, SurrealDB, secret, volume 문제 복구
- [Portainer Runbook](./portainer.md): 관리자 계정/서비스 복구
- [RedisInsight Runbook](./redisinsight.md): 데이터 UI 연결/설정 복구
- [Dozzle Runbook](./dozzle.md): 로그 스트림/서비스 복구
- [Dashboard Runbook](./dashboard.md): Homer 설정/렌더링 복구

## When to Use

- `laboratory-hardening` CI 실패
- 관리 UI 접근 실패(403/401/라우팅 실패)
- 실수로 direct 노출/권한 확대가 반영된 경우
- compose 경계(`infra_net`) 또는 하드닝 계약이 깨진 경우
- laboratory 서비스의 backing data store 또는 secret 주입이 실패한 경우

## How to Work in This Area

1. 복구 절차를 작성하기 전에 관련 operation policy와 service compose file을 확인한다.
2. 새 런북은 `docs/99.templates/runbook.template.md`를 기준으로 작성한다.
3. 명령은 즉시 실행 가능한 순서로 쓰고, destructive action은 사용자 승인 조건을 명시한다.
4. 문서 추가/삭제 후 이 README의 `Structure`와 `Runbook Index`를 갱신한다.

## Related References

- **PRD**: [../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.ard/0025-laboratory-optimization-hardening-architecture.md](../../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/11-laboratory/spec.md](../../04.specs/11-laboratory/spec.md)
- **Guide Index**: [../../07.guides/11-laboratory/README.md](../../07.guides/11-laboratory/README.md)
- **Operations Index**: [../../08.operations/11-laboratory/README.md](../../08.operations/11-laboratory/README.md)
- **Template**: [../../99.templates/runbook.template.md](../../99.templates/runbook.template.md)
