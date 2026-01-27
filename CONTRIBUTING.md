# Contributing to Hy-Home Infrastructure

이 저장소에 관심을 가져주셔서 감사합니다! 👋
우리는 명확한 표준과 문서를 통해 누구나 쉽게 이해하고 기여할 수 있는 프로젝트를 만들고자 합니다.

## 📚 먼저 읽어주세요

본격적인 기여 전에 아래 문서들을 검토하면 프로젝트를 이해하는 데 큰 도움이 됩니다.

- [**Code of Conduct**](.github/CODE_OF_CONDUCT.md): 커뮤니티 행동 강령
- [**Development Guide**](docs/03-development-and-contribution.md): 개발 환경 설정 및 프로젝트 구조

## 🚀 기여 프로세스

1. **이슈(Issue) 확인 및 생성**
   - 버그를 발견하거나 새로운 아이디어가 있다면 [Issue](https://github.com/buenhyden/hy-home.docker/issues)를 등록하여 논의해 주세요.
   - 보안 문제의 경우 `.github/SECURITY.md`를 참고하여 비공개로 제보해 주시기 바랍니다.

2. **브랜치 생성 및 작업**
   - `develop` 브랜치(또는 `main`)에서 분기하여 작업 브랜치를 생성하세요.
   - 예: `feat/add-new-service`, `fix/typo-in-docs`

3. **커밋 메시지**
   - [Conventional Commits](https://www.conventionalcommits.org/) 규약을 준수해 주세요.
   - 예: `feat: add redis cluster configuration`, `docs: update readme`

4. **Pull Request (PR)**
   - 작업 내용을 설명하는 PR을 생성하세요.
   - PR 템플릿의 체크리스트를 확인하여 누락된 사항이 없는지 점검하세요.
   - CI 테스트(`validate-docker-compose`)가 통과해야 합니다.

## 📐 아키텍처 및 코딩 표준

모든 변경 사항은 `docs/standards/` 및 `ARCHITECTURE.md`에 정의된 원칙을 따라야 합니다.
중요한 아키텍처 변경의 경우, `docs/adr/`에 [ADR (Architecture Decision Record)](docs/adr/0001-record-architecture-decisions.md)을 작성해야 할 수도 있습니다.

## 💬 질문 및 논의

궁금한 점이 있다면 [Discussions](https://github.com/buenhyden/hy-home.docker/discussions) 탭을 이용해 주세요.
