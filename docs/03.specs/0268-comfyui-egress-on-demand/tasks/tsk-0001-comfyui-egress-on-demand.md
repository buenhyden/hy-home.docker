---
title: "ComfyUI Egress on Demand Task"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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

### Approval and start (2026-11-08)

The owner approved the SPEC-0268 Spec and Plan on 2026-11-08 after the draft
merged in #796. W1 then found that the default render would also lose the
loopback port, and the owner chose to move the port into the overlay. Spec
and Plan 0.2.0 record that decision and place the attach and detach steps in
RUN-0081, because the README routes commands to the operations documents. W5
(HOME) keeps its own approval.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0268 | draft | approved | #approval-and-start-2026-11-08 |
| SPEC-0268-PLAN-0001 | draft | approved | #approval-and-start-2026-11-08 |
| SPEC-0268-TSK-0001 | draft | ready | #approval-and-start-2026-11-08 |
| SPEC-0268-TSK-0001 | ready | in-progress | #approval-and-start-2026-11-08 |
| SPEC-0268-TSK-0001 | in-progress | completed | #owner-acceptance-2026-11-08 |

### W1 outbound dependencies (2026-11-08)

Read in the running `comfyui` container (ComfyUI-Manager 3.41, image
`yanwk/comfyui-boot:cu126-slim` created 2026-09-14):

| Dependency | When | Source | Needed without maintenance? |
| --- | --- | --- | --- |
| Image entrypoint | Start | `/runner-scripts/entrypoint.sh`: copies the bundled ComfyUI only when `/root/ComfyUI/main.py` is absent; no download | No |
| ComfyUI frontend package | Start | `app/frontend_management.py:233-249` exits only when `comfyui_frontend_package` cannot be imported; the image ships 1.51.10, the version `/root/ComfyUI/requirements.txt` pins | No |
| GitHub frontend release fetch | Start | `app/frontend_management.py:136-192`, used only for `--front-end-version`, which `COMFYUI_ARGS` does not set | No |
| Manager dependencies | Start | `prestartup_script.py:455-478` installs only when `git`, `toml`, `rich` or `chardet` cannot be imported | No |
| Manager pip fixer | Start | `glob/manager_util.py:466-490` reinstalls the frontend package when its package scan misses it; the 2026-11-08 start logged a false miss (`PyTorch is not installed` while torch 2.14.0 is present) and a `fixed` result for a version already installed | No; a failed reinstall is logged and start continues |
| Manager node and model lists | Start, background thread | `glob/manager_server.py:2075-2091`: fetches five lists from `raw.githubusercontent.com` unless `network_mode = offline`; errors are logged | No; the Manager's list view stays on cached files |
| Model, custom-node and package installs | Maintenance | ComfyUI-Manager | Yes; this is the overlay window |
| Workflow execution | Run time | Core nodes load local files under `/root/ComfyUI/models` | No |

`PIP_USER=true` (`entrypoint.sh:53-56`) sends packages installed during
maintenance to `/root/.local`, in the `/root` volume, so they survive a
recreate. Packages already in the image stay in `/usr/local`.

### W2–W4 implementation (2026-11-08)

W3 came first: `test_comfyui_has_no_outbound_access_or_host_port_by_default`
and `test_comfyui_egress_overlay_adds_only_egress_and_loopback_port` replace
`test_comfyui_keeps_outbound_access_without_peers` in
`SsoOnlyIngressContractTests`, which now renders through
`_render_all_profiles(*overlays)`. Both failed on `main`; the other 35 tests
in the module passed. W2 removed `comfyui_egress_net` and the port from
`infra/08-ai/comfyui/docker-compose.yml` and added the overlay. A root-base
overlay may add only new internal networks and no ports (POL-0078), and the
first draft with `base: docker-compose.yml` failed 12 Compose gate tests on
`overlay networks must be a nonempty mapping`; the overlay uses the leaf base
`infra/08-ai/comfyui/docker-compose.yml`, like the `monitor-acl` overlays.
W4 updated RUN-0081 (in-container health check, attach and detach), the
ComfyUI README, GDE-0077 and the m0021 inventory. The related-suite run then
found `COMFYUI_HOST_PORT` orphaned in `.env.example`
(`test_public_environment_has_current_consumers_and_four_way_classification`,
which passes on `main`), because the public environment scan reads only the
root Compose includes. The overlay now publishes `127.0.0.1:8188` and the key
is removed.

