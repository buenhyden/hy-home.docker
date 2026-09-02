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
updated: 2026-09-02
---

# Compose Enablement Model Convergence Plan

## Objective

Converge stack membership onto Compose `profiles:` alone, make all 46 `infra/`
Compose files reachable from the root entry point, and make the generated
coverage snapshot describe the whole tree.

## Dependencies

- SPEC-0155 supplies the deduplicated generated-evidence rules the coverage
  snapshot follows.
- REQ-0023 and ADR-0026 bound network handling, so `infra_net` shape is fixed.
- Docker Compose must be available for rendering; `docker compose version`
  reports v5.4.0 on the development host.

## Execution Sequence

1. **Profile vocabulary.** Define the 15 declared profile names in one place and
   state which are topology selectors and which are domain selectors. Nothing
   else can be decided until the vocabulary is fixed. Verify by listing every
   `profiles:` value under `infra/` against the definition.
2. **Restore commented includes.** Turn the 20 commented `include:` entries into
   unconditional entries, adding `profiles:` to every service they declare.
   Verify with `docker compose config --quiet` selecting no profile: it must
   succeed and start no service.
3. **Resolve sibling pairs.** For each of the 9 unreferenced files, measure the
   difference against its sibling and either express it as a profile or include
   both under mutually exclusive profiles. Record the measured difference and
   the decision per pair in the Task. Verify each pair renders per profile.
4. **Coverage generator.** Change
   `scripts/operations/generate-compose-profile-service-coverage.sh` to
   enumerate services from the `infra/` tree, and extend
   `scripts/validation/validate-docker-compose.sh` to render every declared
   profile. Regenerate the snapshot in the same change. Verify both with
   `--check`.
5. **Root scaffold removal.** Delete `docker-compose.yml.format`. Verify
   `git ls-files docker-compose.yml.format` returns nothing.

## Risk and Rollback

The highest risk is step 2: restoring 20 stacks can collide on ports or volumes
with the 17 already active. The guardrail is that every restored service lands
profile-gated, so the no-profile render must start nothing; the union render is
checked before the step is committed. Each step is one commit, so any step
reverts alone. No step runs `up`, `down`, or any live restart.

## Verification

Every numbered item in the Spec's Acceptance Contract, plus
`python3 scripts/validation/run-ci-gate.py --profile full`.

## Related Documents

- [Specification](./spec.md)
- [Task](./tasks/tsk-0001-compose-enablement.md)
