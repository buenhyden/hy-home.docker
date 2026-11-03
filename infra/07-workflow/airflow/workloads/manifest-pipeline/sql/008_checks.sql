\set ON_ERROR_STOP on
-- Read-only V5 receipt, ACL and recovery-function acceptance.
-- Run only in an approved isolated DB as its existing audit administrator.
-- Caller supplies the exact 007_notification_recovery.sql SHA256; no role grants here.
-- No synthetic publication or notification writes; this is not restore proof.
BEGIN READ ONLY;
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
 IF current_version <> 5
    OR (SELECT count(*) FROM ops_flow.schema_version) <> current_version
    OR (SELECT count(*) FROM ops_flow.schema_version WHERE version=1
        AND migration_sha256='82a4762a8962832c7fdd05826df3b97cf02cc4f96c974a328e42e4493143b18f'
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
 IF observed IS DISTINCT FROM (SELECT schema_fingerprint FROM ops_flow.schema_version WHERE version=current_version)
 THEN RAISE EXCEPTION 'schema_drift'; END IF;
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
 FOREACH r IN ARRAY ARRAY['opsflow_ingest','opsflow_notifier','opsflow_reader'] LOOP
  IF pg_catalog.has_function_privilege(r,'ops_flow.requeue_dead_notification(bigint,integer,uuid,text)','EXECUTE')
     OR pg_catalog.has_function_privilege(r,'ops_flow.quarantine_restored_notification(bigint,integer,uuid,text)','EXECUTE')
  THEN RAISE EXCEPTION 'recovery_grant_to_application'; END IF;
 END LOOP;
 IF NOT pg_catalog.has_function_privilege('opsflow_migrator','ops_flow.requeue_dead_notification(bigint,integer,uuid,text)','EXECUTE')
    OR NOT pg_catalog.has_function_privilege('opsflow_migrator','ops_flow.quarantine_restored_notification(bigint,integer,uuid,text)','EXECUTE')
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_proc p,LATERAL pg_catalog.aclexplode(COALESCE(p.proacl,pg_catalog.acldefault('f',p.proowner))) a
      WHERE p.pronamespace='ops_flow'::pg_catalog.regnamespace
       AND p.proname IN ('requeue_dead_notification','quarantine_restored_notification') AND a.grantee=0)
 THEN RAISE EXCEPTION 'unsafe_operator_recovery_acl'; END IF;
END $acl$;

SET LOCAL ROLE opsflow_reader;
SELECT run_id,data_version FROM ops_flow.published_documents LIMIT 0;
SELECT id,run_id,state FROM ops_flow.delivery_status LIMIT 0;
DO $reader$
DECLARE denied boolean := false;
BEGIN
 BEGIN PERFORM 1 FROM ops_flow.runs;
 EXCEPTION WHEN insufficient_privilege THEN denied := true; END;
 IF NOT denied THEN RAISE EXCEPTION 'reader_base_table_allowed'; END IF;
END $reader$;
ROLLBACK;
