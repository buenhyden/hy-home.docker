# Ollama AI Inference Blueprint

> **Component**: `ollama`
> **Engine**: NVIDIA Container Toolkit (GPU)
> **Endpoint**: `ollama:11434`

## 1. Inference Infrastructure

Ollama provides local LLM inference capabilities, exposed via a standard REST API.

### Technical Specifications

| Attribute | Value |
| --- | --- |
| **Internal DNS** | `ollama` |
| **Main Port** | `11434` |
| **Exporter Port** | `9735` |
| **Static IP** | `172.19.0.40` |
| **External URL** | `https://ollama.${DEFAULT_URL}` |

## 2. Hardware Acceleration

The service is configured to use host GPU resources via the `nvidia` driver.

| Level | Configuration |
| --- | --- |
| **Device** | `all` |
| **Capability** | `[gpu]` |
| **Profile** | Required: `ollama` |

## 3. Monitoring & Verification

Ollama metrics are collected by `ollama-exporter` and scraped by the LGTM stack.

### Verification Steps

```bash
# Check if Ollama is responsive
docker exec ollama ollama list

# Check GPU utilization (from host)
nvidia-smi
```
