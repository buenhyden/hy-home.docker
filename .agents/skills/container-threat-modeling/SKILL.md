---
name: "container-threat-modeling"
description: "Use when a container workload needs a read-only threat model of assets, trust boundaries, exploit paths, and owned mitigations."
metadata:
  title: "container-threat-modeling"
  version: "1.1.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-06"
  function_id: "container-threat-modeling"
  scope: "security"
  owner_agent: "security-auditor"
---

# container-threat-modeling

## Preconditions

Invoke this procedure explicitly. Invocation does not select a role or grant the
owning role's permissions. Use the already selected role's permission profile and
approved Task scope; route to the owner when incompatible.

Workload boundaries, assets, actors, data flows, and deployment assumptions must be identified without reading secret payloads.

## Inputs

- Trust boundaries and workload definition.
- Compose/network/volume/secret metadata and exposed interfaces.

## Procedure

1. Map assets and data flows across host, container, network, storage, secret, and control-plane boundaries.
2. Enumerate plausible spoofing, tampering, disclosure, denial, and privilege-escalation paths tied to tracked configuration.
3. Rank mitigations by exploitability and impact, assign an owner, and identify residual risk requiring approval.

## Outputs

- A container threat model with scoped threats, mitigations, owners, and residual risks.

## Gates

- Every material asset and trust boundary is covered.
- Each accepted mitigation has a canonical implementation or policy owner.

## Failure Handling

Record unknown boundaries and stop any claim of completeness when configuration or authority evidence is missing.

## Related Documents

- [Security auditor](../../roles/security-auditor.md)
- [Security audit](../security-audit/SKILL.md)
- [Security scope](../../governance/quality-standards.md)
