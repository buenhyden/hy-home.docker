---
status: active
artifact_id: task:2026-07-19-compose-runtime-readiness-remediation
artifact_type: task
parent_ids:
  - spec:124-compose-runtime-readiness-remediation
  - plan:2026-07-11-compose-runtime-readiness-remediation
---

# Task: Compose Runtime Readiness Remediation

## Overview

This active Task records implementation and execution evidence for the
exact local-isolated `core` service set: `keycloak`, `oauth2-proxy`, `traefik`,
`vault`, and `vault-agent`. At activation, no service has been started and no
readiness, recovery, timeout, or cleanup result is claimed.

The Task owns the concise
`_workspace/repo-support/task-2026-07-19-compose-runtime-readiness-remediation/compose/readiness-verdict.json`
ready handoff plus `readiness-verdict.startup-readiness.json`,
`readiness-verdict.vault-restart-recovery.json`, and
`readiness-verdict.negative-timeout.json` scenario evidence. Raw logs and
synthetic secret bodies are not evidence consumers.

## Inputs

- [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- [Compose runtime readiness Plan](../plans/2026-07-11-compose-runtime-readiness-remediation.md)
- [Program Plan](../plans/2026-07-19-operational-readiness-closure-program.md)
- Root `docker-compose.yml` and the approved task-only override
- Static Compose validation and profile/service inventory

## Goals and Non-goals

Goals:

- prove startup and initialization for only the exact five services;
- observe container and service-specific endpoint readiness;
- prove a bounded Vault restart recovery and a stable timeout stop path;
- verify cleanup of only the wrapper-created project and task-owned paths;
- emit a redacted, typed readiness verdict for the delivery Task.

Non-goals:

- production/shared-host readiness, default-profile expansion, or any sixth
  service;
- use of external `mng-pg`, `mng-valkey`, `k3d-hyhome`, host ports 80/443, or
  repository data-volume paths;
- data restore, registry access, remote observability, deployment, or secret
  value inspection.

## Scope and Change Boundaries

Allowed authored paths:

- `scripts/validation/run-compose-core-readiness.sh`;
- `scripts/validation/compose-core-readiness.lib.sh`;
- `tests/fixtures/compose-core-readiness/**`;
- `tests/validation/test_compose_core_readiness.py`;
- this Task and directly supported lifecycle/index evidence during closure.

Allowed transient path: only
`_workspace/repo-support/task-2026-07-19-compose-runtime-readiness-remediation/`.
Synthetic secret files and raw diagnostics stay under `/tmp` or task-owned
ignored storage and their bodies are never promoted.

Forbidden paths/actions: shared Docker resources, fixed or nonmatching project
names, external networks/databases/session stores, broad cleanup, root
repository data mounts, live secrets, remote targets, and deployment.

Compose impact: a test-only override may change the rendered local model. The
root production render remains unchanged. The override publishes only loopback
ports `18000`, `18443`, `18082`, `18083`, and `18200`.

Target host class: a local Docker Engine reached from this linked Git worktree,
with a pre-run minimum of 4 logical CPUs, 4 GiB available memory, and 8 GiB
available storage. Remote engines, shared CI runners, and production hosts are
not approved.

Resource limits: `keycloak=1.00 CPU/768 MiB`;
`oauth2-proxy=0.50 CPU/256 MiB`; `traefik=0.50 CPU/256 MiB`;
`vault=0.50 CPU/256 MiB`; `vault-agent=0.25 CPU/128 MiB`. The aggregate
approved ceiling is 2.75 CPUs and 1,664 MiB. The startup timeout is 180 seconds,
the recovery timeout is 120 seconds, and teardown uses `docker compose down
--volumes --remove-orphans --timeout 15` only after exact ownership checks.

Security impact: synthetic local credentials, a file-provider-only Traefik
configuration with no raw Docker socket mount, no secret-body evidence, and
fail-closed project ownership checks.

Operations impact: local startup/readiness/recovery observation only. Stateful
restore or ambiguous teardown stops and escalates.

Runtime impact: the wrapper creates one project named
`hyhome-crr-20260719-<decimal-pid>-<eight-lowercase-alphanumeric-token>` from
`mktemp -d` entropy plus atomic `mkdir`, starts only the exact service set, and
removes only resources matching its owned project identity.

## Approval Evidence

Approval source:

- The user approved protected-surface changes and implementation of the local
  operational-readiness program.
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md),
  [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md),
  and the active Plan define the accepted isolated topology and exact commands.

Protected surfaces: local Docker runtime, test-only Compose override, synthetic
secret files, high loopback ports, validation scripts, tests, and concise
runtime evidence are authorized. Shared/production runtime, live state,
credential values, remote targets, and broad cleanup are not authorized.

