---
title: "Retire the Supabase LAB Task"
version: "0.2.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0263-TSK-0003"
parent_ids:
- "SPEC-0263-PLAN-0001"
created: "2026-11-06"
---

# Retire the Supabase LAB Task

## Scope

### Objective and Parent

#### Objective

Carry out Plan work unit W8: remove the supabase LAB, its operations
documents, catalog rows and Docker socket allowance, and keep the SMTP01
retirement of COMM-003 working without it.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [LAB Promotion Contract Task](tsk-0001-lab-promotion-contract.md)
- [RUN-0106](../../../05.operations/runbooks/04-security-and-secrets/0106-openbao-consumer-catalog.md)

### Inputs and Authority

On 2026-11-06 the owner decided to remove the supabase LAB (`labs/supabase/`).
No LAB is promoted. The owner approved the Spec amendment draft the same day
(see [Spec amendment approval](#spec-amendment-approval)).

This Task starts, stops and recreates no container, reads no secret value and
edits nothing under `secrets/`. The owner applies the public registry edit and
removes the private files (see [Owner steps](#owner-steps)).

## Execution Log

### Work Performed

#### Spec amendment approval

SPEC-0263 moved to `in-review` for the amendment to version 0.4.0: criterion 3
became "No LAB reads a HOME secret path; each LAB uses `secrets/labs/<name>/`
for every secret, each with its catalog and registry rows. No LAB binds the
Docker socket.", the section 3 socket exception was removed, and the
Background records the removal. The owner approved the draft on 2026-11-06
("Spec 수정 초안 승인"), so SPEC-0263 returned to `approved`.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0263 | approved | in-review | #spec-amendment-approval |
| SPEC-0263 | in-review | approved | #spec-amendment-approval |
| SPEC-0263-TSK-0003 | draft | ready | #w8-implementation |
| SPEC-0263-TSK-0003 | ready | in-progress | #w8-implementation |

#### W8 implementation

- **LAB source.** `labs/supabase/` is deleted (Compose, README,
  `naming-exceptions.json`, `promotion.yaml`, `.env.example`). `labs/README.md`
  drops both supabase rows; `labs/.env.example` drops the seven
  `LAB_SUPABASE_*` keys; the root `.env.example` heading drops "SUPABASE".
- **Operations documents.** GDE-0029, RUN-0029 and POL-0029 are deleted with
  their `15-labs` README rows. The RUN-0029 sections "SMTP 전환 확인과 중복
  퇴역" and "SMTP01의 root·lock·증거 계약" moved into
  [RUN-0106](../../../05.operations/runbooks/04-security-and-secrets/0106-openbao-consumer-catalog.md),
  at the same heading level. RUN-0106 already owns the COMM-003 alias probes
  and the secret-structure SMTP checks, and `scripts/manifest.yaml` already
  names it as the authority of the secret tooling, so it is the owner of the
  secret lifecycle step that retires COMM-003. Changed inside the moved text:
  the Auth source/target precondition and the Auth mount alias in the recovery
  line are removed, the `source_sha256` paragraph no longer binds the LAB
  Compose or the LAB Auth proof, and one line records the removal. RUN-0107
  links to RUN-0106 instead of RUN-0029. POL-0001, POL-0006, POL-0078, POL-0107
  and GDE-0041 drop their supabase rows and lines; POL-0107 now says no LAB
  binds the Docker socket.
- **Catalog.** SUPA-002 to SUPA-011, AI-001 and LAB-037 are removed from
  `secret-catalog.json`; no alias pointed at them and no other ID changed.
  `infra/secret-file-support.json` drops the 38 rows of the supabase, `kong`
  and `postgrest/postgrest` images, which only the LAB rendered.
- **`lab.py`.** `_socket_exception` and its four call sites are removed. Every
  socket bind, read-only or writable, is now refused by the allowlist and by
  path integrity.
- **SMTP01 tooling.** `gen-secrets.sh --retire-supabase-smtp(-check)`,
  `smtp_contract.py`, `smtp_public_source.py` and their names stay. With the
  LAB gone, `smtp_contract.source_hashes` raised `auth_alias_missing` on this
  repository, because it required a root Auth alias whenever the LAB source
  was absent. It now passes `require_auth=False`: an Auth alias is still
  validated where one exists, and every old source and old path guard stays
  fail-closed. `validate_lab_sources` already returned `({}, False)` for an
  absent LAB.
- **Inventories.** `infra/tech-stack.versions.json` drops 12 image entries
  and the supabase source of PostgreSQL. The update ledger's 13 supabase
  `historical_lab_entries` keep their original root rows; only their current
  fields became `current_scope: removed`, `current_compose_file: null`.
  Past lookups, observations and verifications stay. `scripts/manifest.yaml`
  points the two SMTP libraries at RUN-0106. The hardening check drops the
  supabase Compose checks. `docs/99.templates/registry.json` drops
  `labs/supabase/README.md`.
- **Architecture.** AD-0004, AD-0019 and AD-0026 drop supabase and
  `supabase_net`. ADRs are unchanged.
- **Tests.** The socket tests now expect every socket bind refused, including
  supabase `vector`. Tests that read the deleted LAB were removed or turned
  into absence checks. The opt-in GoTrue rehearsal skips while its source is
  absent. `test_smtp_contract` records that a missing Auth alias is accepted.

#### Owner steps

1. Remove these 12 rows from `secrets/SENSITIVE_ENV_VARS.md.example`: SUPA-002,
   SUPA-003, SUPA-004, SUPA-005, SUPA-006, SUPA-007, SUPA-008, SUPA-009,
   SUPA-010, SUPA-011, AI-001 and LAB-037. The file is not generated;
   `load_catalog` requires it to match the catalog.
2. Update `secrets/README.md`, which still names `labs/supabase/`.
3. Check and sync the private registry:

   ```bash
   PATH="$HOME/.local/share/hy-home/controller-venv-py312/bin:$PATH" bash scripts/operations/gen-secrets.sh --sync-metadata-check
   PATH="$HOME/.local/share/hy-home/controller-venv-py312/bin:$PATH" bash scripts/operations/gen-secrets.sh --sync-metadata
   ```

   `--sync-metadata-prune` stays blocked while the private registry holds
   COMM-003, so the 12 private rows go only after SMTP01 retires COMM-003.
4. Run `python3 scripts/operations/secret-catalog.py --root "$PWD" check`.
   It must print `P02_METADATA_VALID`.
5. Delete the private files under `secrets/labs/supabase/` and the folder.
6. Optional, if the LAB ever ran: confirm `lab.py status` shows no running
   `hy-home-lab-supabase` project, then remove its data folder
   `${LAB_DATA_DIR}/supabase` and any leftover `hy-home-lab-supabase*`
   network or volume in an owner window.

### Blockers and Decisions

None: nothing was recorded here before this Task moved to the common form.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 3 | W8 | LAB suites | `test_lab_controller`, `test_lab_isolation`, `test_lab_layout` on the uncommitted W8 tree over `982f230de` | FAIL | 116 tests, errors=1: `test_no_document_or_script_starts_the_root_with_every_profile` reads `git ls-files`, which still lists the four deleted files until the commit; the same scan over existing files finds no offender | required | - |
| E2 | 3 | W8 | secret suites | `test_secret_metadata_sync`, `test_secret_catalog_contract`, same tree | FAIL | 49 tests, failures=1, errors=2: the catalog/`.md.example` drift on the 12 removed IDs (owner step 1) and one deleted-file-in-index error | required | - |
| E3 | 3 | W8 | catalog | `secret-catalog.py --root "$PWD" check`, same tree | FAIL | `P02_METADATA_BLOCKED`, exit 2, `catalog_public_source_drift`; the public table has exactly SUPA-002 to SUPA-011, AI-001 and LAB-037 more than the catalog, no differing row, aliases equal | required | - |
| E4 | 3 | W8 | SMTP01 source | `smtp_contract.source_hashes` on this repository, same tree | PASS | before the fix `auth_alias_missing`; after it the root include graph hashes with no LAB entry; `test_smtp_contract` 60 tests OK | required | - |
| E5 | 3 | W8 | focused suites | SMTP, tier layout, SEC01, update gates, workflow contract and runtime compatibility suites, same tree | FAIL | 274 tests, errors=2, skipped=6; both errors read a deleted file still listed by `git ls-files` | required | - |
| E6 | 3 | W8 | hardening | `bash scripts/hardening/check-all-hardening.sh`, same tree | PASS | exit 0, "ALL checks passed successfully" | required | - |
| E7 | 3 | W8 | root render | `docker compose --env-file .env.example --profile '*' config -q`, same tree | PASS | exit 0 | required | - |
| E8 | 3 | W8 | metadata | `check-document-metadata.py --mode check-changed --base-ref origin/main` and `--mode check-active`, same tree | PASS | selected=23 violations=0; selected=539 violations=0 | required | - |
| E9 | 3 | W8 | lifecycle | `check-document-corpus-lifecycle.py`, same tree | PASS | violations=0; active stage occupancy violations=0 | required | - |
| E10 | 3 | W8 | links | `check-document-links.py --mode all`, same tree | FAIL | documents=890 links=8100 failures=1: RUN-0107:51 names `labs/.env`, which this worktree does not carry; the file is unchanged by W8 | required | - |
| E11 | 3 | W8 | operations catalog | `check-operations-catalog.py`, same tree | FAIL | exit 1, `file-unreadable` on the deleted GDE-0029, still listed by `git ls-files` | required | - |
| E12 | 3 | W8 | script manifest | `check-script-manifest.py`, same tree | PASS | "script manifest is valid" | required | - |
| E13 | 3 | W8 | full suite | `env -u LAB_DATA_DIR python -m unittest discover -s tests -t .`, same tree | FAIL | 3316 tests in 2449 s, failures=2, errors=16, skipped=108; 16 read the deleted files through `git ls-files`, 2 are the owner-pending registry drift | required | - |
| E14 | 3 | W8 | LAB suites | same three modules on main `e6031ac93` after #763 merged | PASS | 116 tests OK | required | E1 |
| E15 | 3 | W8 | secret suites | same two modules on main `e6031ac93`, after the owner removed the 12 public rows (`07bb88c2a`) | PASS | 70 tests OK | required | E2 |
| E16 | 3 | W8 | catalog | `secret-catalog.py --root "$PWD" check` on main `e6031ac93` | PASS | `P02_METADATA_VALID`, entries=144, aliases=6 | required | E3 |
| E17 | 3 | W8 | focused suites | SMTP, tier layout, SEC01, workflow contract, runtime compatibility and update gate modules on main `e6031ac93` | PASS | 205 tests OK, skipped=6 | required | E5 |
| E18 | 3 | W8 | links | `check-document-links.py --mode all` on main `e6031ac93` plus this change's two navigation fixes | PASS | `PASS: document link mode all` | required | E10 |
| E19 | 3 | W8 | operations catalog | `check-operations-catalog.py` on main `e6031ac93` | PASS | `operations-catalog: PASS` | required | E11 |
| E20 | 3 | W8 | full suite | `env -u LAB_DATA_DIR python -m unittest discover -s tests -t .` on main `b496a291c` | PASS | 3337 tests OK, skipped=108 | required | E13 |

### Resolution Links

None: nothing was recorded here before this Task moved to the common form.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 3 | pending | E4, E6, E7, E8, E9, E12, E14, E15, E16, E17, E18, E19, E20 | every required row now passes; owner acceptance pending | @buenhyden |

### Remaining Conditions

W8 is implemented on the uncommitted tree. The non-PASS rows have two causes,
neither a W8 defect: deleted files stay in the Git index until the controller
commits (E1, E5, E11, E13), and the public registry keeps the 12 removed rows
until the owner applies step 1 (E2, E3, E13). E10's `labs/.env` is the owner's
private file, absent from this worktree. After the commit and step 1, re-run
E1, E2, E3, E5, E10, E11 and E13; criterion 3 stays pending until then.

After #763 merged and the owner applied step 1, E14 to E20 re-ran the
failed checks on main: each now passes and resolves its earlier row.
Criterion 3 waits only for the owner's acceptance.

## Handoff

### Promotion Receipt

None: nothing was recorded here before this Task moved to the common form.

### Next Owner

None: nothing was recorded here before this Task moved to the common form.
