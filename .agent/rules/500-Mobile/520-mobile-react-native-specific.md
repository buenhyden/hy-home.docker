---
trigger: always_on
glob: "**/*.{js,jsx,ts,tsx}"
description: "React Native: FlatList, Styles, New Architecture, and Performance."
---
# React Native Standards

## 1. Performance (Lists)

- **FlatList/FlashList**: Never use `ScrollView` for dynamic lists. Use `FlashList` (Shopify) for best performance.
- **Memoization**: `renderItem` callback MUST be memoized. Use `useCallback`.
- **Keys**: Provide stable `keyExtractor` (ID, not index).

### Example: Lists

**Good**

```tsx
const renderItem = useCallback(({ item }) => <ValidItem item={item} />, []);
<FlatList data={data} renderItem={renderItem} keyExtractor={(item) => item.id} />
```

**Bad**

```tsx
<FlatList 
  renderItem={({ item }) => <Item />} // Anonymous function creates new prop every render
/>
```

## 2. Styles

- **StyleSheet**: Use `StyleSheet.create()`. No inline styles for static values.
- **Avoid**: Avoid writing styles in render methods.

## 3. New Architecture (Fabric/Turbo Modules)

- **Adoption**: Migrate to New Architecture for Concurrent Rendering and Fast Native Modules.
- **Configuration**: Enable `newArchEnabled=true` in `gradle.properties` and `Podfile`.

## 4. Platform Specifics

- **Extensions**: Use `Button.ios.tsx` / `Button.android.tsx` for platform-specific components.
- **Platform API**: Use `Platform.OS` for conditional logic.
