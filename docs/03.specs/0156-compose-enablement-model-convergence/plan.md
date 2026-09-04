---
title: Compose Enablement Model Convergence Plan
version: 1.0.0
type: sdlc/plan
layer: specs
status: active
owner: "@buenhyden"
artifact_id: SPEC-0156-PLAN-0001
parent_ids: [SPEC-0156]
created: 2026-09-02
updated: 2026-09-04
---

# Compose Enablement Model Convergence Plan

## Objective

Converge stack membership onto Compose `profiles:` alone and make every `infra/`
Compose file reachable from the root entry point, except the six sibling pair
members whose shared service names Compose cannot hold side by side.

## Dependencies

- SPEC-0155 supplies the deduplicated generated-evidence rules the coverage
  snapshot follows.
- REQ-0023 and ADR-0026 bound network handling, so `infra_net` shape is fixed.
- Docker Compose must be available for rendering; `docker compose version`
  reports v5.4.0 on the development host.
- Rendering must read the real `.env`. A linked worktree does not carry the
  ignored `.env`, so every render passes `--env-file` pointing at the main
  checkout; without it every port resolves blank and the collision check is
  meaningless.

## Execution Sequence

1. **Profile vocabulary.** Register the 24 declared profile names as POL-0078
   under `00-workspace`, stating for each what it selects and which names are
   mutually exclusive. Nothing else can be decided until the vocabulary is
   fixed. Verify by listing every `profiles:` value under `infra/` against the
   policy in both directions: no declared name is unregistered, and no
   registered name is undeclared.
2. **Restore includes.** Turn the 20 commented `include:` entries into
   unconditional entries and add the four unreferenced files that share no
   service name with a sibling. Give the four minio cluster services a profile.
   Verify with `docker compose config --services` selecting no profile: it must
   print nothing.
3. **Host-port exclusivity.** Render the union of every declared profile,
   extract published host bindings, and resolve each collision this change
   makes selectable. Record every finding, including the pre-existing one, in
   the Task.
4. **Render coverage.** Extend `scripts/validation/validate-docker-compose.sh`
   to render every declared profile and to fail on an in-profile host-port
   collision. Regenerate the coverage snapshot. Verify both with `--check`.
5. **Root scaffold removal.** Delete `docker-compose.yml.format`. Verify
   `git ls-files docker-compose.yml.format` returns nothing.

## Risk and Rollback

The highest risk is step 2: restoring 20 stacks can collide on ports with the 17
already active. The guardrail is that every restored service lands
profile-gated, so the no-profile render must resolve nothing; the union render
is checked before the step is committed. Volume collision is not a risk here,
because the union render already resolves 74 named volumes with none
undeclared.

The measured collisions are three, and only two are introduced by this change.
Step 3 resolves those two and leaves the pre-existing one recorded, because
changing a published port of an already-included stack reaches outside this
Spec.

Each step is one commit, so any step reverts alone. No step runs `up`, `down`,
or any live restart.

## Verification

Every numbered item in the Spec's Acceptance Contract, plus
`python3 scripts/validation/run-ci-gate.py --profile full`.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-compose-enablement.md)
