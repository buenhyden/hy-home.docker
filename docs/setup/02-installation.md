# 🚀 Installation Guide

프로젝트를 로컬 환경에 설치하고 초기 가동하는 과정을 단계별로 안내합니다.

## 1. 저장소 클론

```bash
git clone https://github.com/buenhyden/hy-home.docker.git
cd hy-home.docker
```

## 2. 환경 변수 설정 (`.env`)

`infra/` 디렉토리에 있는 `.env.example` 파일을 기반으로 실제 환경 파일을 생성합니다.

```bash
cd infra
cp .env.example .env
```

### 필수 수정 항목

- `DEFAULT_URL`: 기본 도메인 설정 (기본값: `127.0.0.1.nip.io`)
- `DEFAULT_MOUNT_VOLUME_PATH`: 모든 데이터가 물리적으로 저장될 호스트 경로
- `DOCKER_HOST_IP`: 호스트의 실제 사설 IP 주소

## 3. 비밀 데이터 관리 (`secrets/`)

보안을 위해 비밀번호와 키 파일은 `secrets/` 디렉토리에서 별도 관리됩니다.

```bash
# root 디렉토리에 secrets 폴더 생성 (이미 있다면 확인)
mkdir secrets
cd secrets

# 필요한 비밀번호 파일 생성
echo "my-super-secret-password" > postgres_password.txt
echo "redis-access-key" > redis_password.txt
# ... 기타 필요한 secrets 생성
```

## 4. 인프라 가동

전체 인프라를 가동하거나 특정 스택만 선택적으로 가동할 수 있습니다.

### 방법 A: 전체 가동 (권장 사양 필요)

```bash
cd infra
docker compose up -d
```

### 방법 B: 핵심 구성 요소부터 단계별 가동

```bash
# 1. Gateway (Traefik) 가동
docker compose up -d traefik

# 2. Database 레이어 가동
docker compose up -d mng-pg redis

# 3. Observability 스택 가동
docker compose up -d grafana prometheus
```

## 5. 설치 확인

브라우저를 열어 다음 주소들에 접속이 가능한지 확인합니다.

- **Traefik Dashboard**: `http://traefik.127.0.0.1.nip.io`
- **Keycloak Admin**: `http://auth.127.0.0.1.nip.io`
- **Grafana**: `http://grafana.127.0.0.1.nip.io`

---

## 🛠️ 문제 해결 (FAQ)

### Q: `nip.io` 도메인 접속이 안 됩니다

A: 호스트 시스템에서 DNS 해결이 가능한지 확인하세요 (`ping 127.0.0.1.nip.io`). VPN이 켜져 있거나 사내망인 경우 차단될 수 있습니다. 이 경우 `/etc/hosts` 파일에 수동 등록이 필요합니다.

### Q: 볼륨 마운트 오류가 발생합니다

A: Windows의 경우 Docker Desktop 설정에서 `DEFAULT_MOUNT_VOLUME_PATH`로 지정한 경로에 대한 접근 권한(File Sharing)이 허용되어 있는지 확인하십시오.
