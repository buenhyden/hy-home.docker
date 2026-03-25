# Local LLM Setup Guide

How to pull, test, and use language models with the local Ollama engine.

## 1. Prerequisites
- Docker stack must be running (`ollama` service active).
- GPU acceleration should be verified (`nvidia-smi` working on host).

## 2. Pulling Models
Execute the following to download a model (e.g., Llama 3):
```bash
docker exec -it ollama ollama pull llama3
```

## 3. Verification
Verify the model is loaded and responding:
```bash
docker exec -it ollama ollama run llama3 "Hello, how are you?"
```

## 4. Integration with Open WebUI
Once pulled, the model will automatically appear in the [Open WebUI](https://chat.${DEFAULT_URL}) selection dropdown.
