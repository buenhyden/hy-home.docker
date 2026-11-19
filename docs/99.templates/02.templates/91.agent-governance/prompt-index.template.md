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

## Responsibility

### Purpose

<!-- Author prompt: State what this stage or folder is for, who reads it, and what information it owns and lets flow in or out; separate fact from assumption and link the real owner. Do not manage Task status here. -->

{{PURPOSE_READERS_AND_OWNED_INFORMATION}}

### Excluded Responsibilities

<!-- Author prompt: Name what this folder does not own and link the owner of each excluded concern; write the reason when nothing is excluded. -->

{{EXCLUDED_RESPONSIBILITIES_AND_OWNERS}}

## Current Contents

### Paths

<!-- Author prompt: List only documents or open changes that exist now, one Path and Purpose row per direct child. A document's own table without a Path column may follow; then name the subtypes, the canonical sources and the boundary to non-authoritative records. -->

| Path | Purpose |
| --- | --- |
| {{DIRECT_CHILD_PATH}} | {{DIRECT_CHILD_PURPOSE}} |

{{SUBTYPES_AUTHORITY_AND_RECORD_BOUNDARY}}

### Owners

<!-- Author prompt: Name the owner of this README and the owner of a listed document only where that document or this README states it; say so in a sentence when it records none. -->

{{OWNERS}}

## Usage

### Entry Points

<!-- Author prompt: Link the requirement, design, task and operations documents that feed or consume this folder, the governing policy, and the template that shapes this document. -->

{{UPSTREAM_DOWNSTREAM_POLICY_AND_TEMPLATE_LINKS}}

### Checks

<!-- Author prompt: Name the template, the review and approval path and the checks to run before changing this folder, and state status transitions, promotion and where an item goes when it leaves; write the reason when there is no transition. -->

{{REVIEW_CHECKS_TRANSITIONS_AND_EXIT}}
