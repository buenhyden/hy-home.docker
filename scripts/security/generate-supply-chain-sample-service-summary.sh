#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

OUTPUT="docs/90.references/data/0079-supply-chain-sample-service/README.md"
CHECKER="scripts/validation/check-supply-chain-policy.py"
MODE="${1:---check}"
if (( $# > 1 )); then
  printf 'Only one mode is accepted.\n' >&2
  exit 2
fi

case "$MODE" in
--write | --check)
  ;;
--help | -h)
  printf '%s\n' "Usage: bash scripts/security/generate-supply-chain-sample-service-summary.sh [--write|--check]"
  exit 0
  ;;
*)
  printf '%s\n' "Usage: bash scripts/security/generate-supply-chain-sample-service-summary.sh [--write|--check]" >&2
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
    tool_rows.append(
        f"| `{tool['name']}` | `{tool['repo_digest']}` | "
        f"`{tool['target_descriptor_digest']}` | `{tool['config_id']}` | "
        f"`{tool['command_contract']}` | `{tool['network_mode']}` |"
    )

lines = [
    "---",
    'title: "Reference: Sample-service Local Supply-chain Verification"',
    "version: 1.0.0",
    "type: reference/data-pack",
    "layer: references",
    "status: active",
    "owner: \"@buenhyden\"",
    "artifact_id: DATA-0079",
    "parent_ids: []",
    "created: 2026-07-19",
    "updated: 2026-08-23",
    "observed_at: 2026-08-23",
    "generated_by: scripts/security/generate-supply-chain-sample-service-summary.sh",
    "---",
    "",
    "# Reference: Sample-service Local Supply-chain Verification",
    "",
    "## Purpose",
    "",
    "This generated reference records the tracked, local-only supply-chain",
    "fixture contract for `examples/sample-web-service`. It is evidence routing,",
    "not a publication, release, registry, remote attestation, OIDC, or SLSA",
    "conformance claim.",
    "",
    "### Verification Intent",
    "",
    "The deterministic policy gate verifies pinned repository manifests,",
    "observed target descriptors, independently hashed config bodies, distinct",
    "baseline/candidate subject fixtures, redacted Grype policy handling, SBOM and",
    "provenance binding, signature-negative fixtures, and Scorecard advisory-only",
    "semantics without network access.",
    "",
    "## Consumers",
    "",
    "This reference is a generated Stage 90 index to completed Spec 126 and its",
    "completed local Stage 04 Task. The checker and wrapper own executable policy",
    "behavior; this document does not replace security policy, CI configuration,",
    "or Task evidence and does not extend the completed local boundary.",
    "",
    "## Limitations",
    "",
    "### In Scope",
    "",
    "- Fixture-only validation for the local sample-service policy.",
    "- Digest-bound portable local subject tuples and redacted verification verdict schema.",
    "- Local ephemeral Cosign key lifetime and advisory-only Scorecard boundary.",
    "",
    "### Out of Scope",
    "",
    "- Registry pushes, artifact publication, remote attestations, workflow dispatch,",
    "  GitHub mutation, OIDC, transparency-log trust, releases, and deployment.",
    "- Raw scan reports, SBOM/provenance bodies, signature bundles, private keys,",
    "  credentials, tokens, and Scorecard response payloads.",
    "",
    "## Schema",
    "",
    f"- **Policy ID**: `{policy['policy_id']}`.",
    f"- **Subject**: `{policy['subject']['service']}` with roles `{', '.join(policy['subject']['roles'])}`.",
    f"- **SBOM format**: `{policy['sbom']['format']}`.",
    f"- **Provenance predicate**: `{policy['provenance']['predicate_type']}`.",
    f"- **Signature mode**: `{policy['signature']['mode']}` with `{policy['signature']['key_lifetime']}` key lifetime.",
    f"- **CI enforcement**: `{policy['ci_enforcement']}`.",
    "",
    "### Definitions / Facts",
    "",
    "- **Fixture-only** means deterministic local JSON validation with no network",
    "  access, image build, signature key, or consumer verdict creation.",
    "- **Advisory rehearsal** means an optional local execution that may report",
    "  unavailable prerequisites without claiming a passing runtime result.",
    "- **Accepted verdict** means a redacted, digest-bound local consumer record;",
    "  it is not a published artifact, remote attestation, or release approval.",
    "",
    "## Inventory",
    "",
    "| Tool | Repository manifest | Target descriptor | Config digest | Command contract | Network mode |",
    "| --- | --- | --- | --- | --- | --- |",
    *tool_rows,
    "",
    "## Provenance",
    "",
    "- The Task consumer contract is exactly three ignored local handoff files:",
    "  `_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json`",
    "  `verification-verdict.candidate.json`, and `verification-verdict.pair.json`.",
    "- Each schema-v2 verdict binds source revision and build context to the full",
    "  portable identity tuple: OCI manifest digest, image config digest, OCI",
    "  archive SHA-256, deterministic Docker-load archive SHA-256, deterministic",
    "  local image reference, observed runtime image ID, and runtime identity kind.",
    "  It also carries policy ID, role, accepted verdict, a null exception ID,",
    "  verification time, and redaction status.",
    "- The schema-v3 pair manifest uses generation",
    "  `hyhome-verification-verdict-pair-v3`; it binds the exact bytes of both",
    "  verdicts and repeats the full per-role identity tuple. Partial, legacy,",
    "  mixed-generation, or substituted handoffs fail closed.",
    "- The OCI-to-Docker handoff is a deterministic, uncompressed Docker load",
    "  archive derived from the validated OCI config and layers. Consumers use",
    "  only the bound local reference, require `pull_policy: never`, `--pull never`,",
    "  and `--no-build`, and compare both the local object's `.Id` and the running",
    "  container `.Image` with the recorded runtime image ID.",
    "- Fixture-only checks do not create consumer verdicts. Advisory execution must",
    "  produce distinct accepted subjects without a vulnerability exception or",
    "  report a truthful prerequisite block, exception-review rejection, or policy",
    "  rejection.",
    "",
    "### Advisory Boundary",
    "",
    "Scorecard is a read-only advisory observation. Its score cannot be a fixture",
    "policy or CI blocking decision. This generator does not assert that any live",
    "tool image, vulnerability database, Scorecard endpoint, or remote workflow",
    "was available or run.",
    "",
    "### Sources",
    "",
    "- [tool registry](../../../../infra/supply-chain.tool-images.json)",
    "- [sample-service policy](../../../../infra/supply-chain.sample-service-policy.json)",
    "- [exception registry](../../../../infra/supply-chain.vulnerability-exceptions.json)",
    "- [fixture checker](../../../../scripts/validation/check-supply-chain-policy.py)",
    "- [local wrapper](../../../../scripts/security/verify-sample-service-supply-chain.sh)",
    "",
    "## Refresh",
    "",
    "- **Owner**: Security Auditor / CI-CD Engineer.",
    "- **Refresh**: run `bash scripts/security/generate-supply-chain-sample-service-summary.sh`",
    "  after changing the fixture contract, policy, tool registry, or wrapper.",
    "- **Freshness**: run `bash scripts/security/generate-supply-chain-sample-service-summary.sh --check`.",
    "",
    "## Traceability",
    "",
    "- [Archive migration lookup](../../../98.archive/migrations/0003-workspace-governance-simplification.md)",
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
