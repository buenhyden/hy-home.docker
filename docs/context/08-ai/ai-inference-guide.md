# AI Inferencing & UI Guide

> **Components**: `ollama`, `open-webui`
> **Internal Port**: `11434` (Ollama), `8080` (WebUI)

## 1. LLM Infrastructure Overview

The local AI stack provides private inference capabilities. Ollama serves the models, and Open-WebUI provides the graphical consumer interface.

- **Internal API**: `http://ollama:11434`
- **Dashboard**: `https://chat.${DEFAULT_URL}`

## 2. Hardware Acceleration Initialization

To achieve usable inference speeds, GPU passthrough must be enabled.

### NVIDIA Setup

Ensure `nvidia-container-toolkit` is present on the host. The `reservations` block in the compose file must be active for the GPU to be visible within the container.

### Local Initialization

Upon first run, the Ollama container is empty. Pull a model manually or via the UI:

```bash
docker exec -it ollama ollama run llama3:8b
```

## 3. UI Configuration

Open-WebUI connects to Ollama via the internal Docker DNS. Verify the connection in **Settings -> Connections** using the internal URL `http://ollama:11434`.

## 4. Resource Usage

LLMs consume significant memory. Monitor host RAM during inference; a 7B-8B parameter model typically requires 6GB-8GB of dedicated video or system memory.
