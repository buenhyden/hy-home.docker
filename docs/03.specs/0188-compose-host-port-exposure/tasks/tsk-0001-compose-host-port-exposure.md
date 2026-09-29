---
title: "Compose Host Port Exposure"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0188-TSK-0001"
parent_ids:
- "SPEC-0188"
- "SPEC-0188-PLAN-0001"
created: "2026-09-29"
---

# Compose Host Port Exposure

## Objective

Execute W1 through W7 of the [Plan](../plan.md) and record the evidence for
every acceptance criterion of [SPEC-0188](../spec.md).

## Inputs

- The owner's request of 2026-09-29 to analyze the 35 Conftest warnings and
  plan their remediation.
- `check-conftest-policy.sh` on `main` at `d6b68128e`: 299 tests, 264 passed,
  35 warnings, 0 failures; policy unit tests 66 passed.
- A read-only survey of each flagged service's profiles, routes, consumers,
  and documented exposure intent.

## Work Log

- 2026-09-29: Spec, Plan, and Task drafted on branch
  `fix/compose-host-port-exposure`. Execution waits for owner approval and
  answers to the Spec open questions.
- 2026-09-29: The owner approved the Spec and Plan and answered both open
  questions: a new host-wide `HOST_LAN_BIND_IP` key that Traefik also reads,
  and `pg-router` 15432 and 15433 stay reachable from the k3d cluster for
  service tests (Group B).
- 2026-09-29: W1 recorded the findings and consumers below.
- 2026-09-29: W2 through W6 landed one commit per unit or leaf (Commit Ledger).
  The owner asked that `.env` and `.env.example` share keys, key order, and
  comments, with `.env` keeping its real values. `.env` is untracked, so that
  work has no commit: `TRAEFIK_BIND_IP` became `HOST_LAN_BIND_IP` with its value
  kept, the unreferenced `KSQLDB_HOST_PORT` and `KSQLDB_PORT` were removed, and
  the file was rebuilt in `.env.example` order (464 lines, 262 keys, mode 0600).
  A value-map hash matched before and after; no value was printed.
- 2026-09-29: W7 found 23 stale Ports cells in the m0021 service inventory,
  which the local `changed` profile had not run; they were refreshed and the
  full profile passed.

### Findings and Consumers (W1)

| Service | Host ports | Group | Consumer |
| --- | --- | --- | --- |
| `traefik` | 80, 443 | A | LAN and k3d through `192.168.0.13` (POL-0096) |
| `loki` | 3100 | B | k3d Alloy push (GDE-0096) |
| `tempo` | 3200 | B | k3d trace export (GDE-0096) |
| `alloy` | 4317, 4318 | B | k3d Istio traces into `config.home.alloy` OTLP receiver (GDE-0040) |
| `mng-valkey` | 26379 | B | k3d Argo CD cache (GDE-0096) |
| `pg-router` | 15432, 15433 | B | k3d service tests (owner ruling) |
| `nginx` | 80, 443 | B | Alternative LAN gateway to Traefik (GDE-0011) |
| `mng-pg` | 25432 | C | None beyond the host operator |
| `pyroscope` | 4040 | C | None; Traefik route and `pyroscope:4040` on the Docker network |
| `locust-master` | 18089 | C | Operator browser at `localhost` (GDE-0064) |
| `supabase` Kong, analytics, Supavisor | 8000, 8443, 4000, 5432, 6543 | C | `localhost` URLs in the leaf README and `.env.example` |
| `opensearch-node1` | 9600 | C | None |
| `kafka-1..3` | external, JMX, JMX exporter (9 ports) | C | None; brokers advertise `localhost`, Prometheus scrapes `kafka-N:9404` |
| `valkey-node-0..5` | 6379-6384 | C | None; nodes announce container names |

## Verification Evidence

