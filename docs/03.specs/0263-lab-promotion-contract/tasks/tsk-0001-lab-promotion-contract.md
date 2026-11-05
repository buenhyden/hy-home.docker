---
title: "LAB Promotion Contract Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-05"
layer: "specs"
artifact_id: "SPEC-0263-TSK-0001"
parent_ids:
- "SPEC-0263-PLAN-0001"
created: "2026-11-05"
---

# LAB Promotion Contract Task

## Overview

### Objective

Carry out the six work units of the Plan:

- **Layout.** Bring the 15 LABs into the `labs/<name>/` layout, each with a
  promotion manifest.
- **supabase.** Move it onto LAB secret copies.
- **Readiness.** Add the promotion readiness check.
- **Documents.** Write the promotion operations documents.

## Inputs and Authorization

On 2026-11-05 the owner asked that supabase move into the LAB structure and
that LABs get a structure and rules for promotion into `infra/`. The owner
answered the three open questions recorded in the Spec Background (host
budget, supabase secret copies, the read-only `vector` socket) and approved
SPEC-0263 in this session.

**Earlier permission:** the owner allowed reading and editing the secrets
registry file for this work. The agent's permission settings still deny
`secrets/`, so the owner applies the registry edits that W3 prepares.

**This Task does not:**

- start any container;
- promote any LAB;
- read or write any secret value.

## Work Log

### Current contract decision

The owner approved SPEC-0263 on 2026-11-05. The Plan waits for the owner's
review.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0263 | draft | approved | #current-contract-decision |

### Decisions

These are agent calls, made in the Plan for the owner to check:

- **Manifest kinds.** `opensearch-cluster` and `kafka-cluster` are
  `replace-same`. The agent left `valkey-cluster` and `postgresql-ha` as
  `undecided`, because HOME runs both an `mng-db` and a `dev-db` node of
  each; owner decision A below settles them. The other 11 are `undecided`.
- **Reserve.** The first reserve is 2 CPUs, 4096 MiB of memory and 10% of
  each filesystem kept free. The host measured on 2026-11-05 has 12 CPUs and
  32020 MiB. Owner decision C below approves it.
- **New operations subjects.**
  - OPS-0107 is `lab-promotion`, with a policy and a runbook.
  - OPS-0108 is `kafka-cluster`.
  - OPS-0109 is `opensearch-cluster`.
- **Secret names across projects.** The tests no longer require a LAB
  secret name to differ from a root secret name. Each LAB is its own Compose
  project, and path isolation keeps each LAB on `secrets/labs/<name>/`, so the
  names cannot reach each other's files. This waits for the owner's
  confirmation.
- **The readiness check.** It is a `lab.py readiness` subcommand, not a new
  script.
- **LAB secret row IDs (deliberate deviation from Spec section 3).** The
  Spec says each LAB copy gets a `LAB-*` row. SUPA-002 to SUPA-011 and
  AI-001 keep their IDs and carry scope `lab` instead, because catalog IDs
  are never renumbered.
- **Spec section 5 narrowing (controller ruling, awaiting owner
  acceptance).** Readiness does not measure three section 5 sub-checks. Each
  is shown in the report as `NOT_RUN`:
  - tier "matches the service function" (`tier.values.function_fit`) is an
    owner-judgment item and does not block `PASS`;
  - linux "groups and file modes" (`linux.values.groups_and_file_modes`)
    keeps linux at `NOT_RUN`;
  - composition "profiles or consumers" clashes
    (`composition.values.profile_and_consumer_clashes`) keeps composition at
    `NOT_RUN`.

  No candidate gets an overall `PASS` until the owner accepts this narrowing
  or the two sub-checks are measured. POL-0107 and RUN-0107 record it.

The owner decided these on 2026-11-05:

- **A.** `valkey-cluster` and `postgresql-ha` are `replace-same` against
  the `dev-db` single nodes. The targets are `infra/04-data/dev-db/valkey/`
  and `infra/04-data/dev-db/pg/`, both with the `dev-data` profile that
  `dev-valkey` and `dev-pg` carry. The retired services are `dev-valkey` and
  `dev-valkey-exporter`, and `dev-pg`, `dev-pg-monitor-provision` and
  `dev-pg-exporter`. Both live in `infra/04-data/dev-db/docker-compose.yml`.
  The consumers listed in each manifest come from `git grep`.
- **B.** The other 11 LABs stay `undecided`.
- **Ruling on decision A (controller).** `dev-platform-provision` and
  `dev-perf-provision` are dev-pg's own provisioning jobs. Their work moves
  to the cluster, so `postgresql-ha` retires them with `dev-pg`.
- **C.** The reserve is approved as
  `PROMOTION_RESERVE = {"cpus": 2.0, "memory_mib": 4096, "disk_percent": 10}`.

