---
trigger: always_on
glob: ["**/*.{ts,js,tsx,jsx}"]
description: "Frontend Networking Standards: Enforces singleton API clients, request cancellation via AbortController, and secure WebSocket/tRPC patterns."
---

# Frontend Networking Standards

- **Role**: Frontend Networking Architect
- **Purpose**: Define standards for robust, secure, and performant network communication between the frontend application and backend services.
- **Activates When**: Implementing API clients (Fetch/Axios), configuring WebSockets (Socket.IO), or designing tRPC procedurals.

**Trigger**: always_on — Apply during the implementation of all network-dependent frontend features.

## 1. Standards

### Principles

- **[REQ-NET-01] Singleton Client Abstraction**
  - All network requests MUST be routed through a centralized, singleton API client. Ad-hoc `fetch()` calls in components are STRICTLY PROHIBITED.
- **[REQ-NET-02] Mandatory Request Cancellation**
  - Asynchronous network requests MUST utilize `AbortController` (Fetch) or `signal` (Axios) to prevent memory leaks and race conditions during component teardown.
- **[REQ-NET-03] Strict Response Typing**
  - All API response payloads MUST have explicit TypeScript interfaces. The use of `any` for network data is STRICTLY PROHIBITED.

### Protocol Baseline

| Protocol | Requirement ID | Authority / Standard |
| --- | --- | --- |
| REST (HTTP) | [REQ-NET-04] | `Axios` / `Fetch` with interceptors |
| WebSockets | [REQ-NET-05] | `Socket.IO` with WSS and Auth |
| Type-Safe RPC| [REQ-NET-06] | `tRPC` with Zod input validation |

### Must

- **[REQ-NET-07] Global Interception Logic**
  - The API client MUST implement global interceptors for handling authentication injections (e.g., Bearer tokens) and standard error normalization.
- **[REQ-NET-08] Secure WebSocket Transport**
  - Real-time communication MUST utilize encrypted `wss://` protocols and transmit authentication tokens via the initial `auth` payload.
- **[REQ-NET-09] Explicit Timeout Configuration**
  - All network clients MUST define explicit timeout thresholds (default < 10s) to prevent hanging UI states during network degradation.

### Must Not

- **[BAN-NET-01] Silent Rejection Adoption**
  - Do NOT ignore network errors; every fail path MUST be handled either by a global notification system or a component-level fallback state.
- **[BAN-NET-02] Token Leakage via Headers**
  - Authentication tokens MUST NOT be passed as URL query parameters; utilize the `Authorization` header exclusively.

### Failure Handling

- **Stop Condition**: Stop feature execution if a network request is identified as lacking a corresponding cancellation signal in a `useEffect` cleanup.

## 2. Procedures

- **[PROC-NET-01] Race Condition Audit**
  - IF a component fetches data based on a changing ID THEN MUST verify that the `AbortController` correctly cancels outdated inflight requests.
- **[PROC-NET-02] Schema Alignment**
  - Regularly sync frontend API interfaces with the backend contract to prevent runtime parsing failures.

## 3. Examples

### Clean Axios Setup (Good)

```typescript
export const api = axios.create({ baseURL: '/api/v1', timeout: 5000 });
api.interceptors.request.use(config => {
  config.headers.Authorization = `Bearer ${getToken()}`;
  return config;
});
```

## 4. Validation Criteria

- **[VAL-NET-01] Interceptor Integrity**
  - [ ] audit confirms that 100% of outgoing requests include the required security headers.
- **[VAL-NET-02] Cancellation Verification**
  - [ ] Browser DevTools confirm that network requests are "Canceled" immediately upon component unmounting.
- **[VAL-NET-03] Type Compliance**
  - [ ] TypeScript compiler verifies that all consumed API data matches the defined response interfaces.
