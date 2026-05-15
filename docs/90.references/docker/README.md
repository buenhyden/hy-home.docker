# Docker References

> Docker image, version drift, registry, and runtime-reference rules

## Overview

`docs/90.references/docker` stores slow-changing Docker reference material used by docs, operations, and validators. It explains how Docker image/version facts are interpreted in this repository.

This folder does not replace Compose files or registry JSON files. Runtime truth remains in `infra/**/docker-compose*.yml`, `infra/tech-stack.versions.json`, and `infra/image-tag-policy.exceptions.json`.

## Category Role

`docs/90.references/docker` explains durable Docker image and version-reference rules. It helps readers understand how Compose image declarations, registry JSON files, and floating-tag exceptions relate to each other without replacing those runtime files.

Use this category for stable interpretation rules and inventory context. Use `docs/05.operations/` for operational procedures and `infra/` for the current runtime source of truth.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Docker image/version drift reference rules
- Tech-stack registry interpretation
- Floating tag exception reference links
- Compose image declaration comparison rules

### Out of Scope

- Deployment procedures
- Service-specific operations runbooks
- New image upgrade execution plans
- Secret values or credential examples

## Structure

```text
docs/90.references/docker/
└── README.md  # This file
```

## Reference Rules

1. Compose files are the runtime source of truth for declared images.
2. `infra/tech-stack.versions.json` is the registry used to check that important images are still declared in Compose files.
3. Floating tags are allowed only when documented in `infra/image-tag-policy.exceptions.json`.
4. Docker reference text should explain durable interpretation rules, not prescribe rollout steps.

## How to Work in This Area

1. Use this folder for stable Docker reference rules only.
2. Update `infra/tech-stack.versions.json` when a major operational image is added to the validated registry.
3. Update `infra/image-tag-policy.exceptions.json` when a floating image tag is intentionally approved.
4. Run `bash scripts/validation/check-repo-contracts.sh` after changing Docker reference docs or registry files.

## Examples

- Airflow image drift is evaluated from the Compose default value such as `${AIRFLOW_IMAGE_NAME:-apache/airflow:3.1.8}`.
- n8n image drift includes both the custom runtime image and the external runner image when both are declared in Compose.

## Related Documents

- [references index](../README.md)
- [image tag exceptions](../../../infra/image-tag-policy.exceptions.json)
- [tech stack versions](../../../infra/tech-stack.versions.json)
- [repo contract checker](../../../scripts/validation/check-repo-contracts.sh)
