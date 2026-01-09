---
trigger: always_on
glob: "**/*.dart"
description: "Flutter: Widget Composition, State Management (Riverpod/Bloc), and Linting."
---
# Flutter Standards

## 1. Widgets & Performance

- **Composition**: Prefer composition over inheritance. Extract small widgets.
- **Const**: Use `const` constructors everywhere possible for tree shaking.
- **Keys**: Use `ValueKey` or `ObjectKey` in lists to preserve state correctly.

### Example: Const

**Good**

```dart
const Padding(
  padding: EdgeInsets.all(8.0),
  child: Text('Hello'),
)
```

**Bad**

```dart
Padding( // Rebuilt unnecessarily
  padding: EdgeInsets.all(8.0),
  child: Text('Hello'),
)
```

## 2. State Management (Riverpod)

- **Providers**: Declare globally, consume with `ref.watch`.
- **Immutability**: Use `freezed` for immutable state classes.
- **Notifiers**: Use `StateNotifier` or `Notifier` for complex state.

### Example: Riverpod

**Good**

```dart
final userProvider = StateNotifierProvider<UserNotifier, User>((ref) => UserNotifier());
```

**Bad**

```dart
// Using global mutable variables
User currentUser = User();
```

## 3. Async

- **Avoid FutureBuilder**: Pre-fetch data in providers where possible.
- **Streams**: Close streams in `dispose()` or use `StreamBuilder`.

## 4. Linting

- **Linter**: Use `flutter_lints` or `very_good_analysis`.
- **Run**: `dart format .` and `dart analyze` on every commit.
