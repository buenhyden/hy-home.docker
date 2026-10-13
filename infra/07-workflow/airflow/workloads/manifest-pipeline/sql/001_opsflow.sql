\set ON_ERROR_STOP on
-- Draft v1: reviewed psql caller supplies migration_sha256 from the exact file.
-- SET ROLE opsflow_owner first through the existing migrator capability.
-- No credentials, role provisioning or automatic ACL repair occurs here.
BEGIN;
SET LOCAL search_path = pg_catalog;
SELECT pg_catalog.set_config('opsflow.migration_sha256', :'migration_sha256', true);
DO $preflight$
DECLARE r record; expected text := pg_catalog.current_setting('opsflow.migration_sha256');
BEGIN
 IF current_database() <> 'opsflow_dev' OR current_user <> 'opsflow_owner' OR session_user <> 'opsflow_migrator'
    OR expected !~ '^[0-9a-f]{64}$' THEN RAISE EXCEPTION 'migration_identity_or_checksum'; END IF;
 IF (SELECT pg_catalog.pg_get_userbyid(datdba) FROM pg_catalog.pg_database WHERE datname=current_database()) <> 'opsflow_owner'
    OR (SELECT pg_catalog.pg_get_userbyid(nspowner) FROM pg_catalog.pg_namespace WHERE nspname='ops_flow') IS DISTINCT FROM 'opsflow_owner'
 THEN RAISE EXCEPTION 'migration_owner_mismatch'; END IF;
 IF (SELECT pg_catalog.pg_get_userbyid(nspowner) FROM pg_catalog.pg_namespace WHERE nspname='public') IS DISTINCT FROM 'pg_database_owner'
 THEN RAISE EXCEPTION 'public_schema_owner_mismatch'; END IF;
 FOR r IN SELECT * FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_owner','opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader') LOOP
  IF r.rolsuper OR r.rolcreatedb OR r.rolcreaterole OR r.rolreplication OR r.rolbypassrls
     OR (r.rolname='opsflow_owner' AND r.rolcanlogin)
     OR (r.rolname<>'opsflow_owner' AND NOT r.rolcanlogin)
  THEN RAISE EXCEPTION 'unsafe_workload_role'; END IF;
 END LOOP;
 IF (SELECT count(*) FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_owner','opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader')) <> 5
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_auth_members WHERE member IN
       (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_owner','opsflow_ingest','opsflow_notifier','opsflow_reader'))
       OR roleid IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_ingest','opsflow_notifier','opsflow_reader'))
       OR (roleid=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_owner')
           AND (member IS DISTINCT FROM (SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_migrator')
                OR inherit_option OR admin_option OR NOT set_option)))
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_auth_members WHERE
       (member=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_migrator') AND roleid<>(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_owner'))
       OR roleid=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_migrator'))
    OR (SELECT count(*) FROM pg_catalog.pg_auth_members WHERE roleid=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_owner')
       AND member=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_migrator') AND NOT inherit_option AND NOT admin_option AND set_option)<>1
 THEN RAISE EXCEPTION 'unsafe_role_membership'; END IF;
 FOR r IN SELECT rolname FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader') LOOP
  IF NOT pg_catalog.has_database_privilege(r.rolname,current_database(),'CONNECT')
     OR pg_catalog.has_database_privilege(r.rolname,current_database(),'CREATE')
     OR pg_catalog.has_database_privilege(r.rolname,current_database(),'TEMP')
  THEN RAISE EXCEPTION 'unsafe_client_database_acl'; END IF;
 END LOOP;
 IF EXISTS (SELECT 1 FROM pg_catalog.pg_database d, LATERAL pg_catalog.aclexplode(COALESCE(d.datacl,pg_catalog.acldefault('d',d.datdba))) a
      WHERE d.datname=current_database() AND a.grantee=0 AND a.privilege_type IN ('CONNECT','CREATE','TEMPORARY'))
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_namespace n, LATERAL pg_catalog.aclexplode(COALESCE(n.nspacl,pg_catalog.acldefault('n',n.nspowner))) a
      WHERE n.nspname IN ('public','ops_flow') AND a.grantee=0)
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_namespace n, LATERAL pg_catalog.aclexplode(n.nspacl) a
      WHERE n.nspname IN ('public','ops_flow') AND a.privilege_type='CREATE' AND a.grantee IN
       (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_ingest','opsflow_notifier','opsflow_reader')))
 THEN RAISE EXCEPTION 'unsafe_database_schema_acl'; END IF;
 IF EXISTS (SELECT 1 FROM pg_catalog.pg_database d,LATERAL pg_catalog.aclexplode(COALESCE(d.datacl,pg_catalog.acldefault('d',d.datdba))) a
    WHERE d.datname=current_database() AND a.grantee<>d.datdba AND
     (a.grantee NOT IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader')) OR a.privilege_type<>'CONNECT' OR a.is_grantable))
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_namespace n,LATERAL pg_catalog.aclexplode(COALESCE(n.nspacl,pg_catalog.acldefault('n',n.nspowner))) a
     WHERE n.nspname IN ('public','ops_flow') AND a.grantee<>n.nspowner AND
      (n.nspname='public' OR a.grantee NOT IN (SELECT oid FROM pg_catalog.pg_roles WHERE rolname IN ('opsflow_migrator','opsflow_ingest','opsflow_notifier','opsflow_reader')) OR a.privilege_type<>'USAGE' OR a.is_grantable))
 THEN RAISE EXCEPTION 'unknown_database_schema_acl'; END IF;
 IF EXISTS (SELECT 1 FROM pg_catalog.pg_namespace WHERE nspname NOT IN ('public','ops_flow','information_schema') AND nspname !~ '^pg_')
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_class WHERE relnamespace='public'::pg_catalog.regnamespace)
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_proc WHERE pronamespace='public'::pg_catalog.regnamespace)
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_type WHERE typnamespace='public'::pg_catalog.regnamespace)
 THEN RAISE EXCEPTION 'isolated_database_not_empty'; END IF;
 -- Reject generic provisioner grants, including future object DML. Do not revoke them silently.
 IF EXISTS (SELECT 1 FROM pg_catalog.pg_default_acl d, LATERAL pg_catalog.aclexplode(d.defaclacl) a
    WHERE d.defaclrole=(SELECT oid FROM pg_catalog.pg_roles WHERE rolname='opsflow_owner')
      AND a.grantee <> d.defaclrole)
 THEN RAISE EXCEPTION 'unsafe_default_acl'; END IF;
 IF pg_catalog.to_regclass('ops_flow.schema_version') IS NOT NULL THEN
  RAISE EXCEPTION 'migration_already_present_requires_independent_fingerprint_verification';
 END IF;
 IF EXISTS (SELECT 1 FROM pg_catalog.pg_class WHERE relnamespace='ops_flow'::pg_catalog.regnamespace)
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_proc WHERE pronamespace='ops_flow'::pg_catalog.regnamespace)
    OR EXISTS (SELECT 1 FROM pg_catalog.pg_type WHERE typnamespace='ops_flow'::pg_catalog.regnamespace)
 THEN RAISE EXCEPTION 'unknown_existing_schema_shape'; END IF;