Approval boundary: the only runtime command forms are `--preflight`,
`--scenario startup-readiness`, `--scenario vault-restart-recovery`,
`--scenario negative-timeout`, and owned `--cleanup-only --project-name` with
project regex `^hyhome-crr-20260719-[0-9]+-[a-z0-9]{8}$`. Any changed
service, resource limit, port, network, path, target, or failure injection
requires stop and new approval.

Rollback or recovery: the wrapper trap and explicit cleanup may remove only
the matching project and task-owned paths. Revert the one logical harness
commit to remove authored changes. If ownership or state is ambiguous, stop,
preserve concise non-secret evidence, and do not prune or delete resources.

Redaction boundary: record service states, endpoint verdicts, elapsed time,
stable exit class, cleanup, and redaction result. Never record synthetic secret
bodies, raw environment, raw logs, tokens, credentials, response bodies, or
private endpoint payloads.

## Work Breakdown

| Task ID | Description | Parent requirement | Validation / evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| `T-CRR-001` | Wrapper, override, synthetic environment, and verdict contract | `CRR-001`–`CRR-003` | Focused RED/GREEN tests and preflight | Fresh implementation agent | Done; current focused suite 42/42 |
| `T-CRR-002` | Exact five-service startup and endpoint readiness | `CRR-001`, `CRR-002` | Startup/readiness scenario and typed verdict | Fresh implementation agent | Done (runtime) |
| `T-CRR-003` | Vault restart, timeout, and cleanup ambiguity | `CRR-003` | Recovery and expected non-zero timeout scenarios | Fresh implementation agent | Done (runtime) |
| `T-CRR-004` | Independent specification and quality/security review | `VAL-CRR-001`–`004` | C0/I0/M0 re-review | Separate reviewers | Current terminal reviews approved C0/I0/M0; Task lifecycle remains active under Program closure |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-19 | Task activation | Contract recorded; no Compose command or service runtime executed. |
| 2026-07-19 | `T-CRR-001` RED | The inherited wrapper's `--preflight` exited `10`: `assert_docker_compose` called `docker info`, which failed with `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`. This incorrectly coupled a no-start render gate to daemon access. |
| 2026-07-19 | `T-CRR-001` GREEN | Split daemon availability into `assert_docker_daemon`; the CLI/dependency assertion and model render remain daemon-independent, while cleanup-only and all runtime scenarios still require daemon access before any mutation. Focused tests pass `8/8`. |
| 2026-07-19 | Static Compose and preflight | Root static validation passed with `services_total=5`. Wrapper preflight exited `0`, emitted the exact service and loopback-port sets, and removed its owned `/tmp/hyhome-crr-20260719-138` path. |
| 2026-07-19 | `T-CRR-002`–`T-CRR-003` runtime boundary | `not_run`: `timeout 10s docker info` exited `1` because the sandbox cannot access `/var/run/docker.sock`. No service startup, Vault restart, failure injection, Compose teardown, runtime cleanup claim, or readiness verdict occurred. |
| 2026-07-19 | `T-CRR-002` startup attempt | After approved daemon access was provided, `bash scripts/validation/run-compose-core-readiness.sh --scenario startup-readiness` exited class `20` after Vault health timed out. The scoped trap cleanup succeeded and no task-owned container remained; no readiness verdict was produced. |
| 2026-07-19 | Vault command RED/GREEN | Read-only image metadata showed `hashicorp/vault:2.0.3` uses `docker-entrypoint.sh` with image command `server -dev`. The override incorrectly supplied `vault server ...` and `vault agent ...`, causing a double `vault` invocation. New regression `test_vault_commands_respect_image_entrypoint` failed `1/1`; removing the leading `vault` from both commands then passed the full focused suite `9/9`. Runtime was not rerun after this fix. |
| 2026-07-19 | `T-CRR-002` second startup attempt | The approved post-command-fix startup again exited class `20`; scoped cleanup passed and no task-owned container remained. A bounded state probe observed Vault `status=exited`, `exit=1`, `health=unhealthy`, and an empty `State.Error`; no secret body or raw log was promoted. |
| 2026-07-19 | Runtime material permission RED/GREEN | Image metadata identifies the Vault runtime user as `vault`, while the inherited helper made bind-mounted config and secret source files `0600`. New mode-only regression `test_runtime_material_permissions_allow_non_root_consumers` failed `1/1`. Container-consumed secret sources became `0444`, non-secret HCL config files became `0644`, and runtime/config/secret parent directories remained `0700`; focused tests passed `10/10`. At this point unseal/root-token files remained host-only `0600`; the later mounted-secret correction supersedes that mode without weakening the `0700` parent boundary. |
| 2026-07-19 | `T-CRR-002` third startup attempt | The approved post-permission-fix startup again exited class `20`; bounded direct diagnostics completed and scoped cleanup passed with no task-owned container left. The permission change remains a valid non-root file contract but did not close startup. |
| 2026-07-19 | Vault server Entrypoint RED/GREEN | Direct diagnostics established the definitive third-attempt cause: the image entrypoint special-cases `server` and prepends `vault server -config=/vault/config`. The override also passed `-config=/vault/config/vault-readiness.hcl`, loading the same HCL through both the directory and file and producing duplicate listener `0.0.0.0:8200 address already in use`. A bounded direct `--entrypoint vault ... -config=file` probe started successfully, proving the HCL is valid. New regression `test_vault_server_loads_entrypoint_config_directory_once` failed `1/1`; the Vault server command is now exactly `[server]`, while Vault Agent remains `agent -config=file`. Focused tests passed `11/11`; the subsequent fourth attempt proved Vault startup and initialization before exposing the unseal transport defect. |
| 2026-07-19 | `T-CRR-002` fourth startup attempt | The approved single-load startup successfully started and initialized Vault, then exited class `20` when unseal failed; scoped cleanup passed and left no task-owned container. Bounded diagnostics showed Vault 2.0.3 rejects piped stdin without a TTY (`file descriptor 0 is not a terminal`) and recommends a positional key, which would expose secret material in host process arguments if invoked directly. |
| 2026-07-19 | Vault mounted-secret RED/GREEN | New regression `test_vault_sensitive_commands_use_mounted_secret_flow` failed `1/1`. Empty unseal-key and root-token source files now exist before Compose render and are mounted only into the task Vault container. After initialization, the wrapper writes them under the `0700` runtime parent, sets source files `0444` for container reads, and uses fixed in-container shells to read them. Unseal passes the key positionally only inside the container; authenticated Vault commands export the root token only inside that shell. Host argv, host `-e VAULT_TOKEN`, logs, verdicts, and tracked files never receive either value. Focused tests pass `12/12`; no post-fix runtime startup ran. |
| 2026-07-19 | `T-CRR-002` fifth startup attempt | The approved mounted-secret startup progressed to OAuth2 Proxy, then failed because v7.15.3 reported `cookie_secret from file must be 16, 24, or 32 bytes ... but is 45 bytes`. Scoped cleanup was verified: no task-owned container, network, or volume remained. No secret body was printed, retained, or promoted. |
| 2026-07-19 | OAuth2 Proxy cookie-secret RED/GREEN | New size-only regression `test_oauth_cookie_secret_has_supported_byte_length` failed with expected `32` versus actual `45` without reading or displaying the secret body. Replaced base64-plus-newline generation with newline-free `openssl rand -hex 16`, producing exactly 32 ASCII bytes accepted by the documented runtime constraint. Focused tests passed `13/13`; the subsequent sixth attempt advanced beyond this validation and exposed the missing issuer setting. |
| 2026-07-19 | `T-CRR-002` sixth startup attempt | The approved 32-byte-cookie startup reached OAuth2 Proxy, which exited with exact non-secret cause `invalid provider verifier options: missing required setting: issuer-url`. Root cleanup checks for runtime project `hyhome-crr-20260719-1357499` and diagnostic project `hyhome-crr-20260719-299992` returned empty container, network, and volume sets; cleanup verification passed. |
| 2026-07-19 | OAuth2 Proxy issuer RED/GREEN | New static regression `test_oauth_manual_endpoints_include_internal_issuer` failed `1/1`. The test requires `--oidc-issuer-url=http://keycloak:8080/realms/master` alongside `--skip-oidc-discovery=true` and the explicit login, redeem, and JWKS endpoints. Added only the missing internal issuer argument; focused tests passed `14/14`. The subsequent seventh attempt proved OAuth health before exposing Traefik readiness and publishing defects. |
| 2026-07-19 | `T-CRR-002` seventh startup attempt | The approved issuer-corrected startup reached healthy OAuth2 Proxy, then Traefik remained unhealthy. Bounded diagnostics showed the process listening internally on `8000`, `8082`, and `8443`; health repeatedly failed with `Head "http://:8080/ping": ... connection refused` because `traefik healthcheck` used its default `:8080` while the configured ping entrypoint was `:8082`. Rendered HostConfig retained the loopback mappings, but Docker Engine 29 did not activate NetworkSettings published ports while the task bridge used `internal: true`, so host endpoint probes failed. Root's global owner-label cleanup check returned empty container, network, and volume sets across all runtime and diagnostic projects; cleanup verification passed. |
| 2026-07-19 | Task bridge and Traefik ping RED/GREEN | Regressions `test_task_bridge_is_dedicated_and_publish_capable` and `test_traefik_healthcheck_ping_matches_published_target` failed `2/2`. The dedicated `crr_net` remains a user-defined, non-external bridge but is now NAT/publish capable with `internal: false`. Traefik ping now listens on default healthcheck target `8080`, and loopback port `18082` maps to container `8080`; the exact published host-port allowlist is unchanged. Focused tests passed `16/16`. The bridge decision follows the official Docker bridge behavior documented at <https://docs.docker.com/engine/network/drivers/bridge/>. The subsequent eighth attempt proved service health and loopback publishing before exposing the Vault Agent output-volume owner mismatch. |
| 2026-07-19 | `T-CRR-002` eighth startup attempt | The approved bridge/ping-corrected startup reached healthy Vault, Keycloak, OAuth2 Proxy, and Traefik, then Vault Agent remained unhealthy. Isolated diagnostics showed successful AppRole authentication followed by `failed writing file: open /vault/out/<random>: permission denied`; image metadata kept the long-running container as user `vault`, while the task-owned named volume root was not writable. Root's global owner-label cleanup check returned empty container, network, and volume sets after runtime and diagnostic execution; cleanup verification passed. |
| 2026-07-19 | Vault Agent output volume RED/GREEN | Regressions `test_vault_agent_output_volume_preparation_is_scoped` and `test_vault_agent_output_preparation_order_and_identity` failed before the helper existed. Added `prepare_vault_agent_output_volume` after Vault configuration and before remaining-service startup. Its first implementation ran one task-scoped `crr_compose run --rm --no-deps --user 0:0 --cap-add CHOWN --entrypoint sh vault-agent -ec 'chown vault:vault /vault/out && chmod 0750 /vault/out'`, suppressed output, and mapped failure to startup class `20`. The long-running Vault Agent stayed on pinned image user `vault`; no service-level root user or world-writable mode was introduced. Focused tests passed `18/18`; the subsequent ninth attempt exposed the minimal-capability operation order defect. |
| 2026-07-19 | `T-CRR-002` ninth startup attempt | The approved output-volume-preparation startup failed before long-running services with class `20`. Isolated one-shot diagnostics returned `chmod: /vault/out: Operation not permitted`: with dropped capabilities plus only `CHOWN`, the initial `chown` transferred directory ownership away from root, which then lacked `FOWNER` for the following `chmod`. No capability expansion was accepted. |
| 2026-07-19 | Cleanup-only idempotency recovery | The failed preparation left the exact synthetic secret source files at container-readable `0444`; cleanup-only regeneration then failed with `Permission denied`. Root restored writable modes only on the exact task files, reran the wrapper's scoped cleanup-only path successfully, confirmed the task `/tmp` path absent, and confirmed the global owner-label container/network/volume sets empty. Cleanup verification passed without broad chmod or prune. |
| 2026-07-19 | Operation order and secret regeneration RED/GREEN | Regressions `test_vault_agent_output_mode_is_set_before_chown` and `test_synthetic_secret_preparation_is_exact_and_idempotent` failed `2/2`. The one-shot now performs `chmod 0750 /vault/out && chown vault:vault /vault/out`, preserving the CHOWN-only capability set. Secret preparation removes and recreates only its exact seven task-owned source files before generation, remains under the `0700` owned parent, and preserves unrelated files; no wildcard chmod/delete was added. Focused tests passed `20/20`; the subsequent tenth startup completed successfully. |
| 2026-07-19 | `T-CRR-002` tenth startup success (superseded contract) | Project `hyhome-crr-20260719-1558838` completed startup-readiness under the then-current PID-only identity and nine-key evidence schema. The result remains historical diagnostic evidence but was superseded by the reviewed collision-resistant identity and schema-v2 contract below; it is not current acceptance evidence. |
| 2026-07-19 | `T-CRR-003` restart-recovery attempt | Project `hyhome-crr-20260719-1570983` reached initial all-healthy state, stopped/restarted and unsealed Vault, then exited class `40` with non-secret message `endpoint recovery verification failed`. Root's global owner-label cleanup check returned empty container, network, and volume sets; cleanup verification passed. Diagnostics showed the running Vault Agent's previous health could be accepted after its sentinel was deleted while the Agent stayed running, without deterministic fresh template rendering. |
| 2026-07-19 | Fresh Vault Agent recovery RED/GREEN | Regressions `test_vault_recovery_requires_fresh_agent_sentinel_sequence` and `test_vault_recovery_steps_fail_closed_as_class_40` failed against the stale-health sequence. Recovery now stops Vault Agent first, removes the sentinel through task-owned `crr_compose run --rm --no-deps --entrypoint sh vault-agent -ec 'rm -f /vault/out/readiness.sentinel'` as image user `vault`, restarts and unseals Vault, then starts Vault Agent and waits for a newly rendered sentinel. All eight steps fail closed as class `40` with non-secret messages. Focused tests pass `22/22`; the subsequent post-fix recovery run passed. |
| 2026-07-19 | `T-CRR-003` post-fix restart-recovery success (superseded contract) | Project `hyhome-crr-20260719-1585299` passed restart recovery under the then-current PID-only identity and nine-key evidence schema. It is retained as historical diagnostic evidence and superseded by the schema-v2 rerun below. |
| 2026-07-19 | `T-CRR-003` negative-timeout expected pass (superseded contract) | Project `hyhome-crr-20260719-1592041` passed the expected timeout path under the then-current PID-only identity and alternate handoff. It is retained as historical diagnostic evidence and superseded by the canonical schema-v2 rerun below. |
| 2026-07-19 | Independent review findings | Specification review returned `C0/I3/M0`: missing traceability fields, collapsed endpoint classification, and omitted host/resource limits. Quality/security review returned `C3/I2/M0`: stopped-container ownership gap, cleanup failure masking, stale negative handoff, predictable/incompletely guarded paths, and over-broad bind acceptance. No approval was claimed. |
| 2026-07-19 | Review remediation RED/GREEN | Safety regressions first failed `6` cases and then passed `26/26`; typed evidence, endpoint classification, and resource-contract regressions then failed until implemented. A Docker CLI preflight exposed uppercase `mktemp` tokens as invalid Compose project names; a lowercase-only identity regression failed before the allocator was corrected. The then-focused suite passed `29/29`; Bash syntax and ShellCheck passed. Cleanup enumerated stopped containers, failed closed on list/down/inspect errors, binds resolved only under the current runtime except Traefik's read-only socket, and every scenario reported an explicit evidence path. |
| 2026-07-19 | Schema-v2 startup acceptance | Project `hyhome-crr-20260719-1746212-hs11x3os` passed startup-readiness with 5/5 healthy containers, 5/5 passed endpoint observations, `observed_state=ready`, 66 seconds elapsed, and schema-v2's exact 18 keys. Redaction and teardown passed; the task `/tmp` path and all task-owner container/network/volume sets were empty. |
| 2026-07-19 | Schema-v2 recovery acceptance | Project `hyhome-crr-20260719-1759144-p9uasniv` passed Vault restart, unseal, and fresh Vault Agent sentinel recovery with 5/5 healthy containers, 5/5 passed endpoints, `recovery_status=passed`, 97 seconds elapsed, and exit `0`. Redaction and teardown passed; no task-owned runtime resource remained. |
| 2026-07-19 | Schema-v2 negative-timeout acceptance (superseded routing) | Project `hyhome-crr-20260719-1770459-dhdhsk0o` reached the healthy baseline and returned class `30`, but wrote the timeout into the canonical handoff. The observation remains historical evidence; the final routing rerun below supersedes it so Task 5 can consume only a ready canonical record. |
| 2026-07-19 | Consumer-contract routing RED/GREEN | Cross-checking the Program Plan exposed that a canonical `timed_out` record could not satisfy Task 5's ready input. A routing regression failed before the wrapper separated per-scenario evidence from the canonical ready handoff. Positive runs now invalidate stale readiness before execution and atomically republish only on success; negative timeout writes and reports only its scenario record. |
| 2026-07-19 | Historical routed startup acceptance | Project `hyhome-crr-20260719-1942512-paazfwvn` produced the exact 18-key `readiness-verdict.startup-readiness.json` and atomically published the same `ready` record as the canonical handoff in 61 seconds. Cleanup and redaction passed. This predates the current early-failure finalization remediation. |
| 2026-07-19 | Historical routed recovery acceptance | Project `hyhome-crr-20260719-1961874-no8otmdh` completed restart, unseal, and fresh-sentinel recovery in 96 seconds. Both the scenario record and canonical handoff reported `scenario=vault-restart-recovery`, `overall_status=ready`, `recovery_status=passed`, and passed cleanup/redaction. This predates the current early-failure finalization remediation. |
| 2026-07-19 | Historical routed negative-timeout acceptance | Project `hyhome-crr-20260719-1985444-ecjzmczd` returned the expected class `30` after 62 seconds and wrote only `readiness-verdict.negative-timeout.json` with `overall_status=timed_out`. The canonical recovery-ready handoff retained SHA-256 `25cc72aa5c64f08517535adbdd2365684fc01c9b2a6d7bdfea719e241b053c12` before and after the negative run. Task-owned containers, networks, volumes, and `/tmp` directories were empty after all three runs. These observations predate the current early-failure finalization remediation. |
| 2026-07-19 | First routing re-review findings | The first specification routing re-review was `CHANGES REQUIRED C0/I3/M0`: positive invalidation was too late, early failures bypassed scenario verdict finalization, and the Compose Plan's Task 5 consumer rule was weaker than the Program Plan. The first quality routing re-review was `CHANGES REQUIRED C0/I2/M0`: routing coverage relied on source strings and did not exercise isolated early-failure/finalization behavior. There were no Critical or Minor findings. The earlier `C0/I0/M0` reviews remain historical pre-routing verdicts. |
| 2026-07-19 | Routing remediation RED/GREEN | Six behavior tests using isolated temporary evidence and wrapper command stubs failed before implementation: stale positive invalidation, ready publication, negative canonical preservation, dual-path stdout, all-mode early-failure evidence, and startup/recovery exit-class preservation. After captured scenario execution plus unconditional typed finalization, those tests passed and the then-current focused suite passed `34/34`. |
| 2026-07-19 | Historical final routed startup acceptance | Project `hyhome-crr-20260719-2111142-y1noqxim` produced the exact 18-key startup scenario record and matching canonical `ready` handoff in 71 seconds. Cleanup and redaction passed. |
| 2026-07-19 | Historical final routed recovery acceptance | Project `hyhome-crr-20260719-2188421-vietv7qq` passed restart, unseal, and fresh-sentinel recovery in 104 seconds. Its exact 18-key scenario and canonical records report `scenario=vault-restart-recovery`, `overall_status=ready`, `recovery_status=passed`, and passed cleanup/redaction. |
| 2026-07-19 | Historical final routed negative-timeout acceptance | Project `hyhome-crr-20260719-2281412-ho7cotsq` returned expected class `30` in 74 seconds and wrote the exact 18-key negative scenario record. The canonical recovery-ready handoff retained SHA-256 `7b95d095764ede50585e8aa267483539c39e652e94a911bdc84fabb416ee6edf` before and after the run. Task-owned containers, networks, volumes, and `/tmp` directories were empty after all final runs. |
| 2026-07-22 | Second routing re-review findings | Specification re-review returned `CHANGES REQUIRED C0/I2/M0`: a signal between Docker mutation and parent-flag synchronization could bypass cleanup, and the Program Task still claimed no live rerun. Quality re-review returned `CHANGES REQUIRED C0/I1/M0` for the same stale Program Task statement; it accepted the routing code and behavior coverage. No Critical or Minor findings remained. |
| 2026-07-22 | Signal cleanup RED/GREEN | The marker-aware EXIT/signal regression first failed two subcases: cleanup was skipped with a valid mutation marker, and cleanup failure preserved class `37` instead of class `50`. The trap now accepts only an exact `/tmp/<owned-project>` marker whose derived identity equals `CRR_PROJECT_NAME`, rejects absent, non-owned, symlinked, non-canonical, or identity-mismatched paths, and preserves the original status unless cleanup is ambiguous. The focused marker test passes `1/1`; the full suite passes `35/35`; Bash syntax, ShellCheck, and diff hygiene pass. |
| 2026-07-22 | Terminal routing re-reviews | After the final Program Plan/Task state correction, independent specification and quality/security reviewers each returned `APPROVED C0/I0/M0`. All prior Critical, Important, and Minor findings are closed. |
| 2026-07-19 | Governance validation | Metadata check selected 16 changed Stage documents with 0 violations; traceability and implementation alignment passed. Repository contracts no longer report either Task 2 script as unregistered after the canonical script inventory and executable set were updated. The remaining five failure categories are owned by later program work: Task 3–5 prospective scripts, final lifecycle-manifest reconciliation, and the existing local `html5lib` validation-runtime dependency. |
| 2026-07-22 | Program closure rerun (historical, superseded) | The 35/35 rerun and its retained handoff were valid for that committed state, but the later local-only readiness hardening and current rerun below supersede its projects and handoff identity. |
| 2026-07-22 | Local-only readiness hardening RED/GREEN (historical, superseded) | RED commit `ba1ba382` captured local-only readiness regressions. GREEN commit `7c6c4ea1` enforced the offline pinned runtime boundary for that committed state. Its 39/39 result is historical. The original implementation identity is `e41f8f04d285fc1962f723d7ec8d80d314f9e422`; `83298464` is historical only. |
| 2026-07-22 | Startup/recovery/timeout acceptance before identity hardening (historical, superseded) | Startup project `hyhome-crr-20260719-1892220-xneqdqor`, recovery project `hyhome-crr-20260719-1897762-rf7ihid9`, timeout project `hyhome-crr-20260719-1905549-soywy1gk`, and canonical SHA-256 `f6195165e46b6c2a6bc8e45eb0fa2f39beac65af60610292d4251420ea19b263` were valid for `7c6c4ea1`; the current evidence below supersedes them. |
| 2026-07-22 | Independent image-identity RED/GREEN | RED `9838034c` proved that a matching configuration ID alone did not establish the required manifest identity. GREEN `14e1dd5d` independently validates membership of every expected manifest digest in `.RepoDigests` and equality of the expected configuration digest with `.Id`, before runtime. The focused suite passes 42/42; static, preflight, and exact render gates pass. Historical terminal reviews predate these commits; the terminal whole-branch reviews below cover them. |
| 2026-07-22 | Current startup/recovery/timeout acceptance | Startup project `hyhome-crr-20260719-2642602-fxq2siqi` passed in 62 seconds. Recovery project `hyhome-crr-20260719-2648660-ov2uzbas` passed Vault restart/unseal/fresh-sentinel recovery in 81 seconds and produced the current canonical. Timeout project `hyhome-crr-20260719-2661806-zqukerpv` returned expected class 30 in 61 seconds while preserving that canonical byte-for-byte. The mode-0600, 1,197-byte canonical SHA-256 is `12fbe9fa47eb0e96a8a2ed23d033dc176bf279fce8e9a8d6b91ccd1d166e76a0`; every owner-scoped container, network, volume, and `/tmp` inventory is zero. |
| 2026-07-23 | Terminal whole-branch review closure | Quality/security review v3 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the then-current 26-document reconciliation diff. Specification review v5 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the final 26-document reconciliation diff. Earlier `CHANGES REQUIRED` iterations remain historical remediation evidence. These approvals do not change the active Task or Program lifecycle and do not authorize the controlled wrapper. |

