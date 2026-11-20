---
title: "Mailpit in HOME and Stalwart as a LAB"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "architecture"
artifact_id: "ADR-0054"
parent_ids:
- "AD-0010"
created: "2026-11-06"
---

# ADR-0054: Mailpit in HOME and Stalwart as a LAB

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-decision payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context

##### Problem and Drivers

Development mail must never reach a real recipient. The HOME SMTP trap is
Mailpit (`infra/11-quality/mailpit/`, root-included). Stalwart is a
standalone LAB (`labs/stalwart/`, SPEC-0262) and is not root-included.
`infra/10-communication/` holds only a README. No production mail server is
deployed.

- Captured development mail must stay local.
- A real mail server needs DNS, a fixed address and deliverability evidence the
  home host does not provide today.
- HOME should hold only services that run every day.

###### Sources
<!-- core-payload-level:4 -->

Evidence is the current repository configuration and
`scripts/hardening/check-all-hardening.sh`, which checks
`labs/stalwart/docker-compose.yml` and its relay refusal; no runtime state is
claimed.

- [REQ-0011 Communication](../../01.requirements/0011-communication.md)
- [AD-0010 Communication architecture](../01.descriptions/0010-communication-architecture.md)
- [POL-0107 LAB promotion](../../05.operations/02.policies/15.labs/0107-lab-promotion.md)

##### Decision Scope

This decision covers the development SMTP trap, the Stalwart LAB and the
`10-communication` tier name. No production mail server is selected.

#### Options

##### Considered Options

- Keep MailHog: rejected; the tree runs Mailpit, the maintained successor with
  the same capture model.
- Promote Stalwart into HOME now: rejected; no deliverability evidence and no
  consumer needs outbound mail.
- Mailpit in HOME, Stalwart as a LAB until promoted: selected.

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Keep MailHog | The ADR records no benefit for this option. | The tree runs Mailpit, the maintained successor with the same capture model. | Rejected; the tree runs Mailpit, the maintained successor with the same capture model. |
| Promote Stalwart into HOME now | The ADR records no benefit for this option. | No deliverability evidence exists, and a real mail server needs DNS, a fixed address and deliverability evidence the home host does not provide today. | Rejected; no deliverability evidence and no consumer needs outbound mail. |
| Mailpit in HOME, Stalwart as a LAB until promoted | Development mail cannot leave the host, and HOME carries no mail server to secure or monitor. | No real outbound or inbound mail exists until Stalwart is promoted. | Selected; captured development mail must stay local and HOME should hold only services that run every day. |

- Trade-off: no real outbound or inbound mail exists until Stalwart is
  promoted.

#### Decision

##### Chosen Option

1. Mailpit in `11-quality` is the HOME SMTP trap. It captures mail without
   relaying it, and its UI sits behind
   `gateway-standard-chain`, `sso-errors` and `sso-auth`.
2. Stalwart stays a LAB in `labs/stalwart/`. It refuses relaying, and its
   hardening check runs against the LAB source.
3. No production mail server is selected. Promoting Stalwart follows the LAB
   promotion policy (POL-0107) and needs TLS, DNS (SPF, DKIM) and
   deliverability evidence first.
4. `10-communication` keeps its tier name and README only; it owns no HOME
   service.

##### Authority and Effect

Decided by the owner, @buenhyden; status `accepted`. No separate approval
record is linked. Effective from 2026-11-06.

###### Supersession
<!-- core-payload-level:4 -->

This record replaces ADR-0010, deleted in the same change (ADR-0051); ADR-0010
is historical and non-authoritative. ADR-0010
selected MailHog as the development SMTP trap (in-memory, no external relay,
port 1025) and Stalwart as the production mail server under
`10-communication` (Rust single binary; JMAP, IMAP and SMTP; ports
25/465/587/993; persistent mail store; web UIs behind the Traefik SSO chain;
TLS and DNS deliverability verified before production). It named no rejected
candidates. The trap is now Mailpit, and Stalwart is an unpromoted LAB.

#### Consequences

##### Impacts

- Positive: development mail cannot leave the host.
- Positive: HOME carries no mail server to secure or monitor.

##### Follow-up

On 2026-11-17 the owner, @buenhyden, directed an in-place amendment of this
record: its sections moved line for line to the core decision form, and the
options table under Trade-offs was derived from the options it records. The
decision text is unchanged.

Communication requirement and description text that still names MailHog or a
production Stalwart is reconciled by its owners.

###### Compliance
<!-- core-payload-level:4 -->

`check_11_quality` and the Stalwart checks in
`scripts/hardening/check-all-hardening.sh` guard both boundaries.

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
