# Communication (10-communication)

## Overview

Communication-related services. Currently this directory hosts **MailHog** for development/testing and an inactive Stalwart blueprint.

## Services

| Service | Profile | Path     | Notes                     |
| ------- | ------- | -------- | ------------------------- |
| MailHog | `mail`  | `./mail` | SMTP test server + web UI |

## Run

```bash
docker compose --profile mail up -d mailhog
```

## File Map

| Path        | Description                                  |
| ----------- | -------------------------------------------- |
| `mail/`     | MailHog stack and commented Stalwart config. |
| `README.md` | Category overview.                           |
