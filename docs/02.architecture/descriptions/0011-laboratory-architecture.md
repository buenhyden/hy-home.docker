---
title: "11-laboratory Architecture Description"
version: "1.1.0"
type: "sdlc/architecture-description"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "architecture"
artifact_id: "AD-0011"
parent_ids:
- "REQ-0012"
created: "2026-03-26"
---

# 11-laboratory Architecture Description

## Context and Stakeholders

The laboratory tier contains optional operator and knowledge-work tools. It is
outside HOME and must not affect core traffic when absent. Its broad visibility
into Docker, Redis/Valkey, provider APIs, and notebook content makes it an admin
security boundary rather than a harmless dashboard layer.

## System Boundaries

- **Dozzle:** `admin`/`admin-logs`; reads Docker logs through a read-only socket,
  stores settings under `/data`, and uses both native OIDC configuration and the
  tracked gateway controls. A read-only socket does not restrict Docker API reads.
- **RedisInsight:** `admin`/`admin-data`; stores local connections/settings under
  `/data` and manages external Redis/Valkey targets. Target data remains owned by
  each target service. Current Compose does not declare `RI_ENCRYPTION_KEY`.
- **Open Notebook:** `admin`/`notebook`; stores local app data under `/app/data`,
  connects to separately owned SurrealDB, and uses password/encryption-key Docker
  Secrets. Provider/API egress is a distinct authorization boundary.
- **SurrealDB:** owned by `infra/04-data/specialized/surrealdb`, selected by
  `admin`, `notebook`, or `surrealdb`, and persists Open Notebook records under
  `/mydata`.
- **Non-goals:** this tier does not own primary Redis/Valkey backups, copied Docker
  logs, production notebook workloads, or Metabase. No current Metabase service is
  declared in this tier.

## Components

```mermaid
flowchart LR
  Admin --> Gateway
  Gateway --> Dozzle --> DockerAPI[Docker API/logs]
  Gateway --> RedisInsight --> Targets[Redis/Valkey targets]
  Gateway --> Notebook[Open Notebook]
  Notebook --> SurrealDB[(SurrealDB /mydata)]
  Notebook --> Providers[approved model/provider APIs]
```

## Data Flow

Dozzle requests Docker log streams, RedisInsight opens operator-defined target
connections, and Open Notebook sends approved provider requests while persisting
application records in SurrealDB. These flows are independent; selecting one
narrow profile must not grant another tool's target or API access.

## Deployment View

The root project includes the three laboratory leaves and the separate SurrealDB
leaf. `admin` selects all four services; narrower profiles are `admin-logs`,
`admin-data`, and `notebook`. There is no `dev` profile for these services.

## Quality Attributes

- **Security:** preserve gateway/allowlist/authentication controls, protect local
  settings databases, and never expose provider credentials, target passwords,
  logs, notebook content, or encryption keys in evidence.
- **Recoverability:** Dozzle settings can be restored without a production Docker
  socket. RedisInsight local settings and each target database recover separately.
  Open Notebook recovery requires app data, SurrealDB data, and the matching
  encryption key at one recovery point; loss of the key can make provider secrets
  unreadable.
- **Isolation:** restore rehearsals block provider egress, production Docker API,
  and production data targets until sanitized acceptance passes.

## Traceability

- [Dozzle operations](../../05.operations/guides/0072-dozzle.md)
- [Open Notebook operations](../../05.operations/guides/0073-open-notebook.md)
- [RedisInsight operations](../../05.operations/guides/0076-redisinsight.md)

## Related Documents

- [Laboratory requirement](../../01.requirements/0012-laboratory.md)
- [Laboratory decision](../decisions/0011-laboratory-services.md)

Runtime pins are owned by Compose/Dockerfile declarations; the
[derived Compose image projection](../../../infra/tech-stack.versions.json) supplies drift verification.
