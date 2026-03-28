# 08.operations

## 목적

이 폴더는 운영 정책(Operations Policy)과 공통 기준을 저장한다. 이곳의 문서는 무엇을 허용하고 금지하는지, 어떤 기준과 통제를 지켜야 하는지를 정의한다.

## 문서 책임

- 운영 기준과 통제 정의
- 환경 및 배포 승격 조건 정의
- 보안·로그·증적·보존 기준 정의
- AI Agent 변경 통제 정의

## 포함할 내용

- 운영 정책
- SLO/SLI 기준
- 보안 기준
- 배포 승격 기준
- 로그/증적/보존 정책
- 모델/프롬프트 변경 관리 정책
- 예외 승인 절차

## 포함하지 말아야 할 내용

- 실제 명령 절차
- 장애 타임라인
- 근본 원인 분석
- 온보딩 또는 how-to 설명

위 내용은 각각 `09.runbooks/`, `10.incidents/`, `11.postmortems/`, `07.guides/`로 분리한다.

## Agent 운영 정책 예시

- Model/Prompt 변경 프로세스
- Eval·Guardrail 통과 기준
- Safety Incident 임계값
- Trace/Log 보존 기준

## Traceability Links

- [05.plans (Implementation Plan Index)](../05.plans/README.md)
- [09.runbooks (Operational Procedure Index)](../09.runbooks/README.md)

## Tier Index

| Tier | Description |
| :--- | :--- |
| [12-infra-service-optimization-catalog](./12-infra-service-optimization-catalog.md) | Cross-tier optimization and expansion recommendations for all infra services |
| [13-common-optimizations-template-exceptions](./13-common-optimizations-template-exceptions.md) | Official exception registry policy for common optimization templates |
| [01-gateway](./01-gateway/README.md) | Ingress and traffic management |
| [02-auth](./02-auth/README.md) | Identity and access control |
| [03-security](./03-security/README.md) | Network hardening and auth policies |
| [04-data](./04-data/README.md) | Database persistence, backups, and lake/object storage policies |
| [05-messaging](./05-messaging/README.md) | Event streaming and message brokering policies |
| [06-observability](./06-observability/README.md) | Retention, alerting, and LGTM stack governance |
| [07-workflow](./07-workflow/README.md) | Workflow orchestration and automation policies (Airflow, n8n, airbyte) |
| [08-ai](./08-ai/README.md) | AI model inference and RAG governance |
| [09-tooling](./09-tooling/README.md) | DevOps and automation governance |
| [10-communication](./10-communication/README.md) | External communication and mail policies |

## Templates

- `../99.templates/operation.template.md`
