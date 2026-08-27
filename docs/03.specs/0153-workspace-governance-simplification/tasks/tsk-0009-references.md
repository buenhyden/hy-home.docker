---
profile_id: task
status: completed
artifact_id: task-0153-0009
artifact_type: task
parent_ids:
  - SPEC-0153
  - plan-0153
created: 2026-08-23
updated: 2026-08-23
---

# Task 0009: References

## Objective

Converge Stage 90 to non-normative Research, Audit, and Data packages with numeric prefixless paths and generator-owned Data outputs.

## Inputs

- [Specification](../spec.md)
- [Implementation Plan](../plan.md)
- Frozen Migration 0003 rows `mig-0003-r0450` through `mig-0003-r0565` (recovery evidence is retained in Git/Stage 98 rather than linked as current authority).
- Stage 99 Research, Audit, Data, and generated profiles.

## Work Log

| Event | Actual result |
| :--- | :--- |
| Preflight | Corroborated stale Graphify evidence against live tracked Stage 90, Stage 00, Stage 99, and frozen Migration rows `mig-0003-r0450` through `mig-0003-r0565`: 116 rows, 105 renames, 11 deletions. |
| Classification | Classified all 116 rows: 38 Audit targets, 23 Data targets, 44 Research targets, and 11 registered deletions. The unregistered noncurrent `data/governance/document-corpus-lifecycle/README.md` routing envelope was also removed so only numeric packages remain. |
| Native moves | Executed all 105 registered renames with literal native `git mv`; no compatibility copy or redirect was created. |
| Consumers | Rewrote Migration-declared current consumers and generator/check/write paths. Generated/historical `graphify-out/**`, frozen Stage 98 recovery evidence, and other noncurrent snapshots were excluded. |
| Review fix round 1 | Reproduced all nine Important review findings with focused mutations, then hardened Stage 90 traversal/link/authority/redirect validation, generator I/O/process safety, Registry parent cardinality/generated classification, exact repo topology, duplicate-list rejection, and bounded active-consumer routing. |
| Review fix round 2 | Closed `C0/I4/M0`: rewrote all 12 live nonnumeric Data-route links plus DATA-0083 broken local links, moved rendered-body classification onto shared Markdown masking, added clause-local authority and strict redirect grammar, rejected immediate/partial generator EOF, and restored strict non-Stage90 parent/generated classification behavior. |
| Review fix round 3 | Closed the remaining Python review finding `C0/I1/M0`: a fence-info `<!--` can no longer leak comment state, negation is scoped to the authority predicate rather than an unrelated adjective, and same-line substantive prose prevents a `# Deprecated` document from being classified as redirect-only. |
| Review fix round 4 | Closed the plain-path redirect regression `C0/I1/M0`: replaced the unregistered-package false-green with a registered-package mutation and allowed exactly one parser-owned Markdown link or one confined raw relative/repository path as the complete transition destination. |
| Review fix round 5 | Closed the Markdown-target safety asymmetry `C0/I1/M0`: Markdown links and raw paths now share one confined decoded-local-path predicate, so absolute, escaping, and percent-encoded scheme targets are rejected identically. |
| Implementation commit | Recorded the approved Stage 90 package simplification and its validators as `49522aa1d782838706bd558b8e139b107918ffee`. |

## Verification Evidence

