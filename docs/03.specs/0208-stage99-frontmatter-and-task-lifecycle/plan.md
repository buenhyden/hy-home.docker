---
title: "Stage 99 Frontmatter and Task Lifecycle Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "active"
owner: "@buenhyden"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0208-PLAN-0001"
parent_ids:
- "SPEC-0208"
created: "2026-10-04"
---

# Stage 99 Frontmatter and Task Lifecycle Plan

## Objective

Deliver the minimum Stage 99 contract, validator implementation and tests,
current-document migration, and one local logical commit for truthful Task
lifecycle evidence and completion-item receipts.

## Dependencies

- SPEC-0208 and its approved Requirement and Architecture inputs.
- Registry/profile-schema/template owners and their existing validators.
- Recorded facts in nonterminal SPEC-0182 and SPEC-0204 documents.
- Read-only review and focused validation before completion. Commit and remote
  integration require their separately recorded authorization and evidence.

## Execution Sequence

1. W1: inventory Stage 99 profiles, templates, schemas, roles, consumers, and
   current Stage 03 records; record every file's disposition in the Task.
2. W2: add the minimal Registry and profile-schema contract, implement and test
   its validator consumers, and align the Spec, Plan, and Task templates.
   Preserve frontmatter value grammar and existing completion-receipt headers.
3. W3: migrate actual terminology in current nonterminal SPEC-0182 and
   SPEC-0204 Plan/Task records and route SPEC-0208 from the Stage 03 README.
4. W4: run owner-selected validation and review, record observed results and
   limitations, then create one local conventional commit when the required
   receipts exist. Push, PR, merge, and remote checks remain separately
   authorized.

## Risk and Rollback

An over-broad schema or template can turn descriptive prose into a parallel
machine contract. Roll back the bounded working-tree changes before integration
if validation or review finds that risk. Do not alter frozen records, terminal
Tasks, or unobserved lifecycle facts.

## Verification

Use the registered metadata, lifecycle, and link checks selected by the owning
validation work, then independently review the diff. Record each actual command
and result in Task 0001; no structural check proves approval or execution.

## Rulings

Queued is a planned/ready summary label, not a lifecycle enum. Existing durable
authority remains in REQ-0024, REQ-0026, AD-0027, AD-0030, and ADR-0037.
