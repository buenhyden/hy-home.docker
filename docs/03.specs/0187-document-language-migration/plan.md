---
title: "Document Language Migration Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0187-PLAN-0001"
parent_ids:
- "SPEC-0187"
created: "2026-09-28"
---

# Document Language Migration Plan

## Objective

Translate the 200 documents that [SPEC-0187](spec.md) measures, then enforce
document language across the whole corpus.

## Dependencies

- SPEC-0184 and SPEC-0186 are integrated into the local `main`.
- The branch starts from that `main`.

## Execution Sequence

1. W1: Record the measured list and the pre-change gate summaries in the Task
   (criteria 1, 5).
2. W2: Translate the 17 Requirements packages into English (criteria 2, 5).
3. W3: Translate the 29 ADRs into English (criteria 2, 5).
4. W4: Translate the 20 architecture descriptions into English (criteria 2, 5).
5. W5: Translate the 45 guides into Korean, with humanize-korean (criteria 2,
   3, 5).
6. W6: Translate the 47 policies into Korean, with humanize-korean (criteria 2,
   3, 5).
7. W7: Translate the 41 runbooks and `.github/repository-surface.md` into
   Korean, with humanize-korean (criteria 2, 3, 5).
8. W8: Widen `--mode language` to the whole corpus and remove the lifecycle
   body filter, tests first (criteria 4, 5, 6).
9. W9: Rerun the gate members and both unit suites and record the evidence
   (criteria 5, 6).

W2 through W7 commit per profile, or in batches of about ten documents for the
larger profiles. W8 is one commit.

## Risk and Rollback

Every batch is its own commit, so reverting one commit restores one batch. If
a batch fails the token comparison, it is redone, not forced.

## Verification

- The scratch token comparison passes for every translated document.
- `check-document-links.py --mode all` and
  `check-document-metadata.py --mode check-changed --base-ref main` pass after
  every batch.
- After W8, `check-document-links.py --mode language` reports no findings.
- `python3 -m unittest discover -s tests/lib -t .` and
  `python3 -m unittest discover -s tests/validation -t .` pass.

## Rulings

None yet.
