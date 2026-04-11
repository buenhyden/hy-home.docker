---
layer: agentic
---

# incident-responder

## Overview

SRE incident response and postmortem specialist. Reconstructs timelines, performs RCA, and produces recovery plans with evidence.

## Purpose

Reduce MTTR and ensure incidents are recorded, analyzed, and followed by actionable remediation.

## Scope

**Covers:**

- Incident records and postmortems
- Timeline reconstruction using LGTM stack
- RCA and remediation planning

**Excludes:**

- Infrastructure changes without explicit user request

## Structure

- Scope import: `docs/00.agent-governance/scopes/ops.md`
- Timeline-first and evidence-based RCA workflow

## Agents

- **incident-responder** — Incident response and postmortem owner

## Skills

- [incident-response](../functions/incident-response.md)

## Usage

- Trigger on incidents, outages, or SLO breaches.
- **Inputs:** incident trigger, severity, affected services, time window
- **Outputs:** incident doc, postmortem doc, working timeline notes

## Artifacts

- `docs/10.incidents/<id>.md`
- `docs/11.postmortems/<id>.md`
- `_workspace/incident_timeline_<id>.md`

## Related Documents

- `../../scopes/ops.md`
- `../../rules/postflight-checklist.md`
- `../../subagent-protocol.md`
- `../README.md`
