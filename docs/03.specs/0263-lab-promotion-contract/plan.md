---
title: "LAB Promotion Contract Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0263-PLAN-0001"
parent_ids:
- "SPEC-0263"
created: "2026-11-05"
---

# LAB Promotion Contract Plan

## Overview

The plan has six steps:

1. Teach `scripts/operations/lab.py` the folder layout and the manifest.
2. Move the 15 LABs into that layout.
3. Move supabase to LAB secret copies.
4. Add the promotion readiness check.
5. Write the promotion operations documents.
6. Record the checks.

Every step extends `lab.py`, its tests and the existing catalogs. No new
controller is added. W7 then sizes reservations, and W8 retires the supabase
LAB by the owner decision of 2026-11-06.

**Executor rules.** Read the [Spec](spec.md) and this Plan together. Steps use
checkboxes. Run each test through the Python 3.12 controller venv
`~/.local/share/hy-home/controller-venv-py312/bin/python -m pytest`, written
`pytest` below.

## Scope

**In scope:**

- the 15 LAB entrypoints, assets and READMEs;
- `scripts/operations/lab.py` and its tests;
- the secret catalog `infra/03-security/openbao/secret-catalog.json`;
- active references to the flat `labs/<name>.yml` paths in `infra/`,
  `scripts/`, `tests/`, `examples/`, Stage 01, Stage 02, Stage 05 and
  non-terminal Stage 03 documents;
- new operations documents under `15-labs`.

**Out of scope:**

- promoting any LAB;
- starting any container;
- reading or writing a secret value;
- editing `secrets/`;
- editing Stage 90 records and the bodies of terminal Tasks. These keep the old
  paths as provenance.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 2, 3 | `lab.py` resolves `labs/<name>/docker-compose.yml`, validates `promotion.yaml`, and allows only supabase `vector`'s read-only socket | None | TSK-0001 | `test_lab_controller.py` |
| W2 | 1, 2 | Move the 15 LABs, their assets and dashboards into `labs/<name>/`, fix relative paths, write each manifest, reconcile active references | W1 | TSK-0001 | `compose config` per LAB; `lab.py check` render; unit suite; hardening |
| W3 | 3 | supabase reads only `secrets/labs/supabase/`; catalog rows, the new SMTP copy row and tests follow; prepare the registry edits for the owner | W2 | TSK-0001 | `test_secret_metadata_sync.py`; `test_supabase_smtp_rehearsal.py`; `lab.py check` |
| W4 | 5 | `lab.py readiness <name>` writes the section 5 report from measured host values, with the reserve from the promotion policy | W1, W2 | TSK-0001 | `test_lab_controller.py`; one read-only run on HOME |
| W5 | 4, 6 | Promotion policy (destination rules, reserve) and Runbook (three procedures); Kafka and OpenSearch cluster Guides and Runbooks | W2, W4 | TSK-0001 | operations catalog; metadata; links |
| W6 | 7 | Record local and hosted CI results | W1-W5 | TSK-0001 | the checks in the Verification Plan |
| W7 | 5, 8 | Amend the resource rule to reservations plus an external-workload allowance; declare reservations in the shared templates from measurements; make the section 5 owner check items non-blocking in readiness and `lab.py check` | W1-W6 | TSK-0002 | `test_lab_controller`; readiness and check on HOME; full suite; hardening |
| W8 | 3 | Retire the supabase LAB: delete `labs/supabase/`, its Guide, Runbook and Policy and its catalog rows; move the SMTP01 retirement sections into RUN-0106; remove the `vector` socket allowance so no LAB binds the Docker socket | W1-W7 | TSK-0003 | LAB suites; secret suites; catalog check; hardening; root render; document checks; full suite |

### Global Constraints

- **Paths.** A LAB entrypoint is exactly `labs/<name>/docker-compose.yml`.
  The manifest is exactly `labs/<name>/promotion.yaml`. Only `labs/README.md`
  and `labs/.env.example` stay at the `labs/` root.
- **Kinds.** `kind` is one of `add`, `replace-same`, `replace-substitute` or
  `undecided`. A manifest with kind `undecided` has no `target`.
- **Docker socket.** No LAB binds the Docker socket. The supabase `vector`
  exception went with the supabase LAB in W8.
