---
trigger: always_on
glob: "**/*.py"
description: "Pillow (PIL): Image Processing, Resource Management, and Optimization specific rules."
---
# Pillow (PIL) Specific Rules

## 1. Resource Management

- **Context Managers**: ALWAYS use `with Image.open(...) as im:` to ensure file handles are closed.
- **Copying**: If returning an image from a context manager, call `.copy()`.

### Example: Safe Opening

#### Good

```python
def load_image(path: str) -> Image.Image:
    with Image.open(path) as im:
        return im.copy()
```

#### Bad

```python
im = Image.open("file.jpg") # Resources may leak if not closed
```

## 2. Optimization

- **Saving**: Optimize for web when saving. Use `quality` and `optimize=True`.
- **Modes**: Convert to `RGB` before saving as JPEG (JPEG does not support RGBA).
- **Resizing**: Use high-quality filters like `Image.Resampling.LANCZOS` for downsizing.

### Example: Web Optimization

#### Good

```python
if im.mode == 'RGBA':
    im = im.convert('RGB')
im.save('out.jpg', quality=85, optimize=True)
```

## 3. Security

- **Decompression Bomb**: Be aware of `Image.MAX_IMAGE_PIXELS`. Don't arbitrarily increase it unless you trust the source.
- **Plugins**: Import specific plugins explicitly if using obscure formats.
