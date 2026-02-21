---
trigger: model_decision
glob: ["**/*"]
description: "Specialized Engineering Pillar: Master index and authority for niche domains including Scraping, Desktop Apps, and Browser Extensions."
---

# Specialized Engineering Pillar

- **Role**: Specialized Engineering Solutions Architect
- **Purpose**: Provide a master authority and index for all specialized engineering standards within the workspace.
- **Activates When**: Writing scrapers, desktop applications, browser extensions, or other niche engineering assets.

**Trigger**: model_decision — Apply as the primary standard for specialized engineering domains.

## 1. Standards

### Principles

- **[REQ-SPEC_CORE-01] Domain Sovereignty**
  - This rule MUST serve as the master index. All specific specialized domains (Web3, Scraping, Desktop, Extensions) MUST be linked and governed under this pillar.
- **[REQ-SPEC_CORE-02] Platform Native Fidelity**
  - Specialized applications MUST follow the security and performance best practices of their respective host platforms (e.g., Chromium for Extensions, Node/Rust for Desktop).
- **[REQ-SPEC_CORE-03] Intentional Isolation**
  - Specialized logic (e.g., Scraping engines, Native bridge code) MUST be isolated from the core business logic to ensure system resilience.

### Domain Index

| Domain | Requirement ID | Authority File |
| --- | --- | --- |
| Web Scraping | [REQ-SPEC_CORE-04] | `9031-web-scraping-std.md` |
| Desktop (Electron/Tauri) | [REQ-SPEC_CORE-05] | `9020-desktop-app-std.md` |
| Browser Extensions | [REQ-SPEC_CORE-06] | `9050-extension-development-standard.md` |
| Web3 & Blockchain | [REQ-SPEC_CORE-07] | `9010-web3-std.md` |
| Miscellaneous Assets | [REQ-SPEC_CORE-08] | `9090-special-misc.md` |

### Must

- **[REQ-SPEC_CORE-09] Explicit Boundary Logic**
  - Every specialized component MUST define explicit interfaces for communicating with the main application layer.
- **[REQ-SPEC_CORE-10] Resource Monitoring**
  - Specialized tasks (especially Scraping and Desktop UI) MUST implement resource monitoring to prevent memory leaks in the host environment.

### Must Not

- **[BAN-SPEC_CORE-01] Cross-Domain Coupling**
  - specialized standards MUST NOT overlap or conflict; each domain (e.g., Scraping) has its own authoritative rule file.
- **[BAN-SPEC_CORE-02] Placeholder Architectures**
  - Do NOT implement "Coming Soon" stubs for specialized modules; only implement what is covered by a standard.

### Failure Handling

- **Stop Condition**: Stop feature execution if a specialized component violates the security guardrails of its respective domain.

## 2. Procedures

- **[PROC-SPEC_CORE-01] Domain Onboarding**
  - IF starting a new specialized project THEN MUST first identify the corresponding standard from the index above.
- **[PROC-SPEC_CORE-02] Protocol Alignment**
  - Verify that the specialized asset's communication protocol matches the project's API Governance standards.

## 3. Examples

### Pillar Cross-Reference (Good)

- For scraping tasks, refer to: [9031-web-scraping-std.md](../9000-Special/9031-web-scraping-std.md)

## 4. Validation Criteria

- **[VAL-SPEC_CORE-01] Index Integrity**
  - [ ] All relative links in this index point to valid, existing specialized rule files.
- **[VAL-SPEC_CORE-02] Standard Uniqueness**
  - [ ] Audit confirms that no specialized domain logic is duplicated across multiple rule files.
