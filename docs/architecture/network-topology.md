# Network Topology

## Overview

All infrastructure services communicate via a dedicated Docker bridge network with static IP assignments for critical services.

## Network Configuration

### infra_net

**Primary infrastructure network**

- **Type**: Docker bridge network
- **Subnet**: `172.19.0.0/16`
- **Gateway**: `172.19.0.1`
- **IPAM Driver**: Default

### project_net

**External network for application projects**

- **Type**: External Docker network
- **Purpose**: Connect application containers to infrastructure services

### kind

**External network for Kubernetes (KIND) integration**

- **Type**: External Docker network
- **Purpose**: KIND cluster connectivity

## Static IP Assignments

Services with static IPs for stable internal communication:

### Service Groups

Services are assigned static IPs in logical blocks within the `172.19.0.0/16` subnet to facilitate management and firewall rules.

| IP Block | Service Group | Services |
| :--- | :--- | :--- |
| `172.19.0.10-19` | **Core Infrastructure** | Keycloak (`.10`), MinIO (`.12`), Traefik (`.13`), OAuth2 Proxy (`.14`), MailHog (`.15`) |
| `172.19.0.20-29` | **Kafka Cluster** | Brokers (`.20` - `.22`), Schema Registry (`.23`), Connect (`.24`), REST Proxy (`.25`), UI (`.26`), Exporter (`.27`) |
| `172.19.0.30-39` | **Observability** | Prometheus (`.30`), Loki (`.31`), Tempo (`.32`), Grafana (`.33`), Alloy (`.34`), cAdvisor (`.35`), Alertmanager (`.36`), Pushgateway (`.37`) |
| `172.19.0.40-49` | **AI & ML** | Ollama (`.40`), Qdrant (`.41`), Open WebUI (`.42`), Export (`.43`) |
| `172.19.0.50-59` | **PostgreSQL HA** | etcd (`.50` - `.52`), Postgres (`.53` - `.55`), HAProxy (`.56`), Exporters (`.57` - `.59`) |
| `172.19.0.60-69` | **Cache (Valkey/Redis)** | Nodes (`.60` - `.65`), Init (`.66`), Exporter (`.67`) |

> **Note**: Most services use Docker's automatic IP assignment within the subnet range.

## DNS Resolution

### Internal Resolution

Services are accessible via container names within the `infra_net`:

```text
kafka-1.infra_net
postgresql-haproxy.infra_net
grafana.infra_net
```

### External Resolution (via Traefik)

Services exposed via Traefik use wildcard DNS with `.nip.io`:

```text
https://grafana.127.0.0.1.nip.io
https://kafka-ui.127.0.0.1.nip.io
https://keycloak.127.0.0.1.nip.io
```

**Why `.nip.io`?**

- Provides automatic DNS resolution for local IPs
- `127.0.0.1.nip.io` resolves to `127.0.0.1`
- `*.127.0.0.1.nip.io` resolves to `127.0.0.1`
- No `/etc/hosts` modification required for development

## Traefik Routing

### Entrypoints

- **web**: Port `80` (HTTP) - Redirects to HTTPS
- **websecure**: Port `443` (HTTPS) - Main entry point
- **traefik**: Port `8080` - Traefik dashboard

### Routing Rules

Services are routed based on Host header matching:

```yaml
Host(`service-name.${DEFAULT_URL}`)
```

Where `${DEFAULT_URL}` defaults to `127.0.0.1.nip.io`.

### Middleware Chains

Common middleware applied:

- **sso-auth@file**: OAuth2 Proxy forward authentication
- **TLS**: Automatic HTTPS with self-signed certs or mkcert

## Port Mappings

### Exposed Ports (Host → Container)

| Service | Host Port | Container Port | Protocol | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| Traefik | `80` | `80` | HTTP | HTTP redirect |
| Traefik | `443` | `443` | HTTPS | Main entry |
| PostgreSQL (Write) | `5000` | `5000` | TCP | DB writes |
| PostgreSQL (Read) | `5001` | `5001` | TCP | DB reads |
| Valkey/Redis Cluster | `6379` | `6379` | TCP | Cache |
| Kafka Brokers | `9092-9094` | `9092` | TCP | Event streaming |
| InfluxDB | Via Traefik | `8086` | HTTP | Time-series DB |
| MinIO API | Via Traefik | `9000` | HTTP | S3 API |

### Internal Ports (Container-only)

Services accessible only within `infra_net`:

- Prometheus: `9090`
- Loki: `3100`
- Tempo: `3200`
- etcd: `2379`, `2380`
- Patroni: `8008`

## Security Considerations

1. **No Direct Exposure**: Only Traefik and database load balancers expose host ports
2. **TLS Everywhere**: All HTTP traffic via Traefik is HTTPS
3. **Network Isolation**: Services isolated in `infra_net`, applications in `project_net`
4. **Internal Communication**: Services communicate via container names (encrypted at Docker layer)

## Troubleshooting

### Port Conflicts

Check for conflicts:

```bash
# Windows
netstat -ano | findstr "5432"

# Linux/Mac
lsof -i :5432
```

### DNS Issues

If `.nip.io` fails, add to `/etc/hosts`:

```properties
127.0.0.1 grafana.127.0.0.1.nip.io
127.0.0.1 keycloak.127.0.0.1.nip.io
```

### Network Inspection

```bash
docker network inspect infra_net
docker network ls
```
