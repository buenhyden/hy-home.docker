---
layer: infra
---

# Nginx Secondary Proxy

Nginx serves as a secondary gateway in the `hy-home.docker` ecosystem, providing specialized path-based routing, static file serving, and legacy proxy configurations.

## Role & Usage

While Traefik is the primary dynamic router, Nginx is used when:
- Complex path-based routing or rewrites are required.
- Serving static assets directly from the filesystem.
- Specialized proxy buffers or timeout configurations are needed.

## Configuration

- **Main Config** ([`./config/nginx.conf`](./config/nginx.conf)): The primary configuration file, mounted to `/etc/nginx/nginx.conf`.
- **Certificates**: Mounted from `../../../../secrets/certs/` to `/etc/nginx/certs/`.

## SSO & Identity Integration

Nginx integrates with `02-auth` (OAuth2 Proxy) using the `auth_request` module. This allows Nginx to verify user sessions before forwarding traffic to backend services.

### Auth Request Pattern

```nginx
location /protected/ {
    auth_request /_oauth2_auth_check;
    error_page 401 = /oauth2/sign_in;
    
    # Pass user headers to backend
    auth_request_set $user   $upstream_http_x_auth_request_user;
    auth_request_set $email  $upstream_http_x_auth_request_email;
    proxy_set_header X-User  $user;
    proxy_set_header X-Email $email;
}
```

## Operations

### Lifecycle Commands

- **Start**: `docker compose up -d nginx`
- **Stop**: `docker compose stop nginx`
- **Restart**: `docker compose restart nginx`

### Maintenance

- **Validate Configuration**: `docker exec nginx nginx -t`
- **Hot Reload**: `docker exec nginx nginx -s reload` (Reloads configuration without dropped connections)
- **Check Logs**: `docker compose logs -f nginx`

## Dependencies

- **Secrets**: Requires valid TLS certificates in `secrets/certs/`.
- **Auth Tier**: Depends on `02-auth` (OAuth2 Proxy) for `auth_request` verification.
