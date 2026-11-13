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

## Purpose

### Project Role

<!-- Author prompt: State the project or folder purpose and the primary reader as fact, apart from assumptions. -->

{{PROJECT_ROLE_AND_AUDIENCE}}

### Boundaries

<!-- Author prompt: State what is supported and what is a non-goal, and link the real owner of each excluded concern. -->

{{SUPPORTED_SCOPE_AND_NON_GOALS}}

## Repository Map

### Directories

<!-- Author prompt: Route readers to implementation and existing documentation owners. Derive inventories from tracked sources instead of fixed counts. Describe lifecycle and validation entrypoints without copying Guide, Policy or Runbook procedures. Outside docs/, route numbered-stage documentation through docs/README.md. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the curated machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

{{DIRECTORY_PURPOSE_AND_OWNER}}

| Path | Purpose |
| --- | --- |
| {{DIRECT_CHILD_PATH}} | {{DIRECT_CHILD_PURPOSE}} |

### Canonical Entry Points

{{POLICY_DEVELOPMENT_AND_OPERATIONS_ENTRY_POINTS}}

## Getting Started

### Prerequisites

{{REQUIRED_TOOLS_ENVIRONMENT_AND_PERMISSIONS}}

### First Verified Path

{{START_CHECK_AND_EXPECTED_RESULT}}

## References

### Current Documentation

{{CURRENT_USAGE_DEVELOPMENT_AND_OPERATIONS_LINKS}}

### Support and Ownership

{{CONTACT_ISSUE_REPORTING_AND_MAINTAINER}}
