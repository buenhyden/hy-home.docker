<!-- Target: docs/03.specs/010-tooling/README.md -->

# 09-tooling Specifications

> 개발 및 운영 도구 서비스 기술 사양

## Overview

`docs/03.specs/010-tooling`는 SonarQube, Terraform, Terrakube, k6, Locust, Registry, Syncthing 등 도구 서비스의 기술 사양을 포함합니다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- QA Engineers
- AI Agents

## Scope

### In Scope

- 코드 품질, IaC 실행, 성능 테스트, 레지스트리, 동기화 서비스 사양
- 도구 통합 인터페이스 및 접근 경계

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/09-tooling/` 담당)

## Structure

```text
09-tooling/
├── spec.md      # Tooling services technical specification
└── README.md    # This file
```

## How to Work in This Area

1. 구현 또는 검증 전 [spec.md](./spec.md)를 먼저 확인합니다.
2. 상위 요구사항과 아키텍처 맥락은 Related Documents의 PRD/ARD/ADR 링크에서 추적합니다.
3. 새 child contract가 필요하면 `docs/99.templates`의 대응 템플릿을 사용하고 이 폴더 README를 함께 갱신합니다.
4. 운영 절차, 정책, runbook 내용은 `docs/05.operations/`에 두고 여기에는 구현 계약만 유지합니다.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/09-tooling/README.md](../../../infra/09-tooling/README.md)
- [docs/05.operations/guides/09-tooling/](../../05.operations/guides/09-tooling/)
