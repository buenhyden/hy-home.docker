# Portainer

> Docker environment management and container orchestration UI.

## Overview

Portainer는 Docker 호스트와 컨테이너 리소스를 웹 인터페이스를 통해 관리할 수 있게 해주는 도구다. `/var/run/docker.sock`에 접근하여 실시간 모니터링 및 관리를 수행한다.

## Implementation Details

| Category   | Technology | Notes |
| ---------- | ---------- | ----- |
| Image      | portainer/portainer-ce:sts | Latest Short Term Support version |
| Port       | 9443 (Internal) | Exposed via Traefik |
| Storage    | ${DEFAULT_MANAGEMENT_DIR}/portainer | Persistent data for users/configs |

## Configuration

### Labels & Traefik

- **Rule**: `portainer.${DEFAULT_URL}`
- **Auth**: `sso-auth@file` 미들웨어 적용 필수.
- **TLS**: Enabled.

## Related References

- **Runbook**: [Resetting Portainer Admin](../../../docs/09.runbooks/11-laboratory/README.md#resetting-portainer-admin)
- **Official Docs**: [Portainer Documentation](https://docs.portainer.io/)
