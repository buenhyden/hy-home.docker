---
trigger: always_on
glob: "**/*.{py,js,ts,go,java}"
description: "SSRF Prevention (OWASP A10): URL validation, allowlisting, and network protection."
---
# SSRF Prevention Standards (OWASP A10)

## 1. URL Validation

- **Allowlisting**: Validate user-supplied URLs against a strict allowlist of domains/protocols (`https` only).
- **Parsing**: Use standard URL parsing libraries to canonicalize the URL before checking.

## 2. Network Protection

- **Internal Networks**: BLOCK access to private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`, `169.254.169.254`).
- **DNS Resolution**: Resolve the hostname to an IP address and check if it is private BEFORE making the connection (Time-of-Check to Time-of-Use mitigation).

## 3. Libraries

- **Wrappers**: Use a centralized HTTP client wrapper that enforces these checks automatically.
- **Redirects**: Disable automatic redirects (`allow_redirects=False`) or validate the redirect URL.

### Example: SSRF Check (Python)

```python
import ipaddress
import socket
from urllib.parse import urlparse

def is_safe_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False
    
    hostname = parsed.hostname
    try:
        # Resolve to IP
        ip = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip)
        # Check against private properties
        return not (ip_obj.is_private or ip_obj.is_loopback)
    except:
        return False
```