Compose checks were static only: no service was started, stopped, or
recreated, and no rendered model or environment value was printed. The
Conftest job ran through `check-conftest-policy.sh`, which the owner
authorized to run locally.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: 35 findings and each port's consumer recorded under Findings and Consumers (`efc07e473`) | N/A: one-time scope record |
| 6 | W1 | PASS: baseline `check-conftest-policy.sh` on `d6b68128e`: 299 tests, 264 passed, 35 warnings, 0 failures | N/A: baseline run evidence |
| 1 | W2 | PASS: the current tests against `main`'s `compose.rego` give 16 tests, 4 failures; against the new rule 16 passed (`2874eff56`) | [compose.rego](../../../../infra/09-tooling/conftest/policy/compose.rego) |
| 2 | W3 | PASS: 24 Group C ports publish as `127.0.0.1:${X_HOST_PORT:-N}:N` across seven leaves (`bf61e5e68`, `f4cfd986d`, `ef4553812`, `1035273f2`, `9c030ae1d`, `ea331c849`, `e1cd6e95e`) | The leaf Compose files |
| 3 | W4 | PASS: the nine Group B ports and Traefik bind `${HOST_LAN_BIND_IP:-192.168.0.13}`; `.env.example` declares `HOST_LAN_BIND_IP` and drops `TRAEFIK_BIND_IP` (`e36a22b7b`) | [.env.example](../../../../.env.example) |
| 4 | W5 | PASS: Conftest 294 tests, 294 passed, 0 warnings, 0 failures; the host publication rule is a `deny` (`b59da2517`) | [compose.rego](../../../../infra/09-tooling/conftest/policy/compose.rego) |
| 5 | W6 | PASS: POL-0096, GDE-0096 (Alloy OTLP contradiction removed), GDE-0095, and 13 service documents state the bindings (`c6ae1a676`); POL-0095 and the Conftest README describe only the rule-agnostic `warn`-then-`deny` lifecycle, so neither needed a change | [POL-0096](../../../05.operations/policies/0096-k8s-integration.md) |
| 6 | W7 | PASS: `validate-docker-compose.sh` selections=72, services_total=355; `docker compose --profile core config --quiet` rc 0 | N/A: run evidence for this change |
| 6 | W7 | PASS: `run-ci-gate.py --profile full` rc 0 (13 members, including `check-conftest-policy.sh` and `check-operations-catalog.py`) after `fd0d23187` | N/A: run evidence for this change |
| 6 | W7 | PASS: `tests/validation` 675 tests OK, 23 skipped; `tests/lib` 945 tests OK after `fd0d23187` (one failure before it, below) | N/A: run evidence for this change |
| 6 | W7 | PASS: `pre-commit run --from-ref main --to-ref HEAD` rc 0 | N/A: run evidence for this change |

## Review Evidence

- The first `tests/lib` run failed
  `test_operations_checker_is_executable_and_has_one_complete_route`: the m0021
  service inventory projects each service's raw `ports` strings, and 23 rows
  were stale. The local `changed` profile, run with no event environment,
  selected only the seven `repository-integrity` members, so
  `leaf.operations-catalog` had not run. `fd0d23187` replaces only those rows'
  Ports cells, taken from the catalog's own `render_service_inventory`; the
  renderer would also have dropped two hand-written lines inside the inventory
  markers, so it was not written back whole.
- Operators must recreate the affected services for the bindings to apply. An
  operator `.env` that still sets `TRAEFIK_BIND_IP` falls back to the
  `192.168.0.13` default until the key is renamed.

## Commit Ledger

| Commit | Unit | Change |
| --- | --- | --- |
| `ee080b87e` | Package | Spec, Plan, and Task drafted; registry allocation |
| `efc07e473` | W1 | Findings, consumers, and rulings |
| `2874eff56` | W2 | Rule scoped to named host addresses, with tests |
| `bf61e5e68` | W3 | `mng-pg` on loopback |
| `f4cfd986d` | W3 | `pyroscope` on loopback |
| `ef4553812` | W3 | `locust-master` on loopback |
| `1035273f2` | W3 | Supabase ports on loopback |
| `9c030ae1d` | W3 | OpenSearch 9600 on loopback |
| `ea331c849` | W3 | Kafka external and JMX ports on loopback |
| `e1cd6e95e` | W3 | Valkey cluster client ports on loopback |
| `e36a22b7b` | W4 | Group B and Traefik on `HOST_LAN_BIND_IP` |
| `b59da2517` | W5 | Rule promoted to `deny` |
| `c6ae1a676` | W6 | Stage 05 and service documents |
| `fd0d23187` | W7 | m0021 service inventory Ports refreshed |

## Rulings

- 2026-09-29: Owner approved the Spec and Plan ("승인") with the two answers above.
- 2026-09-29: Owner ruled that `.env` and `.env.example` keep identical keys,
  key order, and comments; `.env` is the live file and keeps its real values.

## Deferred Items

- `VALKEY_MNG_HOST_POST` is a consistently used misspelling of a host-port key.
  Renaming it changes an operator `.env` key, so it needs its own change.
- POL-0047 and POL-0049 call Pyroscope and Tempo `OPTIONAL`, while POL-0078
  adds `profiling` and `tracing` to HOME.
