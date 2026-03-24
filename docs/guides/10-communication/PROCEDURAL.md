---
layer: infra
---

# Communication Tier: Maintenance & Procedures

This guide covers routine operations, upgrades, and troubleshooting for the mail stack.

## 1. Daily Operations

### Health Checks
```bash
# MailHog
docker inspect --format='{{.State.Health.Status}}' mailhog

# Stalwart
docker inspect --format='{{.State.Health.Status}}' stalwart
```

### Mail History Reset (MailHog)
```bash
docker restart mailhog
```

## 2. Troubleshooting

### Connection Failures
1. Verify `infra_net` connectivity:
   ```bash
   docker exec -it <consumer-container> nc -zv mailhog 1025
   ```
2. Check container logs:
   ```bash
   docker logs mailhog
   docker logs stalwart
   ```

### Stalwart Startup Issues
- Ensure `stalwart-data` volume permissions are correct.
- Verify `stalwart_password` secret is properly mounted.
