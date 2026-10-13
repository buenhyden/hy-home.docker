\set ON_ERROR_STOP on
-- Draft native acceptance script. Run only in an approved isolated DB as the
-- reviewed isolated audit superuser; synthetic ROWS roll back, identity sequence
-- advances do NOT roll back. Use a disposable isolated DB, not a live/restore DB.
-- This is not empty restoration proof; W38 separately reviews that operation.
-- Its session_user must SET ROLE owner and each client only in this isolated
-- audit target. Do not add runtime memberships to permit this script.
BEGIN;
SET LOCAL search_path = pg_catalog;
SELECT pg_catalog.set_config('opsflow.migration_sha256', :'migration_sha256', true);
SET LOCAL ROLE opsflow_owner;
DO $acl$
DECLARE r text; observed text; current_version integer;
BEGIN
 IF current_database()<>'opsflow_dev' THEN RAISE EXCEPTION 'wrong_database'; END IF;
 IF (SELECT pg_catalog.pg_get_userbyid(nspowner) FROM pg_catalog.pg_namespace WHERE nspname='public') IS DISTINCT FROM 'pg_database_owner'
    OR (SELECT pg_catalog.pg_get_userbyid(nspowner) FROM pg_catalog.pg_namespace WHERE nspname='ops_flow') IS DISTINCT FROM 'opsflow_owner'
    OR (SELECT pg_catalog.pg_get_userbyid(datdba) FROM pg_catalog.pg_database WHERE datname=current_database()) IS DISTINCT FROM 'opsflow_owner'
 THEN RAISE EXCEPTION 'owner_mismatch'; END IF;
 IF (SELECT count(*) FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_owner','opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader'))<>5
    OR EXISTS(SELECT 1 FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_owner','opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader')
      AND (rolsuper OR rolcreatedb OR rolcreaterole OR rolreplication OR rolbypassrls OR (rolname='opsflow_owner' AND rolcanlogin) OR (rolname<>'opsflow_owner' AND NOT rolcanlogin)))
    OR EXISTS(SELECT 1 FROM pg_catalog.pg_auth_members WHERE member IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_owner','opsflow_ingest','opsflow_notifier','opsflow_reader'))
      OR roleid IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader'))
      OR (roleid=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_owner') AND
        (member IS DISTINCT FROM (SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_migrator') OR inherit_option OR admin_option OR NOT set_option))
      OR (member=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_migrator') AND roleid<>(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_owner')))
    OR (SELECT count(*) FROM pg_catalog.pg_auth_members WHERE roleid=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_owner')
        AND member=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_migrator') AND NOT inherit_option AND NOT admin_option AND set_option)<>1
 THEN RAISE EXCEPTION 'unsafe_postflight_roles'; END IF;
 IF EXISTS (SELECT 1 FROM pg_catalog.pg_namespace WHERE nspname NOT IN ('public','ops_flow','information_schema') AND nspname !~ '^pg_')
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_class WHERE relnamespace='public'::pg_catalog.regnamespace)
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_proc WHERE pronamespace='public'::pg_catalog.regnamespace)
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_type WHERE typnamespace='public'::pg_catalog.regnamespace)
 THEN RAISE EXCEPTION 'isolated_database_not_empty'; END IF;
 IF EXISTS (SELECT 1 FROM pg_catalog.pg_database d,LATERAL pg_catalog.aclexplode(COALESCE(d.datacl,pg_catalog.acldefault('d',d.datdba))) a
    WHERE d.datname=current_database() AND a.grantee<>d.datdba AND
     (a.grantee NOT IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader')) OR a.privilege_type<>'CONNECT' OR a.is_grantable))
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_namespace n,LATERAL pg_catalog.aclexplode(COALESCE(n.nspacl,pg_catalog.acldefault('n',n.nspowner))) a
     WHERE n.nspname IN ('public','ops_flow') AND a.grantee<>n.nspowner AND
      (n.nspname='public' OR a.grantee NOT IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader')) OR a.privilege_type<>'USAGE' OR a.is_grantable))
 THEN RAISE EXCEPTION 'unknown_database_schema_acl'; END IF;
 SELECT max(version) INTO current_version FROM ops_flow.schema_version;
 IF current_version NOT IN (1,2)
    OR (SELECT count(*) FROM ops_flow.schema_version) <> current_version
    OR (SELECT count(*) FROM ops_flow.schema_version WHERE version=1
        AND migration_sha256='a9fecb083d60947a245e437fbbc97a3a5ac82a58d8d1842aff60ddefcfbca79f'
        AND schema_fingerprint ~ '^[0-9a-f]{64}$')<>1
    OR pg_catalog.current_setting('opsflow.migration_sha256') !~ '^[0-9a-f]{64}$'
    OR (SELECT count(*) FROM ops_flow.schema_version WHERE version=current_version AND migration_sha256=pg_catalog.current_setting('opsflow.migration_sha256') AND schema_fingerprint ~ '^[0-9a-f]{64}$')<>1
 THEN RAISE EXCEPTION 'version_receipt_missing'; END IF;
 SELECT pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(pg_catalog.string_agg(signature,'\n' ORDER BY signature),'UTF8')),'hex') INTO observed FROM (
  SELECT 'column:'||c.relname||':'||a.attnum||':'||a.attname||':'||pg_catalog.format_type(a.atttypid,a.atttypmod)||':'||a.attnotnull AS signature
   FROM pg_catalog.pg_class c JOIN pg_catalog.pg_attribute a ON a.attrelid=c.oid
   WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND a.attnum>0 AND NOT a.attisdropped
  UNION ALL SELECT 'function:'||pg_catalog.pg_get_functiondef(p.oid) FROM pg_catalog.pg_proc p WHERE p.pronamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'constraint:'||c.conrelid::pg_catalog.regclass::text||':'||c.contypid::pg_catalog.regtype::text||':'||c.conname||':'||pg_catalog.pg_get_constraintdef(c.oid) FROM pg_catalog.pg_constraint c WHERE c.connamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'type:'||t.typname||':'||pg_catalog.pg_get_userbyid(t.typowner)||':'||t.typtype::text||':'||t.typcategory::text||':'||t.typrelid::pg_catalog.regclass::text||':'||t.typelem::pg_catalog.regtype::text||':'||t.typbasetype::pg_catalog.regtype::text||':'||t.typtypmod||':'||t.typnotnull||':'||COALESCE(t.typdefault,'') FROM pg_catalog.pg_type t WHERE t.typnamespace='ops_flow'::pg_catalog.regnamespace
  UNION ALL SELECT 'relation:'||c.relname||':'||c.relkind::text||':'||c.relpersistence::text||':'||COALESCE(c.reloptions::text,'')||':'||c.relrowsecurity||':'||c.relforcerowsecurity||':'||pg_catalog.pg_get_userbyid(c.relowner)||':'||COALESCE(c.relacl::text,'') FROM pg_catalog.pg_class c WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace
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
 IF observed IS DISTINCT FROM (SELECT schema_fingerprint FROM ops_flow.schema_version WHERE version=current_version)
 THEN RAISE EXCEPTION 'schema_drift'; END IF;
 IF EXISTS(SELECT 1 FROM ops_flow.runs) OR EXISTS(SELECT 1 FROM ops_flow.documents)
    OR EXISTS(SELECT 1 FROM ops_flow.current_runs) OR EXISTS(SELECT 1 FROM ops_flow.outbox)
 THEN RAISE EXCEPTION 'isolated_database_not_empty'; END IF;
 FOREACH r IN ARRAY ARRAY['opsflow_ingest','opsflow_notifier','opsflow_reader'] LOOP
  IF NOT pg_catalog.has_database_privilege(r,'opsflow_dev','CONNECT')
     OR pg_catalog.has_database_privilege(r,'opsflow_dev','CREATE')
     OR pg_catalog.has_database_privilege(r,'opsflow_dev','TEMP')
     OR pg_catalog.has_schema_privilege(r,'public','CREATE')
     OR pg_catalog.has_schema_privilege(r,'ops_flow','CREATE')
  THEN RAISE EXCEPTION 'unsafe_client_acl'; END IF;
  IF EXISTS (SELECT 1 FROM pg_catalog.pg_class c WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND c.relkind='r'
    AND (pg_catalog.has_table_privilege(r,c.oid,'SELECT') OR pg_catalog.has_table_privilege(r,c.oid,'INSERT')
      OR pg_catalog.has_table_privilege(r,c.oid,'UPDATE') OR pg_catalog.has_table_privilege(r,c.oid,'DELETE')
      OR pg_catalog.has_table_privilege(r,c.oid,'REFERENCES') OR pg_catalog.has_table_privilege(r,c.oid,'TRIGGER') OR pg_catalog.has_table_privilege(r,c.oid,'TRUNCATE') OR pg_catalog.has_table_privilege(r,c.oid,'MAINTAIN')))
  THEN RAISE EXCEPTION 'direct_table_access'; END IF;
  IF EXISTS (SELECT 1 FROM pg_catalog.pg_class c WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND c.relkind='r'
      AND (pg_catalog.has_any_column_privilege(r,c.oid,'SELECT') OR pg_catalog.has_any_column_privilege(r,c.oid,'INSERT') OR pg_catalog.has_any_column_privilege(r,c.oid,'UPDATE') OR pg_catalog.has_any_column_privilege(r,c.oid,'REFERENCES')))
     OR EXISTS (SELECT 1 FROM pg_catalog.pg_class c WHERE c.relnamespace='ops_flow'::pg_catalog.regnamespace AND c.relkind='S'
      AND (pg_catalog.has_sequence_privilege(r,c.oid,'SELECT') OR pg_catalog.has_sequence_privilege(r,c.oid,'UPDATE') OR pg_catalog.has_sequence_privilege(r,c.oid,'USAGE')))
  THEN RAISE EXCEPTION 'direct_column_sequence_access'; END IF;
 END LOOP;
 IF EXISTS (SELECT 1 FROM pg_catalog.pg_database d,LATERAL pg_catalog.aclexplode(COALESCE(d.datacl,pg_catalog.acldefault('d',d.datdba))) a
    WHERE d.datname=current_database() AND a.grantee=0 AND a.privilege_type='CONNECT')
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_namespace n,LATERAL pg_catalog.aclexplode(COALESCE(n.nspacl,pg_catalog.acldefault('n',n.nspowner))) a
    WHERE n.nspname='public' AND a.grantee=0 AND a.privilege_type='CREATE')
 THEN RAISE EXCEPTION 'public_connection_or_create'; END IF;
 IF pg_catalog.has_function_privilege('opsflow_ingest','ops_flow.claim_notification()','EXECUTE')
    OR pg_catalog.has_function_privilege('opsflow_notifier','ops_flow.publish_manifest(text,text,text,timestamptz,jsonb,text)','EXECUTE')
    OR pg_catalog.has_function_privilege('opsflow_reader','ops_flow.ack_notification(bigint,uuid)','EXECUTE')
 THEN RAISE EXCEPTION 'wrong_role_function_grant'; END IF;
END $acl$;

-- Owner seeds only synthetic test input; no actual manifest or credential.
CREATE TEMP TABLE p04_case (source text,sha text,run text,rows jsonb) ON COMMIT DROP;
INSERT INTO p04_case SELECT 'hy-home.docker',repeat('a',64),
 pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to('hy-home.docker:'||repeat('a',64),'UTF8')),'hex'),
 pg_catalog.jsonb_build_array(pg_catalog.jsonb_build_object('path','docs/synthetic.md','revision',repeat('b',40),'content_sha256',repeat('c',64),'title','Synthetic'));
