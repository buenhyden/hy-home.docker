# Runbook: Docker Resource Maintenance

> **Component**: `docker-engine`
> **Profile**: N/A (Global)
> **Severity**: LOW (Cleanup)

## 1. Description

Procedures for reclaiming disk space and managing the WSL2 `.vhdx` growth by pruning unused Docker resources.

## 2. Steps

### 2.1. Standard Cleanup

Remove stopped containers, unused networks, and dangling images.

```bash
docker system prune -f
```

### 2.2. Deep Volume Cleanup
>
> [!CAUTION]
> This removes UNUSED volumes. Ensure no valuable data is sitting in a stopped container's volume.

```bash
docker system prune -a --volumes -f
```

### 2.3. WSL2 VHDX Compression (Windows Only)

After pruning Docker, the WSL virtual disk (`ext4.vhdx`) does not automatically shrink on the Windows host.

1. Stop WSL: `wsl --shutdown`
2. Open PowerShell as Admin.
3. Use DiskPart or `wsl --manage`:

   ```powershell
   # Modern way
   wsl --manage <distro_name> --set-sparse true
   ```

## 3. Frequency

Recommended monthly or when host disk space falls below 10%.
