---
trigger: always_on
glob: "**/*.py"
description: "TensorFlow: Model Building, Training, Performance, and Deployment."
---
# TensorFlow Standards

## 1. Model Building (Keras API)

- **Functional API**: Prefer for complex models with multiple inputs/outputs.
- **Sequential**: Use only for simple linear stacks.

### Example: Functional API

**Good**

```python
import tensorflow as tf

inputs = tf.keras.Input(shape=(784,))
x = tf.keras.layers.Dense(128, activation='relu')(inputs)
outputs = tf.keras.layers.Dense(10, activation='softmax')(x)
model = tf.keras.Model(inputs=inputs, outputs=outputs)
```

**Bad**

```python
# Using deprecated tf.compat.v1 API
with tf.compat.v1.Session() as sess:
    ...
```

## 2. Data Pipeline (tf.data)

- **tf.data.Dataset**: Use for efficient data loading.
- **Prefetch**: Always add `.prefetch(tf.data.AUTOTUNE)`.
- **Cache**: Use `.cache()` for small datasets.

### Example: Pipeline

**Good**

```python
dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
dataset = dataset.shuffle(1000).batch(32).prefetch(tf.data.AUTOTUNE)
```

**Bad**

```python
# Loading all data into memory, no batching
model.fit(x_train, y_train)
```

## 3. Mixed Precision Training

- **Enable**: Use `tf.keras.mixed_precision.set_global_policy('mixed_float16')`.
- **Benefit**: 2-3x speedup on modern GPUs.

## 4. Model Saving

- **SavedModel**: Use `model.save('path/')` for TF Serving.
- **Checkpoints**: Use `ModelCheckpoint` callback during training.

### Example: Save

**Good**

```python
model.save('saved_model/')
# Load: tf.keras.models.load_model('saved_model/')
```

## 5. TensorBoard

- **Logging**: Use `TensorBoard` callback for visualization.
- **Metrics**: Log custom metrics with `tf.summary`.