- **Never touched.** No secret value is read or written, and `secrets/` is not
  edited. The owner applies `secrets/SENSITIVE_ENV_VARS.md.example`.
- **Moves.** Document moves keep `artifact_id` and `created`. Use `git mv` so
  history follows.
- **Profiles.** POL-0078 profile names, the `infra/` tier layout tests and the
  LAB isolation tests stay authoritative.
- **Readiness results.** A value the readiness check cannot measure is
  `NOT_RUN`, and a `NOT_RUN` criterion fails the report.

### Review Focus

1. **Relative paths after the move.** Moving a Compose file one folder deeper
   changes the base that relative paths resolve against. A missed path renders
   to a missing file, or to a path outside the repo. W2 adds
   `test_lab_bind_sources_resolve`.
2. **`LAB_SECRET_DIR` resolution.** `labs/.env.example` sets
   `LAB_SECRET_DIR="../secrets/labs"`, and Compose resolves that against the
   project directory. After the move the project directory is `labs/<name>/`,
   so the value must become `../../secrets/labs`. The same applies to every
   `${LAB_SECRET_DIR:-../secrets/labs}` default. W2 asserts the rendered
   secret paths start with `secrets/labs/<name>/`.
3. **A socket bind that only looks like the exception.** W1 wrote this for the
   supabase `vector` exception; since W8 every socket bind is refused. The
   check must still refuse:
   - a writable bind on `vector`;
   - the same bind on another supabase service;
   - a `.sock` source under another name.

   W1 tests all three.
4. **A running container with no limits.** One such container makes the
   resource criterion `NOT_RUN`, never `PASS`. W4 tests it.
5. **A replacement whose retired service is not running.** Its resources are
   subtracted only when its containers are running and counted, so they are
   never subtracted twice. W4 tests it.

---

### W1: `lab.py` layout, manifest and socket exception

**Files:**

- Modify: `scripts/operations/lab.py` (`lab_file`, `check`, `_sensitive_input`
  and `source_allowlist_problems`, plus a new `manifest_problems`)
- Test: `tests/validation/test_lab_controller.py`

**Interfaces:**

- Produces:
  - `lab_file(name: str) -> str`, which returns
    `labs/<name>/docker-compose.yml`. It raises
    `LabError("unknown LAB ...")` when that file is missing, and
    `LabError("<name>: flat labs/<name>.yml is retired; use labs/<name>/docker-compose.yml")`
    when only the flat file exists.
  - `load_manifest(name: str) -> dict`, which reads with
    `yaml.safe_load`. A missing file raises `LabError`.
  - `manifest_problems(name: str, manifest: dict, lab: dict, catalog_ids: set[str]) -> list[str]`.
  - `footprint()` gains
    `"services": {service: {"cpus": float, "memory": float}}`.

**Manifest schema.** These are the decided field shapes:

```yaml
kind: replace-same            # add | replace-same | replace-substitute | undecided
target:                       # absent when kind is undecided
  folder: infra/04-data/mng-db/valkey/
  profile: data
replaces:                     # replacement kinds only, non-empty
  - service: valkey
    compose_path: infra/04-data/mng-db/valkey/docker-compose.yml
    consumers: [infra/07-workflow/airflow/docker-compose.yml]
integrations:                 # list, may be empty
  - kind: gateway-route       # gateway-route | oidc-client | database-role | observability | openbao | network
    owner: infra/01-gateway/traefik/
secrets:                      # one entry per LAB secret file
  - row: LAB-001
    destination: secrets/data/valkey/password.txt
documents:
  guide: docs/05.operations/guides/15-labs/0022-valkey-cluster.md
  runbook: docs/05.operations/runbooks/15-labs/0022-valkey-cluster.md
  guide_target: docs/05.operations/guides/05-databases-and-storage/
  runbook_target: docs/05.operations/runbooks/05-databases-and-storage/
resources:
  services: {valkey-node-1: {cpus: 0.5, memory_mib: 512}}
  disk_gib: {data: 5, images: 1}
host: {docker: "29.0", compose: "5.0", kernel_features: [cgroup2]}   # optional
```

**`manifest_problems` reports each of these as a string containing the quoted
phrase:**

