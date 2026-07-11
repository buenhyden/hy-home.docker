---
status: active
artifact_id: plan:2026-07-12-agentic-audit-harness-consolidation
artifact_type: plan
parent_ids:
  - spec:128-agentic-audit-harness-consolidation
---

<!-- Target: docs/04.execution/plans/2026-07-12-agentic-audit-harness-consolidation.md -->

# Agentic Audit Harness Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-establish the 2026-07-05 audit pack as current implementation
truth and prevent deterministic remediation closures from silently regressing
to stale or overbroad claims.

**Architecture:** Preserve all audit pack paths and the 11-report, 161-row
structural contract. Add a separate JSON-backed semantic closure validator,
split scoped and broad security readiness signals, and wire the contracts into
existing local and CI quality gates.

**Tech Stack:** Python 3.12 standard library, JSON, Bash, Markdown, YAML,
`unittest`, repository generators, and GitHub Actions.

## Overview

This plan turns approved Spec 128 into six independently testable and reviewed
implementation units. It keeps historical evidence stable, restores the
canonical audit's current-state accuracy, and adds deterministic protection
against known semantic regressions.

## Context

The canonical pack passes its 11-report/161-row structure checks, but some
criteria still describe the pre-Task-8 implementation. Typed metadata,
controlled pre-commit execution, and provider/CI synchronization therefore
exist in tracked source while parts of the audit still call them future or
missing work. The security readiness generator also treats one scoped npm gate
as broad OSV/SCA coverage.

## Goals & In-Scope

- Clarify canonical, historical-snapshot, and superseded audit roles without
  moving paths.
- Reassess every canonical criterion against current tracked evidence.
- Enforce eleven deterministic remediation closures with an offline validator.
- Separate scoped vulnerability gating from broad dependency and image scans.
- Integrate semantic freshness into local repository contracts and the existing
  read-only CI quality job.
- Regenerate canonical evidence and close through independent reviews.

## Non-Goals & Out-of-Scope

- Runtime Compose, infrastructure, deployment, secret, remote GitHub,
  provider-global, `.gemini`, entitlement, and model-policy changes.
- Full historical metadata migration, semantic model scoring, live provider
  validation, CD, broad SCA execution, image scanning, SBOMs, provenance,
  signing, Scorecard, or runtime rehearsal.
- Physical audit pack relocation or a second current-state report set.

## Global Constraints

- The 2026-07-05 pack remains the only current agentic implementation audit.
- The 2026-07-03/04 packs remain dated evidence; preserve their original
  counts, commands, findings, and chronology.
- The 2026-07-07 pack remains mapping-only and `superseded`.
- Retain exactly 11 criterion reports, 161 unique IDs, and ten fields per row.
- Structural completeness and semantic freshness remain separate checks.
- Assertions cover deterministic completed remediation only; never infer
  runtime, entitlement, global config, network, or remote GitHub facts.
- A scoped Storybook `npm audit` proves neither broad SCA nor image scanning.
- No Docker Compose runtime, infrastructure state, deployment, secret, remote
  GitHub, `.gemini`, provider entitlement, or model-policy mutation.
- Specs 124-127 remain draft and approval-gated.
- Use `apply_patch`, TDD for code, and logical Conventional Commits.
- Never run direct all-files pre-commit. Use only the controlled wrapper at the
  final clean-worktree gate and record Git-visible evidence.
- Run Graphify after code changes when available; treat it as advisory.

---

## File Responsibility Map

| File | Responsibility |
| --- | --- |
| `docs/90.references/audits/README.md` | Canonical/snapshot/superseded routing. |
| `docs/90.references/audits/2026-07-03-*/*.md` | Preserved 2026-07-03 snapshot evidence. |
| `docs/90.references/audits/2026-07-04-*/*.md` | Preserved 2026-07-04 snapshot evidence. |
| `docs/90.references/audits/2026-07-05-*/*.md` | Current overview and criterion rows. |
| `scripts/validation/agentic-audit-semantic-contract.json` | Deterministic closure assertions. |
| `scripts/validation/check-agentic-audit-semantic-freshness.py` | Fail-closed semantic validator. |
| `tests/validation/test_agentic_audit_semantic_freshness.py` | Semantic unit/adversarial tests. |
| `scripts/validation/generate-security-automation-readiness.sh` | Scoped/broad security readiness. |
| `tests/validation/test_security_automation_readiness.py` | Security signal regressions. |
| `scripts/validation/generate-audit-implementation-matrix.sh` | Derived structural/semantic summary. |
| `scripts/validation/check-repo-contracts.sh` | Local gate orchestration. |
| `.github/workflows/ci-quality.yml` | Named tracked CI semantic step. |
| `scripts/README.md` | Script ownership and usage. |
| `docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md` | Durable execution/review evidence. |

