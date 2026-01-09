---
trigger: always_on
glob: "**/*.swift"
description: "iOS SwiftUI: View composition, Data flow, and MVVM."
---
# iOS SwiftUI Standards

## 1. View Structure

- **Short**: Views should be small. Extract subviews.
- **Modifiers**: Order matters.

### Example: Modifiers

**Good**

```swift
Text("Hello")
    .padding()
    .background(Color.red) // Background includes padding
```

**Bad**

```swift
Text("Hello")
    .background(Color.red)
    .padding() // Padding is outside background
```

## 2. Data Flow

- **Props**: Use `@Binding` for two-way, `let` for one-way.
- **Objects**: Use `@StateObject` (create) vs `@ObservedObject` (pass).

### Example: Objects

**Good**

```swift
@StateObject var viewModel = ViewModel() // Persists across redraws
```

**Bad**

```swift
@ObservedObject var viewModel = ViewModel() // Recreated on every View init if not injected
```
