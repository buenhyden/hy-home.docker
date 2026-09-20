---
title: "Home and Development Server Convergence Specification"
version: "0.2.1"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "specs"
artifact_id: "SPEC-0180"
parent_ids:
- "REQ-0027"
created: "2026-09-19"
---

# Home and Development Server Convergence Specification

## Overview

Converge the existing single-host Home and Development Server implementation,
operational documentation, profiles, environment contracts and dependency update
ownership. The owner's attached mission authorizes repository implementation and
value-preserving local metadata synchronization; live deployment requires a
separately approved concrete target.

## Boundaries and Inputs

The current comparison baseline is main at
`dffc2ed8bc3bf4b2538b03884ad7ab5d7587375b` on 2026-09-20. The original
`d1e6ded52808b02392c52472d5416518a3b959d6` baseline remains historical evidence
in Task 0001. Implementation uses the isolated
`codex/home-dev-convergence-followup` worktree; this follow-up closes measured
gaps instead of repeating already delivered changes. Inputs are tracked implementation,
rendered safe Compose summaries, executable checks, authorized read-only host
observations and official upstream references, in that order. The existing
SPEC-0179 proposal is independent and is not adopted by this change.

Scope includes infra, root Compose, Stage 01/02/03/05/90/99, public environment
and secret schemas, existing synchronization scripts, validators and tests,
Renovate and Dependabot. Frozen archive bodies, secret values, remote settings,
unapproved runtime changes and destructive data removal are excluded.

## Behavior Contract

Compose and Dockerfile declarations own runtime pins. The version registry is
a machine-readable projection; narrative documentation links to that authority.
Exact runtime patch literals require an explained compatibility, advisory,
workaround, migration or historical-evidence exception. Frontmatter document
versions are independent of runtime pins. Synthetic examples in runtime documentation
use placeholders instead of executable-looking patch pins.

POL-0078 alone owns profile vocabulary. Every tracked Compose is included and
every service has an explicit activation profile. HOME selection excludes
legacy services, cluster experiments and side-effect maintenance jobs.
Each dependency surface has exactly one version-update owner.

Public environment and secret metadata describe current consumers. Private
values remain preserved and never enter output, diffs, reports or model context.
Each retained component has implementation navigation and operational ownership.

## Technical Approach

Compare the nine acceptance criteria and original W1–W9 work units against
current main before implementation. Preserve completed OpenBao and native OIDC
acceptance in Tasks 0002–0004; their exact authorization is not a blanket new
rollout approval. Refresh actual service/profile/config/version inventories and
official evidence, classify services HOME/DEV/OPTIONAL/LAB/REMOVE/MIGRATE, and
update Stage 99 only where a demonstrated contract gap requires it before
authoring dependent documents. Extend existing validator and
synchronization owners with regression tests; do not add competing validators.
Prefer single-node HOME dependencies, explicit optional capabilities and manual
maintenance jobs. Introduce a home selector only if evidence justifies it.

The current Plan assigns bounded A–G/R work units with explicit file ownership and
interfaces. Each implementation unit receives specification and quality/security
review, correction and scoped re-review. Task 0005 owns the acceptance matrix,
execution ledger, check outcomes and rulings; temporary coordination files are
not an additional authority.

## Interfaces and Data

Root Compose includes and service definitions, POL-0078 vocabulary, public
environment keys, secret IDs/paths/grants, registry image references, update
manager ownership, and Guide/Policy/Runbook links are cross-checked contracts.
Evidence contains names, paths, counts, classifications and statuses only.

## Failure Modes and Guardrails

Do not render real environment values into output. Do not run broad profile
deployment, reboot, secret rotation, volume deletion or remote mutation without
the corresponding concrete approval. Preserve existing local values and unknown
private metadata except the later owner-approved exact-key pruning recorded in
Task 0002. A failed or unexecuted check is never recorded as PASS.

## Acceptance Contract

1. Current tracked service, profile, config, secret metadata, image and runtime
   inventory is measured and every service has a justified disposition.
2. Official external evidence supports architecture and dependency decisions.
3. Root includes, profile vocabulary, dependency closure and port validation
   agree; maintenance and legacy services are excluded from normal HOME use.
4. Stage 99 contracts and README/Stage 05 responsibilities agree, with retained
   services covered and unjustified exact runtime patch duplication rejected.
5. Runtime pins and registry agree; ambiguous or missing sources fail closed;
   dependency ownership is unique and infrastructure automerge is disabled.
6. Public environment and secret metadata have unique identities and current
   mappings; private synchronization preserves values with no exposure.
7. Focused regression tests and applicable changed/full, Compose, hardening,
   links, registry and Renovate checks record actual exit status.
8. Approved runtime deployment, health, persistence, resources and backup/restore
   verification are distinguished from pending approval and unverified evidence.
9. Reviewed logical commits and a PR report expose delivered changes, residual
   risks, validation limitations and recovery procedures accurately.

## Traceability

- [REQ-0027](../../01.requirements/0027-home-development-host.md)
- [AD-0028](../../02.architecture/descriptions/0028-operational-readiness-closure.md)
- [AD-0031 Home and Development Host](../../02.architecture/descriptions/0031-home-development-host.md)
- [Plan](plan.md)
- [Initial execution](tasks/tsk-0001-home-dev-convergence.md)
- [OpenBao and environment convergence](tasks/tsk-0002-openbao-access-and-env-convergence.md)
- [Auth research](tasks/tsk-0003-keycloak-oidc-operations-research.md)
- [Native OIDC migration evidence](tasks/tsk-0004-native-oidc-service-migration.md)
- [Prior current-main convergence evidence](tasks/tsk-0005-current-main-convergence.md)
- [Current Task](tasks/tsk-0006-ci-quality-version-alignment.md)

## Open Questions

Actual HOME application consumers, measured host resources and existing data
determine final service disposition. A point-in-time host observation cannot
establish steady/peak consumption, disk growth, reboot recovery or restoration.
These remain explicit evidence gaps. Runtime approval will name targets and
recovery after a validated configuration is available.

The owner clarified that AI and workflow services must remain always-on HOME
capabilities, together with their persistent storage, broker, authentication and
monitoring dependencies.

## Operational Impact

Tracked changes are reviewed before local deployment. Config rollback uses the
baseline Git version; data rollback requires verified backups and separate
approval. No static result establishes live readiness.