- unknown kind (`"unknown kind"`);
- `target` present on `undecided`, or missing on any other kind
  (`"target"`);
- a `target.folder` that does not match `^infra/\d\d-[a-z0-9-]+/.+/$`
  (`"outside infra/<tier>/"`);
- empty `replaces` on a replacement kind (`"replaces"`);
- an unknown integration kind (`"integration"`);
- a `secrets[].row` not in `catalog_ids` (`"no catalog row"`);
- a `resources.services` entry whose name or limits differ from
  `lab["services"]` (`"disagrees with rendered limits"`);
- a `documents` path that does not exist (`"documents"`).

`check()` appends `manifest_problems` for each selected LAB.

- [ ] **Step 1: Write the failing tests.** All of them go in
  `test_lab_controller.py`:
  - `test_lab_file_resolves_folder_entrypoint`;
  - `test_lab_file_refuses_flat_file`, which expects the "flat ... is retired"
    message;
  - `test_manifest_unknown_kind`, `test_manifest_undecided_with_target` and
    `test_manifest_target_outside_infra`;
  - `test_manifest_replacement_needs_replaces`;
  - `test_manifest_secret_without_catalog_row`;
  - `test_manifest_resources_disagree_with_render`. It renders a service with
    `cpus: 1` and has the manifest declare `0.5`;
  - `test_manifest_valid_passes`, which expects `== []`;
  - `test_socket_allowed_only_for_supabase_vector_read_only`, with four cases:
    1. supabase `vector` with `read_only: true` is allowed;
    2. the same bind with `read_only: false` is refused;
    3. a supabase service `kong` with the read-only bind is refused;
    4. `vector` with source `/run/user/1000/docker.sock` is refused.

  Build fixtures with the module's existing helpers
  (`footprint` over a dict model, `tmp_path` repos).
- [ ] **Step 2: Run them and confirm they fail.**
  `pytest tests/validation/test_lab_controller.py -k "lab_file or manifest or socket" -v`.
  Expected: FAIL, because `load_manifest`, `manifest_problems` and folder
  resolution are not defined yet.
- [ ] **Step 3: Implement.**
  - **Socket exception.** It is decided in `source_allowlist_problems`: when
    `name == "supabase"`, the service is `vector`, the source and target are
    both `/var/run/docker.sock` and the bind is read-only, the source is
    allowed. Anything else stays refused.
  - **Catalog ids.** They come from
    `infra/03-security/openbao/secret-catalog.json`.
- [ ] **Step 4: Run the whole controller module.**
  `pytest tests/validation/test_lab_controller.py -v`. Expected: all pass.
  Until W2 lands, existing tests that call `lab_file` on real LABs may need
  their fixtures moved to `labs/<name>/docker-compose.yml`.
- [ ] **Step 5: Commit.**
  `feat: Resolve LAB folders and validate promotion manifests`.

### W2: Standard layout for the 15 LABs

**Files:**

- Move with `git mv` to `labs/<name>/docker-compose.yml`: `cassandra`,
  `couchdb`, `dbt`, `jupyterlab`, `kafka-cluster`, `lakehouse`, `locust`,
  `mongodb`, `opensearch-cluster`, `postgresql-ha`, `sonarqube`, `stalwart`,
  `supabase`, `superset` and `valkey-cluster`.
- **Guides.** For a LAB with no `labs/<name>/README.md`, move `labs/<name>.md`
  to that path; this applies to cassandra, couchdb, kafka-cluster, mongodb,
  opensearch-cluster, postgresql-ha and valkey-cluster. Where a README
  already exists, merge the `.md` content into it and delete the `.md`.
- **Root helpers.** `labs/couchdb-cluster-init.sh` moves to `labs/couchdb/`,
  and `labs/opensearch-cluster-dashboards.config` moves to
  `labs/opensearch-cluster/`.
- **Dashboards.**
  - Each `labs/dashboards/<name>.json` moves to
    `labs/<name>/dashboards/<name>.json`.
  - `etcd-cluster.json` and `haproxy-overview.json` move to
    `labs/postgresql-ha/dashboards/`.
  - `labs/dashboards/README.md` content goes into each owner README, and the
    file is deleted.
