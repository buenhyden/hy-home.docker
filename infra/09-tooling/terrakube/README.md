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
