# Docker Infrastructure & Projects

## 개요

로컬 개발 및 테스트를 위한 **Docker Compose 기반의 완전한 인프라 환경**입니다.  
레이어드 아키텍처로 구성된 26개의 통합 서비스를 제공합니다.

## 📂 주요 구조

```
infra/          # 인프라 서비스 (Traefik, Keycloak, PostgreSQL, Kafka, etc.)
Projects/       # 환경 설정 스크립트
docs/           # 상세 문서 (아키텍처, 가이드, 참고 자료)
secrets/        # Docker Secrets (git-ignored)
```

## 🎯 시스템 아키텍처

레이어드 아키텍처Based on **8개 계층**으로 구성:

- **Ingress**: Traefik + OAuth2 Proxy
- **인증**: Keycloak (SSO/IAM)
- **애플리케이션**: n8n, Ollama
- **관측성**: Prometheus, Grafana, Loki, Tempo
- **데이터**: PostgreSQL HA, Valkey Cluster (Redis Compatible), InfluxDB
- **메시징**: Kafka (KRaft)
- **스토리지**: MinIO (S3)
- **관리 DB**: 인프라 메타데이터

> 📊 **상세 다이어그램 및 서비스 의존성**: [시스템 아키텍처 문서](./docs/architecture/system-architecture.md)

> 🌐 **네트워크 구성 (infra_net: 172.19.0.0/16)**: [네트워크 토폴로지](./docs/architecture/network-topology.md)

## � 빠른 시작

### 1. 사전 준비

```bash
# Secrets 생성
mkdir -p secrets
echo "your_password" > secrets/postgres_password.txt
echo "your_password" > secrets/redis_password.txt
# ... (나머지 secrets)
```

### 2. 전체 실행

```bash
cd infra
docker-compose up -d
```

### 3. 검증

```bash
docker-compose ps  # 모든 서비스 Up (healthy) 확인
```

> 📘 **상세 설치 가이드, 배포 시나리오**: [배포 가이드](./docs/guides/deployment-guide.md)

## 📦 서비스 카탈로그

**활성화된 26개 서비스**:

- **리버스 프록시 & 인증**: Traefik, OAuth2 Proxy, Keycloak
- **데이터베이스**: PostgreSQL HA, Valkey Cluster, InfluxDB
- **메시징**: Kafka, ksqlDB
- **스토리지**: MinIO
- **관측성**: Prometheus, Grafana, Loki, Tempo, Alloy
- **애플리케이션**: n8n, Ollama, SonarQube
- **기타**: Storybook (Optional)

> 🔗 **전체 서비스 목록, 접속 URL, 포트, 연결 정보**: [서비스 카탈로그](./docs/reference/service-catalog.md)

## 📚 문서

| 카테고리 | 내용 | 링크 |
|:---|:---|:---|
| **아키텍처** | 시스템 설계, 네트워크, 의존성 | [docs/architecture/](./docs/architecture/) |
| **가이드** | 배포, 트러블슈팅, 보안, 유지보수 | [docs/guides/](./docs/guides/) |
| **참고** | 서비스 카탈로그, 환경 변수 | [docs/reference/](./docs/reference/) |
| **Infra 상세** | 각 서비스별 README | [infra/](./infra/) |

### 주요 문서

- 🏗️ **[시스템 아키텍처](./docs/architecture/system-architecture.md)**: 전체 구조, 계층별 설명, 서비스 흐름
- 🌐 **[네트워크 토폴로지](./docs/architecture/network-topology.md)**: IP 할당, DNS, Traefik 라우팅
- 🚀 **[배포 가이드](./docs/guides/deployment-guide.md)**: 설치, 시나리오별 배포
- 🐛 **[트러블슈팅](./docs/guides/troubleshooting.md)**: 포트 충돌, DNS, OOM 등 문제 해결
- 🔒 **[보안 가이드](./docs/guides/security.md)**: Secrets, mkcert, OAuth2 설정
- 🔧 **[유지보수 가이드](./docs/guides/maintenance.md)**: 업데이트, 백업, 모니터링
- 📖 **[서비스 카탈로그](./docs/reference/service-catalog.md)**: 모든 서비스 접속 정보

## 🔧 시스템 요구사항

**최소**: CPU 8코어, RAM 16GB, Disk 100GB SSD  
**권장**: CPU 16코어, RAM 32GB, Disk 500GB NVMe, GPU (Ollama 사용 시)

## ⚠️ 주의사항

1. **비밀번호**: `secrets/` 디렉토리는 `.gitignore`에 포함 (절대 커밋 금지)
2. **포트 충돌**: 기본 포트(5432, 6379, 9092) 사용 중인지 확인
3. **리소스**: 전체 실행 시 많은 리소스 필요 - 필요한 서비스만 선택 실행 권장

> 🛠 문제 발생 시: [트러블슈팅 가이드](./docs/guides/troubleshooting.md)

## 📄 라이선스

이 프로젝트는 개인 사용을 위한 것입니다.
