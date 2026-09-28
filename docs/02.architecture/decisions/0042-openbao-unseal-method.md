---
title: "OpenBao Unseal Method"
version: "0.2.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0042"
parent_ids:
- "AD-0003"
created: "2026-09-25"
---

# ADR-0042: OpenBao Unseal Method

## Context

OpenBao runs as a single-node Raft on the 2.6-series image pinned by
[Compose](../../../infra/03-security/openbao/docker-compose.yml). Compose's
`BAO_LOCAL_CONFIG` has no `seal` stanza, so it is the default Shamir seal. Per
RUN-0085, there are 3 shares with a threshold of 2. By owner decision
(2026-09-22), the three shares live together in one file,
`secrets/security/openbao_unseal_keys.txt` (SEC-003, `0600`, excluded from
Git, not mounted into the container). Anyone who can read this file can
unseal OpenBao. This file is also encrypted with BKP-002 inside the host
Restic repository.

Auto-unseal was only deferred as a non-goal in ADR-0018 from the Vault era
("actual KMS/HSM auto-unseal implementation at this stage"); it was never
decided.

The current sequence after a reboot or OpenBao restart is as follows.

1. OpenBao comes up sealed. The healthcheck treats sealed (`bao status` rc 2)
   as passing, so `openbao-agent` starts immediately.
2. The owner enters two shares via `bao operator unseal` in an interactive
   terminal.
3. The Agent reads the SecretID file and then deletes it
   (`remove_secret_id_file_after_reading = true`), so it cannot
   re-authenticate after a restart. The owner must log in via OIDC, issue a
   new SecretID (10 minutes, single use), and place it in the Agent volume
   (the RUN-0085 delivery procedure).
4. hy-home.k8s's External Secrets reads OpenBao via Kubernetes auth, so it
   cannot synchronize until unseal.

**Version check** (OpenBao official documentation 2.6.x, checked 2026-09-25):

- Seals built into the 2.6.x binary: AliCloud KMS, AWS KMS, Azure Key Vault,
  GCP Cloud KMS, KMIP, OCI KMS, OVHcloud KMS, PKCS#11, Static Key, T Cloud
  Public KMS, OpenBao Transit.
- From v2.6.0, methods not built in can be installed as external KMS plugins.
  From v2.7.0, many built-in methods are removed from the standalone binary
  and offered only as plugins. So upgrading to 2.7 may require plugin
  registration for a cloud KMS or PKCS#11 seal.
- PKCS#11 needs an HSM build compiled with cgo, or a plugin from
  openbao-plugins, even on 2.6.x. The documentation does not state whether the
  official image is an HSM build.
- The Static Key seal takes a 32-byte AES-256-GCM key via config, `env://`, or
  `file://`. The documentation recommends it "only when a source of trust
  already exists (for example, another third-party secrets manager)."
- The Transit seal requires the transit server to be reachable at start and
  unseal time, and recommends a periodic orphan token.

## Decision Drivers

- Whether the service must come back without the owner after a reboot
  (currently both unseal and SecretID need the owner).
- If unseal material is in the same place as the host, auto-unseal is only a
  convenience, not a security boundary.
- New external dependencies (cloud account, another device) must not block
  the recovery path.
- Seal transition is hard to reverse. Moving from Shamir to auto-unseal turns
  shares into recovery keys instead of unseal keys, unusable for unsealing.
- The effect on the W11 cold start runbook and the Agent SecretID delivery
  method.

## Options Considered

| Option | Unattended reboot | Key location | New dependency | W11 impact |
| --- | --- | --- | --- | --- |
| (a) Keep manual Shamir | No | Host file SEC-003 (current) | None | Owner performs the unseal step |
| (b) Transit from another OpenBao/Vault | Yes (if the transit server is alive) | Transit key on another device | Second server and network | Order requires booting the transit server first |
| (c) Cloud KMS (AWS/GCP/Azure, etc.) | Yes (if internet and KMS are available) | Cloud KMS | Cloud account, egress | Cannot start without internet |
| (d) Static Key or PKCS#11 (same host) | Yes | Host file or SoftHSM | None (Static) or HSM build/plugin | Unseal step disappears |
| (e) Defer (record owner and trigger) | No | Current | None | Same as (a) |

### (a) Keep manual Shamir unseal (current)

- **Good**: No change. The seal key is not in container config or
  environment. No external dependency.
- **Bad**: The owner is needed at every reboot and OpenBao restart. Since all
  three shares are in one file, the benefit of split custody is already lost.
- **Agent SecretID**: No change. The owner also delivers the SecretID at every
  reboot.

### (b) Transit auto-unseal from a second OpenBao/Vault

- **Method**: Keep a transit engine and key on another instance, and give
  this server's `seal "transit"` the address, key name, and a periodic orphan
  token.
- **Where to run it**: Running it on the same host defeats the purpose; the
  transit server itself needs unsealing, and an attacker with the host has
  both. It must be on another device (NAS, another PC, a small VPS).
  hy-home.k8s does not qualify because it is a container on the same host.
- **Good**: Unattended reboot without a cloud account. The key is outside this
  host.
- **Bad**: The second server has its own unseal problem too (usually manual
  Shamir). If that server is down, this server cannot start. Token
  management, TLS, and a network path are newly needed.
- **Agent SecretID**: No change.

### (c) Cloud KMS auto-unseal

- **Method**: `awskms`, `gcpckms`, `azurekeyvault`, etc., built into the
  current 2.6 series. Credentials are supplied via environment variables or a
  file (the documentation strongly recommends environment variables over
  configuration files).
