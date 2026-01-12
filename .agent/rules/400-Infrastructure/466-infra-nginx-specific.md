---
trigger: always_on
glob: "nginx.conf,**/nginx/**/*.conf"
description: "Nginx: Configuration, Reverse Proxy, SSL, and Performance."
---
# Nginx Standards

## 1. Configuration Structure

- **Modular**: Split config into `sites-available/`, `conf.d/`.
- **Include**: Use `include` for shared snippets (SSL, headers).

### Example: Structure

**Good**

```nginx
http {
    include /etc/nginx/mime.types;
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

## 2. Reverse Proxy

- **proxy_pass**: Use for upstream services.
- **Headers**: Forward `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`.

### Example: Proxy

**Good**

```nginx
location /api/ {
    proxy_pass http://backend:8080/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**Bad**

```nginx
location /api/ {
    proxy_pass http://localhost:8080;  # No headers, broken client IP
}
```

## 3. SSL/TLS

- **TLS 1.2+**: Disable TLS 1.0/1.1. Use strong ciphers.
- **HSTS**: Enable `Strict-Transport-Security` header.
- **Certificates**: Use Let's Encrypt with auto-renewal.

### Example: SSL

**Good**

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

## 4. Performance

- **Gzip**: Enable `gzip` for text content.
- **Caching**: Set `Cache-Control` headers for static assets.
- **Buffers**: Tune `proxy_buffer_size` for large responses.