### W3: supabase on LAB secret copies

**Owner checklist.**

| Step | Action | Status |
| --- | --- | --- |
| 1 | Copy the HOME SMTP password into `secrets/labs/supabase/smtp_password.txt` | DONE by the owner on 2026-11-05 |
| 2 | Place `secrets/labs/supabase/supabase_db_password.txt` from the mng-pg file | DONE by the owner on 2026-11-05 |
| 3 | Move the nine `secrets/data/supabase/*.txt` files to `secrets/labs/supabase/` | DONE by the owner on 2026-11-05 |
| 4 | Apply the prepared rows below to `secrets/SENSITIVE_ENV_VARS.md.example` | DONE by the owner on 2026-11-05, commit `8ad19acc5` |
| 5 | Run the private-registry sync below | DONE by the owner on 2026-11-05, without prune |

The controller checked steps 1 to 3 against an owner-run `find`. It saw the
11 file names in `secrets/labs/supabase/` and no values. `secrets/data/supabase/`
is gone, and `secrets/communication/smtp/` is unchanged for HOME.
`git grep supabase_password -- infra scripts` finds only the catalog row, so
HOME mng-pg does not provision the supabase role. Step 2 is therefore a move
in effect. If `secrets/db/mng-pg/supabase_password.txt` still exists, it has
no catalog row and no consumer, and the owner may remove it.

**Catalog.** In `infra/03-security/openbao/secret-catalog.json`:

- SUPA-002, SUPA-004 to SUPA-011 and AI-001 now point at
  `secrets/labs/supabase/<file>`, recorded on 2026-11-05.
- COMM-002 loses its `labs/supabase/docker-compose.yml` consumer.
- LAB-037 is new. It holds the supabase SMTP copy and is modeled on LAB-036.
- COMM-006, AI-007, AUTO-020, PG-023 and PG-028 are retired. Their files were
  already moved into LAB folders. Each is now a `source_retired` alias of the
  LAB row that holds its value: LAB-036, LAB-034, LAB-032, LAB-029 and LAB-031.
  This is the same form as the COMM-003 to COMM-002 alias. No ID is reused or
  renumbered.

**Prepared registry rows.** The owner applies these to
`secrets/SENSITIVE_ENV_VARS.md.example` in the existing row style. Bold and
backticks are ignored by the parser.

- In these ten rows set the path cell to `secrets/labs/supabase/<file>` and
  the date cell to `2026-11-05`. Keep every other cell.

  | Row | File |
  | --- | --- |
  | SUPA-002 | `supabase_db_password.txt` |
  | SUPA-004 | `supabase_dashboard_password.txt` |
  | SUPA-005 | `supabase_secret_key_base.txt` |
  | SUPA-006 | `supabase_pg_meta_crypto_key.txt` |
  | SUPA-007 | `supabase_logflare_private_token.txt` |
  | SUPA-008 | `supabase_vault_enc_key.txt` |
  | SUPA-009 | `supabase_service_key.txt` |
  | SUPA-010 | `supabase_jwt_secret.txt` |
  | SUPA-011 | `supabase_anon_key.txt` |
  | AI-001 | `supabase_openai_api_key.txt` |

- Add this row:

  ```text
  | LAB-037 | X | PW | (비어있음) | - | secrets/labs/supabase/smtp_password.txt | 2026-11-05 | Supabase LAB SMTP 비밀번호 (HOME COMM-002 값 복사본) |
  ```

- Delete the COMM-006, AI-007, AUTO-020, PG-023 and PG-028 rows.
- Append these rows, in this order, after `| COMM-003 | COMM-002 |` in the
  `| Retired ID | Canonical ID |` table. The order must match the catalog
  `aliases` list.

  ```text
  | COMM-006 | LAB-036 |
  | AI-007 | LAB-034 |
  | AUTO-020 | LAB-032 |
  | PG-023 | LAB-029 |
  | PG-028 | LAB-031 |
  ```

**Owner sync sequence.** These commands need a `python3` on `PATH` that has
`jsonschema` and `referencing`, for example the controller venv. Without
them every metadata mode prints `METADATA rejected` and exits 2.

The owner ran this sequence on 2026-11-05, as reported to the controller:

1. `python3 scripts/operations/secret-catalog.py --root "$PWD" check`.
   `--root` is a top-level option and must be absolute, so `.` does not
   work. After the hand-applied registry (`8ad19acc5`), `load_catalog`
   succeeded.
2. `bash scripts/operations/gen-secrets.sh --sync-metadata-check` reported
   `files_changed=3`.
3. `bash scripts/operations/gen-secrets.sh --sync-metadata` applied them, and
   a second `--sync-metadata-check` reported `files_changed=0`.
