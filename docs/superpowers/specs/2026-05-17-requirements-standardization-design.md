---
status: draft
---

# docs/01.requirements 표준화 설계

**Goal:** `docs/01.requirements` 폴더의 23개 PRD 파일과 README를 `docs/99.templates/prd.template.md` 및 `readme.template.md` 기준에 완전히 준수시킨다.

**Architecture:** README 구조 재정렬 → 전체 PRD frontmatter 일괄 추가 → H1/Target 주석/Related Documents 형식 개별 수정 순서로 적용.

**Scope:** `docs/01.requirements/` 폴더 전체 (README + PRD 23개). 다른 stage 폴더는 이번 범위 밖.

---

## 변경 목록

### 1. README.md

| 변경 항목              | 내용                                                            |
| ---------------------- | --------------------------------------------------------------- |
| frontmatter            | `status: draft` 추가                                            |
| `## Structure`         | 실제 파일명 기준으로 3그룹(기초/추가/최적화-하드닝) 재작성      |
| `## Related Documents` | backtick 형식 → 마크다운 링크 형식                              |
| `## AI Agent Guidance` | Allowed Outputs / Guardrails / Validation 소섹션 추가           |
| 하드닝 공백            | 01-gateway, 10-communication 하드닝 PRD 없음을 구조 섹션에 명시 |

### 2. 모든 PRD 파일 공통 (23개)

- 파일 최상단에 `---\nstatus: draft\n---` frontmatter 추가
- `<!-- Target: docs/01.requirements/파일명.md -->` 주석을 H1 바로 앞에 추가 (없거나 잘못된 위치 수정)

### 3. H1 형식 통일

아래 파일의 H1을 `# {도메인명} Product Requirements` 형식으로 수정:

| 파일                                  | 현재                                              | 변경 후                                                     |
| ------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------- |
| `2026-03-26-03-security.md`           | `# PRD: Security Tier (03-security)`              | `# Security Tier (03-security) Product Requirements`        |
| `2026-03-26-04-data-analytics.md`     | `# PRD: Analytics Tier (04-data/analytics)`       | `# Analytics Tier (04-data/analytics) Product Requirements` |
| `2026-03-26-05-messaging.md`          | `# Product Requirements Document`                 | `# Messaging Tier (05-messaging) Product Requirements`      |
| `2026-03-26-11-laboratory.md`         | `# PRD - 11-laboratory (Management & Laboratory)` | `# Laboratory Tier (11-laboratory) Product Requirements`    |
| `2026-04-01-standardize-infra-net.md` | 이중 H1                                           | `# Standardize infra_net Network Product Requirements`      |
| `2026-03-27-08-ai-open-webui.md`      | H1 뒤에 Target 주석 위치 오류                     | H1 앞으로 이동                                              |

### 4. Related Documents 형식 통일

backtick 링크 `` `[../path]` `` → 마크다운 링크 `[레이블](../상대경로)` 로 교체.

대상: `2026-03-26-01-gateway.md`, `2026-03-26-04-data.md`, `2026-03-26-05-messaging.md`,
`2026-03-26-06-observability.md`, `2026-03-26-11-laboratory.md`, `2026-04-01-standardize-infra-net.md`,
hardening 파일 다수.

### 5. 개별 구조 수정

| 파일                                  | 수정 항목                                     |
| ------------------------------------- | --------------------------------------------- |
| `2026-04-01-standardize-infra-net.md` | 이중 H1 제거, AI Agent Requirements 섹션 추가 |

---

## Non-goals

- 다른 stage 폴더(`02.architecture`, `03.specs` 등) 수정
- PRD 내용(Vision, Requirements 등 비즈니스 로직) 변경
- 신규 PRD 파일 생성 (하드닝 공백은 README에 TODO로 명시)
