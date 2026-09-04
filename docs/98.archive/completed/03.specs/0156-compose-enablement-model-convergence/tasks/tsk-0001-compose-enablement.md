---
title: Converge Compose Enablement onto Profiles
version: 1.0.0
type: sdlc/task
layer: specs
status: completed
owner: "@buenhyden"
artifact_id: SPEC-0156-TSK-0001
parent_ids: [SPEC-0156, SPEC-0156-PLAN-0001]
created: 2026-09-02
updated: 2026-09-04
completed_at: 2026-09-04
---

# Converge Compose Enablement onto Profiles

## Objective

Execute the five steps in the Plan so that stack membership is expressed by
Compose profiles alone and every `infra/` Compose file Compose can hold is
reachable.

## Inputs

- `docker-compose.yml` and its `include:` list
- `infra/**/docker-compose*.{yml,yaml}`
- `scripts/operations/generate-compose-profile-service-coverage.sh`
- `scripts/validation/validate-docker-compose.sh`
- `docs/90.references/data/0059-compose-profile-service-coverage/README.md`

## Work Log

Re-measuring the Spec's inputs before execution contradicted four of them, and
one contradiction was structural rather than numeric.

| Spec claim | Measured 2026-09-04 | Consequence |
| :--- | :--- | :--- |
| 46 Compose files under `infra/` | 47 | One file carries `.yaml`, which the Spec's own acceptance glob could not reach |
| `profiles:` declarations 147 | 145 lines, 160 services | YAML anchors let several services share one declaration |
| 15 distinct profile names | 24 | No scope reproduces the Spec's (15, 44, 8) triple |
| 44 services carry `dev` | 48 | |
| Generator reads the resolved root config | Reads the tracked tree already | Step 4 needed regeneration, not redesign |
| Step 2 adds `profiles:` to the 20 restored files | All their services already declare one | The 8 profile-less services are elsewhere |

The structural contradiction is Plan step 3. It directed that a sibling pair
whose divergence exceeds a profile be included on both sides under mutually
exclusive profiles. `include:` merges files into one model before any profile is
evaluated, so two members declaring the same service name merge into one service
rather than staying alternatives. Rendering all 47 together fails outright:

```text
validating docker-compose.yml: services.airflow-triggerer.security_opt items at 0 and 1 are equal
```

Six pairs share service names, thirty names in total. The `06-observability`
pair shares all nine, adds none, and differs only in settings, so a profile has
nothing to select there at all. Those six went to SPEC-0171 and this Task
executed the rest.

### Sibling pair measurements

| Directory | Shared | Only in the fuller member | Differing keys | Disposition |
| :--- | ---: | :--- | ---: | :--- |
| `06-observability` | 9 | none | 11 | SPEC-0171 |
| `07-workflow/airflow` | 8 | `airflow-valkey` ×2 | 28 | SPEC-0171 |
| `05-messaging/kafka` | 7 | `kafka-2`, `kafka-3` | 20 | SPEC-0171 |
| `07-workflow/n8n` | 4 | `n8n-valkey` ×2 | 10 | SPEC-0171 |
| `02-auth/oauth2-proxy` | 1 | `oauth2-proxy-valkey` ×2 | 2 | SPEC-0171 |
| `04-data/analytics/opensearch` | 1 | `opensearch-node1..3` | 11 | SPEC-0171 |
| `04-data/lake-and-object/minio` | 0 | `minio1..4` | n/a | included here under `storage-cluster` |

The minio pair is the one that shares no service name, so profiles express it.
Its four services declared no profile at all, which meant including the file
would have started them unselected.

### Profile render defects

Rendering the previously unreachable profiles exposed three that could not
render:

```text
ksql   service "ksqldb-cli" depends on undefined service "ksqldb-server"
nginx  service "nginx" depends on undefined service "minio"
obs    service "cassandra-exporter" depends on undefined service "cassandra-node1"
```

A `depends_on` target must carry every profile of the service depending on it,
and the rule is transitive: adding `obs` to `mongo-init` moved the failure to
`mongodb-rep1`. Closing the dependency graph to a fixpoint took seven services
and then converged with no unresolved target.

| Service | Profile added | Required by |
| :--- | :--- | :--- |
| `cassandra-node1` | `obs` | `cassandra-exporter` |
| `ksqldb-server` | `ksql` | `ksqldb-cli`, `ksql-datagen` |
| `mongo-init` | `obs` | `mongodb-exporter` |
| `mongo-key-generator` | `obs` | `mongo-init` (transitive) |
| `mongodb-rep1` | `obs` | `mongo-init` (transitive) |
| `mongodb-rep2` | `obs` | `mongo-init` (transitive) |
| `minio` | `nginx` | `nginx` |

### Host-port findings

| Port | Services | Origin | Disposition |
| :--- | :--- | :--- | :--- |
| 18089 | `k6-master`, `locust-master` | introduced: both carry `tooling` and `testing`, and k6 borrowed `LOCUST_HOST_PORT` | resolved with `K6_HOST_PORT` default 18189 |
| 80, 443 | `nginx`, `traefik` | introduced but profile-disjoint | recorded in POL-0078 as a mutually exclusive pair |
| 8000 | `kong` (supabase), `surrealdb` (open-notebook) | pre-existing: both files are already included | recorded, not repaired |

The 8000 collision predates this change. `kong` carries `data` and `surrealdb`
carries `admin` and `dev`, so selecting `data dev` together binds 8000 twice.
Changing a published port of an already-included stack reaches outside this
Spec's authority, so it is left as a finding.

### Deferred defects found in passing