- **Create.** One `labs/<name>/promotion.yaml` per LAB, 15 in all.
- **Modify:**
  - every relative path inside the moved Compose files;
  - `labs/.env.example`, setting `LAB_SECRET_DIR="../../secrets/labs"`;
  - `labs/README.md`;
  - active references, found with
    `git grep -n 'labs/[a-z-]*\.yml\|labs/dashboards/' -- ':!docs/90.references' ':!docs/98.archive'`.
    Terminal Tasks (`status: "completed"` or `"cancelled"`) keep their bodies.
- **Test:** add `tests/validation/test_lab_layout.py`.

**Manifest content decisions.** These were made by the agent and are recorded
in the Task:

- `opensearch-cluster` and `kafka-cluster` are `replace-same`, targeting
  `infra/04-data/opensearch/` and `infra/05-messaging/kafka/`.
- `valkey-cluster` and `postgresql-ha` are `undecided`: HOME runs two single
  nodes of each (`infra/04-data/mng-db/` and `infra/04-data/dev-db/`), so the
  owner picks which one a cluster would replace.
- The other 11 are `undecided` until the owner names a target.
- `resources` copies the rendered limits.
- `secrets` lists every `LAB-*` or `SUPA-*` row whose `source_path` or
  consumer is the LAB.

- [ ] **Step 1: Write the failing tests.** All of them go in
  `test_lab_layout.py`:
  - `test_labs_root_holds_only_readme_and_env_example`. Every other entry
    under `labs/` is a directory.
  - `test_every_lab_has_entrypoint_readme_manifest`.
  - `test_every_manifest_is_valid`. It calls `manifest_problems` against
    `footprint(render(...))` for each LAB and expects `== []`.
  - `test_lab_bind_sources_resolve`. Every rendered bind source is under
    `LAB_DATA_DIR`, under the LAB secret root, a `LAB_*` operator path, or an
    existing tracked file. This is Review Focus 1.
  - `test_lab_secret_paths_use_lab_root`. Every rendered `secrets.*.file`
    starts with `<repo>/secrets/labs/<name>/`. This is Review Focus 2, and the
    supabase case passes only after W3.

  Render with
  `docker compose --env-file labs/.env.example -f labs/<name>/docker-compose.yml config --format json --no-env-resolution`.
  Use a temporary absolute `LAB_DATA_DIR`, as the existing render tests do.
  Skip with a reason when `docker` is missing.
- [ ] **Step 2: Run them and confirm they fail.** `pytest tests/validation/test_lab_layout.py -v`.
  Expected: FAIL, because the flat files and root helpers are still present.
- [ ] **Step 3: Move and fix the files.** Do one LAB per commit, in the order
  of the list above.
  1. Run `git mv` for the entrypoint, guide, helpers and dashboards.
  2. Rewrite the relative paths. `./x` keeps working when `x` moved with the
     file. A `../` path gains one more `../`.
  3. Write the manifest.
  4. Run `docker compose ... config -q`.

  After all 15, update the references and `labs/README.md`, then run
  `graphify update .`.
- [ ] **Step 4: Run the checks.**
  - `pytest tests/validation/test_lab_layout.py tests/validation/test_lab_controller.py -v`.
    Expected: all pass except `test_lab_secret_paths_use_lab_root[supabase]`,
    which is marked `xfail(strict=True)` with reason "W3" and removed in W3.
  - The whole unit suite, then `scripts/hardening/check-all-hardening.sh`.
    Expected: no new failure against the `main` baseline.
- [ ] **Step 5: Commit** after each LAB, then commit the references:
  `refactor: Move the <name> LAB into labs/<name>/`.

### W3: supabase on LAB secret copies

**Files:**

- Modify: `labs/supabase/docker-compose.yml`. Point the eleven secret
  `file:` entries at `${LAB_SECRET_DIR:-../../secrets/labs}/supabase/<same
  file name>`. The SMTP file is `smtp_password.txt`, and the mng-pg password
  is `supabase_db_password.txt`.
