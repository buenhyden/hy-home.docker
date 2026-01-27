# 🐙 Git & Development Workflow

이 문서는 프로젝트의 일관된 코드 관리와 협업을 위한 Git 표준 및 개발 절차를 정의합니다.

## 1. Commit Message Standard (Conventional Commits)

모든 커밋 메시지는 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 형식을 따라야 합니다.

### 형식: `<type>(<scope>): <subject>`

- **feat**: 새로운 기능 추가
- **fix**: 버그 수정
- **docs**: 문서 업데이트
- **style**: 코드 포맷팅 (코드 변경 없음)
- **refactor**: 코드 리팩토링
- **perf**: 성능 개선
- **test**: 테스트 코드 추가/수정
- **infra**: Docker, CI/CD 등 인프라 설정 변경
- **chore**: 빌드 업무, 패키지 매니저 설정 등

### 예시

- `feat(db): add valkey cluster support`
- `fix(traefik): correct port mapping for dashboard`
- `docs(setup): update installation steps for windows`

## 2. Branch Strategy

프로젝트는 간단하면서도 명확한 브랜치 전략을 사용합니다.

- **main**: 프로덕션 수준의 안정적인 상태를 유지하는 메인 브랜치.
- **feature/**: 새로운 기능 개발 또는 서비스 추가 (`feature/add-airflow`).
- **fix/**: 버그 수정용 브랜치 (`fix/postgres-auth-issue`).
- **infra/**: 인프라 오케스트레션 변경 (`infra/update-lgtm-stack`).
- **docs/**: 문서 개선 및 업데이트 (`docs/expand-ops-guide`).

## 3. Development Lifecycle

1. **Issue Creation**: 작업할 내용을 GitHub 이슈로 등록합니다.
2. **Branch Creation**: 이슈 번호와 관련된 브랜치를 생성합니다.
3. **Local Dev & Test**: `infra/`에서 서비스를 가동하고 `scripts/`를 통해 검증합니다.
4. **Pull Request**: 메인 브랜치로 병합을 요청합니다 (PR 템플릿 준수).
5. **Review & Merge**: AI 에이전트 또는 동료의 리뷰를 거쳐 병합합니다.

## 4. Engineering Pillars

- **Standards First**: 코드를 작성하기 전에 `.agent/rules/`의 관련 표준을 확인하십시오.
- **Traceability**: 모든 변경은 로그(`CHANGELOG.md`)나 문서(`ADR`)를 통해 추적 가능해야 합니다.
- **Zero Circularity**: 인프라 서비스 간의 순환 의존성을 지양합니다.
