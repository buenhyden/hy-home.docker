---
layer: agentic
---

# container-threat-modeling

## Overview

STRIDE/DREAD threat modeling framework for Docker container trust boundaries. Provides structured threat identification, risk scoring, and countermeasure selection for containerized environments.

## Purpose

Systematically surface container-specific threats before security vulnerabilities reach production.

## Scope

**Covers:**

- Trust boundary identification (user → app, app → DB, app → external)
- STRIDE threat enumeration per boundary
- DREAD risk scoring (Damage, Reproducibility, Exploitability, Affected users, Discoverability)
- Docker-specific countermeasures (no privileged, read-only root fs, resource limits, secret hygiene)

**Excludes:**

- SAST/SCA scanning (see ci-cd-patterns security gates)
- CVSS-based vulnerability scoring (handled by security-auditor)

## Structure

- Trust boundary map → STRIDE enumeration → DREAD scoring → countermeasure selection

## Agents

- **security-auditor** — primary caller

## Skills

- This function is a reusable orchestration skill.

## Usage

- Trigger when adding new services, changing network topology, or handling sensitive data flows.
- **Inputs:** service architecture description or Compose file
- **Outputs:** `_workspace/threat_model_<date>.md`

## Artifacts

- `_workspace/threat_model_<date>.md`

## Related Documents

- `../../scopes/security.md`
- `../README.md`
