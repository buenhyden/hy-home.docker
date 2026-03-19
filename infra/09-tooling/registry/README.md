# Registry

A private Docker container image registry based on [Docker Distribution](https://distribution.github.io/distribution/) (formerly Docker Registry v2). Used to store and serve locally-built custom images (e.g., `hy/loki`, `hy/tempo`).

## Services

| Service    | Image        | Role                        | Resources               |
| :---       | :---         | :---                        | :---                    |
| `registry` | `registry:2` | Container image registry    | med (0.5 CPU / 512 MB) |

## Networking

- **Access Port**: `${REGISTRY_PORT:-5000}` exposed directly on the host (no Traefik proxy).
- **Protocol**: Plain HTTP (no TLS). Add `localhost:${REGISTRY_PORT}` to Docker daemon `insecure-registries` for local use.

## Persistence

- **Images Volume**: `registry-data-volume` → `${DEFAULT_REGISTRY_DIR}` bind mount, stored at `/var/lib/registry` in container.

## Configuration

Key environment variables (from `.env`):

| Variable             | Default | Description                          |
| :---                 | :---    | :---                                 |
| `REGISTRY_PORT`      | `5000`  | Host and container port.             |
| `DEFAULT_REGISTRY_DIR` | —     | Host path for image storage.         |

## Usage

```bash
# Tag and push an image
docker tag my-image:latest localhost:${REGISTRY_PORT:-5000}/my-image:latest
docker push localhost:${REGISTRY_PORT:-5000}/my-image:latest

# List repositories via API
curl http://localhost:${REGISTRY_PORT:-5000}/v2/_catalog

# Reference from other containers (within infra_net)
image: registry:${REGISTRY_PORT:-5000}/my-image:latest
```

## File Map

| Path                | Description                                    |
| ------------------- | ---------------------------------------------- |
| `docker-compose.yml`| Service definition with volume and healthcheck.|
| `README.md`         | Service overview (this file).                  |
