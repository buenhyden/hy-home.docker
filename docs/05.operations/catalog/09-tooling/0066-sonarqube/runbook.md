---
title: "SonarQube Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0066"
parent_ids:
- "GDE-0066"
created: "2026-05-17"
---

# SonarQube Runbook

## When to Use

Use for health failure, DB connection failure, background-task backlog, search
index failure, token/auth incident, database restore, or an approved upgrade.

## Procedure

1. From the repository root validate and capture bounded state:

   ```bash
   docker compose --profile sast config --quiet
   docker compose --profile sast ps sonarqube
   docker compose --profile sast logs --tail=200 sonarqube
   ```

2. Separate gateway auth, SonarQube app auth/token, DB connectivity, compute
   engine queue, and search-index symptoms. Redact user/source/token data.
3. Verify the management PostgreSQL service and free space through its owner.
   Do not run `psql` inside SonarQube; the image does not declare that client.
4. Restart only SonarQube after DB/storage checks. Verify system health, gateway
   entry, SonarQube permission, and one representative background task.
5. For token compromise, revoke the token in SonarQube, rotate the owning CI
   secret, and verify the old token is denied. IdP account disablement alone is
   insufficient.

### Database restore and index recovery

1. Stop SonarQube and keep it stopped so no DB writes occur.
2. Restore a verified database-native backup to an isolated PostgreSQL target.
   Preserve the source DB and record backup/checksum/schema/source version.
3. Start an isolated SonarQube instance of the matching version against the
   restored DB with a fresh/empty local search-index path. Do not delete the
   active production index as diagnosis.
4. Allow reindexing, then verify project/settings/user counts, permissions,
   representative search, and one analysis. Promote only after approval.

### Upgrade and rollback

1. Verify the pre-upgrade DB backup and plugin/config inventory; review every
   release note and prerequisite. Ensure migration headroom based on measured DB disk.
2. Test the target image against an isolated restored DB, including reindex and
   scanner compatibility.
3. Upgrade the active instance only with rollback approval. On failure, stop it,
   restore the pre-upgrade DB, and start the prior image. Never point the prior
   image at a DB already migrated by the target release.

## Evidence

Record command exits, image/source commit, DB backup/checksum/schema, project and
task counts, health/index status, plugin inventory, and final disposition. Never
record DB contents, source code, personal data, or tokens.

## Rollback or Recovery

Database restore/reindex and upgrade rehearsal are **planned but unexecuted**.
Search index deletion without a verified database recovery point is prohibited.

## Escalation

Stop on missing/unverified DB backup, migration ambiguity, DB corruption, unknown
plugin compatibility, persistent queue/index failure, or authorization bypass.

## Traceability

- [Guide](guide.md) (`GDE-0066`)
- [Policy](policy.md) (`POL-0066`)
- [SonarQube Compose](../../../../../infra/09-tooling/sonarqube/docker-compose.yml)

## Related Documents

- [SonarQube backup/restore](https://docs.sonarsource.com/sonarqube-server/9.9/instance-administration/backup-and-restore)
- [SonarQube upgrade](https://docs.sonarsource.com/sonarqube-server/9.8/setup-and-upgrade/upgrade-the-server/upgrade-guide)
