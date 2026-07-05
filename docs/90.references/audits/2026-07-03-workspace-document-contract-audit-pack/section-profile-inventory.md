---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/section-profile-inventory.md -->

# Section Profile Inventory

## Overview

This inventory records heading distribution by repository surface. It preserves
the command evidence needed to compare observed section profiles with the
document contract, while leaving all target documents unchanged.

## Purpose

This reference preserves the Task 2 section-profile measurements for the
workspace document contract audit pack. It lets later comparison tasks reuse
observed heading patterns, limitations, and gap candidates without editing the
corpus that was measured.

## Repository Role

This report supports Stage 04 execution evidence and later Stage 90
document-contract audit reports. It is not an active section contract, README
template, parser specification, or authorization to normalize historical
documents.

## Scope

In scope: tracked Markdown headings grouped by root, provider, GitHub, docs
stage, infra, project, scripts, secrets, tests, examples, archive, and generated
graph surfaces.

Out of scope: fenced-aware parser changes, section normalization, renaming
headings, or editing historical evidence.

## Definitions / Facts

- **Heading**: A line matching `^(#{1,6})\s+(.+?)\s*$` in a tracked Markdown
  file.
- **Surface**: The derived repository area used to group heading counts, such
  as `root`, `provider`, `github`, `docs/04.execution`, or `infra`.
- **Line-based scan**: A lightweight heading scan that intentionally does not
  suppress fenced code blocks or comment-like Markdown lines.
- **Gap candidate**: A measured pattern that may require later contract
  comparison before any content rewrite.

## Method

| Evidence ID | Command | Measured Purpose |
| --- | --- | --- |
| SP-001 | See `### Reproduction Commands`. | Count Markdown headings by derived surface and print the 25 most common headings per surface with examples. |

The rerun grouped root `*.md` files as `root`; `.agents`, `.claude`, and
`.codex` as `provider`; `.github/**` as `github`; known stage folders under
`docs/` by stage; `docs/README.md` as `docs/other`; and top-level
`infra`, `projects`, `scripts`, `secrets`, `tests`, `examples`, `archive`,
and `graphify-out` paths by their directory name. No unclassified `other`
surface was present.

### Reproduction Commands

Run this command from the repository root to reproduce `SP-001`. The script is
line-based by design; the fenced-code limitation is recorded in
`## Gaps For Register`.

```bash
python3 - <<'PY'
from collections import Counter, defaultdict
from pathlib import Path
import re
import subprocess

heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
known_doc_stages = {
    "00.agent-governance",
    "01.requirements",
    "02.architecture",
    "03.specs",
    "04.execution",
    "05.operations",
    "90.references",
    "98.archive",
    "99.templates",
}
top_level_surfaces = {
    "archive",
    "examples",
    "graphify-out",
    "infra",
    "projects",
    "scripts",
    "secrets",
    "tests",
}


def surface_for(path):
    parts = path.split("/")
    if "/" not in path:
        return "root"
    if parts[0] in {".agents", ".claude", ".codex"}:
        return "provider"
    if parts[0] == ".github":
        return "github"
    if parts[0] == "docs":
        if len(parts) > 1 and parts[1] in known_doc_stages:
            return f"docs/{parts[1]}"
        return "docs/other"
    if parts[0] in top_level_surfaces:
        return parts[0]
    return "other"


paths = subprocess.check_output(["git", "ls-files", "*.md"], text=True).splitlines()
file_counts = Counter()
heading_totals = Counter()
heading_counts = defaultdict(Counter)
examples = defaultdict(lambda: defaultdict(list))

for path in paths:
    surface = surface_for(path)
    file_counts[surface] += 1
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        match = heading_re.match(line)
        if not match:
            continue
        title = match.group(2).strip()
        heading_totals[surface] += 1
        heading_counts[surface][title] += 1
        if len(examples[surface][title]) < 3:
            examples[surface][title].append(f"{path}:{line_number}")

for surface in sorted(file_counts):
    print(f"## {surface}")
    print(f"files\t{file_counts[surface]}")
    print(f"headings\t{heading_totals[surface]}")
    for title, count in heading_counts[surface].most_common(25):
        print(f"{count}\t{title}\t{', '.join(examples[surface][title])}")
PY
```