4. `--sync-metadata-prune` was rejected, because the private registry still
   holds COMM-003, and only the SMTP01 retirement removes it. COMM-003 and
   the five retired rows stay in the private registry as private-only rows.
   Their values stay in the LAB copies.

**Root `secrets/` overlap.** E6 showed every LAB secret copy overlapping
root's read-only restic bind of `secrets/`. This is not a W2 or W3
regression. A check of stalwart at `6f4eb08dc` with the tracked
`labs/.env.example` gives the same overlap. SPEC-0262 E20 used the synthetic
`compose_controls.LAB_INPUTS`, which set `LAB_SECRET_DIR` to
`/nonexistent/lab-secrets`, so it never met the in-repo copies.
`root_footprint` turns every HOME sensitive input into HOME state, so the
read-only bind looked like owned state. `lab.py` now records the writable
binds as `bound_state` before that step. A read-only root bind of
`secrets/` owns no read-only path of the checked LAB under its own
`secrets/labs/<name>/`. A writable root bind, a HOME secret, another LAB's
copy, the whole `secrets/labs` tree and a writable LAB bind still clash. The
LAB allowlist also takes secrets only from `<LAB_SECRET_DIR>/<name>/`, so no
LAB reads another LAB's copy.

**SMTP retirement path.** `scripts/lib/ops/smtp_public_source.py` now
requires the supabase LAB to read its LAB-037 copy and refuses any LAB file
that names the HOME SMTP path. Its fixed `extends` file is now
`../../infra/common-optimizations.yml`, which W2's move required.
`retire_materials.py`, `secret_structure.py` and `smtp_contract.py` only
handle the COMM-003 duplicate and needed no change. `gen-secrets.sh` now
accepts any well-formed retired-row alias, not only COMM-003.

### W4: Promotion readiness check

`lab.py readiness <name> [--report PATH]` reads HOME state only: the LAB and
root renders, `docker info`, `docker inspect` and disk usage. It prints the
section 5 report and exits 0 only when all five criteria are `PASS`.
`test_reserve_matches_policy` was an expected failure until W5 added the
policy reserve table. Bad manifest, catalog or `disk_gib` input raises
`LabError` with exit 2.

The check makes these calls:

- **Manifest paths.** `documents.*`, `integrations[].owner`,
  `replaces[].compose_path` and `target.folder` must be repo-relative paths
  that resolve inside the repository, with no absolute path and no `..`.
- **Retired services.** Only `replace-same` and `replace-substitute`
  retire anything. Each retired service must be declared in an existing
  `compose_path` that the root `docker-compose.yml` includes, and must be
  rendered in root. Otherwise composition fails and nothing is retired.
- **Tier.** An existing target folder counts as a replacement only when the
  retired services own it exclusively. All three of these must hold:
  - it holds a verified retired Compose file, or a retired service's build
    context or bind source in the root render lies inside it;
  - no kept service's build context or bind source lies inside it;
  - every service that a `*compose*.y*ml` file inside the folder declares
    is retired.

  Tier also fails when such a file cannot be read, when the folder holds a
  symlinked directory (the glob does not follow one), or when the folder
  resolves outside the repository. `dev-valkey` binds files under
  `dev-db/valkey/`, and nothing else uses that folder, so it qualifies.
  `dev-db/` does not, because it still declares `dev-pg`. The tier criterion
  also fails on any `manifest_problems` result, and `manifest_problems`
  refuses a zero or missing service limit.
- **Composition.** The retired services' own containers and ports are
  removed from the root footprint and the running list before
  `collisions()`. A port or container name stays when a kept service also
  declares it. Networks and data paths stay, because retiring a service
  frees neither.
- **Profiles.** The POL-0078 vocabulary comes from
  `operations_catalog._conftest_profile_names`, the reader the profile gates
  use.
- **Resources.** Limits are compared in bytes and reported in MiB. A retired
  container is subtracted only when it is running. A sum over budget stays
  `FAIL` even when some container has no limit, because the known lower
  bound already exceeds the budget; `NOT_RUN` applies only when the
  measured sum fits. A candidate service without a CPU or memory limit also
  makes resources `NOT_RUN`.

**HOME run, 2026-11-05.**

1. As instructed, `lab.py --env-file labs/.env readiness valkey-cluster`
   exited 1 before writing a report. Compose said `required variable
   LAB_DATA_DIR is missing a value`. `lab.py --env-file labs/.env check
   valkey-cluster` fails the same way, so `labs/.env` still gives Compose no
   `LAB_DATA_DIR`. The agent does not read that file. This waits for the
   owner.
2. A supplementary run used the same flags with `LAB_DATA_DIR` set to an
   unused scratch path. The run only renders, and the path was not created.
   The result is `FAIL`.
3. After the owner set `LAB_DATA_DIR` in `labs/.env`, the instructed command
   wrote a report at `24225a7da`. The result is `FAIL` with the same values
   as the supplementary run:

