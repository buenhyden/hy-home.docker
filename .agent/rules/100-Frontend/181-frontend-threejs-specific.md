---
trigger: always_on
glob: "**/*.{js,jsx,ts,tsx}"
description: "Three.js: WebGL Optimization, Asset Management, and Cleanup specific rules."
---
# Three.js Specific Rules

## 1. Resource Management

- **Disposal**: Explicitly call `.dispose()` on Geometries, Materials, and Textures when removing objects to prevent GPU memory leaks.
- **Lazy Loading**: Load assets (GLTF, Textures) asynchronously and on-demand.

### Example: Disposal

#### Good (Pattern)

```javascript
function disposeMesh(mesh) {
    mesh.geometry.dispose();
    mesh.material.dispose();
    scene.remove(mesh);
}
```

## 2. Performance Optimization

- **Draw Calls**: Minimize draw calls. Use `InstancedMesh` for repetitive objects (e.g., forests, particles).
- **Batching**: Merge static geometries where possible.
- **Error Checks**: Check `gl.getError()` during development but disable in production.

### Example: Instancing

#### Good (Pattern)

```javascript
const mesh = new THREE.InstancedMesh(geometry, material, 1000);
// Set matrices...
scene.add(mesh);
```

## 3. WebGL Best Practices

- **Extensions**: Check for WebGL extension support before using advanced features.
- **Fallbacks**: Provide graceful fallbacks for low-end devices.
