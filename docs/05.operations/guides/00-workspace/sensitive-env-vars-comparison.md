---
status: active
---

<!-- Target: docs/05.operations/guides/00-workspace/sensitive-env-vars-comparison.md -->

# `SENSITIVE_ENV_VARS.md.example` vs `SENSITIVE_ENV_VARS.md` Comparison

> **중요**: 이 문서는 secret 카테고리, ID, 파일 경로 구조만 기록한다. 실제 secret 값은 포함하지 않는다.

## Usage

### Overview

이 문서는 `secrets/SENSITIVE_ENV_VARS.md.example`과 `secrets/SENSITIVE_ENV_VARS.md`의 카테고리 및 항목 수 일관성을 확인하는 운영 참조 문서다. 실제 파일은 mode 600의 operator-owned 파일이므로 값 열람 없이 라인 수와 구조 비교만 수행한다.

이 문서는 `secrets/SENSITIVE_ENV_VARS.md.example`의 카테고리 및 항목 수를 기록한다. 실제 `SENSITIVE_ENV_VARS.md`는 mode 600이므로 값 비교 없이 라인 수와 구조 일치 여부만 확인한다. 신규 서비스 추가 시 example 파일에 먼저 항목을 추가하고 실제 파일도 동기화한다.

### Usage Type

`operational-reference | system-guide`

### Target Audience

- Operators
- Developers
- Contributors
- AI Agents

### Purpose

- `SENSITIVE_ENV_VARS.md.example` vs `SENSITIVE_ENV_VARS.md` Comparison의 운영 사용 맥락을 빠르게 파악한다.
- 반복 실행 절차와 장애 대응은 연결된 runbook으로 넘긴다.
- 통제 기준은 연결된 policy 문서와 분리해 유지한다.

### Prerequisites

- Repository checkout 접근 가능
- 관련 `docs/03.specs/` 또는 operations 문서 확인 가능
- 필요한 경우 Docker/Docker Compose 명령 실행 권한

### Step-by-step Instructions

1. 이 문서의 overview와 usage context를 확인한다.
2. 관련 service, configuration, 또는 documentation target을 식별한다.
3. `## Common Checks`의 검증 항목을 실행하거나 검토한다.
4. 반복 절차, 장애 대응, rollback, escalation이 필요하면 `## Runbook Handoff`의 runbook으로 이동한다.

### Common Pitfalls

- guide에 policy control이나 복구 절차를 직접 섞어 목적 프로파일을 흐리는 경우
- target-relative link를 템플릿 위치 기준으로 계산하는 경우
- 검증 명령 실행 결과 없이 운영 가능 상태를 단정하는 경우

## Common Checks

- `wc -l secrets/SENSITIVE_ENV_VARS.md.example` 결과와 아래 요약 표의 라인 수가 일치하는지 확인한다.
- 카테고리 수(11)와 unique ID 수(107)가 변경되면 요약 표를 업데이트한다.
- 새 서비스 추가 후 `<PREFIX>-<NNN>` ID 규칙을 유지하는지 확인한다.

## 감사 기준일

2026-06-04

## 요약

| 항목                      | 결과                   |
| ------------------------- | ---------------------- |
| Example 파일 라인 수      | 184                    |
| 실제 파일 라인 수         | 184                    |
| 카테고리 수 (example)     | 11                     |
| 총 secret ID 수 (example) | 107 unique IDs         |
| 실제 파일 취급 방식       | metadata-only (mode 600) |
| 라인 수 동일 여부         | ✓ 동일                 |

> **참고**: 실제 `SENSITIVE_ENV_VARS.md`는 민감 정보 보호를 위해 mode 600이며, 값 비교는 수행하지 않는다. 라인 수와 ID count 기준으로 구조 일치를 추정한다.

## 카테고리별 항목 현황 (Example 기준)

| 카테고리 접두사 | 섹션명                           | unique ID 수 | `.env` 연계 변수 포함 | secrets/ 파일 포함 |
| --------------- | -------------------------------- | ------------ | --------------------- | ------------------ |
| `INFRA-`        | 인프라 및 게이트웨이             | 6            | ✓                     | ✓                  |
| `IAM-`          | 인증 및 권한 관리                | 9            | ✓                     | ✓                  |
| `PG-`           | 관계형 데이터베이스 (PostgreSQL) | 19           | ✓                     | ✓                  |
| `SUPA-`         | Supabase (Self-hosted)           | 12           | ✓                     | ✓                  |
| `CACHE-`        | NoSQL & 캐시                     | 21           | ✓                     | ✓                  |
| `STRG-`         | 저장소 (Storage - MinIO)         | 4            | ✓                     | ✓                  |
| `AUTO-`         | 자동화 (Airflow, n8n, Terrakube) | 13           | ✓                     | ✓                  |
| `AI-`           | AI 도구 (Ollama, Qdrant)         | 5            | ✓                     | ✓                  |
| `COMM-`         | 공통 및 통신                     | 8            | ✓                     | ✓                  |
| `OBS-`          | 모니터링 (Observability)         | 8            | ✓                     | ✓                  |
| `SEC-`          | 보안 및 비밀 관리 (Vault)        | 2            | ✓                     | ✓                  |
| **합계**        |                                  | **107**      |                       |                    |

## secrets/ 경로 패턴

example 파일 기준 secret 파일은 다음 경로 패턴을 따른다.

| 패턴                     | 예시                                      |
| ------------------------ | ----------------------------------------- |
| `secrets/auth/`          | `secrets/auth/traefik_admin_password.txt` |
| `secrets/db/postgres/`   | `secrets/db/postgres/mng_password.txt`    |
| `secrets/db/valkey/`     | `secrets/db/valkey/*.txt`                 |
| `secrets/db/mongodb/`    | `secrets/db/mongodb/*.txt`                |
| `secrets/data/`          | `secrets/data/minio_*.txt`                |
| `secrets/common/`        | `secrets/common/smtp_password.txt`        |
| `secrets/security/`      | `secrets/security/vault_*.txt`            |
| `secrets/automation/`    | `secrets/automation/airflow_*.txt`        |
| `secrets/observability/` | `secrets/observability/grafana_*.txt`     |

## 유의 사항

1. **실제 파일은 mode 600**: `secrets/SENSITIVE_ENV_VARS.md`는 operator-owned 파일이므로 값 내용을 출력하지 않는다. 구조 변경 시 라인 수, ID count, 경로 패턴 같은 metadata-only 비교로 확인한다.
2. **새 서비스 추가 시**: `SENSITIVE_ENV_VARS.md.example`에 새 항목을 먼저 추가하고, 실제 파일도 동기화한다.
3. **ID 규칙**: `<PREFIX>-<NNN>` 형식을 유지한다 (예: `CACHE-001`).

## 점검 주기

분기 1회 또는 서비스 추가/제거 시. 점검 후 이 문서의 "감사 기준일"과 요약 표를 업데이트한다.

## Runbook Handoff

N/A — 이 가이드에 대응하는 runbook이 없습니다.

## Related Documents

- [Env Key Comparison](env-key-comparison.md)
- [Spec](../../../03.specs/090-workspace-audit-2026-05/spec.md)
- [secrets/SENSITIVE_ENV_VARS.md.example](../../../../secrets/SENSITIVE_ENV_VARS.md.example)
- [secrets/README.md](../../../../secrets/README.md)
