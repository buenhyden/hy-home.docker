---
goal: 'Make the root docker-compose core stack boot-ready with one command by standardizing prerequisites, minimal compose fixes, and deterministic runbooks/scripts.'
version: '1.0'
date_created: '2026-02-24'
last_updated: '2026-02-24'
owner: 'Infra'
status: 'Planned'
tags: ['implementation', 'infra', 'docker-compose', 'readiness']
stack: 'python'
---

# Infra Compose Readiness Implementation Plan

_Target Directory: `specs/infra-compose-readiness/plan.md`_

## 1. Context & Introduction

루트 `docker-compose.yml`의 include된 **Core stack**이 신규 환경에서도 `docker compose up -d`로 기동되도록, 누락된 prerequisites(환경변수/시크릿/로컬 TLS/볼륨 경로/검증)를 정리하고, 변경을 PR 단위로 검토 가능하게 문서/스크립트/compose 정합성을 맞춘다.

- PRD: `docs/prd/infra-compose-readiness-prd.md`
- Spec: `specs/infra-compose-readiness/spec.md`

## 2. Goals & In-Scope

- **Goals:**
  - Core stack가 `docker compose config`에서 에러 없이 구성 렌더링된다.
  - Runbook 절차를 따르면 신규 환경에서도 `docker compose up -d`로 기동 가능하다.
  - Alertmanager는 기존 공통 시크릿(`smtp_password`, `slack_webhook`)을 재사용한다.
- **In-Scope (Scope of this Plan):**
  - Root `docker-compose.yml` include된 compose 파일 + 공통 prerequisites + docs/runbooks/scripts + validation script 정합성

## 3. Non-Goals & Out-of-Scope

- **Non-Goals:**
  - optional stacks/profiles 활성화
  - 서비스 기능 개선/튜닝/대규모 리팩터링
- **Out-of-Scope:**
  - Kubernetes / Helm / Terraform
  - 실제 운영 시크릿/인증서 발급 및 커밋

## 4. Requirements & Constraints

- **Requirements:**
  - `[REQ-BOOT-001]` PostgreSQL HA(Spilo/Patroni) 자격 증명은 `.env.postgres` 대신 Docker secrets로 관리 (필수 secret 파일 2개)
  - `[REQ-BOOT-002]` mkcert 기반 `secrets/certs/{rootCA.pem,cert.pem,key.pem}` 표준화
  - `[REQ-BOOT-003]` Alertmanager 시크릿명 표준화(기존 `smtp_password`/`slack_webhook` 재사용)
  - `[REQ-BOOT-004]` `.env.example` 누락 core 변수 보강 (민감값 제외)
  - `[REQ-BOOT-005]` bind mount 경로/권한 preflight 절차 제공
  - `[REQ-BOOT-006]` `scripts/validate-docker-compose.sh`가 현재 secrets 구조 지원
  - `[REQ-BOOT-007]` 외부 네트워크는 “필요 시 생성”으로 문서화
- **Constraints:**
  - Spec 승인 전에는 compose/scripts 등 “실행 가능한 변경”을 적용하지 않는다. (문서/스펙 정리까지만)
  - 시크릿/인증서는 저장소에 커밋하지 않는다.
  - 변경은 최소/정합성 위주로 유지한다.

## 5. Work Breakdown (Tasks & Traceability)

| Task     | Description | Files Affected | Target REQ | Validation Criteria |
| -------- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Patroni 비밀번호 secret 2개를 표준화: `patroni_superuser_password`, `patroni_replication_password` | `docker-compose.yml`, `secrets/README.md`, `runbooks/core/infra-bootstrap-runbook.md` | [REQ-BOOT-001] | Runbook에 생성 절차 포함 |
| TASK-002 | Alertmanager compose에서 시크릿명 변경: `alertmanager_*` → `smtp_password`/`slack_webhook`로 통일. Compose 변수 보간을 피하기 위해 shell 변수는 `$$` 이스케이프 적용 | `infra/06-observability/docker-compose.yml`, `docker-compose.yml` (필요 시) | [REQ-BOOT-003] | `docker compose config` 에러 0 + 보간 경고 감소 |
| TASK-003 | `.env.example` 변수 보강: core compose 참조 변수 전수 점검 후 누락 추가 | `.env.example` | [REQ-BOOT-004] | `docker compose config` 경고/오류 감소 + 문서에 변수 설명 |
| TASK-004 | mkcert 로컬 인증서 생성 스크립트 추가 및 문서화 | `scripts/generate-local-certs.sh`, `runbooks/core/infra-bootstrap-runbook.md` | [REQ-BOOT-002] | 스크립트 2회 실행해도 동일 결과(멱등) |
| TASK-005 | 볼륨 루트 디렉토리 생성/권한 체크를 runbook + (선택) preflight 스크립트로 제공. (부가) compose healthcheck 내부 shell 변수도 필요 시 `$$` 이스케이프 정합성 점검 | `scripts/preflight-compose.sh`, `runbooks/core/infra-bootstrap-runbook.md`, `infra/**/docker-compose*.yml` (필요 시) | [REQ-BOOT-005] | 누락 경로/권한이 명확히 보고됨 |
| TASK-006 | `scripts/validate-docker-compose.sh`를 현재 secrets 구조로 업데이트(더미 파일 생성 경로 정합) | `scripts/validate-docker-compose.sh`, `docker-compose.yml` | [REQ-BOOT-006] | `scripts/validate-docker-compose.sh` exit 0 |
| TASK-007 | 문서 인덱스 업데이트(부팅/선행조건 링크 추가) | `OPERATIONS.md`, `docs/context/core/infra-lifecycle-ops.md` | [REQ-BOOT-008] | 링크가 실제 파일을 가리킴 |

## 6. Verification Plan

| ID          | Level      | Description | Command / How to Run | Pass Criteria |
| ----------- | ---------- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Lint       | YAML lint (touched only) | `yamllint docker-compose.yml infra/**/docker-compose*.yml infra/**/docker-compose*.yaml` | Zero errors |
| VAL-PLN-002 | Validation | Compose render validation | `docker compose config` | Exit 0 |
| VAL-PLN-003 | Script     | Preflight (optional) | `bash scripts/preflight-compose.sh` | Exit 0 when prerequisites met |
| VAL-PLN-004 | Script     | CI-style validation | `bash scripts/validate-docker-compose.sh` | Exit 0 |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| mkcert 설치/신뢰 설정이 OS별로 다름 | Med | Runbook에 OS별 안내 + 스크립트는 “파일 생성”까지만 책임 |
| Alertmanager 시크릿명 변경으로 런타임 깨짐 | High | Spec에 변경 전/후 명시 + `docker compose config`로 검증 |
| bind mount 권한 이슈 | High | UID 1000 기준 가이드 + preflight로 사전 점검 |

## 8. Completion Criteria

- [ ] PRD/Spec/Plan/Runbook 작성 완료
- [ ] (Spec 승인 후) TASK-001 ~ TASK-007 완료
- [ ] `docker compose config` 에러 0
- [ ] 문서 인덱스 업데이트 완료

## 9. References

- **PRD**: `docs/prd/infra-compose-readiness-prd.md`
- **Spec**: `specs/infra-compose-readiness/spec.md`
- **Secrets**: `secrets/README.md`
- **Architecture**: `ARCHITECTURE.md`
