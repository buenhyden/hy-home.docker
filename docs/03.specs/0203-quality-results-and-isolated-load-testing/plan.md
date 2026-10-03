---
title: "Quality Results and Isolated Load Testing Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0203-PLAN-0001"
parent_ids:
- "SPEC-0203"
created: "2026-10-03"
---

# Quality Results and Isolated Load Testing Plan

## Objective

Implement Prompt 03 from the locally integrated Prompt 02 baseline while
keeping HOME activation, real load and project credential issuance separate.
The supplied Prompt 03 authorizes source work; TSK-0001 records the exact
source-owned paths and evidence. Do not treat earlier SPEC-0199/0200 archive
records or synthetic Prompt 02 checks as live deployment evidence.

## Dependencies

- Baseline local main `5f99e0e51b41b912f128daafb4a3d41539b77560`;
  remote main read-only check at `e2c841eb9ef5086d0fbd6cc2ccd43ea35d89e26d`.
- SPEC-0201 quality choice and SPEC-0202 dev-pg `project.py` contract; current
  Requirements, ADR-0045/0046 and operations policies.
- Official current k6, WireMock, Locust, Timescale/PostgreSQL and Alloy docs;
  tagged image runtime behavior still needs bounded verification.
- No external app ID, target, live secret, bucket or traffic authorization is
  assumed. Prompt 04 consumes the completed shared Alloy contract.

## Execution Sequence

1. **W1: source inventory and contract.** Recheck root services, existing
   k6 remote write/dashboard, WireMock journal, Locust root graph, dev-pg
   provisioner and active document IDs. Register this Spec/Plan/Task and
   stable manifest/result/schema versions.
2. **W2: perf_db authority.** Add quality-owned database schema/migrations
   and project-scoped reader/writer/verdict grants without changing
   management metadata or reimplementing dev-pg engine provisioning. Test
   project A/B, reader write, verdict change, replay and future grants.
3. **W3: bounded runner.** Validate target origin, redirect policy, approved
   scenario path, quota and output ownership before k6. Capture immutable
   manifest, raw/summary/exit metadata and checksum; separate finalization
   from import. Test failed thresholds, interruption and invalid samples.
4. **W4: import and artifact handoff.** Add one transactional normalized
   import and explicit replay/conflict policy. Record restricted SeaweedFS
   object reference without granting a public bucket or issuing credentials.
5. **W5: WireMock and Locust.** Model function/load mock modes with distinct
   journal behavior, read-only synthetic XML/JSON fixtures and admin limits;
   reserve Toxiproxy for non-HTTP dependencies. Move Locust's complete
   master/worker closure to an independent LAB entrypoint and environment
   boundary; verify client-specific OTel support or request-event/timeout
   instrumentation. Update root/static test expectations and Korean
   README/operations guidance.
6. **W6: shared observability.** Keep k6 Prometheus remote write; add only
   bounded Alloy metrics receive, batch/resource control, necessary
   temporality conversion, Prometheus export/remote write and read-only
   Grafana result views. This Task alone writes Alloy; Prompt 04 reads the
   result. Check trace/log/profile preservation, cardinality and synthetic
   counter/histogram delta/cumulative, duplicate/drop/retry/restart behavior.
7. **W7: validation and handoff.** Run focused tests and path-aware static
   checks, then bounded synthetic Docker checks after preflight. Independently
   review security and correctness. Record precise exits and NOT_RUN HOME,
   live target, real bucket and data-migration boundaries in TSK-0001.

## Risk and Rollback

Source rollback reverts only Task-owned commits; it does not remove any live
artifact or database. Runtime cleanup targets only explicitly owned synthetic
containers/volumes/networks. A collision with HOME project, port, network,
volume or secret stops isolated execution. A failed import preserves immutable
raw evidence. Retention/deletion and operational rollback require separate
owner decisions. No full-stack up, `down -v` or volume prune.

## Verification

Use source-local unit/SQL/Compose validation, the repository's path-aware
changed gate, document metadata/links and exact `git diff --check`. Runtime
checks require Docker context/project/port/network/volume/resource/cleanup
preflight and synthetic secrets. Static render does not prove HTTP, SQL,
metrics delivery or backup. Mark unavailable or unauthorized checks `NOT_RUN`
or `BLOCKED`; do not count previous Prompt 02 tests as Prompt 03 evidence.

## Rulings

TSK-0001 is the serial writer of shared root, quality Compose, Alloy,
Grafana, environment, Registry projection and related tests. External
projects own business scenarios/fixtures. Prompt 04 consumes the resulting
Alloy contract; it does not edit the same file concurrently. The 07/08
application ideas confer no deployment or resource authority.
