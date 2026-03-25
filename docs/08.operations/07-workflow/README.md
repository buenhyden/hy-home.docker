# 07-workflow Operations

> Operational policies and standards for the workflow orchestration tier.

## Overview (KR)

이 폴더는 워크플로우 자동화 티어의 운영 정책, 보안 기준 및 자원 관리 정책을 관리합니다. DAG 배포 승인 절차와 작업자 리소스 할당 기준을 규정합니다.

## Policy Index

### Governance
- [01.dag-deployment.md](./01.dag-deployment.md) — Rules for promoting DAGs from staging to production.
- [02.resource-allocation.md](./02.resource-allocation.md) — Worker concurrency and resource limit standards.

### Data & Logs
- [03.log-retention.md](./03.log-retention.md) — Retention policies for Airflow and n8n execution logs.

## Verification

Compliance with these policies is verified during the CI/CD pipeline and via periodic audits of the `airflow-scheduler` logs.
