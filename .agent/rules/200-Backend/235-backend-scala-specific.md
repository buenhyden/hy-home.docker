---
trigger: always_on
glob: "**/*.scala"
description: "Scala 3: Pure functional programming, SOLID, and Kafka Streams."
---
# Scala Standards

## 1. Functional Principles

- **Immutability**: Prefer `val` over `var`. Use immutable collections.
- **Pure Functions**: Minimize side-effects. Use `Try`, `Either`, or `Option` for error handling.
- **Pattern Matching**: Use exhaustively. Avoid nested `if/else`.
- **ADT**: Use `case classes` and `sealed traits` (or `enums` in Scala 3).

## 2. Clean Code

- **Methods**: Keep methods small (< 30 lines).
- **Complexity**: Keep cyclomatic complexity < 10.
- **Nesting**: Avoid for-comprehensions deeper than 2 levels.
- **Tail-Rec**: Use `@tailrec` for recursive functions.

## 3. Modern Scala 3

- **Contextual Abstractions**: Prefer `given`/`using` over `implicit`.
- **Enums**: Use for finite alternatives.
- **Opaque Types**: Use to avoid primitive wrapper overhead.

## 4. Kafka & Streaming

- **Blocking**: Avoid blocking calls in stream processing. Off-load to dedicated thread-pools if necessary.
- **Interop**: Wrap Java collections in Scala facades (`.asScala`).

## 5. Tooling

- **Test**: Use ScalaTest with Given-When-Then layout.
- **Formatting**: Use **scalafmt**.
