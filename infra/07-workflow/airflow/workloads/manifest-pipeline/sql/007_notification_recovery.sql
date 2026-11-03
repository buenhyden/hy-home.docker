\set ON_ERROR_STOP on
-- V5 grants one explicit no-send reprocess and audits restored-send quarantine.
-- Issued001-006 and the six claim fields remain unchanged.
-- The reviewed caller supplies this file's SHA256; no HOME apply is authorized.
BEGIN;
SET LOCAL search_path = pg_catalog;
SET LOCAL lock_timeout = '10s';
SET LOCAL statement_timeout = '60s';
SELECT pg_catalog.set_config('opsflow.migration_sha256', :'migration_sha256', true);
DO $identity$
DECLARE expected text := pg_catalog.current_setting('opsflow.migration_sha256');
BEGIN
 IF current_database() <> 'opsflow_dev' OR current_user <> 'opsflow_owner'
    OR session_user <> 'opsflow_migrator' OR expected !~ '^[0-9a-f]{64}$'
 THEN RAISE EXCEPTION 'migration_identity_or_checksum'; END IF;
END $identity$;
SELECT pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended('opsflow:migration',0));
LOCK TABLE ops_flow.runs, ops_flow.documents, ops_flow.current_runs, ops_flow.outbox, ops_flow.schema_version IN ACCESS EXCLUSIVE MODE;
DO $preflight$
DECLARE observed text;
BEGIN
 IF (SELECT count(*) FROM ops_flow.schema_version) <> 4
    OR (SELECT count(*) FROM ops_flow.schema_version
        WHERE version=4
          AND migration_sha256='85eb63d22f2967ac84996f561a14ca3433e429eaf55a597d294478e21dfe00c2'
          AND schema_fingerprint ~ '^[0-9a-f]{64}$') <> 1
 THEN RAISE EXCEPTION 'unknown_version_or_v4_receipt'; END IF;
 SELECT pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(pg_catalog.string_agg(signature,'\n' ORDER BY signature),'UTF8')),'hex') INTO observed FROM (
  SELECT 'column:'||c.relname||':'||a.attnum||':'||a.attname||':'||pg_catalog.format_type(a.atttypid,a.atttypmod)||':'||a.attnotnull AS signature
   FROM pg_catalog.pg_class c JOIN pg_catalog.pg_attribute a ON a.attrelid=c.oid
   WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND a.attnum>0 AND NOT a.attisdropped
  UNION ALL SELECT 'function:'||pg_catalog.pg_get_functiondef(p.oid) FROM pg_catalog.pg_proc p WHERE p.pronamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'constraint:'||c.conrelid::pg_catalog.regclass::text||':'||c.contypid::pg_catalog.regtype::text||':'||c.conname||':'||pg_catalog.pg_get_constraintdef(c.oid) FROM pg_catalog.pg_constraint c WHERE c.connamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'type:'||t.typname||':'||pg_catalog.pg_get_userbyid(t.typowner)||':'||t.typtype::text||':'||t.typcategory::text||':'||t.typrelid::pg_catalog.regclass::text||':'||t.typelem::pg_catalog.regtype::text||':'||t.typbasetype::pg_catalog.regtype::text||':'||t.typtypmod||':'||t.typnotnull||':'||COALESCE(t.typdefault,'') FROM pg_catalog.pg_type t WHERE t.typnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'relation:'||c.relname||':'||c.relkind::text||':'||c.relpersistence::text||':'||COALESCE(c.reloptions::text,'')||':'||c.relrowsecurity||':'||c.relforcerowsecurity||':'||pg_catalog.pg_get_userbyid(c.relowner)||':'||CASE WHEN c.relkind IN ('r','p','v','m','f','S') THEN COALESCE((SELECT pg_catalog.jsonb_agg(pg_catalog.jsonb_build_array(pg_catalog.pg_get_userbyid(a.grantor),CASE WHEN a.grantee=0 THEN 'PUBLIC' ELSE pg_catalog.pg_get_userbyid(a.grantee) END,a.privilege_type,a.is_grantable) ORDER BY pg_catalog.pg_get_userbyid(a.grantor),CASE WHEN a.grantee=0 THEN 'PUBLIC' ELSE pg_catalog.pg_get_userbyid(a.grantee) END,a.privilege_type,a.is_grantable) FROM pg_catalog.aclexplode(CASE WHEN c.relacl IS NULL THEN pg_catalog.acldefault(CASE WHEN c.relkind='S' THEN 's'::"char" ELSE 'r'::"char" END,c.relowner) ELSE c.relacl END) a),'[]'::pg_catalog.jsonb)::text ELSE COALESCE(c.relacl::text,'') END FROM pg_catalog.pg_class c WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'rule:'||pg_catalog.pg_get_ruledef(r.oid,true)||':'||r.ev_enabled::text FROM pg_catalog.pg_rewrite r JOIN pg_catalog.pg_class c ON c.oid=r.ev_class WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'column_acl:'||c.relname||':'||a.attnum||':'||COALESCE(a.attacl::text,'') FROM pg_catalog.pg_class c JOIN pg_catalog.pg_attribute a ON a.attrelid=c.oid WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND a.attnum>0 AND NOT a.attisdropped
  UNION ALL SELECT 'trigger:'||pg_catalog.pg_get_triggerdef(t.oid)||':'||t.tgenabled::text FROM pg_catalog.pg_trigger t JOIN pg_catalog.pg_class c ON c.oid=t.tgrelid WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND NOT t.tgisinternal
  UNION ALL SELECT 'policy:'||p.polname||':'||p.polcmd::text||':'||p.polpermissive||':'||p.polroles::text||':'||COALESCE(pg_catalog.pg_get_expr(p.polqual,p.polrelid),'')||':'||COALESCE(pg_catalog.pg_get_expr(p.polwithcheck,p.polrelid),'') FROM pg_catalog.pg_policy p JOIN pg_catalog.pg_class c ON c.oid=p.polrelid WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'sequence:'||c.relname||':'||s.seqtypid::pg_catalog.regtype::text||':'||s.seqstart||':'||s.seqincrement||':'||s.seqmin||':'||s.seqmax||':'||s.seqcache||':'||s.seqcycle FROM pg_catalog.pg_sequence s JOIN pg_catalog.pg_class c ON c.oid=s.seqrelid WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'function_security:'||p.proname||':'||pg_catalog.pg_get_userbyid(p.proowner)||':'||COALESCE(p.proacl::text,'') FROM pg_catalog.pg_proc p WHERE p.pronamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'view:'||c.relname||':'||pg_catalog.pg_get_viewdef(c.oid,true) FROM pg_catalog.pg_class c WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND c.relkind='v'
  UNION ALL SELECT 'index:'||c.relname||':'||pg_catalog.pg_get_indexdef(c.oid) FROM pg_catalog.pg_class c WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND c.relkind='i'
  UNION ALL SELECT 'default:'||c.relname||':'||a.attnum||':'||COALESCE(a.attidentity::text,'')||':'||COALESCE(a.attgenerated::text,'')||':'||COALESCE(pg_catalog.pg_get_expr(d.adbin,d.adrelid),'')
   FROM pg_catalog.pg_class c JOIN pg_catalog.pg_attribute a ON a.attrelid=c.oid LEFT JOIN pg_catalog.pg_attrdef d ON d.adrelid=c.oid AND d.adnum=a.attnum
   WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND a.attnum>0 AND NOT a.attisdropped
  UNION ALL SELECT 'schema:'||n.nspname||':'||pg_catalog.pg_get_userbyid(n.nspowner)||':'||COALESCE(n.nspacl::text,'') FROM pg_catalog.pg_namespace n WHERE n.nspname IN ('ops_flow','public')
  UNION ALL SELECT 'database:'||d.datname||':'||pg_catalog.pg_get_userbyid(d.datdba)||':'||COALESCE(d.datacl::text,'') FROM pg_catalog.pg_database d WHERE d.datname=current_database()
  UNION ALL SELECT 'default_acl:'||d.defaclobjtype::text||':'||COALESCE(n.nspname,'global')||':'||d.defaclacl::text FROM pg_catalog.pg_default_acl d LEFT JOIN pg_catalog.pg_namespace n ON n.oid=d.defaclnamespace WHERE d.defaclrole=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_owner')
  UNION ALL SELECT 'role:'||r.rolname||':'||r.rolcanlogin||':'||r.rolsuper||':'||r.rolcreatedb||':'||r.rolcreaterole||':'||r.rolreplication||':'||r.rolbypassrls FROM pg_catalog.pg_roles r WHERE r.rolname IN ('opsflow_owner','opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader')
  UNION ALL SELECT 'membership:'||pg_catalog.pg_get_userbyid(m.roleid)||':'||pg_catalog.pg_get_userbyid(m.member)||':'||m.admin_option||':'||m.inherit_option||':'||m.set_option FROM pg_catalog.pg_auth_members m WHERE m.roleid IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_owner','opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader')) OR m.member IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_owner','opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader'))
 ) shape;
 IF observed IS DISTINCT FROM (SELECT schema_fingerprint FROM ops_flow.schema_version WHERE version=4)
 THEN RAISE EXCEPTION 'schema_drift'; END IF;
