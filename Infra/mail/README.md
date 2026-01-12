# Mail Server / MailHog

## Overview

Currently configured to run **MailHog**, an email testing tool for developers.

> **Note**: A configuration for **Stalwart Mail Server** is present but commented out in the `docker-compose.yml`.

## Service Details

### MailHog (`mailhog`)

- **Image**: `mailhog/mailhog`
- **Purpose**: Catching emails sent by applications during development.
- **Network**: `infra_net`

## Traefik Configuration

- **Domain**: `mail.${DEFAULT_URL}`
- **Port**: `${MAILHOG_UI_PORT}`
- **Entrypoint**: `websecure`
- **TLS**: Enabled
- **Middleware**: `sso-auth` (Protected access)
