---
name: "container-threat-modeling"
description: "Use when a container workload needs a read-only threat model of assets, trust boundaries, exploit paths, and owned mitigations."
metadata:
  title: "container-threat-modeling"
  version: "1.2.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-10-29"
  function_id: "container-threat-modeling"
  scope: "security"
  owner_agent: "security-auditor"
---

# container-threat-modeling

## Purpose

### Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

Workload boundaries, assets, actors, data flows, and deployment assumptions must be identified without reading secret payloads.

## Inputs

- Trust boundaries and workload definition.
- Compose/network/volume/secret metadata and exposed interfaces.

## Procedure

1. Map assets and data flows across host, container, network, storage, secret, and control-plane boundaries.
2. Enumerate plausible spoofing, tampering, disclosure, denial, and privilege-escalation paths tied to tracked configuration.
3. Rank mitigations by exploitability and impact, assign an owner, and identify residual risk requiring approval.

### Gates

- Every material asset and trust boundary is covered.
- Each accepted mitigation has a canonical implementation or policy owner.

## Outputs

- A container threat model with scoped threats, mitigations, owners, and residual risks.

## Verification

- Every asset and trust boundary in scope has at least one threat row or an explicit none-found row.
- Every accepted mitigation names its canonical implementation or policy owner.
- Residual risk that needs approval is listed with its owner.

## Failure Handling

Record unknown boundaries and stop any claim of completeness when configuration or authority evidence is missing.

## References

- [Security auditor](../../roles/security-auditor.md)
- [Security audit](../security-audit/SKILL.md)
- [Security scope](../../governance/quality-standards.md)