| Criterion | Result | Measured values and sources |
| --- | --- | --- |
| tier | PASS | `replace-same`; `infra/04-data/dev-db/valkey/` exists, inside the retired `dev-db/docker-compose.yml` folder (manifest, filesystem) |
| composition | PASS | 0 collisions (`collisions()` against the root render and `docker inspect`); profile `dev-data` is in POL-0078 |
| linux | PASS | cgroup `2` (`docker info .CgroupVersion`); no rendered `user` |
| docker | PASS | Docker `29.9.2` (`docker info .ServerVersion`), Compose `5.6.1` (`docker compose version --short`); drivers `bridge`, `local`; data root `/home/hyunyoun/storage/docker-root/docker` (`docker info .DockerRootDir`) |
| resources | FAIL | NCPU 12 and MemTotal 33575419904 B (`docker info`). The budget is 10 CPUs and 27924 MiB. Running limits are 64 CPUs and 59904 MiB (`docker inspect`). Retired `dev-valkey` frees 1 CPU and 512 MiB. The candidate adds 7 CPUs and 3584 MiB, so it needs 70 CPUs and 62976 MiB. Five running `k3d-hyhome-*` containers declare no limit. Usable disk is 2105.3 GiB on the data root and on the Docker root (`shutil.disk_usage`) |

### W5: Promotion operations documents

The subject numbers OPS-0107, OPS-0108 and OPS-0109 were free; the
`operations-subject` space now has `high_water` 109 and `next_number` 110.

- **OPS-0107 `lab-promotion`.** POL-0107 holds the layout, the manifest
  fields, the secret rules, the `vector` socket exception, the destination
  rules table, the readiness rules and the reserve table. RUN-0107 holds the
  readiness run and the `add`, `replace-same` and `replace-substitute`
  procedures. It states that every step touching HOME runtime needs an
  approved owner window and that SPEC-0263 promotes nothing.
- **OPS-0108 `kafka-cluster` and OPS-0109 `opensearch-cluster`.** Each has a
  Guide and a Runbook in `15-labs`, built from the LAB README and Compose
  file. Neither claims a runtime result. The HOME-input render of both LABs
  is `NOT_RUN`. The controller reported on 2026-11-05 that `labs/.env` lacks
  `LAB_KAFKA_CLUSTER_ID` and `LAB_OPENSEARCH_CERT_DIR`; the agent did not
  read that file. The documents record both as operator inputs.
- **Procedure order (review fix).** RUN-0107 runs readiness first, from the
  LAB location, and a non-zero exit stops the procedure. The move, the
  wiring, render and test, and the start follow. Readiness reads
  `labs/<name>/docker-compose.yml` and `promotion.yaml`, checks that the
  documents exist, and requires the target folder to be absent or a
  declared replacement, so it can never pass after the move. Spec section 5
  ("before any promotion") governs the step numbering in section 6, per the
  controller's ruling.
- **Review text fixes.** `secret-catalog.py --root "$PWD" check` replaces a
  form that exits 2, because `--root` is a top-level option. RUN-0107 lists
  the root `.env` (`--root-env-file`) as a readiness input and defers the
  SMTP01 flags to RUN-0029. POL-0107 names the `hy-home-lab-` project
  prefix.
- **Extra policies.** The Guides name their services in
  `implementation_services`, and `check-operations-catalog.py` then requires
  a current policy per slug (`service-operations-owner`). POL-0108 and
  POL-0109 were added for that reason.
- **Reserve table.** `test_reserve_matches_policy` reads every two-cell
  table row whose first cell is `CPUs`, `Memory MiB` or `Disk percent` and
  compares the second cell, as a float, with `PROMOTION_RESERVE`. Its
  `expectedFailure` decorator is removed.
- **Manifests.** The kafka-cluster and opensearch-cluster `documents.guide`
  and `documents.runbook` now point at the new `15-labs` documents.
- **`labs/README.md`.** Direct links from it to individual stage documents
  fail `check-document-links.py` (`stage-link-outside-docs`). The README
  therefore names the `15-labs` folders and OPS-0107 in text and links only
  the operations entry point.
- **Status.** The new documents start at `draft`, because the metadata check
  refuses a new runbook at any other status. They also link
  `infra/tech-stack.versions.json`, because the metadata check treats a
  `kafka` or `opensearch` slug as owning the HOME runtime entries.
- **Static renders.** With `labs/.env.example` and synthetic inputs, the
  kafka-cluster render lists its five services and the opensearch-cluster
  render its four, both exit 0. Neither starts anything.
