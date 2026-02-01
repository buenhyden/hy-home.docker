# Development & Contribution Guide

이 문서는 프로젝트 개발 환경 설정과 기여 절차를 안내합니다.

## 1. 개발 환경 설정 (Prerequisites)

이 프로젝트에 기여하기 위해서는 다음 도구들이 필요합니다.

### 필수 도구

- **Git**
- **Docker & Docker Compose**
- **Node.js** (LTS 버전 권장)
- **Python** (3.9+, pre-commit 실행용)

### 설치 절차

1. **저장소 클론**

   ```bash
   git clone https://github.com/buenhyden/hy-home.docker.git
   cd hy-home.docker
   ```

2. **Pre-commit 훅 설치 (중요)**
   모든 코드 변경 사항은 커밋 시 자동으로 검사됩니다.

   ```bash
   pip install pre-commit
   pre-commit install
   ```

   > **Note**: 이제 `git commit` 시 자동으로 Lint/Format 검사가 수행됩니다.

3. **npm 패키지 설치**
   Frontend 프로젝트들의 의존성을 설치합니다.

   ```bash
   cd projects/storybook/react-ts && npm install
   cd ../nextjs && npm install
   cd ../../../
   ```

## 2. 프로젝트 구조

- `.github/`: GitHub Actions 및 이슈 템플릿
- `docs/`: 프로젝트 문서 및 표준 가이드
- `infra/`: Docker Compose 기반 인프라 정의
- `projects/`: 애플리케이션 소스 코드 (React, Next.js 등)
- `scripts/`: 유틸리티 스크립트

## 3. 기여 가이드

### 브랜치 전략

- `main`: 배포 가능한 안정 버전
- `develop`: 개발 통합 브랜치 (기본)
- `feat/*`: 기능 추가
- `fix/*`: 버그 수정
- `docs/*`: 문서 수정

### 커밋 메시지

[Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따릅니다.

- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅 (로직 변경 없음)
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드
- `chore`: 빌드 업무 수정, 패키지 매니저 설정 등

### Pull Request

1. PR 생성 시 템플릿의 체크리스트를 확인하세요.
2. 모든 CI 테스트(`validate-docker-compose` 등)를 통과해야 합니다.
3. 리뷰어의 승인을 받은 후 Merge 합니다.
