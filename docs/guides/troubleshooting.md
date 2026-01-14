# Troubleshooting Guide

## Common Issues

### 1. Port Conflicts

**Symptom**: Service fails to start with "port already allocated" error.

**Diagnosis**:

```bash
# Windows
netstat -ano | findstr "5432"
netstat -ano | findstr "6379"

# Linux/Mac
lsof -i :5432
lsof -i :6379
```

**Solution**:

1. Stop the conflicting service
2. Or change the port mapping in `docker compose.yml`

```yaml
ports:
  - "15432:5432"  # Use alternative host port
```

### 2. DNS Resolution Issues

**Symptom**: Cannot access services via `*.127.0.0.1.nip.io` domains.

**Diagnosis**:

```bash
nslookup grafana.127.0.0.1.nip.io
ping grafana.127.0.0.1.nip.io
```

**Solution A**: Manually add to hosts file

**Windows**: `C:\Windows\System32\drivers\etc\hosts`  
**Linux/Mac**: `/etc/hosts`

```
127.0.0.1 grafana.127.0.0.1.nip.io
127.0.0.1 keycloak.127.0.0.1.nip.io
127.0.0.1 kafka-ui.127.0.0.1.nip.io
127.0.0.1 n8n.127.0.0.1.nip.io
```

**Solution B**: Use localhost directly
Access via `https://localhost` and accept certificate warnings.

### 3. Volume Permission Issues

**Symptom**: Service crashes with "permission denied" on mounted volumes.

**Common on**: Linux, WSL2

**Diagnosis**:

```bash
docker compose logs <service-name>
```

Look for errors like:

```
Permission denied: /var/lib/postgresql/data
```

**Solution**:

```bash
# Stop services
docker compose down

# Option 1: Fix permissions (if using bind mounts)
sudo chown -R $USER:$USER ./data

# Option 2: Remove and recreate volumes (DESTRUCTIVE)
docker volume prune
docker compose up -d
```

### 4. Container Health Check Failing

**Symptom**: Container stuck in "starting" or "unhealthy" state.

**Diagnosis**:

```bash
docker inspect <container-name> | grep -A 10 Health
docker logs <container-name> --tail 100
```

**Common Causes**:

- Service not ready (wait longer)
- Dependency not available
- Configuration error

**Solution**:

```bash
# Check dependency services first
docker compose ps

# Restart the service
docker compose restart <service-name>

# If persistent, check logs
docker compose logs -f <service-name>
```

### 5. Out of Memory (OOM)

**Symptom**: Services randomly crash, Docker becomes unresponsive.

**Diagnosis**:

```bash
docker stats
```

**Solution**:

- Increase Docker Desktop memory limit (Settings ??Resources)
- Reduce running services
- Add resource limits to `docker compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 2G
```

### 6. Network Connectivity Between Services

**Symptom**: Service cannot connect to another service.

**Diagnosis**:

```bash
# Check networks
docker network ls
docker network inspect infra_net

# Test from inside container
docker exec -it <container> ping <other-service-name>
docker exec -it <container> curl http://<other-service>:port
```

**Solution**:
Ensure both services are on the same network:

```yaml
networks:
  - infra_net
```

### 7. SSL/TLS Certificate Errors

**Symptom**: Browser shows "Your connection is not private" or CURL fails with SSL errors.

**For Development (mkcert)**:

```bash
# Install mkcert root CA
mkcert -install

# Regenerate certificates
cd certs
mkcert -key-file local-key.pem -cert-file local-cert.pem \
  "localhost" "127.0.0.1" "*.127.0.0.1.nip.io"
```

**For Production**:
Use Let's Encrypt with Traefik's ACME resolver.

### 8. Image Pull Failures

**Symptom**: `docker compose pull` fails or times out.

**Common Causes**:

- Docker Hub rate limiting
- Network issues
- Invalid image tag

**Solution**:

```bash
# Check rate limit
curl https://auth.docker.io/token\?service\=registry.docker.io\&scope\=repository:ratelimitpreview/test:pull

# Use authenticated pull
docker login

# Or use mirror/cache
```

## Service-Specific Issues

### PostgreSQL Cluster

**Issue**: Patroni shows "no leader" or split-brain

**Solution**:

```bash
# Check cluster status
docker exec -it etcd1 etcdctl member list
docker exec -it patroni1 patronictl -c /etc/patroni.yml list

# Force reinitialize (DESTRUCTIVE)
docker compose down
docker volume rm postgres-data-*
docker compose up -d
```

### Kafka

**Issue**: Broker not starting, controller election failing

**Diagnosis**:

```bash
docker logs kafka-1 --tail 100
```

**Solution**:

- Ensure all 3 brokers are running
- Check `KAFKA_CFG_PROCESS_ROLES` includes both `broker,controller`
- Verify cluster ID consistency

### Keycloak

**Issue**: Database migration failing

**Solution**:

```bash
# Check mng-pg is healthy
docker compose ps mng-pg

# Force reinitialize Keycloak
docker compose down keycloak
docker volume rm keycloak-data
docker compose up -d keycloak
```

## Debugging Tools

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker logs <container-name> -f --tail=100

# Search logs
docker logs <container-name> 2>&1 | grep ERROR
```

### Shell Access

```bash
# Get shell in running container
docker exec -it <container-name> /bin/bash
docker exec -it <container-name> /bin/sh

# Check processes
docker exec <container-name> ps aux
```

### Network Debugging

```bash
# Inspect network
docker network inspect infra_net

# Test connectivity
docker run --rm --network infra_net nicolaka/netshoot \
  curl http://service-name:port
```

### Resource Usage

```bash
# Live stats
docker stats

# Detailed info
docker system df
docker system info
```

## Complete Reset (Nuclear Option)

**Warning**: This deletes **ALL data**.

```bash
# Stop everything
cd infra
docker compose down -v

# Remove all containers, networks, volumes
docker system prune -a --volumes

# Restart
docker compose up -d
```

## Getting Help

1. Check service-specific README: `infra/<service>/README.md`
2. View logs: `docker compose logs <service>`
3. Check [GitHub Issues](https://github.com/your-repo/issues)
4. Consult official documentation for each service

## See Also

- [Deployment Guide](./deployment-guide.md)
- [Network Topology](../architecture/network-topology.md)
- [Security Guide](./security.md)
