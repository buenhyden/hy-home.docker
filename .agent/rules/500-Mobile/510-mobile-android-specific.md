---
trigger: always_on
glob: "**/*.{kt,kts,java,xml}"
description: "Android (Kotlin): Jetpack Compose, Coroutines, Hilt DI, and MVVM."
---
# Android Standards

## 1. Jetpack Compose

- **State Hoisting**: Pass state DOWN, events UP. Composables should be stateless where possible.
- **Side Effects**: Use `LaunchedEffect` for one-off events, `DisposableEffect` for cleanup.
- **Recomposition**: Avoid unnecessary recompositions. Use `remember`, `derivedStateOf`.

### Example: Compose

**Good**

```kotlin
@Composable
fun UserScreen(
  user: User, 
  onSave: (User) -> Unit
) { ... }
```

**Bad**

```kotlin
@Composable
fun UserScreen(viewModel: UserViewModel) {
  // Hard coupling to ViewModel makes preview/testing hard
}
```

## 2. Coroutines & Lifecycle

- **Scope**: Use `viewModelScope` for ViewModel tasks. Use `lifecycleScope` for Activity/Fragment.
- **Context**: Use `Dispatchers.IO` for DB/Network.

### Example: Coroutines

**Good**

```kotlin
viewModelScope.launch(Dispatchers.IO) {
    repo.saveData()
}
```

**Bad**

```kotlin
GlobalScope.launch { ... } // Memory leak risk
```

## 3. Dependency Injection (Hilt)

- **Modules**: Use `@Module` and `@Provides` for external dependencies.
- **Scoping**: Use `@Singleton`, `@ActivityScoped` appropriately.

## 4. Room (Persistence)

- **Entities**: Use `@Entity` for DB tables.
- **DAOs**: Use `suspend fun` for DAO methods.
