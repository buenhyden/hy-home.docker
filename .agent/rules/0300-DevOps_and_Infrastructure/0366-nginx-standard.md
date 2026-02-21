---
trigger: always
glob: ["nginx.conf", "**/nginx/**/*.conf"]
description: "Nginx Standards: Enforces modular configuration, secure SSL/TLS defaults, and optimized reverse proxy patterns."
---

# Nginx Development Standards

- **Role**: Web Server & Load Balancing Architect
- **Purpose**: Define standards for configuring high-performance, secure, and maintainable Nginx instances for reverse proxying, SSL termination, and static asset delivery.
- **Activates When**: Modifying Nginx configuration files, configuring SSL certificates, or designing load balancing architectures.

**Trigger**: always — Apply during the design and maintenance of all Nginx-based infrastructure.

## 1. Standards

### Principles

- **[REQ-NGX-01] Modular Configuration Architecture**
  - Configurations MUST be organized into modular snippets (e.g., `conf.d/`, `sites-enabled/`). Monolithic `nginx.conf` files are PROHIBITED for non-trivial setups.
- **[REQ-NGX-02] Secure-by-Default TLS**
  - All public-facing instances MUST utilize TLS 1.2 or 1.3 with strong cipher suites. HSTS MUST be enabled to enforce encrypted transport.
- **[REQ-NGX-03] Transparent Proxy Forwarding**
  - Reverse proxy configurations MUST correctly forward client identification headers (`X-Real-IP`, `X-Forwarded-For`) to upstream services.

### Configuration Baseline

| Category | Requirement ID | Mandatory Directive / Value |
| --- | --- | --- |
| Security | [REQ-NGX-04] | `server_tokens off;` (Hide version) |
| SSL | [REQ-NGX-05] | `ssl_protocols TLSv1.2 TLSv1.3;` |
| Performance | [REQ-NGX-06] | `gzip on;` with appropriate types |
| Logging | [REQ-NGX-07] | Structured JSON access logs |

### Must

- **[REQ-NGX-08] Explicit Include Directives**
  - Utilize `include` statements for shared logic (e.g., `ssl.conf`, `proxy_params`) to minimize duplication across virtual host files.
- **[REQ-NGX-09] Mandatory Header Filtering**
  - Nginx MUST be configured to filter out unwanted or dangerous incoming headers before passing requests to the application layer.
- **[REQ-NGX-10] Resource-Aware Buffering**
  - Proxy buffer sizes MUST be explicitly tuned based on the expected response sizes to prevent premature disk swapping.

### Must Not

- **[BAN-NGX-01] Root Execution Hazard**
  - Nginx worker processes MUST NOT run with elevated privileges; utilize a dedicated, unprivileged user (e.g., `www-data`).
- **[BAN-NGX-02] Direct Public Access to Backends**
  - Backend application ports MUST NOT be exposed to the internet; all traffic MUST be routed through the Nginx perimeter.

### Failure Handling

- **Stop Condition**: Stop configuration deployment if `nginx -t` identifies a syntax error or if the SSL certificate identifies as expired.

## 2. Procedures

- **[PROC-NGX-01] Config Validation Flow**
  - IF modifying Nginx configuration THEN MUST run `nginx -t` in the target environment before reloading the service.
- **[PROC-NGX-02] Certificate Audit**
  - Weekly, monitor certificate expiration dates and verify that automated renewal mechanisms (e.g., Certbot) are operational.

## 3. Examples

### Secure Proxy Block (Good)

```nginx
location /api/ {
    proxy_pass http://backend_upstream/;
    include proxy_params; # Standardized headers
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 4. Validation Criteria

- **[VAL-NGX-01] SSL Lab Rating**
  - [ ] Public-facing endpoints achieve an "A+" or "A" rating on industry-standard SSL auditing tools.
- **[VAL-NGX-02] Config Consistency**
  - [ ] audit confirms that 100% of sites-enabled utilize the modular snippet architecture.
- **[VAL-NGX-03] Header Transparency**
  - [ ] Sample logs confirm that the backend accurately receives the end-user's real IP address.