- Modify: `infra/03-security/openbao/secret-catalog.json`:
  - **SUPA-002..011 and AI-001.** Set `source_path` to
    `secrets/labs/supabase/<file>` and consumers to
    `labs/supabase/docker-compose.yml`.
  - **COMM-002.** Remove the `labs/supabase.yml` consumer.
  - **LAB-037 (new).** Model it on LAB-036: `source_path`
    `secrets/labs/supabase/smtp_password.txt`, scope `lab`, classification
    `lab_excluded`, purpose "Supabase LAB SMTP 비밀번호 (HOME COMM-002 값
    복사본)".
- Modify: `tests/validation/test_secret_metadata_sync.py`. Delete
  `SUPABASE_CANONICAL_SECRET_PATHS` and the `shared_supabase` branch; supabase
  then follows the general LAB rule.
- Modify: `tests/validation/test_supabase_smtp_rehearsal.py`, the supabase
  Guide `docs/05.operations/guides/15-labs/0029-supabase.md`, and its Runbook.
- Task only: the owner checklist and the prepared registry rows.

**Owner checklist.** The agent writes it in the Task and does not run it:

1. Copy `secrets/communication/smtp/smtp_password.txt` to
   `secrets/labs/supabase/smtp_password.txt`.
2. Copy `secrets/db/mng-pg/supabase_password.txt` to
   `secrets/labs/supabase/supabase_db_password.txt`. HOME mng-pg keeps its
   copy because HOME provisions that role.
3. Move the nine `secrets/data/supabase/*.txt` files to
   `secrets/labs/supabase/`.
4. Apply the prepared rows to `secrets/SENSITIVE_ENV_VARS.md.example`.

The copy-or-move split for steps 2 and 3 is confirmed by
`git grep supabase_password -- infra scripts` during W3. If mng-pg does not
use the password, step 2 becomes a move.

- [ ] **Step 1: Make the tests fail.**
  - Remove the W2 `xfail` on `test_lab_secret_paths_use_lab_root[supabase]`.
  - Add `test_supabase_reads_no_home_secret` to `test_secret_metadata_sync.py`.
    No rendered supabase secret path is outside `secrets/labs/supabase/`.
- [ ] **Step 2: Run them and confirm they fail.**
  `pytest tests/validation/test_lab_layout.py tests/validation/test_secret_metadata_sync.py -k supabase -v`.
  Expected: FAIL on the eleven HOME paths.
- [ ] **Step 3: Implement.** Apply the Compose, catalog, test and document
  edits listed above.
- [ ] **Step 4: Run the checks.** Run
  `pytest tests/validation/test_secret_metadata_sync.py tests/validation/test_supabase_smtp_rehearsal.py tests/validation/test_lab_layout.py tests/lib/ops -v`.
  Expected: PASS. Then run
  `lab.py check supabase --env-file labs/.env.example` in render-only form.
  Expected: no secret or socket problem. A missing secret file is the owner's
  step 1-3 and is recorded as `NOT_RUN` until it is done.
- [ ] **Step 5: Commit.** `fix: Move supabase onto LAB secret copies`.

### W4: Promotion readiness check

**Files:**

- Modify: `scripts/operations/lab.py`. Add a `readiness` subcommand and the
  `PROMOTION_RESERVE` constant.
- Test: `tests/validation/test_lab_controller.py`.

**Interfaces:**

- Consumes:
  - `footprint`, `render`, `root_footprint`, `running_containers`,
    `docker_root` and `collisions` from the existing code;
  - `load_manifest` and `manifest_problems` from W1.
- Produces:
  - `PROMOTION_RESERVE = {"cpus": 2.0, "memory_mib": 4096, "disk_percent": 10}`;
  - `readiness(name: str, manifest: dict, lab: dict, host: dict, running: list[dict], root: dict) -> dict`,
    a pure function;
  - `measure_host(docker: str, data_root: str) -> dict`;
  - CLI `lab.py readiness <name> [--report PATH]`, which prints the report
    JSON and exits 0 only when every criterion is `PASS`.

The first reserve value is proposed here. The host was measured on
2026-11-05 at 12 CPUs, 32020 MiB of memory, 123 GiB free of 249 GiB, Docker
29.9.2 and Compose 5.6.1. The reserve of 2 CPUs and 4096 MiB is about 1/6 of
the CPUs and 1/8 of the memory; disk keeps 10% of each filesystem free.

**Report shape:**

