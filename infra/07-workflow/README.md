# Workflow (07-workflow)

> Automation workflows, ETL pipelines, and task orchestration.

## Overview (KR)

이 티어는 시스템 전반의 자동화 워크플로우, ETL 파이프라인 및 작업 오케스트레이션을 관리합니다. Apache Airflow(프로그래밍 방식)와 n8n(Low-code 방식)을 통해 복잡한 비즈니스 로직과 데이터 흐름을 자동화합니다.

## Overview

The Workflow tier provides the infrastructure for automating repetitive tasks and orchestrating complex data pipelines. It balances power and ease-of-use by offering Apache Airflow for programmatic, highly-customizable DAGs and n8n for rapid, low-code automation and third-party integrations.

## Structure

```text
07-workflow/
├── airflow/            # Programmatic workflow orchestration (DAGs)
├── n8n/                # Low-code automation and integrations
└── README.md           # This file
```

---

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Orchestrator | [Apache Airflow](https://airflow.apache.org/) | Python-based programmatic DAGs |
| Automation | [n8n](https://n8n.io/) | Low-code workflow automation |
| Broker | [Valkey](https://valkey.io/) | Dedicated instances for task queuing |
| Database | [PostgreSQL](../04-data/postgresql-cluster/) | Management cluster for metadata |

## Optimization Note (March 2026)

> [!IMPORTANT]
> Both services in this tier utilize the Management PostgreSQL cluster for persistence. Airflow is configured with `CeleryExecutor` for high scalability, brokered by a dedicated Valkey instance.

## SSoT References

- **Guides**: [Workflow Implementation Guide](../../docs/07.guides/07-workflow/README.md)
- **Operations**: [Workflow Scaling & Retention](../../docs/08.operations/07-workflow/README.md)
- **Secrets**: [Workflow Credentials](../../secrets/SENSITIVE_ENV_VARS.md#07-workflow)

---

## License

Copyright (c) 2026. Licensed under the MIT License.
