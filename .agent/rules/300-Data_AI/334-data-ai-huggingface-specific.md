---
trigger: always_on
glob: "**/*.py"
description: "Hugging Face: Auto Classes, Pipeline, PEFT, and Model Hub."
---
# Hugging Face / Transformers Standards

## 1. Model & Tokenizer Loading

- **Auto Classes**: Use `AutoModelForX` and `AutoTokenizer` for flexibility.
- **from_pretrained**: Always use `from_pretrained()` to load models.

### Example: Loading

**Good**

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
```

**Bad**

```python
from transformers import BertForSequenceClassification, BertTokenizer
# Hardcoding specific class limits flexibility
```

## 2. Inference with Pipeline

- **Pipeline**: Use `pipeline()` for common tasks (sentiment, NER, QA).
- **Batching**: Use batch inputs for efficiency.

### Example: Pipeline

**Good**

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
result = classifier("I love Hugging Face!")
```

**Bad**

```python
# Manually tokenizing, running model, argmax, id2label mapping
# Error-prone and verbose
```

## 3. Performance (PEFT / Quantization)

- **LoRA**: Use `peft` library for Parameter-Efficient Fine-Tuning.
- **Quantization**: Use `bitsandbytes` for 4-bit/8-bit quantization.
- **Mixed Precision**: Enable `fp16=True` or `bf16=True` in `TrainingArguments`.

## 4. Saving & Sharing

- **save_pretrained**: Use `model.save_pretrained()` for Hub compatibility.
- **safetensors**: Prefer `safe_serialization=True` for security.
