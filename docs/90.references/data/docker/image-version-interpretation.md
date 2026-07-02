---
status: active
---
<!-- Target: docs/90.references/data/docker/image-version-interpretation.md -->

# Reference: Docker Image and Version Interpretation

## Overview

This reference explains how Docker image and version information should be interpreted in `hy-home.docker`. It does not duplicate current image values or rollout procedures; it only explains how to read Compose declarations and registry files.

## Purpose

Clarify which files should be treated as sources when reading Docker image/version documents and validation results.

## Repository Role

This reference provides stable context for interpreting Docker image drift, floating tag exceptions, and the tech-stack registry. Current runtime truth lives in `infra/**/docker-compose*.yml`, `infra/tech-stack.versions.json`, `infra/image-tag-policy.exceptions.json`, and validation scripts.

## Scope

### In Scope

- Interpretation rules for Compose image declarations
- Role separation between the tech-stack registry and Compose sources
- Reference boundary for floating tag exceptions
- Source priority when writing Docker image/version documents

### Out of Scope

- Copy of the current image tag inventory
- image upgrade rollout plan
- deployment procedure or rollback runbook
- secret values, credentials, tokens
- unverified copy of the latest external registry release status

## Definitions / Facts

- **Compose image declaration**: Service image value declared in Docker Compose files. It is the primary source for current runtime configuration.
- **Tech-stack registry**: Validation-target image registry in `infra/tech-stack.versions.json`. It is used to confirm that important images remain present in Compose.
- **Floating tag exception**: An intentionally allowed non-pinned tag such as `latest`, a branch tag, or a mutable tag. The allowance rationale lives in `infra/image-tag-policy.exceptions.json`.
- **Version drift**: A state where image declarations expected by the registry or policy differ from Compose sources. Drift decisions must check both validator results and tracked source files.

## Source Rules

- Check current Docker image declarations in Compose files.
- Check whether important images are registered for validation in `infra/tech-stack.versions.json`.
- Check floating tag allowances in `infra/image-tag-policy.exceptions.json`.
- Validator results are evidence that helps interpretation; they do not replace original source files.
- Recheck current external registry, release note, or vendor page status when that latest status is needed.

## Sources

- [Docker reference category](./README.md) - Docker reference category role and working rules
- [tech stack versions](../../../../infra/tech-stack.versions.json) - tracked registry for important Docker images
- [image tag exceptions](../../../../infra/image-tag-policy.exceptions.json) - tracked floating tag exception registry
- [repo contract checker](../../../../scripts/validation/check-repo-contracts.sh) - repository contract validation for Docker image/tag policy and version drift

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when Docker image policy, registry validation, or Compose source ownership changes
- **Update Trigger**: Update when Docker image interpretation rules change, not when an individual image tag changes

## Related Documents

- [Docker references](./README.md)
- [90.references](../../README.md)
- [docs index](../../README.md)
- [reference template](../../../99.templates/templates/common/reference.template.md)
