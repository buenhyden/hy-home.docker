---
title: "External Research Refresh"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0185-TSK-0001"
parent_ids:
- "SPEC-0185"
- "SPEC-0185-PLAN-0001"
created: "2026-09-27"
---

# External Research Refresh

## Objective

Execute W1–W6 of the [Plan](../plan.md) against the [Spec](../spec.md).

## Inputs

- Owner execution request and 2026-09-27 explicit new-package/allocation approval.
- Baseline `f30b168e2fbb0959e4a31749935568fd5b3942f1`; fetched origin/main matches.
- Isolated branch `codex/research-refresh`; original checkout's dirty documents
  remain untouched. Its HEAD was `be949f338056ee05ca139ea72403576aa18f21d8`.
- Existing SPEC-0184 belongs to README navigation/language work on that checkout;
  no existing active package covers this research refresh. Allocate SPEC-0185,
  high_water 185 / next_number 186, without altering profiles or templates.

## Work Log

- 2026-09-27: Bootstrap, ownership, templates, identity and baseline inspected.
- 2026-09-27: Four primary-source research agents dispatched on disjoint topic groups; after package approval their scope extended to doc-writer edits of those same members. A fifth writer owns m0015/m0020 only. Controller owns README/index/Task/Registry/Git index.

### Preflight consistency

| Work/interface | Check | Result |
| --- | --- | --- |
| W1 | Inventory does not become an implementation audit | Scope bounded to research and document contract |
| W2 | Provider facts do not prove local adoption | All new internal statuses unassessed |
| W3 | Memory patterns do not restore retired wiki; service history retained | Separate historical boundary required |
| W4 | Research recommendations do not become policy | Route to existing owners |
| W5 | External security facts do not become internal diagnosis | No live/account/security scans |
| W6 | Gates and commits cover full task delta | Explicit baseline/path selection required |
| W2/W3 | Provider memory explanation vs knowledge lifecycle | m0012 comparison, m0011 lifecycle owner |
| W2/W5 | Provider hooks vs CI/Git/editor automation | m0012 native semantics, m0004 execution pipeline |
| W4/W5 | SDLC acceptance vs verification evidence | m0016 roles, m0019 evidence owner |
| W2–W5/W6 | Claims feed README/m0015 navigation | Controller integrates; authors do not edit shared files |

## Verification Evidence

Setup observations (not final completion evidence):

- `run-ci-gate.py --profile changed --explain`: PASS, exit 0; selected
  document-contract, document-graph, document-lifecycle and repository-integrity
  because Registry allocation is included. Local changed paths are unstaged,
  staged and untracked paths; this public CLI has no baseline/path-list option.
- Metadata check-changed, explicit base
  `f30b168e2fbb0959e4a31749935568fd5b3942f1` and explicit Registry, Stage 03
  index, Spec, Plan, Task paths: PASS, exit 0, selected 4 documents, violations 0.
- Initial public-gate observations: metadata check-active selected 445, violations 0;
  document links mode all failures 0; lifecycle/archive checks violations 0.
  Public gate exited 1: 492 document contract tests ran in 404.631s,
  with two failures. Identity-history scans all local refs and sees unrelated
  ADR-0044 on the README work branch, while this baseline owns ADR high-water 43.
  The non-mutation test also saw controller README/index edits during its run.
  This concurrency-contaminated initial run is FAIL, not final evidence;
  all affected gates will rerun on a stable isolated validation snapshot.
  These are setup observations before ongoing research edits, not a final snapshot.
- README self-check: PASS, exit 0; required eight H2 headings, protected file set,
  reversibly preserved previous body in historical quotation and immutable provenance fields.