## Work Breakdown

| Task | Description | Target | Validation |
| --- | --- | --- | --- |
| T-AHC-001 | Clarify lifecycle routes and snapshot interpretation. | VAL-AHC-001/002 | Exact headings, banners, preserved literals. |
| T-AHC-002 | Reassess canonical rows and overview. | VAL-AHC-003/004 | 11/161 and exact current distribution. |
| T-AHC-003 | Add semantic closure contract and tests. | VAL-AHC-005 | RED/GREEN tests and 11-assertion pass marker. |
| T-AHC-004 | Split scoped vulnerability readiness from broad SCA/images. | VAL-AHC-006 | Exact 13 controls and negative overclaim tests. |
| T-AHC-005 | Integrate semantic freshness locally and in tracked CI. | VAL-AHC-004/007 | Named gates and generated semantic summary. |
| T-AHC-006 | Regenerate, run full QA/wrapper, and close evidence. | VAL-AHC-008/009/010 | Fresh outputs and clean independent reviews. |

## Task 1: Audit Lifecycle Organization

**Files:** root audit README; every Markdown leaf in the 2026-07-03 and
2026-07-04 packs; execution task evidence.

**Interfaces:** Produces exact headings `## Canonical Current Audit`,
`## Dated Historical Snapshots`, `## Supersession Ledgers`, and one snapshot
boundary block on each dated report.

- [ ] **Step 1: Capture historical literals before editing**

```bash
rg -H '930|948|872|1,073|6 workflows|failures=2|active 19|completed 16|superseded 2' docs/90.references/audits/2026-07-0{3,4}-* | LC_ALL=C sort > /tmp/ahc-historical-before.txt
```

- [ ] **Step 2: Replace the root routing sections with exact content**

```markdown
## Canonical Current Audit

- Label: `Agentic engineering implementation audit references`
- Target: `./2026-07-05-agentic-engineering-implementation-audit-pack/README.md`
- Role: the sole current implementation-status audit.

## Dated Historical Snapshots

- `Workspace document contract audit references` -> `./2026-07-03-workspace-document-contract-audit-pack/README.md` — evidence as of 2026-07-03; not current corpus truth.
- `Document restructure audit references` -> `./2026-07-04-document-restructure-audit-contract-archive/README.md` — evidence as of 2026-07-04; not current corpus truth.

## Supersession Ledgers

- `2026-07-07 implementation audit update mapping` -> `./2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md` — mapping-only history; never a current status, count, or recommendation source.
```

Render each label/target pair as a normal Markdown link in the actual audit
index.

- [ ] **Step 3: Add a boundary to every historical report**

Insert after `## Overview`, substituting the correct date:

```markdown
## Evidence Snapshot Boundary

- **Evidence as of**: 2026-07-03
- **Current implementation route label**: `canonical agentic implementation audit`
- **Current implementation route target**: `../2026-07-05-agentic-engineering-implementation-audit-pack/README.md`
- **Citation rule**: Preserve the counts, findings, commands, and dispositions below as dated evidence. Do not cite them as the current workspace state without current tracked-source revalidation.
```

Render the route label and target as one Markdown link in each actual report.

Rename the 2026-07-03 README's `Planned References` to `Included Reports`.

- [ ] **Step 4: Verify preservation**

