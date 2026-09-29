---
title: "Compose Host Port Exposure"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
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

Not started.

## Review Evidence

None yet.

## Commit Ledger

None yet.

## Rulings

- 2026-09-29: Owner approved the Spec and Plan ("승인") with the two answers above.

## Deferred Items

- `VALKEY_MNG_HOST_POST` is a consistently used misspelling of a host-port key.
  Renaming it changes an operator `.env` key, so it needs its own change.
- POL-0047 and POL-0049 call Pyroscope and Tempo `OPTIONAL`, while POL-0078
  adds `profiling` and `tracing` to HOME.
