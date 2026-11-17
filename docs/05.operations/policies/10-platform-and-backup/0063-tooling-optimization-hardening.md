---
title: "Platform Operations and Quality Optimization Hardening Operations Policy"
version: "1.5.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0063"
parent_ids:
- "AD-0009"
created: "2026-05-10"
next_review_at: "2027-05-13"
---

# Platform Operations and Quality Optimization Hardening Operations Policy

## Purpose and Scope

### Objective

이 문서는 `09-platform-ops`·`11-quality`의 최적화/하드닝 운영 정책을 정의한다. 관리 경로 보안, 네트워크 경계, 테스트 도구 안정성, 카탈로그 확장 승인 게이트를 통제한다.

#### Authority

- 상위 문서: [Platform Operations·Quality 아키텍처](../../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)

현재 IaC helper는 OpenTofu다. 기존 Terraform workspace는 [Terraform 이관](../../guides/10-platform-and-backup/0082-opentofu.md#terraform-이관)을 따른다. Syncthing runtime은 제거되었으며 현재 하드닝 기동 대상에 포함하지 않는다.

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

### Applies To

- `infra/09-platform-ops/*/docker-compose.yml` 및 `infra/11-quality/*/docker-compose.yml`
- `scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality`

- **Systems**: opentofu, terrakube, registry, SonarQube LAB, k6, Locust LAB, renovate
- **Environments**: 단일 HOME/DEV 호스트(별도 stage·production 환경은 없다)

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0063-R1 | 항상 | 필수: Terrakube 공개 라우터에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다 | none | none |
| POL-0063-R2 | 항상 | 필수: SonarQube LAB(`labs/sonarqube/docker-compose.yml`)은 gateway route 없이 `LAB_HOST_BIND_IP` bind의 loopback port만 게시한다 | none | none |
| POL-0063-R3 | 항상 | 필수: tooling 서비스는 root Compose가 정의한 선언된 network bridge에 연결한다 | 루트 Compose 네트워크 문맥 검증 | none |
| POL-0063-R4 | 항상 | 필수: `labs/locust/docker-compose.yml`의 Locust LAB worker healthcheck를 유지한다 | none | none |
| POL-0063-R5 | 항상 | 필수: k6 volume 계약(`k6-data:/scripts:ro`)을 유지한다 | none | none |
| POL-0063-R6 | tooling 변경 시 | 필수: `bash scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality` 및 CI `infrastructure-hardening`을 통과한다 | `bash scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality` / CI `infrastructure-hardening` | none |
| POL-0063-R7 | 항상 | 필수: optimization-hardening 문서(PRD~Procedure) 링크를 유지한다 | none | none |
| POL-0063-R8 | 항상 | 허용: 카탈로그 확장 항목을 단계적으로 도입하는 설계/운영 작업 | 수동 | none |
| POL-0063-R9 | 항상 | 허용: 성능/품질/보안 기준의 보수적 강화 | 수동 | none |
| POL-0063-R10 | 항상 | 금지: 무승인 SSO/middleware 완화 | 수동 | none |
| POL-0063-R11 | 항상 | 금지: 검증 게이트 우회 배포 | 수동 | none |
| POL-0063-R12 | 항상 | 금지: 감사/보존 정책 없이 확장 항목 운영 전환 | 수동 | none |
| POL-0063-R13 | opentofu 카탈로그 항목 도입 시 | 필수: plan/apply 승인 게이트 문서화, state 잠금/백업 정책 및 drift 자동 탐지 절차 정의 | none | none |
| POL-0063-R14 | terrakube 카탈로그 항목 도입 시 | 필수: workspace 분리 전략 문서화, 실행 권한 모델/RBAC 및 감사로그 연계 정의 | none | none |
| POL-0063-R15 | registry 카탈로그 항목 도입 시 | 필수: cosign 서명/검증 정책 정의, 취약점 스캔 실패 차단 정책 및 예외 절차 정의 | none | none |
| POL-0063-R16 | sonarqube 카탈로그 항목 도입 시 | 필수: 품질게이트 임계값 재정의, 브랜치 정책과 보안 룰셋 분리 운영 | none | none |
| POL-0063-R17 | k6/Locust LAB 카탈로그 항목 도입 시 | 필수: 회귀 baseline 저장/비교 및 시나리오 태그 표준화, 분산 실행 토폴로지와 데이터 초기화/정리 루틴 문서화 | none | none |
| POL-0063-R18 | renovate 카탈로그 항목 도입 시 | 필수: `dependency-update` 작업 범위(`hyhome-renovate.timer` 주간 기본 실행과 온디맨드 실행)와 최소 token 권한을 유지하고 self-host `allowedCommands` 허용 목록과 변경 PR 검증을 확인한다 | 수동 | none |
| POL-0063-R19 | 항상 | 필수: 일반 변경·예외 절차는 공통 운영 정책(`0006-infrastructure-optimization-governance.md`)을 따른다 | none | none |
| POL-0063-R20 | Terrakube cookie ForwardAuth와 CLI/executor 비호환이 남아 있는 동안 | 필수: gateway 통제를 유지하면서 실행 활성화를 차단하고 `@buenhyden`에게 보고한다 | none | none |

- **Required**:
  - Terrakube 공개 라우터는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
  - SonarQube LAB(`labs/sonarqube/docker-compose.yml`, SPEC-0262)은 gateway route를 두지 않고 `LAB_HOST_BIND_IP` bind의 loopback port만 게시한다.
  - tooling 서비스는 root Compose가 정의한 선언된 network bridge에 연결한다.
  - `labs/locust/docker-compose.yml`의 Locust LAB worker healthcheck를 유지한다.
  - k6 volume 계약(`k6-data:/scripts:ro`)을 유지한다.
  - tooling 변경은 `check-all-hardening.sh 09-platform-ops 11-quality` 및 CI `infrastructure-hardening`을 통과해야 한다.
  - optimization-hardening 문서(PRD~Procedure) 링크를 유지해야 한다.
- **Allowed**:
  - 카탈로그 확장 항목을 단계적으로 도입하는 설계/운영 작업
  - 성능/품질/보안 기준의 보수적 강화
- **Disallowed**:
  - 무승인 SSO/middleware 완화
  - 검증 게이트 우회 배포
  - 감사/보존 정책 없이 확장 항목 운영 전환

#### Catalog Expansion Approval Gates

- **opentofu 승인 조건**:
  - plan/apply 승인 게이트 문서화
  - state 잠금/백업 정책 및 drift 자동 탐지 절차 정의
- **terrakube 승인 조건**:
  - workspace 분리 전략 문서화
  - 실행 권한 모델/RBAC 및 감사로그 연계 정의
- **registry 승인 조건**:
  - cosign 서명/검증 정책 정의
  - 취약점 스캔 실패 차단 정책 및 예외 절차 정의
- **sonarqube 승인 조건**:
  - 품질게이트 임계값 재정의
  - 브랜치 정책과 보안 룰셋 분리 운영
- **k6/Locust LAB 승인 조건**:
  - 회귀 baseline 저장/비교 및 시나리오 태그 표준화
  - 분산 실행 토폴로지와 데이터 초기화/정리 루틴 문서화
- **renovate 승인 조건**:
  - `dependency-update` 작업 범위(`hyhome-renovate.timer` 주간 기본 실행과 온디맨드 실행)와 최소 token 권한을 유지한다.
  - self-host `allowedCommands` 허용 목록과 변경 PR 검증을 확인한다.

#### 확장 게이트와 현재 제한

위 카탈로그 항목은 추가 운영 전환의 승인 조건이며 구현 완료 목록이 아니다.
일반 변경·예외 절차는 [공통 운영 정책](../01-common/0006-infrastructure-optimization-governance.md)을
따른다. Terrakube의 cookie ForwardAuth와 CLI/executor 비호환은 별도 구현 검토
대상이다. gateway 통제를 유지하면서 실행 활성화를 차단하고 `@buenhyden`에게 보고한다.

### Exceptions

#### Exception Conditions

- 장애 대응 시 일시 완화는 승인 기록과 종료 조건이 필수다.
- 예외 종료 후 동일 릴리스 내 원상복구 및 재검증을 수행한다.

#### Approval and Review

- 월 1회 정기 검토
- tooling 구성/권한/정책 변경 시 수시 검토

## Enforcement

### Mechanisms

- `bash scripts/hardening/check-all-hardening.sh 09-platform-ops 11-quality`
- `bash scripts/validation/check-template-security-baseline.sh`
- `python3 scripts/validation/check-document-links.py --mode traceability`
- 원격 PR public `changed` 검사 ([quality policy](../../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))
- 프로필로 선택한 서비스는 루트 Compose의 네트워크·secret·의존성 문맥으로 검증한다. 개별 서비스 파일만으로 실행 구성을 판정하지 않는다.

### Limits

아래 규칙은 규칙과 직접 연결된 검사가 정책에 없거나 수동 검토에 의존한다.

- 라우팅·네트워크: 지정된 검사 없음: `POL-0063-R1`, `POL-0063-R2`
- 부하 도구: 지정된 검사 없음: `POL-0063-R4`, `POL-0063-R5`
- 문서 링크: 지정된 검사 없음: `POL-0063-R7`
- 허용/금지: 수동 검토/승인에 의존: `POL-0063-R8`, `POL-0063-R9`, `POL-0063-R10`, `POL-0063-R11`, `POL-0063-R12`
- 확장 승인 조건: 수동 검토/승인에 의존: `POL-0063-R18` / 지정된 검사 없음: `POL-0063-R13`, `POL-0063-R14`, `POL-0063-R15`, `POL-0063-R16`, `POL-0063-R17`
- 변경 절차: 지정된 검사 없음: `POL-0063-R19`, `POL-0063-R20`
- Catalog Expansion Approval Gates는 추가 운영 전환의 승인 조건이며 이를 점검하는 검사가 지정되어 있지 않다.
- 정책은 hardening 검사, template baseline, traceability, PR 검사를 나열하지만 개별 규칙에 연결하지 않는다.
- 개별 서비스 파일만으로는 실행 구성을 판정할 수 없다.
- 월 1회 정기 검토는 자동 점검이 없다.

## Ownership

### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

### Review Triggers

- 동일 주제 문서: [Guide](../../guides/10-platform-and-backup/0063-tooling-optimization-hardening.md) (`GDE-0063`), [Runbook](../../runbooks/10-platform-and-backup/0063-tooling-optimization-hardening.md) (`RUN-0063`)

- [Operations index](../../README.md)
- [Usage guide](../../guides/10-platform-and-backup/0063-tooling-optimization-hardening.md)
- [Recovery runbook](../../runbooks/10-platform-and-backup/0063-tooling-optimization-hardening.md)