- **Open owner decision.** HOME's declared limits already exceed the host
  budget, so no replacement candidate can pass resources. POL-0107 records
  the options: (a) cut HOME limits and give k3d limits; (b) judge
  reservations instead of limits, which needs a Spec change and is
  recommended; (c) judge measured usage. The rule is unchanged.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 7 | W6 | metadata | `check-document-metadata.py --mode check-changed --base-ref main` on the Plan working tree over `56446f74c` | PASS | selected=4 violations=0 | required | - |
| E2 | 3 | W3 | RED tests | `test_lab_secret_paths_use_lab_root_supabase`, `test_supabase_reads_no_home_secret` and `test_repository_lab_reads_its_own_smtp_copy` before the Compose change, over `a8d6e4299` | FAIL | 11 HOME paths, and `invalid_lab_source` | required | - |
| E3 | 3 | W3 | focused unit suites | `tests.lib.ops` SMTP, catalog, structure and retirement modules, `test_supabase_smtp_rehearsal`, `test_lab_layout`, `test_smtp_generator`, `test_service_runtime_compatibility` on the W3 working tree | PASS | 0 failures | required | - |
| E4 | 3 | W3 | full unit suite | `python -m unittest discover -s tests -t .` with the controller venv first on `PATH`, on the W3 working tree | FAIL | 4 failures and 1 error, all against the unapplied public registry; superseded by the clean-env PASS rows E42 and E55, which a W3 row cannot cite as Resolves | required | - |
| E5 | 3 | W3 | registry round trip | `render_views` of the W3 catalog parsed back by `parse_public_table` | PASS | entries and aliases equal the catalog | required | - |
| E6 | 3 | W3 | `lab.py check supabase` render-only | `--env-file labs/.env.example --root-env-file .env.example`, a temporary `LAB_DATA_DIR` and synthetic budgets | FAIL | no socket or catalog problem; the 11 secret paths overlap the root `restic` read-only `secrets/` bind, as stalwart's does; the other problems are empty LAB_DATA_DIR seed files and the synthetic budget; superseded by E12 and the final `check supabase` row E58 | required | - |
| E7 | 3 | W3 | hardening | `bash scripts/hardening/check-all-hardening.sh` | PASS | all checks passed | required | - |
| E8 | 3 | W3 | operations catalog and script manifest | `check-operations-catalog.py`, `check-script-manifest.py` | PASS | both PASS | required | - |
| E9 | 3 | W3 | owner registry and sync | prepared rows and the sync sequence in the W3 Work Log | NOT_RUN | owner step 4 and 5 pending | required | - |
| E10 | 3 | W3 | metadata and links | `check-document-metadata.py --mode check-changed --base-ref main`, `check-document-links.py --mode all` on the W3 working tree | PASS | violations=0; failures=0 | required | - |
| E11 | 3 | W3 | RED test | `test_read_only_secrets_backup_owns_no_lab_secret_copy` with root's read-only `secrets/` bind through `root_footprint`, before the `lab.py` fix | FAIL | the LAB copy "overlaps root" | required | - |
| E12 | 3 | W3 | `lab.py check supabase` render-only | the E6 inputs after the `secrets/` and per-LAB fixes, also run for all 15 LABs | FAIL | no overlap or allowlist problem left; remaining problems are environment seed files (LAB_DATA_DIR seeds, synthetic operator files, ignored lakehouse `__pycache__`); superseded by E58; the `lab.py check supabase` FAIL rows have no later PASS | required | - |
| E13 | 5 | W4 | decision A manifests | `manifest_problems` for `valkey-cluster` and `postgresql-ha` against their `labs/.env.example` renders with a temporary `LAB_DATA_DIR`, at `f4e94cae9` | PASS | no problem for either | required | - |
| E14 | 5 | W4 | RED tests | `ReadinessTests` in `test_lab_controller` before `readiness` existed | FAIL | 14 errors: `readiness` undefined and no `users` in the footprint | required | - |
| E15 | 5 | W4 | LAB suites | `test_lab_controller`, `test_lab_isolation`, `test_lab_layout` at `8fc269531` | PASS | 91 tests; 1 expected failure, `test_reserve_matches_policy`, until W5 | required | - |
| E16 | 5 | W4 | HOME readiness, as instructed | `lab.py --env-file labs/.env readiness valkey-cluster --report <scratchpad>` | NOT_RUN | render refused: `labs/.env` gives Compose no `LAB_DATA_DIR`; no report written; `check` fails the same way | required | - |
| E17 | 5 | W4 | HOME readiness, supplementary | the E16 command with `LAB_DATA_DIR` set to an unused scratch path | FAIL | tier, composition, linux and docker PASS; resources FAIL: 70 CPUs and 62976 MiB needed against 10 CPUs and 27924 MiB, and 5 `k3d-hyhome-*` containers without limits; see the W4 Work Log; superseded by E23 and the final-HEAD run E53 | required | - |
| E18 | 5 | W4 | full unit suite | `python -m unittest discover -s tests -t .` with the controller venv first on `PATH`, at `d1b6747e4` | PASS | 3318 tests, 0 failures, 108 skipped, 1 expected failure | required | - |
| E19 | 5 | W4 | hardening and script manifest | `bash scripts/hardening/check-all-hardening.sh`, `check-script-manifest.py` | PASS | all checks passed; manifest valid | required | - |
| E20 | 5 | W4 | metadata and links | `check-document-metadata.py --mode check-changed --base-ref main`, `check-document-links.py --mode all` on the W4 working tree | PASS | selected=136 violations=0; link mode all PASS | required | - |
| E21 | 5 | W4 | RED tests | the review repros in `ReadinessTests` before the retirement fix, at `a738a5618` | FAIL | 7 failures and 1 error: `add` honored `replaces`, retired-name text hid clashes, `dev-db/pg/` and `qdrant/` passed tier, unparsable `docker info` raised | required | - |
| E22 | 5 | W4 | LAB suites | `test_lab_controller`, `test_lab_isolation`, `test_lab_layout` at `24225a7da` | PASS | 99 tests; 1 expected failure until W5 | required | - |
| E23 | 5 | W4 | HOME readiness, as instructed | `lab.py --env-file labs/.env readiness valkey-cluster --report <scratchpad>` at `24225a7da` | FAIL | report written; tier, composition, linux and docker PASS; resources FAIL: 70 CPUs and 62976 MiB needed against 10 CPUs and 27924 MiB, and 5 `k3d-hyhome-*` containers without limits; supersedes the E16 NOT_RUN, which a FAIL row cannot resolve | required | - |
| E24 | 5 | W4 | metadata and links | `check-document-metadata.py --mode check-changed --base-ref main`, `check-document-links.py --mode all` after the fix | PASS | violations=0; link mode all PASS | required | - |
| E25 | 5 | W4 | HOME readiness `postgresql-ha` | `lab.py --env-file labs/.env readiness postgresql-ha --report <scratchpad>` at `dade9cf06`, after retiring its provisioning jobs; `manifest_problems` returns no problem | FAIL | tier, composition, linux and docker PASS; resources FAIL: 72 CPUs and 66048 MiB needed against 10 CPUs and 27924 MiB, and 5 `k3d-hyhome-*` containers without limits | required | - |
| E26 | 5 | W4 | LAB suites, metadata and links | `test_lab_controller`, `test_lab_isolation`, `test_lab_layout`; `check-document-metadata.py --mode check-changed --base-ref main`; `check-document-links.py --mode all`, after the exclusive-ownership fix `17698152c` | PASS | 102 tests and 1 expected failure; violations=0; link mode all PASS | required | - |
| E27 | 4 | W5 | RED test | `test_reserve_matches_policy` with `expectedFailure` removed, before the policy existed, over `eac1cb6fb` | FAIL | `FileNotFoundError` for `docs/05.operations/policies/15-labs/0107-lab-promotion.md` | required | - |
| E28 | 4 | W5 | GREEN test | `test_reserve_matches_policy` after POL-0107, at `e33f174b3` | PASS | 1 test OK | required | - |
| E29 | 4, 6 | W5 | LAB suites | `test_lab_controller`, `test_lab_isolation`, `test_lab_layout` with the controller venv, at `e33f174b3` | PASS | 102 tests, 0 failures, no expected failure left | required | - |
| E30 | 4, 6 | W5 | operations catalog | `check-operations-catalog.py` at `e33f174b3` | PASS | operations-catalog PASS; an earlier run required POL-0108 and POL-0109 (`service-operations-owner`) | required | - |
| E31 | 4, 6 | W5 | metadata | `check-document-metadata.py --mode check-changed --base-ref main` and `--mode check-active` on the W5 tree | PASS | check-changed selected=144 violations=0; check-active selected=543 violations=0 | required | - |
| E32 | 4, 6 | W5 | links and lifecycle | `check-document-links.py --mode all`, `check-document-corpus-lifecycle.py` at `e33f174b3` | PASS | link failures=0; lifecycle violations=0 | required | - |
| E33 | 4, 6 | W5 | markdownlint and staged hooks | `scripts/validation/run-ci-precommit.sh --mode local-staged` on each W5 commit's staged files | PASS | markdownlint-cli2, check json, ruff and secret detection passed | required | - |
| E34 | 6 | W5 | static renders | `docker compose --env-file labs/.env.example ... config --services` for kafka-cluster and opensearch-cluster with synthetic `LAB_*` inputs | PASS | 5 and 4 services, exit 0; no container started | required | - |
| E35 | 6 | W5 | HOME render of the cluster LABs | `lab.py --env-file labs/.env check kafka-cluster opensearch-cluster` | NOT_RUN | not run by the agent; the controller reported on 2026-11-05 that `labs/.env` lacks `LAB_KAFKA_CLUSTER_ID` and `LAB_OPENSEARCH_CERT_DIR`; operator input pending | required | - |
| E36 | 3 | W3 | owner registry and sync | owner run on 2026-11-05: registry hand-applied in `8ad19acc5`, `secret-catalog.py --root "$PWD" check`, `--sync-metadata-check`, `--sync-metadata`, `--sync-metadata-check` | PASS | `load_catalog` OK; files_changed=3 then 0 after sync; prune rejected while COMM-003 remains, by design | required | E9 |
| E38 | 7 | W6 | root render | `docker compose --env-file .env.example config -q` at `b79bd797a` | PASS | exit 0; no container started | required | - |
| E39 | 7 | W6 | LAB renders, example inputs | `docker compose --env-file labs/.env.example -f labs/<name>/docker-compose.yml config -q` for the 15 LABs, `LAB_DATA_DIR` a temporary absolute scratch path, at `b79bd797a` | FAIL | 7 render (cassandra, couchdb, jupyterlab, mongodb, postgresql-ha, supabase, valkey-cluster); 8 refuse on a required variable that `labs/.env.example` leaves empty by design (dbt, kafka-cluster, lakehouse, locust, opensearch-cluster, sonarqube, stalwart, superset), for example `LAB_KAFKA_CLUSTER_ID is missing a value`; no path or secret error | required | - |
| E40 | 7 | W6 | LAB renders, synthetic owner inputs | the E39 command for the 8 refusing LABs with the 12 missing `LAB_*` variables set to synthetic hosts and scratch directories, at `b79bd797a` | PASS | all 8 exit 0; no container started | required | - |
| E41 | 7 | W6 | full unit suite | `python -m unittest discover -s tests -t .` with the controller venv first on `PATH`, at `b79bd797a`, run from a shell that had exported `LAB_DATA_DIR` | FAIL | Ran 3330, failures=11, skipped=108; all 11 in `test_lab_controller.LifecycleTests` (`0 != 3`); the cause was the exported `LAB_DATA_DIR` in the runner, and `test_lab_controller` alone passed in a clean shell | required | - |
| E42 | 7 | W6 | full unit suite | the E41 command in a shell with no `LAB_*` variable, at `b79bd797a` | PASS | Ran 3330 tests, 0 failures, 0 errors, 108 skipped | required | E41 |
| E43 | 7 | W6 | hardening | `bash scripts/hardening/check-all-hardening.sh` at `b79bd797a` | PASS | ALL checks passed successfully | required | - |
| E44 | 7 | W6 | metadata | `check-document-metadata.py --mode check-changed --base-ref main` and `--mode check-active` at `b79bd797a` | PASS | check-changed selected=144 violations=0; check-active selected=543 violations=0 | required | - |
| E45 | 7 | W6 | links and lifecycle | `check-document-links.py --mode all`, `check-document-corpus-lifecycle.py` at `b79bd797a` | PASS | documents=892 failures=0; lifecycle violations=0 | required | - |
| E46 | 7 | W6 | operations catalog and script manifest | `check-operations-catalog.py`, `check-script-manifest.py` at `b79bd797a` | PASS | operations-catalog PASS; script manifest valid | required | - |
| E47 | 7 | W6 | local full CI gate | `python3 scripts/validation/run-ci-gate.py` | NOT_RUN | BLOCKED, not run: it needs Python 3.14.8 with memfd sealing; this host has 3.12 and uv's build lacks sealing, as the earlier Tasks record | required | - |
| E48 | 7 | W6 | hosted CI | pull request checks | NOT_RUN | the branch is not pushed and no pull request is open | required | - |
| E37 | 4, 6 | W5 | review fix checks | `check-document-metadata.py --mode check-changed --base-ref main`, `check-document-links.py --mode all`, `check-operations-catalog.py`, staged markdownlint, `test_reserve_matches_policy` after the review fixes | PASS | violations=0; link failures=0; catalog PASS; markdownlint passed; 1 test OK | required | - |
| E49 | 1 | W2 | layout tests | `test_lab_layout` with the controller venv at `4bec12fa2` | PASS | 6 tests OK | required | - |
| E50 | 2 | W1 | manifest and `check` tests | `test_lab_controller` `LabLayoutAndManifestTests` and `AdmissionGuardTests` at `4bec12fa2` | PASS | 17 tests OK | required | - |
| E51 | 5 | W4 | RED tests | final-review repros in `ReadinessTests`; `LifecycleTests` with `LAB_DATA_DIR` exported, before `4bec12fa2` | FAIL | 6 failures and 2 errors (candidate without limits, zero limit, unreadable or escaping subtree, repo paths, root include, bad input, unmeasured sub-checks); `LifecycleTests` 11 failures | required | - |
| E52 | 5 | W4 | LAB suites | `test_lab_controller`, `test_lab_isolation`, `test_lab_layout` at `4bec12fa2`; `LifecycleTests` again with `LAB_DATA_DIR` exported | PASS | 108 tests OK; `LifecycleTests` OK with the variable exported | required | - |
| E53 | 5 | W4 | HOME readiness `valkey-cluster` | `lab.py --env-file labs/.env readiness valkey-cluster --report <scratchpad>` at `4bec12fa2` | FAIL | tier PASS; composition NOT_RUN and linux NOT_RUN (unmeasured section 5 sub-checks); docker PASS; resources FAIL: 70 CPUs and 62976 MiB needed against 10 CPUs and 27924 MiB, and 5 `k3d-hyhome-*` containers without limits | required | - |
| E54 | 5 | W4 | HOME readiness `postgresql-ha` | the E53 command for `postgresql-ha` at `4bec12fa2` | FAIL | tier PASS; composition NOT_RUN and linux NOT_RUN; docker PASS; resources FAIL: 72 CPUs and 66048 MiB needed against 10 CPUs and 27924 MiB, and 5 `k3d-hyhome-*` containers without limits | required | - |
| E55 | 7 | W6 | full unit suite | `python -m unittest discover -s tests -t .` with the controller venv first on `PATH` and every `LAB_*` variable unset, at `4bec12fa2` | PASS | Ran 3336 tests, 0 failures, 0 errors, 108 skipped | required | - |
| E56 | 7 | W6 | hardening, operations catalog and script manifest | `bash scripts/hardening/check-all-hardening.sh`, `check-operations-catalog.py`, `check-script-manifest.py` at `4bec12fa2` | PASS | ALL checks passed; operations-catalog PASS; manifest valid | required | - |
| E57 | 7 | W6 | metadata and links | `check-document-metadata.py --mode check-changed --base-ref main` and `--mode check-active`, `check-document-links.py --mode all`, on the final fix wave working tree | PASS | check-changed selected=144 violations=0; check-active selected=543 violations=0; link mode all PASS | required | - |
| E58 | 3 | W3 | `lab.py check supabase` with owner inputs | `lab.py --env-file labs/.env check supabase` at `4bec12fa2` | NOT_RUN | exit 2 before any report: `labs/.env` gives no numeric `LAB_HOST_BUDGET_CPUS` | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | pending | - | - | @buenhyden |
| 2 | pending | - | - | @buenhyden |
| 3 | pending | - | - | @buenhyden |
| 4 | pending | - | - | @buenhyden |
| 5 | pending | - | - | @buenhyden |
| 6 | pending | - | - | @buenhyden |
| 7 | pending | - | - | @buenhyden |

