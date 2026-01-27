# 💻 Development & Contribution Guide

Hy-Home Docker 프로젝트에 기여하거나, 이를 기반으로 개발을 진행하기 위한 가이드입니다.

## 🚀 개발 환경 설정 (Getting Started)

### 1. 전제 조건 (Prerequisites)

- **OS**: Windows 10/11 (WSL2 권장) 또는 Linux (Ubuntu 등)
- **Runtime**: Docker Engine & Docker Compose V2
- **Tools**: Git, VS Code (권장)

### 2. 초기 설정 (Initial Setup)

```bash
# 1. 저장소 클론
git clone https://github.com/your-repo/hy-home.docker.git
cd hy-home.docker

# 2. 환경 변수 설정
cd infra
cp .env.example .env

# 3. .env 파일 수정
# - DATA_PATH: 실제 데이터가 저장될 로컬 호스트 경로 지정
# - DOMAIN: 서비스에 할당할 도메인 설정
```

### 3. 서비스 실행

```bash
# 전체 서비스 실행 (리소스 주의)
docker compose up -d

# 특정 서비스만 실행 (예: postgresql)
docker compose up -d postgresql
```

## 🛠 프로젝트 활용 가이드

### 새 인프라 서비스 추가하기

1. `infra/` 폴더 내에 새로운 서비스 이름으로 디렉토리를 생성합니다.
2. 해당 디렉토리 안에 서비스별 `docker-compose.yml` (또는 메인의 `include` 구조에 맞게)과 설정 파일을 작성합니다.
3. 필요한 경우 `infra/.env.example`에 환경 변수를 추가하고 문서화합니다.
4. `infra/README.md` 목록에 서비스를 추가합니다.

### 새 애플리케이션 프로젝트 시작하기

1. `projects/` 폴더로 이동하여 새 프로젝트 폴더를 만듭니다.
2. 인프라 서비스(DB, API 등)와 연동하는 코드를 작성합니다.
3. 프로젝트별 의존성(requirements.txt, package.json 등)은 해당 프로젝트 폴더 내에서 관리합니다.

## 🤝 기여 가이드 (Contributing)

### 브랜치 전략

- `main` (또는 `master`): 배포 가능한 안정 버전
- `develop`: 개발 중인 버전 (Feature 브랜치 병합 대상)
- `feature/*`: 새로운 기능 개발
- `fix/*`: 버그 수정

### 커밋 메시지 컨벤션

[Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따르는 것을 권장합니다.

- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅, 세미콜론 누락 등 (코드 변경 없음)
- `refactor`: 코드 리팩토링 (기능 변경 없음)
- `chore`: 빌드 업무, 패키지 매니저 설정 등

### Pull Request (PR) 프로세스

1. Issue를 생성하여 작업 내용을 논의합니다.
2. Feature 브랜치를 생성하고 작업을 진행합니다.
3. 작업 완료 후 PR을 생성합니다.
4. `.github/PULL_REQUEST_TEMPLATE.md` 양식에 맞춰 작성합니다.
5. 리뷰어의 승인을 받은 후 Merge 합니다.

## 📜 스크립트 활용 (`scripts/`)

향후 자동화를 위해 `scripts/` 디렉토리에 유용한 쉘 스크립트가 추가될 예정입니다.

- **backup.sh**: 주요 데이터 볼륨 백업
- **restore.sh**: 백업 데이터 복구
- **init.sh**: 초기 개발 환경 세팅 자동화

---

더 자세한 내용은 [CONTRIBUTING.md](file:///d:/hy-home.docker/CONTRIBUTING.md)를 참조하십시오.
