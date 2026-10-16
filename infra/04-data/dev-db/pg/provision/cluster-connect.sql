\set ON_ERROR_STOP on
-- Operator-only: first record current consumers, database ACLs and exact rollback.
-- This explicit acknowledgement is not approval or proof of consumer discovery.
\if :{?reviewed_connect_consumers}
\else
\echo 'reviewed_connect_consumers is required; no ACL change performed'
SELECT 'cluster_connect_review_required'::integer;
\endif
SELECT :'reviewed_connect_consumers' = 'reviewed' AS consumer_reviewed \gset
\if :consumer_reviewed
\else
SELECT 'cluster_connect_review_required'::integer;
\endif
BEGIN;
SET LOCAL lock_timeout = '10s';
SET LOCAL statement_timeout = '30s';
DO $admin$
BEGIN
 IF current_database()<>'postgres' OR NOT EXISTS
    (SELECT 1 FROM pg_roles WHERE rolname=current_user AND rolsuper)
 THEN RAISE EXCEPTION 'cluster_connect_admin_required'; END IF;
 IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname='dev_pg_monitor'
      AND shobj_description(oid,'pg_authid') IS DISTINCT FROM 'dev-pg:development:monitor')
 THEN RAISE EXCEPTION 'monitor_role_ownership_mismatch'; END IF;
END $admin$;
-- Preserve owners and all explicit grants; only the inherited PUBLIC path changes.
REVOKE CONNECT ON DATABASE postgres, template1 FROM PUBLIC;
SELECT 'GRANT CONNECT ON DATABASE postgres TO dev_pg_monitor'
 WHERE EXISTS (SELECT 1 FROM pg_roles WHERE rolname='dev_pg_monitor') \gexec
COMMIT;
