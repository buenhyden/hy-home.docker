<!-- [ID:09-tooling:sonarqube] -->
# SonarQube

> Continuous code quality inspection and security scanning.

## 1. Overview (KR)

이 서비스는 코드 정적 분석을 통해 버그, 취약점, 코드 스멜을 탐지하는 **코드 품질 분석 도구**입니다. 개발 프로세스의 품질 관리를 위해 활용됩니다.

## 2. Overview

The `sonarqube` service provides the quality gate for `hy-home.docker`. It performs deep static analysis of source code to identify technical debt, security issues, and compliance violations, ensuring high code standards across the platform.

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **sonarqube** | SonarQube 10.7 | Analysis Engine (Community) |

## 4. Networking

| Service | Port | Description |
| :--- | :--- | :--- |
| **Web UI** | `9000` | Main analysis dashboard (`sonarqube.${DEFAULT_URL}`). |
| **Internal** | `${SONARQUBE_PORT}` | Internal service communication. |

## 5. Persistence & Secrets

- **Volumes**: `sonarqube-data-volume`, `sonarqube-logs-volume`.
- **Secrets**: `sonarqube_db_password`.
- **Database**: Uses `sonarqube` database in `mng-db` (PostgreSQL).
- **Host Path**: `${DEFAULT_TOOLING_DIR}/sonarqube/data`.

## 6. File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | SonarQube service definition. |
| `README.md` | Service overview (this file). |

---

## Documentation References

- [DevOps Tooling Guide](../../../docs/07.guides/09-tooling/README.md)
- [Recovery Runbook](../../../docs/09.runbooks/09-tooling/sonarqube-recovery.md)
