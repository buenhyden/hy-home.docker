---
trigger: always_on
glob: "**/*.{ts,tsx,js,jsx}"
description: "Firebase: Firestore, Auth, Cloud Functions, and Security Rules."
---
# Firebase Standards

## 1. Firestore Data Modeling

- **Denormalize**: Duplicate data to avoid complex joins.
- **Document Size**: Keep documents under 1MB.
- **Subcollections**: Use for large related datasets.

## 2. Security Rules

- **Deny by Default**: Start with `allow read, write: if false;`.
- **Granular Permissions**: Validate user roles and resource ownership.
- **Validation**: Validate data types and required fields in rules.

## 3. Cloud Functions

- **Idempotency**: Design functions to be idempotent.
- **Cold Starts**: Minimize global scope code.
- **Firebase Admin SDK**: Use for server-side operations.

## 4. Emulator

- **Local Dev**: Use Firebase Local Emulator Suite for all services.
- **Testing**: Write integration tests against emulators.