## Verification Evidence

Exact command envelope:

```bash
python3 -m unittest tests.validation.test_compose_core_readiness -v
bash scripts/validation/validate-docker-compose.sh
bash scripts/validation/run-compose-core-readiness.sh --preflight
bash scripts/validation/run-compose-core-readiness.sh --scenario startup-readiness
bash scripts/validation/run-compose-core-readiness.sh --scenario vault-restart-recovery
bash scripts/validation/run-compose-core-readiness.sh --scenario negative-timeout
```

An explicit recovery-only cleanup may use:

```bash
bash scripts/validation/run-compose-core-readiness.sh --cleanup-only --project-name hyhome-crr-20260719-<decimal-pid>-<eight-lowercase-alphanumeric-token>
```

Expected evidence: focused tests pass; static Compose validation remains
labeled static; positive scenarios produce the exact five-service verdict with
`overall_status=ready`, `cleanup_status=passed`, and
`redaction_status=passed`; the negative timeout returns class `30`, records
`overall_status=timed_out`, and still verifies cleanup.

Actual static evidence:

- `timeout 20s bash -n scripts/validation/run-compose-core-readiness.sh scripts/validation/compose-core-readiness.lib.sh` exited `0`;
- `timeout 30s shellcheck scripts/validation/run-compose-core-readiness.sh scripts/validation/compose-core-readiness.lib.sh` exited `0`;
- the new targeted Vault Entrypoint regression first failed `1/1` against the inherited override;
- the new runtime-material permission regression first failed `1/1` against inherited `0600` container-consumed files;
- the new single-load Vault server Entrypoint regression first failed `1/1` against the explicit duplicate `-config=file` argument;
- the new mounted-secret regression first failed `1/1` against stdin unseal and host `-e VAULT_TOKEN` behavior;
- the new OAuth2 Proxy cookie-secret size regression first failed with expected `32` versus actual `45` bytes;
- the new OAuth2 Proxy internal-issuer regression first failed `1/1` against the missing required option;
- the task bridge publish-capability and Traefik ping-alignment regressions first failed `2/2`;
- the scoped Vault Agent output-volume preparation regressions first failed because the helper and ordered call did not exist;
- the CHOWN-only operation-order and exact secret-regeneration regressions first failed `2/2`;
- the deterministic fresh-sentinel recovery sequence and eight-step fail-closed regressions first failed against the stale Agent flow;
- the six routing behavior tests first failed because sourcing the inherited
  wrapper immediately dispatched usage class `2`; the inherited executable
  path also invalidated the canonical handoff only after render/daemon/capacity
  and had no unconditional early-failure scenario finalizer;
