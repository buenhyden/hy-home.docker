---
trigger: always_on
glob: ["**/*.{js,ts,tsx}"]
description: "Data Visualization Standards: Enforces frame-rate independent animations, declarative WebGL (R3F), and modular D3.js patterns."
---

# Data Visualization Standards

- **Role**: Data Visualization Specialist
- **Purpose**: Define standards for building performant, accessible, and mathematically sound data visualizations using WebGL and SVG-based libraries.
- **Activates When**: Implementing charts, 3D scenes (Three.js/R3F), or complex interactive data representations.

**Trigger**: always_on — Apply during the design and development of visualization components.

## 1. Standards

### Principles

- **[REQ-VIZ-01] Frame-Rate Independence**
  - All animations MUST be calculated based on delta time (`delta`), not absolute frames, to ensure consistent speed across 60Hz and 120Hz displays.
- **[REQ-VIZ-02] Modular Resource Loading**
  - Heavy visualization assets (Models, Textures, large Datasets) MUST be loaded asynchronously with appropriate progress feedback (Suspense/Loaders).
- **[REQ-VIZ-03] Accessible Representation**
  - Visualizations MUST include ARIA labels, roles (`img`), and accessible descriptions (`title`/`desc`) for screen reader compatibility.

### Visualization Technology Baseline

| Technology | Requirement ID | Critical Implementation |
| --- | --- | --- |
| WebGL (R3F) | [REQ-VIZ-04] | Declarative JSX over imperative Mesh |
| D3.js | [REQ-VIZ-05] | Data-Join pattern (Enter/Update/Exit) |
| SVG | [REQ-VIZ-06] | Responsive `viewBox` management |
| Optimization | [REQ-VIZ-07] | Geometry instancing (> 50 identical objects) |

### Must

- **[REQ-VIZ-08] Explicit Disposal**
  - Manual Three.js objects (Geometries, Materials, Textures) MUST be explicitly disposed of using `.dispose()` to prevent GPU memory leaks.
- **[REQ-VIZ-09] Modular D3 Lifecycle**
  - D3.js implementations MUST utilize modular imports (`d3-selection`, `d3-scale`) to support tree-shaking and minimize bundle size.
- **[REQ-VIZ-10] High-DPI Support**
  - All canvas-based visualizations MUST account for `devicePixelRatio` to prevent blurring on Retina/High-DPI displays.

### Must Not

- **[BAN-VIZ-01] Main-Thread Heavy Lifting**
  - Do NOT perform complex data processing (e.g., large-scale coordinate mapping) inside the 60fps frame loop; utilize Web Workers or pre-computation.
- **[BAN-VIZ-02] Fixed-Pixel Sizing**
  - Avoid hardcoding pixel widths for charts; utilize responsive containers and `viewBox` for SVGs.

### Failure Handling

- **Stop Condition**: Stop feature execution if a 3D scene identifies a memory leak that causes the GPU memory to grow monotonically over time.

## 2. Procedures

- **[PROC-VIZ-01] Instancing Review**
  - IF a scene renders multiple identical items (> 50) THEN MUST refactor to an `InstancedMesh` to optimize draw calls.
- **[PROC-VIZ-02] Accessibility Pass**
  - Verify for every chart that color-blind safe palettes are utilized or that patterns are used to distinguish data series.

## 3. Examples

### Delta-Time Animation (Good)

```tsx
useFrame((state, delta) => {
  meshRef.current.rotation.y += delta * rotationSpeed;
});
```

## 4. Validation Criteria

- **[VAL-VIZ-01] Memory leak Audit**
  - [ ] Heap snapshot confirms that disposals are correctly removing Three.js objects from memory.
- **[VAL-VIZ-02] Frame Continuity**
  - [ ] Performance monitoring confirms zero "Long Tasks" (> 50ms) during complex visualization interactions.
- **[VAL-VIZ-03] A11y Compliance**
  - [ ] Screen reader testing confirms that chart data trends are conveyed via accessible descriptions.
