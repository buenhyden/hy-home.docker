---
title: "Admin and Experiment Tools Hardening Operations Policy"
version: "1.4.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0074"
parent_ids:
- "AD-0011"
created: "2026-05-10"
next_review_at: "2027-05-13"
---

# Admin and Experiment Tools Hardening Operations Policy

## Purpose and Scope

### Objective

이 문서는 여러 tier의 관리·실험 기능 최적화/하드닝 운영 정책을 정의한다. 관리 UI 보안 경계, 실험성 서비스 운영 통제, 카탈로그 확장 승인 게이트를 명문화한다.

#### Authority

- 상위 문서: [Administration and Experimentation Architecture Description](../../../02.architecture/descriptions/0011-laboratory-architecture.md) (`AD-0011`)

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

### Applies To

- 각 패키지의 `docker-compose.yml`: `infra/04-data/redisinsight/`, `infra/06-observability/dozzle/`, `infra/08-ai/open-notebook/`, `infra/08-ai/mlflow/`; JupyterLab LAB은 `labs/jupyterlab/docker-compose.yml`과 `labs/jupyterlab/`(SPEC-0262)
- `.env.example` (`ADMIN_UI_ALLOWED_CIDRS`)
- `scripts/hardening/check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics`

- **Systems**: dozzle, redisinsight, open-notebook, surrealdb, mlflow, JupyterLab LAB
- **Environments**: 단일 HOME/DEV 호스트의 관리 환경(별도 stage·production 환경은 없다)

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0074-R1 | 항상 | 필수: 라우터는 서비스 정책의 gateway/IP allowlist/인증 통제를 적용하고 Dozzle native OIDC와 Open Notebook 공유 SSO 제외 예외를 유지한다 | `check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics` | hardening 검사 결과 |
| POL-0074-R2 | 항상 | 필수: 모든 compose는 root 선언된 network context에 합류하는 service network block을 유지한다 | `HYHOME_COMPOSE_PROFILES=admin,notebook bash scripts/validation/validate-docker-compose.sh` | compose 검증 결과 |
| POL-0074-R3 | 항상 | 금지: dashboard direct host `ports` 노출 | `check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics` | hardening 검사 결과 |
| POL-0074-R4 | 항상 | 필수: dozzle docker socket은 read-only로 유지한다 | `check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics` | hardening 검사 결과 |
| POL-0074-R5 | 항상 | 필수: open-notebook UI route는 allowlist+large-body+앱 비밀번호 경계를 유지하고 credential은 Docker Secret file로만 주입한다 | `check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics` | hardening 검사 결과 |
| POL-0074-R6 | production-like promotion 전 | 필수: Open Notebook API loopback 게시와 SurrealDB 호스트 게시 없음을 현재 경계로 기록하고 direct exposure review를 수행한다 | 수동 | exposure review 기록 |
| POL-0074-R7 | 관리·실험 기능 변경 시 | 필수: `check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics` 및 CI `infrastructure-hardening`을 통과한다 | `check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics` / CI `infrastructure-hardening` | hardening 검사 결과 |
| POL-0074-R8 | 항상 | 필수: optimization-hardening 문서(PRD~Procedure)와 README 인덱스를 동기화한다 | `python3 scripts/validation/check-document-links.py --mode traceability` | traceability 검사 결과 |
| POL-0074-R9 | 항상 | 허용: 카탈로그 확장 항목의 단계적 도입 정책/절차/문서 작업 | 수동 | none |
| POL-0074-R10 | 항상 | 금지: 무승인 allowlist 완화 | 수동 / `check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics` | 승인 기록 |
| POL-0074-R11 | 항상 | 금지: 인증 우회 direct 노출 복원 | `check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics` | hardening 검사 결과 |
| POL-0074-R12 | 항상 | 금지: 감사 기준 없이 운영 캐시 직접 수정 | 수동 | none |
| POL-0074-R13 | 카탈로그 확장 항목 도입 시 | 필수: dashboard/dozzle/redisinsight/open-notebook별 승인 조건을 갖춘다 | 수동 | none |

