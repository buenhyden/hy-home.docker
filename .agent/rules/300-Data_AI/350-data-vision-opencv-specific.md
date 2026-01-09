---
trigger: always_on
glob: "**/*.py"
description: "OpenCV: Vectorized Operations, BGR/RGB Handling, and Type Safety specific rules."
---
# OpenCV (opencv-python) Specific Rules

## 1. Vectorization & Performance

- **Vectorize**: Use NumPy vectorized operations instead of Python loops for pixel manipulation.
- **Functions**: Prefer `cv2` C++ optimized functions over manual implementation.
- **Copies**: Avoid `copy()` unless necessary; use slicing/views.

### Example: Inversion

#### Good (Vectorized)

```python
# Fast (Vectorized)
inverted = 255 - image
```

#### Bad (Loop)

```python
# Slow (Pixel Loop)
for y in range(h):
    for x in range(w):
        img[y,x] = 255 - img[y,x]
```

## 2. Common Pitfalls

- **BGR vs RGB**: OpenCV uses **BGR** by default. Matplotlib uses **RGB**. Explicitly convert with `cv2.cvtColor`.
- **Loading**: Check if `cv2.imread` returns `None`. It does not raise an exception on failure.

### Example: Safe Loading

#### Good (Vectorized)

```python
img = cv2.imread(path)
if img is None:
    raise FileNotFoundError(f"Cannot load {path}")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

## 3. Type Safety

- **Types**: Use `np.uint8` for images. Convert to `np.float32` for math, then back.
- **Hints**: Annotate image arguments as `np.ndarray`.
