# Mail Services

## Overview

Mail infrastructure including MailHog for testing and Stalwart for production.

## Services

- **mailhog**: Web-based SMTP testing tool.
  - UI URL: `https://mail.${DEFAULT_URL}`
  - SMTP Port: `1025` (Internal)
  - HTTP Port: `8025` (Internal)

## Configuration

### Environment Variables

- `STALWART_ADMIN_USER`: Admin user (for Stalwart, commented out by default).
- `STALWART_ADMIN_PASSWORD`: Admin password.

### Volumes

- `stalwart-data`: `/opt/stalwart` (for Stalwart)

## Networks

- `infra_net`

## Traefik Routing

- **Domain**: `mail.${DEFAULT_URL}`
- **SSO**: Recommended for Stalwart UI.
