---
title: "Unseal Share File Out of Host Backups"
version: "0.2.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0240"
parent_ids:
- "REQ-0003"
- "AD-0004"
- "ADR-0041"
- "ADR-0042"
created: "2026-10-14"
---

# Unseal Share File Out of Host Backups

## Overview

The OpenBao unseal share file `secrets/security/openbao/openbao_unseal_keys.txt`
holds all three Shamir shares (threshold 2). The Restic host set backs up all
of `secrets/` with no exclusion, and `restic-offsite` copies that repository
to a bucket-locked R2 repository encrypted with BKP-003. Once BKP-003 is kept
off the host, as RUN-0085 checklist step 5 requires, whoever holds BKP-003 and
R2 read access can recover every share. POL-0085 also called the file the only
copy. An independent security review of PR #461 found this on 2026-10-14, and
the owner chose that day (AskUserQuestion) to exclude the file from the host
backup, to rekey in a separate window, and to correct the policy text. Later
that day, because one administrator holds every place, the owner chose
(AskUserQuestion) to allow three places with a condition on BKP-003.

## Scope

In scope: `infra/09-platform-ops/restic/sets/host-exclude.txt`, its test, the
POL-0085 exception text, ADR-0042's context, and RUN-0085's custody procedure
and maintenance-window plan. Out of scope: running the rekey, deleting the
host file or any existing snapshot, the R2 bucket lock and retention, and any
change to the state set.

## Contracts

1. The host set excludes exactly the unseal share file and nothing else.
2. The exclusion is merged, and present in the operating checkout, only after
   RUN-0085 step 5 is `owner-attested`, because that checkout applies it to the
   next daily backup and new recovery points then rely on off-host custody.
3. POL-0085 and ADR-0042 state where copies of the file exist and that BKP-003
   with R2 read access meets the threshold; neither closes the POL-0085
   exception.
4. RUN-0085 keeps BKP-003 apart from the R2 credentials and from Cloudflare
   account access, and apart from every share except as contract 5 allows, defines a place as a separately
   credentialed or physically held unit, plans the rekey as W1b before any new
   Raft snapshot with new shares never written to the host, and states that
   the exposure ends only when pre-exclusion host snapshots are deleted.
5. For a single administrator, RUN-0085 and POL-0085 allow three places, one
   share each. BKP-003 may share a place with one share only after the
   exclusion is confirmed in a new host snapshot (W4) and no pre-exclusion
   host snapshot remains in the R2 repository; until then it needs a place
   with no share. A place's opening means may not be stored in another place.
   The POL-0085 exception stays open.

## Acceptance Criteria

1. A test pins the host exclusion to the unseal file alone, and a dry run of
   the pinned Restic image on a synthetic tree omits that file and keeps its
   siblings.
2. POL-0085, ADR-0042 and RUN-0085 state contracts 3 and 4, and the document
   checks pass.
3. Independent IaC, security and rules reviews find nothing blocking.
4. After the owner attests step 5 and the change merges, the next daily host
   snapshot does not contain the file.
5. RUN-0085 and POL-0085 state contract 5, the step 5 table and verdict
   accept it, and independent security and rules reviews find nothing
   blocking.

## Related Documents

- [REQ-0003](../../01.requirements/0003-security.md)
- [AD-0004](../../02.architecture/descriptions/0004-data-architecture.md)
- [ADR-0041](../../02.architecture/decisions/0041-offsite-backup-target.md)
- [ADR-0042](../../02.architecture/decisions/0042-openbao-unseal-method.md)
- [Plan](plan.md)
