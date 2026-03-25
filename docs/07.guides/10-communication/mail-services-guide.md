# Mail Services Guide

Manual for managing and using mail services in `hy-home.docker`.

## 1. Development (MailHog)

All non-production services should point their SMTP settings to MailHog to prevent accidental email leakage to external addresses.

- **Host**: `mailhog`
- **Port**: `1025`
- **Encryption**: None
- **Web UI**: `https://mailhog.${DEFAULT_URL}`

### Capturing Emails

Navigate to the Web UI to view, delete, or download messages captured by the trap. Messages are stored in memory and are discarded when the container restarts.

## 2. Production (Stalwart)

Stalwart provides production-ready SMTP and IMAP services.

- **Admin UI**: `https://mail.${DEFAULT_URL}`
- **Username**: `admin`
- **Password**: Managed via `stalwart_password` secret.

### Client Configuration

| Setting | Value |
| :--- | :--- |
| **IMAP Server** | `mail.${DEFAULT_URL}` |
| **IMAP Port** | `993` (SSL/TLS) |
| **SMTP Server** | `mail.${DEFAULT_URL}` |
| **SMTP Port** | `465` (SSL/TLS) or `587` (STARTTLS) |

## 3. Security Notes

- Stalwart relies on certificates located in `secrets/certs`.
- Ensure DNS records (MX, SPF, DKIM, DMARC) are correctly configured at your provider if exposed to the internet.
