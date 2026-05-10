# Tooling Tier Operations (09-tooling)

> `09-tooling` 계층 운영 정책과 통제 기준 문서 모음.

## Overview

이 디렉터리는 Tooling 계층의 운영 거버넌스를 관리한다. 도구별 정책(terraform, terrakube, registry, sonarqube, k6, locust, syncthing)과 최적화/하드닝 기준을 정의하며, 실행 절차는 runbook으로 분리한다.

## Documents

- [Performance Testing Operations Policy](./performance-testing.md)
- [Locust Operations Policy](./locust.md)
- [k6 Operations Policy](./k6.md)
- [Registry Operations Policy](./registry.md)
- [SonarQube Operations Policy](./sonarqube.md)
- [Syncthing Operations Policy](./syncthing.md)
- [Terraform Operations Policy](./terraform.md)
- [Terrakube Operations Policy](./terrakube.md)
- [Optimization Hardening Operations Policy](./optimization-hardening.md)

## Operational Standards

- 공개 tooling 라우터는 gateway 표준 체인 + SSO 체인을 강제한다.
- compose 네트워크 경계(`infra_net` external)를 유지한다.
- tooling 하드닝 회귀는 script/CI 게이트로 차단한다.
- 카탈로그 확장 항목은 승인 게이트와 함께 단계적으로 도입한다.

## Related References

- [Tooling Usage Index](../../07.operations/09-tooling/README.md)
- [Tooling Procedure Index](../../07.operations/09-tooling/README.md)
- [Tooling PRD](../../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- [Tooling Plan](../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- [Tooling Tasks](../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- [Optimization Catalog](../12-infra-service-optimization-catalog.md)

---

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 운영 정책과 controls
- 허용/금지/예외 기준
- 검증 방법과 review cadence

### Out of Scope

- 단계별 복구 절차
- 튜토리얼 문서
- incident timeline

## Structure

```text
docs/07.operations/09-tooling/
├── iac-deployment-policy.md  # 문서
├── k6.md  # 문서
├── locust.md  # 문서
├── optimization-hardening.md  # 문서
├── performance-testing.md  # 문서
├── README.md  # This file
├── registry.md  # 문서
├── sonarqube.md  # 문서
├── syncthing.md  # 문서
├── terraform.md  # 문서
└── terrakube.md  # 문서
```

## How to Work in This Area

1. 같은 서비스의 guide와 runbook을 확인해 정책과 실행 절차가 분리되어 있는지 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Usage

> Migrated from `docs/07.operations/09-tooling/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Tooling Tier Usages (09-tooling)

> `09-tooling` 계층의 사용/설정/운영 준비를 위한 가이드 문서 모음.

#### Overview

이 디렉터리는 Tooling 계층(terraform, terrakube, registry, sonarqube, k6, locust, syncthing)의 사용 방법과 하드닝 적용 절차를 제공한다. 운영 정책은 `07.operations`, 장애 대응은 `07.operations`에서 관리한다.

#### Documents

- [01. IaC Automation Usage](./01.iac-automation.md)
- [02. Performance Testing Usage](./performance-testing.md)
- [03. Locust Usage](./locust.md)
- [04. k6 Usage](./k6.md)
- [05. Registry Usage](./registry.md)
- [06. SonarQube Usage](./sonarqube.md)
- [07. Syncthing Usage](./syncthing.md)
- [08. Terraform Usage](./terraform.md)
- [09. Terrakube Usage](./terrakube.md)
- [10. Optimization Hardening Usage](./optimization-hardening.md)

#### How to Work in This Area

1. 새 가이드는 `docs/99.templates/operation.template.md`를 사용한다.
2. 실행 절차 변경 시 대응 Operation/Procedure 링크를 함께 갱신한다.
3. 최적화/하드닝 변경은 `optimization-hardening.md`와 Plan/Tasks를 동시 갱신한다.

#### Related References

- [Tooling Infra](../../../infra/09-tooling/README.md)
- [Tooling PRD](../../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- [Tooling Spec](../../04.specs/09-tooling/spec.md)
- [Tooling Plan](../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- [Tooling Tasks](../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- [Tooling Operations](../../07.operations/09-tooling/README.md)
- [Tooling Procedures](../../07.operations/09-tooling/README.md)

---

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

#### Scope

##### In Scope

- how-to, onboarding, troubleshooting guide
- 관련 infra/operation/runbook 링크
- 작업 전제조건과 흔한 실수

##### Out of Scope

- 운영 통제 정책 원문
- 실시간 장애 대응 절차
- secret 값 또는 credential 원문

#### Structure

```text
docs/07.operations/09-tooling/
├── 01.iac-automation.md  # 문서
├── k6.md  # 문서
├── locust.md  # 문서
├── optimization-hardening.md  # 문서
├── performance-testing.md  # 문서
├── README.md  # This file
├── registry.md  # 문서
├── sonarqube.md  # 문서
├── syncthing.md  # 문서
├── terraform.md  # 문서
└── terrakube.md  # 문서
```

## Procedure

> Migrated from `docs/07.operations/09-tooling/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Tooling Tier Procedures (09-tooling)

> `09-tooling` 계층의 실행형 복구/유지보수 런북 모음.

#### Overview

이 디렉터리는 Tooling 계층 장애 상황에서 즉시 실행 가능한 절차를 제공한다. 서비스 단위 복구 런북과 최적화/하드닝 회귀 복구 런북을 함께 관리한다.

#### Documents

- [Performance Testing Procedure](./performance-testing.md)
- [Locust Procedure](./locust.md)
- [k6 Procedure](./k6.md)
- [Registry Procedure](./registry.md)
- [SonarQube Procedure](./sonarqube.md)
- [Syncthing Procedure](./syncthing.md)
- [Terraform Procedure](./terraform.md)
- [Terrakube Procedure](./terrakube.md)
- [Optimization Hardening Procedure](./optimization-hardening.md)

#### Verification Baseline

- `for f in infra/09-tooling/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
- `bash scripts/check-tooling-hardening.sh`
- `bash scripts/check-template-security-baseline.sh`
- `bash scripts/check-doc-traceability.sh`

#### Related References

- [Tooling Usages](../../07.operations/09-tooling/README.md)
- [Tooling Operations](../../07.operations/09-tooling/README.md)
- [Tooling Spec](../../04.specs/09-tooling/spec.md)
- [Tooling Plan](../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- [Tooling Tasks](../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)

---

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

#### Scope

##### In Scope

- 실행 절차와 checklist
- 검증 명령과 evidence source
- rollback 또는 recovery 기준

##### Out of Scope

- 정책 결정 자체
- 학습용 튜토리얼
- postmortem 분석

#### Structure

```text
docs/07.operations/09-tooling/
├── k6.md  # 문서
├── locust.md  # 문서
├── optimization-hardening.md  # 문서
├── performance-testing.md  # 문서
├── README.md  # This file
├── registry.md  # 문서
├── sonarqube.md  # 문서
├── syncthing.md  # 문서
├── terraform.md  # 문서
└── terrakube.md  # 문서
```

#### How to Work in This Area

1. 관련 operation policy를 확인한 뒤 절차, 검증, rollback 항목을 갱신한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
