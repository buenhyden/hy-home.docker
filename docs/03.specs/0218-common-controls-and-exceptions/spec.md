---
title: "Common Controls and Exceptions"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
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

## Scope

In scope: the shared templates, the exception registry and its validator, the
leaves that deviate, the Conftest Compose policy, the tests and the operations
documents that state these rules. Out of scope: measured optimal resource
limits (no load test runs here), read-only root filesystems for the services
that are writable today, and HOME recreation of running services, which
applies the changed definitions only when the owner recreates them.

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

## Acceptance Criteria

1. The validator and schema v2 replace both shell checks, with tests that
   fail on each registry defect and each enforced control.
2. The old exceptions are kept, narrowed or retired against the actual
   leaves, and every remaining entry names a verification.
3. Template and leaf changes are proven by real runs of the affected LABs or
   exact images, and HOME services that change on recreation are listed with
   the evidence that they keep working.
4. The Conftest rule has positive and negative fixtures that fail against the
   previous policy.
5. Operations documents, the script manifest and the gate contract match the
   new validator, and the changed gate passes.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-common-controls-and-exceptions.md)
- [HOME development host requirement](../../01.requirements/0027-home-development-host.md)
- [Exceptions policy](../../05.operations/policies/0001-common-optimizations-template-exceptions.md)
