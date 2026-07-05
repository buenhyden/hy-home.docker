<!-- Target: docs/90.references/data/docker/README.md -->

# Docker References

> Docker image, version drift, registry, and runtime-reference rules

## Overview

`docs/90.references/data/docker` stores slow-changing Docker reference material used by docs, operations, and validators. It explains how Docker image/version facts and generated Compose inventory facts are interpreted in this repository.

This folder does not replace Compose files or registry JSON files. Runtime truth remains in `infra/**/docker-compose*.yml`, `infra/tech-stack.versions.json`, and `infra/image-tag-policy.exceptions.json`.

## Category Role

`docs/90.references/data/docker` explains durable Docker image and version-reference rules. It helps readers understand how Compose image declarations, registry JSON files, and floating-tag exceptions relate to each other without replacing those runtime files.

Use this category for stable interpretation rules and inventory context. Use `docs/05.operations/` for operational procedures and `infra/` for the current runtime source of truth.

## Language Rule

이 category README와 사람 대상 reference 설명은 한국어를 기본으로 작성하되, Docker image name/tag, Compose path, registry JSON key, validator command는 원문을 보존합니다. Generated 또는 machine-readable registry data는 해당 파일 형식을 우선합니다.

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
- Generated Compose profile/service coverage inventory

### Out of Scope

- Deployment procedures
- Service-specific operations runbooks
- New image upgrade execution plans
- Secret values or credential examples

## Structure

```text
docs/90.references/data/docker/
├── README.md                       # This file
├── compose-profile-service-coverage.md # Generated Compose profile/service coverage snapshot
├── image-version-interpretation.md # Docker image/version source interpretation rules
└── tech-stack-version-provenance.md # Generated tech-stack registry provenance snapshot
```

## Current References

- [compose-profile-service-coverage.md](./compose-profile-service-coverage.md) - generated Docker Compose profile/service coverage snapshot
- [image-version-interpretation.md](./image-version-interpretation.md) - Docker image/version source interpretation rules
- [tech-stack-version-provenance.md](./tech-stack-version-provenance.md) - generated tech-stack registry drift severity and source provenance snapshot

## Reference Rules

1. Compose files are the runtime source of truth for declared images.
2. `infra/tech-stack.versions.json` is the registry used to check that important images are still declared in Compose files.
3. Floating tags are allowed only when documented in `infra/image-tag-policy.exceptions.json`.
4. Generated Compose coverage output is derived inventory and must be regenerated after tracked Compose service/profile changes.
5. Generated tech-stack provenance output is derived registry/Compose evidence and must be regenerated after tracked registry, exception, or listed Compose image changes.
6. Docker reference text should explain durable interpretation rules and inventory context, not prescribe rollout steps.

## How to Work in This Area

1. Use this folder for stable Docker reference rules only.
2. Keep current image values in Compose and registry files, not in reference prose.
3. Update `infra/tech-stack.versions.json` when a major operational image is added to the validated registry.
4. Update `infra/image-tag-policy.exceptions.json` when a floating image tag is intentionally approved.
5. Run `bash scripts/operations/generate-compose-profile-service-coverage.sh` after changing tracked Compose services or profiles.
6. Run `bash scripts/operations/generate-tech-stack-version-provenance.sh` after changing tracked tech-stack registry, floating exception, or listed Compose image declarations.
7. Run `bash scripts/validation/check-repo-contracts.sh` after changing Docker reference docs or registry files.

## Examples

- Airflow image drift is evaluated from the Compose default value such as `${AIRFLOW_IMAGE_NAME:-apache/airflow:3.1.8}`.
- n8n image drift includes both the custom runtime image and the external runner image when both are declared in Compose.

## Related Documents

- [references index](../../README.md)
- [Compose profile/service coverage](./compose-profile-service-coverage.md)
- [image/version interpretation](./image-version-interpretation.md)
- [tech-stack version provenance](./tech-stack-version-provenance.md)
- [image tag exceptions](../../../../infra/image-tag-policy.exceptions.json)
- [tech stack versions](../../../../infra/tech-stack.versions.json)
- [Compose coverage generator](../../../../scripts/operations/generate-compose-profile-service-coverage.sh)
- [tech-stack provenance generator](../../../../scripts/operations/generate-tech-stack-version-provenance.sh)
- [repo contract checker](../../../../scripts/validation/check-repo-contracts.sh)
