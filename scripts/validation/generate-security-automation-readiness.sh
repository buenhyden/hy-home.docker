#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

OUTPUT="docs/90.references/data/security/security-automation-readiness.md"

usage() {
  cat <<'EOF'
Usage: bash scripts/validation/generate-security-automation-readiness.sh [--check|--dry-run]

Generate the Stage 90 security automation readiness snapshot from tracked repo surfaces.

Options:
  --check    Fail when the generated snapshot is stale.
  --dry-run  Print the generated snapshot to stdout without writing it.
  -h, --help Show this help.
EOF
}

mode="write"
case "${1:-}" in
  "")
    ;;
  --check)
    mode="check"
    ;;
  --dry-run)
    mode="dry-run"
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

python3 - "$mode" "$OUTPUT" <<'PY'
from __future__ import annotations

import collections
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass

MODE = sys.argv[1]
OUTPUT = pathlib.Path(sys.argv[2])


@dataclass(frozen=True)
class Control:
    control_id: str
    control: str
    status: str
    evidence: tuple[str, ...]
    gap: str


def git_ls_files() -> set[str]:
    result = subprocess.run(["git", "ls-files"], check=True, capture_output=True, text=True)
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


TRACKED = git_ls_files()


def exists(path_text: str) -> bool:
    return path_text in TRACKED and pathlib.Path(path_text).is_file()


def read(path_text: str) -> str:
    path = pathlib.Path(path_text)
    if not path.is_file():
        return ""
    return path.read_text(errors="ignore")


