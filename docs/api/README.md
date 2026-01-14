# API Reference

## Overview

This directory contains API specifications and reference documentation for the services deployed in `hy-home.docker`.

## Hosted API Documentation

Most services allow access to their API documentation directly via their deployed URL:

- **Traefik**: <https://dashboard.127.0.0.1.nip.io/api> (Raw API)
- **Keycloak**: <https://keycloak.127.0.0.1.nip.io/js/doc/index.html> (Admin REST API)
- **Grafana**: <https://grafana.127.0.0.1.nip.io/docs/http_api/index.html>
- **Ollama**: `localhost:11434/api/tags` (See [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md))
- **n8n**: <https://n8n.127.0.0.1.nip.io/api/v1/docs/>

## Specs

Place any custom OpenAPI (`.yaml` / `.json`) specifications in this folder.

- `examples/` - Example payloads
- `schemas/` - JSON schemas
