---
title: "Archive Disposition Consistency Assessment"
version: "0.1.0"
type: "reference/research-pack"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-15"
layer: "references"
artifact_id: "RES-0096"
parent_ids: []
created: "2026-09-15"
observed_at: "2026-09-15"
---

# Archive Disposition Consistency Assessment

## Question

Where do the Stage 98 archive policy, the Registry, the registered checks, and
the active documents that describe them agree, and where do they diverge, at
`main@e233d2a19a3a266e3535184a95c55222f9793c8e`? For each divergence, which
current owner resolves it, and does the resolution change meaning or only
describe the current state more accurately?

## Scope

- In scope: `.agents/governance/documentation-protocol.md` (Document Retention
  and Retirement), `docs/98.archive/README.md`, `docs/99.templates/registry.json`
  and its schema, `REQ-0026`, `AD-0030`, `ADR-0033`, `ADR-0035`, the SPEC-0177
  package, and the modules and tests under `scripts/lib/document_governance/`
  and `tests/lib/document_governance/` that enforce them.
- Out of scope: runtime services, Compose, hosted CI runs, and the other
  repositories whose archive models the operator compared. Their descriptions
  were comparison input only, and no count, test total, or identifier from them
  is carried here as a fact about this repository.

## Method

Every claim is split into one checkable statement and recorded on two axes that
are kept apart: consistency, and how the statement was verified. The levels are
`source read` (the governing text was read), `static code` (the enforcing code
was read), `reproduced` (a command or probe ran in this observation), and
`unverified`. A `source read` or `static code` row is not execution evidence.

Commands run on 2026-09-15 against the clean tree at the observed commit:

| Command | Result |
| --- | --- |
| `python3 -m unittest tests.lib.document_governance.test_archive tests.lib.document_governance.test_links tests.lib.document_governance.test_registry tests.lib.document_governance.metadata.test_reference tests.validation.lifecycle.test_equivalence` | exit 0, 216 tests |
| `python3 scripts/validation/check-document-corpus-lifecycle.py` | exit 0, `migrations=3 tombstones=140 preserved=200 decisions=286 recovery_rows=374 violations=0` |
| `python3 scripts/validation/check-document-links.py --mode all` | exit 0, `documents=885 links=6662 archive_direct_links_total=61 failures=0` |
| A regular-expression probe of `archive._CATALOG_PACKAGE`, `archive.retention_unit`, and `archive._ARTIFACT_IDENTIFIER` | An Incident bundle directory does not match the unit pattern, and neither `inc-2026-0001` nor an `.agents/` path matches the identifier pattern |
| `git diff --no-index` of each SPEC-0176 member at `d174fc50b^` against its preserved copy at `HEAD` | Every member differs in `version` and `status`; the Task also gained a paragraph and two table rows; every mode is `100644` |

The counts above are observations of that commit. They are not thresholds, and
the link total already differs from the `links=6655` the SPEC-0177 Task
recorded for W3 earlier the same day.

## Findings

### Consistency by review item

The item numbers A01 to A25 are the review checklist of this assessment, not
Registry identifiers.