- `python3 -m pytest` was unavailable in the repository runtime (`No module named pytest`), so no pytest verdict is claimed;
- `python3 -m unittest tests.validation.test_compose_core_readiness` passes the current focused suite `42/42` after the routing, signal-cleanup, local-only readiness, and independent manifest/config identity RED cycles;
- `timeout 120s bash scripts/validation/validate-docker-compose.sh` exited `0` with `services_total=5`;
- `timeout 60s bash scripts/validation/run-compose-core-readiness.sh --preflight` exited `0`, emitted `keycloak,oauth2-proxy,traefik,vault,vault-agent` and ports `18000,18443,18082,18083,18200`, and left no owned temporary path;
- the focused daemon-separation regression proves `assert_docker_compose` passes with a Compose-capable CLI even when the Docker API fails, while `assert_docker_daemon` returns class `10`.
- metadata, documentation traceability, and implementation-alignment gates pass;
  the repository-contract gate reports five deferred categories owned by later
  program Tasks and no Task 2 script-inventory or script-usage failure.

Runtime verification results: all prior PID-only/nine-key and pre-identity-
hardening runs, including handoffs at SHA-256
`7b95d095764ede50585e8aa267483539c39e652e94a911bdc84fabb416ee6edf`,
`e78d1a0bf3470b14a545f4d99971c7b2b88a67e422937896632533ce1ebe9d64`,
and `f6195165e46b6c2a6bc8e45eb0fa2f39beac65af60610292d4251420ea19b263`,
are explicitly historical and superseded. The current identity-hardened rerun
used startup project `hyhome-crr-20260719-2642602-fxq2siqi`, recovery project
`hyhome-crr-20260719-2648660-ov2uzbas`, and timeout project
`hyhome-crr-20260719-2661806-zqukerpv`. Startup and recovery passed; timeout
returned class `30` and preserved the recovery-ready canonical byte-for-byte.
The current canonical is mode 0600, 1,197 bytes, schema 2, and SHA-256
`12fbe9fa47eb0e96a8a2ed23d033dc176bf279fce8e9a8d6b91ccd1d166e76a0`.
It records five healthy containers, five passed endpoints, and passed recovery,
teardown, cleanup, and redaction. All current owner-scoped container, network,
volume, and `/tmp` inventories are empty.
Exit classes remain
`0=pass`, `2=usage`, `10=preflight/scope`, `20=startup`, `30=readiness`,
`40=recovery`, and `50=cleanup ambiguity`.