All 21 members have completed current research; independent source review and stable-snapshot gates pass. Domain tests/coverage,
runtime checks, remote CI, entitlement and operational acceptance are NOT
APPLICABLE to this documentation task or explicitly outside authorization.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: Existing paths, identities, original body lines and all 11 service-history tables preserved | [RES-0002](../../../90.references/research/0002-agentic-engineering-research-pack/README.md) |
| 2 | W2 | PASS: Provider/instruction/model/harness research reviewed; instruction authoring distinctions added | [RES-0002](../../../90.references/research/0002-agentic-engineering-research-pack/README.md) |
| 2 | W3 | PASS: Compose/wiki/memory/service principles sourced without new internal assessment | [RES-0002](../../../90.references/research/0002-agentic-engineering-research-pack/README.md) |
| 2 | W4 | PASS: Documentation/SDLC/operations/tracker questions sourced and scoped | [RES-0002](../../../90.references/research/0002-agentic-engineering-research-pack/README.md) |
| 2 | W5 | PASS: CI/QA/security/verification claims sourced and independently reviewed | [RES-0002](../../../90.references/research/0002-agentic-engineering-research-pack/README.md) |
| 3 | W6 | PASS: All 100 future-check rows provide eleven fields, analytical axes and unassessed status | [RES-0002](../../../90.references/research/0002-agentic-engineering-research-pack/README.md) |
| 4 | W6 | PASS: Registered baseline-snapshot gate and affected follow-up checks passed; independent reviews approved | [RES-0002](../../../90.references/research/0002-agentic-engineering-research-pack/README.md) |
| 5 | W6 | PASS: Six original logical local commits plus 9a63d651a preserve reviewed research without remote mutation | [RES-0002](../../../90.references/research/0002-agentic-engineering-research-pack/README.md) |

### Promotion

The durable output is non-normative external research in RES-0002 at
`docs/90.references/research/0002-agentic-engineering-research-pack/README.md`
and its existing 21 members. No normative requirement, architecture or operating
rule was adopted, so no Stage 01/02/05 promotion is required. This Task owns only
execution evidence. Completion preserves the whole package under Stage 98 and
updates the Stage 03 index plus the direct RES-0002 README/m0015/m0019/m0020
consumers in the same change. Frozen package bodies and original outbound link
text will remain unchanged; the Retention Catalog names their source commit.

### Completion follow-through

The user approved the reported research result and then explicitly instructed
completion according to the original attachment. The first six commits completed
the research but left package lifecycle and temporary validation artifacts open.
This is a correction of that incomplete closeout, not a new implementation audit.
Independent attachment-to-result review identified two narrow content gaps:
instruction/policy/role/procedure/tool/style authoring examples and explicit
level/concern axes in several future rows. Commit `9a63d651a` fixes both in five
existing members. Independent follow-up review APPROVE; metadata selected 5,
violations 0; links 960 documents / 9,904 links, failures 0; all exits 0.

The previously displayed acceptance table was readable but not terminal-machine
valid: grouped W values, `PASS;` and plain owner IDs did not meet the completion
receipt contract. The table above now uses single W values, `PASS: ` and direct
owner links. The actual prior outcomes have not been upgraded or invented.
The owner approval and independent reviews support the registered lifecycle
edges; status changes do not grant remote or runtime authority.

### Final-snapshot verification

All authors froze writes before copying the exact 28 task paths to the isolated
validation clone at the same baseline. The source snapshot manifest SHA256 is
`41af5b30c06d4a19ba4df3c12f66c3e38c4aae6655c30d2d338fda8ddb929f33`.
The manifest maps repository-relative paths to SHA256, serializes with Python
`json.dumps(mapping, sort_keys=True)` and hashes UTF-8 bytes. All paths remain
staged there so the public changed selector covers the complete task delta,
including the new Spec/Plan/Task, rather than a later clean worktree.

- First stable attempt: FAIL, exit 1; m0009 had an original fenced-example
  comment incorrectly outside the new quotation, interpreted as a second H1.
  Put that comment inside the same quotation without changing its text.
- Next stable attempts: FAIL, exit 1; metadata passed, but four historical
  links targeted three quoted H3 headings. Explicit HTML IDs also failed because
  the registered parser only collects raw Markdown headings. The final fix
  retains those exact original H3 headings outside the quotation with an
  immediate historical-evidence marker; no original words changed.
- Final stable attempt: PASS, exit 0; includes those three restored headings
  and m0017 host-access recommendation. Metadata selected 445, violations 0;
  links mode all scanned 960 documents / 9,904 links, failures 0. Document
  lifecycle violations 0; 492 document-contract tests passed in 398.748s.
  Selected repository-integrity leaves also passed. Negative wrapper fixtures
  intentionally printed rejection diagnostics; the full runner exit was 0.
  No concurrent writes to the clone. Task-only evidence edits are checked
  separately against the same baseline before and after logical commits.
  These are documentation/contract outcomes, not fresh infrastructure adoption,
  deployed-state, provider/account or security acceptance evidence.