GRANT SELECT ON p04_case TO opsflow_ingest;
SET LOCAL ROLE opsflow_ingest;
DO $invalid$
DECLARE c record; bad jsonb; denied boolean; variant text;
BEGIN
 SELECT * INTO c FROM pg_temp.p04_case;
 FOREACH variant IN ARRAY ARRAY['extra','typed','traversal','SECRET','PASSWORDS','credentials','tokens','control','c1','duplicate','null','empty','scalar','bad_hash','bad_source','bad_artifact','infinite'] LOOP
  bad:=c.rows;
  IF variant='extra' THEN bad:=pg_catalog.jsonb_set(bad,'{0,extra}','"x"'); END IF;
  IF variant='typed' THEN bad:=pg_catalog.jsonb_set(bad,'{0,title}','5'); END IF;
  IF variant='traversal' THEN bad:=pg_catalog.jsonb_set(bad,'{0,path}','"docs/../x"'); END IF;
  IF variant IN ('SECRET','PASSWORDS','credentials','tokens') THEN bad:=pg_catalog.jsonb_set(bad,'{0,path}',pg_catalog.to_jsonb(variant||'/file.md')); END IF;
  IF variant='control' THEN bad:=pg_catalog.jsonb_set(bad,'{0,title}',pg_catalog.to_jsonb('x'||pg_catalog.chr(127))); END IF;
  IF variant='c1' THEN bad:=pg_catalog.jsonb_set(bad,'{0,path}',pg_catalog.to_jsonb('docs/'||pg_catalog.chr(159)||'.md')); END IF;
  IF variant='duplicate' THEN bad:=bad||bad; END IF;
  IF variant='null' THEN bad:=NULL; END IF;
  IF variant='empty' THEN bad:='[]'; END IF;
  IF variant='scalar' THEN bad:='[5]'; END IF;
  denied:=false;
  BEGIN
   PERFORM ops_flow.publish_manifest(CASE WHEN variant='bad_source' THEN 'unknown' ELSE c.source END,c.run,
    CASE WHEN variant='bad_hash' THEN 'invalid' ELSE c.sha END,
    CASE WHEN variant='infinite' THEN 'infinity'::timestamptz ELSE '2026-01-02T00:00:00Z'::timestamptz END,bad,
    CASE WHEN variant='bad_artifact' THEN 'wrong' ELSE 'manifest-validated/'||c.source||'/'||c.run||'.json' END);
  EXCEPTION WHEN raise_exception THEN denied:=true; END;
  IF NOT denied THEN RAISE EXCEPTION 'invalid_variant_accepted'; END IF;
 END LOOP;
 denied:=false;
 BEGIN PERFORM 1 FROM ops_flow.outbox; EXCEPTION WHEN insufficient_privilege THEN denied:=true; END;
 IF NOT denied THEN RAISE EXCEPTION 'ingest_table_read_allowed'; END IF;
 denied:=false;
 BEGIN CREATE TABLE public.p04_denied(x integer); EXCEPTION WHEN insufficient_privilege THEN denied:=true; END;
 IF NOT denied THEN RAISE EXCEPTION 'ingest_create_allowed'; END IF;
 IF ops_flow.publish_manifest(c.source,c.run,c.sha,'2026-01-02T00:00:00Z',c.rows,'manifest-validated/'||c.source||'/'||c.run||'.json')<>'published'
 THEN RAISE EXCEPTION 'initial_publish_failed'; END IF;
 IF ops_flow.publish_manifest(c.source,c.run,c.sha,'2026-01-02T00:00:00Z',c.rows,'manifest-validated/'||c.source||'/'||c.run||'.json')<>'replayed'
 THEN RAISE EXCEPTION 'replay_failed'; END IF;
