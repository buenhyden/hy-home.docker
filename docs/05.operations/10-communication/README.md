# Operations — 10 Communication

> Mail and communication operations grouped by stable subject and role.

## Overview

This domain co-locates the existing Stalwart and MailHog guide, policy, and
runbook under the frozen `ops-0070-mail` identity. No operational role is
created beyond the three roles recorded in the migration ledger.

## Audience

- Operators, SREs, platform engineers, developers, and AI agents.

## Scope

- Optional communication-stack use, DNS/TLS and access controls, hardening,
  evidence collection, recovery, and escalation.
- No service restart, DNS mutation, credential access, or deployment action is
  authorized by this index.

## Structure

| Subject | Available documents |
| --- | --- |
| [Mail](./ops-0070-mail/guide.md) | [Guide](./ops-0070-mail/guide.md), [Policy](./ops-0070-mail/policy.md), [Runbook](./ops-0070-mail/runbook.md) |

## How to Work in This Area

Use the guide for routine context and non-destructive checks, the policy for
mandatory controls and exceptions, and the runbook for ordered recovery. The
guide hands off to the sibling runbook only because that runbook exists.

## Related Documents

- [Operations index](../README.md)
- [Communication infrastructure](../../../infra/10-communication/README.md)
- [Incident records](../incidents/README.md)
- [Release records](../releases/README.md)
