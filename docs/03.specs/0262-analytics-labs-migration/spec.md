---
title: "Analytics Labs Migration Specification"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0262"
parent_ids:
- "REQ-0005"
- "REQ-0010"
- "REQ-0011"
- "REQ-0012"
- "AD-0011"
- "AD-0012"
created: "2026-11-04"
---

# Analytics Labs Migration Specification

## Overview

### Intent

Move the OPTIONAL analytics services, SonarQube and Stalwart out of the root
Compose into standalone LAB entrypoints under `labs/`, so the root model only
holds HOME and the remaining OPTIONAL services.

### Owning Requirements

On 2026-11-04 the owner chose to move the lakehouse bundle (Spark, Flink
JobManager and TaskManager, Trino, Great Expectations and the SeaweedFS table
bucket job), dbt with its provisioner, Superset with its init and provisioner,
and JupyterLab into `labs/`. The same day the owner added SonarQube and
Stalwart with its config helper. None of these services has a consumer outside
its own cluster; all are OPTIONAL in the service consolidation ledger.

This Spec makes concrete REQ-0005, REQ-0010, REQ-0011 and REQ-0012 and the Architecture Descriptions AD-0011 and AD-0012, its frontmatter `parent_ids`. The body cites no REQ-####-FR or REQ-####-NFR identifier.

## Scope

### In Scope

- LAB entrypoints `labs/lakehouse/docker-compose.yml`, `labs/dbt/docker-compose.yml`, `labs/superset/docker-compose.yml`,
  `labs/jupyterlab/docker-compose.yml`, `labs/sonarqube/docker-compose.yml` and `labs/stalwart/docker-compose.yml`, with
  their build and bind assets moved under `labs/`.
- Removal of their root includes and of root secrets only they used.
- Every current reference: tests, hardening, the secret catalog, the
  supply-chain ledger, READMEs, Stage 01 and 02 statements, and the Stage 05
  documents, which move to the `15-labs` family with their identities kept.

### Non-goals

- Kafka and every `05-messaging` service, MLflow and its provisioner, SeaweedFS
  master, volume, filer, S3 and bucket job, `mng-pg`, `dev-pg`, Keycloak and
  Mailpit stay in the root.
- Making a HOME service reachable from a LAB network, moving existing data,
  migrating OpenBao KV paths, and any runtime start, push or merge.

## Behavior Contract

### Normal Behavior

Each LAB is its own Compose project `hy-home-lab-<name>`, labelled
`hy-home.tier: lab`, with no Traefik route and only LAB networks, as SPEC-0215
requires. A HOME dependency is a required `LAB_*` endpoint input. Secret files
keep their canonical root paths, as the Supabase LAB does. Data binds under
`LAB_DATA_DIR`.

Static rendering proves declaration only. A LAB that needs a HOME service is
render-only until the owner approves a reachable endpoint.

### Failure and Edge Cases

A LAB rendered without a required endpoint or data root refuses to render.

No secret value is read. No container is started. The root profiles
`lakehouse`, `bi` and `data-science` keep selecting their HOME base services.

**Observable failures.**

The root still selects a moved service, a LAB shares a root network, or a
current document names a removed path.

**Stop boundaries.**

This Task pushes, merges and starts nothing.

## Acceptance Criteria

### Criteria

1. The root renders without the moved services; the wildcard service count
   drops by exactly the moved services.
2. Every new LAB renders on its own and passes the LAB isolation tests.
3. No current reference points at a removed path; historical evidence stays.
4. The moved Stage 05 documents live in `15-labs` with their identities.
5. The document, hardening and unit checks pass locally, with actual results
   in the Task.

### Evidence Requirements

- Criterion 1 is observed by `docker compose config` on the root, comparing the `--profile '*' config --services` count before and after (`compose-root` row).
- Criterion 2 is verified by rendering each LAB file with `docker compose config`, the LAB isolation and infra tier layout unit tests, and the `scripts/operations/lab.py check` controller checks (`compose-lab`, `lab-isolation`, `lab-controller*` and `security-review` rows); a controller check not run stays `NOT_RUN`.
- Criterion 3 is verified by `check-all-hardening.sh`, the unit suite and `check-script-manifest.py`; criterion 4 by `check-operations-catalog.py`.
- Criterion 5 is verified by `check-document-metadata.py`, `check-document-links.py`, `check-document-corpus-lifecycle.py` and the hosted CI row.
- The frontmatter owner (`@buenhyden`) judges each criterion and records the decision in the Task's Criterion Acceptance table; a failed, blocked or skipped check is reported as such and does not count as met.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](tasks/tsk-0001-analytics-labs-migration.md)

### Historical and Navigation

No retired, superseded or purely navigational link applies to this Spec.
