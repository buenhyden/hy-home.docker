---
trigger: always_on
glob: ["**/*.{html,js}"]
description: "HTMX Standards: Enforces hypermedia-driven interfaces, server-side partial rendering, and progressive enhancement."
---

# HTMX Development Standards

- **Role**: Hypermedia Solutions Architect
- **Purpose**: Define standards for building modern, responsive user interfaces using the HTMX library and server-side partial rendering.
- **Activates When**: Implementing HTMX attributes, configuring server-side fragment responses, or managing hypermedia flow control.

**Trigger**: always_on — Apply during the development of HTMX-enhanced UI components.

## 1. Standards

### Principles

- **[REQ-HTMX-01] Explicit Trigger Definition**
  - HTMX interactions MUST explicitly define their triggers (e.g., `keyup delay:500ms`) to prevent server-side load spikes.
- **[REQ-HTMX-02] Hypermedia Fragment Integrity**
  - The server MUST return partial HTML fragments (e.g., `<li>...</li>`), NOT full pages or raw JSON data for HTMX requests.
- **[REQ-HTMX-03] Progressively Enhanced Boost**
  - Utilize `hx-boost="true"` for standard links and forms to provide a single-page-application (SPA) experience while maintaining SEO compatibility.

### Attribute Baseline

| Attribute | Requirement ID | Primary Responsibility |
| --- | --- | --- |
| Request | [REQ-HTMX-04] | `hx-get`, `hx-post`, `hx-put` |
| Target | [REQ-HTMX-05] | Explicit `hx-target` ID selector |
| Swap | [REQ-HTMX-06] | `hx-swap` strategy (outerHTML/innerHTML) |
| Indicator | [REQ-HTMX-07] | Visual feedback during inflight requests |

### Must

- **[REQ-HTMX-08] Explicit Loading Cues**
  - Every asynchronous HTMX request MUST be accompanied by a visual indicator (e.g., `hx-indicator`) to manage user expectations.
- **[REQ-HTMX-09] Server-Side Header Verification**
  - Backend handlers MUST verify the `HX-Request` header to distinguish between partial fragments and full-page refreshes.
- **[REQ-HTMX-10] Out-Of-Band (OOB) Lifecycle**
  - Critical UI state updates (e.g., Cart counts, notifications) MUST use `hx-swap-oob="true"` to ensure atomicity across the page.

### Must Not

- **[BAN-HTMX-01] JSON Dependency**
  - Do NOT attempt to parse or render JSON data on the client using HTMX; maintain the "HATEOAS" principle of server-side HTML generation.
- **[BAN-HTMX-02] Blind Polling**
  - Avoid using short-interval polling (`hx-trigger="every 1s"`) unless strictly required for real-time monitoring; prefer WebSockets where available.

### Failure Handling

- **Stop Condition**: Stop feature development if the server returns a 200 OK status with an empty body for a request that expects a UI update.

## 2. Procedures

- **[PROC-HTMX-01] Partial Sync Audit**
  - IF a new UI fragment is created THEN MUST verify its accessibility (ARIA roles) as an independent DOM subtree.
- **[PROC-HTMX-02] Fragmentation Review**
  - Conduct a monthly audit of server templates to ensure fragments are granular and reusable across multiple routes.

## 3. Examples

### Debounced Search Input (Good)

```html
<input
  type="text"
  name="q"
  hx-get="/search"
  hx-trigger="keyup changed delay:500ms"
  hx-target="#results"
/>
```

## 4. Validation Criteria

- **[VAL-HTMX-01] Fragment Validity**
  - [ ] Every HTMX-targeted route returns valid, partial HTML without <html> or <body> tags.
- **[VAL-HTMX-02] Trigger Efficiency**
  - [ ] Network logs confirm zero "redundant" requests during rapid user interaction.
- **[VAL-HTMX-03] Indicator Visibility**
  - [ ] Visual audit confirms that a loading state is visible within 100ms of any HTMX request.
