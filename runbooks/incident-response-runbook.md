# Incident Response Runbook

## 1. Document Purpose

Standard response process for production incidents with clear roles and cadence.

## 2. Prerequisites

- Access Requirements: Incident channel, service dashboards, deployment controls
- Tools: Incident tracker/document, alerting and observability tools

## 3. Execution Steps

### Phase P1: Declare and Staff

1. Classify severity.
   - **SEV-1**: Widespread user impact or data loss risk.
   - **SEV-2**: Partial user impact or high-risk dependency failure.
   - **SEV-3**: Limited internal-only impact.
2. Declare incident and assign roles (Incident Commander, Communications Lead, Operations Lead).

   ```bash
   # Create incident document and incident communication channel.
   ```

### Phase P2: Stabilize and Mitigate

1. Assess blast radius and apply immediate mitigation.

   ```bash
   # Execute containment action to reduce user impact under IC authority.
   ```

### Phase P3: Communicate

1. Communicate updates on a fixed cadence based on Severity:
   - **SEV-1**: Every 15 minutes.
   - **SEV-2**: Every 30 minutes.
   - **SEV-3**: Every 60 minutes.

   ```bash
   # Publish status updates detailing current impact, hypothesis, and next update time.
   ```

### Phase P4: Resolve and Verify

1. Resolve and verify recovery.

   ```bash
   # Confirm service health and customer impact recovery.
   ```

## 4. Validation

- Timestamped Event Timeline is captured from detection to resolution (detection, declaration, mitigation start/end, full resolution).
- User impact resolved and verified.
- Required postmortem created when applicable (Mandatory for SEV-1/SEV-2).

## 5. Rollback / Reversal Procedure

- If mitigation fails, roll back using deployment runbook and re-check health.

## 6. Escalation Contacts

- Primary Contact: Incident Commander / On-call
- Secondary Contact: Engineering leadership
