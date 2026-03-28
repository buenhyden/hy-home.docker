# 07-Workflow Optimization & Hardening Product Requirements

## Overview (KR)

이 문서는 `infra/07-workflow` 계층(Airflow, n8n)의 최적화/하드닝 요구사항을 정의한다. 목표는 관리 경로 보안 강화, health 기반 안정성 확보, 컨테이너 런타임 하드닝, 그리고 카탈로그 기반 확장 항목의 실행 로드맵 수립이다.

## Vision

워크플로 계층을 "기본적으로 안전하고, 장애 전파에 강하며, 운영 확장 기준이 명확한" 오케스트레이션 플랫폼으로 표준화한다.

## Problem Statement

- Airflow/n8n 관리 UI 라우터의 middleware 정책이 불균일하여 경계 보안이 약해질 수 있다.
- 일부 서비스는 health 기반 dependency/healthcheck 계약이 부족해 기동 race condition 위험이 있다.
- n8n 이미지/entrypoint 하드닝 계약이 compose 구성과 일치하지 않아 drift 가능성이 있다.
- 카탈로그의 workflow 확장 항목(Airflow 품질 게이트, n8n backup/Vault, airbyte artifact 보강)이 실행 문서로 충분히 연결되지 않았다.

## Personas

- **Platform SRE**: workflow 서비스 가용성과 보안을 동시에 운영해야 한다.
- **DevOps Engineer**: compose/CI/이미지 하드닝 기준선을 유지해야 한다.
- **Workflow Maintainer**: DAG/automation의 변경을 안전하게 배포해야 한다.

## Key Use Cases

- **STORY-WRK-01**: 운영자는 Airflow/n8n 경로가 gateway+SSO 정책을 충족하는지 확인한다.
- **STORY-WRK-02**: 엔지니어는 health 기반 기동 계약을 통해 worker startup 실패를 줄인다.
- **STORY-WRK-03**: CI는 workflow 하드닝 회귀를 PR 단계에서 자동 차단한다.
- **STORY-WRK-04**: 팀은 Airflow DAG 품질 게이트/오토스케일 기준, n8n Git backup/Vault 연계 기준, airbyte artifact 보강 계획을 추적한다.

## Functional Requirements

- **REQ-PRD-WRK-FUN-01**: Airflow/n8n 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용해야 한다.
- **REQ-PRD-WRK-FUN-02**: Airflow 핵심 서비스는 broker(`airflow-valkey`) health 기반 의존성을 사용해야 한다.
- **REQ-PRD-WRK-FUN-03**: n8n worker/task-runner는 healthcheck를 제공하고 task-runner는 n8n/valkey health 의존성을 사용해야 한다.
- **REQ-PRD-WRK-FUN-04**: n8n 서비스는 multi-stage/custom image 기반 비루트 실행 및 secret guard를 제공해야 한다.
- **REQ-PRD-WRK-FUN-05**: `scripts/check-workflow-hardening.sh`와 CI `workflow-hardening` job을 제공해야 한다.
- **REQ-PRD-WRK-FUN-06**: `docs/01~09` optimization-hardening 문서 세트와 README 인덱스를 동기화해야 한다.
- **REQ-PRD-WRK-FUN-07**: 카탈로그 기준으로 Airflow DAG 품질 게이트/워커 오토스케일 기준, n8n Git backup/Vault 연계, airbyte artifact 보강 태스크를 정의해야 한다.

## Success Criteria

- **REQ-PRD-WRK-MET-01**: `bash scripts/check-workflow-hardening.sh` 실패 0건.
- **REQ-PRD-WRK-MET-02**: Airflow/n8n compose static validation 통과.
- **REQ-PRD-WRK-MET-03**: workflow optimization-hardening 문서 간 양방향 링크 정합성 확보.
- **REQ-PRD-WRK-MET-04**: workflow 카탈로그 확장 항목이 Plan/Tasks에 반영.

## Scope and Non-goals

- **In Scope**:
  - `infra/07-workflow/airflow/docker-compose.yml`
  - `infra/07-workflow/n8n/{docker-compose.yml,Dockerfile,docker-entrypoint.sh}`
  - `scripts/check-workflow-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09` workflow optimization-hardening 문서 및 README 인덱스
- **Out of Scope**:
  - 개별 DAG/워크플로 비즈니스 로직 구현
  - Airbyte 프로덕션 컨테이너/compose 신규 도입
- **Non-goals**:
  - 즉시 멀티클러스터 workflow 아키텍처 전환
  - 외부 SaaS orchestration 서비스 이전

## Risks, Dependencies, and Assumptions

- SSO 체인 강화는 기존 자동화 접근 경로에 영향을 줄 수 있어 운영 승인 절차가 필요하다.
- Airflow/n8n은 `04-data` PostgreSQL, `01-gateway` Traefik, `02-auth` SSO middleware 구성에 의존한다.
- Airbyte는 현재 infra artifact 부재 상태이며 본 사이클에서는 backlog 정의가 중심이다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: workflow compose/image/script/docs/ci 변경과 정적 검증 실행
- **Disallowed Actions**: 무승인 인증 완화, 부동 태그 도입, 무검증 포트 노출 확대
- **Human-in-the-loop Requirement**: 접근제어 완화, HA topology 확장 시 승인 필수
- **Evaluation Expectation**: workflow hardening + template baseline + doc traceability 통과

## Related Documents

- **ARD**: [../02.ard/0022-workflow-optimization-hardening-architecture.md](../02.ard/0022-workflow-optimization-hardening-architecture.md)
- **Spec**: [../04.specs/07-workflow/spec.md](../04.specs/07-workflow/spec.md)
- **Plan**: [../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md](../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md)
- **ADR**: [../03.adr/0022-workflow-hardening-and-ha-expansion-strategy.md](../03.adr/0022-workflow-hardening-and-ha-expansion-strategy.md)
- **Tasks**: [../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md](../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/07-workflow/optimization-hardening.md](../07.guides/07-workflow/optimization-hardening.md)
- **Operation**: [../08.operations/07-workflow/optimization-hardening.md](../08.operations/07-workflow/optimization-hardening.md)
- **Runbook**: [../09.runbooks/07-workflow/optimization-hardening.md](../09.runbooks/07-workflow/optimization-hardening.md)
