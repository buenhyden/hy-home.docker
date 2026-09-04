---
title: "compose-stack-agent"
version: "1.0.0"
type: "governance/skill"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
function_id: "compose-stack-agent"
scope: "infra"
owner_agent: "infra-implementer"
---

# compose-stack-agent

## Preconditions

An approved Compose specification, exact service scope, and rollback path must exist before configuration mutation.

## Inputs

- Approved Compose specification and current Compose tree.
- Service dependencies, networks, volumes, secrets, health checks, and resource constraints.

## Procedure

1. Resolve the complete affected service graph and compare each requested change with workspace Compose conventions.
2. Implement the smallest atomic YAML/configuration change while preserving external secret references and dependency semantics.
3. Run static Compose validation and any explicitly approved scoped runtime check, then inspect the rendered delta.

## Outputs

- A validated Compose change plus exact configuration and safety evidence.

## Gates

- `docker compose config` or the repository wrapper succeeds.
- Secret values never enter Compose files, logs, or evidence.

## Failure Handling

Stop on unresolved variables, missing secret files, invalid dependency order, or unapproved runtime impact and revert the logical change.

## Related Documents

- [Infrastructure implementer](../roles/infra-implementer.md)
- [Docker Compose patterns](docker-compose-patterns.md)
- [Infrastructure validation](infra-validate.md)
