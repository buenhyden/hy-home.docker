# AI Stack Setup Guide

> Deployment and interconnection strategies for the local AI inferencing and UI stack.

## 1. Description

The local AI ecosystem runs entirely privately leveraging `infra/08-ai/`. We use **Ollama** as the underlying LLM executor, mapping hardware APIs directly, and **Open-WebUI** as a ChatGPT-like graphical frontend for users to interact with downloaded models.

## 2. Hardware Acceleration Initialization

> [!WARNING]
> Without specific docker runtimes, Ollama will execute strictly on the CPU, resulting in abysmal inference speeds.

- If utilizing NVIDIA graphics, ensure `nvidia-container-toolkit` is correctly installed on the host and the `deploy.resources.reservations.devices.driver=nvidia` block is un-commented inside `infra/08-ai/ollama/docker-compose.yml`.
- If running under WSL, Windows allows GPU passthrough natively without specialized container toolkits provided Docker Desktop is set up accurately.

## 3. Downloading LLM Models

The `ollama` container starts empty. To use it, you must explicitly pull a model into its storage volume.

1. Jump into the container:

```bash
docker exec -it ollama sh
```

1. Pull a model (e.g., llama3, mistral, gemma):

```bash
ollama run llama3:8b
```

1. A test prompt will appear indicating the model is downloaded and ready for API queries.

## 4. Open-WebUI Configuration

Open-WebUI natively networks with Ollama to detect available models.

1. Access the dashboard via `https://chat.${DEFAULT_URL}`.
2. Complete the initial admin registration.
3. If no models appear in the top-left dropdown, navigate to `Settings -> Connections` and ensure the Ollama API URL is strictly `http://ollama:11434` (the internal Docker DNS name, not localhost).
4. Utilize the **Admin Panel -> Models** interface to pull models graphically without needing terminal `docker exec` interventions moving forward.
