---
trigger: always_on
glob: "**/*.{css,js,tsx,html}"
description: "Cross-Browser Compatibility Standards: Enforces multi-browser testing, polyfilling, and graceful degradation."
---

# Cross-Browser Compatibility Standards

- **Role**: Browser Specialist
- **Purpose**: Define standards for ensuring consistent user experience across different browsers, versions, and devices.
- **Activates When**: Writing frontend code, configuring build targets, or defining CSS features.

**Trigger**: always_on — Apply during the testing and development of frontend assets.

## 1. Standards

### Principles

- **[REQ-BROWSER-01] Graceful Degradation**
  - Applications MUST remain functional even in older browsers, although visual fidelity may be reduced.
- **[REQ-BROWSER-02] Feature Detection**
  - Browser features MUST be detected (using Modernizr or JS) rather than assuming support based on user-agent strings.
- **[REQ-BROWSER-03] Modern Purity**
  - Code SHOULD target the latest 2 versions of major browsers (Chrome, Firefox, Safari, Edge) as the primary baseline.

### Support Baseline

| Browser | Version Target | Priority |
| --- | --- | --- |
| Chrome | Last 2 | Critical |
| Safari | Last 2 | Critical |
| Firefox | Last 2 | High |
| Safari iOS | Last 2 | Critical |

### Must

- **[REQ-BROWSER-04] Vendor Prefixing**
  - Use Autoprefixer to automatically handle vendor prefixes for CSS properties.
- **[REQ-BROWSER-05] Transpilation**
  - JavaScript MUST be transpiled (Babel/SWC) to support the identified browser baseline.
- **[REQ-BROWSER-06] Functional Parity**
  - Critical business logic (checkout, auth) MUST work identically across all supported browsers.

### Must Not

- **[BAN-BROWSER-01] User-Agent Sniffing**
  - Code MUST NOT rely on User-Agent strings for logic branching (use feature detection).
- **[BAN-BROWSER-02] IE11 Support**
  - IE11 support is FORBIDDEN unless explicitly required by the project contract and justified by use case.

### Failure Handling

- **Stop Condition**: Stop deployment if a critical functional regression is detected on any Tier 1 browser.

## 2. Procedures

- **[PROC-BROWSER-01] Layout Testing**
  - IF modifying global layouts THEN MUST verify on Safari (macOS/iOS) due to unique rendering engine quirks.
- **[PROC-BROWSER-02] Polyfill Management**
  - Only load required polyfills to avoid bloating the bundle for modern users.

## 3. Examples

### Feature Detection

```javascript
if ('serviceWorker' in navigator) {
  // Service Worker supported
}
```

## 4. Validation Criteria

- **[VAL-BROWSER-01] Multi-Engine Success**
  - [ ] App is tested and confirmed working on WebKit (Safari), Blink (Chrome), and Gecko (Firefox).
- **[VAL-BROWSER-02] Layout Integrity**
  - [ ] CSS Grid/Flexbox layouts are verified to not break on older Mobile Safari versions.
- **[VAL-BROWSER-03] Mobile Verification**
  - [ ] Touch-specific events work as intended on mobile versions of the browsers.
