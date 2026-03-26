# StarRocks (OLAP Warehouse)
>
> High-performance analytical database for real-time analytics.

## Overview

The `warehouses` stack provides a StarRocks cluster (FE and BE nodes) for sub-second OLAP queries and large-scale data warehousing. It is integrated with `infra_net` for secure data ingestion and querying.

## Audience

- Data Engineers
- Analytics Developers
- AI Agents

## Scope

### In Scope

- StarRocks Frontend (FE) and Backend (BE) nodes.
- Local volume persistence for data and metadata.
- Health monitoring via Prometheus Exporter.

### Out of Scope

- External catalog integration (e.g., Iceberg, Hudi) - see System Guide.
- Routine data ingestion (ETL) procedures.
- Resource partitioning and multi-tenancy.

## Structure

```text
warehouses/
├── fe/                 # Frontend metadata and configuration
├── be/                 # Backend storage and computation
├── docker-compose.yml  # Standard StarRocks stack
└── README.md           # This file
```

## How to Work in This Area

1. Read the [System Guide](../../../../docs/07.guides/04-data/analytics/warehouses.md) for architectural context.
2. Check [Operations Policy](../../../../docs/08.operations/04-data/analytics/warehouses.md) for resource governance.
3. Use the [Recovery Runbook](../../../../docs/09.runbooks/04-data/analytics/warehouses.md) for maintenance.

## Related References

- **System Guide**: [warehouses.md](../../../../docs/07.guides/04-data/analytics/warehouses.md)
- **Operations Policy**: [warehouses.md](../../../../docs/08.operations/04-data/analytics/warehouses.md)
- **Recovery Runbook**: [warehouses.md](../../../../docs/09.runbooks/04-data/analytics/warehouses.md)
- **Monitoring**: `starrocks-fe:8030/metrics`

---
Copyright (c) 2026. Licensed under the MIT License.
