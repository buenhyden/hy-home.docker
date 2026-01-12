# Maintenance Guide

## Regular Updates

### Updating Container Images

**Check for updates**:

```bash
cd infra
docker-compose pull
```

**Apply updates**:

```bash
docker-compose up -d
```

Docker Compose automatically recreates containers if image has changed.

**Cleanup old images**:

```bash
docker image prune -f
```

### Automated Updates (Watchtower)

**Setup** (optional, not included by default):

```yaml
services:
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 86400 --cleanup
```

Checks for updates daily and automatically updates containers.

## Backup Procedures

### PostgreSQL Backups

**Manual backup**:

```bash
# Full dump
docker exec postgresql-haproxy pg_dumpall -U postgres > backup_$(date +%Y%m%d).sql

# Specific database
docker exec postgresql-haproxy pg_dump -U postgres mydb > mydb_backup.sql
```

**Automated backup script** (`scripts/backup-postgres.sh`):

```bash
#!/bin/bash
BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)

docker exec postgresql-haproxy pg_dumpall -U postgres | \
  gzip > "$BACKUP_DIR/full_backup_$DATE.sql.gz"

# Keep last 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
```

**Restore**:

```bash
gunzip < backup.sql.gz | docker exec -i postgresql-haproxy psql -U postgres
```

### Redis Backups

**Redis uses RDB snapshots**:

```bash
# Trigger save
docker exec redis-cluster-node-1 redis-cli -a $(cat ../secrets/redis_password.txt) SAVE

# Copy RDB file
docker cp redis-cluster-node-1:/data/dump.rdb ./backups/redis/
```

### MinIO Backups

**Using MinIO Client (mc)**:

```bash
# Setup alias
docker run --rm --network infra_net minio/mc alias set myminio \
  http://minio:9000 \
  $(cat secrets/minio_root_user.txt) \
  $(cat secrets/minio_root_password.txt)

# Backup bucket
docker run --rm --network infra_net -v $(pwd)/backups:/backups minio/mc \
  mirror myminio/mybucket /backups/mybucket
```

### Volume Backups

**Backup named volumes**:

```bash
# Create tarball of volume
docker run --rm -v grafana-data:/data -v $(pwd)/backups:/backup \
  alpine tar czf /backup/grafana-data.tar.gz -C /data .
```

**Restore volume**:

```bash
docker run --rm -v grafana-data:/data -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/grafana-data.tar.gz -C /data
```

## Monitoring

### Resource Usage

**Check container stats**:

```bash
docker stats
```

**Check disk usage**:

```bash
docker system df
```

**Volume sizes**:

```bash
docker system df -v
```

### Log Management

**View log size**:

```bash
docker inspect -f '{{.LogPath}}' <container-name>
ls -lh $(docker inspect -f '{{.LogPath}}' <container-name>)
```

**Configure log rotation** in `docker-compose.yml`:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

**Clear logs** (DESTRUCTIVE):

```bash
truncate -s 0 $(docker inspect -f '{{.LogPath}}' <container-name>)
```

### Health Monitoring

**Check service health**:

```bash
docker-compose ps
```

Look for `Up (healthy)` status.

**Automated health checks** via Grafana:

- CPU/Memory usage alerts
- Disk space alerts
- Service up/down alerts

## Maintenance Windows

### Rolling Updates (Zero Downtime)

**For clustered services** (PostgreSQL, Redis, Kafka):

1. Update one node at a time
2. Wait for cluster to rebalance
3. Proceed to next node

**PostgreSQL HA**:

```bash
# Update replica first
docker-compose stop patroni2
docker-compose pull patroni2
docker-compose start patroni2

# Wait for sync
docker exec patroni1 patronictl list

# Repeat for patroni3, then patroni1 (leader)
```

### Scheduled Maintenance Tasks

**Weekly**:

- Update images: `docker-compose pull`
- Review logs for errors
- Check backup success

**Monthly**:

- Clean old images: `docker image prune -a`
- Clean unused volumes: `docker volume prune` (CAREFUL!)
- Review resource usage trends
- Update dependencies

**Quarterly**:

- Full backup test (restore to test environment)
- Security audit
- Review and update access controls in Keycloak

## Disaster Recovery

### Recovery Plan

1. **Restore from backups**
2. **Recreate secrets**
3. **Deploy infrastructure**: `docker-compose up -d`
4. **Restore data**:
   - PostgreSQL dumps
   - Redis RDB files
   - MinIO buckets
   - Volume tarballs
5. **Verify services**
6. **Update DNS/networking**

### Test Recovery Annually

**Run in test environment**:

```bash
# Restore backups
# Deploy fresh infrastructure
# Import data
# Validate functionality
```

Document time to recovery (RTO) and data loss tolerance (RPO).

## Performance Optimization

### Database Optimization

**PostgreSQL**:

```bash
# Vacuum and analyze
docker exec patroni1 psql -U postgres -c "VACUUM ANALYZE;"

# Reindex
docker exec patroni1 psql -U postgres -c "REINDEX DATABASE mydb;"
```

**Redis**:

```bash
# Memory usage
docker exec redis-cluster-node-1 redis-cli INFO memory

# Eviction policy (if using as cache)
docker exec redis-cluster-node-1 redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Container Resource Tuning

Monitor with `docker stats`, then adjust:

```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 8G
    reservations:
      memory: 4G
```

## Deprecated Services Cleanup

**Remove unused services**:

```bash
# Stop and remove
cd infra/old-service
docker-compose down -v

# Remove from include list in main docker-compose.yml
```

## See Also

- [Deployment Guide](./deployment-guide.md)
- [Troubleshooting Guide](./troubleshooting.md)
- [Security Guide](./security.md)
