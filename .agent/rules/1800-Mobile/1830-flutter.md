---
trigger: always_on
glob: "**/*.{dart,yaml}"
description: "Flutter Development Standards: Enforces Dart null safety, widget composition, and mobile performance optimization."
---

# Flutter Development Standards

- **Role**: Flutter Mobile Architect
- **Purpose**: Define technical standards for building multi-platform (iOS, Android, Web) applications using the Flutter framework and Dart language.
- **Activates When**: Developing Flutter widgets, configuring Dart packages, or managing mobile state.

**Trigger**: always_on — Apply during the implementation of Flutter application features.

## 1. Standards

### Principles

- **[REQ-FLT-01] Sound Null Safety**
  - All Dart code MUST utilize sound null safety. The use of the bang operator (`!`) is PROHIBITED unless a value is mathematically guaranteed to be non-null.
- **[REQ-FLT-02] Immutable Composition**
  - UI layouts MUST be built using immutable widget composition. Favor `StatelessWidget` and `const` constructors to minimize re-renders.
- **[REQ-FLT-03] Reactive State Flow**
  - State management MUST utilize reactive patterns (Streams, ValueNotifiers, or MVVM) to ensure UI consistency and performance.

### Core Stack

| Domain | Requirement ID | Recommended Tooling |
| --- | --- | --- |
| Naming | [REQ-FLT-04] | PascalCase (Class) / snake_case (File) |
| Routing | [REQ-FLT-05] | GoRouter |
| Serialization | [REQ-FLT-06] | json_serializable |
| Testing | [REQ-FLT-07] | flutter_test / integration_test |

### Must

- **[REQ-FLT-08] Lazy List Loading**
  - Large or dynamic collections MUST use `ListView.builder` or `SliverList` for memory-efficient lazy loading.
- **[REQ-FLT-09] Explicit Error Boundaries**
  - Asynchronous data fetches using `FutureBuilder` or `StreamBuilder` MUST explicitly handle error and loading states.
- **[REQ-FLT-10] GPU-Aware Rendering**
  - Computationally heavy tasks (e.g., large data parsing) MUST be offloaded to an `Isolate` (via `compute()`) to prevent UI jank.

### Must Not

- **[BAN-FLT-01] Inline Helper Functions**
  - UI logic MUST NOT be defined in multi-line helper functions within the `build()` method; use private `Widget` classes.
- **[BAN-FLT-02] Hardcoded Multi-Region Strings**
  - UI text MUST NOT be hardcoded; utilize the `intl` or `i18n-js` libraries for all user-facing content.

### Failure Handling

- **Stop Condition**: Stop execution if a required null-check fails or a widget rebuild loop is detected.

## 2. Procedures

- **[PROC-FLT-01] Build Runner Audit**
  - IF modifying data models THEN MUST run `dart run build_runner build` to regenerate serialization logic.
- **[PROC-FLT-02] Performance Profiling**
  - Use the Flutter DevTools "Performance" bridge to verify that the app maintains a consistent 60FPS on target hardware.

## 3. Examples

### Secure Pattern Matching (Dart)

```dart
String? getUserName(User? user) {
  return switch (user) {
    User(name: final name) => name,
    null => null,
  };
}
```

## 4. Validation Criteria

- **[VAL-FLT-01] Analyze Coverage**
  - [ ] `flutter analyze` returns zero errors or high-priority lint warnings.
- **[VAL-FLT-02] Jank Verification**
  - [ ] Frame time profiles confirm zero frames exceeding 16ms during scroll interactions.
- **[VAL-FLT-03] Model Integrity**
  - [ ] Serialization tests confirm that `fromJson` and `toJson` cycles are lossless.
