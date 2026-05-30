<!-- README Target: docs/05.operations/policies/09-tooling/README.md -->

# Operations Policies - 09 Tooling

> 운영 통제, 보안/가용성 기준, 예외 승인 기준을 관리한다.

## Overview

`policies/09-tooling`는 `docs/05.operations`의 policy 문서를 관리합니다. 필수/허용/금지 상태, 예외 승인, 검증 기준, 검토 주기를 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 합니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 운영 controls, allowed/disallowed 상태, exception, review cadence
- 현재 경로에 속한 policy 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 사용 온보딩과 명령 순서 중심 복구 절차
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
policies/09-tooling/
├── iac-deployment-policy.md
├── k6.md
├── locust.md
├── optimization-hardening.md
├── performance-testing.md
├── registry.md
├── sonarqube.md
├── syncthing.md
├── terraform.md
├── terrakube.md
└── README.md
```

## How to Work in This Area

1. 문서 추가, 이동, 삭제 시 이 README와 관련 bucket README를 함께 갱신합니다.
2. guide는 사용 맥락, policy는 통제 기준, runbook은 반복 실행 절차만 담습니다.

## Contents

| Path | Purpose |
| --- | --- |
| [iac-deployment-policy.md](./iac-deployment-policy.md) | Iac Deployment Policy policy 문서 |
| [k6.md](./k6.md) | K6 policy 문서 |
| [locust.md](./locust.md) | Locust policy 문서 |
| [optimization-hardening.md](./optimization-hardening.md) | Optimization Hardening policy 문서 |
| [performance-testing.md](./performance-testing.md) | Performance Testing policy 문서 |
| [registry.md](./registry.md) | Registry policy 문서 |
| [sonarqube.md](./sonarqube.md) | Sonarqube policy 문서 |
| [syncthing.md](./syncthing.md) | Syncthing policy 문서 |
| [terraform.md](./terraform.md) | Terraform policy 문서 |
| [terrakube.md](./terrakube.md) | Terrakube policy 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Policies index](../README.md)
- [Operations Guides - 09-tooling](../../guides/09-tooling/README.md)
- [Operations Runbooks - 09-tooling](../../runbooks/09-tooling/README.md)
- [Incident records](../../incidents/README.md)
