---
title: "{{TITLE}}"
version: "0.1.0"
type: "reference/research-pack"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "references"
artifact_id: "{{ARTIFACT_ID}}"
created: "{{CREATED}}"
observed_at: "{{OBSERVED_AT}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: `observed_at` is the observation date and keeps its original value; add optional `reviewed_at` (and `next_review_at` for research and data) after it only when a later review happens. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Responsibility

### Purpose

<!-- Author prompt: State the research question and the scope of this package. -->

{{RESEARCH_QUESTION_AND_SCOPE}}

### Excluded Responsibilities

<!-- Author prompt: Name what this package does not cover and its limitations. -->

{{EXCLUSIONS_AND_LIMITATIONS}}

## Current Contents

### Paths

<!-- Author prompt: List each member that exists now, one Path and Purpose row per member. -->

| Path | Purpose |
| --- | --- |
| {{DIRECT_CHILD_PATH}} | {{RESEARCH_MEMBER_PURPOSE}} |

### Owners

<!-- Author prompt: Name the owner of this README and the owner of a listed document only where that document or this README states it; say so in a sentence when it records none. -->

{{OWNERS}}

## Usage

### Entry Points

<!-- Author prompt: Link the current authority documents and state the implications for them. -->

{{IMPLICATIONS_AND_AUTHORITY_LINKS}}

### Checks

<!-- Author prompt: State the method, the primary sources and the findings that support this package. -->

{{METHOD_SOURCES_AND_FINDINGS}}
