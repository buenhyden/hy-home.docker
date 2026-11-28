---
title: "OpenBao Audit Retention and Capacity Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0024"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-11-28"
---

# OpenBao Audit Retention and Capacity Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion 25/W85 in the [Spec](../spec.md) and [Plan](../plan.md): the
rest of W6 that [TSK-0006](tsk-0006-openbao-trust-bootstrap-and-recovery.md)
leaves open after [TSK-0023](tsk-0023-logrotate-failure-alert.md) added the
failure alert: measured growth, retention, audit filesystem capacity and the
rotated-inode check.

##### Inputs and Authority

On 2026-11-28 the user asked in this chat to handle the rest of W6 and, asked
here, chose `maxsize 512M` for 14-day retention and `chmod o+x /home/hyunyoun`
so node-exporter can read the audit filesystem. Work ran in the primary
checkout on branch `feat/openbao-audit-retention` from `main` `14b223211`;
brief `audit-retention` bound the changed files. Only file metadata was read;
no audit content or secret was read. Direct user authorization is authority;
this record is not.

#### Execution Log

##### Work Performed

###### Changes

| Area | Change |
| --- | --- |
| Measurement | The audit file grows about 250-270 MB a day. With `maxsize 256M` most days rotated twice, by size near 22:00 KST and daily at 00:00 KST (rotated files ~11 MB and ~1 MB compressed), so `rotate 14` kept about 7-8 days, not 14. The audit filesystem is `/home/hyunyoun/storage` (`/dev/sdb`, 2.7 TB, 82.5% free), not `/` |
| Rule | `infra/03-security/openbao/config/logrotate/openbao`: `maxsize 512M`; the provisional-sizing comment is replaced by the measurement. Only the daily rotation runs at the current volume, about 14 days and ~1 GB are kept, and a burst near twice the daily volume is still cut |
| Capacity metric | node-exporter runs as `nobody` and `/home/hyunyoun` was 0750, so statfs of `/home/hyunyoun/storage` failed (`node_filesystem_device_error` 1) and `SeaweedFSDataDiskLow`, the only alert on that filesystem, could never fire. `chmod o+x /home/hyunyoun` (751, traverse only, run by the user's own account) fixed it; listing the home directory is still refused. The rule file comment records the dependency |
| Docs | RUN-0105 rule sizing and Audit Rotation Contract: the measurement, the filesystem and its alert dependency, and the owner reinstall with a parser check |

##### Blockers and Decisions

The new rule takes effect when the owner reinstalls `/etc/logrotate.d/openbao`
with sudo (RUN-0105). Until then the host keeps `maxsize 256M`.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 25 | W85 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_openbao_audit_rotation | `maxsize 512M` assertion before the rule change | FAIL | The rule still had 256M | required | - |
| E02 | 25 | W85 | method=automated; tool=Python3 venv; command=python -m unittest tests.validation.test_openbao_audit_rotation | After the rule change | PASS | OK | required | E01 |
| E03 | 25 | W85 | method=observation; tool=docker exec stat/ls -lni of the audit directory (metadata only); command=audit inodes, sizes and mtimes | HOME, 2026-11-28 21:20 KST; listed in UTC | PASS | audit.json inode 115607912 at 221,574,640 bytes and still written; audit.json.1 inode 115607799 (the 2026-11-27 rotation in SPEC-0212 TSK-0128 E09) at 249,156,752 bytes with its mtime still the rotation time, so it stopped growing for over 30 hours; 14 compressed files back to 2026-11-20 alternate ~11 MB size rotations near 13:00 UTC and ~1 MB daily rotations at 15:00 UTC | required | - |
| E04 | 25 | W85 | method=observation; tool=Prometheus API; command=node_filesystem_device_error, avail/size and SeaweedFSDataDiskLow for mountpoint /home/hyunyoun/storage | HOME, 2026-11-28 before the change | FAIL | device_error 1, no avail or size series, so the alert had no input | required | - |
| E05 | 25 | W85 | method=observation; tool=Prometheus API; command=node_filesystem_device_error, avail/size and SeaweedFSDataDiskLow for mountpoint /home/hyunyoun/storage | HOME, 2026-11-28 after `chmod o+x /home/hyunyoun` | PASS | device_error 0, avail/size 0.825 on /dev/sdb, SeaweedFSDataDiskLow inactive with health ok; node-exporter still cannot list /host/root/home/hyunyoun | required | E04 |
| E06 | 25 | W85 | method=observation; tool=cmp, logrotate -d, docker exec ls -lni; command=installed rule equals the source, parser clean, the next rotations are daily only | HOME after the owner reinstall | NOT_RUN | Owner reinstall pending | required | - |

##### Resolution Links

E02 resolves E01. E05 resolves E04. E06 runs after the owner reinstall.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 25 | pending | E01,E02,E03,E04,E05,E06 | Awaiting the owner reinstall (E06) and acceptance | @buenhyden |

##### Remaining Conditions

- E06 after the owner reinstall and the next natural rotations.

#### Handoff

##### Promotion Receipt

The sizing and the reinstall are promoted to RUN-0105.

##### Next Owner

@buenhyden reinstalls the rule with sudo.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