| Item | Statement checked | Observed fact | Consistency | Level | Disposition |
| --- | --- | --- | --- | --- | --- |
| A01 Authority | The index owns navigation, the policy owns meaning, the Registry owns machine values | The index says so and defers to the policy, and then restates the policy's two disposition tables in Korean | Duplicate, with the policy named as owner | source read | Keep; SPEC-0177 W7 rewrites the index with the switch |
| A02 Six dispositions | Four retention classes and two route dispositions | Policy, `REQ-0026-FR-0013`, and `ADR-0035` agree; `PRESERVED_DISPOSITIONS` names the four classes | Consistent | static code | Keep |
| A03 Retention modes | Frozen body, sealed record, retain in place, Git history only | The Registry has no mode vocabulary; `sealed-record` is a lifecycle; no profile is Git-history-only (policy Transition item 6) | Local difference | source read | Keep; not a defect |
| A04 Stage boundary | Current control documents stay; individual forms move by profile | `ACTIVE_STAGE_PREFIXES` covers Stages 01, 02, 03, 05, and 90; whether a Stage 99 document can reach a terminal status was not checked | Unverified for Stage 99 | static code | Record |
| A05 First-use paths | A disposition directory exists only once used | `resolved/` is absent; `load_archive` admits it only at `adopted`; the index and policy Transition item 2 still say the Registry and loader do not know it | Stale description of implemented, inactive code | reproduced | Corrected in the change that records this assessment |
| A06 Units and members | A unit is a whole Spec package, a whole Incident bundle, or a standalone document | The catalog unit pattern matches Stage 03 packages only; coverage scans `*.md` only while `retired/90.references/data/` holds `data.yaml` members | Policy–implementation gap | reproduced | SPEC-0177 W4b |
| A07 Status and disposition | A unit's meaning decides its disposition | `validate_active_stage_occupancy` judges each document; `TERMINAL_DOCUMENT_STATUSES` excludes `resolved` and `published`, which SPEC-0177 records as out of scope | Policy-documented constraint | static code | SPEC-0178 for occupancy; the terminal-status gap stays recorded |
| A08 Completion and disposition approval | A finished Task can say so before its package is disposed | The policy directs a finished Task of an unfinished package to hold `in-progress`; `_validate_execution_states` constrains only `in-progress` and `blocked` Tasks | Status field contradicts the recorded fact by rule | static code | SPEC-0178 (completed Tasks only) |
| A09 Promotion receipt | One receipt owner | SPEC-0176's Task carries the receipt rows; the divergent handoff uses `branch_integration_receipts` | Consistent | source read | Keep |
| A10 Atomicity | Status change and move land in one result tree | `REQ-0026-FR-0009` and `ADR-0033` Decision 3 require it; the SPEC-0173 and SPEC-0176 completing commits edit status inside the move; pre-commit runs `run-ci-gate.py --profile changed` per commit | Consistent | reproduced | Keep |
| A11 Closure evidence | A resolved Incident carries a closure date | The `incident` profile lists `resolved_at` as optional and declares no status-conditional requirement, while `postmortem` requires `reviewed_at` at `published` | Gap | static code | Open; no approved owner yet |
| A12 Catalog | One row per unit naming what its class must name | W4 checks header, rows, class, and `Source`; the index has no catalog section yet, which is inert at `transition`; `Names` requires an uppercase identifier outside `retired` | Policy–implementation gap for `Names` | reproduced | SPEC-0177 W4b |
| A13 Git provenance | `Source` proves the original object | The check covers path, ancestry, and object type, not bytes, mode, or members; `ci-quality.yml` checks out with `fetch-depth: 0` | Partial by design (SPEC-0177 Behavior Contract 7) | static code | SPEC-0178 |
| A14 Freeze and allowed transforms | A preserved body is byte-identical to its body at the move | Completing commits change `version`, `status`, and Task evidence in the same commit, so no Git object holds the pre-move bytes; relative links are not rebased | Requirement–practice mismatch (`REQ-0026-FR-0012`) | reproduced | SPEC-0178 |
| A15 Legacy generations | A sealed shape is admitted only for a record present at base | Designed as SPEC-0177 W5; `sealed_section_shapes` appears nowhere in the tree; the Tombstone parser still requires the sealed headings | Approved, not implemented | static code | SPEC-0177 W5 |
| A16 Citation by target | Active documents cite the index and `completed/` now, and `resolved/` once adopted | `links.py` matches, with the adopted list behind the switch | Consistent | reproduced | Keep |
| A17 Source and exception order | The incident exception exists for preserved bodies | The exception admits every archive path, including route records; tests cover `retired/` only; runbooks do not inherit it; documents outside `docs/` reach Stage 98 only through `docs/README.md` (`entrypoint` mode) | Exception wider than its stated reason | static code | SPEC-0178 |
| A18 Reference syntax | Code examples are not links | `_unfenced_lines` skips fences and blanks inline code spans; reference, wiki, and HTML link support was not checked | Partially verified | static code | Record |
| A19 Link integrity | Historical links are judged in their own context | Outbound links of preserved bodies are skipped, not checked against their source snapshot; inbound links into them are checked; `architecture.py` rejects dangling, cross-type, and non-effective supersession | Local choice | static code | Record |
| A20 Templates and identity | One machine contract per identity | A Tombstone takes `tomb-<retired identity>` while its filename uses the separate `tombstone` allocation (policy Authoring Rule 8); that allocation's high water (234) was not reconciled against the 140 tracked Tombstones | Consistent in rule; count unverified | source read | Record |
| A21 Gates | A switch-gated rule is proven inert | Tests for W3, W4, and W6 assert inertness at `transition`; the corpus checks above report no violation | Consistent | reproduced | Keep |
| A22 Publishing and context | Archive bodies are not republished as current | No documentation site configuration is tracked; `llms.txt` names no archive path | Not applicable | reproduced | Keep |
| A23 Security and public routes | Archive route records are not HTTP routing | No public site or redirect configuration is tracked; secret handling follows `.agents/governance/approval-boundaries.md` | Not applicable | source read | Keep |
| A24 Stale facts and counts | Current text matches the current tree | Dated counts in the SPEC-0177 Task are dated observations; the transition tables of the index and the policy describe implemented code as absent (A05, A12); the Task's Commit Ledger ends before W2 approval | Stale current descriptions | reproduced | Corrected in the change that records this assessment |
| A25 Integration | Existing work is reused rather than duplicated | SPEC-0177 W5, W7, and W8 remain; `ADR-0035` is `proposed`; the policy changes this assessment surfaced are proposed in a separate draft package instead of widening SPEC-0177 | Consistent | source read | SPEC-0177 amended for W4b; SPEC-0178 drafted |

### External sources

Each row states what the source supports and what it does not. Retrieval was
read-only on 2026-09-15.