## Findings

| Surface | Measurement | Representative Paths | Disposition |
| --- | --- | --- | --- |
| `root` | 6 tracked Markdown files, 47 headings; `Related Documents` appears 4 times and provider quick-reference headings appear twice each | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md` | no-action |
| `github` | 3 tracked Markdown files, 23 headings; PR template, security policy, and ruleset proposal headings each appear once | `.github/PULL_REQUEST_TEMPLATE.md`, `.github/SECURITY.md`, `.github/rulesets/main-protection.md` | no-action |
| `provider` | 102 tracked Markdown files, 888 headings; `Related Documents` appears 46 times, `Error Handling` 19 times, `Purpose` 18 times, and skill bootstrap headings 16 times | `.agents/README.md`, `.claude/CLAUDE.md`, `.claude/agents/code-reviewer.md`, `.claude/skills/compose-stack-agent/skill.md` | no-action |
| `docs/other` | 1 tracked Markdown file, 18 headings; root docs routing headings each appear once | `docs/README.md` | no-action |
| `docs/00.agent-governance` | `Related Documents` appears 105 times; `Overview`, `Scope`, and `Structure` each appear 33 times | `docs/00.agent-governance/README.md`, `docs/00.agent-governance/agents/README.md` | no-action |
| `docs/01.requirements` | PRD sections repeat across 24 to 25 files, including `Vision`, `Problem Statement`, `Functional Requirements`, and `Success Criteria` | `docs/01.requirements/001-gateway.md`, `docs/01.requirements/002-auth.md` | historical-evidence |
| `docs/02.architecture` | Architecture profiles show 51 `Overview` and 51 `Related Documents` headings, plus ADR and ARD-specific section clusters | `docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md`, `docs/02.architecture/requirements/0001-gateway-architecture.md` | no-action |
| `docs/03.specs` | Spec profile sections appear 24 to 26 times, including `Contracts`, `Core Design`, `Verification`, and `Success Criteria & Verification Plan` | `docs/03.specs/001-gateway/spec.md`, `docs/03.specs/002-auth/spec.md` | no-action |
| `docs/04.execution` | Execution documents show 156 `Overview`, 156 `Related Documents`, 88 `Task Table`, 88 `Verification Summary`, and 64 plan-section repeats | `docs/04.execution/plans/2026-03-26-01-gateway-standardization.md`, `docs/04.execution/tasks/2026-03-26-01-gateway-tasks.md` | no-action |
| `docs/05.operations` | Operations docs show 267 `Related Documents`, 273 `Overview` headings across all levels, 67 `Usage`, 67 `Common Checks`, 73 README profile repeats, and 130 nested `Purpose` headings | `docs/05.operations/README.md`, `docs/05.operations/guides/00-workspace/developer-setup.md` | no-action |
| `docs/90.references` | Reference surfaces now show 29 files, 426 headings, 29 `Overview`, 29 `Scope`, 29 `Related Documents`, 18 `Repository Role`, and 17 each of `Purpose`, `Definitions / Facts`, `Sources`, and `Maintenance` after the Task 2 quality fix | `docs/90.references/README.md`, `docs/90.references/audits/README.md`, `docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-inventory.md` | no-action |
| `docs/98.archive` | Archive tombstones show 20 `Archive Metadata`, 20 `Current Replacement`, and 20 `Archive Ledger` headings | `docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md`, `docs/98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md` | historical-evidence |
| `docs/99.templates` | 36 tracked Markdown files, 390 headings; `Related Documents` appears 36 times, `Overview` 33 times, and template category headings such as `Templates` and `Target Rules` 6 times each | `docs/99.templates/README.md`, `docs/99.templates/support/README.md`, `docs/99.templates/templates/common/readme.template.md` | no-action |
| `infra` | 68 tracked Markdown files, 1055 headings; `Related Documents` appears 70 times, and `Audience`, `Scope`, `Structure`, and `How to Work in This Area` each appear 68 times | `infra/01-gateway/README.md`, `infra/01-gateway/nginx/README.md` | no-action |
| `projects` | 3 tracked Markdown files, 29 headings; README profile headings appear 3 times, and `Related References` appears 3 times | `projects/README.md`, `projects/storybook/README.md`, `projects/storybook/nextjs/README.md` | batch-fix |
| `scripts` | 1 tracked Markdown file, 44 headings; README profile and script-catalog headings each appear once | `scripts/README.md` | no-action |
| `secrets` | 1 tracked Markdown file, 18 headings; README profile, inventory, registry, automation, and security-policy headings each appear once | `secrets/README.md` | no-action |
| `tests` | 1 tracked Markdown file, 9 headings; README profile headings and `Related References` each appear once | `tests/README.md` | batch-fix |
| `examples` | 2 tracked Markdown files, 18 headings; `Validation` and `Related Documents` each appear twice across the sample README and service scaffold | `examples/sample-web-service/README.md`, `examples/sample-web-service/service.md` | out-of-scope-gap |
| `archive` | 1 tracked Markdown file, 1 heading | `archive/Windows-Network-IP.md` | historical-evidence |
| `graphify-out` | 3 tracked Markdown files, 3128 headings; generated report headings such as `Corpus Check`, `Summary`, `Graph Freshness`, and graph community headings repeat across the three reports | `graphify-out/GRAPH_REPORT.md`, `graphify-out/2026-06-04/GRAPH_REPORT.md`, `graphify-out/2026-06-05/GRAPH_REPORT.md` | no-action |

## Gaps For Register

| Gap Candidate | Evidence | Disposition | Register Handling |
| --- | --- | --- | --- |
| Requirement agent section naming is split | `AI Agent Requirements (If Applicable)` appears 20 times and `AI Agent Requirements` appears 4 times under `docs/01.requirements` | batch-fix | Add to the register as a future naming-normalization batch if requirements profiles require one spelling. |
| Line-based heading scan surfaces fenced or comment-like H1 lines | `.github/PULL_REQUEST_TEMPLATE.md`, `scripts/README.md`, and `secrets/README.md` report H1 entries such as command or instruction lines | out-of-scope-gap | Record as an automation/parser gap for later fenced-aware audit tooling, not a Task 2 content fix. |
| Infra validation terminology has a small split | `Validation` appears 48 times and `Validation Commands` appears 2 times under `infra` | batch-fix | Defer to a later infra README profile decision before any content edits. |
| Operations nested `Overview` and `Purpose` headings are common | `docs/05.operations` reports 98 H3 `Overview` and 123 H3 `Purpose` entries | no-action | Treat as expected nested guide/runbook profile evidence unless a later contract comparison proves otherwise. |

## Sources

- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md) - Defines the Task 2 audit scope and validation evidence.
- [Template selection](../../../99.templates/support/template-selection.md) - Supports later mapping from observed headings to document profiles.
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - Defines stage-level authoring expectations for comparison work.
- [Reference template](../../../99.templates/templates/common/reference.template.md) - Defines the required Stage 90 reference structure.

## Maintenance

- **Owner**: Documentation Specialist / `doc-writer`.
- **Review Cadence**: Review when the audit pack advances to section-contract
  comparison or when heading-profile validators change.
- **Update Trigger**: Rerun the inventory when tracked Markdown membership,
  template section contracts, or Stage 90 reference template requirements
  change.

## Related Documents

- [Document contract audit references](./README.md)
- [Workspace document contract audit pack task](../../../04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md)
- [Template selection](../../../99.templates/support/template-selection.md)
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Reference template](../../../99.templates/templates/common/reference.template.md)
