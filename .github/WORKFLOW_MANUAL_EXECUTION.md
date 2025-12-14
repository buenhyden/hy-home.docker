# GitHub Actions 워크플로우 수동 실행 가이드

## 개요

CI/CD 파이프라인은 이제 자동 실행이 제거되어 다음 방법으로만 실행됩니다:

- **Pull Request**: `main` 브랜치로의 PR 생성 시 자동 실행
- **수동 실행**: GitHub Actions UI에서 workflow_dispatch 트리거 사용

## 수동 실행 방법

### 1. GitHub 웹 UI에서 실행

1. 리포지토리로 이동
2. **Actions** 탭 클릭
3. 왼쪽 사이드바에서 **CI/CD Pipeline** 워크플로우 선택
4. **Run workflow** 버튼 클릭
5. (선택사항) 테스트할 특정 서비스 입력
   - 예: `kafka minio postgresql`
   - 빈 칸으로 두면 변경된 모든 서비스 테스트
6. **Run workflow** 버튼 클릭하여 실행

### 2. GitHub CLI로 실행

```bash
# 기본 실행 (모든 변경된 서비스)
gh workflow run "CI/CD Pipeline"

# 특정 서비스 지정
gh workflow run "CI/CD Pipeline" \
  -f services="kafka minio postgresql"
```

### 3. REST API로 실행

```bash
# 기본 실행
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/ci-cd.yaml/dispatches \
  -d '{"ref":"main"}'

# 특정 서비스 지정
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/actions/workflows/ci-cd.yaml/dispatches \
  -d '{"ref":"main","inputs":{"services":"kafka minio postgresql"}}'
```

## 워크플로우 구조

```text
lint (yamllint + shellcheck)
  ↓
validate (Docker Compose 검증 + 변경 감지)
  ↓
smoke-tests (변경된 서비스별 매트릭스 테스트)
  ↓
collect-failures (실패 집계 및 보고)
  ↓
powershell-tests (PowerShell 스크립트 검증)
```

## 주요 변경사항

### ✅ 제거된 기능

- ❌ `push` 이벤트 자동 실행 (main 브랜치 푸시 시 자동 실행 안 됨)
- ❌ 중복된 checkout 액션
- ❌ 중복된 Docker Compose 설치
- ❌ 중복된 shellcheck 실행
- ❌ 깨진 shell-tests 작업
- ❌ `continue-on-error` 플래그

### ✅ 추가/개선된 기능

- ✅ `workflow_dispatch` 트리거로 수동 실행 가능
- ✅ 특정 서비스 지정 입력 파라미터
- ✅ 명확한 작업 구조 (5개 작업으로 정리)
- ✅ 엄격한 실패 처리 (모든 오류에서 중단)

## PR 워크플로우

Pull Request 생성 시 자동으로 다음이 실행됩니다:

1. **변경 감지**: `Infra/` 디렉토리 내 변경된 서비스 자동 감지
2. **검증**: 변경된 서비스만 스모크 테스트 실행
3. **보고**: PR에 자동 코멘트로 결과 보고
4. **검증**: PR 본문의 서비스 목록과 감지된 서비스 일치 여부 확인

## 로컬 테스트

워크플로우 실행 전 로컬에서 테스트:

```bash
# 특정 서비스 스모크 테스트
./scripts/validate_compose_change.sh kafka --up

# YAML 파일 검증
yamllint .

# Shell 스크립트 검증
find scripts -type f -name "*.sh" -print0 | xargs -0 shellcheck

# Docker Compose 설정 검증
docker compose -f Infra/docker-compose.yml config
```

## 문제 해결

### 워크플로우가 실행되지 않는 경우

1. **Actions 탭 확인**: 워크플로우가 비활성화되지 않았는지 확인
2. **권한 확인**: 리포지토리에 대한 쓰기 권한이 있는지 확인
3. **브랜치 확인**: 올바른 브랜치에서 실행하고 있는지 확인

### 스모크 테스트 실패

1. **아티팩트 다운로드**: Actions 실행 결과에서 실패 로그 다운로드
2. **로컬 재현**: 동일한 서비스로 로컬에서 테스트
3. **로그 확인**: Docker Compose 로그 확인

```bash
docker compose -f Infra/docker-compose.yml logs <service>
```

## 모범 사례

1. **PR 전 로컬 테스트**: PR 생성 전 로컬에서 변경 사항 테스트
2. **작은 변경**: 한 번에 적은 수의 서비스만 변경
3. **명확한 PR 설명**: PR 본문에 변경된 서비스를 `Infra/<service>` 형식으로 명시
4. **수동 실행 활용**: 의심스러운 경우 수동으로 워크플로우 실행
