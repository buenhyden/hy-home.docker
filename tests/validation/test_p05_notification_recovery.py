"""Immutable SQL source boundaries and reusable real-PostgreSQL recovery checks.

The ordinary suite does not start a database. ``RecoverySQLProbe.run`` must be
called only inside the separately authorized, owned synthetic PostgreSQL fixture.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import time
import unittest
from pathlib import Path

from tests.validation.test_opsflow_database_rehearsal import publish_sql

ROOT = Path(__file__).resolve().parents[2]
SQL = ROOT / "infra/07-workflow/airflow/workloads/manifest-pipeline/sql"
MIGRATION = SQL / "007_notification_recovery.sql"
CHECKS = SQL / "008_checks.sql"
PREDECESSORS = {
    "001_opsflow.sql": "82a4762a8962832c7fdd05826df3b97cf02cc4f96c974a328e42e4493143b18f",
    "002_checks.sql": "7ed4bfd5f160e93ad810e8d32ce2221a02f1629946e5e4297817385acbbb13ed",
    "003_business_date.sql": "830b62c6e8d175d5a4350bab27976121637df4aeca6688748865756be2d84d72",
    "004_notification_quarantine.sql": "ad8176d875b75c15d0e7bfc21c1cb67cd5b31240a4901bccec5b8bb0d931bde9",
    "005_data_version.sql": "85eb63d22f2967ac84996f561a14ca3433e429eaf55a597d294478e21dfe00c2",
    "006_checks.sql": "38eb6b22e99e573c40cd1fa920af7a3cc5945d0ce0a53e9d2872983834c0ef76",
}


class RecoverySourceTests(unittest.TestCase):
    def test_predecessors_are_immutable(self):
        for name, digest in PREDECESSORS.items():
            with self.subTest(name=name):
                self.assertEqual(
                    digest, hashlib.sha256((SQL / name).read_bytes()).hexdigest()
                )

    def test_migration_and_independent_checker_are_present(self):
        self.assertTrue(
            MIGRATION.is_file(), "approved v4-to-v5 recovery migration missing"
        )
        self.assertTrue(CHECKS.is_file(), "independent v5 checker missing")
        migration = MIGRATION.read_text()
        checks = CHECKS.read_text()
        self.assertTrue(migration.startswith("\\set ON_ERROR_STOP on\n"))
        self.assertTrue(migration.rstrip().endswith("COMMIT;"))
        self.assertIn(PREDECESSORS["005_data_version.sql"], migration)
        self.assertIn("BEGIN READ ONLY;", checks)
        self.assertTrue(checks.rstrip().endswith("ROLLBACK;"))


class RecoverySQLProbe:
    """Exercise actual stored functions through an existing authorized fixture.

    This deliberately owns no Docker lifecycle. Its clean v5 database must not
    be reused for historical C22 exact-row-count scenarios without resetting it.
    All values below are synthetic; only closed assertions leave the fixture.
    """

    def __init__(self, fixture):
        self.fixture = fixture
        self.check = unittest.TestCase()

    def query(self, sql, role="p04_audit"):
        if role == "opsflow_migrator":
            sql = "SET ROLE opsflow_owner;" + sql
        result = self.fixture.psql(role, "opsflow_dev", sql)
        return (
            result.stdout.decode().strip()
            if isinstance(result.stdout, bytes)
            else result.stdout.strip()
        )

    def reject(self, sql, role="opsflow_migrator", code="P0001"):
        if role == "opsflow_migrator":
            sql = "SET ROLE opsflow_owner;" + sql
        result = self.fixture.psql(role, "opsflow_dev", sql, check=False)
        self.check.assertNotEqual(0, result.returncode)
        stderr = (
            result.stderr.decode()
            if isinstance(result.stderr, bytes)
            else result.stderr
        )
        self.check.assertIn(code, stderr)

    def row(self, item):
        return self.query(
            "SELECT state||'|'||attempts||'|'||attempt_limit||'|'||"
            f"coalesce(last_error_code,'') FROM ops_flow.outbox WHERE id={item};"
        )

    @staticmethod
    def call(name, item, attempt, request, evidence="a" * 64):
        # All callers below use fixed synthetic scalars, never request payloads.
        return (
            f"SELECT ops_flow.{name}({item},{attempt},'{request}'::uuid,'{evidence}');"
        )

    def publish(self, sequence):
        digest = hashlib.sha256(f"p05-recovery-{sequence}".encode()).hexdigest()
        run, sql = publish_sql(
            "hy-home.docker", digest, f"2026-11-{sequence:02d}T00:00:00Z"
        )
        self.check.assertEqual("published", self.query(sql, "opsflow_ingest"))
        item = self.query(f"SELECT id FROM ops_flow.outbox WHERE run_id='{run}';")
        self.check.assertTrue(item.isdecimal())
        return item

    def claim_and_retry(self, item):
        sql = (
            "SELECT id AS cid,lease_token::text AS ctok FROM ops_flow.claim_notification() \\gset\n"
            "SELECT :'cid'||'|'||ops_flow.retry_not_sent_notification(:'cid'::bigint,:'ctok'::uuid);"
        )
        self.check.assertEqual(f"{item}|true", self.query(sql, "opsflow_notifier"))

    def exhaust_default(self):
        item = self.publish(1)
        self.check.assertEqual(
            "5",
            self.query(f"SELECT attempt_limit FROM ops_flow.outbox WHERE id={item};"),
        )
        for attempt in range(1, 6):
            self.claim_and_retry(item)
            expected = "dead" if attempt == 5 else "retry"
            self.check.assertEqual(
                f"{expected}|{attempt}|5|smtp_not_started", self.row(item)
            )
            self.check.assertEqual(
                "0",
                self.query(
                    "SELECT count(*) FROM ops_flow.claim_notification();",
                    "opsflow_notifier",
                ),
            )
            self.query(
                f"UPDATE ops_flow.outbox SET next_attempt_at=clock_timestamp() WHERE id={item};"
            )
        return item

    def permissions(self, item):
        for role in ("opsflow_ingest", "opsflow_notifier", "opsflow_reader"):
            for name in (
                "requeue_dead_notification",
                "quarantine_restored_notification",
            ):
                sql = self.call(name, item, 5, "10000000-0000-0000-0000-000000000001")
                self.reject(sql, role, "42501")
            self.reject(
                "SELECT 1 FROM ops_flow.notification_recovery_audit;", role, "42501"
            )
        # SET ROLE owner does not convert an unrelated session into the operator.
        self.reject(
            "SET ROLE opsflow_owner;"
            + self.call(
                "requeue_dead_notification",
                item,
                5,
                "10000000-0000-0000-0000-000000000002",
            ),
            "p04_audit",
        )

    def parallel_conflict(self, item):
        request = "15000000-0000-0000-0000-000000000001"
        locks = (
            f"SELECT id FROM ops_flow.outbox WHERE id={item} FOR UPDATE;",
            "SELECT pg_advisory_xact_lock(hashtextextended("
            f"'opsflow:notification-recovery:{request}',0));",
        )
        for lock in locks:
            script = "BEGIN;" + lock + "/*p05_recovery_lock*/SELECT pg_sleep(5);COMMIT;"
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                holder = executor.submit(self.query, script)
                ready = False
                for _ in range(40):
                    observed = self.query(
                        "SELECT count(*) FROM pg_stat_activity "
                        "WHERE query LIKE '/*p05_recovery_lock*/%' AND wait_event='PgSleep';"
                    )
                    if observed == "1":
                        ready = True
                        break
                    time.sleep(0.05)
                self.check.assertTrue(
                    ready, "owned PostgreSQL lock barrier not observed"
                )
                self.reject(self.call("requeue_dead_notification", item, 5, request))
                holder.result()
        self.check.assertEqual("dead|5|5|smtp_not_started", self.row(item))

    def one_approval(self, item):
        request = "20000000-0000-0000-0000-000000000001"
        sql = self.call("requeue_dead_notification", item, 5, request)
        self.check.assertEqual("t", self.query(sql, "opsflow_migrator"))
        self.check.assertEqual("retry|5|6|smtp_not_started", self.row(item))
        self.check.assertEqual("t", self.query(sql, "opsflow_migrator"))
        self.check.assertEqual(
            "1",
            self.query("SELECT count(*) FROM ops_flow.notification_recovery_audit;"),
        )
        self.reject(self.call("requeue_dead_notification", item, 5, request, "b" * 64))
        self.reject(
            self.call(
                "requeue_dead_notification",
                item,
                5,
                "20000000-0000-0000-0000-000000000002",
            )
        )
        self.check.assertEqual("retry|5|6|smtp_not_started", self.row(item))

    def restored_sending(self, item):
        self.check.assertEqual(
            item,
            self.query(
                "SELECT id FROM ops_flow.claim_notification();", "opsflow_notifier"
            ),
        )
        self.check.assertEqual("sending|6|6|smtp_not_started", self.row(item))
        self.check.assertEqual(
            "t",
            self.query(
                f"SELECT lease_until>clock_timestamp() FROM ops_flow.outbox WHERE id={item};"
            ),
        )
        request = "30000000-0000-0000-0000-000000000001"
        self.reject(self.call("requeue_dead_notification", item, 6, request))
        sql = self.call("quarantine_restored_notification", item, 6, request)
        self.check.assertEqual("t", self.query(sql, "opsflow_migrator"))
        self.check.assertEqual("t", self.query(sql, "opsflow_migrator"))
        self.check.assertEqual("unknown|6|6|restored_delivery_unknown", self.row(item))
        self.check.assertEqual(
            "t",
            self.query(
                f"SELECT lease_token IS NULL AND lease_until IS NULL FROM ops_flow.outbox WHERE id={item};"
            ),
        )
        self.check.assertEqual(
            "0",
            self.query(
                "SELECT count(*) FROM ops_flow.claim_notification();",
                "opsflow_notifier",
            ),
        )
        self.reject(
            self.call(
                "requeue_dead_notification",
                item,
                6,
                "30000000-0000-0000-0000-000000000002",
            )
        )
        self.reject(
            self.call(
                "quarantine_restored_notification",
                item,
                6,
                "30000000-0000-0000-0000-000000000003",
            )
        )
        self.check.assertEqual(
            "t",
            self.query(
                f"SELECT ops_flow.reconcile_notification({item},'not_sent','{'c' * 64}');",
                "opsflow_migrator",
            ),
        )
        self.check.assertEqual("dead|6|6|reconciled_no_send", self.row(item))

    def repeated_approval_and_sent(self, item):
        sql = self.call(
            "requeue_dead_notification", item, 6, "40000000-0000-0000-0000-000000000001"
        )
        self.check.assertEqual("t", self.query(sql, "opsflow_migrator"))
        self.check.assertEqual("retry|6|7|reconciled_no_send", self.row(item))
        accepted = (
            "SELECT id AS cid,lease_token::text AS ctok FROM ops_flow.claim_notification() \\gset\n"
            "SELECT :'cid'||'|'||ops_flow.ack_notification(:'cid'::bigint,:'ctok'::uuid);"
        )
        self.check.assertEqual(f"{item}|true", self.query(accepted, "opsflow_notifier"))
        self.check.assertEqual(
            "accepted_by_smtp|7|7|reconciled_no_send", self.row(item)
        )
        self.reject(
            self.call(
                "requeue_dead_notification",
                item,
                7,
                "40000000-0000-0000-0000-000000000002",
            )
        )
        self.reject(
            self.call(
                "quarantine_restored_notification",
                item,
                7,
                "40000000-0000-0000-0000-000000000003",
            )
        )
        # Replaying the original approval after delivery cannot grant attempt8.
        self.check.assertEqual("t", self.query(sql, "opsflow_migrator"))
        self.check.assertEqual(
            "7",
            self.query(f"SELECT attempt_limit FROM ops_flow.outbox WHERE id={item};"),
        )

    def insufficient_proof_and_overflow(self):
        item = self.publish(2)
        self.query(
            f"UPDATE ops_flow.outbox SET attempts=5,state='retry' WHERE id={item};"
        )
        self.check.assertEqual(
            "0",
            self.query(
                "SELECT count(*) FROM ops_flow.claim_notification();",
                "opsflow_notifier",
            ),
        )
        self.check.assertEqual("dead|5|5|retry_exhausted", self.row(item))
        request = "50000000-0000-0000-0000-000000000001"
        self.reject(self.call("requeue_dead_notification", item, 5, request))
        self.query(
            f"UPDATE ops_flow.outbox SET last_error_code='reconciled_no_send' WHERE id={item};"
        )
        self.reject(self.call("requeue_dead_notification", item, 5, request))
        self.query(
            f"UPDATE ops_flow.outbox SET attempts=2147483647,attempt_limit=2147483647,last_error_code='smtp_not_started' WHERE id={item};"
        )
        self.reject(self.call("requeue_dead_notification", item, 2147483647, request))
        self.check.assertEqual(
            "2147483647|2147483647",
            self.query(
                f"SELECT attempts||'|'||attempt_limit FROM ops_flow.outbox WHERE id={item};"
            ),
        )
        # Large lifetime counts are synthetic admin fixtures, not extra grants.
        self.query(
            f"UPDATE ops_flow.outbox SET attempts=32,attempt_limit=32 WHERE id={item};"
        )
        sql = self.call("requeue_dead_notification", item, 32, request)
        self.check.assertEqual("t", self.query(sql, "opsflow_migrator"))
        self.claim_and_retry(item)
        self.check.assertEqual("dead|33|33|smtp_not_started", self.row(item))
        self.check.assertEqual(
            "t",
            self.query(
                "SELECT next_attempt_at BETWEEN clock_timestamp()+interval '897 seconds' "
                f"AND clock_timestamp()+interval '901 seconds' FROM ops_flow.outbox WHERE id={item};"
            ),
        )
        request = "50000000-0000-0000-0000-000000000002"
        self.query(
            "BEGIN;"
            + self.call("requeue_dead_notification", item, 33, request)
            + "ROLLBACK;",
            "opsflow_migrator",
        )
        self.check.assertEqual("dead|33|33|smtp_not_started", self.row(item))
        self.check.assertEqual(
            "0",
            self.query(
                f"SELECT count(*) FROM ops_flow.notification_recovery_audit WHERE request_id='{request}'::uuid;"
            ),
        )

    def invalid_inputs(self):
        args = (
            "NULL,5,'60000000-0000-0000-0000-000000000001'," + "'a'",
            "1,NULL,'60000000-0000-0000-0000-000000000001','" + "a" * 64 + "'",
            "1,5,NULL,'" + "a" * 64 + "'",
            "1,5,'00000000-0000-0000-0000-000000000000','" + "a" * 64 + "'",
            "1,5,'60000000-0000-0000-0000-000000000001',NULL",
        )
        for name in ("requeue_dead_notification", "quarantine_restored_notification"):
            for values in args:
                self.reject(f"SELECT ops_flow.{name}({values});")

    def run(self):
        self.check.assertEqual("0", self.query("SELECT count(*) FROM ops_flow.outbox;"))
        item = self.exhaust_default()
        self.permissions(item)
        self.parallel_conflict(item)
        self.one_approval(item)
        self.restored_sending(item)
        self.repeated_approval_and_sent(item)
        self.insufficient_proof_and_overflow()
        self.invalid_inputs()
        return {
            name: "PASS"
            for name in (
                "default_five_attempts",
                "operator_only",
                "single_attempt_approval",
                "idempotent_request",
                "conflicting_request_denied",
                "restored_unexpired_unknown",
                "unknown_and_sent_denied",
                "reconciled_proof_required",
                "lifetime_attempts_preserved",
                "integer_overflow_denied",
                "invalid_input_denied",
                "large_attempt_backoff_capped",
                "approval_transaction_rollback",
                "parallel_recovery_conflict_denied",
            )
        }


if __name__ == "__main__":
    unittest.main()
