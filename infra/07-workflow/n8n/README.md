# n8n Low-code Automation

> [!NOTE]
> Rapid workflow automation and third-party integrations with visual logic.

---

## Overview (KR)

n8n은 시각적 인터페이스를 통해 워크플로우 자동화를 구현하는 로우코드 도구이다. 복잡한 Airflow DAG와 달리 직관적인 노드 연결을 통해 API 통합, 웹후크 처리, 이벤트 기반 자동화를 빠르게 배포할 수 있다.

## Tech Stack

| Component | Technology | Version | Note |
| :--- | :--- | :--- | :--- |
| Core Service | n8n | 2.15.0 | Node.js based |
| Metadata DB | PostgreSQL | 16-alpine | Managed via `infra/04-data/postgres-mng` |
| Queue Broker | Valkey (Redis) | 9.0.2 | External queue orchestration |
| Task Runner | n8nio/runners | 2.15.0 | Isolated execution environment |

## Architecture

n8n 환경은 고성능 및 확장성을 위해 분산 모드로 구성된다:

- **Main Service**: UI 제공 및 워크플로우 관리.
- **Worker**: 실제 태스크 실행 담당 (Valkey 큐 기반).
- **Task Runner**: 특정 복잡한 태스크를 격리된 환경에서 안전하게 처리.
- **Valkey**: 워커 간 작업 분배를 위한 메시지 브로커.

## AI Agent Guidance

1. **Modularization**: 복잡한 로직은 `Sub-workflows`를 활용하여 분리하고 재사용성을 확보하십시오.
2. **Credential Safety**: 모든 외부 인증 정보는 n8n 내부의 `Credentials` 시스템에 암호화되어 저장되어야 하며, `docker-compose.yml`의 시크릿(`secrets`)을 통해 안전하게 공급됩니다.
3. **Execution Mode**: `EXECUTIONS_MODE: queue`로 설정되어 있으므로 대량의 병렬 작업 처리가 가능합니다.

## Traceability (Golden 5)

- **PRD**: [07-workflow PRD](../../../docs/01.prd/2026-03-26-07-workflow.md)
- **ARD**: [07-workflow ARD](../../../docs/02.ard/0007-workflow-architecture.md)
- **ADR**: [N8N Integration ADR](../../../docs/03.adr/0007-airflow-n8n-hybrid-workflow.md)
- **Spec**: [07-workflow Technical Spec](../../../docs/04.specs/07-workflow/spec.md)
- **Plan**: [07-workflow Implementation Plan](../../../docs/05.plans/2026-03-26-07-workflow-standardization.md)

## Operational Documentation

- **System Guide**: [n8n System Guide](../../../docs/07.guides/07-workflow/n8n.md)
- **Operations Policy**: [n8n Operations Policy](../../../docs/08.operations/07-workflow/n8n.md)
- **Recovery Runbook**: [n8n Recovery Runbook](../../../docs/09.runbooks/07-workflow/n8n.md)

---

## Overview

`infra/07-workflow/n8n`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

## Structure

```text
infra/07-workflow/n8n/
├── custom/  # 하위 구성 영역
├── dev.Dockerfile  # 구성 파일
├── docker-compose.dev.yml  # Docker Compose 정의
├── docker-compose.yml  # Docker Compose 정의
├── docker-entrypoint.dev.sh  # 구성 파일
├── docker-entrypoint.sh  # 구성 파일
├── Dockerfile  # 구성 파일
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Related References

- [infra/README.md](../../README.md)
- [docs/07.guides/README.md](../../../docs/07.guides/README.md)
- [docs/08.operations/README.md](../../../docs/08.operations/README.md)
- [docs/09.runbooks/README.md](../../../docs/09.runbooks/README.md)
