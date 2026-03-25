# Pyroscope Continuous Profiling

> Continuous profiling platform for analyzing application performance.

## Overview

Pyroscope provides continuous profiling of applications to identify performance bottlenecks and resource leaks. It collects profiling data (CPU, memory, etc.) and allows developers to visualize it over time.

## Audience

- Developers (Code optimization)
- SREs (Resource leak hunting)

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Profiling | Pyroscope | v1.18.1 |

## Configuration

- **Inspiration**: Alloy collects profiling data and sends it to Pyroscope.
- **Persistence**: Local storage with S3-compatible backend support.

## AI Agent Guidance

1. Use `Flame Graphs` to identify hot code paths.
2. Monitor `Pyroscope` resource usage as profiling can be CPU-intensive.
