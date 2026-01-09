---
trigger: always_on
glob: "**/*.{ts,tsx}"
description: "Zustand Best Practices: Typed stores, slices, and performance."
---
# Zustand Best Practices

## 1. Type Safety

- **Interfaces**: ALWAYS define explicit interfaces for State and Actions.
- **Generics**: Use `create<State>()` to enforce types.

```typescript
interface CounterState {
  count: number;
  increment: () => void;
}
const useStore = create<CounterState>((set) => ({ ... }));
```

## 2. Store Structure

- **Slices**: For large apps, use the Slice pattern to split state into logical units (`authSlice`, `uiSlice`).
- **Composition**: Compose slices into a root store.
- **Single Instance**: Define the store at the module level, never inside a component.

## 3. Actions & Updates

- **Functional Updates**: Use `set((state) => ({ count: state.count + 1 }))` to avoid stale closures.
- **Async**: Handle async logic directly in actions. Zustand supports async/await out of the box.
- **Immer**: Use `immer` middleware for complex nested state updates if needed.

## 4. Performance

- **Selectors**: Select ONLY the state you need to prevent unnecessary re-renders.

  ```typescript
  // Good
  const count = useStore((state) => state.count);
  
  // Bad (Re-renders on ANY change)
  const { count } = useStore();
  ```

- **Shallow**: Use `useShallow` or `shallow` comparison when selecting multiple values or objects.

## 5. Middleware

- **Persist**: Use `persist` middleware for LocalStorage/SessionStorage. Always version your store.
- **DevTools**: Enable `devtools` in development mode.

## 6. React Hooks Integration

- **Rules**: Top-level only. No loops/conditions.
- **useMemo/Callback**: Use `useMemo` for expensive computations, `useCallback` for stable function references.
- **Custom Hooks**: Name with `use` prefix (`useFetch`, `useAuth`).
