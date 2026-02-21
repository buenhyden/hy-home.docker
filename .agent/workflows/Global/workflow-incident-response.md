---
description: AI Ops Agent logic for responding to system alerts and managing incidents.
---

# Workflow: Incident Response

This workflow defines the execution loop for the **Ops Agent** when an automated alert or human report triggers an incident response.

## 1. Alert Triage & Containment

When triggered by an alert (e.g., from Prometheus, Datadog, or PagerDuty):

1. **Acknowledge**: Immediately register the alert and confirm assignment.
2. **Context Gathering**: Pull the relevant logs, metrics, and recent CI/CD deployment history.
3. **Severity Assessment**: Review `0380-incident-response.md` to determine if this is a SEV-1, SEV-2, or SEV-3 incident.
4. **Immediate Containment**: If a recent deployment caused an elevated error rate (e.g., SEV-1), draft a rollback plan or disable the offending feature flag immediately and request human approval.

## 2. Root Cause Analysis (RCA)

Once the system is stabilized (or if it is a non-critical alert):

1. Trace the error through the application logs and correlate it with recent infrastructure or code changes.
2. Document a "Five Whys" analysis.
3. Identify the faulty component, missing unit test, or infrastructure bottleneck.

## 3. Postmortem Drafting

1. Gather all findings from the RCA phase.
2. **Template Enforcement**: You MUST use `templates/operations/postmortem-template.md`.
3. Save the drafted postmortem document to `docs/manuals/postmortems/YYYY-MM-DD-[incident-name].md`.
4. The document MUST include actionable remediation steps (e.g., adding a new E2E test, updating an alert threshold).

## 4. End State

Notify the human engineering team that the incident has been analyzed, contained (if applicable), and the Postmortem draft is ready for their final review and approval.