```json
{"lab": "...", "kind": "...", "result": "PASS|FAIL|NOT_RUN",
 "criteria": {"tier": {...}, "composition": {...}, "linux": {...}, "docker": {...}, "resources": {...}}}
```

Each criterion is
`{"result": "PASS|FAIL|NOT_RUN", "values": {<name>: {"value": ..., "source": "<command or file>"}}, "problems": [str]}`.
The overall result is `PASS` only when all five criteria pass. Otherwise it
is `FAIL` when any criterion fails, and `NOT_RUN` in the remaining cases.

**Criterion rules:**

- **tier.** Kind is not `undecided`. `target.folder` matches the W1 pattern and its tier folder exists. The service folder is absent, or is listed in `replaces[].compose_path`.
- **composition.** `collisions()` against the root and running containers finds no problem besides the candidate's own retired services. `target.profile` is in the POL-0078 vocabulary; reuse the reader `tests/validation` already uses. Every `integrations[].owner` path exists.
- **linux.** `host["cgroup_version"] == "2"` when any limit is declared. Each rendered numeric `user` is valid. Each `host.kernel_features` entry other than `cgroup2` is `NOT_RUN`.
- **docker.** Docker and Compose versions are at least `host.docker` and `host.compose`, compared as dotted ints. Every rendered network and volume driver is `local`, `bridge` or `overlay`. Docker's data root is absolute.
- **resources.** The values come from `docker info` (`NCPU`, `MemTotal`, `DockerRootDir`), `docker compose version --short`, and `shutil.disk_usage` on DEFAULT_DATA_DIR and the Docker root. The budget is the measured value minus the reserve. `running` is the sum of the limits of running containers, minus those in projects or containers named by `replaces` and actually running (Review Focus 5), plus the candidate. `running` must not exceed the budget, and free disk minus the reserve percentage must be at least `disk_gib`. Any running container with a zero limit makes this criterion `NOT_RUN` and lists that container (Review Focus 4).

- [ ] **Step 1: Write the failing tests.** Each test calls the pure
  `readiness()` with dict fixtures:
  - `test_readiness_passes_within_budget`;
  - `test_readiness_fails_over_cpu_budget`, where the reserve leaves 10 CPUs
    and running plus candidate needs 10.5;
  - `test_readiness_unlimited_container_is_not_run`, which expects
    resources `NOT_RUN` and the overall result `NOT_RUN`;
  - `test_readiness_replacement_subtracts_only_running_retired`. It covers two
    cases: the retired service running is subtracted once, and the retired
    service stopped subtracts nothing;
  - `test_readiness_undecided_fails_tier`;
  - `test_readiness_unknown_profile_fails_composition`;
  - `test_readiness_old_docker_fails`;
  - `test_readiness_unmeasured_value_is_not_run`, where `host` lacks `NCPU`;
  - `test_reserve_matches_policy`. The reserve table in the W5 policy document
    equals `PROMOTION_RESERVE`. Mark it `xfail(strict=True)` until W5.
- [ ] **Step 2: Run them and confirm they fail.**
  `pytest tests/validation/test_lab_controller.py -k readiness -v`.
  Expected: FAIL, because `readiness` is not defined yet.
- [ ] **Step 3: Implement.** Write `readiness`, `measure_host` and the
  subcommand. `measure_host` uses one `docker info --format '{{json .}}'` call
  and records each command as the value `source`.
- [ ] **Step 4: Run the checks.**
  - `pytest tests/validation/test_lab_controller.py -v`. Expected: PASS.
  - A read-only run on HOME:
    `python3 scripts/operations/lab.py readiness valkey-cluster --report <scratchpad>/readiness-valkey-cluster.json`.
    It changes nothing. Its JSON goes into the Task as evidence, whatever the
    result.
- [ ] **Step 5: Commit.** `feat: Add the LAB promotion readiness check`.

### W5: Promotion operations documents

**Files:**

- **Create subject OPS-0107, `lab-promotion`.**
  - `docs/05.operations/policies/15-labs/0107-lab-promotion.md` holds the
    layout, the manifest fields, the secret rules, the destination rules
    table (Spec section 4) and a two-column reserve table (`Resource`,
    `Reserve`) with the rows CPUs 2, Memory MiB 4096 and Disk percent 10.

  - `docs/05.operations/runbooks/15-labs/0107-lab-promotion.md` holds the
    readiness check run and three procedures: `add`, `replace-same` and
    `replace-substitute`. Each replacement procedure has the consumer
    inventory, data migration (export, import, verify), cutover, rollback and
    retirement sections. `replace-substitute` adds the format mapping.
