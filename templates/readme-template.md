# README Template (Universal & Modular)

> Use this template to create `README.md` files for any directory. 
> 1. Select the **Core Section**.
> 2. Pick the appropriate **Snippet(s)** for your folder type.
> 3. Fill in the placeholders (e.g., `{Name}`).

---

# {Folder or Project Name}

> One-line catchy description of this specific component.

## Overview

**KR**: {이 폴더/프로젝트의 목적과 해결하려는 문제를 간략하게 설명하세요.}
**EN**: {Briefly describe the purpose of this folder/project and the problem it solves.}

## Navigation / Inventory

| Component | Path | Purpose |
| :--- | :--- | :--- |
| {Item 1} | `{path/to/file}` | {Quick description} |
| {Item 2} | `{path/to/dir/}` | {Quick description} |

---

<!-- [SNIPPET: ROOT ONLY] -->
## 🚀 Quick Start (Root Project)

### 1. Prerequisites
- Node.js >= 20.x
- Docker >= 24.x
- {Other Tool} >= {Version}

### 2. Setup & Run
```bash
git clone {URL}
cd {Project}
cp .env.example .env
npm install
npm run dev
```

### 3. Tech Stack
| Category | Technology |
| :--- | :--- |
| Runtime | Node.js |
| Database | PostgreSQL |
| Ops | Docker Compose |
<!-- [/SNIPPET] -->

---

<!-- [SNIPPET: DOCS ONLY] -->
## 📚 Documentation Hub

### Navigation Map
| Marker | Entry Point | Use when |
| :--- | :--- | :--- |
| `[LOAD:INDEX]` | [README.md](README.md) | Initial orientation |
| `[LOAD:SPEC]` | [specs/](specs/) | Checking API/Design specs |

### Key Resources
- [Architecture Principles](/ARCHITECTURE.md)
- [Operator Guide](/docs/guides/)
<!-- [/SNIPPET] -->

---

<!-- [SNIPPET: INFRA & COMPONENT ONLY] -->
## ⚙️ Infrastructure / Component Details

### Services & Resources
| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `{name}` | `{image:tag}` | `{primary/replica}` | `{CPU/RAM}` |

### Networking
| Port (Int) | Port (Host) | Protocol | Purpose |
| :--- | :--- | :--- | :--- |
| `5432` | `${VAR_PORT}` | TCP | SQL Traffic |

### Operational Commands
```bash
# Check status
docker compose exec {service} {status-cmd}

# View logs
docker compose logs -f {service}
```
<!-- [/SNIPPET] -->

---

<!-- [SNIPPET: SCRIPTS ONLY] -->
## 🛠️ Utilities & Automation

### Standard Rules
- **Idempotency**: Scripts should be safe to run multiple times.
- **No Secrets**: Never hardcode credentials; use environment variables.

### Usage Examples
```bash
# Run bootstrap
./scripts/bootstrap.sh --force

# Validate config
./scripts/validate.sh
```
<!-- [/SNIPPET] -->

---

## Extensibility & References

- [🤖 Agent Governance](/AGENTS.md)
- [🏛️ System Architecture](/ARCHITECTURE.md)
- [⚙️ Operations](/OPERATION.md)

---
*Maintained by {Team/Role}*
