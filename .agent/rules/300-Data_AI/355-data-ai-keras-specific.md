---
trigger: always_on
glob: "**/*.py"
description: "Keras: Deep Learning Framework Standards."
---
# Keras Standards

## 1. API Choice

- **Functional API**: Prefer the Functional API (`inputs = Input(); x = Dense()(inputs); Model(inputs, x)`) over `Sequential` models for anything beyond simple stacks. It is more flexible and readable.
- **Subclassing**: Use Model Subclassing ONLY when defining custom training loops or complex dynamic behaviors.

## 2. Preprocessing

- **Layers**: Include preprocessing logic (rescaling, vectorization) INSIDE the model using Keras preprocessing layers (`Rescaling`, `TextVectorization`). This ensures the model is portable (inputs are raw strings/images).

### Example: Preprocessing

**Good**

```python
inputs = keras.Input(shape=(None,), dtype="string")
x = layers.TextVectorization(max_tokens=20000)(inputs)
x = layers.Embedding(20000, 128)(x)
...
```

## 3. Callbacks

- **Safety**: Always use `ModelCheckpoint` and `EarlyStopping` to prevent overfitting and data loss during training.
- **TensorBoard**: Use `TensorBoard` callback for monitoring training metrics.

## 4. Saving

- **Format**: Use the new `.keras` format (Keras v3 format) rather than `.h5` or SavedModel folder, as it is the current standard.
