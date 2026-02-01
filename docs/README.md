# Documentation Index

이 디렉토리는 `hy-home.docker` 프로젝트의 문서 인덱스를 제공합니다. 모든 문서는 저장소 루트 기준의 상대 경로로 참조합니다.

## 구조

| 경로              | 설명                                |
| ----------------- | ----------------------------------- |
| `docs/adr/`       | Architecture Decision Records (ADR) |
| `docs/setup/`     | 초기 설정 및 실행 흐름              |
| `docs/ops/`       | 운영, 모니터링, 장애 대응           |
| `docs/guides/`    | 서비스별 사용 가이드 모음           |
| `docs/standards/` | 규칙/표준 및 문서 기준              |

## 주요 링크

- 인프라 스택: `infra/README.md`
- 저장소 구조: `ARCHITECTURE.md`
- 기여 가이드: `CONTRIBUTING.md`
- 변경 이력: `CHANGELOG.md`
- 지원: `SUPPORT.md`

## 문서 유지 보수 규칙

- 비밀값은 문서에 직접 기입하지 않고 `secrets/` 또는 `.env` 경로를 안내합니다.
- 서비스별 상세 내용은 각 `infra/<번호-카테고리>/<서비스>/README.md`에 정리합니다.
