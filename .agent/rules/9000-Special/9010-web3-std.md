---
trigger: manual
glob: "**/*.{ts,tsx}"
description: "Web3 Frontend Standards: Enforces Wagmi v2, Viem, transaction safety, and DApp state management patterns."
---

# Web3 Frontend Standards

- **Role**: Web3 Solutions Architect
- **Purpose**: Define standards for high-reliability decentralized application (DApp) development using modern Ethereum toolchains.
- **Activates When**: Developing frontend code for blockchain interaction, configuring wallet connectors, or handling smart contract transactions.

**Trigger**: manual — Apply when the user initiates Web3-related feature development.

## 1. Standards

### Principles

- **[REQ-WEB3-01] Toolchain Modernity**
  - All new Web3 development MUST use Wagmi v2 and Viem. Avoid legacy libraries like `ethers.js` unless required by strict dependencies.
- **[REQ-WEB3-02] Transaction Integrity**
  - Transaction success MUST NOT be assumed based on the hash alone; receipt confirmation is mandatory.
- **[REQ-WEB3-03] UI Interlock**
  - Critical UI interactions (buttons, forms) MUST be disabled during active transaction signing or waiting phases.

### Wallet Connectors

| Connector | Usage | Recommendation |
| --- | --- | --- |
| MetaMask | Browser | Standard |
| WalletConnect | Mobile / Universal | **Mandatory for cross-device** |
| Coinbase | Universal | Highly Recommended |

### Must

- **[REQ-WEB3-04] Typed Chain Config**
  - Wagmi `createConfig` MUST define explicitly typed chains and RPC transports.
- **[REQ-WEB3-05] Receipt Waiting**
  - Uses of `useWriteContract` MUST be paired with `useWaitForTransactionReceipt` to confirm network inclusion.
- **[REQ-WEB3-06] Zod-Validated Actions**
  - Inputs for Web3-related Server Actions MUST be validated with Zod before transaction data construction.

### Must Not

- **[BAN-WEB3-01] Blocking RPC Calls**
  - RPC calls MUST NOT be made synchronously on the main thread; use asynchronous hooks with loading state handlers.
- **[BAN-WEB3-02] Insecure Key Storage**
  - Private keys or sensitive environment variables MUST NOT be exposed to the client-side DApp environment.

### Failure Handling

- **Stop Condition**: Stop transaction flow if the user's connected network (Chain ID) does not match the application configuration.

## 2. Procedures

- **[PROC-WEB3-01] Migration Check**
  - IF updating a legacy DApp THEN MUST audit for any remaining `ethers.js` v5 calls and plan for Viem migration.
- **[PROC-WEB3-02] Loading UX**
  - Handle `isPending` and `isLoading` states for every smart contract interaction to prevent user confusion.

## 3. Examples

### Secure Contract Write

```ts
const { writeContract, data: hash } = useWriteContract();
const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({ hash });
```

## 4. Validation Criteria

- **[VAL-WEB3-01] Network Guarding**
  - [ ] App correctly handles and displays "Wrong Network" alerts.
- **[VAL-WEB3-02] Transaction Flow**
  - [ ] Success/Error feedback is only shown after transaction receipt validation.
- **[VAL-WEB3-03] Bundle Size**
  - [ ] Web3 binaries (Viem/Wagmi) are lazily loaded to minimize initial TTI.
