# Workflow (07-workflow)

## Overview

Workflow orchestration tools for automation and data pipelines. **n8n** is part of the core stack, while **Airflow** is available via profiles for more advanced scheduling.

## Services

| Service | Profile | Path | Notes |
| --- | --- | --- | --- |
| n8n | (core) | `./n8n` | Workflow automation with queue mode |
| Airflow | `airflow` | `./airflow` | Orchestrator (CeleryExecutor) |

## Run

```bash
# Core workflow
docker compose up -d n8n

# Airflow stack (optional)
docker compose --profile airflow up -d
```

## Notes

- Airflow can also enable `flower` and `debug` profiles for monitoring and debug services.
- Both stacks typically rely on shared DB/queue services from `infra/04-data`.

## File Map

| Path | Description |
| --- | --- |
| `n8n/` | n8n worker/queue setup. |
| `airflow/` | Airflow CeleryExecutor stack. |
| `README.md` | Category overview. |
