---
trigger: always_on
glob: "**/*.py"
description: "Modal: Serverless Infrastructure, GPU Configuration, and Volumes specific rules."
---
# Modal Specific Rules

## 1. Application Structure

- **Single Stub**: Define ONE `stub = modal.Stub("name")` per major service.
- **Entrypoints**: define `@stub.local_entrypoint()` for local testing.
- **Modularity**: Keep Modal configuration (images, volumes) separate from business logic.

## 2. Resource Configuration

- **Explicit Resources**: Always specify `gpu`, `cpu`, and `memory` requirements explicitly.
- **Images**: Build custom images with dependencies pre-installed. Avoid installing heavy deps at runtime.

### Example: Configured Function

#### Good (Configuration)

```python
image = modal.Image.debian_slim().pip_install("torch", "transformers")

@stub.function(
    image=image,
    gpu="A10G",
    timeout=600
)
def run_inference(x):
    ...
```

## 3. Storage & Secrets

- **Volumes**: Use `modal.Volume` for large model weights (lazy loading). Do NOT download weights in the image build if they change often or are huge.
- **Secrets**: Use `modal.Secret` for keys. Never hardcode.

### Example: Volume Usage

#### Good (Configuration)

```python
vol = modal.Volume.from_name("model-weights")

@stub.function(volumes={"/models": vol})
def predict():
    # Load from /models/...
```
