# 09-tooling Specifications

> 개발 및 운영 도구 서비스 기술 사양

## Overview

`docs/03.specs/09-tooling`는 SonarQube, Terraform, Terrakube, k6, Locust, Registry, Syncthing 등 도구 서비스의 기술 사양을 포함합니다.

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

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/09-tooling/README.md](../../../infra/09-tooling/README.md)
- [docs/05.operations/guides/09-tooling/](../../05.operations/guides/09-tooling/)