| Check | Command | Result |
| :--- | :--- | :--- |
| RED | `PYTHONPATH=. python3 -m unittest tests.validation.test_reference_packages -v` | EXPECTED FAIL — 7/7 assertions reported the missing Task 9 reference authority before production implementation existed. The first minimal module skeleton remained RED on its unresolved shared rendered-link parser API, so no false GREEN was recorded. |
| Focused GREEN | `PYTHONPATH=. python3 -m unittest tests.validation.test_reference_packages tests.validation.test_generate_llm_wiki tests.validation.test_llm_wiki_retiring_pack_exclusion -q` | PASS — 19 tests, including path/category/identity/authority mutations and generator wrapper parity. |
| Review RED | `python3 -m unittest tests.validation.test_reference_packages -v` plus focused generator, metadata, and repository-topology mutations | EXPECTED FAIL — unsafe symlink/FIFO traversal, payload/encoded retired links, authority negation/passive cases, active retired consumers, unsafe generator leaves/process bounds, global empty-parent relaxation, duplicate foundation sources, and retired repo roots were each reproduced before their fixes. |
| Review GREEN | `python3 -m unittest tests.validation.test_reference_packages tests.validation.test_generate_llm_wiki tests.validation.test_llm_wiki_retiring_pack_exclusion tests.validation.test_reference_stage_repo_contract -v` | PASS — 36 tests. The metadata/Registry mutation slice separately passed 8/8. |
| Generator write/check | `python3 scripts/knowledge/generate-llm-wiki.py --write`; then `--check` | PASS — DATA-0082 index and DATA-0076 coverage are fresh under their registered packages. |
| Wrapper parity | Both shell adapters with `--check` | PASS — both thin adapters delegate to the canonical candidate/render/check authority. |
| Changed metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref HEAD` | PASS — `selected=149 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Stage 90 authority | `validate_current_references(...)`; `validate_active_reference_consumers(...)` | PASS — `reference_findings=0 active_consumer_findings=0`; all package payload Markdown and indexes are included. |
| Link alignment | Prior `python3 scripts/validation/check-document-links.py --mode alignment` snapshot | Diagnostic only — its 42 residual count omitted seven Task 9 payload links identified by review. Those links are now rewritten and the Task 9 parser-owned normalized-target scan is zero; the broad alignment diagnostic was not rerun per controller direction. |
| Static | Ruff, `py_compile`, `bash -n`, `git diff --check HEAD`, graphify diff | PASS. A separate script-manifest invocation produced no output for 60 seconds and was interrupted rather than treated as a false pass. |
| Round-2 RED | Focused payload/parser, generator EOF, and metadata mutations | EXPECTED FAIL — 3 payload/parser tests; 4 candidate/current-output immediate/partial EOF cases; Guide/Policy/Runbook/Incident root permission and generated root README classification. |
| Round-2 focused GREEN | Combined references/generator/wrapper/topology suite; metadata slice | PASS — 40 combined tests and 49 metadata tests. Generator module was 16/16 within the combined suite. |
| Round-2 generator parity | Canonical, index wrapper, and coverage wrapper with `--check` | PASS — all three reported both generated outputs fresh. |
| Round-2 metadata | `check-document-metadata.py --mode check-changed --base-ref HEAD` | PASS — `selected=150 violations=0 legacy_exceptions=0 transition_overrides=0`. Guide, Policy, and Runbook are traced to `SPEC-0096`. |
| Round-2 links | Parser-normalized scan of every live Stage 90 Markdown payload/index | PASS — `retired_rendered_links=0`; DATA-0083 missing local links zero through `reference_findings=0`. |
| Round-3 RED | Exact shared-parser and References mutations | EXPECTED FAIL — 2/2 tests reproduced all three reviewed cases: leaked comment state from a fence info string, unrelated `not descriptive` suppressing an affirmative override, and same-line substantive Deprecated prose classified as redirect-only. |
| Round-3 targeted GREEN | Exact two-test rerun; `tests.validation.test_document_links.DocumentGraphTests` | PASS — 2/2 exact tests and 16/16 affected shared parser tests. The complete shared link module ran 29 tests with 3 pre-existing repository-level failures in active-publication, Spec-0137 traceability, and cross-stage alignment diagnostics; no broad-pass claim is made. |
| Round-3 combined GREEN | References/generator/wrapper/topology focused suite | PASS — 40/40 tests in 69.703 seconds. Generator code was unchanged in round 3, so its round-2 three-entrypoint parity evidence remains applicable. |
| Round-3 contracts | Current References/active-consumer validators; changed metadata | PASS — `reference_findings=0`, `active_consumer_findings=0`, and `selected=150 violations=0 legacy_exceptions=0 transition_overrides=0`. |
| Round-3 static | Ruff, `py_compile`, bounded `git diff --check HEAD`, frozen hash, graphify status/diff | PASS — Migration SHA remains `271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9`; `graphify-out/**` is clean and was treated as stale advisory evidence. |
| Round-4 RED | Registered-package end-to-end mutation plus direct redirect classifier | EXPECTED FAIL — 2/2 tests showed that a plain `Moved to ../0002-.../.` transition was not classified as redirect-only; the registered-package mutation produced no redirect finding, eliminating the previous 0099 false-green. |
| Round-4 targeted GREEN | Same two exact tests; `tests.validation.test_document_links.DocumentGraphTests` | PASS — 2/2 exact tests and 16/16 shared link-parser tests. Positive raw relative and repository-root paths pass; substantive suffixes, absolute/escaping or percent-encoded scheme paths, and multiple destinations remain rejected. A self-review encoded-scheme mutation was RED 1/1 before the decoded-token restriction and GREEN afterward. |
| Round-4 combined GREEN | References/generator/wrapper/topology focused suite | PASS — 40/40 tests in 44.464 seconds after the final safety mutation. No broad or full repository gate was run. |
| Round-4 contracts/static | Current References/active-consumer validators, changed metadata, Ruff, `py_compile`, diff check, frozen hash, graphify | PASS — findings `0/0`, metadata `selected=150 violations=0`, Migration SHA exact, and graphify status/diff empty. |
| Round-5 RED | Direct redirect-classifier Markdown safety mutations | EXPECTED FAIL — absolute `/docs/...`, repository-escaping `../../../../outside/`, and percent-encoded `https://...` Markdown targets all incorrectly returned redirect-only (`3/3` failing subtests). |
| Round-5 targeted GREEN | Exact classifier/end-to-end tests; `tests.validation.test_document_links.DocumentGraphTests` | PASS — exact 2/2 and shared parser 16/16. Safe relative/repository-root raw paths and Markdown links remain accepted; substantive, multiple, absolute, escaping, and encoded-scheme targets are rejected in both forms. |
| Round-5 combined GREEN | References/generator/wrapper/topology focused suite | PASS — 40/40 tests in 42.296 seconds. No broad or full repository gate was run. |
| Round-5 contracts/static | Current References/active-consumer validators, changed metadata, Ruff, `py_compile`, diff check, frozen hash, graphify | PASS — findings `0/0`, metadata `selected=150 violations=0`, Migration SHA exact, and graphify status/diff empty. |
| Independent reviews | Task 9 specification and Python/validator reviews | APPROVED — specification `C0/I0/M0`; Python/validator final round `C0/I0/M0`. Five mutation-driven review rounds closed every reported Important finding without widening the repository gate. |
| Controller verification | Focused 40-test suite; shared `DocumentGraphTests`; metadata; three generator entrypoints; References validators; static and frozen evidence checks | PASS — 40/40 and 16/16; metadata `selected=150 violations=0`; generator checks fresh; findings `0/0`; Ruff, `py_compile`, `bash -n`, diff check, frozen SHA, and graphify exclusion all pass. |
| Frozen authority | `sha256sum docs/98.archive/migrations/0003-workspace-governance-simplification.md` | PASS — `271f21c50cf4ab765422ee552de244a4340c160e53149231eb6be45f03476ab9`. |