- `infra/09-tooling/k6/docker-compose.yml` is a copy of the locust file. It runs
  `locust -f /mnt/locust/locustfile.py --master`, mounts at `/mnt/locust`, and
  declares `build: .` with no Dockerfile in that directory. Including it makes
  the file reachable, which is what this Spec owns; making the service work is
  service configuration content, which it does not.
- The first all-files QA run rewrote five preserved records under
  `docs/98.archive/retired/03.specs/`. That is a SPEC-0170 gap this Task closed
  rather than carried, because leaving it means every future all-files run
  silently edits frozen bodies.

## Verification Evidence

| Acceptance item | Command | Result |
| :--- | :--- | :--- |
| 1 | `grep -c '^  # - infra/' docker-compose.yml` | `0` |
| 2 | tracked `infra/**/docker-compose*.{yml,yaml}` in `include:` | `41` of 47; the 6 SPEC-0171 members excluded |
| 3 | `docker compose config --services` with no profile | prints nothing |
| 4 | `docker compose config --quiet` per declared profile | 25 of 25 render |
| 5 | published host bindings per profile | no in-profile collision |
| 6 | declared names against POL-0078, both directions | `declared=25 registered=25`, neither set has an extra |
| 7 | `bash scripts/validation/validate-docker-compose.sh` | `selections=25 services_total=220`, exit 0 |
| 8 | `bash scripts/operations/generate-compose-profile-service-coverage.sh --check` | `PASS`; 48 files, 168 services, profile-less down from 8 to 4 |
| 9 | `git ls-files docker-compose.yml.format` | empty |
| 10 | `python3 scripts/validation/run-ci-gate.py --profile full` | `GATE_EXIT=0`, 18 `OK` suites |
| 11 | this section and the findings above | recorded |

### Per-profile render

```text
admin 6   ai 4    auth 2   communication 2   core 5    data 58
dev 47    graph 1  iac 4    ksql 3            messaging 8
messaging-option 1  mng 5   nginx 2  obs 18   registry 1
sast 1    security 2  service 19  storage 2   storage-cluster 4
sync 1    testing 2   tooling 10  workflow 12
```

The four profile-less services that remain are the opensearch cluster members
SPEC-0171 owns; they are the only reason the coverage snapshot still reports a
`default` group.

### Mutation evidence

A passing check proves nothing until it has been made to fail.

| Check | Mutation | Observed |
| :--- | :--- | :--- |
| in-profile host-port collision | restore k6's `LOCUST_HOST_PORT` | `FAIL: testing: ... 0.0.0.0:18089/tcp <- k6-master, locust-master`, exit 1 |
| profile enumeration ordering | call `config --profiles` before `.env` exists | `no port specified: :<empty>`, then `No Docker Compose profiles resolved` |
| preserved-record protection | run all-files QA without the ignore entries | 5 records under `docs/98.archive/retired/` rewritten |

## Review Evidence

- `python3 scripts/validation/check-document-metadata.py --mode check-contracts`: `violations=0`
- `python3 scripts/validation/check-document-links.py --mode all`: `documents=674 links=5634 failures=0`
- `bash scripts/validation/run-agent-precommit-all-files.sh --task <this file> --allow-prefix infra --allow-prefix docs --allow-prefix scripts --allow-prefix README.md --allow-prefix .env.example --allow-prefix docker-compose.yml`: `QA_EXIT=0 hook_result=passed changed_count=0 unexpected_count=0`

Run before completion, per the sequencing `documentation-protocol.md` records:
this Task must still live under `docs/03.specs/` to receive the evidence.

## Commit Ledger

| Commit | Scope |
| :--- | :--- |
| `95ad9c41` | Re-scope the Spec to what `include:` can hold; open SPEC-0171 |
| `ed89277b` | Register the profile vocabulary as POL-0078 |
| `a574ce6a` | Include 41 files unconditionally; close the profile dependency graph |
| `18de4d9e` | Render every declared profile and fail on in-profile port collisions |
| `a735e37b` | Remove the root Compose scaffold |
| `bb8a6d51` | Stop the markdown formatter rewriting preserved archive records |

## Rulings

- The package was completed and activated on 2026-09-02 without executing it.
  A Spec with no Plan and no Task cannot be executed by the governance flow, and
  the enablement change itself rewrites service selection across the tree, so it
  is its own reviewed unit rather than a rider on a documentation change.
- Correcting the Spec was preferred over executing it as written. Four measured
  inputs did not reproduce and one instruction was impossible in Compose, so
  executing the text would have produced a broken render and a false record.
- Adding a profile to a `depends_on` target was treated as in scope even though
  the Spec's scope names only services declaring none. Acceptance item 4 cannot
  be met otherwise: three profiles do not render until the graph is closed.
- The k6 stub was made reachable rather than repaired. Reachability is what this
  Spec owns; the service content belongs to its domain owner, and hiding the
  file again is the failure mode the Spec exists to end.
- The formatter conflict was fixed here rather than referred to SPEC-0170. That
  package is completed and preserved, so it cannot take the change, and leaving
  it would let every future all-files run corrupt preserved bodies.

## Deferred Items

| Item | Owner |
| :--- | :--- |
| Six sibling pairs that share service names | SPEC-0171 |
| `kong` and `surrealdb` both publishing host 8000 | operations domain owner for `04-data` and `11-laboratory` |
| `infra/09-tooling/k6/` running locust with a missing Dockerfile | operations domain owner for `09-tooling` |

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Compose profile vocabulary](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md)
- [Compose sibling pair resolution](../../0171-compose-sibling-pair-resolution/spec.md)
