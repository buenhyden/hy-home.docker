# 🏠 Hy-Home Docker Infrastructure

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

**Hy-Home Docker**는 확장 가능하고 안정적인 홈 서버 및 AI 최적화 개발 환경을 위한 **Docker 기반 인프라 프로젝트**입니다.
복잡한 마이크로서비스 아키텍처를 로컬 환경에서 손쉽게 구축하고 관리할 수 있도록 설계되었습니다.

> 📖 **자세한 문서는 [docs/README.md](docs/README.md)에서 확인하실 수 있습니다.**

---

## 🚀 주요 특징

- **Modular Architecture**: 서비스별로 독립된 설정(`infra/<service>`)과 Docker Compose의 `include`를 활용한 유연한 구성.
- **AI-Ready Stack**: **Ollama** (LLM), **Qdrant** (Vector DB), **n8n** (Automation) 사전 통합.
- **Enterprise Observability**: **Grafana, Prometheus, Loki, Tempo**를 통한 풀 스택 모니터링.
- **Security First**: **Keycloak**(SSO), **Vault**, **OAuth2 Proxy**를 통한 철저한 보안/인증 레이어.

---

## 📂 저장소 안내

| 디렉토리 | 설명 | 상세 문서 |
| --- | --- | --- |
| [**`infra/`**](infra/) | Docker Compose 기반 인프라 서비스 | [Stack Details](docs/02-infrastructure-stack.md) |
| [**`projects/`**](projects/) | 인프라 위에서 구동될 애플리케이션 | - |
| [**`docs/`**](docs/) | 프로젝트 전체 상세 문서 및 가이드 | [Documentation Index](docs/README.md) |
| [**`scripts/`**](scripts/) | 배포 및 관리 자동화 스크립트 | [Dev Guide](docs/03-development-and-contribution.md) |

---

## 🏁 빠른 시작 (Quick Start)

자세한 설치 가이드는 [Development Guide](docs/03-development-and-contribution.md)를 참조하세요.

### 1. 설정

```bash
cd infra
cp .env.example .env
# .env 파일 내의 DOMAIN 및 DATA_PATH 설정 필수
```

### 2. 실행

```bash
docker compose up -d
```

### 3. 접속

- **Traefik Dashboard**: `http://traefik.localhost` (또는 설정한 도메인)
- **Grafana**: `http://grafana.localhost`

---

## 🤝 기여 (Contributing)

이 프로젝트는 오픈 소스 기여를 환영합니다.
기여하기 전에 다음 문서들을 꼭 확인해 주세요.

- [**CONTRIBUTING.md**](CONTRIBUTING.md): 기여 가이드라인
- [**Code of Conduct**](.github/CODE_OF_CONDUCT.md): 행동 강령
- [**Architecture Guide**](docs/01-repository-structure.md): 구조 이해

## 📝 License

이 프로젝트는 **Apache License 2.0** 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---
© 2026 Hy-Home Infrastructure Project.
