---
layer: agentic
status: active
---

# Current Project Memory

## Current objective

- Current task: `docs/04.execution/tasks/2026-08-07-agentic-research-pack-extension.md`
- T-ARPE-001 through T-ARPE-013 are complete. The canonical agentic research
  pack gained three leaves covering documentation architecture, the LLM-WIKI
  system, and the agent memory hierarchy, and its fifteen existing leaves were
  revalidated against repository facts and current external sources. This Task
  is the successor Task the previous handoff asked for, so the lifecycle
  boundary that paused
  `task:2026-07-26-agent-governance-canonical-convergence` is released.

## Approved decisions

- The pack is extended in place. No new dated research pack directory is
  created, which preserves the Spec 122 consolidation outcome.
- The `2026-07-07-agentic-research-pack-update/` pack is removed. It held only
  redirect stubs with no analysis, and its canonical destination mapping now
  lives in the Superseded Paths table of the research category index. Spec 122
  paired this disposition with a human-escalation precondition, which the user
  instruction satisfies.
- Revalidation covers two axes: repository-local counted facts and current
  official external sources.
- Governance lifecycle for this work is one Stage 04 Task, without a new Spec
  or Plan.
- Fixed historical boundaries stay unchanged by this revalidation: the
  2026-07-10 model cutoff, the 2026-07-26 typed contract timestamps, and every
  claim recorded as unverified.

## Active boundary

- The Task covers three new Stage 90 leaves, fifteen revalidated leaves, both
  README indexes, this record, the three generated artifacts whose freshness
  contracts the changes tripped, and the consolidation unit that removed the
  duplicate pack and repaired its inbound links in Spec 122, its README, and
  the two 2026-07-10 consolidation artifacts.
- Push, remote mutation, live provider calls beyond read-only public
  documentation retrieval, runtime changes, Compose operations, Stage 00 policy
  changes, and the controlled all-files wrapper stay outside this Task.
- Independent review of this Task has not happened.

## Verified state

- Verified commit: `6faf9444d2eeda93766d1912100a28c4628c8aa4`
- Verified at: `2026-08-07T13:52:00+09:00`
- Coverage analysis before authoring found that nineteen of twenty-two
  requested research topics already had canonical coverage across fifteen
  leaves totalling 3,523 lines, and that three had none.
- Workspace fact re-derivation confirmed twenty-one of twenty-three cited
  figures and found one real drift: local QA runner step counts were
  understated by four in both modes because two helper functions were omitted
  from the original enumeration. Re-derived counts are 24 default and 22
  harness steps, which reconciles with the 25 bullets the list mode prints
  minus one advisory recommender.
- External revalidation corrected the Codex `SessionEnd` claim in five places,
  the Gemini per-agent reasoning claim, the Codex effort range, the Claude and
  Gemini hook event counts, and six stale or redirected source URLs.
- Five external sources could not be re-fetched and are recorded as not
  re-verified rather than removed, since none was disproven.
- The repository contract check exits with ten failures, down from thirteen
  during this Task. Every failing subject is untouched by this work, and no
  `infra/`, `scripts/`, or `.github/` path changed.
- Changed-document metadata validation selected twenty-four documents and
  reports three findings, all the same heading-contract conflict on the three
  new leaves.
- Traceability passes with forty-six catalog pairs and zero failures, and the
  final diff has no whitespace drift.
- The research category now holds one pack. The removed pack's six files and
  416 lines carried no analysis. The generated LLM Wiki index fell from 1,330
  to 1,324 path rows.
- Spec 122 line 173 stated that the pack remains at its current path, and its
  acceptance criterion VAL-ARC-006 referred to the pack and its children. Both
  are superseded by this removal; the mapping they protected is preserved in
  the category index. Spec 122 stays `completed` and was reopened only for
  inbound-link repair.
- The repository contract check after consolidation reports the same ten
  predecessor failures with no new subject.
- Sixteen logical-unit commits span `19ee4727` to `6faf9444`.
- All five previously unfetchable sources are verified through upstream sources
  of record. The earlier HTTP 429 diagnosis was wrong: those hosts return a
  Cloudflare bot challenge that retrying never clears from an automated client.
- The heading-contract conflict is resolved by aligning the reference template,
  the reference role required headings, and the template-source heading list to
  the heading 69 documents already use. The audit role forbidden-heading entry
  is unchanged because 34 audit documents would break.
- Predecessor drift fell from ten findings to two. Six registry entries, the
  provenance snapshot, and two hardcoded hardening image-tag expectations were
  catch-up corrections only; Compose already declared every newer image, so no
  service version changed. A seventh drifted image, dozzle, surfaced only after
  the Keycloak expectation was corrected.
- The repository contract check now reports two remaining subjects. Metadata
  validation selected thirty-nine documents with zero violations.

## Blockers and unverified facts

- Two repository-check subjects stay open and both need an action outside the
  repository. The private `.env` carries `INFLUXDB_BUCKET`, `INFLUXDB_ORG`, and
  `INFLUXDB_USERNAME`, which `.env.example` does not; the user chose to leave
  that as an environment fact, and it links to the separate InfluxDB review.
  The `html5lib` dependency is declared in `scripts/requirements.txt` but is not
  installed, and PEP 668 blocks installation in this externally-managed Python
  environment; a virtual environment or the distribution package is needed.
- The audit role still forbids the reference heading that 34 audit documents
  carry. That rule is vacuous today and retargeting it would surface 34
  violations, so it is recorded rather than changed.
- Provider acceptance and entitlement, live comparative model evaluation, and
  authenticated remote GitHub enforcement stay unverified.
- A typed domain-memory taxonomy with validator-enforced promotion, retention,
  archival, and deletion stays outside current scope. The new memory-hierarchy
  leaf records the research basis for it. That leaf also corrects the record
  that the deferral wording originates in the Stage 04 Task ledger rather than
  in Spec 134.

## Evidence links

- [Active Task ledger](../../04.execution/tasks/2026-08-07-agentic-research-pack-extension.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Documentation architecture leaf](../../90.references/research/2026-07-05-agentic-research-pack-refresh/documentation-architecture.md)
- [LLM-WIKI system leaf](../../90.references/research/2026-07-05-agentic-research-pack-refresh/llm-wiki-system.md)
- [Memory hierarchy leaf](../../90.references/research/2026-07-05-agentic-research-pack-refresh/memory-hierarchy.md)
- [Predecessor convergence Task](../../04.execution/tasks/2026-07-26-agent-governance-canonical-convergence.md)

## Next handoff

- Keep the result on the local branch and do not push. Seek separate approval
  for the heading-contract correction, for independent review of this Task, and
  for the runtime and Compose drift task. A future Stage 03 memory-governance
  specification can build on the new memory-hierarchy leaf.
