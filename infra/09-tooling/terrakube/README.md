# Terrakube IaC Automation

> Enterprise-grade Terraform orchestration and remote state management.

## Overview

Terrakube provides a centralized platform for managing Terraform workflows. It handles API-driven execution, private registry for modules, and secure remote state storage using MinIO (S3-compatible).

## Audience

- DevOps Engineers (Automation)
- Platform Engineers (IaC governance)

## Structure

```text
terrakube/
├── docker-compose.yml  # API, UI, and Executor orchestration
└── README.md           # This file
```

## How to Work in This Area

1. Read the [IaC Automation Guide](../../../docs/07.guides/09-tooling/01.iac-automation.md).
2. Access the UI at `https://terrakube-ui.${DEFAULT_URL}`.

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| API / UI | Terrakube | v2.29.0 |
| Storage | MinIO (S3) | State storage |
| Auth | Keycloak / DEX | SSO Integration |

## AI Agent Guidance

1. The `terrakube-executor` needs access to `/var/run/docker.sock` to spin up ephemeral Terraform containers.
2. All secrets for Terraform providers should be managed within Terrakube Workspaces.
3. Monitor the `actuator/health` endpoint for API/Executor drift.
