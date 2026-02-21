---
trigger: model_decision
glob: ["**/pipelines/**", "**/etl/**", "**/dbt/**", "**/airflow/**"]
description: "Data Engineering Standards: Enforces idempotent ETL/ELT pipelines, schema-first design, and rigorous data quality validation."
---

# Data Engineering Standards

- **Role**: Data Engineering Architect
- **Purpose**: Define standards for building reliable, scalable, and observable data pipelines and storage architectures (Lakehouse/Warehouse).
- **Activates When**: Developing ETL/ELT jobs, configuring orchestrators (Airflow), or defining transformation models (dbt).

**Trigger**: model_decision — Apply during the design and implementation of data infrastructure.

## 1. Standards

### Principles

- **[REQ-DATE-01] Idempotent Pipeline Design**
  - All data pipelines MUST be idempotent. Re-running a job for the same time period MUST yield the same result without data duplication.
- **[REQ-DATE-02] Schema-First Integrity**
  - Data models MUST be defined with explicit schemas. Schema-on-read is PROHIBITED for production-grade transformation layers.
- **[REQ-DATE-03] Automated Data Quality (DQ) Gates**
  - Every pipeline stage MUST include automated data quality checks (e.g., uniqueness, nullness, range validation) before data promotion.

### Data Ecosystem Baseline

| Tool | Requirement ID | Critical Standard |
| --- | --- | --- |
| Orchestration | [REQ-DATE-04] | Airflow (DAG-based isolation) |
| Transformation | [REQ-DATE-05] | dbt (modular SQL/Python) |
| Storage | [REQ-DATE-06] | Parquet/Delta Lake (Versioned) |
| Monitoring | [REQ-DATE-07] | Data lineage & SLA tracking |

### Must

- **[REQ-DATE-08] Versioned Transformation Code**
  - All transformation logic (dbt models, Spark jobs) MUST be version-controlled and tested in an environment matching production.
- **[REQ-DATE-09] Functional Data Partitioning**
  - Large datasets MUST be partitioned by logical keys (e.g., `event_date`) to optimize query performance and data lifecycle management.
- **[REQ-DATE-10] Standardized Error Dead-Letter-Queues (DLQ)**
  - Records failing validation or transformation MUST be routed to a DLQ for manual audit and potential re-processing.

### Must Not

- **[BAN-DATE-01] Mutation of Production Seeds**
  - Avoid using manual "seeds" or static files for primary production data; utilize automated ingestion from source systems.
- **[BAN-DATE-02] Cross-DAG Dependency Coupling**
  - Do NOT hard-link Airflow DAGs; utilize ExternalTaskSensors or metadata-driven orchestration to maintain decoupling.

### Failure Handling

- **Stop Condition**: Stop pipeline execution if the "Data Quality Gate" identifies a violation in the "Critical" tier (e.g., > 1% nulls in primary keys).

## 2. Procedures

- **[PROC-DATE-01] Lineage Impact Analysis**
  - IF modifying a core data model THEN MUST conduct an impact analysis on downstream dashboard and report dependencies.
- **[PROC-DATE-02] Cost Monitoring**
  - Perform a monthly audit of compute resource usage (e.g., Snowflake credits, Databricks DBUs) to optimize query efficiency.

## 3. Examples

### dbt Test Configuration (Good)

```yaml
models:
  - name: dim_users
    columns:
      - name: user_id
        tests:
          - unique
          - not_null
```

## 4. Validation Criteria

- **[VAL-DATE-01] DQ Assertion Pass**
  - [ ] 100% of pipeline runs pass the mandatory "Bronze-to-Silver" data quality assertions.
- **[VAL-DATE-02] Lineage Clarity**
  - [ ] Data catalog correctly visualizes the end-to-end lineage from source ingestion to the final BI layer.
- **[VAL-DATE-03] Idempotency Verification**
  - [ ] Manual test confirms that re-executing a backfill job does not result in duplicate primary keys.
