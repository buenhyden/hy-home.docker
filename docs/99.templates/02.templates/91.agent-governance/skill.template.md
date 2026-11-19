---
name: "{{FUNCTION_ID}}"
description: "{{DESCRIPTION}}"
metadata:
  title: "{{TITLE}}"
  version: "0.1.0"
  type: "governance/skill"
  status: "draft"
  owner: "{{OWNER}}"
  updated: "{{UPDATED}}"
  function_id: "{{FUNCTION_ID}}"
  scope: "{{SCOPE}}"
  owner_agent: "{{OWNER_AGENT}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Trigger

### When to Use

{{WHEN_THIS_PROCEDURE_IS_VALID_AND_PRECONDITIONS}}

### When Not to Use

<!-- Author prompt: Name the requests this skill must not handle and the skill or role that owns them instead. -->

{{WHEN_THIS_PROCEDURE_DOES_NOT_APPLY}}

## Procedure

### Steps

<!-- Author prompt: List ordered single-action steps, then the required inputs the steps read. -->

{{ORDERED_SINGLE_ACTION_STEPS_AND_REQUIRED_INPUTS}}

### Failure Handling

{{STOP_CONDITIONS_AND_RECOVERY}}

## Outputs

### Artifacts

{{PRODUCED_ARTIFACTS_AND_EVIDENCE}}

### Handoff

<!-- Author prompt: Say when the skill is complete, what is handed to whom, and link the owning role and policies. -->

{{COMPLETION_HANDOFF_AND_OWNING_LINKS}}

## Verification

### Checks

{{OBSERVABLE_SUCCESS_CONDITIONS}}

### Limits

<!-- Author prompt: Name what the checks do not prove; write that the skill records no limit when it states none. -->

{{WHAT_THE_CHECKS_DO_NOT_PROVE}}
