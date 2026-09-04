---
title: Compose Sibling Pair Resolution Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0171-PLAN-0001
parent_ids: [SPEC-0171]
created: 2026-09-04
updated: 2026-09-04
completed_at: 2026-09-04
---

# Compose Sibling Pair Resolution Plan

## Objective

Make both topologies of each of the six sibling pairs selectable from the root
entry point, without the invalid merge that including both members produces.

## Dependencies

- SPEC-0156 converged every other file and left these six measured.
- POL-0078 owns the profile vocabulary any new selector joins.
- Docker Compose must be available for rendering; `docker compose version`
  reports v5.4.0 on the development host.
- Rendering must read the real `.env`. A linked worktree does not carry the
  ignored file, so every render passes `--env-file` pointing at the main
  checkout.

## Execution Sequence

The Spec listed three candidate approaches. Measurement found a fourth that
covers all six, so the sequence below applies it and the other three are not
used.

1. **Capture a baseline.** Render every one of the twelve members alone,
   through a temporary root that includes only it, and store the resolved
   service model. `extends.file` resolves against the project directory, so a
   member rendered with `-f` alone cannot find `../common-optimizations.yml`;
   including it reproduces the resolution the repository actually uses. Nothing
   else may start until this exists, because it is the only evidence that a
   merge preserved behavior.
2. **Merge the near-duplicate.** `06-observability` shares all nine service
   names and differs on two settings. Keep one file, make both settings
   variables, delete the other. Verify both members reproduce.
3. **Merge the three shared-broker pairs.** `oauth2-proxy`, `n8n`, and
   `airflow` differ on whether the app uses the shared `mng-valkey` or its own.
   Gate the dedicated brokers behind one selector, and drive the app's address,
   secret path, and build target from variables defaulting to the shared
   instance. Verify all six members reproduce.
4. **Fold the opensearch cluster.** Move its three nodes behind a selector and
   keep the integrated dashboards rather than the draft's. Verify both members.
5. **Merge kafka onto the running member.** The two files drifted apart, so the
   member the root includes wins and the extra brokers move onto it. Verify the
   single-broker member reproduces exactly and record where the cluster
   topology departs from the file that declared it.
6. **Register and reconcile.** Add every new selector to POL-0078 with its
   coupling and exclusivity, declare the variables in `.env.example`, and
   update every citation of a removed file.

## Risk and Rollback

The highest risk is that a merge changes an effective setting without anyone
noticing, because 3,817 lines collapse to about half that and a silent
substitution looks like a clean diff.

The guardrail is step 1. Every merge is checked against the pre-merge render of
both members, service by service and key by key, and a difference is either
zero or explicitly declared as intended with a reason. A merge that produces an
unexplained difference is not committed.

`profiles` is excluded from that count, because a merged file necessarily
carries the union of both members' selectors.

Each pair is one commit, so any pair reverts alone. No step runs `up`, `down`,
or any live restart.

## Verification

Every numbered item in the Spec's Acceptance Contract, the twelve baseline
comparisons, `bash scripts/validation/validate-docker-compose.sh`, and
`python3 scripts/validation/run-ci-gate.py --profile full`.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-sibling-pair-resolution.md)
