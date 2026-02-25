---
title: 'Infra Compose Readiness Product Requirements Document'
status: 'Draft'
version: 'v1.0.0'
owner: 'Infra'
stakeholders: '[DevOps, Platform, Contributors]'
parent_epic: 'N/A'
tags: ['prd', 'infra', 'docker-compose', 'readiness']
---

# Product Requirements Document (PRD)

> **Status**: Draft
> **Target Version**: v1.0.0
> **Owner**: Infra
> **Stakeholders**: DevOps, Platform, Contributors
> **Parent Epic**: N/A

_Target Directory: `docs/prd/infra-compose-readiness-prd.md`_
_Note: This document defines the What and Why. It must be approved before implementation changes to compose/scripts._

---

## 0. Pre-Review Checklist (Business & Product)

| Item                  | Check Question                                                         | Required | Alignment Notes (Agreement) | PRD Section |
| --------------------- | ---------------------------------------------------------------------- | -------- | --------------------------- | ----------- |
| Vision & Goal         | Is the problem + business goal defined in one paragraph?               | Must     |                             | Section 1   |
| Success Metrics       | Are the key success/failure metrics defined with quantitative targets? | Must     |                             | Section 3   |
| Target Users          | Are specific primary personas and their pain points defined?           | Must     |                             | Section 2   |
| Use Case (GWT)        | Are acceptance criteria written in Given-When-Then format?             | Must     |                             | Section 4   |
| Scope (In)            | Is the feature list included in this release clearly defined?          | Must     |                             | Section 5   |
| Not in Scope          | Is what we will NOT build in this release explicitly listed?           | Must     |                             | Section 6   |
| Timeline & Milestones | Are PoC / MVP / Beta / v1.0 milestones dated?                          | Must     |                             | Section 7   |
| Risks & Compliance    | Are major risks, privacy, or regulatory constraints documented?        | Must     |                             | Section 8   |

---

## 1. Vision & Problem Statement

**Vision**: 루트 `docker-compose.yml`에 포함된 **Core stack**이 신규 환경에서도 “단일 명령”(`docker compose up -d`)으로 안정적으로 기동되도록, 누락된 prerequisites(환경변수/시크릿/로컬 TLS/볼륨 경로/검증 절차)를 표준화하고 문서화한다.

**Problem Statement**: 현재 Core stack은 `docker compose config` / `docker compose up -d` 과정에서 다음과 같은 “첫 부팅 장애 요소”가 발생한다.

- PostgreSQL HA(Spilo/Patroni) 자격 증명(secret 파일) 누락 시 즉시 실패
- Traefik 로컬 TLS 인증서 파일(`secrets/certs/{rootCA.pem,cert.pem,key.pem}`) 부재 시 TLS 라우팅이 실패하거나 경고/오류 유발
- Alertmanager 시크릿 이름이 루트 compose registry와 불일치하여 런타임에서 `/run/secrets/...` 조회 실패 가능
- `.env.example`가 core compose가 참조하는 값을 충분히 포함하지 않아 초기 설정에 혼선
- bind mount 기반 데이터 디렉토리가 사전에 없거나 권한이 맞지 않아 일부 서비스가 부팅/healthcheck에서 실패 가능
- 일부 compose의 `command`/`healthcheck`에 `$VAR`가 그대로 포함되어 Docker Compose의 변수 보간 경고가 발생하고, 런타임에서 의도치 않게 빈 문자열로 대체될 수 있음 (예: Valkey healthcheck, Alertmanager entrypoint)

---

## 2. Target Personas

- **Persona 1 (New Contributor / Developer)**:
  - **Pain Point**: 문서대로 따라 했는데 `docker compose`가 파일/변수/시크릿 문제로 실패하고, 어디가 부족한지 알기 어렵다.
  - **Goal**: 저장소 클론 후 30분 내 core stack을 띄우고, 각 서비스에 접속 가능한 상태가 된다.
- **Persona 2 (DevOps / SRE)**:
  - **Pain Point**: PR마다 compose 변경이 들어오면 “부팅 가능성”이 깨지는 drift가 발생한다.
  - **Goal**: 검증 절차(`docker compose config`, preflight, yamllint)가 명시되어 회귀가 줄어든다.

---

## 3. Success Metrics (Quantitative)

| ID                 | Metric Name                       | Baseline (Current) | Target (Success)                               | Measurement Period |
| ------------------ | --------------------------------- | ------------------ | ---------------------------------------------- | ------------------ |
| **REQ-PRD-MET-01** | First boot success rate (core)    | Unknown            | 100% (문서 절차 준수 시 1회에 부팅 완료)       | 30 days            |
| **REQ-PRD-MET-02** | Time-to-boot (new machine)        | Unknown            | 30분 이내 (prereq + `up -d` + 기본 health 확인) | 30 days            |
| **REQ-PRD-MET-03** | Compose config validity           | Failing            | `docker compose config` 에러 0                 | Every PR           |
| **REQ-PRD-MET-04** | Doc/runbook completeness (core)   | Partial            | Core 부팅 prerequisites가 runbook에 모두 존재  | Every PR           |