## Review Evidence

Round-1 inputs contained `C0/I9/M0`; all nine Important findings have targeted RED/GREEN dispositions. Self-review completed against the exact Task 9 brief and both review artifacts. The live root set is exactly `audits/`, `data/`, and `research/`; package paths are numeric, prefixless, and date-free; stable IDs are category-correct; Stage 90 remains non-normative; every current Markdown payload/index is scanned through normalized parser targets; generators use one bounded canonical authority; standalone parents are limited to Research/Audit/Data; current consumers no longer name retired roots; and historical/generated graph snapshots remain untouched.

Round-2 inputs contained `C0/I4/M0`; all four Important findings now have targeted GREEN evidence. Shared Markdown masking prevents inline/fenced comment delimiters from hiding later assertions, negation is predicate-local, substantive Deprecated documents are not redirects, generator short reads fail closed, and only exact registered numeric Data package READMEs retain Data classification when `generated_by` is present.

Round-3 input contained `C0/I1/M0`; the one Important finding covered three exact parser/classifier cases. A visible opening fence now owns its complete info string before HTML-comment masking; coordinated predicates reset negation only when the preceding predicate is unrelated to authority; and redirect transitions must consist only of an allowed transition prefix, exactly one local Markdown link, and optional terminal punctuation. The exact RED mutations and both targeted/shared GREEN reruns are recorded above.

Round-4 input contained `C0/I1/M0`; the prior unregistered `0099-redirect` fixture could pass through the independent unregistered-package finding. The end-to-end mutation now preserves the frontmatter of a registered Research package and replaces only its body. Redirect transition grammar accepts one exact Markdown destination or one raw path token whose parser-normalized target is neither absolute nor outside the repository; decoded raw tokens must also remain path-only, preventing a percent-encoded URL scheme from bypassing the raw grammar. The full line permits only an approved prefix and optional terminal punctuation.

Round-5 input contained `C0/I1/M0`; the Markdown branch previously validated only exact link syntax while raw targets also validated confinement. Both branches now call the same immutable `DocumentLink` predicate, which requires no unsafe location flags and a decoded path-only target. Exact grammar and multiplicity checks remain outside that shared safety predicate.

Final independent reviews approved the Task 9 implementation at `C0/I0/M0` for both specification conformance and Python/shell/validator quality. Controller verification independently reproduced the focused 40/40 and shared parser 16/16 passes, zero current-reference and active-consumer findings, zero changed-metadata violations, fresh generator outputs through all three entrypoints, static-check passes, the frozen Migration hash, and a clean `graphify-out/**` exclusion.

The final combined bounded state available before handoff was: the round-5 focused 40-test suite PASS; affected shared parser tests 16/16 PASS; changed metadata `selected=150 violations=0`; round-2 canonical generator plus both wrapper `--check` commands PASS with no generator change in rounds 3–5; `reference_findings=0`; `active_consumer_findings=0`; `retired_rendered_links=0`; `git diff --check HEAD` PASS; frozen SHA exact; and no `graphify-out/**` status or diff.

## Commit Ledger

- `49522aa1d782838706bd558b8e139b107918ffee` — `refactor(references): simplify evidence packages`

## Rulings

- Migration 0003 is frozen structural authority and must remain byte-identical.
- Stage 90 is supplementary evidence and cannot override Stages 00, 01, 02, 03, or 05.
- Deprecated redirect bodies and compatibility copies are not retained.
- Superseded evidence remains connected by stable `supersedes` and `superseded_by` IDs; issued IDs are not reused.

## Deferred Items

- Link-alignment residuals outside Task 9 and the intentionally unrun full repository gate remain with their declared later owners.
- The script-manifest validator did not return within the bounded 60-second diagnostic window; no success claim is made for that invocation.