Task 6 documentation, owner regeneration, safe gates, and whole-branch
re-review are recorded by the Program Task. The controlled all-files wrapper
remains blocked and `not_run`.

## Controlled Agent Pre-commit Evidence

Controlled wrapper command: not owned by this domain Task. The program Task
owns the single final all-files invocation after all domains and reviews pass.

Allowed prefixes: `not_applicable` at domain activation.

Wrapper exit status: `not_run`.

Snapshot result and path sets: `not_run`.

Observation boundary: if the program wrapper later runs, it observes only
Git-visible, non-ignored repository paths.

Disposition: defer to the
[program Task](./2026-07-19-operational-readiness-closure-program.md); never run
`pre-commit run --all-files` directly.

## Review Evidence

Implementation review verdict: static implementation and the three current
schema-v2 runtime scenario gates pass under the independent manifest/config
identity boundary. The routing findings have a test-first implementation and
live runtime response. Historical terminal reviews pass only for their exact
reviewed commits; the current hardening is covered by the terminal whole-branch
reviews below.

Specification review verdict: the earlier remediation review returned
`APPROVED C0/I0/M0`; it is retained as historical pre-routing evidence. The
first routing re-review was `CHANGES REQUIRED C0/I3/M0`. After remediation,
the second re-review was `CHANGES REQUIRED C0/I2/M0` for signal cleanup and a
stale Program Task statement. Both findings were remediated; the terminal
specification review returned `APPROVED C0/I0/M0` for the then-reviewed
commits. Terminal specification review v5 returned `APPROVED C0/I0/M0` for the
full branch range through `20022458` plus the final 26-document reconciliation
diff, including `9838034c` and `14e1dd5d`.

