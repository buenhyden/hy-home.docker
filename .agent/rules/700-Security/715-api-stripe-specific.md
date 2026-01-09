---
trigger: always_on
glob: "**/*.js,**/*.ts,**/*.py"
description: "Stripe Integration Standards: Security, Idempotency, and Webhooks."
---
# Stripe Integration Standards

## 1. Security

- **Secrets**: NEVER hardcode API keys. Use `STRIPE_SECRET_KEY` env var.
- **Client**: Initialize the client once per process with the specific API version pinned.

### Example: Init

**Good**

```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2025-12-15',
});
```

## 2. Reliability

- **Idempotency**: Always send an `Idempotency-Key` header for write operations (creates/updates) to safely retry network failures.
- **Retries**: Handle `StripeError` exceptions gracefully using the error code/type.

## 3. Webhooks

- **Signature Verification**: ALWAYS verify webhook signatures (`stripe.webhooks.constructEvent`) to prevent spoofing.
- **Async Processing**: Return `200 OK` quickly from webhook handlers and process heavy logic asynchronously (queue).

## 4. UI Flow

- **Elements/Checkout**: Prefer Stripe Checkout or Elements over raw card handling to minimize PCI compliance scope.
