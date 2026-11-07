---
title: "ComfyUI Egress on Demand Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-08"
layer: "specs"
artifact_id: "SPEC-0268-TSK-0001"
parent_ids:
- "SPEC-0268-PLAN-0001"
created: "2026-11-08"
---

# ComfyUI Egress on Demand Task

## Overview

### Objective

Execute W1–W5 of the Plan: confirm ComfyUI needs no outbound access outside
maintenance, remove it from the default render, add the opt-in overlay, test,
document and, under separate approval, apply the change in HOME.

## Inputs and Authorization

On 2026-11-08 the owner reviewed ComfyUI's unrestricted outbound access,
recorded as open by SPEC-0266 and SPEC-0267, and chose egress off by default
with an opt-in overlay, over a domain-allowlist proxy and over an accepted
risk. The Spec and Plan are `draft`; no implementation starts until both are
approved. HOME recreation (W5) needs its own approval.

## Work Log

### Draft inputs (2026-11-08)

Read from `main` and the running HOME container:

| Item | Observation |
| --- | --- |
| Network | `comfyui_egress_net` (`10.250.42.0/24`, `ip_range .128/25`), non-internal, ComfyUI its only member (`docker-compose.yml:158-163`) |
| Image | `yanwk/comfyui-boot:cu126-slim`; command `bash /runner-scripts/entrypoint.sh`, which has no `git`, `curl` or `wget` call |
| Custom nodes | `ComfyUI-Manager` 3.41 only, plus the image's example files |
| ComfyUI-Manager | `/root/ComfyUI/user/__manager/config.ini`: `network_mode` not set (public default), `security_level = weak` |
| References | `docker-compose.yml`, `infra/08-ai/comfyui/docker-compose.yml`, `infra/08-ai/comfyui/README.md`, `tests/validation/test_p02_service_contracts.py`, GDE-0077, the m0021 inventory |

ComfyUI-Manager's start-up fetch of its node list is the one outbound call
still to be checked in W1; the `weak` security level is out of scope and
recorded for the owner.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | Draft source and container review | `main` `802e77f34`, HOME `comfyui` | NOT_RUN | Draft input only; the dependency table is W1 | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | Awaiting W1 | @buenhyden |
| 2 | pending | - | Awaiting W2 | @buenhyden |
| 3 | pending | - | Awaiting W2 | @buenhyden |
| 4 | pending | - | Awaiting W3 | @buenhyden |
| 5 | pending | - | Awaiting W4 | @buenhyden |
| 6 | pending | - | Awaiting W5 and its approval | @buenhyden |

## Review and Completion

Not started. The Spec and Plan are drafts.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [SPEC-0267 Task](../../0267-secondary-listener-hardening/tasks/tsk-0001-secondary-listener-hardening.md)
