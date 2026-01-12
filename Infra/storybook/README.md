# Design System Storybook

## Overview

A UI component explorer for the Design System, built with Storybook (React).

## Services

- **storybook**: Storybook server.
  - Internal Port: 80
  - URL: `https://design.${DEFAULT_URL}`

## Configuration

### Environment Variables

- `DEFAULT_URL`: Domain handling.

## Networks

- `infra_net`

## Traefik Routing

- **Domain**: `design.${DEFAULT_URL}`
- **Auth**: Protected by SSO (Keycloak).
