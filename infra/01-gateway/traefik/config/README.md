# Traefik Static Configuration

This directory contains the static configuration for Traefik.

- `traefik.yml`: Main static configuration.
  - Configures `web` (80) and `websecure` (443) entrypoints.
  - Enables Docker provider for label-based routing.
  - Enables File provider for dynamic configuration (in `../dynamic`).
  - **Observability**: Configures Prometheus metrics and OTLP tracing (Tempo).
