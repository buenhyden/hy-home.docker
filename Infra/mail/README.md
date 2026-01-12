# Mail Server Infrastructure

## Overview

This directory contains configurations for mail services. Currently, **MailHog** is the active service used for development and testing. A configuration for **Stalwart Mail Server** (an all-in-one production solution) is also present but currently inactive.

## Active Service: MailHog

MailHog is an email testing tool for developers that catches all emails sent to it and displays them in a web UI.

### Service Details

- **Service Name**: `mailhog`
- **Image**: `mailhog/mailhog`
- **Internal SMTP Port**: `1025` (Use this port in your applications)
- **Web UI Port**: `${MAILHOG_UI_PORT}` (Exposed via Traefik)
- **Network**: `infra_net`

### Traefik Configuration

The Web UI is exposed with security enabled:

- **Domain**: `mail.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS Enabled)
- **Authentication**: **SSO Enabled** (via `sso-auth` middleware)

## Inactive Service: Stalwart

> **Note**: The `docker-compose.yml` contains a fully commented-out configuration for **Stalwart Mail Server**, intended for future production use.

### Stalwart Features (Planned)

- **Protocols**: SMTP, SMTPS, IMAPS, ManageSieve.
- **Port Mappings**:
  - `25`: SMTP (Relay)
  - `587`: Submission (StartTLS)
  - `465`: SMTPS (Implicit TLS)
  - `993`: IMAPS
  - `4190`: ManageSieve
  - `8080`: Web Admin UI
- **Storage**: Persistent volume `stalwart-data`.

- **Storage**: Persistent volume `stalwart-data`.

## Environment Variables

**Active Service (MailHog)**:
MailHog is configured primarily via command flags and does not require complex environment variables for this setup.

**Inactive Service (Stalwart)**:
See `docker-compose.yml` comments for `STALWART_ADMIN_USER` and `STALWART_ADMIN_PASSWORD` usage if enabling.

## Usage

### Configuring Applications (Internal)

To send emails from other services within the `infra_net` network:

- **Host**: `mailhog`
- **Port**: `1025`
- **Auth**: None (MailHog accepts everything)

### Accessing Web UI

- **URL**: `https://mail.<your-domain>`
- **Login**: Authenticate via your SSO provider.
