# Operations History Hub

This directory (`operations/`) is the **exclusive home for historical records** and diagnostic anomalies. It serves as the project's institutional memory for what has happened in the past.

> [!IMPORTANT]
> Non-historical technical guides and service context have been migrated to the **[Documentation Hub](../docs/context/)** to maintain a clean separation between design context and incident history.

## Historical Data Stores

- **`incidents/`**: Active and resolved incident tracking documents.
  - Every time an alert fires or an incident is declared, a document must be created here using `../../templates/operations/incident-template.md`.
- **`postmortems/`**: Detailed "after-action" reviews for SEV-1 and SEV-2 incidents.
  - Must be created using `../../templates/operations/postmortem-template.md` and linked in `incidents/README.md`.

## Golden Rules for History Tracking

1. **Mandatory Threading**: Every Postmortem (`postmortems/*.md`) MUST explicitly link back to its corresponding triggering Incident document (`incidents/*.md`).
2. **Immutability**: Never delete old incidents or postmortems. They are essential for identifying systemic failures over time.
3. **Strict Policy**: Per `[REQ-RSK-03]`, reviews focus on system failures (Blameless Culture).
4. **RCA Requirement**: Per `[REQ-RSK-10]`, all major incidents result in a "Five Whys" analysis.

## Navigation Reference

| Content Type | Location |
| :--- | :--- |
| **Historical Records** | `operations/` (This folder) |
| **Technical Context** | `docs/context/` |
| **Executable Procedures** | `runbooks/` |
