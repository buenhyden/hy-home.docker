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
  `replace-same`. `valkey-cluster` and `postgresql-ha` are `undecided`,
  because HOME runs both an `mng-db` and a `dev-db` node of each. The other
  11 are `undecided`.
- **Reserve.** The first reserve is 2 CPUs, 4096 MiB of memory and 10% of
  each filesystem kept free. The host measured on 2026-11-05 has 12 CPUs and
  32020 MiB.
- **New operations subjects.**
  - OPS-0107 is `lab-promotion`, with a policy and a runbook.
  - OPS-0108 is `kafka-cluster`.
  - OPS-0109 is `opensearch-cluster`.
- **The readiness check.** It is a `lab.py readiness` subcommand, not a new
  script.

### W3: supabase on LAB secret copies

**Owner checklist.**

| Step | Action | Status |
| --- | --- | --- |
| 1 | Copy the HOME SMTP password into `secrets/labs/supabase/smtp_password.txt` | DONE by the owner on 2026-11-05 |
| 2 | Place `secrets/labs/supabase/supabase_db_password.txt` from the mng-pg file | DONE by the owner on 2026-11-05 |
| 3 | Move the nine `secrets/data/supabase/*.txt` files to `secrets/labs/supabase/` | DONE by the owner on 2026-11-05 |
| 4 | Apply the prepared rows below to `secrets/SENSITIVE_ENV_VARS.md.example` | PENDING, owner |
| 5 | Run the private-registry sync below | PENDING, owner |

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

1. `python3 scripts/operations/secret-catalog.py --root . check`. Expect
   `P02_METADATA_VALID` with 156 entries and 6 aliases. Before step 4 it
   prints `P02_METADATA_BLOCKED` and exits 2, because the catalog and the
   public registry differ.
2. `bash scripts/operations/gen-secrets.sh --sync-metadata-prune-check`.
   Expect `METADATA files_changed=N values=preserved secret_files=untouched`
   and exit 1 while the private registry still holds the five retired rows.
   Exit 2 means a rejected input. One cause is a COMM-003 row still in the
   private registry: only SMTP01 removes it.
3. `bash scripts/operations/gen-secrets.sh --sync-metadata-prune`. Expect the
   same line and exit 0. It drops the five retired private rows; their values
   stay in the LAB copies. LAB-037 gets the public placeholder. Other value
   cells and `.env` values are kept.
4. Run `--sync-metadata-prune-check` again. Expect `files_changed=0` and
   exit 0.

**SMTP retirement path.** `scripts/lib/ops/smtp_public_source.py` now
requires the supabase LAB to read its LAB-037 copy and refuses any LAB file
that names the HOME SMTP path. Its fixed `extends` file is now
`../../infra/common-optimizations.yml`, which W2's move required.
`retire_materials.py`, `secret_structure.py` and `smtp_contract.py` only
handle the COMM-003 duplicate and needed no change. `gen-secrets.sh` now
accepts any well-formed retired-row alias, not only COMM-003.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 7 | W6 | metadata | `check-document-metadata.py --mode check-changed --base-ref main` on the Plan working tree over `56446f74c` | PASS | selected=4 violations=0 | required | - |
| E2 | 3 | W3 | RED tests | `test_lab_secret_paths_use_lab_root_supabase`, `test_supabase_reads_no_home_secret` and `test_repository_lab_reads_its_own_smtp_copy` before the Compose change, over `a8d6e4299` | FAIL | 11 HOME paths, and `invalid_lab_source` | required | - |
| E3 | 3 | W3 | focused unit suites | `tests.lib.ops` SMTP, catalog, structure and retirement modules, `test_supabase_smtp_rehearsal`, `test_lab_layout`, `test_smtp_generator`, `test_service_runtime_compatibility` on the W3 working tree | PASS | 0 failures | required | - |
| E4 | 3 | W3 | full unit suite | `python -m unittest discover -s tests -t .` with the controller venv first on `PATH`, on the W3 working tree | FAIL | 4 failures and 1 error, all against the unapplied public registry | required | - |
| E5 | 3 | W3 | registry round trip | `render_views` of the W3 catalog parsed back by `parse_public_table` | PASS | entries and aliases equal the catalog | required | - |
| E6 | 3 | W3 | `lab.py check supabase` render-only | `--env-file labs/.env.example --root-env-file .env.example`, a temporary `LAB_DATA_DIR` and synthetic budgets | FAIL | no socket or catalog problem; the 11 secret paths overlap the root `restic` read-only `secrets/` bind, as stalwart's does; the other problems are empty LAB_DATA_DIR seed files and the synthetic budget | required | - |
| E7 | 3 | W3 | hardening | `bash scripts/hardening/check-all-hardening.sh` | PASS | all checks passed | required | - |
| E8 | 3 | W3 | operations catalog and script manifest | `check-operations-catalog.py`, `check-script-manifest.py` | PASS | both PASS | required | - |
| E9 | 3 | W3 | owner registry and sync | prepared rows and the sync sequence in the W3 Work Log | NOT_RUN | owner step 4 and 5 pending | required | - |
| E10 | 7 | W3 | metadata and links | `check-document-metadata.py --mode check-changed --base-ref main`, `check-document-links.py --mode all` on the W3 working tree | PASS | violations=0; failures=0 | required | - |

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

W1 to W3 have changed the repository. Criterion 3 waits for the owner's
registry edit and sync (E9). No criterion is accepted.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
