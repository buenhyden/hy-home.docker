# standardize-infra-net Specifications

> 인프라 네트워크 표준화 사양

## Overview

`docs/03.specs/standardize-infra-net`는 Docker 네트워크 이름, 브리지/외부 네트워크 경계, 서비스 간 통신 패턴 표준화 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- Operations Engineers
- AI Agents

## Status

이 사양은 네트워크 표준화 작업(P0–P15)의 설계 사양을 보존합니다.

## Scope

### In Scope

- `infra_net` name, subnet, gateway, static IP assignment contract
- Docker Compose network boundary and preservation rules
- 관련 PRD/ARD/ADR/Plan/Task/Operations 링크

### Out of Scope

- cloud VPC, physical firewall, or host network policy
- service-specific business logic
- new network migration plan creation

## Structure

```text
standardize-infra-net/
├── spec.md      # Network standardization specification
└── README.md    # This file
```

## How to Work in This Area

1. 새 작업을 시작하기 전에 [spec.md](./spec.md)의 IP mapping과 network contract를 확인합니다.
2. 네트워크 변경은 `docker-compose.yml`, 관련 infra README, operations guide/runbook 링크를 함께 확인합니다.
3. 새 네트워크 의사결정은 이 완료 spec을 덮어쓰지 말고 새 ADR/Spec/Plan 흐름으로 추적합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [docker-compose.yml](../../../docker-compose.yml)
- [infra/README.md](../../../infra/README.md)
