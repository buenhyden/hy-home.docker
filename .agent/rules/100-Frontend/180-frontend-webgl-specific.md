---
trigger: always_on
glob: "**/*.{js,ts,tsx}"
description: "WebGL/Three.js: R3F, Memory Management, and Frame Loops."
---
# WebGL & Three.js Standards

## 1. React Three Fiber (R3F)

- **Declarative**: Use JSX `<mesh>` over imperative `new Mesh()`.
- **Hooks**: Use `useThree()` for scene access, `useLoader()` for assets.

## 2. Frame Loop Optimization

- **Animation**: Use `useFrame((state, delta) => ...)` for animation loops.
- **Throttling**: Don't put heavy logic inside `useFrame`. It runs 60/120 times per second.

### Example: Animation

**Good**

```tsx
useFrame((state, delta) => {
  ref.current.rotation.y += delta; // Frame-rate independent
});
```

**Bad**

```tsx
useFrame(() => {
  ref.current.rotation.y += 0.01; // Tied to refresh rate (faster on 144hz)
  heavyCalculation(); // KILLS performance
});
```

## 3. Memory Management

- **Instancing**: Use `<InstancedMesh>` for >50 duplicate objects.
- **Disposal**: R3F handles disposal for components. For manual Three.js objects, call `.dispose()`.