END $invalid$;
SET LOCAL ROLE opsflow_owner;
DO $history$
DECLARE c record; older_sha text:=repeat('d',64); older text; newer_sha text:=repeat('e',64); newer text; conflict_sha text:=repeat('f',64); conflict_run text; denied boolean;
BEGIN
 SELECT * INTO c FROM pg_temp.p04_case;
 older:=pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(c.source||':'||older_sha,'UTF8')),'hex');
 newer:=pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(c.source||':'||newer_sha,'UTF8')),'hex');
 conflict_run:=pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(c.source||':'||conflict_sha,'UTF8')),'hex');
 IF ops_flow.publish_manifest(c.source,older,older_sha,'2026-01-01T00:00:00Z',c.rows,'manifest-validated/'||c.source||'/'||older||'.json')<>'historical'
 THEN RAISE EXCEPTION 'historical_failed'; END IF;
 IF (SELECT run_id FROM ops_flow.current_runs WHERE source=c.source)<>c.run OR (SELECT count(*) FROM ops_flow.outbox WHERE run_id IN(c.run,older))<>1
 THEN RAISE EXCEPTION 'replay_or_history_event'; END IF;
 PERFORM ops_flow.publish_manifest(c.source,newer,newer_sha,'2026-01-03T00:00:00Z',c.rows,'manifest-validated/'||c.source||'/'||newer||'.json');
 IF (SELECT status FROM ops_flow.runs WHERE run_id=c.run)<>'published' OR (SELECT status FROM ops_flow.runs WHERE run_id=older)<>'historical'
 THEN RAISE EXCEPTION 'history_rewritten'; END IF;
 denied:=false;
 BEGIN PERFORM ops_flow.publish_manifest(c.source,conflict_run,conflict_sha,'2026-01-01T00:00:00Z',c.rows,'manifest-validated/'||c.source||'/'||conflict_run||'.json');
 EXCEPTION WHEN raise_exception THEN denied:=true; END;
 IF NOT denied THEN RAISE EXCEPTION 'all_history_timestamp_conflict_allowed'; END IF;
