---
trigger: always_on
glob: "**/*.{py,js,ts,jsx,tsx,json,yml,yaml}"
description: "Security Integrity (OWASP A08): Safe deserialization, SRI, and package integrity."
---
# Security Integrity Standards (OWASP A08)

## 1. Safe Deserialization

- **No `eval()`**: NEVER use `eval()` or `new Function()` with user input.
- **Python**:
  - **AVOID** `pickle`, `marshal`, `shelve` on untrusted data.
  - **USE** `json.loads` or `yaml.safe_load()`.
- **JavaScript**:
  - **AVOID** `eval()`. Use `JSON.parse()`.
  - **Prototype Pollution**: Use `Object.create(null)` or `Map` to prevent pollution.

## 2. Subresource Integrity (SRI)

- **Frontend**: All third-party scripts (CDNs) MUST have an `integrity` attribute (SHA-384/512).

  ```html
  <script src="https://cdn.example.com/lib.js" 
          integrity="sha384-..." 
          crossorigin="anonymous"></script>
  ```

## 3. Supply Chain Security

- **Lockfiles**: ALWAYS commit `package-lock.json`, `npm-shrinkwrap.json`, or `yarn.lock`.
- **Audits**: Run `npm audit` or `pip-audit` in CI/CD.
- **Pinning**: Pin dependency versions exactly (no `^` or `~` for critical infra) or use hash checking (`pip install --require-hashes`).

## 4. Input Integrity

- **Downloads**: Verify checksums of downloaded binaries/files before execution.
- **Updates**: Cryptographically sign and verify software updates.
