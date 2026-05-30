---
status: active
---
<!-- Target: docs/05.operations/guides/09-tooling/syncthing.md -->

# Syncthing Usage Guide

<!-- [ID:07-tooling:syncthing] -->

## Overview (KR)

이 문서는 `docs/05.operations/guides/09-tooling/syncthing.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

## Usage
>
> Usage for real-time, secure peer-to-peer file synchronization.

### Overview

Syncthing is the platform's decentralized solution for file synchronization. It allows for secure data replication across infrastructure nodes and personal devices without relying on third-party cloud providers.

### Architecture Context

- **Endpoint**: `https://syncthing.${DEFAULT_URL}`
- **Protocol**: BEP (Block Exchange Protocol)
- **Local Discovery**: UDP Broadcast on port 21027
- **Data Transfer**: TCP/UDP on port 22000

### How-to Procedures

#### 1. Accessing the GUI

1. Navigate to `https://syncthing.${DEFAULT_URL}`.
2. Log in using the platform credentials (`SYNCTHING_USERNAME`).
3. Note your **Device ID** via **Actions** -> **Show ID**.

#### 2. Pairing a New Device

To sync files with another device:

1. Obtain the **Device ID** of the remote device.
2. In the Syncthing GUI, click **Add Remote Device**.
3. Paste the Device ID and give it a recognizable **Device Name**.
4. Click **Save**.
5. On the remote device, a notification will appear; click **Add Device** to confirm the pairing.

#### 3. Sharing the Sync Folder

1. Click **Add Folder** or edit an existing one (e.g., `Default Folder`).
2. Ensure the **Folder Path** is correctly set (usually `/var/syncthing/` or specifically `/Sync` for resource data).
3. In the **Sharing** tab, check the box for the remote device(s) you want to sync with.
4. Click **Save**.
5. The remote device will receive a request to join the folder; accept it to begin synchronization.

### Troubleshooting & Pitfalls

#### "Out of Sync" State

**Symptom**: Folder status shows "Out of Sync" even after recent changes.

**Solution**:

1. Check the **Failed Items** link for specific file errors (e.g., permissions).
2. Use **Actions** -> **Rescan All** to force a file system check.
3. If persistent, refer to the [Procedure](../../runbooks/09-tooling/syncthing.md) for database reset procedures.

#### Connection Failures

**Symptom**: Devices show as "Disconnected".

**Solution**:

1. Ensure port `22000` (TCP/UDP) is open between devices.
2. Verify that **Global Discovery** and **Relaying** are enabled if devices are on different networks.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- AI Agent

### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

## Common Checks

- Step-by-step Instructions 의 검증 단계를 따른다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/09-tooling/syncthing.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/09-tooling/syncthing.md)
- [Recovery runbook](../../runbooks/09-tooling/syncthing.md)