```bash
rg --files-without-match '^## Evidence Snapshot Boundary$' docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/*.md docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/*.md
rg -H '930|948|872|1,073|6 workflows|failures=2|active 19|completed 16|superseded 2' docs/90.references/audits/2026-07-0{3,4}-* | LC_ALL=C sort > /tmp/ahc-historical-after.txt
diff -u /tmp/ahc-historical-before.txt /tmp/ahc-historical-after.txt
bash scripts/validation/check-repo-contracts.sh
git diff --check
```

Expected: `rg --files-without-match` and `diff` produce no output; contracts
have zero failures.

- [ ] **Step 5: Commit**

```bash
git add docs/90.references/audits docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md
git commit -m "docs(audits): clarify audit lifecycle routes"
```

## Task 2: Canonical Current-State Reassessment

**Files:** canonical overview; DML, QAF, AUT reports; HAR, LOOP, PIC, WRE, and
agent/model reports where completed-task future tense is stale; generated audit
matrix; task evidence.

**Interfaces:** Produces exact state distribution `Implemented=67`,
`Partial=69`, `Missing=14`, `Not Applicable=2`,
`Needs Revalidation=9`.

- [ ] **Step 1: Reproduce structural-pass/semantic-stale baseline**

```bash
python3 scripts/validation/audit_criterion_contract.py
rg -n 'wrapper.*(absent|does not yet exist)|Task 9 will|Task 10 may|no typed semantic metadata parser|No `artifact_id` exists|Task 5 remains' docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack
```

- [ ] **Step 2: Update deterministic DML closures**

Set `DML-01`, `02`, `03`, `04`, `05`, `07`, `08`, `11`, and `14` to
`Implemented`, depth `3`, disposition `Retain`. Cite metadata profiles,
checker, tests, T-AER-008/012, active-chain scope, transition overrides, and
referential-integrity hardening. Keep DML-09/12 Partial and do not claim full
historical-corpus migration.

- [ ] **Step 3: Update wrapper closures**

Set QAF-12 and AUT-09 to `Implemented`, depth `3`, disposition `Retain`, citing
the wrapper, its 29-case fake-hook suite, and T-AER-009. Preserve its exact
Git-visible/non-ignored observation boundary.

- [ ] **Step 4: Correct completed provider/task future tense**

For HAR-02/04, LOOP-02, PIC-03/04/05/15 and related summaries, replace “Task
10 may/will” with current provider sync, semantic parity, hook parity, and CI
evidence. Keep Partial where native acceptance, `.gemini` adoption, or live
execution remains unproved. Replace stale Task 5 lifecycle wording with final
PASS/APPROVED evidence.

- [ ] **Step 5: Rewrite overview and regenerate**

The overview must distinguish implemented changed/new metadata and wrapper;
advisory historical metadata inventory; partial provider/eval; missing
runtime/CD/broad supply chain; and Needs Revalidation live/remote facts.

```bash
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/report-audit-pack-coverage.sh --check
python3 scripts/validation/audit_criterion_contract.py
rg -n 'Implemented \| 67|Partially Implemented \| 69|Gap / Not Implemented \| 14|Not Applicable \| 2|Unknown / Needs Revalidation \| 9' docs/90.references/data/governance/audit-implementation-matrix.md
git diff --check
```

- [ ] **Step 6: Commit**

```bash
git add docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack docs/90.references/data/governance/audit-implementation-matrix.md docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md
git commit -m "docs(audits): refresh canonical implementation status"
```

## Task 3: Semantic Freshness Validator

**Files:** create JSON contract, Python validator, unit test module; update task
evidence.

**Interfaces:** Produces
`validate_semantics(repo_root: pathlib.Path, contract_path: pathlib.Path) -> SemanticValidationResult`
and `audit_semantic_freshness: PASS assertions=11 failures=0`.

- [ ] **Step 1: Write failing tests**

