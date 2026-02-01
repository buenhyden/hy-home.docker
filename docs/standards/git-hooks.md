# Git Hooks & Linting Standards

이 프로젝트는 [pre-commit](https://pre-commit.com/) 프레임워크를 사용하여 코드 품질을 자동으로 관리합니다.

## 개요

커밋 시 자동으로 실행되는 훅을 통해 다음을 보장합니다:

- **Linting**: ESLint (JS/TS), Markdownlint (문서), ShellCheck (Shell Script)
- **Docker**: Hadolint (Dockerfile), Docker Compose Check (YAML validation)
- **Formatting**: Prettier (Code Style)
- **Sanity Checks**: Trailing whitespace, End of file fixer, YAML/JSON 유효성 검사

## 설정 방법 (최초 1회)

프로젝트 루트에서 다음 명령어를 실행하여 훅을 설치해야 합니다.

```bash
# pre-commit 설치 (Python 필요)
pip install pre-commit

# 훅 활성화
pre-commit install
```

## 동작 방식

1. `git commit` 실행 시 설정된 훅들이 자동으로 실행됩니다.
2. 위반 사항이 발견되면 커밋이 중단됩니다.
3. 일부 규칙(Prettier, End of file 등)은 파일을 **자동으로 수정**합니다. 수정된 내용을 다시 `add` 하고 커밋하면 됩니다.

## 훅 구성

`.pre-commit-config.yaml` 파일에 정의되어 있으며, 주요 내용은 다음과 같습니다:

- **pre-commit-hooks**: 기본 파일 검사 (공백 제거, 대용량 파일 체크 등)
- **Prettier**: 코드 포맷팅 (JS, TS, JSON, YAML, MD)
- **Markdownlint**: 마크다운 문법 검사 (`.markdownlint.json` 기준)
- **ESLint**: 프로젝트별(`projects/storybook/*`) 린트 규칙 적용
- **ShellCheck**: 쉘 스크립트 정적 분석
- **Hadolint**: Dockerfile 베스트 프랙티스 검사
- **Docker Compose Check**: `docker-compose.yml` 유효성 검증

## 수동 실행

커밋 없이 모든 파일에 대해 검사를 실행하려면 다음 명령어를 사용하세요:

```bash
pre-commit run --all-files
```

## 우회 방법

비상 시(권장하지 않음) 훅을 건너뛰려면:

```bash
git commit --no-verify
```