END $history$;
SET LOCAL ROLE opsflow_notifier;
DO $lease$
DECLARE receipt record; denied boolean;
BEGIN
 SELECT * INTO receipt FROM ops_flow.claim_notification();
 IF receipt.id IS NULL OR receipt.lease_token IS NULL THEN RAISE EXCEPTION 'claim_failed'; END IF;
 IF receipt.lease_until-pg_catalog.clock_timestamp() NOT BETWEEN interval '9 minutes 59 seconds' AND interval '10 minutes'
 THEN RAISE EXCEPTION 'lease_deadline_failed'; END IF;
 IF ops_flow.ack_notification(receipt.id,pg_catalog.gen_random_uuid())
    OR ops_flow.retry_notification(receipt.id,pg_catalog.gen_random_uuid())
 THEN RAISE EXCEPTION 'wrong_token_accepted'; END IF;
 IF NOT ops_flow.ack_notification(receipt.id,receipt.lease_token) OR ops_flow.ack_notification(receipt.id,receipt.lease_token)
 THEN RAISE EXCEPTION 'ack_not_idempotent'; END IF;
 SELECT * INTO receipt FROM ops_flow.claim_notification();
 IF receipt.id IS NULL OR NOT ops_flow.retry_notification(receipt.id,receipt.lease_token)
 THEN RAISE EXCEPTION 'notifier_retry_failed'; END IF;
 denied:=false;
 BEGIN UPDATE ops_flow.outbox SET state='dead'; EXCEPTION WHEN insufficient_privilege THEN denied:=true; END;
 IF NOT denied THEN RAISE EXCEPTION 'notifier_direct_write_allowed'; END IF;