END $preflight$;

CREATE TABLE ops_flow.runs (
 run_id text PRIMARY KEY CHECK(run_id ~ '^[0-9a-f]{64}$'),
 source text NOT NULL CHECK(source IN ('hy-home.docker','hy-home.k8s','Project-Template','blog-data')),
 raw_sha256 text NOT NULL CHECK(raw_sha256 ~ '^[0-9a-f]{64}$'),
 captured_at timestamptz NOT NULL CHECK(pg_catalog.isfinite(captured_at)),
 artifact_key text NOT NULL, row_count integer NOT NULL CHECK(row_count BETWEEN 1 AND 5000),
 status text NOT NULL CHECK(status IN ('published','historical')),
 created_at timestamptz NOT NULL DEFAULT pg_catalog.clock_timestamp(), UNIQUE(source,raw_sha256),
 UNIQUE(source,captured_at), UNIQUE(run_id,source,captured_at), UNIQUE(run_id,source,row_count)
);
CREATE TABLE ops_flow.documents (
 run_id text REFERENCES ops_flow.runs NOT NULL, path text NOT NULL,
 revision text NOT NULL CHECK(revision ~ '^[0-9a-f]{40}$'),
 content_sha256 text NOT NULL CHECK(content_sha256 ~ '^[0-9a-f]{64}$'), title text NOT NULL,
 PRIMARY KEY(run_id,path)
);
CREATE TABLE ops_flow.current_runs (
 source text PRIMARY KEY, run_id text UNIQUE NOT NULL,
 captured_at timestamptz NOT NULL CHECK(pg_catalog.isfinite(captured_at)),
 FOREIGN KEY(run_id,source,captured_at) REFERENCES ops_flow.runs(run_id,source,captured_at)
);
CREATE TABLE ops_flow.outbox (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 run_id text UNIQUE NOT NULL, source text NOT NULL, row_count integer NOT NULL,
 state text NOT NULL DEFAULT 'pending' CHECK(state IN ('pending','sending','retry','accepted_by_smtp','dead')),
 attempts integer NOT NULL DEFAULT 0 CHECK(attempts BETWEEN 0 AND 5),
 next_attempt_at timestamptz NOT NULL DEFAULT pg_catalog.clock_timestamp(),
 lease_token uuid, lease_until timestamptz, last_error_code text, accepted_at timestamptz,
 created_at timestamptz NOT NULL DEFAULT pg_catalog.clock_timestamp(),
 CHECK((state='sending')=(lease_token IS NOT NULL AND lease_until IS NOT NULL)),
 CHECK((state='accepted_by_smtp')=(accepted_at IS NOT NULL)),
 FOREIGN KEY(run_id,source,row_count) REFERENCES ops_flow.runs(run_id,source,row_count)
);
CREATE INDEX outbox_pending_idx ON ops_flow.outbox(state,next_attempt_at);

