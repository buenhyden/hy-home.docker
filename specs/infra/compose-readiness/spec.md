---
title: 'Infra Compose Readiness Implementation Spec'
status: 'Draft'
version: '1.0'
owner: 'Infra'
prd_reference: '../../docs/prd/infra-compose-readiness-prd.md'
api_reference: 'N/A'
arch_reference: '../../ARCHITECTURE.md'
tags: ['spec', 'infra', 'docker-compose', 'readiness']
---

# Implementation Specification (Spec)

> **Status**: Draft
> **Related PRD**: `docs/prd/infra-compose-readiness-prd.md`
> **Related API Spec**: N/A
> **Related Architecture**: `ARCHITECTURE.md`

_Target Directory: `specs/infra-compose-readiness/spec.md`_
_Note: This document is the Source of Truth for implementation changes in compose/scripts for “core stack boot-ready”._

---

## 0. Pre-Implementation Checklist (Governance)

### 0.1 Architecture / Tech Stack

| Item               | Check Question                                        | Required | Alignment Notes | Where to document |
| ------------------ | ----------------------------------------------------- | -------- | --------------- | ----------------- |
| Architecture Style | Is the style defined for this change?                 | Must     | Compose-based infra bootstrap | Section 1 |
| Service Boundaries | Are the boundaries/scope explicit (core stack only)?  | Must     | Root `docker-compose.yml` include list only | Section 1 |
| Backend Stack      | Are tooling/deps clear?                               | Must     | Docker Compose v2 + mkcert | Section 1 |

### 0.2 Quality / Testing / Security

| Item            | Check Question                                 | Required | Alignment Notes | Where to document |
| --------------- | ---------------------------------------------- | -------- | --------------- | ----------------- |
| Test Strategy   | Verification commands + pass criteria defined? | Must     | `yamllint` + `docker compose config` (+ optional preflight) | Section 7 |
| Secret Handling | Secrets/certs are not committed to VCS?        | Must     | Follow `secrets/SENSITIVE_ENV_VARS.md` | Section 9 |

### 0.3 Operations / Deployment / Monitoring

| Item         | Check Question                                           | Required | Alignment Notes | Where to document |
| ------------ | -------------------------------------------------------- | -------- | --------------- | ----------------- |
| Runbook      | Is a deterministic bootstrap runbook provided?            | Must     | `runbooks/core/infra-bootstrap-runbook.md` | Section 9 |
| Drift Check  | Are doc updates required when compose changes occur?      | Must     | Index updates in `OPERATIONS.md` and lifecycle docs | Section 9 |

---

## 1. Technical Overview & Architecture Style

본 작업은 애플리케이션 기능 개발이 아니라, **루트 `docker-compose.yml`에 포함된 Core stack**을 “처음 설치자 기준”으로 **단일 명령 부팅 가능(boot-ready)** 하게 만드는 **prerequisites 표준화 + 최소 compose 정합성 수정 + 검증 스크립트/런북 제공**이다.

- **Component Boundary**:
  - In-scope: root `docker-compose.yml` include된 compose 파일 + 공통 prerequisites + 문서/스크립트
  - Out-of-scope: 주석 처리된 optional stacks / profiles / k8s
- **Key Dependencies**:
  - Docker Engine + Docker Compose v2
  - `mkcert` (local TLS)
- **Tech Stack**:
  - Shell scripts (`bash`) for preflight / cert generation
  - Docs: PRD/Spec/Plan/Runbook (repo templates 준수)

---

## 2. Coded Requirements (Traceability)

| ID             | Requirement Description | Priority | Parent PRD REQ |
| -------------- | ----------------------- | -------- | -------------- |
| **REQ-BOOT-001** | PostgreSQL HA(Spilo/Patroni) 자격 증명은 `.env.postgres` 대신 Docker secrets로 관리한다. 필수 secret 파일: `secrets/db/postgres/patroni_superuser_password.txt`, `secrets/db/postgres/patroni_replication_password.txt`. | High | REQ-PRD-FUN-01 |
| **REQ-BOOT-002** | 로컬 TLS는 `mkcert` 기반으로 `secrets/certs/{rootCA.pem,cert.pem,key.pem}`를 생성/배치한다. | High | REQ-PRD-FUN-02 |
| **REQ-BOOT-003** | Alertmanager 시크릿명은 신규 `alertmanager_*`를 만들지 않고 기존 `smtp_password`/`slack_webhook`로 통일한다. 또한 compose의 `command`/`healthcheck`에서 shell 변수는 `$VAR`가 아닌 `$$VAR`로 표기하여 Compose 변수 보간 경고/오동작을 방지한다. | High | REQ-PRD-FUN-03 |
| **REQ-BOOT-004** | `.env.example`에 core compose가 참조하는 “비-민감 변수”(예: `QDRANT_HOST_PORT`, OpenSearch dashboard/exporter username)를 누락 없이 포함한다. | Medium | REQ-PRD-FUN-04 |
| **REQ-BOOT-005** | bind mount 경로(특히 `${DEFAULT_*_DIR}` 계열)가 존재/권한이 맞는지 runbook에서 preflight 절차로 제공한다. | Medium | REQ-PRD-FUN-01 |
| **REQ-BOOT-006** | `scripts/validate-docker-compose.sh`가 “현재 secrets 디렉토리 구조”를 지원하도록 수정 또는 대체한다. | High | REQ-PRD-FUN-05 |
| **REQ-BOOT-007** | 외부 네트워크(`project_net`, `kind`)는 core 부팅 필수로 강제하지 않고 “필요 시 생성”으로 문서화한다. | Medium | REQ-PRD-FUN-01 |
| **REQ-BOOT-008** | 변경 사항이 반영되도록 문서 인덱스를 업데이트한다. (`OPERATIONS.md`, `docs/context/core/infra-lifecycle-ops.md`) | Low | REQ-PRD-FUN-01 |

