<!-- [ID:09-tooling:registry] -->
# Docker Registry

> Private OCI-compliant image distribution service.

## 1. Overview (KR)

이 서비스는 컨테이너 이미지를 내부 네트워크에서 관리하고 배포하는 **프라이빗 도커 레지스트리**입니다. 외부 네트워크 의존성을 줄이고 보안이 강화된 이미지 저장소로 활용됩니다.

## 2. Overview

The `registry` service acts as the internal repository for container images in `hy-home.docker`. It enables fast, local pulls for internal infrastructure and avoids dependency on external public registries for proprietary or sensitive images.

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **registry** | Registry v2 | Image Distribution |

## 4. Networking

| Service | Port | Description |
| :--- | :--- | :--- |
| **Registry Port** | `5000` | Standard distribution port (via `REGISTRY_PORT`). |
| **Protocol** | Plain HTTP | Add to `insecure-registries` in Docker daemon. |

## 5. Persistence

- **Images Volume**: `registry-data-volume` mapped to `/var/lib/registry`.
- **Host Path**: `${DEFAULT_REGISTRY_DIR}`.

## 6. File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Registry service definition. |
| `README.md` | Service overview (this file). |

---

## Documentation References

- [DevOps Tooling Guide](../../../docs/07.guides/09-tooling/README.md)
- [Tooling Operations](../../../docs/08.operations/09-tooling/README.md)
