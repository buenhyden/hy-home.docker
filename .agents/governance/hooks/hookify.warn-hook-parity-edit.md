---
title: "WARNING: hook parity contract review required"
version: "2.0.0"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: 'WARNING: hook parity contract review required'
  layer: agent
updated: "2026-11-20"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(\\.claude/settings\\.json|\\.codex/hooks\\.json)$"
enabled: true
event: "file"
name: "warn-hook-parity-edit"
---

# WARNING: hook parity contract review required

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the rule payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose

##### Objective

Apply the declared `warn` action for warn-hook-parity-edit.

##### Authority

Owning contract: `.agents/governance/providers/registry.yaml`.

#### Scope

##### Applies To

The `warn-hook-parity-edit` rule applies on the `file` event and matches file edits whose path meets its structured `conditions` entry ("WARNING: hook parity contract review required"). The frontmatter owns the exact matcher.

##### Exclusions

None.

#### Rules

##### Requirements

**Hook file edit detected; parity contract review required (project rule)**

**When changing hook files, confirm:**

| Contract | Claude | Codex |
| --- | --- | --- |
| Registry owner | `.agents/governance/providers/registry.yaml` `semantic_events.claude` and `hook_contracts.claude` | `.agents/governance/providers/registry.yaml` `semantic_events.codex` and `hook_contracts.codex` |
| Native consumer | `.claude/settings.json` | `.codex/hooks.json` |
| Dispatch | `.claude/hooks/*.sh` thin wrappers | `scripts/hooks/agent-event-hook.sh` |

**Parity checklist:**

- [ ] Change the Provider Registry contract and matching native consumer in the
      same approved unit.
- [ ] Preserve provider-specific unsupported events instead of claiming false
      parity.
- [ ] Bind each command to its registered executable and semantic event.
- [ ] Keep Claude wrappers thin and route shared behavior through
      `scripts/hooks/agent-event-hook.sh`.

**After completion, verify:**

```bash
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section providers
python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all
python3 scripts/operations/provider_surface_renderer.py --check
```

##### Enforcement

Native event delivery is a separate observation from the frontmatter match.

#### Exceptions

##### Exception Conditions

No exception is declared by this rule.

##### Approval and Review

None.

#### Ownership

##### Responsibilities

`@buenhyden`.

##### Change and Adoption

`.agents/README.md`.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
