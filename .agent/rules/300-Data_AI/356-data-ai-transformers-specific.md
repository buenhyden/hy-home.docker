---
trigger: always_on
glob: "**/*.py"
description: "Transformers Best Practices: Modular models, Trainer API, and safetensors."
---
# Transformers Best Practices

## 1. Model Definition

- **Modular**: Inherit from existing base classes (e.g., `LlamaModel`) instead of rewriting from scratch.
- **Location**: `src/transformers/models/<name>/`.

## 2. Training & Inference

- **Trainer**: Always use `transformers.Trainer` for training loops (optimization, mixed precision, efficient hardware usage).
- **Pipeline**: Use `transformers.pipeline` for standard inference tasks.

## 3. Serialization

- **Safetensors**: ALWAYS use `safe_serialization=True` when saving models. Avoid pickle-based `torch.save`.

### Example: Inference

#### Good (Inference)

```python
from transformers import pipeline
classifier = pipeline("sentiment-analysis")
result = classifier("I love this!")
```

#### Bad (Inference)

```python
# Manual tokenizer handling and model forward pass for simple tasks
```