- **Create OPS-0108, `kafka-cluster`.** A Guide and a Runbook in `15-labs`,
  built from the `labs/kafka-cluster/README.md` content.
- **Create OPS-0109, `opensearch-cluster`.** The same, from
  `labs/opensearch-cluster/README.md`.
- **Modify:**
  - the `15-labs` READMEs for guides, runbooks and policies;
  - the operations catalog inputs that `check-operations-catalog.py` reads;
  - `docs/99.templates/registry.json`, where `operations-subject` `high_water`
    becomes 109 and `next_number` becomes 110;
  - the manifests' `documents` for kafka-cluster and opensearch-cluster.
- Add a Kafka or OpenSearch policy only if `check-operations-catalog.py`
  requires one.

- [ ] **Step 1: Make the check fail.** Remove the W4 `xfail` on
  `test_reserve_matches_policy`. Run it and confirm it fails.
- [ ] **Step 2: Write the documents.** Use the Stage 99 operations templates
  and the Korean or English language their profile sets.
- [ ] **Step 3: Run the checks.**
  - `check-operations-catalog.py`;
  - `check-document-metadata.py --mode check-changed`;
  - `check-document-links.py --mode all`;
  - `pytest -k reserve_matches_policy`.

  Expected: PASS.
- [ ] **Step 4: Commit.** `docs: Add LAB promotion policy, runbook and cluster LAB documents`.

### W6: Evidence

- [ ] **Step 1: Run the Verification Plan.** Record each result in the Task
  as an Evidence row with the revision it examined.
- [ ] **Step 2: Open the pull request.** Wait for hosted CI and record its
  result.
- [ ] **Step 3: Leave criteria pending.** Set each Criterion Acceptance row to
  `pending`; the owner accepts them.

### W7: Reservations and owner check items

Spec 0.3.0 (owner decisions, 2026-11-06) changes the resource rule from summed
limits to summed reservations plus an external-workload allowance. It also
turns two section 5 sub-checks into owner check items.

**Files:**

- Modify `infra/common-optimizations.yml`. Add a reservation next to each
  `x-resource-*` anchor.
- Modify every HOME or LAB service that sets its own `cpus` or `mem_limit`
  outside the anchors. Find them with the root render plus the 15 LAB renders.
- Modify `scripts/operations/lab.py`:
  - `footprint`;
  - `running_containers`;
  - `budget`;
  - `readiness`;
  - `PROMOTION_EXTERNAL_ALLOWANCE`.
- Modify POL-0107, RUN-0107 and the Task.
- Test: `tests/validation/test_lab_controller.py`.

**Decided values:**

- **Reservation sizing.** For each anchor, take at least 3 `docker stats`
  samples of its running members, keep the peak, and multiply it by 1.5.
  - Round CPU up to 0.05 and memory up to 32 MiB.
  - The result never exceeds the anchor's limit.
  - The minimum is 0.05 CPU and 32 MiB.
  - The Task records the samples.
- **Declaration form.** `deploy.resources.reservations.cpus` and
  `.memory`.
  - Docker does not enforce a CPU reservation; it is a declared budget.
  - The memory reservation is a soft limit.
  - Limits keep their current short form.
- **External-workload allowance.** The first value is
  `PROMOTION_EXTERNAL_ALLOWANCE = {"cpus": 2.0, "memory_mib": 6144}`. It is
  based on k3d measured at about 1.0 CPU and 4.1 GiB on 2026-11-06. POL-0107
  carries the same table, and a test checks that the two match.
- **Summation.**
  - A running container counts with the reservation of its rendered service,
    looked up by the `com.docker.compose.project` and `.service` labels from
    the root or LAB render.
  - A container outside those projects counts only through the allowance.
  - A Compose service without a reservation gives resources `NOT_RUN`.
  - Limits stay required, and `reservation > limit` fails.
