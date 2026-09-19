---
title: "09-tooling: Tooling Tier"
version: "1.0.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
created: "2025-11-12"
---

# 09-tooling: Tooling Tier

## Overview

The root Compose project includes every tooling leaf; profiles alone select work.
The current map is exact:

| Profile | Services | Runtime class |
| --- | --- | --- |
| `tooling` | `registry`, `sonarqube` | optional management services |
| `registry` | `registry` | OCI storage |
| `sast` | `sonarqube` | code-quality service |
| `testing` | `k6`, `locust-master`, `locust-worker` | explicit load-test jobs/services |
| `iac` | `opentofu`, `terrakube-api`, `terrakube-ui`, `terrakube-executor` | explicit infrastructure tooling |
| `dependency-update` | `renovate` | one-shot remote repository maintenance |

`tooling` does not select IaC or load generation. Terraform and Syncthing runtime
were removed; OpenTofu is the current CLI engine. None of these services is part
of the HOME selector.

## Audience

Platform operators, developers using these tools, security reviewers, and
documentation agents responsible for the tooling profile contract.

## Scope

- [k6](k6/README.md) and [Locust](locust/README.md) generate traffic only after
  target-owner approval. k6 is one-shot; Locust has master and worker services.
- [OpenTofu](opentofu/README.md) is a local CLI job with workspace state and
  read-only provider credential mounts. Plan and apply are separate approvals.
- [Terrakube](terrakube/README.md) stores metadata in management PostgreSQL,
  state objects in MinIO, and transient coordination in Valkey. The three fixed
  services on one host are not an HA deployment.
- [Registry](registry/README.md) persists OCI objects under
  `${DEFAULT_REGISTRY_DIR}`. Current Compose publishes port 5000 without tracked
  TLS/auth, so exposure must be bounded before use.
- [SonarQube](sonarqube/README.md) persists authority in PostgreSQL plus declared
  data/log volumes. Search indexes are derived, but database and extensions/config
  must be recovered consistently.
- [Renovate](renovate/README.md) uses a Docker Secret token and disposable cache.
  A live job can create remote branches/PRs and needs explicit authorization.

## Structure

```text
09-tooling/
├── k6/          # one-shot load job
├── locust/      # master/worker load service
├── opentofu/    # IaC CLI job
├── terrakube/   # IaC automation API/UI/executor
├── registry/    # OCI Distribution storage
├── sonarqube/   # code-quality/SAST service
├── renovate/    # dependency-update job
└── README.md
```

## How to Work in This Area

Use the [documentation index](../../docs/README.md), then the exact Stage 05
subjects under `docs/05.operations/catalog/09-tooling/` (`0061`, `0062`, `0065`,
`0066`, `0069`, `0082`, `0083`). Run from the repository root:

```bash
bash scripts/hardening/check-all-hardening.sh 09-tooling
HYHOME_COMPOSE_PROFILES=testing bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES=iac bash scripts/validation/validate-docker-compose.sh
```

Static validation is not load-test, IaC apply, backup/restore, remote update, or
service readiness evidence. Compose/Dockerfile declarations own runtime pins;
[tech-stack.versions.json](../tech-stack.versions.json) is a derived image projection.

## Related Documents

- [Documentation index](../../docs/README.md)
- [Infrastructure index](../README.md)
- Stage 05 tooling package: `docs/05.operations/catalog/09-tooling/README.md`