### W5 HOME apply (2026-11-08)

The owner approved W5 on 2026-11-08 after #799 merged. The live tree was
fast-forwarded to `1861caae2` with no local changes. Before the change
(`~/storage/backups/spec0268-w5-20261108/pre-state.txt`): `comfyui` on
`comfyui_egress_net` (`10.250.42.129`) and `comfyui_ingress_net`, port
`127.0.0.1:8188` published, `https://raw.githubusercontent.com` answering
200 from inside the container, and 75, 182, 3, 2 and 18 entries in `models`,
`custom_nodes`, `input`, `output` and `user`. A `--dry-run` recreated only
`comfyui` and created no network or volume. ComfyUI's data sits on bind
volumes that the change does not touch, so no backup copy was taken.

| Step (UTC) | Command | Observation |
| --- | --- | --- |
| Default, 22:19:22–22:21:21 | `up -d --no-deps --force-recreate comfyui` | `healthy`; networks `comfyui_ingress_net` only; port `8188/tcp` unpublished; `raw.githubusercontent.com` and `pypi.org` fail with `URLError`, `1.1.1.1:443` with `OSError`; RUN-0081 in-container check OK; host `127.0.0.1:8188` refused; SSO route 302 to the Keycloak realm; data counts unchanged |
| Start-up log | `docker logs comfyui` | ComfyUI-Manager logs `Failed to perform initial fetching` on DNS and continues; frontend 1.51.10 served; `Starting server`. The Manager's `comfyui-frontend-package ... fixed` line appears offline as well, so its pip step needs no network |
| Attach, 22:21:44–22:22:25 | RUN-0081 attach with `docker-compose.egress.yml` | `healthy`; networks `comfyui_egress_net` and `comfyui_ingress_net`; `127.0.0.1:8188` published; outbound 200; host `/system_stats` 200 |
| Detach, 22:22:32–22:23:11 | RUN-0081 detach | `healthy`; `comfyui_ingress_net` only; port unpublished; outbound blocked; route 302; data counts unchanged; `comfyui_egress_net` has 0 members |

A workflow run with a local model was not part of criterion 6 and was not
run.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | W1 | Draft source and container review | `main` `802e77f34`, HOME `comfyui` | NOT_RUN | Draft input only; the dependency table is W1 | optional | - |
| E2 | 1 | W1 | Source read of start-up and run-time outbound calls | HOME `comfyui`, ComfyUI-Manager 3.41 | PASS | "W1 outbound dependencies" table | required | - |
| E3 | 4 | W3 | ComfyUI default and overlay render tests before and after W2 | `main` `279d23d39` then this branch | PASS | 2 failures before W2; `test_p02_service_contracts` 37 tests OK after | required | - |
| E4 | 2, 3 | W2 | `validate-docker-compose.sh`, `check-all-hardening.sh`, Compose gate suites | This branch | PASS | 65 selections valid; all hardening tiers pass; `test_compose_baseline_gates`, `test_p02_service_contracts` and `PublicSecretSchemaTests` 200 tests OK, 31 opt-in skips; the other failures in the eleven related suites also fail on `main` | required | - |
| E5 | 5 | W4 | Operations catalog, metadata and link checks | This branch | PASS | `check-operations-catalog.py` PASS after the m0021 re-render | required | - |
| E6 | 6 | W5 | HOME recreate on the default render, refusal, route, data, and attach and detach rehearsal | `1861caae2`, HOME | PASS | "W5 HOME apply" table | required | - |
| E7 | 6 | W5 | Workflow run with a local model | HOME | NOT_RUN | Not part of criterion 6 | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | E2 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 2 | accepted | E4 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 3 | accepted | E4 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 4 | accepted | E3 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 5 | accepted | E5 | Accepted by the owner on 2026-11-08 | @buenhyden |
| 6 | accepted | E6 | Accepted by the owner on 2026-11-08 | @buenhyden |

## Review and Completion

W1–W5 are done and every criterion has PASS evidence.

### Owner acceptance (2026-11-08)

The owner accepted criteria 1–6 on 2026-11-08 after the W5 evidence merged
(#800), and the Task closed as `completed`. ComfyUI runs without outbound
access or a host port; RUN-0081 owns the maintenance attach and detach.
ComfyUI-Manager's `security_level = weak` stays outside this Task.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [SPEC-0267 Task](../../0267-secondary-listener-hardening/tasks/tsk-0001-secondary-listener-hardening.md)