END $preflight$;

ALTER TABLE ops_flow.schema_version DROP CONSTRAINT schema_version_version_check;
ALTER TABLE ops_flow.schema_version ADD CONSTRAINT schema_version_version_check CHECK(version IN (1,2,3,4,5));
ALTER TABLE ops_flow.outbox ADD COLUMN attempt_limit integer NOT NULL DEFAULT 5 CHECK(attempt_limit>=5);
ALTER TABLE ops_flow.outbox DROP CONSTRAINT outbox_attempts_check;
ALTER TABLE ops_flow.outbox ADD CONSTRAINT outbox_attempts_check CHECK(attempts BETWEEN 0 AND attempt_limit);
ALTER TABLE ops_flow.notification_reconciliations DROP CONSTRAINT notification_reconciliations_attempt_check;
ALTER TABLE ops_flow.notification_reconciliations ADD CONSTRAINT notification_reconciliations_attempt_check CHECK(attempt>=1);

CREATE TABLE ops_flow.notification_recovery_audit (
 request_id uuid PRIMARY KEY CHECK(request_id<>'00000000-0000-0000-0000-000000000000'::uuid),
 outbox_id bigint NOT NULL REFERENCES ops_flow.outbox(id),
 attempt integer NOT NULL CHECK(attempt>=1),
 action text NOT NULL CHECK(action IN ('requeue_dead','quarantine_restored')),
 evidence_sha256 text NOT NULL CHECK(evidence_sha256 ~ '^[0-9a-f]{64}$'),
 approved_by name NOT NULL CHECK(approved_by='opsflow_migrator'),
 recorded_at timestamptz NOT NULL DEFAULT pg_catalog.clock_timestamp(),
 UNIQUE(outbox_id,attempt,action)
);
REVOKE ALL ON ops_flow.notification_recovery_audit FROM PUBLIC;

