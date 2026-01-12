# Nginx / Proxy Manager

## Overview

A lightweight Nginx service acting as a reverse proxy or static file server.

## Services

- **nginx**: Nginx Web Server.
  - Ports: 80, 443

## Configuration

### Volumes

- `./config/nginx.conf`: Nginx configuration.
- `./certs`: SSL Certificates.

## Networks

- `infra_net`
  - IP: `172.19.0.13`
