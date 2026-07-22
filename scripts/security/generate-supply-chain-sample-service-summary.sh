#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

OUTPUT="docs/90.references/data/security/supply-chain-sample-service.md"
CHECKER="scripts/validation/check-supply-chain-policy.py"
MODE="${1:-write}"

case "$MODE" in
write | --check)
  ;;
--help | -h)
  printf '%s\n' "Usage: bash scripts/security/generate-supply-chain-sample-service-summary.sh [--check]"
  exit 0
  ;;
*)
  printf '%s\n' "Usage: bash scripts/security/generate-supply-chain-sample-service-summary.sh [--check]" >&2
  exit 2
  ;;
esac

python3 "$CHECKER" --check >/dev/null

generated="$(python3 - <<'PY'
import json
import pathlib

registry = json.loads(pathlib.Path("infra/supply-chain.tool-images.json").read_text())
policy = json.loads(pathlib.Path("infra/supply-chain.sample-service-policy.json").read_text())
tool_rows = []
for tool in registry["tools"]:
    tool_rows.append(f"| `{tool['name']}` | `{tool['image']}@{tool['digest']}` | `{tool['command_contract']}` | `{tool['network_mode']}` |")

lines = [
    "---",
    "status: active",
    "generated_by: scripts/security/generate-supply-chain-sample-service-summary.sh",
    "---",
    "",
    "# Reference: Sample-service Local Supply-chain Verification",
    "",
    "## Overview",
    "",
    "This generated reference records the tracked, local-only supply-chain",
    "fixture contract for `examples/sample-web-service`. It is evidence routing,",
    "not a publication, release, registry, remote attestation, OIDC, or SLSA",
    "conformance claim.",
    "",
    "## Purpose",
    "",
    "The deterministic policy gate verifies pinned tool identities, distinct",
    "baseline/candidate subject fixtures, redacted Grype policy handling, SBOM and",
    "provenance binding, signature-negative fixtures, and Scorecard advisory-only",
    "semantics without network access.",
    "",
    "## Repository Role",
    "",
    "This reference is a generated Stage 90 index to the active Spec 126 and",
    "Stage 04 Task. The checker and wrapper own executable policy behavior; this",
    "document does not replace security policy, CI configuration, or Task evidence.",
    "",
    "## Scope",
    "",
    "### In Scope",
    "",
    "- Fixture-only validation for the local sample-service policy.",
    "- Digest-bound local subject tuples and redacted verification verdict schema.",
    "- Local ephemeral Cosign key lifetime and advisory-only Scorecard boundary.",
    "",
    "### Out of Scope",
    "",
    "- Registry pushes, artifact publication, remote attestations, workflow dispatch,",
    "  GitHub mutation, OIDC, transparency-log trust, releases, and deployment.",
    "- Raw scan reports, SBOM/provenance bodies, signature bundles, private keys,",
    "  credentials, tokens, and Scorecard response payloads.",
    "",
    "## Policy Contract",
    "",
    f"- **Policy ID**: `{policy['policy_id']}`.",
    f"- **Subject**: `{policy['subject']['service']}` with roles `{', '.join(policy['subject']['roles'])}`.",
    f"- **SBOM format**: `{policy['sbom']['format']}`.",
    f"- **Provenance predicate**: `{policy['provenance']['predicate_type']}`.",
    f"- **Signature mode**: `{policy['signature']['mode']}` with `{policy['signature']['key_lifetime']}` key lifetime.",
    f"- **CI enforcement**: `{policy['ci_enforcement']}`.",
    "",
    "## Definitions / Facts",
    "",
    "- **Fixture-only** means deterministic local JSON validation with no network",
    "  access, image build, signature key, or consumer verdict creation.",
    "- **Advisory rehearsal** means an optional local execution that may report",
    "  unavailable prerequisites without claiming a passing runtime result.",
    "- **Accepted verdict** means a redacted, digest-bound local consumer record;",
    "  it is not a published artifact, remote attestation, or release approval.",
    "",
    "## Pinned Tool Images",
    "",
    "| Tool | Image manifest | Command contract | Network mode |",
    "| --- | --- | --- | --- |",
    *tool_rows,
    "",
    "## Evidence Boundary",
    "",
    "- The Task consumer contract is exactly two ignored local verdicts at",
    "  `_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json`",
    "  and `verification-verdict.candidate.json`.",
    "- Each published consumer verdict carries only source revision, image config",
    "  digest, OCI archive SHA-256, policy ID, role, verdict, a null exception ID,",
    "  verification time, and redaction status.",
    "- Fixture-only checks do not create consumer verdicts. Advisory execution must",
    "  produce distinct accepted subjects without a vulnerability exception or",
    "  report a truthful prerequisite block, exception-review rejection, or policy",
    "  rejection.",
    "",
    "## Advisory Boundary",
    "",
    "Scorecard is a read-only advisory observation. Its score cannot be a fixture",
    "policy or CI blocking decision. This generator does not assert that any live",
    "tool image, vulnerability database, Scorecard endpoint, or remote workflow",
    "was available or run.",
    "",
    "## Sources",
    "",
    "- [tool registry](../../../../infra/supply-chain.tool-images.json)",
    "- [sample-service policy](../../../../infra/supply-chain.sample-service-policy.json)",
    "- [exception registry](../../../../infra/supply-chain.vulnerability-exceptions.json)",
    "- [fixture checker](../../../../scripts/validation/check-supply-chain-policy.py)",
    "- [local wrapper](../../../../scripts/security/verify-sample-service-supply-chain.sh)",
    "",
    "## Maintenance",
    "",
    "- **Owner**: Security Auditor / CI-CD Engineer.",
    "- **Refresh**: run `bash scripts/security/generate-supply-chain-sample-service-summary.sh`",
    "  after changing the fixture contract, policy, tool registry, or wrapper.",
    "- **Freshness**: run `bash scripts/security/generate-supply-chain-sample-service-summary.sh --check`.",
    "",
    "## Related Documents",
    "",
    "- [Supply-chain Task](../../../04.execution/tasks/2026-07-19-security-supply-chain-remediation.md)",
    "- [Supply-chain Plan](../../../04.execution/plans/2026-07-11-security-supply-chain-remediation.md)",
    "- [Spec 126](../../../03.specs/126-security-supply-chain-remediation/spec.md)",
    "- [security data index](./README.md)",
    "",
]
print("\n".join(lines))
PY
)"

if [[ "$MODE" == "--check" ]]; then
  if [[ ! -f "$OUTPUT" || "$(<"$OUTPUT")" != "$generated" ]]; then
    printf 'FAIL: stale generated supply-chain summary: %s\n' "$OUTPUT" >&2
    printf 'Run: bash scripts/security/generate-supply-chain-sample-service-summary.sh\n' >&2
    exit 1
  fi
  printf 'PASS: generated supply-chain summary is fresh: %s\n' "$OUTPUT"
  exit 0
fi

printf '%s\n' "$generated" >"$OUTPUT"
printf 'Generated %s\n' "$OUTPUT"
