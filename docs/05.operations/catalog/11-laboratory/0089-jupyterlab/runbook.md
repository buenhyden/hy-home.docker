---
title: "JupyterLab Recovery Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "RUN-0089"
parent_ids:
- "GDE-0089"
created: "2026-09-21"
---

# JupyterLab Recovery Runbook

## When to Use

Start failure, token exposure, stuck kernels, lost work files, or image upgrade.

## Procedure

1. Inspect from the repository root:

   ```bash
   docker compose --profile core --profile data-science config --quiet
   docker compose --profile core --profile data-science ps -a jupyterlab
   docker compose --profile core --profile data-science logs --tail=100 jupyterlab
   ```

2. Exit `64` means the token secret is missing or shorter than 16 characters. A
   bind error means `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work` does not exist;
   create it with owner UID 1000 instead of letting Docker create it.
3. For a suspected token exposure: stop the service, replace
   `secrets/tools/jupyter_token.txt` through the registered secret workflow,
   review the work directory for unexpected files, then start again. Existing
   browser cookies stop working after the restart.
4. For stuck kernels, restart the kernel from the UI; restart the container only
   when the server itself is unresponsive.

### Restore and upgrade

1. Stop the service and copy the work directory; record the source commit and
   file count.
2. Restore to a new directory and start an isolated instance against it before
   replacing the live directory.
3. For an image upgrade, rebuild in an approved environment and open a notebook
   that imports every pinned library and logs one MLflow run.

## Evidence

Record exit codes, image tag, source commit and file counts. Never record the
token or notebook contents.

## Rollback or Recovery

Configuration rollback restores Compose and requirements from Git; the previous
image must be rebuilt. Work-directory restore is **planned but unexecuted**.

## Escalation

Stop on evidence of unknown code execution, a request for multi-user access
without JupyterHub, or a request to disable the token.

## Traceability

- [Guide](guide.md) (`GDE-0089`)
- [Policy](policy.md) (`POL-0089`)
- [JupyterLab Compose](../../../../../infra/11-laboratory/jupyterlab/docker-compose.yml)

## Related Documents

- [Image Dockerfile](../../../../../infra/11-laboratory/jupyterlab/Dockerfile) and [derived version projection](../../../../../infra/tech-stack.versions.json)
- [MLflow runbook](../0088-mlflow/runbook.md)
