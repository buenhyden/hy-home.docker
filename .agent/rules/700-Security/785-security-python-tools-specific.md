---
trigger: always_on
glob: "**/*.py"
description: "Python Security Tools: Standards for developing cybersecurity utilities."
---
# Python Security Tools

## 1. Architecture

- **RORO Pattern**: Use "Receive Object, Return Object" for all tool interfaces.
- **Async**: Use `asyncio` for network-bound operations (scanning, requests).
- **Structure**:
  - `scanners/` (port, vulns)
  - `enumerators/` (DNS, SMB)
  - `attackers/` (brute-force)
  - `utils/` (crypto, net)

## 2. Libraries

- **Network**: `scapy` (packet crafting), `httpx`/`aiohttp` (async requests).
- **Scanning**: `python-nmap` or `libnmap`.
- **SSH**: `asyncssh` or `paramiko`.
- **Crypto**: `cryptography` library (not `pycrypto`).

## 3. Safety & Style

- **Rate Limiting**: Implement back-off to prevent DOS.
- **Input Sanitization**: NEVER pass unsanitized input to shell.
- **Type Hints**: Mandatory for all signatures.

### Example: Scanner Pattern

#### Good

```python
async def scan_target(target: TargetConfig) -> ScanResult:
    # ... logic using async libs ...
    return ScanResult(status="vulnerable")
```
