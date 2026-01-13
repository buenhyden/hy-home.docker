# .github 폴더 가이드 (GitHub Folder Guide)

이 폴더는 GitHub 저장소의 설정, 템플릿, 워크플로우를 관리합니다.
(This folder manages GitHub repository settings, templates, and workflows.)

## 📂 구조 (Structure)

### 1. 템플릿 (Templates)

- **ISSUE_TEMPLATE/**:
  - `bug-report.yml`: 버그 제보 서식 (Bug report attributes)
  - `feature-spec.yml`: 기능 요청 및 명세 서식 (Feature request & spec attributes)
  - `documentation.yml`: 문서 개선 제안 (Docs improvement)
  - `task.yml`: 일반 작업 및 리팩토링 (General task & refactoring)
  - `config.yml`: 이슈 작성 페이지의 링크 및 안내 설정 (Contact links configuration)
- **pull_request_template.md**: PR 생성 시 기본으로 표시되는 양식 (Default PR template)

### 2. 가이드 및 정책 (Guides & Policies)

- **CONTRIBUTING.md**: 프로젝트 기여 가이드라인. Tech Stack 선택 및 AI 도구 사용 정책 포함. (Contribution guidelines including Tech Stack selection & AI policy.)
- **CODEOWNERS**: 코드 소유권 및 리뷰어 자동 할당 설정. (Code ownership & auto-assignment of reviewers.)
- **SECURITY.md**: 보안 정책 및 취약점 신고 방법. (Security policy & vulnerability reporting.)
- **SUPPORT.md**: 지원 및 문의 채널 안내. (Support channels.)
- **dependabot.yml**: 의존성 자동 업데이트 설정. (Dependency auto-update config.)

### 3. 워크플로우 (Workflows) - `workflows/`

- **ci.yml**: CI 파이프라인 템플릿. (CI pipeline template.)
  - Node.js, Python, Security Scan 등 다양한 작업이 주석 처리되어 있습니다.
  - 프로젝트에 맞는 섹션의 주석을 해제하여 사용하세요. (Uncomment sections relevant to your project.)

## 🛠️ 설정 방법 (How to Configure)

1. **ISSUE_TEMPLATE/config.yml** 수정:
   - `[REPO]`를 실제 저장소 이름으로 변경하세요.

2. **CODEOWNERS** 수정:
   - 팀원 및 메인테이너의 GitHub 핸들을 등록하세요.

3. **workflows/ci.yml** 활성화:
   - 프로젝트 언어/프레임워크에 맞는 Job의 주석을 해제하세요.

4. **dependabot.yml** 확인:
   - 사용하는 패키지 매니저(npm, pip, cargo 등)가 올바르게 설정되었는지 확인하세요.