CREATE FUNCTION ops_flow.publish_manifest(p_source text,p_run text,p_sha text,p_time timestamptz,p_rows jsonb,p_artifact text)
RETURNS text LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog AS $publish$
DECLARE n integer; old_time timestamptz; result_state text; prior ops_flow.runs%ROWTYPE;
BEGIN
 IF p_source IS NULL OR p_source NOT IN ('hy-home.docker','hy-home.k8s','Project-Template','blog-data')
    OR p_run IS NULL OR p_sha IS NULL OR p_time IS NULL OR NOT pg_catalog.isfinite(p_time)
    OR p_sha !~ '^[0-9a-f]{64}$' OR p_run !~ '^[0-9a-f]{64}$'
    OR p_run <> pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(p_source||':'||p_sha,'UTF8')),'hex')
    OR p_artifact IS DISTINCT FROM 'manifest-validated/'||p_source||'/'||p_run||'.json'
    OR pg_catalog.jsonb_typeof(p_rows) IS DISTINCT FROM 'array'
 THEN RAISE EXCEPTION 'invalid_manifest_contract'; END IF;
 n := pg_catalog.jsonb_array_length(p_rows);
 IF n NOT BETWEEN 1 AND 5000 THEN RAISE EXCEPTION 'invalid_row_count'; END IF;
 -- Check object kinds first: jsonb_object_keys must never receive a scalar.
 IF EXISTS (SELECT 1 FROM pg_catalog.jsonb_array_elements(p_rows) r WHERE pg_catalog.jsonb_typeof(r) IS DISTINCT FROM 'object')
 THEN RAISE EXCEPTION 'invalid_row_type'; END IF;
 IF EXISTS (SELECT 1 FROM pg_catalog.jsonb_array_elements(p_rows) r
    WHERE (SELECT pg_catalog.count(*) FROM pg_catalog.jsonb_object_keys(r)) <> 4
       OR NOT (r ?& ARRAY['path','revision','content_sha256','title'])
       OR pg_catalog.jsonb_typeof(r->'path') IS DISTINCT FROM 'string'
       OR pg_catalog.jsonb_typeof(r->'revision') IS DISTINCT FROM 'string'
       OR pg_catalog.jsonb_typeof(r->'content_sha256') IS DISTINCT FROM 'string'
       OR pg_catalog.jsonb_typeof(r->'title') IS DISTINCT FROM 'string'
       OR r->>'revision' !~ '^[0-9a-f]{40}$' OR r->>'content_sha256' !~ '^[0-9a-f]{64}$'
       OR pg_catalog.length(r->>'path') NOT BETWEEN 1 AND 512
       OR pg_catalog.length(r->>'title') NOT BETWEEN 1 AND 256
       OR r->>'path' ~ '(^/|\\|(^|/)\.{1,2}(/|$)|(^|/)\.|//|/$|[[:cntrl:]])'
       OR r->>'path' ~* '(^|/)(secret|secrets|password|passwords|credentials|tokens)(/|$)'
       OR r->>'title' ~ '[[:cntrl:]]'
       OR EXISTS (SELECT 1 FROM pg_catalog.generate_series(127,159) code
          WHERE pg_catalog.strpos(r->>'path',pg_catalog.chr(code))>0 OR pg_catalog.strpos(r->>'title',pg_catalog.chr(code))>0))
    OR (SELECT pg_catalog.count(DISTINCT r->>'path') FROM pg_catalog.jsonb_array_elements(p_rows) r) <> n
 THEN RAISE EXCEPTION 'invalid_rows'; END IF;
 PERFORM pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended('opsflow:'||p_source,0));
 SELECT * INTO prior FROM ops_flow.runs WHERE run_id=p_run;
 IF FOUND THEN
  IF prior.source<>p_source OR prior.raw_sha256<>p_sha OR prior.captured_at<>p_time
     OR prior.artifact_key<>p_artifact OR prior.row_count<>n
     OR EXISTS ((SELECT path,revision,content_sha256,title FROM ops_flow.documents WHERE run_id=p_run)
        EXCEPT (SELECT r->>'path',r->>'revision',r->>'content_sha256',r->>'title' FROM pg_catalog.jsonb_array_elements(p_rows) r))
     OR EXISTS ((SELECT r->>'path',r->>'revision',r->>'content_sha256',r->>'title' FROM pg_catalog.jsonb_array_elements(p_rows) r)
        EXCEPT (SELECT path,revision,content_sha256,title FROM ops_flow.documents WHERE run_id=p_run))
  THEN RAISE EXCEPTION 'replay_payload_conflict'; END IF;
  RETURN 'replayed';
 END IF;
 IF EXISTS (SELECT 1 FROM ops_flow.runs WHERE source=p_source AND captured_at=p_time)
 THEN RAISE EXCEPTION 'same_time_conflicting_manifest'; END IF;
 SELECT captured_at INTO old_time FROM ops_flow.current_runs WHERE source=p_source;
 result_state := CASE WHEN old_time IS NULL OR p_time>old_time THEN 'published' ELSE 'historical' END;
 INSERT INTO ops_flow.runs VALUES(p_run,p_source,p_sha,p_time,p_artifact,n,result_state,pg_catalog.clock_timestamp());
 INSERT INTO ops_flow.documents SELECT p_run,r->>'path',r->>'revision',r->>'content_sha256',r->>'title' FROM pg_catalog.jsonb_array_elements(p_rows) r;
 IF result_state='published' THEN
  INSERT INTO ops_flow.current_runs VALUES(p_source,p_run,p_time)
   ON CONFLICT(source) DO UPDATE SET run_id=EXCLUDED.run_id,captured_at=EXCLUDED.captured_at;
  INSERT INTO ops_flow.outbox(run_id,source,row_count) VALUES(p_run,p_source,n);
 END IF;
 RETURN result_state;
