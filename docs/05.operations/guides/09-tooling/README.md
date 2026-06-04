<!-- README Target: docs/05.operations/guides/09-tooling/README.md -->

# Operations Guides - 09 Tooling

> 서비스 사용, 설정, 온보딩 문서를 domain/service 구조로 관리한다.

## Overview

`guides/09-tooling`는 `docs/05.operations`의 guide 문서를 관리합니다. 사용 맥락, 전제 조건, 일반 점검, 관련 runbook handoff를 제공한다. guide, policy, runbook 목적을 섞지 않고 필요한 운영 지식을 빠르게 찾도록 합니다.

## Audience

이 README의 주요 독자:

- Operators
- SREs
- Developers
- AI Agents

## Scope

### In Scope

- 서비스 사용 맥락, 설정 방법, 온보딩, 일반 점검
- 현재 경로에 속한 guide 문서 인덱스
- 관련 guide/policy/runbook 문서로 이동하기 위한 navigation

### Out of Scope

- 운영 통제 기준과 반복 실행 복구 절차
- 다른 bucket 또는 다른 stage가 담당하는 운영 지식
- secret 값, credential, token, 인증서 원문

## Structure

```text
guides/09-tooling/
├── 01.iac-automation.md
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
3. leaf 문서의 ID 주석은 현재 경로 tier와 같은 `09-tooling:<service>` 형식을 사용합니다.

## Contents

| Path | Purpose |
| --- | --- |
| [01.iac-automation.md](./01.iac-automation.md) | 01.Iac Automation guide 문서 |
| [k6.md](./k6.md) | K6 guide 문서 |
| [locust.md](./locust.md) | Locust guide 문서 |
| [optimization-hardening.md](./optimization-hardening.md) | Optimization Hardening guide 문서 |
| [performance-testing.md](./performance-testing.md) | Performance Testing guide 문서 |
| [registry.md](./registry.md) | Registry guide 문서 |
| [sonarqube.md](./sonarqube.md) | Sonarqube guide 문서 |
| [syncthing.md](./syncthing.md) | Syncthing guide 문서 |
| [terraform.md](./terraform.md) | Terraform guide 문서 |
| [terrakube.md](./terrakube.md) | Terrakube guide 문서 |

## Related Documents

- [Operations index](../../README.md)
- [Operations Guides index](../README.md)
- [Operations Policies - 09-tooling](../../policies/09-tooling/README.md)
- [Operations Runbooks - 09-tooling](../../runbooks/09-tooling/README.md)
- [Incident records](../../incidents/README.md)
