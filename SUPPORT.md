# Support & Security Policy

## 지원 안내 (Support)

본 프로젝트는 개인 연구 및 학습용으로 제작되었습니다. 지원이 필요한 경우 아래 방법을 이용해 주십시오.

- **GitHub Issues**: 버그나 기능 제안은 [이슈 템플릿](file:///d:/hy-home.docker/.github/ISSUE_TEMPLATE/)을 사용하여 남겨주세요.
- **Discussions**: 일반적인 질문이나 구성 방법에 대한 논의는 GitHub Discussions (활성화 시)를 이용해 주십시오.

## 보안 취약점 보고 (Security Policy)

이 인프라는 보안 레이어(Keycloak, Vault 등)를 포함하고 있으나, 로컬 환경을 목적으로 합니다.
보안 취약점을 발견하신 경우 퍼블릭 이슈를 생성하기 전에 아래 절차를 따라주십시오.

1. 취약점 요약과 재현 방법을 설명하는 내용을 준비합니다.
2. 가능한 경우 담당자에게 직접 연락하거나(프로필 참조), 비공개 취약점 보고(Private vulnerability reporting) 기능을 사용해 주십시오.

## 업데이트 정책

- **코어 서비스**: 주요 보안 패치나 안정적인 상위 버전이 출시되면 정기적으로 업데이트됩니다.
- **의존성**: `dependabot`을 통해 매주 Actions 및 Docker 이미지 태그의 업데이트가 확인됩니다.
