---
trigger: always_on
glob: "**/*"
description: "Mobile Core: Touch UX, Offline First, Permissions, and Deep Linking."
---
# Mobile General Standards

## 1. UX & Touch

- **Targets**: 44pt+ (iOS) / 48dp+ (Android) for all tappable elements.
- **Feedback**: Provide visual feedback (ripple, highlight, opacity change) for ALL tappable elements.
- **Edge-to-Edge**: Support modern navigation bars and notches (SafeAreaView/SafeAreaInsets).

### Example: Touch

**Good**

```css
min-height: 48px;
padding: 12px;
```

**Bad**

```css
height: 20px; /* Too small, frustrating for users */
```

## 2. Offline First

- **Caching**: Store data in local DB (SQLite/Realm/MMKV) before attempting network.
- **Optimistic UI**: Update UI immediately, then sync. Handle sync failures gracefully.
- **Queue**: Queue failed network operations for retry.

## 3. Permissions

- **Context**: Explain *why* before requesting (pre-prompt modal).
- **Timing**: Request Just-in-Time, not on app launch.
- **Fallback**: Always have a graceful degradation if permission denied.

## 4. Deep Linking

- **Universal Links (iOS)**: Configure `apple-app-site-association`.
- **App Links (Android)**: Use `assetlinks.json`.
- **Fallback**: If app not installed, redirect to App Store/Play Store.

## 5. Performance

- **Startup**: Minimize cold start time (<2s to first content).
- **Memory**: Monitor for memory leaks using Xcode Instruments / Android Profiler.
