---
trigger: always_on
glob: "**/*.{js,ts,json,webmanifest}"
description: "Progressive Web App (PWA) Standards: Enforces manifest compliance, offline resilience, and service worker best practices."
---

# PWA Standards

- **Role**: Mobile Web Architect
- **Purpose**: Define standards for building resilient, installable, and performant Progressive Web Apps.
- **Activates When**: Configuring Service Workers, Web Manifests, or offline-first logic.

**Trigger**: always_on — Apply during the development of PWA-capable applications.

## 1. Standards

### Principles

- **[REQ-PWA-01] Offline Resilience**
  - Applications SHOULD provide a meaningful experience (e.g., offline page) when the network is unavailable.
- **[REQ-PWA-02] Installability**
  - PWAs MUST meet all browser criteria for "Add to Home Screen" (Manifest, HTTPS, Service Worker).
- **[REQ-PWA-03] Fast Re-engagement**
  - Service worker caching MUST prioritize high-performance data retrieval for return users.

### Must

- **[REQ-PWA-04] Valid Manifest**
  - The `manifest.webmanifest` MUST include all required fields (name, icons, start_url, display).
- **[REQ-PWA-05] Resource Fetching**
  - Service workers MUST implement a caching strategy (e.g., Stale-While-Revalidate) for static assets.
- **[REQ-PWA-06] HTTPS Enforcement**
  - PWAs MUST only be deployed over secure (HTTPS) connections.

### Must Not

- **[BAN-PWA-01] Large Caches**
  - Service workers MUST NOT cache large, unnecessary assets (> 20MB total) without user consent or explicit need.
- **[BAN-PWA-02] Obtrusive Install Prompts**
  - "Install App" prompts MUST NOT interrupt critical user workflows (checkout, form entry).

### Failure Handling

- **Stop Condition**: Stop the update process if a new Service Worker fails to activate or creates a fetch loop.

## 2. Procedures

- **[PROC-PWA-01] Sync Verification**
  - IF using Background Sync THEN MUST handle potential data conflicts on reconnection.
- **[PROC-PWA-02] Manifest Testing**
  - Verify manifest validity using Lighthouse or the Chrome DevTools Application tab.

## 3. Examples

### Basic Service Worker Cache

```javascript
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((res) => {
      return res || fetch(event.request);
    })
  );
});
```

## 4. Validation Criteria

- **[VAL-PWA-01] Lighthouse Audit**
  - [ ] App passes the PWA category in the Lighthouse audit.
- **[VAL-PWA-02] Offline Mode**
  - [ ] App displays a fallback UI when the network is toggled off in DevTools.
- **[VAL-PWA-03] Splash Screen**
  - [ ] Icons and theme colors are correctly applied during app launch.
