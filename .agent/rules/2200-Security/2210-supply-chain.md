---
trigger: model_decision
glob: [".github/workflows/**", "Dockerfile", "**/package.json", "**/pom.xml"]
description: "Supply Chain Security Standards: Enforces SBOM generation, artifact signing, and dependency pinning with mandatory security gates."
---

# Supply Chain Security Standards

- **Role**: DevSecOps Engineer
- **Purpose**: Define standards for ensuring the integrity and auditability of software artifacts through secure build pipelines and dependency management.
- **Activates When**: Modifying CI/CD pipelines, updating build dependencies, or configuring artifact signing/SBOM generation.

**Trigger**: model_decision — Apply during the configuration of build and publishing workflows.

## 1. Standards

### Principles

- **[REQ-SC-01] Build Traceability (SBOM)**
  - Every release artifact MUST be accompanied by a Software Bill of Materials (SBOM) in a standard format (CycloneDX/SPDX).
- **[REQ-SC-02] Cryptographic Provenance**
  - Published artifacts (containers, packages) MUST be cryptographically signed to ensure authenticity and prevent tampering.
- **[REQ-SC-03] Strict Dependency Pinning**
  - All dependencies MUST be pinned to specific versions or immutable digests (hashes). Use of floating tags or unbounded ranges is PROHIBITED.

### Security Gates

| Gate Type | Requirement ID | Failure Condition |
| --- | --- | --- |
| Vulnerability | [REQ-SC-04] | Any CVSS > 7.0 (High/Critical) |
| License | [REQ-SC-05] | Prohibited licenses (e.g., AGPL) |
| SBOM | [REQ-SC-06] | Missing or invalid SBOM artifact |
| Signing | [REQ-SC-07] | Missing signature for production target |

### Must

- **[REQ-SC-08] Automated Build Provenance**
  - Build pipelines MUST capture metadata including commit SHA, build timestamp, and the identity of the build trigger.
- **[REQ-SC-09] Mandatory Lockfile Commits**
  - Lockfiles (`package-lock.json`, `npm-shrinkwrap.json`, `poetry.lock`) MUST be committed to ensure reproducible builds.
- **[REQ-SC-10] Isolated Build Environments**
  - Artifact builds MUST occur in short-lived, isolated environments with restricted network access to prevent lateral movement.

### Must Not

- **[BAN-SC-01] Unverified Third-Party Scripts**
  - Do NOT download and execute scripts (e.g., `curl | sh`) from third-party URLs during the build process without hash verification.
- **[BAN-SC-02] Secrets in Artifacts**
  - Build artifacts MUST NOT contain baked-in secrets, API tokens, or private keys.

### Failure Handling

- **Stop Condition**: Stop the release pipeline if the vulnerability scanner identifies a "Critical" threat in a direct or transitive dependency.

## 2. Procedures

- **[PROC-SC-01] Artifact Audit Trail**
  - IF a new release is prepared THEN MUST verify that the SBOM and signature are correctly uploaded to the artifact registry.
- **[PROC-SC-02] Pipeline Hardening**
  - Regularly audit CI/CD secrets and permissions to ensure they follow the "Principle of Least Privilege".

## 3. Examples

### Secure GitHub Action Job (Good)

```yaml
jobs:
  build:
    steps:
      - name: Generate SBOM
        run: syft . -o cyclonedx-json > sbom.json
      - name: Sign Image
        run: cosign sign --key ${{ secrets.COSIGN_KEY }} $IMAGE_URL
```

## 4. Validation Criteria

- **[VAL-SC-01] SBOM Integrity**
  - [ ] Every production artifact in the registry is associated with a valid SBOM file.
- **[VAL-SC-02] Digest Match**
  - [ ] Validation tests confirm that the deployed binary's SHA matches the signed digest recorded in the pipeline logs.
- **[VAL-SC-03] Gate Enforcement**
  - [ ] CI/CD logs demonstrate that builds with 10.0 CVSS vulnerabilities were successfully blocked.
