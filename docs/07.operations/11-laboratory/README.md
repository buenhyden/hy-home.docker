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
- **Usage Index**: [../../07.operations/11-laboratory/README.md](../../07.operations/11-laboratory/README.md)
- **Procedure Index**: [../../07.operations/11-laboratory/README.md](../../07.operations/11-laboratory/README.md)
- **Template**: [../../99.templates/operation.template.md](../../99.templates/operation.template.md)

## Usage

> Migrated from `docs/07.operations/11-laboratory/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Laboratory (11-laboratory) Usages

> 실험 및 관리 서비스 계층의 사용, 구성, 하드닝 가이드 인덱스.

#### Overview

이 디렉터리는 `11-laboratory` 계층의 관리 UI와 실험 도구를 안전하게 사용하는 방법을 정리한다. 각 가이드는 사람이 직접 따라 할 수 있는 접근/확인 절차를 제공하며, 운영 정책과 장애 대응 절차는 각각 `docs/07.operations/11-laboratory/`와 `docs/07.operations/11-laboratory/`에서 관리한다.

#### Audience

이 README의 주요 독자:

- Operators
- DevOps Engineers
- Developers
- Security Reviewers
- AI Agents

#### Scope

##### In Scope

- `11-laboratory` 계층 서비스별 사용/접근 가이드
- gateway, SSO, allowlist, Docker Secret 관련 사용자 확인 절차
- 서비스 문서와 운영/런북 문서 간 링크

##### Out of Scope

- 운영 통제 정책 자체
- 장애 발생 시 즉시 실행할 복구 절차
- Compose 서비스 정의 변경
- secret 값, token, credential 원문

#### Structure

```text
11-laboratory/
├── dashboard.md              # Homer dashboard guide
├── dozzle.md                 # Dozzle log viewer guide
├── open-notebook.md          # Open Notebook usage guide
├── optimization-hardening.md # Laboratory hardening guide
├── portainer.md              # Portainer management UI guide
├── redisinsight.md           # RedisInsight guide
└── README.md                 # This file
```

#### Usage Index

- [Optimization Hardening Usage](./optimization-hardening.md): gateway+allowlist+SSO 경계, 최소권한, 정책 게이트 적용 절차
- [Open Notebook Usage](./open-notebook.md): Open Notebook 및 SurrealDB 기반 노트북 작업 환경 사용
- [Portainer Usage](./portainer.md): 컨테이너 관리 UI 사용
- [RedisInsight Usage](./redisinsight.md): Redis 데이터 시각화/분석
- [Dozzle Usage](./dozzle.md): Docker 로그 모니터링
- [Dashboard Usage](./dashboard.md): Homer 서비스 대시보드 구성

#### Common Pitfalls

- allowlist CIDR 미설정으로 운영자 접근이 차단됨
- dashboard 또는 관리 UI `ports` 재노출로 인증 우회 경로가 생김
- Docker socket 쓰기 권한으로 최소권한 원칙이 깨짐
- 문서 인덱스/링크를 업데이트하지 않아 추적성이 깨짐

#### How to Work in This Area

1. 새 laboratory 서비스를 추가할 때는 먼저 `infra/11-laboratory/<service>/docker-compose.yml`과 `docs/04.specs/11-laboratory/spec.md`를 확인한다.
2. 사용자 사용 절차는 `docs/99.templates/operation.template.md`를 기준으로 이 디렉터리에 작성한다.
3. 운영 통제는 `docs/07.operations/11-laboratory/`, 복구 절차는 `docs/07.operations/11-laboratory/`에 함께 연결한다.
4. 문서 추가/삭제 후 이 README의 `Structure`와 `Usage Index`를 갱신한다.

#### Related References

- **Infra Source**: [../../../infra/11-laboratory/README.md](../../../infra/11-laboratory/README.md)
- **Spec**: [../../04.specs/11-laboratory/spec.md](../../04.specs/11-laboratory/spec.md)
- **Operations Index**: [../../07.operations/11-laboratory/README.md](../../07.operations/11-laboratory/README.md)
- **Procedures Index**: [../../07.operations/11-laboratory/README.md](../../07.operations/11-laboratory/README.md)
- **Template**: [../../99.templates/operation.template.md](../../99.templates/operation.template.md)

## Procedure

> Migrated from `docs/07.operations/11-laboratory/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Laboratory (11-laboratory) Procedures

> 관리 UI 계층의 회귀 대응 및 복구 절차 인덱스.

#### Overview

이 디렉터리는 `11-laboratory` 계층에서 발생하는 접근 경계 회귀, 설정 드리프트, UI 장애, 데이터 의존성 장애를 빠르게 복구하기 위한 절차 문서를 모은다. 정책 판단은 `docs/07.operations/11-laboratory/`를 따르고, 사용자 사용법은 `docs/07.operations/11-laboratory/`를 따른다.

#### Audience

이 README의 주요 독자:

- Operators
- DevOps Engineers
- Incident Responders
- AI Agents

#### Scope

##### In Scope

- `11-laboratory` 서비스별 장애 대응 절차
- 복구 전 점검, 검증, rollback 기준
- 운영 정책과 guide 문서 연결

##### Out of Scope

- 장기 운영 정책 정의
- 일반 사용 튜토리얼
- postmortem 또는 incident timeline 원문
- 사용자의 승인 없는 destructive cleanup

#### Structure

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

#### Procedure Index

- [Optimization Hardening Procedure](./optimization-hardening.md): middleware/allowlist/network/socket/direct exposure 회귀 복구
- [Open Notebook Procedure](./open-notebook.md): Open Notebook UI, SurrealDB, secret, volume 문제 복구
- [Portainer Procedure](./portainer.md): 관리자 계정/서비스 복구
- [RedisInsight Procedure](./redisinsight.md): 데이터 UI 연결/설정 복구
- [Dozzle Procedure](./dozzle.md): 로그 스트림/서비스 복구
- [Dashboard Procedure](./dashboard.md): Homer 설정/렌더링 복구

#### When to Use

- `laboratory-hardening` CI 실패
- 관리 UI 접근 실패(403/401/라우팅 실패)
- 실수로 direct 노출/권한 확대가 반영된 경우
- compose 경계(`infra_net`) 또는 하드닝 계약이 깨진 경우
- laboratory 서비스의 backing data store 또는 secret 주입이 실패한 경우

#### How to Work in This Area

1. 복구 절차를 작성하기 전에 관련 operation policy와 service compose file을 확인한다.
2. 새 런북은 `docs/99.templates/operation.template.md`를 기준으로 작성한다.
3. 명령은 즉시 실행 가능한 순서로 쓰고, destructive action은 사용자 승인 조건을 명시한다.
4. 문서 추가/삭제 후 이 README의 `Structure`와 `Procedure Index`를 갱신한다.

#### Related References

- **PRD**: [../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../../02.ard/0025-laboratory-optimization-hardening-architecture.md](../../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../04.specs/11-laboratory/spec.md](../../04.specs/11-laboratory/spec.md)
- **Usage Index**: [../../07.operations/11-laboratory/README.md](../../07.operations/11-laboratory/README.md)
- **Operations Index**: [../../07.operations/11-laboratory/README.md](../../07.operations/11-laboratory/README.md)
- **Template**: [../../99.templates/operation.template.md](../../99.templates/operation.template.md)