END $lease$;
SET LOCAL ROLE opsflow_owner;
DO $expiry$
DECLARE old_receipt record; replacement record; i integer;
BEGIN
 UPDATE ops_flow.outbox SET next_attempt_at=pg_catalog.clock_timestamp()-interval '1 second' WHERE state='retry';
 SELECT * INTO old_receipt FROM ops_flow.claim_notification();
 IF old_receipt.id IS NULL THEN RAISE EXCEPTION 'second_claim_failed'; END IF;
 UPDATE ops_flow.outbox SET lease_until=pg_catalog.clock_timestamp()-interval '1 second' WHERE id=old_receipt.id;
 IF ops_flow.ack_notification(old_receipt.id,old_receipt.lease_token) OR ops_flow.retry_notification(old_receipt.id,old_receipt.lease_token)
 THEN RAISE EXCEPTION 'expired_token_accepted'; END IF;
 SELECT * INTO replacement FROM ops_flow.claim_notification();
 IF replacement.id<>old_receipt.id OR replacement.lease_token=old_receipt.lease_token THEN RAISE EXCEPTION 'lease_not_rotated'; END IF;
 FOR i IN 3..5 LOOP
  IF NOT ops_flow.retry_notification(replacement.id,replacement.lease_token) THEN RAISE EXCEPTION 'retry_failed'; END IF;
  IF (SELECT next_attempt_at-pg_catalog.clock_timestamp()>interval '15 minutes' FROM ops_flow.outbox WHERE id=replacement.id)
  THEN RAISE EXCEPTION 'backoff_unbounded'; END IF;
  UPDATE ops_flow.outbox SET next_attempt_at=pg_catalog.clock_timestamp()-interval '1 second' WHERE id=replacement.id;
  IF i<5 THEN SELECT * INTO replacement FROM ops_flow.claim_notification(); END IF;
 END LOOP;
 IF (SELECT state FROM ops_flow.outbox WHERE id=old_receipt.id)<>'dead' OR (SELECT attempts FROM ops_flow.outbox WHERE id=old_receipt.id)<>5
 THEN RAISE EXCEPTION 'attempt_budget_failed'; END IF;
END $expiry$;
SET LOCAL ROLE opsflow_reader;
SELECT count(*) FROM ops_flow.published_documents;
SELECT count(*) FROM ops_flow.delivery_status;
DO $reader$
DECLARE denied boolean:=false;
BEGIN
 BEGIN PERFORM 1 FROM ops_flow.runs; EXCEPTION WHEN insufficient_privilege THEN denied:=true; END;
 IF NOT denied THEN RAISE EXCEPTION 'reader_base_table_allowed'; END IF;
END $reader$;
ROLLBACK;
-- Separate fresh connections must still prove runtime cannot CONNECT to other
-- workload/MNG DBs: this single-DB rollback script cannot establish that boundary.