```python
class AgenticAuditSemanticFreshnessTests(unittest.TestCase):
    def test_current_repository_contract_passes(self):
        result = module.validate_semantics(ROOT, CONTRACT)
        self.assertEqual(11, result.assertion_count)

    def test_wrong_required_state_fails(self):
        self.mutate_row("QAF-12", "Implemented", "Missing")
        self.assert_failure("QAF-12", "required state Implemented")

    def test_missing_required_evidence_fails(self):
        self.remove_evidence("scripts/validation/run-agent-precommit-all-files.sh")
        self.assert_failure("QAF-12", "required tracked evidence")

    def test_completed_task_described_as_future_fails(self):
        self.append_to_report("QAF-12", "Task 9 will add wrapper")
        self.assert_failure("QAF-12", "forbidden stale phrase")

    def test_wrong_lifecycle_heading_fails(self):
        self.replace_index_heading("## Canonical Current Audit", "## Current References")
        self.assert_failure("audit index", "required heading")

    def test_path_escape_is_rejected(self):
        self.contract["assertions"][0]["required_evidence_paths"] = ["../outside"]
        self.assert_failure("unsafe repository-relative path")
```

The fixture copies required tracked files to a temporary Git repository.

- [ ] **Step 2: Run RED**

```bash
python3 -m unittest tests.validation.test_agentic_audit_semantic_freshness -v
```

Expected: FAIL because module/contract do not exist.

- [ ] **Step 3: Create the exact JSON shape**

```json
{
  "schema_version": 1,
  "audit_index": "docs/90.references/audits/README.md",
  "canonical_pack": "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack",
  "overview": "docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md",
  "task_evidence": "docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md",
  "required_index_headings": ["## Canonical Current Audit", "## Dated Historical Snapshots", "## Supersession Ledgers"],
  "assertions": []
}
```

Add exactly 11 Implemented assertions for DML-01/02/03/04/05/07/08/11/14,
QAF-12, and AUT-09. Each names its report, exact tracked evidence, completed
task IDs, and narrow pre-remediation stale phrases.

- [ ] **Step 4: Implement fail-closed types and entry points**

```python
@dataclass(frozen=True)
class SemanticValidationResult:
    assertion_count: int

class AuditSemanticContractError(ValueError):
    def __init__(self, errors: list[str]):
        self.errors = tuple(errors)
        super().__init__("; ".join(errors))

def validate_semantics(
    repo_root: pathlib.Path = pathlib.Path("."),
    contract_path: pathlib.Path = DEFAULT_CONTRACT,
) -> SemanticValidationResult:
    contract = _load_contract(repo_root / contract_path)
    criterion_contract = validate_pack(repo_root / contract["canonical_pack"])
    rows = {row.criterion_id: row for row in criterion_contract.rows}
    tracked = _tracked_paths(repo_root)
    errors = _validate_lifecycle(repo_root, contract)
    errors.extend(_validate_assertions(repo_root, contract, rows, tracked))
    if errors:
        raise AuditSemanticContractError(errors)
    return SemanticValidationResult(assertion_count=len(contract["assertions"]))

def main() -> int:
    try:
        result = validate_semantics()
    except AuditSemanticContractError as exc:
        for error in exc.errors:
            print(f"FAIL: {error}")
        return 1
    print(
        "audit_semantic_freshness: PASS "
        f"assertions={result.assertion_count} failures=0"
    )
    return 0
```

Reject duplicate JSON keys, wrong schema/keys, duplicate IDs, absolute/`..`
paths, missing or untracked evidence, report/state mismatch, missing completed
task IDs, stale phrases, missing lifecycle headings, non-active canonical
README, and non-superseded 2026-07-07 README. `git ls-files -z` proves tracked
membership; Git history is forbidden.

- [ ] **Step 5: Run GREEN and commit**

```bash
python3 -m unittest tests.validation.test_agentic_audit_semantic_freshness -v
python3 scripts/validation/check-agentic-audit-semantic-freshness.py
python3 -m py_compile scripts/validation/check-agentic-audit-semantic-freshness.py
git add scripts/validation/agentic-audit-semantic-contract.json scripts/validation/check-agentic-audit-semantic-freshness.py tests/validation/test_agentic_audit_semantic_freshness.py docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md
git commit -m "feat(audit): enforce semantic audit freshness"
```

## Task 4: Security Readiness Precision

**Files:** security generator, new unit tests, generated readiness, security and
automation audit leaves, task evidence.

**Interfaces:** Produces exactly 13 controls: SEC-AUTO-008 scoped ecosystem
gate, SEC-AUTO-012 broad dependency SCA, SEC-AUTO-013 image scanning.

