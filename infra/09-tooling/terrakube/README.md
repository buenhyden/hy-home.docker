<!-- [ID:09-tooling:terrakube] -->
# Terrakube IaC Automation Platform

> Enterprise-grade Terraform orchestration, remote state management, and private module registry.

## 1. Overview (KR)

이 서비스는 팀 단위의 Terraform 워크플로우를 자동화하고 중앙 집중화하는 **Terrakube 플랫폼**입니다. API 기반 실행(`executor`), 프라이빗 모듈 레지스트리, 그리고 MinIO를 이용한 보안 상태(State) 저장을 지원하며 Keycloak(DEX) 기반의 SSO 통합을 제공합니다.

## 2. Overview

Terrakube provides a centralized platform for managing Terraform workflows at scale. It handles API-driven execution via ephemeral executors, hosts a private registry for infrastructure modules, and ensures secure remote state storage using S3-compatible backends (MinIO). Integration with Keycloak ensures enterprise-ready identity and access management for IaC governance.

## 3. Tech Stack

| Component | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| **API Server** | AzBuilder API | 2.29.0 | Core Orchestration & API |
| **UI** | Terrakube UI | 2.29.0 | Management Console |
| **Executor** | AzBuilder Executor | 2.29.0 | Ephemeral Job Runner |
| **Persistence** | PostgreSQL / MinIO | - | Metadata & State Storage |

## 4. Networking

| Name | Type | Target | Description |
| :--- | :--- | :--- | :--- |
| **API** | HTTPS | `terrakube-api.${DEFAULT_URL}` | REST API and OIDC callback. |
| **UI** | HTTPS | `terrakube-ui.${DEFAULT_URL}` | Web management dashboard. |
| **Internal** | HTTP | `8080`, `8090` | Internal communication between API and Executor. |

## 5. Persistence

- **Metadata**: Managed via the `mng-db` (PostgreSQL) instance.
- **State Storage**: S3-compatible bucket `tfstate` in MinIO.
- **Secrets**: Integrated with Docker Secrets (`terrakube_db_password`, etc.).

## 6. Usage

Access the platform via the following URLs:

- **Dashboard**: `https://terrakube-ui.${DEFAULT_URL}`
- **API Docs**: `https://terrakube-api.${DEFAULT_URL}/swagger-ui.html`

## 7. File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Multi-service orchestration for the platform. |
| `README.md` | Infrastructure-level documentation (this file). |

---

## Documentation References

- **Guide**: [Terrakube System Guide](../../../docs/07.guides/09-tooling/terrakube.md)
- **Operation**: [Terrakube Operations Policy](../../../docs/08.operations/09-tooling/terrakube.md)
- **Runbook**: [Terrakube Recovery Runbook](../../../docs/09.runbooks/09-tooling/terrakube.md)

---

## Overview

`infra/09-tooling/terrakube`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

## Structure

```text
infra/09-tooling/terrakube/
├── docker-compose.yml  # Docker Compose 정의
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Related References

- [infra/README.md](../../README.md)
- [docs/07.guides/README.md](../../../docs/07.guides/README.md)
- [docs/08.operations/README.md](../../../docs/08.operations/README.md)
- [docs/09.runbooks/README.md](../../../docs/09.runbooks/README.md)
