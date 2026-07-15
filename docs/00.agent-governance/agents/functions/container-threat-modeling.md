---
layer: agentic
artifact_type: agent-function
function_id: container-threat-modeling
scope: security
status: active
---

# container-threat-modeling

## Preconditions

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

- [Security auditor](../agents/security-auditor.md)
- [Security audit](./security-audit.md)
- [Security scope](../../scopes/security.md)