- Provider preservation/schema check: PASS, exit 0; 7 members, 49 individually
  traced claims, 19 future rows, exact original body hashes and stable metadata.
- Other author/reviewer checks: 25 infrastructure/memory claims and 19 future
  rows; 34 SDLC/documentation claims and 22 rows; 48 CI/security/V&V claims and
  25 rows; scope/history adds 15 future rows. Combined: 156 traced external
  claims and 100 full eleven-field future-check rows. Counts describe these
  authored tables, not source completeness or local implementation adoption.
- Cross-member checks: current source IDs unified for shared originals; source
  delimiters match headers; all member Related Documents link to pack README;
  `git diff --check` PASS, exit 0, using unfiltered Git diagnostics.
- Final worktree metadata with explicit baseline and all 28 task paths: PASS,
  exit 0; selected 27 documents, violations 0, transition overrides 0.
  All 27 non-Task file hashes match the passing full-gate snapshot; only this
  Task's outcome/commit evidence differs. Final diff whitespace check PASS. After the first five logical commits,
  worktree links mode all again PASS, exit 0: 960 documents, 9,904 links, zero
  failures. Final metadata uses all baseline-to-final paths, including commits.
  The last 27-document rerun caught one Task-only forbidden H2 introduced by
  the cleanup receipt (FAIL, exit 1). Moving it below Commit Ledger as H3 fixed
  the contract; the affected Task rerun PASS, exit 0, selected 1, violations 0.
  The other 26 documents and all research payload hashes were unchanged.
- No new research member, filename/ID replacement or other-pack edit. The
  sole protected-path delta is owner-approved spec allocation 185/186.

### Baseline isolation comparison

A task-owned validation clone at the identical baseline contains only main,
origin/main and the existing release tag; unrelated work branches are absent.
The exact failing identity-history test passes there: exit 0, one test in 8.659s.
No Registry ADR counter, test, policy or shared ref was changed to obtain this
comparison. This proves the local-ref condition, not a final research gate.

## Review Evidence

Independent setup review by package_review: no source defects; spec compliance
and source quality structurally approved. Its initial disposition was blocked pending
registered Registry/schema evidence. Reviewer observed diff whitespace check
exit 0, and confirmed minimal allocation avoids the independently issued 0184.
Focused explicit-base metadata then passed; public gate subsequently failed as recorded above. Reviewer follow-up approved
with follow-up: baseline Registry vs baseline history has no findings; baseline
vs all refs has ADR43<44 and SPEC183<184; task Registry vs all refs has only
ADR43<44. The task did not alter ADR allocation. H3 Preservation Declaration
retains the same 22 protected paths under the existing parser.
Independent scope/history and README/index review then found a real
README anchor collision was identified: old quoted headings preceded current
Sources/Traceability sections. The controller escaped the old heading markers,
kept legacy-only anchors, and verified exact body reconstruction (exit 0).
README anchor fix independently rechecked PASS. Scoped reviews approve m0015/m0020,
m0006/7/16/18 and m0005/9/11/21. The latter review confirms all 11 historical
m0021 tables are byte-identical. Separate CI/security review approves
m0004/14/17/19 after adding pack-navigation links, qualifying worker-only QA
limits and removing blank-quotation trailing spaces. Current source IDs for
Claude memory/subagents are unified across owners. Immutable metadata comparison
across all 21 members passes; only version/updated differ from baseline.
Provider review corrected an overbroad child-agent approval claim: interactive
CLI approval surfacing differs from noninteractive execution. The reviewer
accepted that fix and the explicit two-axis scopes. Model/rate/retirement source
samples match their originals. A final coverage note added privileged-container
and host-bind access recommendations, source detail and future target evidence
in m0017. Independent final whole-pack specification/quality review APPROVES,
with no open findings. The reviewer independently confirmed all 100 future rows,
protected metadata and primary-source samples; it did not claim exhaustive
URL reopening or gate execution. Final historical-heading compatibility changes
were separately re-read and approved. Parent baseline comparison confirms all
original nonempty body-line multiplicities retained across 21 members (exit 0).
Reviewers are separate from the five disjoint author groups; controller edits
were included in their final review.

