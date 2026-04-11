---
layer: agentic
---

# incident-response

## Overview

Incident response playbook for Docker infrastructure. Emphasizes timeline reconstruction, evidence-based RCA, and postmortem completion.

## Purpose

Provide a repeatable response workflow for outages, SLO breaches, and security incidents.

## Scope

**Covers:**

- Incident detection and classification
- Timeline reconstruction and RCA
- Postmortem creation and follow-up actions

**Excludes:**

- Non-infra incidents unrelated to runtime services

## Structure

- Phases: detect → timeline → mitigation → RCA → recovery → postmortem

## Agents

- **incident-responder** — primary operator

## Skills

- This function is the incident response orchestration skill.

## Usage

- Trigger on service outages, SLO breaches, or suspected secret exposure.
- **Inputs:** incident trigger, severity, affected services
- **Outputs:** incident and postmortem documents

## Artifacts

- `docs/10.incidents/<id>.md`
- `docs/11.postmortems/<id>.md`
- `_workspace/incident_timeline_<id>.md`

## Related Documents

- `../../scopes/ops.md`
- `../../rules/postflight-checklist.md`
- `../README.md`
