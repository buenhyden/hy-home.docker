---
title: "{{TITLE}}"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Service

### Purpose

<!-- Author prompt: State the service role this package plays. -->

{{SERVICE_ROLE}}

### Interfaces

<!-- Author prompt: Describe actual Compose/Dockerfile/config linkage, profiles, dependencies, networks, published ports, persistence paths, environment key names, secret references and health semantics, and the security boundary. Record removal or migration state explicitly. Keep operational procedures with the owning Guide/Policy/Runbook and route numbered-stage links through docs/README.md outside docs/. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the curated machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

<!-- Author prompt: When the package has an external interface, list each in this table: Interface the boundary, Producer and Consumer its two sides, Contract the input and output meaning, and Failure how a failure is handled. Otherwise delete the table. -->

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| {{INTERFACE}} | {{PRODUCER}} | {{CONSUMER}} | {{CONTRACT}} | {{FAILURE}} |

{{INPUTS_OUTPUTS_AND_SECURITY_BOUNDARY}}

## Usage

### Prerequisites

<!-- Author prompt: Name the supported environment, profiles and permissions the package needs. -->

{{SUPPORTED_ENVIRONMENT}}

### Selected Start

<!-- Author prompt: Give the local workflow that starts or uses only this package. -->

{{LOCAL_WORKFLOW}}

## Checks

### Readiness

<!-- Author prompt: Name the checks and health signals that show the package is ready. -->

{{CHECKS}}

### Failure Handling

<!-- Author prompt: Link the runbooks and state observability and recovery; do not copy their commands. -->

{{RUNBOOK_LINKS_OBSERVABILITY_AND_RECOVERY}}
