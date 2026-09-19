---
title: "k6 Load Test Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0061"
parent_ids:
- "GDE-0061"
created: "2026-05-17"
---

# k6 Load Test Recovery Runbook

## When to Use

Use this procedure when k6 targets the wrong endpoint, breaches an agreed limit,
fails to export results, or exits unexpectedly. Commands run from the repository
root and name only `k6`.

## Procedure

1. Stop new load first:

   ```bash
   docker compose --profile testing stop k6
   docker compose --profile testing ps k6
   ```

2. Confirm target recovery using target-side latency, error, and saturation
   signals. Do not restart while impact remains unexplained.
3. Capture sanitized job evidence:

   ```bash
   docker compose --profile testing logs --tail=200 k6
   ```

   Record target, `K6_SCRIPT`, `K6_TESTID`, image declaration, start/stop time,
   exit code, and target recovery. Do not record credentials or response bodies.
4. If metrics are absent, check the configured remote-write endpoint and the
   receiving Prometheus before changing the scenario. Local job completion does
   not prove result retention.
5. If a scenario or image change caused the failure, restore the last reviewed
   Git version, run the static checks, and use a disposable low-load target before
   seeking approval to repeat the real test.

### Verification

```bash
bash scripts/hardening/check-all-hardening.sh 09-tooling
HYHOME_COMPOSE_PROFILES=testing bash scripts/validation/validate-docker-compose.sh
```

Recovery is complete only when k6 is stopped or exited, target signals have
returned to the agreed range, and retained evidence identifies whether results
reached Prometheus.

### Backup and Recovery Status

No persistent job-container restore exists. Version-controlled scripts are
restored from Git; retained metrics are recovered under the Prometheus backup
procedure. This procedure is planned documentation and was not executed during
the 2026-09-20 correction.

## Evidence

Record the approval, target, scenario commit, test ID, image declaration,
timestamps, exit code, sanitized summary, result-retention status, and target-side
recovery. Never capture credentials or response bodies.

## Rollback or Recovery

Stop the job, restore scenarios from the last reviewed Git commit, and recover
retained metrics under the receiving Prometheus procedure. Re-run only against a
disposable target before seeking authorization for the original target.

## Escalation

Escalate when the job cannot be stopped, traffic continues after stop, target
signals do not recover, credentials may be exposed, or result retention is
needed but the receiving backend is unavailable.

## Traceability

- Declared parent: [k6 Usage Guide](guide.md) (`GDE-0061`)
- Governing authority: [Tooling Tier Architecture Description](../../../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- Subject peers: [Guide](guide.md), [Policy](policy.md)

## Related Documents

- [k6 Compose source](../../../../../infra/09-tooling/k6/docker-compose.yml)
- [Derived Compose image projection](../../../../../infra/tech-stack.versions.json)
- [k6 results output](https://grafana.com/docs/k6/latest/results-output/)
- [Operations index](../../../README.md)
