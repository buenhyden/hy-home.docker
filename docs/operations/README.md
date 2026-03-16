---
layer: infra
---

# Operations History Hub (`operations/`)

This directory is the **exclusive home for historical records** and diagnostic anomalies. It serves as the project's institutional memory.

## Incident Log & Postmortems

| Date | ID | Severity | Status | Summary | Postmortem |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-02-26 | [2026-02-26-inc-infra-bootstrap](2026-02-26-inc-infra-bootstrap.md) | SEV-3 | RESOLVED | Documentation stack debt audit. | [2026-02-26-rca-infra-bootstrap-postmortem](2026-02-26-rca-infra-bootstrap-postmortem.md) |

## Golden Rules for History Tracking

1. **Mandatory Threading**: Every Postmortem MUST explicitly link back to its corresponding triggering Incident document.
2. **Immutability**: Never delete old incidents or postmortems. They are essential for identifying systemic failures.
3. **Strict Policy**: Reviews focus on system failures (Blameless Culture).
4. **RCA Requirement**: All major incidents result in a "Five Whys" analysis.

---
> [!IMPORTANT]
> Non-historical technical guides belong in **[Documentation Hub](../context/README.md)**.

Use this README as the lazy-load entrypoint for historical operational records.
