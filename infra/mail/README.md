# Mail Server Infrastructure

## Overview

This directory contains configurations for mail services. Currently, **MailHog** is the active service used for development and testing. A configuration for **Stalwart Mail Server** (an all-in-one production solution) is also present but currently inactive.

## Services

### Active: MailHog

- **Service Name**: `mailhog`
- **Image**: `mailhog/mailhog:v1.0.1`
- **Role**: Email testing tool for developers
- **Internal SMTP Port**: `1025`
- **Web UI Port**: `${MAILHOG_UI_PORT}`

### Inactive: Stalwart

> **Note**: A fully commented-out configuration for **Stalwart Mail Server** exists in `docker-compose.yml` for future production use.

- **Role**: All-in-one Mail Server (SMTP, IMAP, JMAP)
- **Features**: Protocols (SMTP, SMTPS, IMAPS), ManageSieve, Web Admin UI.
- **Persistence**: Uses `stalwart-data` volume and `./certs` directory.

## Networking

- **Network**: `infra_net`
- **MailHog Internal Host**: `mailhog`
- **MailHog Internal Port**: `1025` (No auth required)

## Configuration

### MailHog

MailHog is configured primarily via command flags and does not require complex environment variables for this setup.

### Stalwart (Inactive)

Check `docker-compose.yml` comments for:

- `STALWART_ADMIN_USER`
- `STALWART_ADMIN_PASSWORD`

## Traefik Integration

The Web UI for MailHog is exposed with security enabled:

- **Domain**: `mail.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS Enabled)
- **Service Port**: `${MAILHOG_UI_PORT}`
- **Authentication**: **SSO Enabled** (via `sso-auth` middleware)

## Usage

### Configuring Applications (Internal)

To send emails from other services within the `infra_net` network:

- **Host**: `mailhog`
- **Port**: `1025`
- **Auth**: None (MailHog accepts everything)

### Accessing Web UI

- **URL**: `https://mail.<your-domain>`
- **Login**: Authenticate via your SSO provider.
