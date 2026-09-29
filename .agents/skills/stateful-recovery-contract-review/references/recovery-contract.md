# Recovery Contract Matrix

Review only sanitized facts supplied for the named system and scope. Record the
source and observation time for evidence without copying secret values, raw
credentials, or unrelated runtime data.

| Area | Required contract facts | Ready condition |
| --- | --- | --- |
| State and volumes | Stateful components, data classes, volume or storage identifiers, ownership, and exclusions | Every required state source has one disposition and owner. |
| Backup or rebuild | Sanitized backup artifact identity, source, capture or freshness time, integrity result, and dated prior restoreability verification; or the versioned inputs and deterministic procedure that prove rebuildability | Each state source has a backup whose identity, integrity, freshness, and dated prior restoreability evidence support the reviewed scope, or a provable rebuild path; volume existence alone is insufficient. |
| Consistency | Quiescing, snapshot, transaction, replication, or other consistency boundary and its dependent components | The method covers the dependency set and states its consistency limit. |
| Retention and capacity | Retention window, restore-point selection, source size, target capacity, and expected growth | The selected restore point is retained and the target has bounded capacity evidence. |
| Encryption and key custody | Encryption boundary plus named key custodian and approved key-availability process, without key material | Required keys have an accountable custody and availability path. |
| Dependency and restore order | Ordered components, prerequisites, identity or network dependencies, and decision points | The order is complete and has explicit stop conditions. |
| Version compatibility | Source version, target version, format or schema compatibility, and required migrations | Compatibility is supported by current evidence and migrations are bounded. |
| Isolated target | Named non-production or otherwise isolated target, access boundary, network boundary, and cleanup owner | Validation cannot affect the source or an unapproved runtime. |
| RPO and RTO | Objectives, separately recorded observations, observation time, and measurement method | Objectives and observations are labeled separately; an objective is never reported as an observed result. |
| Application acceptance | Data integrity, application behavior, dependency, and rollback checks with expected results | Checks determine whether the restored application is usable, not only whether storage mounted. |
| Failure and stop | Abort signals, partial-result handling, preservation needs, cleanup, and escalation owner | Unsafe, ambiguous, or partial recovery has a bounded stop and escalation path. |
| Responsibility | Named implementer, independent reviewer, and human approver for the separate operational action, each assigned to a distinct identity or role | Implementation, independent review, and human approval are pairwise distinct; no implementer or reviewer approves their own protected action or review. |

Any missing row, contradiction, stale evidence that cannot support the stated
scope, or request for secret/live inspection makes the verdict `BLOCKED`.

Dated historical recovery observations are supplied evidence only. They do not
mean this review executed recovery. The verdict always records the current
operational action as `NOT_RUN` and records historical operational evidence
separately with its source and observation time.
