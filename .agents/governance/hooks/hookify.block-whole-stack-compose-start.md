---
title: "BLOCKED: whole-stack Compose start"
version: "1.0.0"
type: "governance/rule"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-18"
action: "block"
enabled: true
event: "bash"
name: "block-whole-stack-compose-start"
pattern: "(?:\\bdocker[ -]compose\\b[^;&|\\n]*?--profile(?:\\s+|=)(?:'\\*'|\"\\*\"|\\\\\\*|\\*)(?=[\\s;&|'\"]|$)[^;&|\\n]*\\b(?:up|start|create)\\b|\\bdocker[ -]compose\\b[^;&|\\n]*\\b(?:up|start|create)\\b[^;&|\\n]*--profile(?:\\s+|=)(?:'\\*'|\"\\*\"|\\\\\\*|\\*)(?=[\\s;&|'\"]|$)|COMPOSE_PROFILES=['\"]?(?:[\\w-]+,)*\\*(?:,[\\w-]+)*['\"]?(?=[\\s;&|]).*?\\bdocker[ -]compose\\b[^;&|\\n]*\\b(?:up|start|create)\\b)"
---

# BLOCKED: whole-stack Compose start

## Purpose

### Objective

Apply the declared `block` action for block-whole-stack-compose-start.

### Authority

[Environment constraints](../environment-constraints.md#2-infrastructure-constraints),
ENVIRONMENT-CONSTRAINTS-R149 and R150: services on this server start only
by name or by a named profile, never every profile at once.

## Scope

### Applies To

The declared `bash` event and `pattern` match `docker compose` or
`docker-compose` with `up`, `start` or `create` when the command selects
every profile: `--profile '*'` in any quoting, `--profile=*`, or
`COMPOSE_PROFILES` holding `*`, including an earlier `export` in the same
command. Every service in the root project sits behind a profile, so these
are the forms that start the whole stack.

### Exclusions

Rendering and inspection with every profile (`config`, `ps`) stay allowed,
as do starts by named profile or named service.

## Rules

### Requirements

```bash
# BLOCKED: every profile at once
docker compose --profile '*' up -d
COMPOSE_PROFILES='*' docker compose up -d

# ALLOWED: render everything, start a named set
docker compose --profile '*' config --quiet
docker compose --profile core up -d keycloak
```

The declared action applies when the pattern matches.

### Enforcement

The shared dispatcher evaluates the rule before a provider runs the command.
A command assembled at run time, a profile list read from an environment
file, or a hook bypass is outside what the text shows; the operator rule in
environment constraints still applies.

## Exceptions

### Exception Conditions

No exception is declared by this rule.

### Approval and Review

None.

## Ownership

### Responsibilities

`@buenhyden`.

### Change and Adoption

Changes land with their Task evidence and the rule test
`tests/lib/hooks/test_compose_start_rule.py`.
