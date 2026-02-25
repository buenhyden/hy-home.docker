---
title: 'Startup Automation & Makefile Spec'
status: 'Draft'
version: '1.0'
owner: 'Platform/DevOps'
prd_reference: 'N/A'
api_reference: 'N/A'
arch_reference: '../../ARCHITECTURE.md'
tags: ['spec', 'infra', 'startup', 'automation', 'makefile']
---

# Startup Automation & Makefile Spec

## 1. Technical Overview

This specification covers the implementation of a root-level `Makefile` and enhancements to the `scripts/preflight-compose.sh` script. The goal is to provide a unified, user-friendly interface for initializing the infrastructure, managing TLS certificates, and controlling core services.

## 2. Coded Requirements (Traceability)

| ID | Requirement Description | Priority |
| :-- | :-- | :-- |
| **REQ-BOT-001** | A root `Makefile` MUST be provided for consolidated command management (`make up`, `make setup`). | High |
| **REQ-BOT-002** | `scripts/preflight-compose.sh` MUST handle automatic `.env` creation from `.env.example` with user confirmation. | High |
| **REQ-BOT-003** | The `Makefile` MUST include targets for `status`, `logs`, and `validate`. | Medium |

## 3. Automation Details

### 3.1 root Makefile

The `Makefile` will define the following targets:

- `setup`: Combined execution of environment checks and certificate generation.
- `up`: Starts the primary infrastructure stack in detached mode.
- `down`: Stops and removes core service containers.
- `status`: Displays current container health and status.
- `validate`: Runs syntax checks across all included compose files.

### 3.2 scripts/preflight-compose.sh

The script will be updated to:

- Detect the absence of a `.env` file.
- Prompt the user: `[?] .env not found. Copy from .env.example? (y/n)`.
- Verify the existence of required directories (e.g., `volumes/`).

## 4. Verification Plan

- **[VAL-BOT-001]**: `make setup` successfully creates a functional `.env`.
- **[VAL-BOT-002]**: `make up` and `make down` correctly manage the core stack.
- **[VAL-BOT-003]**: `make status` reports accurate service health.
