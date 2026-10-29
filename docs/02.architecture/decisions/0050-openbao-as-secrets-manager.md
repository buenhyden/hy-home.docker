---
title: "OpenBao as Secrets Manager"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "architecture"
artifact_id: "ADR-0050"
parent_ids:
- "AD-0003"
created: "2026-10-29"
---

# ADR-0050: OpenBao as Secrets Manager

## Context

ADR-0003 chose HashiCorp Vault as the secrets manager and was deprecated on
2026-10-15. ADR-0018 (accepted) still describes the Vault and `vault-agent`
hardening strategy. Vault and `vault-agent` were removed in SPEC-0180 S08, and
[AD-0003](../descriptions/0003-security-architecture.md) already names OpenBao
plus `openbao-agent` as the canonical HOME implementation. No accepted record
states that decision, so two decisions that describe a removed product remain
the nearest ADRs.

## Decision Drivers

- One current decision record must own the secrets manager choice.
- The record must match the tracked implementation in
  [`infra/03-security/openbao`](../../../infra/03-security/openbao/docker-compose.yml).
- Unseal method, backup custody and operations keep their own owners.

## Options

### Alternatives

- Keep ADR-0003 and ADR-0018 as the owners: rejected; they describe a removed
  product and leave the current choice undecided in the ADR set.
- Amend ADR-0003 in place: rejected; its Vault decision and 2026-03-26
  acceptance are historical evidence.

## Decision

OpenBao is the platform secrets manager. `openbao-agent` is the HOME
implementation of consumer secret rendering.

1. OpenBao runs as a single-node integrated Raft service in
   `infra/03-security/openbao`, with its own audit file volume and a Traefik UI
   route. Multi-node Raft HA is not part of this decision.
2. `openbao-agent` authenticates with AppRole and renders approved templates to
   the declared output volume for consumer services.
3. Humans sign in through native Keycloak OIDC; the root token is break-glass.
4. The unseal method is owned by [ADR-0042](0042-openbao-unseal-method.md).
   Operational controls, bootstrap, recovery and backup custody stay in the
   OpenBao guide, policy and runbook.

## Consequences

Once accepted, this record supersedes ADR-0003 and ADR-0018, which then move
to the superseded archive; until then it is a proposal and both stay where
they are. The Vault-era
auto-unseal and remote-audit deferral recorded in ADR-0018 was never decided
and is not carried here; ADR-0042 owns the seal question. This record changes
no runtime behavior and claims no data migration, recovery or deployment result.

### Compliance

The documentation gates check the supersession links and metadata. Runtime
state needs separate execution evidence.

### Follow-up

Accept this record, then mark ADR-0003 and ADR-0018 superseded by it and
archive them. Any change of seal method or HA topology needs its own ADR.

## Related Documents

- [AD-0003](../descriptions/0003-security-architecture.md)
- [ADR-0003](0003-vault-as-secrets-manager.md)
- [ADR-0018](0018-vault-hardening-and-ha-expansion-strategy.md)
- [ADR-0042](0042-openbao-unseal-method.md)
- [OpenBao policy](../../05.operations/policies/04-security-and-secrets/0085-openbao.md)
