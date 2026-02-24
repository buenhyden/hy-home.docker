# 🏠 Hy-Home Docker Infrastructure

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

**Hy-Home Docker**는 확장 가능하고 안정적인 홈 서버 및 AI 최적화 개발 환경을 위한 **Docker 기반 인프라 프로젝트**입니다.
복잡한 마이크로서비스 아키텍처를 로컬 환경에서 손쉽게 구축하고 관리할 수 있도록 설계되었습니다.

> 📖 **자세한 문서는 [docs/README.md](docs/README.md)에서 확인하실 수 있습니다.**
> 🧭 **인프라 스택 상세는 [infra/README.md](infra/README.md)에서 확인하실 수 있습니다.**

---

## ✅ 준비 사항

- Docker Engine / Docker Desktop (WSL2 백엔드 사용 권장)
- Docker Compose v2 (CLI 기반)
- **Windows 개발 시**: 볼륨 I/O 성능 극대화를 위해 프로젝트 파일은 `/mnt/c/` 경로가 아닌 **WSL 내부 리눅스 파일 시스템(`~` 또는 `/home/user`)**에 클론해야 합니다.
- **메모리 최적화**: `.wslconfig` 파일을 통해 WSL에 할당된 램이 전체 시스템의 50~80% 정도로 제한되어 있는지 확인하는 것을 권장합니다 (`memory=16GB` 등).

---

## 🏁 빠른 시작 (Quick Start)

자세한 설치 가이드는 [Setup Guide](docs/setup/README.md)를 참조하세요.

### 1. 설정

```bash
# 저장소 루트에서
cp .env.example .env
```

- `.env` 파일 내의 각 서비스별 경로 및 포트, 비밀번호 설정을 사용자의 환경에 맞게 수정합니다.
  - `DEFAULT_URL`: 서비스 접속 도메인 (기본값: `127.0.0.1.nip.io`)
  - `DEFAULT_MOUNT_VOLUME_PATH`: 볼륨 데이터가 저장될 호스트 경로
  - `INFRA_SUBNET`, `INFRA_GATEWAY`: 내부 네트워크 대역 설정
- `secrets/` 내 `*.txt` 파일의 초기 비밀번호/토큰 값을 확인합니다.

### 2. 실행

```bash
docker compose up -d
```

### 3. 접속 예시

- **Traefik Dashboard**: `http://traefik.localhost` (또는 설정한 도메인)
- **Grafana**: `http://grafana.localhost`

### 4. 프로파일로 옵션 스택 실행

```bash
docker compose --profile ollama --profile airflow up -d
```

> 사용 가능한 프로파일 목록은 [infra/README.md](infra/README.md)를 참고하세요.

---

## 🚀 주요 특징

- **Modular Architecture**: 서비스별로 독립된 설정(`infra/<번호-카테고리>/<service>`)과 Docker Compose의 `include`를 활용한 유연한 구성.
- **AI-Ready Stack**: **Ollama** (LLM), **Qdrant** (Vector DB), **n8n** (Automation) 사전 통합.
- **Full-Stack Observability**: **Grafana, Prometheus, Loki, Tempo** (LGTM Stack) 사전 구성.
- **Enterprise-Grade Security**: **Keycloak**(SSO), **Vault**, **OAuth2 Proxy** 및 Docker Secrets 기반의 시크릿 관리.

---

## 📂 Repository Guide

| Directory | Purpose | Docs |
| :--- | :--- | :--- |
| [**`infra/`**](infra/) | Docker Compose based infrastructure services | [Stack Details](infra/README.md) |
| [**`projects/`**](projects/) | Application source code & microservices | - |
| [**`docs/`**](docs/) | Architectural blueprints and life-cycle guides | [Index](docs/README.md) |
| [**`secrets/`**](secrets/) | Security-hardened runtime secret files (`*.txt`) | [Secret Guide](secrets/README.md) |
| [**`operations/`**](operations/) | Service operational context & incident history | [Records](operations/README.md) |
| [**`runbooks/`**](runbooks/) | Executable playbooks for maintenance & recovery | [Playbooks](runbooks/README.md) |
| [**`specs/`**](specs/) | Component-level implementation specifications | - |
| [**`scripts/`**](scripts/) | Automation scripts for deployment and ops | - |
| [**`.github/`**](.github/) | CI/CD Workflows (Lint, Validate, Secret Scan) | - |

---

## 🤝 기여 (Contributing)

이 프로젝트는 오픈 소스 기여를 환영합니다.
기여하기 전에 다음 문서들을 꼭 확인해 주세요.

- [**CONTRIBUTING.md**](CONTRIBUTING.md): 기여 가이드라인
- [**CODE_OF_CONDUCT.md**](CODE_OF_CONDUCT.md): 행동 강령
- [**ARCHITECTURE.md**](ARCHITECTURE.md): 구조 이해

## 📝 License

이 프로젝트는 **Apache License 2.0** 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

© 2026 Hy-Home Infrastructure Project.