END $publish$;

CREATE FUNCTION ops_flow.claim_notification()
RETURNS TABLE(id bigint,run_id text,source text,row_count integer,lease_token uuid,lease_until timestamptz)
LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog AS $claim$
BEGIN
 UPDATE ops_flow.outbox o SET state='dead',last_error_code='retry_exhausted',lease_token=NULL,lease_until=NULL
 WHERE o.attempts>=5 AND (o.state IN ('pending','retry') OR (o.state='sending' AND o.lease_until<=pg_catalog.clock_timestamp()));
 RETURN QUERY WITH candidate AS (
  SELECT o.id FROM ops_flow.outbox o WHERE o.attempts<5 AND
   ((o.state IN ('pending','retry') AND o.next_attempt_at<=pg_catalog.clock_timestamp())
    OR (o.state='sending' AND o.lease_until<=pg_catalog.clock_timestamp()))
  ORDER BY o.id FOR UPDATE SKIP LOCKED LIMIT 1
 ), claimed AS (
  UPDATE ops_flow.outbox o SET state='sending',attempts=o.attempts+1,lease_token=pg_catalog.gen_random_uuid(),
   lease_until=pg_catalog.clock_timestamp()+interval '10 minutes'
  FROM candidate c WHERE o.id=c.id RETURNING o.id,o.run_id,o.source,o.row_count,o.lease_token,o.lease_until
 ) SELECT c.id,c.run_id,c.source,c.row_count,c.lease_token,c.lease_until FROM claimed c;
