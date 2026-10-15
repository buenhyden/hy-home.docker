---
title: "Common Controls and Exceptions"
version: "0.1.2"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "specs"
artifact_id: "SPEC-0218"
parent_ids:
- "REQ-0027"
- "AD-0031"
- "ADR-0046"
created: "2026-10-09"
---

# Common Controls and Exceptions

## Overview

`infra/common-optimizations.yml` gives every root and LAB service its security
defaults, lifecycle and resource tier through `extends`, and
`infra/common-optimizations.exceptions.json` lists where a service may differ.
Before this package the two shell validators rendered only the `core` profile,
keyed exceptions by service name alone, required every service to declare a
Docker secret, and the shared base granted the secret-reading group to every
service. This package checks the effective controls of all services, gives
each exception an exact target and rationale, and corrects the templates and
leaves where the defaults were wrong.

The W1–W8 execution record remains historical evidence in TSK-0001. P07
continues this package through TSK-0002 using the existing controls and
inventory owners; it does not repeat accepted source or LAB work.

## Scope

In scope: the shared templates, the exception registry and its validator, the
leaves that deviate, the Conftest Compose policy, the tests and the operations
documents that state these rules. The W1–W8 source slice excluded measured
optimal limits, new read-only root filesystems and HOME recreation. Those
exclusions describe that earlier slice, not the current P07 continuation.

P07 includes retained root-service consumer classification, representative
workload measurements, measured resource budgets, least privilege and
selective read-only filesystems. Initial public schemas, synthetic fixtures
and bounded source assessment may start independently. Sanitized read-only
baseline observation requires exact host/service/deployed-image attribution,
read-only tool permission and a recorded window against concurrent rollout;
it does not wait for SEC security acceptance or successful restore. Record
source target and deployed identity separately; unreadable private inputs
remain UNKNOWN. Benchmark/load, permission/configuration change and HOME
rollout require the relevant accepted image, function, workload, endpoint,
backup and recovery contracts plus an exclusive service window.

LAB runtime, images, data, secrets and lifecycle changes are excluded from
P07. Learning apps and actual Wiki implementation, model pulls, new workers
or workspace creation are excluded. Stage05 LAB document movement remains
with P08. Consumer retirement remains with CLN01 and the owning executor.

## Contracts

1. Effective controls. A validator renders the root with every profile and
   each LAB entrypoint with synthetic inputs and reads each service's final
   controls after `extends` and merge. Registered controls are enforced; the
   rest are reported.
2. Exact exceptions. An exception names its `scope` (`root` or
   `lab:<name>`), `compose_file`, `service`, `control` and `allowed_value`,
   with `kind`, `owner`, `reason`, `impact`, `mitigation`, `verification`,
   `reviewed`, `review_by` and `release_condition`. Orphan, duplicate,
   wildcard, unregistered, expired, overlong, stale and mismatched entries
   fail, and a root and a LAB service of one name are distinct.
3. Lifecycle is not weakening. A job (`restart: "no"`) needs no healthcheck
   and a service that reads no secret needs no Docker secret; neither is an
   exception.
4. Secret group. `SECRETS_GID` is granted by the leaf that reads a Docker
   secret or a file under a secrets directory, not by a template. A service
   that writes a data directory owned by the host group keeps the group only
   through a recorded exception.
5. Capabilities. Every template drops all capabilities. A leaf adds the
   capabilities its image proves it needs, recorded as an exact exception.
   GPU services keep the security base.
6. Process limits. Every service has a PID limit from its tier or a leaf
   override, labelled as an initial budget until measured under load.
7. URL credentials. Conftest denies a URL that carries a literal userinfo
   password or a secret-named query parameter under any variable, and checks
   the LAB entrypoints too.
8. Measurement honesty. Limit values without a load measurement are initial
   budgets with their basis recorded; no optimum or savings figure is claimed.
9. Current root assessment. Reuse the current service inventory and effective
   controls; distinguish declared, running, healthy, used and recovered states.
   Classify consumer/data ownership, role, cadence, dependency and failure cost
   without a fixed service count or parallel inventory. No traffic or disabled
   profile alone proves that a consumer is absent.
10. Scoped execution. Reuse `compose_controls.check` and `deviations` with
    explicitly selected root input. The current CLI renders root and LAB models
    and has no root-only scope flag. Do not execute a guessed flag or duplicate
    the renderer; a needed root-only extension is a coordinator proposal.

## Acceptance Criteria

1. The validator and schema v2 replace both shell checks, with tests that
   fail on each registry defect and each enforced control.
2. The old exceptions are kept, narrowed or retired against the actual
   leaves, and every remaining entry names a verification.
3. Template and leaf changes are proven by real runs of the affected LABs or
   exact images, and HOME services that change on recreation are listed with
   the evidence that they keep working.
   Earlier LAB/exact-image evidence remains historical; TSK-0002 owns only
   the open HOME residual for changed root services, without new LAB runs.
4. The Conftest rule has positive and negative fixtures that fail against the
   previous policy.
5. Operations documents, the script manifest and the gate contract match the
   new validator, and the changed gate passes.
6. Every retained root service has current consumer/data ownership, dependency,
   role and demand classification derived from the existing inventory. Decisions
   use `NO_CHANGE`, `IMPLEMENT`, `VERIFY_RUNTIME`, `DELETE`, `BLOCKED_FACTS`
   or `OUT_OF_SCOPE`; unresolved retirement facts stay with their owner.
7. Representative idle/startup/steady/peak/backfill/backup/recovery workloads
   establish numeric budgets, application overhead and measured before/after
   effects. GPU demand uses existing named workloads. Unknown measurements
   remain unknown; idle RSS and initial tiers do not prove optimal limits.
8. Actual runtime UID/GID, initialization and privilege drop, capability needs,
   rootfs write paths, secret traversal/inode/reload and restricted Docker socket
   access prove least privilege. No recursive data chown, blanket read-only
   conversion or secret-group grant is used to satisfy a validator.
9. Remaining root exceptions name exact scope/file/service/control/value,
   evidence, mitigation, owner and release condition. Existing inventory,
   version and operational projections are reconciled by their owners;
   synthetic/static findings never claim deployment or recovered state.
10. Only changed root services receive scoped rollout with exact image/config,
    health/function checks, benchmark comparison, backup and empty-target
    recovery evidence. Rollback preserves data and restores the named service
    boundary; whole-stack recreation or source revert alone is insufficient.

## Failure Conditions

Malformed, orphaned, expired or mismatched exceptions and missing enforced
controls fail effective-model validation. Unmeasured limits cannot be called
optimal, and least-privilege proof cannot be replaced by blanket secret-group,
read-only or ownership changes; root rollout requires its exact service,
function, backup and recovery evidence.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-common-controls-and-exceptions.md)
- [P07 root resource optimization](tasks/tsk-0002-p07-root-resource-optimization.md)
- [HOME development host requirement](../../01.requirements/0027-home-development-host.md)
- [Exceptions policy](../../05.operations/policies/01-common/0001-common-optimizations-template-exceptions.md)
