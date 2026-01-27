# 📋 Prerequisites

이 프로젝트를 안정적으로 가동하고 관리하기 위해 필요한 하드웨어 및 소프트웨어 요구 사양입니다.

## 1. 지원 운영체제

- **Windows**: Docker Desktop (WSL 2 Backend 권장)
- **Linux**: Ubuntu 22.04 LTS 이상 (Docker Engine & Compose V2 설치)
- **macOS**: Docker Desktop (Apple Silicon 권장) - *일부 가속 기능이 제한될 수 있음*

## 2. 하드웨어 요구 사양

전체 인프라를 동시에 가동하려면 상당한 리소스가 필요합니다.

| 서비스 그룹 | 최소 사양 | 권장 사양 | 비고 |
| :--- | :--- | :--- | :--- |
| **코어 인프라** (Traefik, Auth) | 2 vCPU, 4GB RAM | 4 vCPU, 8GB RAM | 필수적 리소스 |
| **데이터베이스 클러스터** (Postgres, Redis) | 4 vCPU, 8GB RAM | 8 vCPU, 16GB RAM | HA 구성 시 필수 |
| **관측성 스택** (Grafana, Loki, etc) | 2 vCPU, 4GB RAM | 4 vCPU, 8GB RAM | 데이터 수집량에 비례 |
| **AI 스택** (Ollama, Qdrant) | 4 vCPU, 16GB RAM | 8 vCPU, 32GB RAM+ | NVIDIA GPU 권장 |
| **전체 동시 가동** | **12 vCPU, 32GB RAM** | **16 vCPU, 64GB RAM** | |

### 💡 리소스 절약 팁

모든 서비스를 동시에 켤 필요는 없습니다. `infra/docker-compose.yml`에서 필요한 서비스만 `include`하여 가동하세요.

## 3. 필수 소프트웨어

1. **Docker & Docker Compose (V2)**: 인프라 오케스트레션의 핵심.
2. **Git**: 저장소 관리 및 서브모듈 동기화.
3. **Command Line Tools**: PowerShell (Windows) 또는 Bash (Linux).
4. **Database Clients (Optional)**: `psql`, `redis-cli`, `kafdrop` 등 디버깅용 도구.

## 4. 네트워크 요구 사항

- **Internal Subnet**: `172.19.0.0/16` 대역을 Docker 내부용으로 사용합니다. 다른 VPN이나 로컬 네트워크와 충돌하지 않는지 확인하십시오.
- **Ports**: 80 (HTTP), 443 (HTTPS) 및 각 DB/대시보드 전용 포트가 호스트에서 점유되지 않아야 합니다.
