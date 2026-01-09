---
trigger: always_on
glob: "**/*.py"
description: "PyTorch: Deep learning tensor operations, models, and training loops."
---
# PyTorch Standards

## 1. Device Management

- **Explicit**: Always check `torch.cuda.is_available()`.
- **Movement**: Use `.to(device)` explicitly for models and tensors.
- **Consistency**: Ensure all tensors in an op are on the same device.

## 2. Gradient Management

- **Inference**: Wrap inference code in `with torch.no_grad():`.
- **Zeroing**: Call `optimizer.zero_grad(set_to_none=True)` for slight perf boost.

## 3. Performance

- **DataLoader**: Set `num_workers > 0`, `pin_memory=True` for GPU training.
- **Compilation**: Use `torch.compile(model)` (PyTorch 2.0+) for speedups.
- **Mixed Precision**: Use `torch.cuda.amp` or `torch.autocast` for memory savings.

## 4. Models

- **Structure**: Inherit from `nn.Module`. separate `__init__` (layers) and `forward`.
- **Validation**: Test input/output shapes in unit tests.
