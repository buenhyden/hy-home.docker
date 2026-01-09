---
trigger: always_on
glob: "**/*.py"
description: "Airflow: DAG Design, Idempotency, and Task best practices."
---
# Airflow Standards

## 1. DAG Design

- **Idempotency**: Every DAG run must be repeatable and produce the same result for the same time interval.
- **Atoms**: Tasks should be atomic (one logical step). Avoid "God Tasks" that do everything.
- **Dependencies**: Use the `>>` operator for clear, visual dependency definition.

### Example: Idempotency

**Good**
> A task that overwrites a specific partition for `ds` (execution date).

**Bad**
> A task that appends data to a table without checking if it already exists. (Running twice doubles the data).

## 2. Code Practices

- **Templates**: Always use Jinja templates (`{{ ds }}`) for dynamic dates. NEVER use `datetime.now()` inside task logic.
- **Providers**: Use specialized Operators (S3ToRedshift, PostgresOperator) instead of generic PythonOperator with manual SQL.
- **Variables**: Use Airflow Variables/Connections instead of hardcoded secrets.

## 3. Scheduling

- **Catchup**: Set `catchup=False` by default unless you explicitly need to backfill.
- **Pools**: Use Pools to limit concurrency for heavy tasks (e.g., hitting a limited external API).

## 4. Monitoring

- **Callbacks**: Implement `on_failure_callback` to send alerts (Slack/Email).
- **SLA**: Set `sla` parameters for time-sensitive pipelines.