---

## 3. Data Modeling & Storage Strategy

본 작업은 데이터 모델 변경이 목적이 아니다. 다만 core stack은 bind mount 기반 볼륨을 다수 사용하므로, **호스트 디렉토리 존재/권한**이 부팅 성공률에 직접 영향을 준다.

- **Storage**: local bind mounts (`${DEFAULT_DATA_DIR}`, `${DEFAULT_OBSERVABILITY_DIR}`, `${DEFAULT_DOCKER_PROJECT_PATH}` 등)
- **Policy**: runbook 및 preflight에서 “필수 경로 목록”과 생성 명령을 제공한다.

---

## 4. Interfaces & Data Structures

### 4.1. Shell Script Interfaces (CLI)

작업에서 추가되는 스크립트는 다음과 같은 안정적인 CLI 계약을 가진다.

- `scripts/generate-local-certs.sh`
  - 입력: `.env`의 `DEFAULT_URL` (없으면 기본값 사용)
  - 출력: `secrets/certs/{rootCA.pem,cert.pem,key.pem}`
  - 실패 조건: `mkcert` 미설치, `mkcert -install` 실패
- `scripts/preflight-compose.sh`
  - 입력: repository root
  - 출력: 누락 prerequisites 목록(파일/디렉토리) + 종료코드(OK=0, Fail=1)

### 4.2. AuthN / AuthZ

N/A (부팅 준비/문서/구성 정합성 작업)

---

## 5. Component Breakdown

- `docs/prd/infra-compose-readiness-prd.md`: 부팅 readiness 요구사항/성공지표.
- `specs/infra-compose-readiness/spec.md`: 요구사항(REQ-BOOT-xxx)과 구현 기준.
- `specs/infra-compose-readiness/plan.md`: 작업 단위(TASK-xxx) + 검증 명령.
- `runbooks/core/infra-bootstrap-runbook.md`: Core stack 기동 절차.
- (Spec 승인 후) `infra/06-observability/docker-compose.yml`: Alertmanager secret 표준화.
- (Spec 승인 후) `.env.example`: 누락된 core 변수 보강.
- (Spec 승인 후) `scripts/validate-docker-compose.sh`: secrets 구조 지원.
- (Spec 승인 후, 선택) `scripts/generate-local-certs.sh`, `scripts/preflight-compose.sh`.

---

## 6. Edge Cases & Error Handling

- **Missing Patroni secret files**:
  - Expected: preflight/runbook에서 `secrets/db/postgres/patroni_superuser_password.txt` 및 `secrets/db/postgres/patroni_replication_password.txt` 준비로 안내.
- **Missing `secrets/certs/cert.pem` / `key.pem`**:
  - Expected: TLS 라우팅 실패/경고 → `generate-local-certs.sh`로 해결.
- **External networks (`project_net`, `kind`) not present**:
  - Expected: core 부팅에는 비필수로 문서화. 필요 시 `docker network create ...` 안내.
- **Host volume permission issues**:
  - Expected: UID 1000 기준 디렉토리 소유권/권한 가이드 제공.

---

## 7. Verification Plan (Testing & QA)

- **[VAL-SPC-001] YAML lint**: 변경된 compose/YAML 파일에 대해 `yamllint`를 실행한다.
- **[VAL-SPC-002] Compose validation**: repo root에서 `docker compose config`가 에러 없이 완료되어야 한다.
- **[VAL-SPC-003] Preflight** (선택): `scripts/preflight-compose.sh`가 누락 항목을 정확히 보고한다.
- **[VAL-SPC-004] Boot smoke** (로컬): `docker compose up -d` 후 최소 health check 기준을 통과한다.

---

## 8. Non-Functional Requirements (NFR) & Scalability

- **Determinism**: “첫 부팅” 시 필요한 파일/명령이 runbook에 빠짐없이 존재해야 한다.
- **Security**: 시크릿/인증서 값이 문서/스크립트/로그에 노출되지 않도록 한다.
- **Minimal Change**: 기능 변화가 아닌 정합성/부팅 가능성 개선에 한정한다.

---

## 9. Operations & Observability

- **Docs/Runbooks**:
  - Bootstrap 절차는 `runbooks/core/infra-bootstrap-runbook.md`를 canonical로 유지한다.
- **Secrets**:
  - 파일 기반 시크릿은 `docker-compose.yml` registry 및 `secrets/README.md`와 정합성을 유지한다.
  - 민감값은 `secrets/` 파일에만 저장하고 `.env.example`에는 넣지 않는다.
- **TLS**:
  - 로컬 TLS는 mkcert 기반 파일명/경로를 고정한다: `secrets/certs/{rootCA.pem,cert.pem,key.pem}`.
