# Troubleshooting: WSL2 Clock Drift and Observability Alerts

## Symptom

You may receive repeated alerts for **PrometheusTooManyRestarts** or **LokiProcessTooManyRestarts**, even though the services are stable and strict `docker ps` shows no restarts.

Example Alert:
> Alert: Prometheus too many restarts (instance localhost:9090) - warning
> Description: 프로메테우스가 5분 내 2회 이상 재시작했습니다.

## Root Cause

This is caused by a known issue in **WSL2 (Windows Subsystem for Linux 2)** where the VM's system clock drifts significantly from the host hardware clock (often by several seconds per minute) when the host sleeps or under heavy load.

Prometheus calculates restarts by monitoring the `process_start_time_seconds` metric. If the system clock drifts, this timestamp (relative to the epoch) appears to change constantly, triggering the `changes()` function in alert rules.

## Solutions

### 1. Robust Alert Rules (Recommended)

We have updated the alert rules to use `resets()` on the **derived uptime** instead of tracking the start timestamp directly. This method is immune to clock drift.

**Old Pattern (Fragile):**

```yaml
expr: changes(process_start_time_seconds{job="..."}[5m]) > 2
```

**New Pattern (Robust):**

```yaml
expr: resets((time() - process_start_time_seconds{job="..."})[5m:15s]) > 2
```

### 2. Fix WSL2 Clock Sync

If you need accurate time for logs or other applications, you can force a clock sync.

**Option A: One-time Sync (Requires Admin/Privileged)**
Run this command in WSL2 (if `hwclock` is available or via Alpine container):

```bash
docker run --rm --privileged alpine hwclock -s
```

**Option B: Restart WSL2**
In PowerShell (Host):

```powershell
wsl --shutdown
```

Then restart your Docker Desktop or WSL distribution.

## Verification

To verify the fix, query the robust metric in Prometheus:
`resets((time() - process_start_time_seconds{job='loki'})[5m:15s])`

This should return `0` (or empty) if the service is stable, regardless of clock drift.
