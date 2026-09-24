---
title: "Messaging Tier (05-messaging)"
version: "1.1.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-24"
created: "2025-11-12"
---

# 05 Messaging

## Overview

The current tier contains one [`kafka`](kafka/README.md) package. It is an
OPTIONAL Kafka-family event-streaming surface; no second broker family is present.

## Audience

This package map is for operators and maintainers of the messaging tier.

## Scope

It covers the current Kafka package and its root Compose selectors.

## Structure

The tier has one leaf package: [`kafka`](kafka/README.md).

## How to Work in This Area

The exact root selectors are `messaging`, `messaging-broker`,
`messaging-cluster`, `messaging-schema`, `messaging-connect`, `messaging-rest`,
and `messaging-admin`; use the package map to see which services each
selects. A named producer and
consumer, retention/capacity plan, plaintext-listener risk acceptance and complete
recovery plan are required before activation. Three brokers on one host are not
host availability.

## Related Documents

Use the [documentation entry point](../../docs/README.md) to locate Stage 05
Messaging subjects `05-messaging/0036-kafka` and
`05-messaging/0037-optimization-hardening`.
