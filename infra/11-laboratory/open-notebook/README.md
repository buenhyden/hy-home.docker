# Laboratory Open Notebook

> Local knowledge notebook and SurrealDB-backed laboratory service.

## Overview

Open Notebook provides an admin/laboratory notebook UI for local knowledge workflows. The stack includes the `open_notebook` application and a local `surrealdb` data store, both connected to `infra_net` and exposed through the gateway profile when enabled.

## Audience

- **Operators**: Managing local laboratory services and data persistence.
- **Developers**: Testing notebook-driven AI or knowledge workflows.
- **AI Agents**: Discovering service boundaries, secrets, and validation paths.

## Scope

### In Scope

- Docker Compose definitions for `open_notebook` and `surrealdb`.
- Local persistent volumes under `${DEFAULT_MANAGEMENT_DIR}`.
- Gateway exposure through Traefik labels.
- Docker secret consumption for notebook and database credentials.

### Out of Scope

- Production notebook promotion policy.
- User content governance inside notebook data.
- External model provider credentials or private notebook exports.

## Structure

```text
open-notebook/
├── docker-compose.yml     # Open Notebook and SurrealDB service definitions
├── surrealdb/             # Custom SurrealDB image context
└── README.md              # This file
```

## How to Work

1. Validate static Compose configuration before running the service:
   `docker compose -f infra/11-laboratory/open-notebook/docker-compose.yml config`
2. Start only when the `admin` or `dev` profile is intentionally selected.
3. Keep floating image usage reviewed through `infra/image-tag-policy.exceptions.json`.
4. Keep credentials in Docker secrets and environment variables; do not commit plaintext values.

## Service Configuration

| Component | Image / Source | Purpose |
| --- | --- | --- |
| `open_notebook` | `lfnovo/open_notebook:v1-latest-single` | Notebook UI and API runtime |
| `surrealdb` | `./surrealdb/Dockerfile` | Local metadata and notebook persistence |

## Related Documentation

- [Laboratory guides](../../../docs/07.guides/11-laboratory/README.md)
- [Laboratory operations](../../../docs/08.operations/11-laboratory/README.md)
- [Laboratory runbooks](../../../docs/09.runbooks/11-laboratory/README.md)
- [Image tag exceptions](../../image-tag-policy.exceptions.json)

---

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