def grep_any(paths: tuple[str, ...], patterns: tuple[str, ...]) -> bool:
    combined = "\n".join(read(path) for path in paths)
    return any(re.search(pattern, combined, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def link(path_text: str) -> str:
    target = "../../../../" + path_text
    return f"[{path_text}]({target})"


def evidence_text(items: tuple[str, ...]) -> str:
    return "<br>".join(link(item) if exists(item) else f"`{item}`" for item in items)


WORKFLOW_PATHS = tuple(sorted(path for path in TRACKED if path.startswith(".github/workflows/") and path.endswith((".yml", ".yaml"))))
SCRIPT_PATHS = tuple(
    sorted(
        path
        for path in TRACKED
        if path.startswith("scripts/")
        and path.endswith(".sh")
        and path != "scripts/validation/generate-security-automation-readiness.sh"
        and path != "scripts/validation/generate-audit-implementation-matrix.sh"
    )
)
SECURITY_CODE_SURFACES = WORKFLOW_PATHS + SCRIPT_PATHS + (".pre-commit-config.yaml",)
SECURITY_SCAN_EVIDENCE = (
    ".github/workflows/ci-quality.yml",
    "scripts/README.md",
    ".pre-commit-config.yaml",
)
SECURITY_SCAN_SUMMARY = (
    f"Scanned tracked workflow/script surfaces: {len(WORKFLOW_PATHS)} workflows, "
    f"{len(SCRIPT_PATHS)} scripts, and `.pre-commit-config.yaml`."
)

ci_text = "\n".join(read(path) for path in WORKFLOW_PATHS)
precommit_text = read(".pre-commit-config.yaml")
dependabot_text = read(".github/dependabot.yml")

has_security_policy = exists(".github/SECURITY.md")
has_codeowners = exists(".github/CODEOWNERS")
has_ruleset_record = exists(".github/rulesets/main-protection.md")
has_gitleaks = exists(".gitleaks.toml") and "gitleaks" in precommit_text.lower()
has_dependabot = exists(".github/dependabot.yml") and "package-ecosystem" in dependabot_text
has_workflow_security = "permissions:" in ci_text and "zizmor" in ci_text and "upload-sarif" in ci_text
has_hardening = exists("scripts/hardening/check-all-hardening.sh") and "check-all-hardening.sh" in ci_text
has_template_security = exists("scripts/validation/check-template-security-baseline.sh") and "check-template-security-baseline.sh" in ci_text
has_repo_contracts = exists("scripts/validation/check-repo-contracts.sh") and "workflow security" in read("scripts/validation/check-repo-contracts.sh").lower()
has_tech_stack_provenance = all(
    exists(path)
    for path in (
        "infra/tech-stack.versions.json",
        "infra/image-tag-policy.exceptions.json",
        "scripts/operations/generate-tech-stack-version-provenance.sh",
        "docs/90.references/data/docker/tech-stack-version-provenance.md",
    )
)

has_scoped_ecosystem_gate = bool(
    re.search(
        r"npm\s+audit\s+--audit-level=high\s+--prefix\s+projects/storybook/nextjs",
        ci_text,
    )
)
has_broad_dependency_sca = grep_any(
    SECURITY_CODE_SURFACES,
    (
        r"\bosv-scanner\b",
        r"\bsnyk\b",
        r"\bpip-audit\b",
        r"\bcargo\s+audit\b",
        r"\bgovulncheck\b",
    ),
)
has_container_scan = grep_any(
    SECURITY_CODE_SURFACES,
    (
        r"\btrivy\b.*(?:image|fs)",
        r"\bgrype\b",
        r"docker\s+scout\s+cves",
    ),
)
has_sbom_generation = grep_any(
    SECURITY_CODE_SURFACES,
    (
        r"\bsyft\b",
        r"\bcyclonedx\b",
        r"\bspdx-sbom-generator\b",
        r"\bnpm\s+sbom\b",
    ),
)
has_attestation = grep_any(
    SECURITY_CODE_SURFACES,
    (
        r"\bcosign\s+",
        r"slsa-framework/slsa-github-generator",
        r"actions/attest",
    ),
)
has_scorecard = grep_any(
    SECURITY_CODE_SURFACES,
    (
        r"ossf/scorecard",
        r"scorecard-action",
        r"\bscorecard\b.*--repo",
    ),
)

controls: list[Control] = [
    Control(
        "SEC-AUTO-001",
        "Security disclosure and vulnerability reporting boundary",
        "Implemented" if has_security_policy else "Gap",
        (".github/SECURITY.md",),
        "Keep reporting and response expectations current." if has_security_policy else "Add a security disclosure policy before claiming a reporting boundary.",
    ),
    Control(
        "SEC-AUTO-002",
        "Workflow permissions and dangerous-workflow scanning",
        "Implemented" if has_workflow_security and has_repo_contracts else "Partially Implemented",
        (".github/workflows/ci-quality.yml", "scripts/validation/check-repo-contracts.sh"),
        "Continue checking SHA-pinned actions, least-privilege permissions, and zizmor SARIF upload." if has_workflow_security and has_repo_contracts else "Wire workflow-security checks into CI and repo contracts.",
    ),
    Control(
        "SEC-AUTO-003",
        "Secret scanning and secret-boundary enforcement",
        "Implemented" if has_gitleaks and has_template_security else "Partially Implemented",
        (".pre-commit-config.yaml", ".gitleaks.toml", "scripts/validation/check-template-security-baseline.sh"),
        "Pre-commit secret scanning and template/security baseline exist; keep secret values out of generated reports." if has_gitleaks and has_template_security else "Add or verify gitleaks and template/security baseline coverage.",
    ),
    Control(
        "SEC-AUTO-004",
        "Dependency update automation",
        "Implemented" if has_dependabot else "Gap",
        (".github/dependabot.yml",),
        "Dependabot coverage exists; vulnerability severity gating remains separate." if has_dependabot else "Add dependency update automation before relying on automated dependency hygiene.",
    ),
    Control(
        "SEC-AUTO-005",
        "Infrastructure hardening baseline",
        "Implemented" if has_hardening else "Gap",
        ("scripts/hardening/check-all-hardening.sh", ".github/workflows/ci-quality.yml"),
        "Hardening script is wired into CI quality checks." if has_hardening else "Wire hardening checks into local and CI quality gates.",
    ),
    Control(
        "SEC-AUTO-006",
        "Tracked image/version provenance snapshot",
        "Implemented" if has_tech_stack_provenance else "Partially Implemented",
        (
            "infra/tech-stack.versions.json",
            "infra/image-tag-policy.exceptions.json",
            "scripts/operations/generate-tech-stack-version-provenance.sh",
            "docs/90.references/data/docker/tech-stack-version-provenance.md",
        ),
        "Generated provenance describes tracked registry/Compose evidence, not SBOMs, signatures, or SLSA attestations." if has_tech_stack_provenance else "Regenerate or add the tech-stack provenance snapshot.",
    ),
    Control(
        "SEC-AUTO-007",
        "Branch protection and review evidence",
        "Partially Implemented" if has_codeowners and has_ruleset_record else "Gap",
        (".github/CODEOWNERS", ".github/rulesets/main-protection.md"),
        "Local and last-recorded branch-protection evidence exist; live remote enforcement must be re-verified before current claims." if has_codeowners and has_ruleset_record else "Add CODEOWNERS and recorded branch-protection evidence.",
    ),
    Control(
        "SEC-AUTO-008",
        "Scoped ecosystem vulnerability gate",
        "Implemented" if has_scoped_ecosystem_gate else "Gap",
        (".github/workflows/ci-quality.yml",),
        "The tracked Storybook Next.js npm audit gate has an explicit project and severity scope."
        if has_scoped_ecosystem_gate
        else "Add an explicitly scoped dependency vulnerability gate with project, ecosystem, severity, and exception ownership.",
    ),
    Control(
        "SEC-AUTO-009",
        "SBOM generation",
        "Implemented" if has_sbom_generation else "Gap",
        SECURITY_SCAN_EVIDENCE,
        "An SBOM generation command is present in tracked workflow/script surfaces." if has_sbom_generation else f"No tracked SBOM generator command was found in workflow/script surfaces. {SECURITY_SCAN_SUMMARY}",
    ),
    Control(
        "SEC-AUTO-010",
        "Artifact signing or provenance attestation",
        "Implemented" if has_attestation else "Gap",
        SECURITY_SCAN_EVIDENCE,
        "Signing or attestation command is present in tracked workflow/script surfaces." if has_attestation else f"No tracked signing, SLSA provenance, or attestation workflow command was found. {SECURITY_SCAN_SUMMARY}",
    ),
    Control(
        "SEC-AUTO-011",
        "OpenSSF Scorecard automation",
        "Implemented" if has_scorecard else "Gap",
        SECURITY_SCAN_EVIDENCE,
        "Scorecard automation is present in tracked workflow/script surfaces." if has_scorecard else f"No tracked OpenSSF Scorecard automation command was found. {SECURITY_SCAN_SUMMARY}",
    ),
    Control(
        "SEC-AUTO-012",
        "Broad dependency SCA coverage",
        "Implemented" if has_broad_dependency_sca else "Gap",
        SECURITY_SCAN_EVIDENCE,
        "A broad dependency SCA command is present in tracked workflow/script surfaces."
        if has_broad_dependency_sca
        else f"No tracked broad dependency SCA command was found; the scoped npm audit does not satisfy this control. {SECURITY_SCAN_SUMMARY}",
    ),
    Control(
        "SEC-AUTO-013",
        "Container/image vulnerability scanning",
        "Implemented" if has_container_scan else "Gap",
        SECURITY_SCAN_EVIDENCE,
        "A container/image vulnerability scanning command is present in tracked workflow/script surfaces."
        if has_container_scan
        else f"No tracked container/image vulnerability scanning command was found. {SECURITY_SCAN_SUMMARY}",
    ),
]

status_counts = collections.Counter(control.status for control in controls)
readiness_order = {"Implemented": 0, "Partially Implemented": 1, "Gap": 2}
ready_count = status_counts["Implemented"]
partial_count = status_counts["Partially Implemented"]
gap_count = status_counts["Gap"]

residual_security_gaps: list[str] = []
if not has_sbom_generation:
    residual_security_gaps.append("SBOM generation")
if not has_attestation:
    residual_security_gaps.append("artifact signing/provenance attestation")
if not has_scorecard:
    residual_security_gaps.append("OpenSSF Scorecard automation")
if not has_broad_dependency_sca:
    residual_security_gaps.append("broad dependency SCA")
if not has_container_scan:
    residual_security_gaps.append("container/image vulnerability scanning")

follow_up_rows: list[tuple[str, str, str]] = []
if not has_scoped_ecosystem_gate:
    follow_up_rows.append(
        (
            "SEC-AUTO-008",
            "Add a scoped ecosystem vulnerability gate with explicit project, severity, and exception handling.",
            "Stage 03 security spec + Stage 04 plan",
        )
    )
spec_126_route = "[Draft Spec 126](../../../03.specs/126-security-supply-chain-remediation/spec.md)"
if not has_sbom_generation:
    follow_up_rows.append(
        (
            "SEC-AUTO-009",
            "Add SBOM generation and storage rules for build or release artifacts.",
            spec_126_route,
        )
    )
if not has_attestation:
    follow_up_rows.append(
        (
            "SEC-AUTO-010",
            "Add artifact signing, SLSA provenance, or attestation design for artifact-producing workflows.",
            spec_126_route,
        )
    )
if not has_scorecard:
    follow_up_rows.append(
        (
            "SEC-AUTO-011",
            "Add OpenSSF Scorecard advisory reporting if maintainers want an external security-health signal.",
            spec_126_route,
        )
    )
if not has_broad_dependency_sca:
    follow_up_rows.append(
        (
            "SEC-AUTO-012",
            "Define broad dependency SCA ecosystems, thresholds, exceptions, remediation ownership, and rollout mode.",
            spec_126_route,
        )
    )
if not has_container_scan:
    follow_up_rows.append(
        (
            "SEC-AUTO-013",
            "Define container/image scan targets, digest identity, thresholds, exceptions, and remediation ownership.",
            spec_126_route,
        )
    )

if residual_security_gaps:
    if len(residual_security_gaps) == 1:
        residual_sentence = residual_security_gaps[0]
    else:
        residual_sentence = ", ".join(residual_security_gaps[:-1])
        residual_sentence = f"{residual_sentence}, and {residual_security_gaps[-1]}"
    residual_finding = f"- {residual_sentence} are still gaps in tracked workflow/script surfaces."
else:
    residual_finding = "- No tracked security automation gap remains in this readiness snapshot."

lines: list[str] = [
    "---",
    "status: active",
    "generated_by: scripts/validation/generate-security-automation-readiness.sh",
    "---",
    "",
    "<!-- Target: docs/90.references/data/security/security-automation-readiness.md -->",
    "",
    "# Reference: Security Automation Readiness",
    "",
    "## Overview",
    "",
    "This generated reference summarizes repository-local security automation",
    "readiness for scoped vulnerability gating, broad dependency SCA, container/image",
    "scanning, SBOM generation, provenance/attestation, workflow security, secret",
    "scanning, dependency updates, and hardening.",
    "",
    "## Purpose",
    "",
    "The purpose is to make the remaining security automation gaps explicit from",
    "tracked repository evidence. It does not run scanners, generate SBOMs, sign",
    "artifacts, attest builds, query registries, or change CI behavior.",
    "",
    "## Repository Role",
    "",
    "This reference supports Stage 90 security maturity audits and future Stage",
    "03/04 security automation planning. It does not replace Stage 00 security",
    "governance, `.github/workflows/**`, `.github/SECURITY.md`, runtime",
    "hardening scripts, branch protection, release workflows, or vulnerability",
    "management procedures.",
    "",
    "## Scope",
    "",
    "### In Scope",
    "",
    "- Tracked workflow, script, governance, Dependabot, hardening, and registry",
    "  evidence.",
    "- Readiness classification for security automation capabilities.",
    "- Explicit distinction between implemented controls and future gates.",
    "",
    "### Out of Scope",
    "",
    "- Running OSV, SCA, SAST, container scanners, Scorecard, SBOM tools, signing,",
    "  attestation, registry lookups, or remote GitHub checks.",
    "- Changing workflow permissions, CI required checks, release artifacts,",
    "  branch protection, runtime Compose files, secrets, credentials, tokens,",
    "  private keys, shell history, raw logs, or `.env` values.",
    "",
    "## Definitions / Facts",
    "",
    "- **Implemented**: tracked local evidence exists for the automation surface.",
    "- **Partially Implemented**: tracked evidence exists, but live enforcement,",
    "  framework depth, or automation coverage is incomplete.",
    "- **Gap**: no tracked workflow/script automation command or required evidence",
    "  was found for that capability.",
    "- **Readiness snapshot**: a generated reference for planning, not a security",
    "  certification, score, vulnerability statement, SBOM, signature, or",
    "  attestation.",
    "",
    "## Summary",
    "",
    "| Status | Count |",
    "| --- | ---: |",
    f"| Implemented | {ready_count} |",
    f"| Partially Implemented | {partial_count} |",
    f"| Gap | {gap_count} |",
    "",
    "## Readiness Matrix",
    "",
    "| Control ID | Control | Status | Evidence | Gap / Next Step |",
    "| --- | --- | --- | --- | --- |",
]

for control in sorted(controls, key=lambda item: (readiness_order[item.status], item.control_id)):
    lines.append(
        "| "
        + " | ".join(
            [
                control.control_id,
                control.control,
                control.status,
                evidence_text(control.evidence),
                control.gap.replace("|", "\\|"),
            ]
        )
        + " |"
    )

lines.extend(
    [
        "",
        "## Findings",
        "",
        "- Security disclosure, workflow security, secret scanning, Dependabot,",
        "  hardening, and tracked image-version provenance all have repo-local",
        "  evidence.",
        "- Branch protection and review evidence is partial because the repository",
        "  stores CODEOWNERS and last-recorded ruleset evidence, but this generator",
        "  does not query live remote GitHub settings.",
        "- The scoped Storybook Next.js npm audit gate does not close broad dependency",
        "  SCA or container/image vulnerability scanning readiness.",
        residual_finding,
        "",
        "## Gap / Follow-up",
        "",
        "| Gap ID | Gap | Suggested Future Stage |",
        "| --- | --- | --- |",
    ]
)

if follow_up_rows:
    for gap_id, gap, stage in follow_up_rows:
        lines.append(f"| `{gap_id}` | {gap} | {stage} |")
else:
    lines.append("| N/A | No tracked security automation gap remains in this snapshot. | N/A |")

lines.extend(
    [
        "",
        "## Source Rules",
        "",
        "- Use tracked repository files for readiness claims.",
        "- Treat this generated snapshot as planning evidence, not active policy or",
        "  runtime truth.",
        "- Do not include secret values, private keys, tokens, shell history, raw",
        "  secret logs, or `.env` values.",
        "",
        "## Sources",
        "",
        "- [.github/workflows/ci-quality.yml](../../../../.github/workflows/ci-quality.yml) - CI quality and workflow-security evidence.",
        "- [.pre-commit-config.yaml](../../../../.pre-commit-config.yaml) - local pre-commit and secret-scanning hook evidence.",
        "- [.github/dependabot.yml](../../../../.github/dependabot.yml) - dependency update automation evidence.",
        "- [.github/SECURITY.md](../../../../.github/SECURITY.md) - vulnerability reporting boundary.",
        "- [Security framework maturity audit](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md) - framework coverage and gap baseline.",
        "- [Security governance research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md) - secure SDLC and supply-chain reference context.",
        "- [Repository contracts](../../../../scripts/validation/check-repo-contracts.sh) - repo-local governance and workflow contract checks.",
        "",
        "## Maintenance",
        "",
        "- **Owner**: Security Reviewer / QA Engineer.",
        "- **Review Cadence**: Regenerate after security workflow, Dependabot,",
        "  hardening, vulnerability-gate, broad SCA, container/image scanning, SBOM,",
        "  signing, attestation, or Scorecard",
        "  changes.",
        "- **Update Trigger**: Update when tracked workflow/script security automation",
        "  changes or when Stage 90 security maturity audits are refreshed.",
        "",
        "## Related Documents",
        "",
        "- [security data index](./README.md)",
        "- [reference data index](../README.md)",
        "- [security framework maturity audit](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md)",
        "- [automation candidates](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)",
        "- [security governance research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md)",
        "",
    ]
)

generated = "\n".join(lines)

if MODE == "dry-run":
    print(generated, end="")
elif MODE == "check":
    if not OUTPUT.is_file():
        print(f"FAIL: missing generated security automation readiness snapshot: {OUTPUT}", file=sys.stderr)
        sys.exit(1)
    current = OUTPUT.read_text()
    if current != generated:
        print(f"FAIL: stale generated security automation readiness snapshot: {OUTPUT}", file=sys.stderr)
        print("Run: bash scripts/validation/generate-security-automation-readiness.sh", file=sys.stderr)
        sys.exit(1)
    print(f"PASS: generated security automation readiness snapshot is fresh: {OUTPUT}")
else:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(generated)
    print(f"Generated {OUTPUT} with {len(controls)} controls")
PY
