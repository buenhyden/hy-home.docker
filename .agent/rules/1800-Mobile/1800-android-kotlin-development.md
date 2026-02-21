---
trigger: always_on
glob: "**/*.{kt,kts,xml}"
description: "Android Kotlin Development: Enforces Jetpack Compose, Material Design, and modern UDF architecture."
---

# Android Kotlin Development Standards

- **Role**: Android Platform Architect
- **Purpose**: Define technical standards for building high-performance, maintainable Android applications using Kotlin and Jetpack Compose.
- **Activates When**: Developing Android activities, Composable functions, or configuring Gradle build scripts.

**Trigger**: always_on — Apply during the implementation of Android application features.

## 1. Standards

### Principles

- **[REQ-AND-01] Reactive UI Totality**
  - All new UI development MUST use Jetpack Compose. Legacy XML Views are reserved for specialized maintenance only.
- **[REQ-AND-02] Unidirectional Data Flow (UDF)**
  - Application state MUST flow downwards, and events MUST flow upwards. Use `ViewModel` and `StateFlow` to manage state.
- **[REQ-AND-03] Lifecycle Awareness**
  - Logic MUST explicitly handle Android lifecycle events and configuration changes without leaking memory.

### Android Jetpack Stack

| Component | Requirement ID | Standard Library |
| --- | --- | --- |
| Database | [REQ-AND-04] | Room |
| DI | [REQ-AND-05] | Hilt |
| Async | [REQ-AND-06] | Coroutines / Flow |
| Background | [REQ-AND-07] | WorkManager |

### Must

- **[REQ-AND-08] Null-Safe Kotlin Logic**
  - Leverage Kotlin's null-safety features. The use of `!!` is PROHIBITED except in verified initialization paths.
- **[REQ-AND-09] Material 3 Adherence**
  - UI components MUST follow Material 3 design systems and utilize the standard `ColorScheme` and `Typography` tokens.
- **[REQ-AND-10] ProGuard/R8 Hardening**
  - Production builds MUST be obfuscated and shrunk using R8, with well-defined baseline profiles for startup optimization.

### Must Not

- **[BAN-AND-01] Blocking IO UI**
  - Network or database operations MUST NOT occur on the main thread; use `Dispatchers.IO` exclusively.
- **[BAN-AND-02] Context Leakage**
  - Do NOT store or pass `Activity` or `Fragment` contexts into long-lived singleton objects or ViewModels.

### Failure Handling

- **Stop Condition**: Stop the build if a memory leak is identified in unit tests or if the Lint check returns high-priority errors.

## 2. Procedures

- **[PROC-AND-01] Module Audit**
  - IF creating a new feature THEN MUST implement it as a separate feature module to support modularization best practices.
- **[PROC-AND-02] Permission Context**
  - Always request permissions in the context of the specific feature use case, providing a rationalization to the user.

## 3. Examples

### Composable State Hoisting

```kotlin
@Composable
fun Counter(count: Int, onIncrement: () -> Unit) {
    Button(onClick = onIncrement) {
        Text("Count: $count")
    }
}
```

## 4. Validation Criteria

- **[VAL-AND-01] Lint Integrity**
  - [ ] Every module passes the standard Android Lint audit with zero "Critical" reports.
- **[VAL-AND-02] Memory Profile**
  - [ ] LeakCanary confirms zero memory leaks during a standard navigation cycle.
- **[VAL-AND-03] Startup Latency**
  - [ ] Baseline profiles verify that the app cold-start remains under 500ms on reference hardware.