-- Evidence is a digest of a sanitized NONSECRET approval/barrier receipt.
-- The database cannot establish that an SMTP socket or old execution stopped.
-- A matching request is a read-only replay even after its allowance was used.
CREATE FUNCTION ops_flow.requeue_dead_notification(p_id bigint,p_attempt integer,p_request uuid,p_evidence text)
RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog AS $requeue$
DECLARE item ops_flow.outbox%ROWTYPE; prior ops_flow.notification_recovery_audit%ROWTYPE;
BEGIN
 IF session_user<>'opsflow_migrator' OR p_id IS NULL OR p_id<1
    OR p_attempt IS NULL OR p_attempt<1 OR p_attempt>=2147483647
    OR p_request IS NULL OR p_request='00000000-0000-0000-0000-000000000000'::uuid
    OR p_evidence IS NULL OR p_evidence !~ '^[0-9a-f]{64}$'
 THEN RAISE EXCEPTION 'notification_recovery_rejected'; END IF;
 IF NOT pg_catalog.pg_try_advisory_xact_lock(pg_catalog.hashtextextended('opsflow:notification-recovery:'||p_request::text,0))
 THEN RAISE EXCEPTION 'notification_recovery_conflict'; END IF;
 SELECT * INTO prior FROM ops_flow.notification_recovery_audit WHERE request_id=p_request;
 IF FOUND THEN
  IF prior.outbox_id=p_id AND prior.attempt=p_attempt AND prior.action='requeue_dead' AND prior.evidence_sha256=p_evidence
  THEN RETURN true; END IF;
  RAISE EXCEPTION 'notification_recovery_conflict';
 END IF;
 SELECT * INTO item FROM ops_flow.outbox WHERE id=p_id FOR UPDATE NOWAIT;
 IF NOT FOUND OR item.state<>'dead' OR item.attempts<>p_attempt OR item.attempt_limit<>p_attempt
    OR item.last_error_code IS NULL OR item.last_error_code NOT IN ('smtp_not_started','reconciled_no_send')
 THEN RAISE EXCEPTION 'notification_recovery_rejected'; END IF;
 IF item.last_error_code='reconciled_no_send' AND NOT EXISTS (
  SELECT 1 FROM ops_flow.notification_reconciliations
   WHERE outbox_id=p_id AND attempt=p_attempt AND result='not_sent')
 THEN RAISE EXCEPTION 'notification_recovery_rejected'; END IF;
 INSERT INTO ops_flow.notification_recovery_audit(request_id,outbox_id,attempt,action,evidence_sha256,approved_by)
 VALUES(p_request,p_id,p_attempt,'requeue_dead',p_evidence,session_user);
 UPDATE ops_flow.outbox SET state='retry',attempt_limit=p_attempt+1,
  next_attempt_at=pg_catalog.clock_timestamp(),lease_token=NULL,lease_until=NULL
 WHERE id=p_id;
 RETURN true;