- [ ] **Step 1: Write RED tests**

```python
def test_scoped_gate_does_not_close_broad_scanning(self):
    output = self.render()
    self.assertIn("| SEC-AUTO-008 | Scoped ecosystem vulnerability gate | Implemented |", output)
    self.assertIn("| SEC-AUTO-012 | Broad dependency SCA coverage | Gap |", output)
    self.assertIn("| SEC-AUTO-013 | Container/image vulnerability scanning | Gap |", output)
    self.assertNotIn("| SEC-AUTO-008 | OSV/SCA vulnerability gate | Implemented |", output)

def test_control_count_and_summary_are_precise(self):
    output = self.render()
    self.assertEqual(13, len(re.findall(r"^\| SEC-AUTO-[0-9]{3} \|", output, re.MULTILINE)))
    self.assertIn("| Implemented | 7 |", output)
    self.assertIn("| Partially Implemented | 1 |", output)
    self.assertIn("| Gap | 5 |", output)
```

- [ ] **Step 2: Run RED, then split detection**

```bash
python3 -m unittest tests.validation.test_security_automation_readiness -v
```

Implement:

```python
has_scoped_ecosystem_gate = bool(
    re.search(r"npm\s+audit\s+--audit-level=high\s+--prefix\s+projects/storybook/nextjs", ci_text)
)
has_broad_dependency_sca = grep_any(
    SECURITY_CODE_SURFACES,
    (r"\bosv-scanner\b", r"\bsnyk\b", r"\bpip-audit\b", r"\bcargo\s+audit\b", r"\bgovulncheck\b"),
)
has_container_scan = grep_any(
    SECURITY_CODE_SURFACES,
    (r"\btrivy\b.*(?:image|fs)", r"\bgrype\b", r"docker\s+scout\s+cves"),
)
```

Rename control 008 and add controls/follow-ups 012/013. Run no scanner.

- [ ] **Step 3: Align audits, regenerate, test, and commit**

```bash
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/validation/generate-security-automation-readiness.sh --check
python3 -m unittest tests.validation.test_security_automation_readiness -v
git diff --check
git add scripts/validation/generate-security-automation-readiness.sh tests/validation/test_security_automation_readiness.py docs/90.references/data/security/security-automation-readiness.md docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md
git commit -m "fix(security): distinguish scoped and broad scan readiness"
```

Expected: 13 controls; 7 Implemented, 1 Partial, 5 Gap; broad gaps route to
Spec 126.

## Task 5: QA and CI Integration

**Files:** audit generator, repo contracts, CI workflow, scripts README,
semantic tests, generated matrix, task evidence.

**Interfaces:** Consumes `validate_semantics()`; produces a named CI step,
repo-contract pass marker, and three semantic summary metrics.

- [ ] **Step 1: Add a failing integration test**

```python
def test_repo_contracts_and_ci_name_the_semantic_gate(self):
    repo_contracts = (ROOT / "scripts/validation/check-repo-contracts.sh").read_text()
    workflow = (ROOT / ".github/workflows/ci-quality.yml").read_text()
    generator = (ROOT / "scripts/validation/generate-audit-implementation-matrix.sh").read_text()
    command = "python3 scripts/validation/check-agentic-audit-semantic-freshness.py"
    self.assertIn(command, repo_contracts)
    self.assertIn(command, workflow)
    self.assertIn("validate_semantics", generator)
```

- [ ] **Step 2: Add the local pass-marker section**

```bash
section "Agentic audit semantic freshness"
semantic_audit_output="$(mktemp "${TMPDIR:-/tmp}/check-repo-contracts-agentic-audit-semantic.XXXXXX")"
if ! python3 scripts/validation/check-agentic-audit-semantic-freshness.py >"$semantic_audit_output" 2>&1; then
  fail "agentic audit semantic freshness failed"
  cat "$semantic_audit_output" >&2
elif ! grep -q 'audit_semantic_freshness: PASS assertions=11 failures=0' "$semantic_audit_output"; then
  fail "agentic audit semantic validator did not print the pass marker"
  cat "$semantic_audit_output" >&2
fi
rm -f "$semantic_audit_output"
```

