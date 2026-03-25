# n8n (Low-code Automation)

> Low-code workflow automation tool connecting 400+ apps and services.

## Overview (KR)

n8n은 로우코드 워크플로우 자동화 도구로, 다양한 앱과 서비스를 코드 없이 연결할 수 있습니다. 자체 호스팅을 통해 데이터 주권을 유지하며, Valkey를 브로커로 사용하는 큐 모드로 고성능 자동화를 지원합니다.

## Overview

n8n provides a visual interface for building automation workflows. It is the designated "rapid prototyping" orchestrator in the `hy-home.docker` stack. This implementation includes a custom Dockerfile with CJK fonts and Python support, and operates in `queue` mode with dedicated Valkey workers for parallel execution.

## Structure

```text
n8n/
├── custom/              # Custom n8n nodes
├── Dockerfile          # CJK + Python custom image
├── docker-compose.yml  # n8n stack with worker and runner
├── docker-entrypoint.sh # Custom initialization script
└── README.md           # This file
```

---

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Base Image | `n8nio/n8n:2.12.3` | Community edition |
| Broker | Valkey (9.0.2) | Queue broker for Bull |
| Task Runner | `n8nio/runners` | External node execution |
| Runtime | Node.js / Python | Integrated Python support |

## Configuration

### Services & Resources

| Service | Role | Resources |
| :--- | :--- | :--- |
| `n8n` | Main UI & Scheduler | 1.0 CPU / 2G |
| `n8n-worker` | Workflow Execution | 1.0 CPU / 2G |
| `n8n-task-runner`| Sandbox execution | 0.5 CPU / 1G |

### Environment Variables

| Variable | Description |
| :--- | :--- |
| `EXECUTIONS_MODE` | Set to `queue` (scalable) |
| `WEBHOOK_URL` | `https://n8n.${DEFAULT_URL}` |

## Persistence

- **Database**: PostgreSQL (mng-pg) using the `n8n` database.
- **Config**: Volume `n8n-data` mounted at `/home/node/.n8n`.
- **Custom Nodes**: Mounted from `./custom` directory.

## Operational Status

> [!WARNING]
> n8n is disabled in the root `docker-compose.yml` by default to conserve resources. Enable it by uncommenting the include entry for this directory.

---

## License

Copyright (c) 2026. Licensed under the MIT License.