EXCEPTION WHEN lock_not_available OR unique_violation THEN
 RAISE EXCEPTION 'notification_recovery_conflict';
END $requeue$;

-- Operator attests the external recovery barrier before clearing even a future
-- lease. This quarantines uncertainty only; it is neither SMTP fencing nor a
-- no-send reconciliation, and grants no retry or additional attempt.
CREATE FUNCTION ops_flow.quarantine_restored_notification(p_id bigint,p_attempt integer,p_request uuid,p_evidence text)
RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog AS $quarantine$
DECLARE item ops_flow.outbox%ROWTYPE; prior ops_flow.notification_recovery_audit%ROWTYPE;
BEGIN
 IF session_user<>'opsflow_migrator' OR p_id IS NULL OR p_id<1
    OR p_attempt IS NULL OR p_attempt<1
    OR p_request IS NULL OR p_request='00000000-0000-0000-0000-000000000000'::uuid
    OR p_evidence IS NULL OR p_evidence !~ '^[0-9a-f]{64}$'
 THEN RAISE EXCEPTION 'notification_recovery_rejected'; END IF;
 IF NOT pg_catalog.pg_try_advisory_xact_lock(pg_catalog.hashtextextended('opsflow:notification-recovery:'||p_request::text,0))
 THEN RAISE EXCEPTION 'notification_recovery_conflict'; END IF;
 SELECT * INTO prior FROM ops_flow.notification_recovery_audit WHERE request_id=p_request;
 IF FOUND THEN
  IF prior.outbox_id=p_id AND prior.attempt=p_attempt AND prior.action='quarantine_restored' AND prior.evidence_sha256=p_evidence
  THEN RETURN true; END IF;
  RAISE EXCEPTION 'notification_recovery_conflict';
 END IF;
 SELECT * INTO item FROM ops_flow.outbox WHERE id=p_id FOR UPDATE NOWAIT;
 IF NOT FOUND OR item.state<>'sending' OR item.attempts<>p_attempt
 THEN RAISE EXCEPTION 'notification_recovery_rejected'; END IF;
 INSERT INTO ops_flow.notification_recovery_audit(request_id,outbox_id,attempt,action,evidence_sha256,approved_by)
 VALUES(p_request,p_id,p_attempt,'quarantine_restored',p_evidence,session_user);
 UPDATE ops_flow.outbox SET state='unknown',last_error_code='restored_delivery_unknown',lease_token=NULL,lease_until=NULL
 WHERE id=p_id;
 RETURN true;