| Source | Supports | Does not establish |
| --- | --- | --- |
| Git `gitrevisions` | `<rev>:<path>` names the blob or tree at that path in that commit | How long the object survives |
| Git `git-cat-file` | `-e` and `-t` confirm an object exists locally and its type | That a missing object is absent upstream rather than outside a shallow or partial clone |
| Git `git-gc` | Unreachable objects are pruned after the prune grace period (default two weeks) once no reflog holds them | Hosting-side retention |
| Git `git-clone` | `--depth` truncates history and `--filter=blob:none` omits blobs until needed | The failure mode when a check needs an omitted object |
| Nygard, *Documenting Architecture Decisions* | A reversed decision is kept and marked superseded with a reference to its replacement | Where a superseded record lives, or any prohibition on linking to it as history |
| Google SRE Book, *Postmortem Culture* | Postmortems are reviewed and kept in a shared repository and read later | Who owns action items |
| Google SRE Workbook, *Postmortem Culture* | Action items need an owner and a tracking number | A formal definition of closing a postmortem |
| PREMIS ontology | Not retrieved: HTTP 403 | Any claim about fixity or transformation events; none is made here |
| RFC 9110 §15.4.2, §15.4.9, §15.5.11 | 301 and 308 assign a new permanent URI; 410 marks intentional permanent removal and need not be kept | Anything about relative links inside a repository |
| GitHub, *Removing sensitive data from a repository* | Rotate the secret first; a rewrite changes every later commit identity; clones, forks, and cached views may retain the data | Squash or reflog behaviour |
| JSON Schema, *Conditionals*, *Annotations*, *Type* | `if`/`then` makes a field conditionally required; `default` and `deprecated` do not validate; `format` is an annotation unless the validator asserts it | The behaviour of a specific validator |
| Diátaxis | Reference and explanation serve different reader needs and degrade when mixed | Archives or supersession |
| Write the Docs, *Docs as Code* | Documentation uses version control, review, and automated tests | Which checks to run |
| CommonMark 0.31.2 §4.4, §4.5, §4.7, §6.1, §6.3 | Code blocks and fences are literal text; code spans bind tighter than link brackets; reference definitions resolve reference links | GitHub Flavored Markdown extensions |

## Sources

- <https://git-scm.com/docs/gitrevisions>
- <https://git-scm.com/docs/git-cat-file>
- <https://git-scm.com/docs/git-gc>
- <https://git-scm.com/docs/git-clone>
- <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
- <https://sre.google/sre-book/postmortem-culture/>
- <https://sre.google/workbook/postmortem-culture/>
- <https://www.loc.gov/standards/premis/ontology/index.html> (not retrieved)
- <https://www.rfc-editor.org/rfc/rfc9110.html>
- <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository>
- <https://json-schema.org/understanding-json-schema/reference/conditionals>
- <https://json-schema.org/understanding-json-schema/reference/annotations>
- <https://json-schema.org/understanding-json-schema/reference/type>
- <https://diataxis.fr/>
- <https://www.writethedocs.org/guide/docs-as-code/>
- <https://spec.commonmark.org/>

## Implications

- The six dispositions, the retention classes' names, and the prohibition on a
  second recovery ledger are local design choices. No retrieved source requires
  them, and none forbids citing a superseded decision as history; the
  repository's citation limit is its own rule against a replaced rule returning
  through a citation.
- Items A06 and A12 are gaps between `ADR-0035`, which already names an Incident
  bundle and a corrective-work owner, and the catalog check that cannot record
  either. They change no meaning, so SPEC-0177 takes them as W4b.
- Items A08, A14, and A17 change meaning: which statuses may stand in an active
  package, what "byte-identical" guarantees, and which archive paths an incident
  may cite. They are proposed in `ADR-0036` and SPEC-0178, which depend on
  SPEC-0177 completing.
- Items A05 and A24 describe implemented but inactive code as absent. Correcting
  that wording changes no rule.
- Item A11 has no owner in either package and stays open.

## Traceability

- [Document retention policy](../../../../.agents/governance/documentation-protocol.md#document-retention-and-retirement)
- [REQ-0026 Document Retention and Retirement](../../../01.requirements/0026-document-retention-and-retirement.md)
- [ADR-0035 Stage 98 Retention Classes and Route Dispositions](../../../02.architecture/decisions/0035-stage-98-retention-classes-and-route-dispositions.md)
- [ADR-0036 Archive Occupancy, Route Citation, and Frozen Identity](../../../02.architecture/decisions/0036-archive-occupancy-citation-and-frozen-identity.md)
- [SPEC-0177 Archive Disposition Enforcement](../../../03.specs/0177-archive-disposition-enforcement/spec.md)
- [SPEC-0178 Archive Occupancy, Route Citation, and Frozen Identity](../../../03.specs/0178-archive-occupancy-citation-and-frozen-identity/spec.md)

## Limitations

- This is a dated observation of one commit. It does not record a hosted CI run,
  an all-files or full-profile run, or any runtime state.
- Preserved bodies that predate the Retention Catalog carry no recorded source,
  so their identity with an original object is not assessed.
- PREMIS was not retrieved, so no preservation-standard conformance is claimed
  or implied.