Quality/security review verdict: the earlier remediation review returned
`APPROVED C0/I0/M0`; it is retained as historical pre-routing evidence. The
first routing quality review was `CHANGES REQUIRED C0/I2/M0`. After
remediation, the second review was `CHANGES REQUIRED C0/I1/M0` only for the
stale Program Task statement and accepted the code/test response. That finding
was remediated; the terminal quality/security review returned
`APPROVED C0/I0/M0` for the then-reviewed commits. Terminal quality/security
review v3 returned `APPROVED C0/I0/M0` for the full branch range through
`20022458` plus the then-current 26-document reconciliation diff.

Findings and disposition: terminal routing review severities were specification
`C0/I0/M0` and quality/security `C0/I0/M0` for their historical exact range.
The current implementation response passes `42/42` focused tests and the
document gates. The current whole-branch review severities are specification
v5 `C0/I0/M0` and quality/security v3 `C0/I0/M0`; earlier
`CHANGES REQUIRED` iterations remain historical remediation evidence.

## Commit Ledger

Original implementation identity:
`e41f8f04d285fc1962f723d7ec8d80d314f9e422`
(`feat(harness): add compose runtime acceptance`). The short identity
`83298464` is historical only. The local-only boundary used RED `ba1ba382` and
GREEN `7c6c4ea1`; current identity hardening is RED `9838034c` followed by
GREEN `14e1dd5d`.

Logical unit: `feat(harness): add compose runtime acceptance`.

Commit validation: the three current routed runtime scenarios pass as recorded
above, including independent manifest/config identity checks, scoped cleanup,
redaction, and byte-identical ready handoff preservation. Focused/static gates
pass; terminal whole-branch specification v5 and quality/security v3 reviews
are APPROVED C0/I0/M0.

## Deferred and Blocked Items

Deferred items: production/shared-host startup, broader profiles, data restore,
remote observability, registry access, deployment, and live secret integration.

Blocked items: implementation/runtime and current review have no remaining
local blocker. The Task remains active under the Program lifecycle; the
controlled wrapper is still blocked by the separate Task 3 and Task 5 domain
outcomes.

Deferral destination: data restore routes to [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md);
remote or broader runtime requires a new approved design chain and Task.

## Related Documents

- [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- [Compose Plan](../plans/2026-07-11-compose-runtime-readiness-remediation.md)
- [Program Task](./2026-07-19-operational-readiness-closure-program.md)
- [Infrastructure Task](./2026-07-19-infrastructure-operations-readiness-remediation.md)
- [Delivery Task](./2026-07-19-deployment-release-engineering-remediation.md)
- [Docker bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/)
