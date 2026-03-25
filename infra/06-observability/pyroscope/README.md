# Pyroscope

> Continuous profiling backend for aggregating performance profiles.

## Overview

Pyroscope is the profiling backend for the hy-home.docker ecosystem. It allows for aggregating and querying performance profiles (CPU, Memory, etc.) to identify bottlenecks in real-time.

## Structure

```text
pyroscope/
├── config/
│   └── pyroscope.yaml   # Master configuration file
└── README.md           # This file
```

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| Engine | grafana/pyroscope:1.18.1 | Profiling backend |
| Storage | Filesystem (local) | Profile persistence |
| Ingestion | Alloy | Profile forwarding |

## Configuration

- **Config File**: `config/pyroscope.yaml`.
- **Backend**: Local filesystem (configured to `${DEFAULT_OBSERVABILITY_DIR}/pyroscope`).
- **Multitenancy**: Disabled (single-tenant).
- **Self-profiling**: Disabled by default.

## Persistence

- **Data**: Persistent volume `pyroscope-data` (mounted to `/var/lib/pyroscope`).

## Operational Status

> [!NOTE]
> Alloy acts as the primary profile collector. Ensure Alloy is healthy to receive profiles from protected applications.

---

Copyright (c) 2026. Licensed under the MIT License.
