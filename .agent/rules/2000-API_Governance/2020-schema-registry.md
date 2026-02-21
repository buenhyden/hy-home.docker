---
trigger: model_decision
glob:
  - "contracts/events/**/*.yml"
  - "contracts/events/**/*.yaml"
  - "contracts/events/**/*.json"
  - "schemas/**/*.avsc"
  - "schemas/**/*.proto"
  - "schemas/**/*.json"
description: "Event contract governance: Schema Registry usage, compatibility rules, subject naming, versioning, and deterministic breaking-change control."
---

# 1700-Event-Contract-Schema-Registry

- **Role**: Event Contract Governance Owner
- **Purpose**: Enforce deterministic event schema governance so producers and consumers evolve safely with explicit compatibility guarantees and versioning.
- **Activates When**: Creating/updating event schemas, changing producers/consumers, or modifying schema registry configuration.

---

## 1. Standards (Mandatory Compliance)

### 1.1 Prerequisites (Executable Contract)

- **[REQ-SR-PREREQ-01] Schema Registry Exists**
  - A Schema Registry (or equivalent schema governance service) MUST exist for production-like environments.
  - If missing, event schema changes MUST be blocked.

- **[REQ-SR-PREREQ-02] Canonical Schema Location**
  - All event schemas MUST live under a canonical path:
    - `contracts/events/` OR `schemas/`

- **[REQ-SR-OUT-01] Out of Scope**
  - This Rule does NOT define broker configuration. See Kafka governance rule.
  - This Rule defines schema design, compatibility, and publishing governance.

---

### 1.2 Schema Formats and Ownership

- **[REQ-SR-FMT-01] Allowed Schema Formats**
  - Schemas MUST use one of:
    - Avro
    - Protobuf
    - JSON Schema

- **[REQ-SR-OWN-01] Ownership Metadata**
  - Each schema MUST declare:
    - owning team
    - domain
    - event name
    - versioning strategy

---

### 1.3 Subject Naming and Versioning

- **[REQ-SR-NAM-01] Subject Naming Convention**
  - Subjects MUST follow:
    - `<domain>.<eventName>.<value|key>`
  - Event names MUST be stable and descriptive.

- **[REQ-SR-VER-01] Version Signaling**
  - Breaking changes MUST increment the major version.
  - Schema versions MUST be registered and traceable to a commit SHA.

---

### 1.4 Compatibility Policy (Decision Rule)

- **[REQ-SR-COMP-01] Compatibility Mode Declared**
  - Every subject MUST declare one compatibility mode:
    - BACKWARD
    - FORWARD
    - FULL
    - NONE (ONLY for non-production-like environments)

- **[BAN-SR-COMP-01] NONE in Production-like**
  - Compatibility mode MUST NOT be NONE in production-like environments.

- **[REQ-SR-COMP-02] Breaking Change Control**
  - Any breaking schema change MUST be blocked unless:
    1) a new major version subject exists, OR
    2) a parallel event name is introduced with migration plan.

- **[REQ-SR-COMP-03] Compatibility Tests**
  - Schema changes MUST run automated compatibility checks against the last released version.

---

### 1.5 Schema Design Requirements

- **[REQ-SR-DES-01] Stable Field Semantics**
  - Existing field meaning MUST remain stable across minor versions.

- **[REQ-SR-DES-02] Optional Fields for Evolution**
  - New fields MUST be optional unless the compatibility mode guarantees safety.

- **[BAN-SR-DES-01] Reusing Fields for New Meaning**
  - Fields MUST NOT be repurposed for a different meaning.

---

### 1.6 Success & Failure Behavior

- **[REQ-SR-SUCCESS-01] Success Criteria**
  - Schema change is valid ONLY if:
    - compatibility mode is declared and enforced
    - compatibility tests pass
    - breaking changes are versioned
    - ownership metadata exists

- **[REQ-SR-FAIL-01] Failure Behavior**
  - Any violation of `[BAN-*]` MUST reject the change.
  - Missing compatibility tests MUST block the change.

---

### 1.7 Reference-First

- **[REQ-SR-REF-01] Canonical Examples**
  - Use canonical examples:
    - `contracts/events/_examples/subject-naming.md`
    - `contracts/events/_examples/compatibility-matrix.md`
    - `contracts/events/_examples/schema-evolution.md`

---

## 2. Procedures (Phased Execution)

### Phase P1 — Define the Event Contract

1) Choose schema format and subject name.
2) Declare compatibility mode.
3) Add ownership metadata.

- **Outcome**: Contract identity and policy are explicit.

### Phase P2 — Validate Compatibility

1) Run compatibility checks against last released version.
2) Classify changes as breaking or non-breaking.

- **Outcome**: Compatibility is proven, not assumed.

### Phase P3 — Version and Publish

1) If breaking, publish new major subject or parallel event.
2) Register schema and link to commit SHA.

- **Outcome**: Consumers can migrate deterministically.

---

## 3. Examples

### Good Example — Non-Breaking Evolution

**Input**

- Add an optional field `nickname` under BACKWARD compatibility.

**Expected Output**

- Compatibility checks pass; no major version bump required.

### Bad Example — Breaking Change Without Version

**Input**

- Change `userId` type from integer to string under same subject and major version.

**Rejected Because**

- Violates `[REQ-SR-COMP-02]`.

---

## 4. Validation Criteria (Final Checklist)

- [ ] Schema registry exists for production-like. (`[REQ-SR-PREREQ-01]`)
- [ ] Compatibility mode declared and not NONE in production-like. (`[REQ-SR-COMP-01]`, `[BAN-SR-COMP-01]`)
- [ ] Compatibility checks run and pass. (`[REQ-SR-COMP-03]`)
- [ ] Breaking changes are versioned. (`[REQ-SR-COMP-02]`, `[REQ-SR-VER-01]`)
- [ ] Ownership metadata exists. (`[REQ-SR-OWN-01]`)

---

## See Also

- @0000-Rule-Writing-Standard-Master-v3.md
- @1800-Kafka-Topic-Governance.md
- examples/contracts/events/subject-naming.md
- examples/contracts/events/compatibility-matrix.md
- examples/contracts/events/schema-evolution.md