- **Owner check items.** Groups and file modes, and profile and consumer
  clashes, are reported with result `OWNER_JUDGMENT` and do not block PASS.
  - The tier `function_fit` entry uses the same value.
  - Readiness PASS still needs every measured criterion to pass.
- **`lab.py check`.** `budget` uses the same reservation sum and the same
  allowance against `LAB_HOST_BUDGET_*`.

**Tests (RED first):**

- `test_readiness_sums_reservations_not_limits`;
- `test_readiness_external_allowance_counts_once`;
- `test_readiness_service_without_reservation_is_not_run`;
- `test_readiness_reservation_above_limit_fails`;
- `test_owner_check_items_do_not_block_pass`;
- `test_check_budget_uses_reservations`;
- `test_allowance_matches_policy`;
- `test_shared_templates_declare_reservations`, which checks that every
  `x-resource-*` anchor has a reservation no larger than its limit.

**Verification:**

- Run the LAB suites and the full suite.
- Run hardening, including `common-optimizations` validation.
- Run a root render.
- Run read-only HOME readiness for valkey-cluster and postgresql-ha.
- Run `lab.py check valkey-cluster` with the owner's `labs/.env`.

The HOME services pick up the new reservations only when they are recreated,
in an owner window. This work unit restarts nothing.

### W8: Retire the supabase LAB

Spec 0.4.0 (owner decision, 2026-11-06) removes the supabase LAB. No LAB is
promoted.

**Files:**

- Delete `labs/supabase/` and `docs/05.operations/{guides,runbooks,policies}/15-labs/0029-supabase.md`.
  Fix every inbound link and README index row; leave no redirect.
- Move the RUN-0029 sections "SMTP 전환 확인과 중복 퇴역" and "SMTP01의 root·lock·증거
  계약" into RUN-0106, which already owns the COMM-003 alias probes and the
  secret-structure SMTP checks.
- Remove the supabase rows from `infra/03-security/openbao/secret-catalog.json`
  and `infra/secret-file-support.json`; prepare the matching
  `secrets/SENSITIVE_ENV_VARS.md.example` edit for the owner.
- `scripts/operations/lab.py`: remove `_socket_exception`.
- `scripts/lib/ops/smtp_contract.py`: an Auth alias is no longer required once
  no LAB source exists.
- Current inventories: `labs/README.md`, `labs/.env.example`,
  `infra/tech-stack.versions.json`, the update ledger's current fields,
  `scripts/manifest.yaml`, `scripts/hardening/check-all-hardening.sh`,
  `docs/99.templates/registry.json`, POL-0001, POL-0006, POL-0078, POL-0107,
  RUN-0107, GDE-0041 and AD-0004, AD-0019, AD-0026.
- Tests that read the deleted files.

**Verification:** the LAB suites, the secret suites, the catalog check,
hardening, a root render, the document checks and the full suite, recorded in
TSK-0003.

## Verification Plan

**Local checks:**

- `docker compose config -q` for the root and for each
  `labs/<name>/docker-compose.yml`;
- the full unit suite under the py312 controller venv;
- `scripts/hardening/check-all-hardening.sh`;
- `check-document-metadata.py` in `check-changed` and `check-active` modes;
- `check-document-links.py --mode all`;
- `check-document-corpus-lifecycle.py`;
- `check-operations-catalog.py`;
- `check-script-manifest.py`.

**The readiness run.** One read-only `lab.py readiness` run on HOME.

**Known gap.** The local full CI gate stays `BLOCKED`, because it needs
Python 3.14.8 with memfd sealing. The Task records that, and hosted CI is the
gate.

## Risks and Recovery

### Risks and Rollback

| Risk | Handling |
| --- | --- |
| A missed relative path breaks a LAB render | `test_lab_bind_sources_resolve` |
| The large reference rename touches terminal or Stage 90 records | W2 excludes them; the link checker decides any residue |
| The proposed reserve is too small or too large | It is one policy value plus one constant, changed together |

**Rollback.** Revert the branch. No runtime, data or secret state changes.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-lab-promotion-contract.md)
- [supabase LAB retirement Task](tasks/tsk-0003-retire-supabase-lab.md)
- [Analytics LAB migration Plan](../0262-analytics-labs-migration/plan.md)
