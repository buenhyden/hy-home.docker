---
trigger: always_on
glob: "**/*.{swift}"
description: "iOS Swift Development: Enforces SwiftUI, Human Interface Guidelines (HIG), and actor-based concurrency."
---

# iOS Swift Development Standards

- **Role**: iOS Platform Architect
- **Purpose**: Define technical standards for building expressive, safe, and performant iOS applications using Swift and SwiftUI.
- **Activates When**: Developing iOS views, configuring App Intents, or managing data with SwiftData.

**Trigger**: always_on — Apply during the implementation of iOS application features.

## 1. Standards

### Principles

- **[REQ-IOS-01] Declarative SwiftUI Preference**
  - All new UI development MUST utilize SwiftUI. UIKit is reserved for complex low-level interoperability or legacy maintenance.
- **[REQ-IOS-02] Value-Type Primacy**
  - Favor `struct` over `class` for data models and UI state to ensure thread safety and performance.
- **[REQ-IOS-03] Modern Concurrency**
  - Asynchronous work MUST utilize `async/await` and `Actors` instead of legacy completion handlers or global dispatch queues.

### iOS Ecosystem Baseline

| Category | Requirement ID | Recommended Tooling |
| --- | --- | --- |
| Dependency | [REQ-IOS-04] | Swift Package Manager (SPM) |
| Persistence | [REQ-IOS-05] | SwiftData / Core Data |
| Networking | [REQ-IOS-06] | URLSession / Alamofire |
| Security | [REQ-IOS-07] | Keychain Services |

### Must

- **[REQ-IOS-08] HIG Compliance**
  - Every UI element MUST adhere to Apple's Human Interface Guidelines, specifically regarding safe areas and interaction spacing.
- **[REQ-IOS-09] Privacy Manifests**
  - Applications MUST include a Privacy Manifest (`PrivacyInfo.xcprivacy`) declaring all data usage and tracking behaviors.
- **[REQ-IOS-10] Strict Error Handling**
  - Fallible operations MUST use `do-try-catch` blocks. The use of `try!` is strictly PROHIBITED in production code.

### Must Not

- **[BAN-IOS-01] Massive View Controllers**
  - Do NOT consolidate logic, networking, and UI into a single file; utilize the MVVM-C or Clean Swift architectures.
- **[BAN-IOS-02] Retain Cycle Risks**
  - Avoid strong reference cycles in closures; always use `[weak self]` when capturing class instances.

### Failure Handling

- **Stop Condition**: Stop execution if an unhandled `Result` error occurs or a race condition is identified in thread-sanitizer testing.

## 2. Procedures

- **[PROC-IOS-01] Asset Cataloging**
  - IF adding a new image THEN MUST provide 2x and 3x scale variants to ensure visual clarity across all Retina displays.
- **[PROC-PROC-02] Accessibility Audit**
  - perform a VoiceOver and Dynamic Type verification for every new screen to ensure inclusion.

## 3. Examples

### Safe SwiftUI State

```swift
struct ProfileView: View {
    @State private var isLoading = false
    var body: some View {
        Text("Profile info")
    }
}
```

## 4. Validation Criteria

- **[VAL-IOS-01] Type-Check Pass**
  - [ ] The Xcode compiler emits zero warnings or errors for the current build target.
- **[VAL-IOS-02] Battery Profile**
  - [ ] Energy impact audit in Xcode Instruments confirms zero excessive background wakeups.
- **[VAL-IOS-03] Layout Adaptability**
  - [ ] Previews confirm that the UI remains functional across all standard screen sizes (iPhone SE to iPad Pro).
