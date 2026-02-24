# PostgreSQL Router (HAProxy) Operational Guide

> **Component**: `pg-router`
> **Internal Traffic Entry**: `pg-router`
> **Stateless Node**: 1

## 1. Load Balancing Strategy

The router uses `HAProxy` to distribute traffic across the Patroni cluster. It identifies node health using the Patroni REST API (`8008`).

- **Write Operations**: Routed to the current cluster Leader on port `5000`.
- **Read Operations**: Round-robined across healthy Replicas on port `5001`.

## 2. Global DB Connection (Mng-PG)

For management databases (Keycloak, SSO, n8n) not part of the HA cluster:

- **Host**: `mng-pg`
- **Port**: `5432`
- **Auth**: Docker Secret `@postgres_password`

## 3. High-Traffic Tuning

If connection bottlenecks occur at the router layer, adjust the `maxconn` settings in the HAProxy configuration file mounted at `/usr/local/etc/haproxy/haproxy.cfg`.

## 4. UI Stats

Access the real-time load balancer statistics dashboard:

- **URL**: `https://pg-haproxy.${DEFAULT_URL}`
