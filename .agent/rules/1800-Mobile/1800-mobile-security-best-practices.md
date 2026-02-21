---
trigger: always_on
glob: "**/*.{kt,swift,tsx,js}"
description: "Mobile Security Standards: Enforces zero-trust input, secure data at rest, and platform-specific hardening."
---

# Mobile Security Best Practices

- **Role**: Mobile Security Engineer
- **Purpose**: Define standards for securing mobile applications against data leakage, unauthorized access, and malicious exploitation.
- **Activates When**: Developing security-critical features, handling sensitive user data, or configuring network communication.

**Trigger**: always_on — Apply during the security-sensitive phases of mobile development.

## 1. Standards

### Principles

- **[REQ-MOBS-01] Zero-Trust Input Handling**
  - All external inputs (Deep Links, API responses, File uploads) MUST be assumed malicious until validated against an allow-list.
- **[REQ-MOBS-02] Mandatory Encryption at Rest**
  - Sensitive data MUST NEVER be stored in plain text. Use platform-specific secure storage (Keychain for iOS, EncryptedSharedPreferences for Android).
- **[REQ-MOBS-03] Defense in Depth**
  - Apply multiple layers of security, including code obfuscation, certificate pinning, and runtime integrity checks.

### Security Framework

| Category | Requirement ID | Recommended Tooling |
| --- | --- | --- |
| Storage | [REQ-MOBS-04] | SQLCipher / Keychain / SecureStore |
| Network | [REQ-MOBS-05] | TLS 1.2+ / Cert Pinning |
| Hardening | [REQ-MOBS-06] | R8 (Android) / Bitcode (iOS) |
| Auth | [REQ-MOBS-07] | OAuth2 / Biometrics |

### Must

- **[REQ-MOBS-08] Explicit Certificate Pinning**
  - High-security applications MUST implement certificate pinning to prevent Man-in-the-Middle (MitM) attacks.
- **[REQ-MOBS-09] Biometric Verification**
  - Sensitive operations (e.g., wallet access) MUST require secondary biometric or passcode verification.
- **[REQ-MOBS-10] Scoped Storage Enforcement**
  - Applications MUST utilize scoped storage (Android) and App Sandboxing (iOS) to prevent unauthorized file access.

### Must Not

- **[BAN-MOBS-01] Hardcoded API Secrets**
  - API keys and private secrets MUST NOT be hardcoded in the primary binary; use build-time injection or secure vaulting.
- **[BAN-MOBS-02] Plain-Text Logging**
  - Personally Identifiable Information (PII) and authentication tokens MUST NOT be written to the system logs in production.

### Failure Handling

- **Stop Condition**: Stop feature activation if the device is detected to be Rooted or Jailbroken (for high-security apps).

## 2. Procedures

- **[PROC-MOBS-01] Dependency Audit**
  - IF adding a new mobile dependency THEN MUST run SAST/DAST audits to verify its security posture.
- **[PROC-MOBS-02] Tamper Verification**
  - Regularly verify the integrity of the application binary against known signatures during runtime.

## 3. Examples

### Secure Storage (React Native)

```typescript
import EncryptedStorage from 'react-native-encrypted-storage';

async function saveToken(token: string) {
  await EncryptedStorage.setItem('auth_token', token);
}
```

## 4. Validation Criteria

- **[VAL-MOBS-01] Pinning Verification**
  - [ ] Network audit confirms that requests fail if the server's certificate does not match the pinned hash.
- **[VAL-MOBS-02] Secret Audit**
  - [ ] Gitleaks and binary analysis confirm zero exposure of hardcoded private keys or tokens.
- **[VAL-MOBS-03] Sandboxing Check**
  - [ ] verify that the app cannot access files outside its own designated sandbox directory.
