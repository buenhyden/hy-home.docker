---
title: "{{TITLE}}"
version: "0.1.0"
type: "reference/research"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "references"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids:
- "{{PARENT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Question and Scope

### Question

<!-- Author prompt: State the design question this research answers. -->

{{RESEARCH_QUESTION}}

### Scope

<!-- Author prompt: Name what was read or run and what is out of scope. -->

{{OBSERVED_BOUNDARIES_AND_METHOD}}

## Sources

### Primary Sources

<!-- Author prompt: List the sources actually opened, with their location and the claims they support. -->

{{PRIMARY_SOURCES}}

### Versions and Dates

<!-- Author prompt: List each source in the table: Source ID a stable identifier within this member, Source its location, Version the source's own version or "none", Checked At when it was opened, Finding what it actually supports, Application the use chosen here, and Limits what stays unconfirmed. -->

| Source ID | Source | Version | Checked At | Finding | Application | Limits |
| --- | --- | --- | --- | --- | --- | --- |
| {{SOURCE_ID}} | {{SOURCE}} | {{VERSION}} | {{CHECKED_AT}} | {{FINDING}} | {{APPLICATION}} | {{LIMITS}} |

## Analysis

### Findings

<!-- Author prompt: Record the dated observations and their interpretation, each with its source. -->

{{FINDINGS}}

### Alternatives

<!-- Author prompt: Compare the alternatives the sources support; say so when none was compared. -->

{{ALTERNATIVES}}

## Application and Limits

### Design Implications

<!-- Author prompt: Name what the findings change, what is not adopted and how acceptance would be tested. -->

{{DESIGN_IMPLICATIONS}}

### Unverified Conditions

<!-- Author prompt: Name the facts not observed and the limits of the interpretation. -->

{{UNVERIFIED_CONDITIONS}}