Use the repository's trap cleanup style if review requires signal-safe cleanup.

- [ ] **Step 3: Add the exact existing-job CI step**

```yaml
      - name: Check canonical audit semantic freshness
        run: python3 scripts/validation/check-agentic-audit-semantic-freshness.py
```

Place it after changed-document metadata and before broad repo contracts. Add
no job, permission, dependency, or remote claim.

- [ ] **Step 4: Add generated semantic metrics and docs**

Import/call `validate_semantics` before rendering and add:

```markdown
| Semantic closure assertions expected | 11 |
| Semantic closure assertions passed | 11 |
| Semantic closure assertion failures | 0 |
```

Add the validator to `scripts/README.md` as a CI/quality gate and explain its
bounded scope.

- [ ] **Step 5: Verify and commit**

```bash
python3 -m unittest tests.validation.test_agentic_audit_semantic_freshness -v
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash -n scripts/validation/check-repo-contracts.sh scripts/validation/generate-audit-implementation-matrix.sh
python3 -c 'import yaml; yaml.safe_load(open(".github/workflows/ci-quality.yml"))'
actionlint .github/workflows/ci-quality.yml
zizmor .github/workflows/ci-quality.yml
bash scripts/validation/check-repo-contracts.sh
git add scripts/validation/generate-audit-implementation-matrix.sh scripts/validation/check-repo-contracts.sh scripts/README.md tests/validation/test_agentic_audit_semantic_freshness.py .github/workflows/ci-quality.yml docs/90.references/data/governance/audit-implementation-matrix.md docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md
git commit -m "ci(governance): gate canonical audit freshness"
```

## Task 6: Generated Evidence and Closure

**Files:** regenerate metadata/audit/security/Wiki references; update progress,
Spec/Plan/Task and parent READMEs.

**Interfaces:** Consumes five reviewed implementation commits; produces final
generated bytes, wrapper evidence, completed chain, and branch review package.

- [ ] **Step 1: Regenerate and run full validation**

```bash
python3 scripts/validation/check-document-metadata.py --mode report --output docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
bash scripts/validation/generate-audit-implementation-matrix.sh
bash scripts/validation/generate-security-automation-readiness.sh
bash scripts/knowledge/generate-llm-wiki-index.sh
bash scripts/knowledge/generate-llm-wiki-coverage.sh
python3 -m unittest discover -s tests/validation -q
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 8b58abc22abb8f93c5580e7185efa0f6a62c4e7b
python3 scripts/validation/check-agentic-audit-semantic-freshness.py
bash scripts/validation/generate-audit-implementation-matrix.sh --check
bash scripts/validation/report-audit-pack-coverage.sh --check
bash scripts/validation/generate-security-automation-readiness.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/validation/check-repo-contracts.sh
git diff --check
```

- [ ] **Step 2: Refresh Graphify and classify it**

```bash
graphify update .
bash scripts/knowledge/report-graphify-health.sh
```

Record unavailable/advisory status without using Graphify as completion proof.

- [ ] **Step 3: Commit any reviewed generated/formatter changes, then require clean state**

```bash
git status --short
```

Expected: no output before the wrapper.

- [ ] **Step 4: Run the controlled final gate**

```bash
bash scripts/validation/run-agent-precommit-all-files.sh \
  --task docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md \
  --allow-prefix .github/workflows/ci-quality.yml \
  --allow-prefix docs/00.agent-governance/memory/progress.md \
  --allow-prefix docs/03.specs/128-agentic-audit-harness-consolidation \
  --allow-prefix docs/03.specs/README.md \
  --allow-prefix docs/04.execution/plans/2026-07-12-agentic-audit-harness-consolidation.md \
  --allow-prefix docs/04.execution/plans/README.md \
  --allow-prefix docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md \
  --allow-prefix docs/04.execution/tasks/README.md \
  --allow-prefix docs/90.references/audits \
  --allow-prefix docs/90.references/data/governance \
  --allow-prefix docs/90.references/data/security \
  --allow-prefix docs/90.references/data/knowledge \
  --allow-prefix docs/90.references/llm-wiki \
  --allow-prefix scripts/README.md \
  --allow-prefix scripts/validation \
  --allow-prefix tests/validation
```