- **Good**: The key is outside the host (in the KMS) and KMS audit logs
  remain. Cost is around $1/month (list-price estimate) for one key and few
  calls. Cutting off KMS access on host theft prevents data from being
  opened.
- **Bad**: OpenBao cannot start if the internet or KMS is unavailable (a home
  lab line outage becomes a secret-store outage). Since the KMS access key is
  on the host, anyone who took over the host can also unseal while the host
  is alive. This may change with plugin registration after v2.7.0. Needs new
  cloud credentials (a new SEC row) and egress on the OpenBao container.
- **Agent SecretID**: No change.

### (d) Static Key or PKCS#11 seal (same host)

- **Method**: Give `seal "static"` a 32-byte key via `file://` and mount that
  file as a Docker Secret. PKCS#11 keeps the key in a software token like
  SoftHSM but needs an HSM build or a plugin.
- **Security trade-off**: Since the key is on the same host, anyone who has
  the host or the OpenBao container can unseal. The same is already possible
  today with the single SEC-003 file, so **protection against host takeover
  does not meaningfully change**. Two things do change: the key is mounted
  into the container and could be exposed without a container escape, and if
  the Raft snapshot and key end up in the same backup, whoever takes only the
  snapshot can also open it. SoftHSM is no better than Static Key since its
  key file is also on disk. The official documentation recommends Static Key
  only when an existing source of trust is present.
- **Good**: Unattended reboot with no external dependency.
- **Bad**: Seal protection effectively reduces to file permissions. Requires
  a seal transition (`-migrate`) and a recovery key scheme change.
- **Agent SecretID**: No change.

### (e) Defer (record owner and trigger)

Keep (a) while recording an owner and review trigger per criterion 10.
Candidate triggers:

- An unplanned reboot or power outage leaves OpenBao sealed for over 24 hours
  while the owner is unavailable.
- hy-home.k8s or another service comes to require OpenBao immediately after
  boot.
- ADR-0041 selects a cloud provider (creating grounds to review KMS on the
  same account).
- OpenBao 2.7 upgrade (when the seal method shifts to a plugin).

## Decision

**(e) Defer, keep (a) manual Shamir unseal** (owner decision, 2026-09-25). The
owner is @buenhyden. Whichever of the following triggers comes first opens a
new ADR that supersedes this decision.

- An unplanned reboot or power outage leaves OpenBao sealed for over 24 hours
  while the owner is unavailable.
- hy-home.k8s or another service comes to require OpenBao immediately after
  boot.
- ADR-0041 selects a cloud provider (Cloudflare R2 was chosen, but R2 has no
  KMS, so this trigger fires when a provider that offers a KMS is chosen).
- OpenBao 2.7 upgrade (when the seal method shifts to a plugin).

Rationale:

- Auto-unseal alone does not give an unattended reboot. The Agent needs a
  single-use SecretID issued by the owner at every restart, so the owner is
  already part of the reboot procedure regardless.
- A same-host key (d) widens the key-exposure surface with no security gain.
  Another device (b) or cloud (c) creates a new availability dependency. At
  the current scale, this cost outweighs the benefit.

## Consequences

- **W11 cold start runbook**:
  - (a)/(e): The order is OpenBao start -> owner unseal (2 shares, hidden
    input) -> OIDC login -> SecretID issuance and delivery to the Agent ->
    Agent authentication check -> hy-home.k8s External Secrets sync check.
    Owner time is recorded at the unseal and SecretID steps.
  - (b)/(c)/(d): The unseal step becomes automatic, but the SecretID delivery
    step remains. (b) requires booting the transit server first; (c) requires
    checking internet and KMS availability as a runbook precondition.
- **Agent SecretID**: Single-use SecretID delivery remains under every
  option. Removing it needs a separate decision to extend SecretID lifetime
  or count, or to use a different auth method, and that is out of this ADR's
  scope.
- **On seal transition**: Shares become recovery keys. RUN-0085's
  generate-root and break-glass procedures, the SEC-003 description, the
  POL-0021 OpenBao row, and a new SEC row (key or KMS credential) all need to
  be updated together. A protected Raft snapshot and an isolated recovery
  rehearsal are needed before the transition.

## Traceability

- Parent: [AD-0003 Security Architecture](../descriptions/0003-security-architecture.md)
- Earlier deferral: [ADR-0018](0018-vault-hardening-and-ha-expansion-strategy.md)
- Spec: [SPEC-0182](../../03.specs/0182-home-residual-backlog/spec.md) criterion 10 and 11,
  Plan W10/W11,
  [Task 0003](../../03.specs/0182-home-residual-backlog/tasks/tsk-0003-recovery-and-auth-acceptance.md)
- Runbook: [RUN-0085](../../05.operations/runbooks/0085-openbao.md)
- Runtime sources: [OpenBao Compose](../../../infra/03-security/openbao/docker-compose.yml),
  [Agent configuration](../../../infra/03-security/openbao/config/agent.hcl)

## Follow-up

- The W11 runbook records the unseal method actually in use at decision time.
- If deferred, record the owner and trigger in Task 0003's Deferred Items.

### Official references

- [OpenBao seal configuration (2.6.x)](https://openbao.org/docs/2.6.x/configuration/seal/)
- [Static Key seal](https://openbao.org/docs/configuration/seal/static/)
- [Transit seal](https://openbao.org/docs/configuration/seal/transit/)
- [PKCS#11 seal (2.6.x)](https://openbao.org/docs/2.6.x/configuration/seal/pkcs11/)
- [AWS KMS seal](https://openbao.org/docs/configuration/seal/awskms/)
