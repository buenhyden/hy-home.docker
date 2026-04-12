---
name: adr-writing
description: >
  Architecture Decision Record (ADR) writing reference for hy-home.docker infrastructure decisions.
  Covers MADR format guidance, ADR status lifecycle, category numbering, quality attribute
  tradeoff matrix (CAP theorem, weighted scoring, ATAM), and ADR quality checklist.
  Use for 'ADR', 'architecture decision', 'tradeoff analysis', 'quality attributes', 'CAP theorem',
  'weighted scoring', 'ATAM', 'decision status', 'rejection rationale'.
  Enhances doc-writer. Note: this skill guides ADR writing; it does not run performance tests.
---

# ADR Writing — Architecture Decision Reference for hy-home.docker

Reference for the `doc-writer` agent when authoring Architecture Decision Records
for infrastructure, security, and operational decisions in this Docker-based home lab.

## ADR Status Lifecycle

```
[Proposed] -> [Accepted] -> [Deprecated]
                   |
             [Superseded by ADR-NNN]
```

| Status | Meaning | When to Use |
|--------|---------|-------------|
| **Proposed** | Under review | Immediately after writing; awaiting stakeholder consensus |
| **Accepted** | Adopted decision | Consensus reached; implementation may begin |
| **Deprecated** | No longer valid | Premises changed but no direct replacement |
| **Superseded** | Replaced by new ADR | An explicit follow-up ADR re-evaluates this decision |

Update the Status field and add a Change History entry whenever the status transitions.

## Category-Prefixed Numbering System

```
docs/03.adr/NNNN-<category>-<short-title>.md

Category codes (hy-home.docker):
  INFRA  — Docker Compose, networking, resource allocation
  SEC    — Secrets management, auth, TLS, access control
  OPS    — Observability, backups, incident response, SLO policy
  DATA   — Storage engines, retention, migration strategy
  ARCH   — Cross-cutting patterns, service boundaries, protocols
```

Examples:
- `0001-infra-network-isolation-strategy.md`
- `0002-sec-secrets-docker-vs-env.md`
- `0003-ops-log-aggregation-loki-vs-elk.md`
- `0004-data-postgres-high-availability.md`

Always check the highest existing sequence number in `docs/03.adr/` before assigning a new one.

## MADR-Extended Template (hy-home.docker)

Use `docs/99.templates/adr.template.md` as the base, then add these sections:

```markdown
## Status

Proposed | Accepted | Deprecated | Superseded by ADR-NNN

## Decision Drivers

* [Driver 1: e.g., Container P99 latency must stay below 200ms]
* [Driver 2: e.g., No plaintext credentials in docker inspect output]
* [Driver 3: e.g., Recoverable within 30 minutes after single host failure]

## Quality Attribute Assessment

[See quality attribute matrix below — fill in for INFRA/DATA decisions]

## Validation Criteria

- [ ] [Metric or observable that proves the decision is correct — with deadline]
- [ ] [Rollback criterion — what would trigger reverting to a previous approach]

## Change History

| Date | Status | Reason |
|------|--------|--------|
| YYYY-MM-DD | Proposed | Initial write |
```

### Rejection Rationale (Required)

Every rejected alternative must state **why it was rejected**, not just what it is.

Good: "Alternative B (Vault) was rejected because it requires an additional persistent service and Vault unsealing ceremony on every host restart, adding operational complexity disproportionate to a single-host home lab."

Bad: "Alternative B was not chosen."

Future engineers will re-propose alternatives that were already considered. Explicit rejection rationale prevents this.

---

## Quality Attribute Analysis

Apply to INFRA, DATA, and ARCH decisions. Use the weighted scoring matrix to make
tradeoffs explicit and comparable.

### Quality Attribute Dictionary — hy-home.docker Context

| Attribute | Definition | Measurement | Target |
|-----------|-----------|-------------|--------|
| **Performance** | Container response time, throughput | p99 latency, TPS | p99 < 200ms (LATENCY_SLO) |
| **Availability** | Uptime under normal conditions | Uptime %, MTTR | 99.9% (43.8 min/month budget) |
| **Reliability** | Error-free operation | Failure rate, MTBF | MTTR < 30 min |
| **Security** | Resistance to threats | CVSS findings, audit gaps | Zero CRIT/HIGH unmitigated |
| **Maintainability** | Ease of change and operation | Config complexity, change lead time | Solo operator maintainable |
| **Deployability** | Frequency and safety of changes | Deploy frequency, rollback time | Rollback < 5 min |
| **Observability** | System state visibility | Log coverage, dashboard coverage | All services in Loki + Grafana |
| **Cost** | Resource consumption | CPU/RAM overhead, disk usage | Fits within host resource envelope |

### Common Tradeoff Relationships

| If you increase... | This may decrease... | Reason |
|--------------------|----------------------|--------|
| Performance (caching) | Consistency | Stale cache vs. fresh data |
| Security (encryption, auth) | Performance | Cryptographic overhead |
| Scalability (replication) | Consistency | CAP theorem — AP vs. CP |
| Flexibility (abstraction layers) | Performance | Indirection overhead |
| Availability (redundancy) | Simplicity / Cost | Additional services to operate |