Stop without cleanup on unexpected paths. Record command, prefixes, hook exit,
before/after/new/unexpected paths, and disposition.

- [ ] **Step 5: Close evidence after all reviews and commit**

Set Spec/Plan/Task completed, mark six tasks Done, record exact commits,
commands, review verdicts, protected boundaries, wrapper result, and Graphify
status. Regenerate metadata/Wiki after status changes.

```bash
git add docs scripts/validation tests/validation .github/workflows/ci-quality.yml
git commit -m "docs(task): close audit harness consolidation"
```

## Verification Plan

| ID | Level | Command | Pass Criteria |
| --- | --- | --- | --- |
| VAL-PLN-001 | Structural | `python3 scripts/validation/audit_criterion_contract.py` | 11 reports, 161 rows, unique IDs. |
| VAL-PLN-002 | Semantic | semantic validator CLI | 11 assertions, zero failures. |
| VAL-PLN-003 | Unit | validation unittest discovery | All tests pass. |
| VAL-PLN-004 | Security | security readiness `--check` | 13 precise controls, fresh output. |
| VAL-PLN-005 | Metadata | changed check from exact base | Zero violations/unapproved exceptions. |
| VAL-PLN-006 | Docs | traceability and alignment | Both report zero failures. |
| VAL-PLN-007 | CI | PyYAML/actionlint/zizmor | All pass; no permission expansion. |
| VAL-PLN-008 | Repository | repo contracts | `failures=0`. |
| VAL-PLN-009 | Final QA | controlled wrapper | Hook 0; no unresolved unexpected path. |
| VAL-PLN-010 | Review | SDD task/final packages | Spec PASS, Quality APPROVED, no Critical/Important. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical evidence becomes current truth. | High | Boundary-only edits and literal before/after diff. |
| Semantic contract duplicates all criteria. | High | Only 11 deterministic closures are asserted. |
| Conservative criteria are inflated. | High | Keep provider/runtime/remote uncertainty Partial/Needs Revalidation. |
| Scoped npm evidence closes broad SCA. | High | Three independent signals and negative tests. |
| Workflow integration expands authority. | High | One step in existing read-only job; no permission/job changes. |
| Generated outputs drift. | Medium | Owner generation plus write/check idempotence. |
| Wrapper changes unrelated paths. | High | Clean linked worktree, explicit prefixes, exit-20 stop. |
| Graphify is treated as proof. | Medium | Advisory-only and tracked-source corroboration. |

## Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: Unit/adversarial, structural/semantic, generated
  freshness, and independent review.
- **Sandbox / Canary Rollout**: No runtime rollout; linked worktree isolation.
- **Human Approval Gate**: Spec 128 and this non-runtime plan. Any protected
  scope expansion stops for separate approval.
- **Rollback Trigger**: Cardinality drift, semantic false positive, workflow
  permission expansion, historical evidence mutation, or unexpected paths.
- **Prompt / Model Promotion Criteria**: N/A; no prompt/model change.

## Completion Criteria

- [ ] Six tasks and separate reviews are complete.
- [ ] Historical evidence and routes are clear.
- [ ] Canonical 161 rows reflect current tracked evidence.
- [ ] Semantic 11-assertion contract passes.
- [ ] Security readiness has 13 precise controls.
- [ ] Local and tracked CI gates execute semantic freshness.
- [ ] Generated references and controlled wrapper pass.
- [ ] Whole-branch review approves the exact range.
- [ ] Protected boundaries remain unchanged.

## Related Documents

- [Spec 128](../../03.specs/128-agentic-audit-harness-consolidation/spec.md)
- [Execution task](../tasks/2026-07-12-agentic-audit-harness-consolidation.md)
- [Parent Spec 123](../../03.specs/123-agentic-engineering-audit-remediation/spec.md)
- [Canonical audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Audit index](../../90.references/audits/README.md)
- [Draft Compose follow-up](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- [Draft infrastructure follow-up](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- [Draft security follow-up](../../03.specs/126-security-supply-chain-remediation/spec.md)
- [Draft deployment follow-up](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