END $claim$;
CREATE FUNCTION ops_flow.ack_notification(p_id bigint,p_token uuid)
RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog AS $ack$
DECLARE n integer;
BEGIN
 UPDATE ops_flow.outbox o SET state='accepted_by_smtp',accepted_at=pg_catalog.clock_timestamp(),lease_token=NULL,lease_until=NULL
 WHERE o.id=p_id AND o.state='sending' AND o.lease_token=p_token AND o.lease_until>pg_catalog.clock_timestamp();
 GET DIAGNOSTICS n=ROW_COUNT; RETURN n=1;
END $ack$;
CREATE FUNCTION ops_flow.retry_notification(p_id bigint,p_token uuid)
RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog AS $retry$
DECLARE n integer;
BEGIN
 UPDATE ops_flow.outbox o SET state=CASE WHEN o.attempts>=5 THEN 'dead' ELSE 'retry' END,
  next_attempt_at=pg_catalog.clock_timestamp()+least(900,30*pg_catalog.power(2,o.attempts)::integer)*interval '1 second',
  last_error_code='smtp_outcome_unknown',lease_token=NULL,lease_until=NULL
 WHERE o.id=p_id AND o.state='sending' AND o.lease_token=p_token AND o.lease_until>pg_catalog.clock_timestamp();
 GET DIAGNOSTICS n=ROW_COUNT; RETURN n=1;
END $retry$;

CREATE VIEW ops_flow.published_documents AS SELECT d.*,r.source,r.captured_at
 FROM ops_flow.current_runs c JOIN ops_flow.runs r USING(run_id) JOIN ops_flow.documents d USING(run_id);
CREATE VIEW ops_flow.delivery_status AS SELECT id,run_id,source,state,attempts,created_at,accepted_at,last_error_code FROM ops_flow.outbox;
REVOKE ALL ON ALL TABLES IN SCHEMA ops_flow FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA ops_flow FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA ops_flow FROM PUBLIC;
GRANT USAGE ON SCHEMA ops_flow TO opsflow_ingest,opsflow_notifier,opsflow_reader;
GRANT EXECUTE ON FUNCTION ops_flow.publish_manifest(text,text,text,timestamptz,jsonb,text) TO opsflow_ingest;
GRANT EXECUTE ON FUNCTION ops_flow.claim_notification(),ops_flow.ack_notification(bigint,uuid),ops_flow.retry_notification(bigint,uuid) TO opsflow_notifier;
GRANT SELECT ON ops_flow.published_documents, ops_flow.delivery_status TO opsflow_reader;
-- Not self-referential: caller's file digest is stored separately from observed schema fingerprint.
-- Reapplication always aborts; an independent verifier must compare both before a future migration.
CREATE TABLE ops_flow.schema_version(version integer PRIMARY KEY CHECK(version=1), migration_sha256 text NOT NULL, schema_fingerprint text NOT NULL);
INSERT INTO ops_flow.schema_version SELECT 1,pg_catalog.current_setting('opsflow.migration_sha256'),
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