### CAP Theorem — Distributed Storage Decision

When choosing or configuring stateful services in hy-home.docker:

```
Consistency + Availability + Partition Tolerance: choose 2.

CP  (Consistent + Partition Tolerant):
    PostgreSQL (primary), Redis (when cluster mode off), Zookeeper
    -> Rejects writes during partition to preserve consistency

AP  (Available + Partition Tolerant):
    Kafka (consumer groups), OpenSearch (replica read), MinIO (distributed)
    -> Serves possibly stale data during partition to preserve availability

CA  (Consistent + Available, no partition tolerance):
    Single-node PostgreSQL, single-node Redis
    -> Safe only in single-host setup with no network partitions
```

For a single-host home lab: CA is acceptable for most services. Document explicitly when choosing AP for a multi-replica service.

### Weighted Scoring Matrix Template

```markdown
| Quality Attribute | Weight | Alt A | Wtd A | Alt B | Wtd B | Alt C | Wtd C |
|-------------------|--------|-------|-------|-------|-------|-------|-------|
| Performance       | ___%   |       |       |       |       |       |       |
| Availability      | ___%   |       |       |       |       |       |       |
| Security          | ___%   |       |       |       |       |       |       |
| Maintainability   | ___%   |       |       |       |       |       |       |
| Deployability     | ___%   |       |       |       |       |       |       |
| Observability     | ___%   |       |       |       |       |       |       |
| Cost              | ___%   |       |       |       |       |       |       |
| **Total**         | **100%** |    |       |       |       |       |       |

Score each alternative 1–5 per attribute. Weighted score = Weight x Score.
```

#### Weight Guidelines by Decision Type

| Decision Type | Performance | Security | Maintainability | Cost | Observability |
|--------------|-------------|----------|-----------------|------|---------------|
| Network/Proxy (INFRA) | 25% | 20% | 20% | 10% | 15% |
| Secrets Management (SEC) | 10% | 35% | 25% | 10% | 15% |
| Storage Engine (DATA) | 20% | 15% | 20% | 20% | 15% |
| Logging/Monitoring (OPS) | 15% | 10% | 20% | 15% | 30% |

### Simplified ATAM (Architecture Tradeoff Analysis)

For decisions with significant architectural impact (ARCH category or cross-cutting changes):

```
Step 1 — Identify Architecture Drivers
  Core operational goals + quality attribute scenarios (specific, measurable)

Step 2 — Utility Tree
  Quality attribute -> Sub-item -> Scenario -> Priority (High/Med/Low)
  Example: Availability -> Single-host restart -> "Service restores in < 5 min" -> High

Step 3 — Analyse Each Alternative
  For each alternative: which scenarios does it satisfy? Which does it risk?

Step 4 — Identify Sensitivity Points and Tradeoffs
  Sensitivity: a decision that strongly affects one attribute
  Tradeoff: a decision that benefits one attribute at the cost of another

Step 5 — Classify Risks
  Resolved tradeoff: accepted with mitigation documented
  Unresolved risk: record in ADR as "Risk: [description]; Mitigation: [TBD or planned action]"

Step 6 — Compile for ADR
  List the top 3 tradeoffs in the Consequences section.
  List unresolved risks in a Risk/Mitigation table.
```

---

## ADR Writing Quality Checklist

### Required Elements

- [ ] Context explains the trigger: why is this decision needed now?
- [ ] Decision Drivers are listed (specific, measurable where possible)
- [ ] At least 3 alternatives compared
- [ ] Pros and cons of each alternative are specific, not generic
- [ ] Selection rationale is logical and references the Decision Drivers
- [ ] Rejection reasons are explicitly stated for every rejected alternative
- [ ] Tradeoffs (negative consequences) are honestly described
- [ ] Validation Criteria are testable (not "should be fast" — "p99 < 200ms")
- [ ] Related ADRs are listed
- [ ] Status field is set

### Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Decision stated without context | Write "why was this decision needed" first |
| Only one alternative | Always document at least 2 rejected alternatives |
| Consequences only positive | Honestly record cons and tradeoffs — these inform future engineers |
| Vague rejection: "not chosen" | Specific rejection: "rejected because X would require Y which conflicts with Z" |
| ADR never updated | Always update Status and Change History when reality changes |
| Too long | Target 1–3 pages; link to detailed analyses rather than embedding them |
| Implementation spec disguised as ADR | ADR records the decision and rationale; the spec records how to implement it |

### hy-home.docker-Specific Checklist (INFRA/SEC decisions)

- [ ] Impact on `no-new-privileges`, `mem_limit`, `infra_net` assessed
- [ ] Secrets management impact documented (does this require a new secret? Rotation procedure?)
- [ ] Health-check and restart policy consequences noted
- [ ] SLO error budget impact estimated (does this choice affect the 99.9% availability target?)
- [ ] Rollback procedure described (how do we revert if this decision proves wrong?)