EXCEPTION WHEN lock_not_available OR unique_violation THEN
 RAISE EXCEPTION 'notification_recovery_conflict';
END $quarantine$;
REVOKE ALL ON FUNCTION ops_flow.requeue_dead_notification(bigint,integer,uuid,text),ops_flow.quarantine_restored_notification(bigint,integer,uuid,text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION ops_flow.requeue_dead_notification(bigint,integer,uuid,text),ops_flow.quarantine_restored_notification(bigint,integer,uuid,text) TO opsflow_migrator;

CREATE OR REPLACE FUNCTION ops_flow.claim_notification()
RETURNS TABLE(id bigint,run_id text,source text,row_count integer,lease_token uuid,lease_until timestamptz)
LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog AS $claim$
BEGIN
 UPDATE ops_flow.outbox o SET state='unknown',last_error_code='lease_expired_delivery_unknown',lease_token=NULL,lease_until=NULL
 WHERE o.state='sending' AND o.lease_until<=pg_catalog.clock_timestamp();
 UPDATE ops_flow.outbox o SET state='dead',last_error_code='retry_exhausted'
 WHERE o.attempts>=o.attempt_limit AND o.state IN ('pending','retry');
 RETURN QUERY WITH candidate AS (
  SELECT o.id FROM ops_flow.outbox o WHERE o.attempts<o.attempt_limit
   AND o.state IN ('pending','retry') AND o.next_attempt_at<=pg_catalog.clock_timestamp()
  ORDER BY o.id FOR UPDATE SKIP LOCKED LIMIT 1
 ), claimed AS (
  UPDATE ops_flow.outbox o SET state='sending',attempts=o.attempts+1,lease_token=pg_catalog.gen_random_uuid(),
   lease_until=pg_catalog.clock_timestamp()+interval '10 minutes'
  FROM candidate c WHERE o.id=c.id RETURNING o.id,o.run_id,o.source,o.row_count,o.lease_token,o.lease_until
 ) SELECT c.id,c.run_id,c.source,c.row_count,c.lease_token,c.lease_until FROM claimed c;
END $claim$;

CREATE OR REPLACE FUNCTION ops_flow.retry_not_sent_notification(p_id bigint,p_token uuid)
RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog AS $retry$
DECLARE n integer;
BEGIN
 UPDATE ops_flow.outbox o SET state=CASE WHEN o.attempts>=o.attempt_limit THEN 'dead' ELSE 'retry' END,
  next_attempt_at=pg_catalog.clock_timestamp()+
   (CASE WHEN o.attempts>=5 THEN 900 ELSE 30*pg_catalog.power(2,o.attempts)::integer END)*interval '1 second',
  last_error_code='smtp_not_started',lease_token=NULL,lease_until=NULL
 WHERE o.id=p_id AND o.state='sending' AND o.lease_token=p_token AND o.lease_until>pg_catalog.clock_timestamp();
 GET DIAGNOSTICS n=ROW_COUNT; RETURN n=1;
END $retry$;

CREATE OR REPLACE FUNCTION ops_flow.reconcile_notification(p_id bigint,p_result text,p_evidence text)
RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog AS $reconcile$
DECLARE n integer;
BEGIN
 IF session_user<>'opsflow_migrator' OR p_result IS NULL OR p_result NOT IN ('accepted_by_smtp','not_sent')
    OR p_evidence IS NULL OR p_evidence !~ '^[0-9a-f]{64}$'
 THEN RAISE EXCEPTION 'notification_reconciliation_rejected'; END IF;
 UPDATE ops_flow.outbox o SET
  state=CASE WHEN p_result='accepted_by_smtp' THEN 'accepted_by_smtp' WHEN o.attempts>=o.attempt_limit THEN 'dead' ELSE 'retry' END,
  accepted_at=CASE WHEN p_result='accepted_by_smtp' THEN pg_catalog.clock_timestamp() ELSE NULL END,
  next_attempt_at=pg_catalog.clock_timestamp(),
  last_error_code=CASE WHEN p_result='accepted_by_smtp' THEN 'reconciled_smtp_acceptance' ELSE 'reconciled_no_send' END
 WHERE o.id=p_id AND o.state='unknown';
 GET DIAGNOSTICS n=ROW_COUNT;
 IF n=1 THEN
  INSERT INTO ops_flow.notification_reconciliations(outbox_id,attempt,result,evidence_sha256)
   SELECT o.id,o.attempts,p_result,p_evidence FROM ops_flow.outbox o WHERE o.id=p_id;
 END IF;
 RETURN n=1;
END $reconcile$;

INSERT INTO ops_flow.schema_version SELECT 5,pg_catalog.current_setting('opsflow.migration_sha256'),
 pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(pg_catalog.string_agg(signature,'\n' ORDER BY signature),'UTF8')),'hex')
 FROM (
  SELECT 'column:'||c.relname||':'||a.attnum||':'||a.attname||':'||pg_catalog.format_type(a.atttypid,a.atttypmod)||':'||a.attnotnull AS signature
   FROM pg_catalog.pg_class c JOIN pg_catalog.pg_attribute a ON a.attrelid=c.oid
   WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND a.attnum>0 AND NOT a.attisdropped
  UNION ALL SELECT 'function:'||pg_catalog.pg_get_functiondef(p.oid) FROM pg_catalog.pg_proc p WHERE p.pronamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'constraint:'||c.conrelid::pg_catalog.regclass::text||':'||c.contypid::pg_catalog.regtype::text||':'||c.conname||':'||pg_catalog.pg_get_constraintdef(c.oid) FROM pg_catalog.pg_constraint c WHERE c.connamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'type:'||t.typname||':'||pg_catalog.pg_get_userbyid(t.typowner)||':'||t.typtype::text||':'||t.typcategory::text||':'||t.typrelid::pg_catalog.regclass::text||':'||t.typelem::pg_catalog.regtype::text||':'||t.typbasetype::pg_catalog.regtype::text||':'||t.typtypmod||':'||t.typnotnull||':'||COALESCE(t.typdefault,'') FROM pg_catalog.pg_type t WHERE t.typnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'relation:'||c.relname||':'||c.relkind::text||':'||c.relpersistence::text||':'||COALESCE(c.reloptions::text,'')||':'||c.relrowsecurity||':'||c.relforcerowsecurity||':'||pg_catalog.pg_get_userbyid(c.relowner)||':'||CASE WHEN c.relkind IN ('r','p','v','m','f','S') THEN COALESCE((SELECT pg_catalog.jsonb_agg(pg_catalog.jsonb_build_array(pg_catalog.pg_get_userbyid(a.grantor),CASE WHEN a.grantee=0 THEN 'PUBLIC' ELSE pg_catalog.pg_get_userbyid(a.grantee) END,a.privilege_type,a.is_grantable) ORDER BY pg_catalog.pg_get_userbyid(a.grantor),CASE WHEN a.grantee=0 THEN 'PUBLIC' ELSE pg_catalog.pg_get_userbyid(a.grantee) END,a.privilege_type,a.is_grantable) FROM pg_catalog.aclexplode(CASE WHEN c.relacl IS NULL THEN pg_catalog.acldefault(CASE WHEN c.relkind='S' THEN 's'::"char" ELSE 'r'::"char" END,c.relowner) ELSE c.relacl END) a),'[]'::pg_catalog.jsonb)::text ELSE COALESCE(c.relacl::text,'') END FROM pg_catalog.pg_class c WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'rule:'||pg_catalog.pg_get_ruledef(r.oid,true)||':'||r.ev_enabled::text FROM pg_catalog.pg_rewrite r JOIN pg_catalog.pg_class c ON c.oid=r.ev_class WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'column_acl:'||c.relname||':'||a.attnum||':'||COALESCE(a.attacl::text,'') FROM pg_catalog.pg_class c JOIN pg_catalog.pg_attribute a ON a.attrelid=c.oid WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND a.attnum>0 AND NOT a.attisdropped
  UNION ALL SELECT 'trigger:'||pg_catalog.pg_get_triggerdef(t.oid)||':'||t.tgenabled::text FROM pg_catalog.pg_trigger t JOIN pg_catalog.pg_class c ON c.oid=t.tgrelid WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND NOT t.tgisinternal
  UNION ALL SELECT 'policy:'||p.polname||':'||p.polcmd::text||':'||p.polpermissive||':'||p.polroles::text||':'||COALESCE(pg_catalog.pg_get_expr(p.polqual,p.polrelid),'')||':'||COALESCE(pg_catalog.pg_get_expr(p.polwithcheck,p.polrelid),'') FROM pg_catalog.pg_policy p JOIN pg_catalog.pg_class c ON c.oid=p.polrelid WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'sequence:'||c.relname||':'||s.seqtypid::pg_catalog.regtype::text||':'||s.seqstart||':'||s.seqincrement||':'||s.seqmin||':'||s.seqmax||':'||s.seqcache||':'||s.seqcycle FROM pg_catalog.pg_sequence s JOIN pg_catalog.pg_class c ON c.oid=s.seqrelid WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'function_security:'||p.proname||':'||pg_catalog.pg_get_userbyid(p.proowner)||':'||COALESCE(p.proacl::text,'') FROM pg_catalog.pg_proc p WHERE p.pronamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'view:'||c.relname||':'||pg_catalog.pg_get_viewdef(c.oid,true) FROM pg_catalog.pg_class c WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND c.relkind='v'
  UNION ALL SELECT 'index:'||c.relname||':'||pg_catalog.pg_get_indexdef(c.oid) FROM pg_catalog.pg_class c WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND c.relkind='i'
  UNION ALL SELECT 'default:'||c.relname||':'||a.attnum||':'||COALESCE(a.attidentity::text,'')||':'||COALESCE(a.attgenerated::text,'')||':'||COALESCE(pg_catalog.pg_get_expr(d.adbin,d.adrelid),'')
   FROM pg_catalog.pg_class c JOIN pg_catalog.pg_attribute a ON a.attrelid=c.oid LEFT JOIN pg_catalog.pg_attrdef d ON d.adrelid=c.oid AND d.adnum=a.attnum
   WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND a.attnum>0 AND NOT a.attisdropped
  UNION ALL SELECT 'schema:'||n.nspname||':'||pg_catalog.pg_get_userbyid(n.nspowner)||':'||COALESCE(n.nspacl::text,'') FROM pg_catalog.pg_namespace n WHERE n.nspname IN ('ops_flow','public')
  UNION ALL SELECT 'database:'||d.datname||':'||pg_catalog.pg_get_userbyid(d.datdba)||':'||COALESCE(d.datacl::text,'') FROM pg_catalog.pg_database d WHERE d.datname=current_database()
  UNION ALL SELECT 'default_acl:'||d.defaclobjtype::text||':'||COALESCE(n.nspname,'global')||':'||d.defaclacl::text FROM pg_catalog.pg_default_acl d LEFT JOIN pg_catalog.pg_namespace n ON n.oid=d.defaclnamespace WHERE d.defaclrole=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_owner')
  UNION ALL SELECT 'role:'||r.rolname||':'||r.rolcanlogin||':'||r.rolsuper||':'||r.rolcreatedb||':'||r.rolcreaterole||':'||r.rolreplication||':'||r.rolbypassrls FROM pg_catalog.pg_roles r WHERE r.rolname IN ('opsflow_owner','opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader')
  UNION ALL SELECT 'membership:'||pg_catalog.pg_get_userbyid(m.roleid)||':'||pg_catalog.pg_get_userbyid(m.member)||':'||m.admin_option||':'||m.inherit_option||':'||m.set_option FROM pg_catalog.pg_auth_members m WHERE m.roleid IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_owner','opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader')) OR m.member IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_owner','opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader'))
 ) shape;
COMMIT;
