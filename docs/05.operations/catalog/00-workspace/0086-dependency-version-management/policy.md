---
title: "Dependency Version Management Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0086"
parent_ids:
- "AD-0031"
created: "2026-09-19"
---

# Dependency Version Management Policy

## Overview

Infrastructure version changes must remain reviewable and reproducible on one
HOME/DEV host. A version update does not authorize deployment or data migration.

## Policy Scope

Compose, Dockerfile and inline build sources, the curated registry, Renovate,
Dependabot and runtime-version references in current implementation/operations docs.

## Controls

| Surface | Update owner | Authority and review |
| --- | --- | --- |
| Compose images and normal Dockerfiles | Renovate | enabled Docker managers; source pin changes reviewed |
| OpenTofu inline Dockerfile | Renovate custom manager | narrow declared source pattern, no arbitrary regex scope |
| GitHub Actions and enabled infrastructure managers | Renovate | infrastructure automerge disabled |
| Storybook npm | Dependabot | only configured project directory; no Renovate npm overlap |
| OpenTofu provider/module dependencies | operator-reviewed workspace owner | no tracked provider/module manifests currently exist in the tooling packages; enable a scoped manager with the first such manifest |
| Python validation tools and pre-commit hooks | maintainer review | pinned requirements/hook revisions; these are outside the currently enabled automatic managers |
| Curated image registry | synchronization script | generated proposal from source, fail on ambiguity or missing source |
| Narrative docs | human/agent review and existing metadata validator | authority links; justified exact-literal exceptions only |

Regular patch/minor updates follow the configured soak window and groups. Major
updates stay separate. Security alerts bypass normal waiting and receive explicit
review; urgency does not bypass migration or rollback evidence. This fast path applies to vulnerability alerts the configured manager actually receives; it does not establish container-image CVE scanning or installed-image vulnerability coverage. Do not enable
infra automerge or broaden self-host allowedCommands. Config syntax must pass the
official strict validator with separate repository/global modes.

Image tags are source pins but may remain mutable. Preserve existing digests when
present; propose digest pinning per component after verifying the platform manifest,
update behavior and rollback identity. The current policy does not globally enable
Renovate digest pinning or treat ordinary tags as immutable. Exception exit conditions
may require a verified digest; do not invent one or substitute a registry digest
without resolving the intended architecture and image source.

## Exceptions

Mutable image exceptions live in `infra/image-tag-policy.exceptions.json` with
owner, reason, risk, review cadence and exit condition. A prose exception cannot
waive source-image validation. Review image compatibility before removing an
exception; changing a tag is not evidence of GPU or data-format compatibility.

## Verification

Existing synchronization `--check` is the registry drift gate. Validate Compose,
modified build sources, document contracts and official Renovate config independently.
Never accept registry output as proof of runtime health or backup/restore.

## Review Cadence

Monthly and on manager scope, source parser, image exception or major update changes.

## Traceability

- [Home/Dev architecture](../../../../02.architecture/descriptions/0031-home-development-host.md) (`AD-0031`)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Runtime version projection](../../../../../infra/tech-stack.versions.json)
- [Repository Renovate policy](../../../../../renovate.json5)
- [Dependabot scope](../../../../../.github/dependabot.yml)
