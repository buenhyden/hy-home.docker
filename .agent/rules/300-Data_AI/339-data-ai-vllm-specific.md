---
trigger: always_on
glob: "**/*.py"
description: "vLLM: LLM Inference, Environment, and Quantization specific rules."
---
# vLLM Specific Rules

## 1. Environment & Installation

- **Isolation**: Always install vLLM in a dedicated environment (Conda/venv).
- **Pinning**: Pin `vllm` version strictly in `requirements.txt` to avoid CUDA mismatch.
- **Hardware**: Ensure GPU compute capability >= 7.0.

## 2. Inference Optimization

- **Quantization**: Use quantization (e.g., `kv_cache_dtype="fp8"` or AWQ/GPTQ models) for production throughput.
- **Continuous Batching**: Enabled by default; configure `max_num_seqs` if needed.
- **Engine Usage**: Separate engine initialization from request handling.

### Example: Efficient Engine

#### Good

```python
engine = LLM(
    model="meta-llama/Llama-2-7b-hf",
    kv_cache_dtype="fp8",
    tensor_parallel_size=1
)
sampling_params = SamplingParams(temperature=0.7, top_p=0.95)
```

## 3. Observability

- **OpenLIT**: Instrument with OpenLIT for OpenTelemetry tracing.
- **Metrics**: Monitor token generation speed and latency.

### Example: Instrumentation

#### Good

```python
from openlit import openlit
openlit.init(service_name="my-llm-service")
# Initialize LLM AFTER OpenLIT
llm = LLM(...)
```
