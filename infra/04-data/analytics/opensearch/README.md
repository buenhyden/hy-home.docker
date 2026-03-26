<!-- [ID:04-data:analytics:opensearch] -->
# OpenSearch
> Distributed search and analytics engine with Dashboards.

## Overview
The `opensearch` stack provides a scalable search backend for log aggregation, full-text search, and real-time visualization. It is designed for high-availability observability and analytical workloads.

## Audience
- Developers
- Operators
- AI Agents

## Scope

### In Scope
- Docker infrastructure for OpenSearch 2.18 and Dashboards 3.4.0.
- Resource allocation (JVM Heap) and volume persistence.
- Security configurations (Docker Secrets, HTTPS).

### Out of Scope
- Detailed search query logic (see System Guide).
- Index retention policies (see Operations Policy).
- Node recovery procedures (see Runbook).

## Structure
```text
opensearch/
├── opensearch/             # Engine configuration
├── opensearch-dashboards/  # Visualization configuration
├── Dockerfile              # Custom build for security
├── docker-compose.yml      # Standard stack
└── README.md               # This file
```

## How to Work in This Area
1. Read the [System Guide](../../../../docs/07.guides/04-data/analytics/opensearch.md) for architectural context.
2. Check [Operations Policy](../../../../docs/08.operations/04-data/analytics/opensearch.md) for resource governance.
3. Use the [Recovery Runbook](../../../../docs/09.runbooks/04-data/analytics/opensearch.md) for maintenance.

## Related References
- **System Guide**: [opensearch.md](../../../../docs/07.guides/04-data/analytics/opensearch.md)
- **Operations Policy**: [opensearch.md](../../../../docs/08.operations/04-data/analytics/opensearch.md)
- **Recovery Runbook**: [opensearch.md](../../../../docs/09.runbooks/04-data/analytics/opensearch.md)
- **Monitoring**: `opensearch-exporter:9114/metrics`

---
Copyright (c) 2026. Licensed under the MIT License.