## Review and Completion

The final review fix wave (E49 to E58) re-ran the checks at `4bec12fa2`.
Readiness now shows the unmeasured section 5 sub-checks as `NOT_RUN`, a
narrowing that awaits the owner's acceptance. Hosted CI stays NOT_RUN (E48)
until the controller pushes.

All work units W1 to W6 are done. W6 ran the Verification Plan at
`b79bd797a` (E38 to E48): the unit suite, hardening, metadata, links, lifecycle,
catalog and manifest checks pass, and 7 of 15 LABs render from
`labs/.env.example` as is. The other 8 need owner inputs that the example
leaves empty (E39; they render with synthetic inputs, E40). The local full CI
gate is BLOCKED by the host Python (E47) and hosted CI is NOT_RUN until the
branch is pushed (E48). No criterion is accepted.

Owner decisions on 2026-11-06:

- **Resource rule:** judge the declared `deploy.resources.reservations`
  instead of limits. This needs a Spec amendment, reservations on the HOME
  services and a readiness change. That is a follow-up Task under this Spec;
  E53 and E54 keep refusing on resources until it lands.
- **Section 5 narrowing:** accepted as owner check items. Groups and file
  modes, and profile and consumer clashes, become checklist items in each
  promotion Task. The follow-up Task amends the Spec and makes those
  readiness entries owner-judgment, non-blocking.
- **Secret-name uniqueness:** the dropped root/LAB name uniqueness is
  accepted, because the per-LAB path rule keeps the copies apart.
- **Delivery:** push the branch and open a PR; the owner merges after
  hosted CI.

Open owner items:

- `labs/.env` `LAB_HOST_BUDGET_*` for `lab.py check` (E58);
- `labs/.env` `LAB_KAFKA_CLUSTER_ID` and `LAB_OPENSEARCH_CERT_DIR` (E35);
- SMTP01 removing COMM-003;
- retiring the unused `secrets/db/mng-pg/supabase_password.txt`.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
