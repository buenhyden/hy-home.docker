---
title: "Keycloak and OIDC Operations Research"
version: "0.1.1"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0180-TSK-0003"
parent_ids:
- "SPEC-0180"
- "SPEC-0180-PLAN-0001"
created: "2026-09-19"
---

# Keycloak and OIDC Operations Research

## Objective

After the OpenBao/private-schema implementation, research Keycloak, OAuth2 Proxy,
OIDC and Keycloak-backed application OIDC using official sources, then explain
this repository's implementation in the existing architecture and operations
owners. The owner explicitly requested this follow-up. No runtime or credential
change is part of this documentation task.

## Inputs

- [Spec](../spec.md) and [Plan](../plan.md).
- [OpenBao/private-schema evidence](tsk-0002-openbao-access-and-env-convergence.md).
- Tracked auth, Traefik and application configuration; no private values.
- OpenID Foundation, IETF, Keycloak, OAuth2 Proxy and Traefik primary sources.

## Work Log

- Previous implementation committed as `a88af6e1d` and delivered in Draft
  [PR #168](https://github.com/buenhyden/hy-home.docker/pull/168). Readback confirmed
  the expected head, open/draft state and running required CI; no merge occurred.
- Separate product responsibilities from protocol concepts, and browser/Keycloak/
  proxy/application token states from each other. Trace each current behavior to
  source or earlier verified runtime evidence.
- Extend existing Keycloak and OAuth2 Proxy guide/runbook pairs and application
  integration guide. Reconcile the current auth architecture/policy with the
  owner-approved OpenBao native OIDC implementation.

## Verification Evidence

Official-source research is documented inline in GDE-0079 and the Keycloak/
OAuth2 Proxy guide/runbook pairs. Sources cover OIDC Core, OAuth security BCP,
RP-initiated logout, Keycloak hostname/proxy/health/OIDC endpoints, OAuth2 Proxy
provider/configuration/session/endpoints and Traefik ForwardAuth.

Metadata check selected 9 documents with zero violations. Link check passed
918 documents / 7,701 links. Markdown lint passed all 9 changed documents.
These are documentation checks; Compose and application behavior were not
changed or re-executed in this follow-up. Previous runtime acceptance applies only to its named OpenBao checks;
this documentation work does not establish all-application live readiness.

## Review Evidence

Independent review identified residual ForwardAuth topology text, an overbroad
file-secret statement and missing OpenBao verification coverage. All were
corrected, including the duplicated check heading and OpenBao purpose text.
Final independent specification and quality/security review passed without
findings across all nine documents. Live whole-stack acceptance remains unverified.

## Commit Ledger

Documentation is delivered as a separate reviewed commit on `codex/openbao-bootstrap-access`
and delivered through PR #168. Normal commits provide recovery; no merge,
force push or remote protection change is authorized.

## Rulings

Official documentation describes upstream capability, tracked config describes
declared behavior, and named acceptance evidence describes observed behavior.
Do not conflate them. Preserve service pins and all runtime/private state.

## Deferred Items

Closure (2026-09-24): whole-stack login/logout acceptance moves to [SPEC-0181](../../0181-home-residual-operations/spec.md) as the SSO route matrix. Client provisioning closed per service in later Tasks (Superset in Task 0008 S16) except Terrakube, which moves to SPEC-0181.

Whole-stack login/logout acceptance, missing client provisioning and any security
configuration remediation require their own scoped implementation and acceptance.