- **Required**:
  - 라우터는 해당 서비스 정책의 gateway·IP allowlist·인증 통제를 적용한다. Dozzle의 native OIDC와 Open Notebook의 공유 SSO 제외 예외를 유지한다.
  - 모든 compose는 root 선언된 network context에 합류하는 service network block을 유지한다.
  - dashboard direct host `ports` 노출을 금지한다.
  - dozzle docker socket은 read-only로 유지한다.
  - open-notebook UI route는 승인된 allowlist+large-body+앱 비밀번호 경계를 유지하고, credential은 Docker Secret file로만 주입한다.
  - Open Notebook API의 loopback 게시와 SurrealDB의 호스트 게시 없음은 현재 경계로 기록하되, production-like promotion 전 direct exposure review를 수행해야 한다.
  - 관리·실험 기능 변경은 `check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics` 및 CI `infrastructure-hardening` 통과가 필수다.
  - optimization-hardening 문서(PRD~Procedure)와 README 인덱스를 동기화한다.
- **Allowed**:
  - 카탈로그 확장 항목을 단계적으로 도입하는 정책/절차/문서 작업
- **Disallowed**:
  - 무승인 allowlist 완화
  - 인증 우회 direct 노출 복원
  - 감사 기준 없이 운영 캐시 직접 수정

#### Catalog Expansion Approval Gates

- **dashboard 승인 조건**:
  - 실험성 dashboard 접근 만료 정책(자동 종료 기준) 문서화
  - 운영 예외 허용 시간/범위 명시
- **dozzle 승인 조건**:
  - 로그 열람 범위 제한 규칙(프로덕션 로그 차단 포함) 문서화
  - 로그 접근 감시/감사 방식 정의
- **redisinsight 승인 조건**:
  - 최소권한 접근정책 문서화
  - 운영 캐시 직접 수정 금지 + 감사로그 절차 정의
- **open-notebook 승인 조건**:
  - notebook data retention/expiration 기준 문서화
  - API/SurrealDB host-bound port 노출 필요성, 방화벽, 접근 경계 evidence 기록

### Exceptions

#### Exception Conditions

- 장애 대응 시 일시 완화는 승인 기록과 종료 조건이 필수다.
- 예외 종료 후 동일 릴리스 내 기준선 복구 및 재검증을 수행한다.

#### Approval and Review

- 월 1회 정기 검토
- allowlist/권한/노출 정책 변경 시 수시 검토

## Enforcement

### Mechanisms

- `HYHOME_COMPOSE_PROFILES=admin,notebook bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 04-data 06-observability 08-ai 12-analytics`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`

### Limits

정책은 compose 검증, hardening 검사, template baseline, traceability 검사를 지정하지만 아래 항목은 기계적으로 강제되지 않는다.

- Catalog Expansion Approval Gates(만료 정책, 로그 열람 범위, 최소권한, retention 기준)는 문서화 조건이며 점검하는 검사가 지정되어 있지 않다.
- 허용/금지 항목과 allowlist 완화 금지는 수동 검토에 의존한다.
- Open Notebook API/SurrealDB 노출은 현재 경계로 기록되며 production-like promotion 전 direct exposure review가 필요하다.
- 월 1회 정기 검토는 자동 점검이 없다.

## Ownership

### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

### Review Triggers

- 동일 주제 문서: [Guide](../../guides/10-platform-and-backup/0074-laboratory-optimization-hardening.md) (`GDE-0074`), [Runbook](../../runbooks/10-platform-and-backup/0074-laboratory-optimization-hardening.md) (`RUN-0074`)

- [Operations index](../../README.md)
- [Usage guide](../../guides/10-platform-and-backup/0074-laboratory-optimization-hardening.md)
- [Recovery runbook](../../runbooks/10-platform-and-backup/0074-laboratory-optimization-hardening.md)
