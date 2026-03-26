<!-- [ID:07-tooling:syncthing] -->
# Syncthing System Guide

> Guide for real-time, secure peer-to-peer file synchronization.

## Overview

Syncthing is the platform's decentralized solution for file synchronization. It allows for secure data replication across infrastructure nodes and personal devices without relying on third-party cloud providers.

## Architecture Context

- **Endpoint**: `https://syncthing.${DEFAULT_URL}`
- **Protocol**: BEP (Block Exchange Protocol)
- **Local Discovery**: UDP Broadcast on port 21027
- **Data Transfer**: TCP/UDP on port 22000

## How-to Procedures

### 1. Accessing the GUI

1. Navigate to `https://syncthing.${DEFAULT_URL}`.
2. Log in using the platform credentials (`SYNCTHING_USERNAME`).
3. Note your **Device ID** via **Actions** -> **Show ID**.

### 2. Pairing a New Device

To sync files with another device:

1. Obtain the **Device ID** of the remote device.
2. In the Syncthing GUI, click **Add Remote Device**.
3. Paste the Device ID and give it a recognizable **Device Name**.
4. Click **Save**.
5. On the remote device, a notification will appear; click **Add Device** to confirm the pairing.

### 3. Sharing the Sync Folder

1. Click **Add Folder** or edit an existing one (e.g., `Default Folder`).
2. Ensure the **Folder Path** is correctly set (usually `/var/syncthing/` or specifically `/Sync` for resource data).
3. In the **Sharing** tab, check the box for the remote device(s) you want to sync with.
4. Click **Save**.
5. The remote device will receive a request to join the folder; accept it to begin synchronization.

## Troubleshooting & Pitfalls

### "Out of Sync" State

**Symptom**: Folder status shows "Out of Sync" even after recent changes.

**Solution**: 

1. Check the **Failed Items** link for specific file errors (e.g., permissions).
2. Use **Actions** -> **Rescan All** to force a file system check.
3. If persistent, refer to the [Runbook](../../09.runbooks/09-tooling/syncthing.md) for database reset procedures.

### Connection Failures

**Symptom**: Devices show as "Disconnected".

**Solution**:

1. Ensure port `22000` (TCP/UDP) is open between devices.
2. Verify that **Global Discovery** and **Relaying** are enabled if devices are on different networks.

## Related References

- **Infrastructure**: [Syncthing Service](../../../infra/09-tooling/syncthing/README.md)
- **Operation**: [Syncthing Operations Policy](../../08.operations/09-tooling/syncthing.md)
- **Runbook**: [Syncthing Runbook](../../09.runbooks/09-tooling/syncthing.md)