---

## 4. Key Use Cases & Acceptance Criteria (GWT)

| ID           | User Story (INVEST)                                                                                                                                 | Acceptance Criteria (Given-When-Then)                                                                                                                                                                                                 |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **STORY-01** | **As a** New Contributor,<br>**I want** prerequisites를 준비하고,<br>**So that** `docker compose up -d`로 core stack을 부팅할 수 있다.             | **Given** I have Docker Engine + Docker Compose v2 installed,<br>**When** I follow the runbook steps (env/secrets/certs/dirs) and run `docker compose up -d`,<br>**Then** core services start and key health checks become healthy. |
| **STORY-02** | **As a** DevOps/SRE,<br>**I want** PR에서 부팅 가능성을 자동/반자동으로 검증하고,<br>**So that** drift를 줄일 수 있다.                               | **Given** repo 변경이 발생했을 때,<br>**When** I run `docker compose config` (and optional preflight scripts),<br>**Then** it exits 0 and reports missing prerequisites deterministically.                                             |
| **STORY-03** | **As a** maintainer,<br>**I want** Alertmanager가 기존 공통 시크릿(smtp/slack)을 재사용하고,<br>**So that** 시크릿 레지스트리 중복을 피한다.       | **Given** root secrets registry defines `smtp_password` and `slack_webhook`,<br>**When** Alertmanager is configured,<br>**Then** it reads only those existing secrets (no new alertmanager_* secrets introduced).                       |

---

## 5. Scope & Functional Requirements

- **[REQ-PRD-FUN-01]** Core stack boot prerequisites(파일/변수/디렉토리/네트워크)를 PRD/Spec/Runbook으로 명확히 정의한다.
- **[REQ-PRD-FUN-02]** 로컬 개발 TLS는 `mkcert` 기반으로 `secrets/certs/{rootCA.pem,cert.pem,key.pem}`를 생성하도록 표준화한다.
- **[REQ-PRD-FUN-03]** Alertmanager는 신규 시크릿을 추가하지 않고, 기존 `smtp_password`/`slack_webhook` 재사용으로 표준화한다.
- **[REQ-PRD-FUN-06]** PostgreSQL HA(Spilo/Patroni) 자격 증명은 `.env.postgres` 대신 Docker secrets로 표준화한다.
- **[REQ-PRD-FUN-04]** `.env.example`는 core compose에서 요구하는 “비-민감 변수”를 누락 없이 포함한다. (민감값은 `secrets/` 기준)
- **[REQ-PRD-FUN-05]** 검증 절차를 제공한다: `yamllint` + `docker compose config` + (선택) preflight.

---

## 6. Out of Scope

- optional profiles / optional stacks 활성화 (주석 처리된 include)
- Kubernetes / Helm / Terraform
- 신규 서비스 추가, 기능 개선, 성능 튜닝
- “실제 시크릿 값”을 생성/배포하거나 저장소에 커밋

---

## 7. Milestones & Roadmap

- **PoC**: 2026-02-26 - PRD/Spec/Plan/Runbook 초안 + core 부팅 blocker 목록 확정
- **MVP**: 2026-03-03 - spec 승인 후 compose/scripts 최소 변경으로 `docker compose config` 무오류 달성
- **v1.0**: 2026-03-10 - 문서 인덱스 정리 + 검증 스크립트 적용 + 회귀 체크 기준 확정

---

## 8. Risks, Security & Compliance

- **Risk: 로컬 TLS(mkcert) 설치/신뢰 설정이 OS별로 상이**:
  - Mitigation: Runbook에 Linux/macOS/WSL2 경로별 절차 제공 + preflight에서 파일 존재 여부만 강제.
- **Risk: Alertmanager 시크릿명 변경으로 런타임 깨짐**:
  - Mitigation: spec에 변경 전/후를 명시하고 `docker compose config`로 구조 검증.
- **Security**:
  - 시크릿/인증서 파일은 커밋 금지. `secrets/` 정책 문서를 준수한다.

---

## 9. Assumptions & Dependencies

- **Assumptions**:
  - 로컬 개발 환경에서 `mkcert` 설치가 가능하다.
  - Core stack은 root `docker-compose.yml`의 include 목록을 기준으로 한다.
- **External Dependencies**:
  - Docker Engine + Docker Compose v2
  - `mkcert` (로컬 TLS)

---

## 10. Q&A / Open Issues

- **[ISSUE-01]** core stack “필수” 범위의 health check 기준(서비스별 endpoint)은 어디까지를 최소로 볼 것인가? - **Update**: Spec에 최소 기준(traefik/keycloak/minio/postgres/opensearch/observability)로 고정한다.

---

## 11. Related Documents (Reference / Traceability)

- **Technical Specification**: `specs/infra-compose-readiness/spec.md`
- **Implementation Plan**: `specs/infra-compose-readiness/plan.md`
- **Operations**: `OPERATIONS.md`
- **Secrets Registry**: `secrets/README.md`
