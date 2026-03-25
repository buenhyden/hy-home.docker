# GPU Recovery Runbook

Procedures for restoring NVIDIA GPU acceleration if containers fail to detect the hardware.

## 1. Symptom
- Ollama logs show "CPU only" or "Failed to load NVIDIA driver".
- `nvidia-smi` fails inside the container.

## 2. Verification Steps (Host)
Check if the NVIDIA Container Toolkit is healthy:
```bash
nvidia-smi
docker run --rm --runtime=nvidia --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
```

## 3. Recovery Procedure
1. **Restart Docker Service**:
   ```bash
   sudo systemctl restart docker
   ```
2. **Recreate Container**:
   ```bash
   docker-compose down ollama
   docker-compose up -d ollama
   ```
3. **Verify Reservation**: Check `docker inspect ollama` and look for `DeviceRequests`.

## 4. Escalation
If hardware failure is suspected, check host kernel logs:
```bash
dmesg | grep -i nvidia
```
