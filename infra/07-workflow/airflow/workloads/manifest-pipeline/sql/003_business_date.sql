\set ON_ERROR_STOP on
-- V2 adds the source/UTC-business-date invariant without changing the frozen
-- publication function or P05 interface. The caller supplies this file's SHA256.
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
 IF (SELECT count(*) FROM ops_flow.schema_version) <> 1
    OR (SELECT count(*) FROM ops_flow.schema_version
        WHERE version=1
          AND migration_sha256='a9fecb083d60947a245e437fbbc97a3a5ac82a58d8d1842aff60ddefcfbca79f'
          AND schema_fingerprint ~ '^[0-9a-f]{64}$') <> 1
 THEN RAISE EXCEPTION 'unknown_version_or_v1_receipt'; END IF;
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
 IF observed IS DISTINCT FROM (SELECT schema_fingerprint FROM ops_flow.schema_version WHERE version=1)
 THEN RAISE EXCEPTION 'schema_drift'; END IF;
 IF EXISTS (
  SELECT 1 FROM ops_flow.runs
  GROUP BY source,((captured_at AT TIME ZONE 'UTC')::date)
  HAVING count(*)>1
 ) THEN RAISE EXCEPTION 'existing_source_business_date_conflict'; END IF;
END $preflight$;

ALTER TABLE ops_flow.schema_version DROP CONSTRAINT schema_version_version_check;
ALTER TABLE ops_flow.schema_version ADD CONSTRAINT schema_version_version_check CHECK(version IN (1,2));
CREATE UNIQUE INDEX runs_source_business_date_uidx
 ON ops_flow.runs (source, ((captured_at AT TIME ZONE 'UTC')::date));

INSERT INTO ops_flow.schema_version SELECT 2,pg_catalog.current_setting('opsflow.migration_sha256'),
 pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(pg_catalog.string_agg(signature,'\n' ORDER BY signature),'UTF8')),'hex')
 FROM (
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
COMMIT;
