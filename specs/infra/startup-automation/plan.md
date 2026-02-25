---
title: 'Startup Automation & Makefile Plan'
status: 'Draft'
version: '1.0'
owner: 'Platform/DevOps'
spec_reference: './spec.md'
tags: ['plan', 'infra', 'startup', 'automation']
---

# Startup Automation & Makefile Plan

## 1. Execution Phases

### Phase 1: Interactive Preflight

- **TASK-BOT-01**: Enhance `scripts/preflight-compose.sh` with `.env` auto-copy and prompt logic.

### Phase 2: Makefile Implementation

- **TASK-BOT-02**: Create root `Makefile` with targets: `setup`, `up`, `down`, `status`, `logs`, `validate`.

### Phase 3: Documentation

- **TASK-BOT-03**: Update root `README.md` to introduce the `make` workflow as the primary entry point.

## 2. Verification Plan

- [ ] Execute `make setup` and verify `.env` presence.
- [ ] Execute `make up` and verify services are running via `docker compose ps`.
- [ ] Run `make validate` to ensure script integrity.
