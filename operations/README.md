# Operations Tracking

This directory (`operations/`) serves as the permanent, historical record for production events and system failures. It is distinctly separate from `runbooks/`, which contains executable procedures, and `OPERATIONS.md` in the root directory, which defines the global operational blueprint.

## Directory Structure

- **`incidents/`**: Active and resolved incident tracking documents.
  - Every time an alert fires or an incident is declared, a document must be created here using `templates/operations/incident-template.md`.
- **`postmortems/`**: Detailed "after-action" reviews for SEV-1 and SEV-2 incidents.
  - Must be created using `templates/operations/postmortem-template.md`.

## Golden Rules for Operations Tracking

1. **Mandatory Linking**: Every Postmortem (`operations/postmortems/*.md`) MUST explicitly link back to its corresponding triggering Incident document (`operations/incidents/*.md`). An incident without a postmortem (if SEV-1/SEV-2) is considered incomplete.
2. **Immutable History**: Do not delete old incidents or postmortems. They serve as the project's institutional memory and help identify systemic weaknesses over time.
3. **Template Enforcement**: Always use the standardized templates to ensure all necessary metadata (Severity, Timelines, Action Items) is accurately captured.
4. **Blameless Post-Mortem Culture**: Per `[REQ-RSK-03]`, incident reviews MUST focus on system and process failures rather than individual errors. The goal is learning and prevention, not blame.
5. **Documented Root Cause Analysis (RCA)**: Per `[REQ-RSK-10]`, all significant incidents MUST result in a documented RCA featuring a "Five Whys" analysis and actionable remediation items.

## AI Agent Guidelines

AI Agents interacting with incidents or postmortems must rigidly follow these rules:

1. **Strict Rule Adherence**: Agents MUST validate all operational documentation against `.agent/rules/0380-incident-response.md` and `.agent/rules/0385-risk-management-standard.md`.
2. **Template Compliance**: When generating postmortems, agents must explicitly include the "Five Whys" structure.
3. **Actionable Remediation**: Agents must ensure that identified action items from the RCA explicitly address the root causes found in the "Five Whys" analysis.
