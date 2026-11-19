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

### Audience

<!-- Author prompt: Name the primary reader of this project or folder as fact, apart from assumptions. -->

{{PRIMARY_READERS}}

### Outcome

<!-- Author prompt: State the project or folder purpose, what is supported and what is a non-goal, and link the real owner of each excluded concern. -->

{{PROJECT_ROLE_SUPPORTED_SCOPE_AND_NON_GOALS}}

## Getting Started

### Prerequisites

{{REQUIRED_TOOLS_ENVIRONMENT_AND_PERMISSIONS}}

### First Use

<!-- Author prompt: Give the first verified path: what to start or check and the expected result. -->

{{START_CHECK_AND_EXPECTED_RESULT}}

## Repository Map

### Current Paths

<!-- Author prompt: Route readers to implementation and existing documentation owners, one Path and Purpose row per direct child. Derive inventories from tracked sources instead of fixed counts. Describe lifecycle and validation entrypoints without copying Guide, Policy or Runbook procedures. Outside docs/, route numbered-stage documentation through docs/README.md. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the curated machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

| Path | Purpose |
| --- | --- |
| {{DIRECT_CHILD_PATH}} | {{DIRECT_CHILD_PURPOSE}} |

{{DIRECTORY_PURPOSE_AND_ENTRY_POINTS}}

### Owners

<!-- Author prompt: Name the maintainer or owner the folder states; say so in a sentence when it records none. -->

{{OWNERS}}

## Support

### Help

<!-- Author prompt: Name the contact and issue reporting route. -->

{{CONTACT_AND_ISSUE_REPORTING}}

### Related Documentation

{{CURRENT_USAGE_DEVELOPMENT_AND_OPERATIONS_LINKS}}