## Commit Ledger

At the initial six-commit result `570e4ef43`, the 27 non-Task file SHA256 values
matched the passing full-gate snapshot after normal commits. Their sorted JSON mapping hashes to
`5dcf0c7fd2cdd07e0819fda6ed59e8ad9461cc5a9c39692036181cbf03a0d57a`; this historical digest is reproducible from that initial tree after excluding
this Task from the 28 baseline-to-final changed paths.

| Local commit | Concern / Plan unit |
| --- | --- |
| `9f2432766216cd5d0526be338043e71b3bf1d9fb` | Authorized package and minimal allocation / W1 |
| `bf775e5bdd364f3825c4d3b472e42f6376ab1651` | CI, quality, security, verification / W5 |
| `43a1d125d06f93ccf0324fa95d5700ca89bae8fb` | Documentation and SDLC / W4 |
| `a7dbf69c07d9f48f8704cf9eedd5615c28d4b2bc` | Compose and service research / W3 |
| `25c8e5c6326a6e915bacff14b190a9895e6450ca` | Agent/provider and memory research / W2–W3 |
| This commit: `docs(research): Integrate coverage navigation and validation evidence` | README/index/scope/history and final evidence / W6 |

Commit partition selected by actual new-anchor dependencies:

1. Register Spec/Plan/Task, Stage 03 index and minimal allocation.
2. CI/quality/security/verification: m0004/14/17/19 (W5).
3. Document lifecycle/architecture/SDLC: m0006/7/16/18 (W4).
4. Compose/service research: m0005/21 (part of W3).
5. Agent/provider plus linked knowledge/memory: m0001/2/3/8/9/10/11/12/13
   (W2 and remaining W3). These mutually link to new sections, so commit together.
6. Pack/index/scope/history integration: README, research index, m0015/m0020
   and final Task evidence (W6).

All required selected local checks have completed. A direct `cz` invocation
was unavailable (executable and module absent); the repository-pinned
Commitizen 4.15.1 was run via an isolated task-owned uv cache. All six draft-message checks PASS, exit 0. Normal automatic commit hooks remain enabled.

### Cleanup and Retention

After integrating author/reviewer receipts and validation results above, removed
44 explicitly identified task-owned scratch files: authoring/self-check scripts,
drafts, original backups, review diffs/reports and intermediate QA logs/manifests.
No repository scratch file or second progress ledger remains. Unknown-ownership
`/tmp/research-refresh-*` files were not removed. No bulk folder deletion, Git
clean, reset, stash, history rewrite or user-file cleanup was performed.

The exact validation clone `/tmp/hyhome-research-validation` and isolated pinned
Commitizen cache `/tmp/research-commitizen-cache` remain as reproducible local
validation/tool artifacts. They are outside the tracked deliverable, not another
research pack or progress authority. The managed worktree and six local logical
commits remain available; no push, PR, merge, tag, release or worktree removal.

## Rulings

- New package/allocation explicitly authorized by the owner; no other protected
  configuration change authorized. Newly introduced Spec/Plan/Task metadata
  initially retained the Registry-required draft state. Subsequent owner result
  approval and completion instruction now drive the registered forward edges;
  no historical approval date is invented.
- Scope describes future surfaces as candidates, never claims they exist based
  on this run. Approval, validation and historical observation dates are distinct.

## Deferred Items

All internal implementation, runtime, account and security assessments remain
separate future authorized work. Hosted CI, remote protection and paid/provider
execution are NOT RUN by scope. Domain-code tests/coverage are NOT APPLICABLE
because no implementation changed. Direct/all-files pre-commit is NOT RUN;
normal automatic commit hooks are retained. No tracked generated projection is
affected. Retired wiki generation is NOT RUN; Graphify regeneration is NOT RUN
because it is outside this external-only research scope, and no generated output
is added. Original shared refs still include the unrelated ADR-0044 history;
only the isolated canonical-baseline fixture excludes it. No claim of a passing
shared-ref full gate or protected-branch merge readiness is made.
