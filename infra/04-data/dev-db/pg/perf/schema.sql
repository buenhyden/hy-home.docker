BEGIN;

CREATE SCHEMA IF NOT EXISTS quality AUTHORIZATION perf_owner;
REVOKE ALL ON SCHEMA quality FROM PUBLIC;

CREATE TABLE IF NOT EXISTS quality.schema_migrations (
  version integer PRIMARY KEY,
  applied_at timestamptz NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE IF NOT EXISTS quality.projects (
  project_id text PRIMARY KEY
    CHECK (project_id ~ '^[a-z][a-z0-9-]{0,62}$'),
  reader_role name NOT NULL UNIQUE,
  writer_role name NOT NULL UNIQUE,
  verdict_role name NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  CHECK (reader_role <> writer_role),
  CHECK (reader_role <> verdict_role),
  CHECK (writer_role <> verdict_role)
);

CREATE TABLE IF NOT EXISTS quality.run_attempts (
  run_id uuid NOT NULL,
  attempt integer NOT NULL CHECK (attempt > 0),
  project_id text NOT NULL REFERENCES quality.projects(project_id),
  manifest_sha256 text NOT NULL CHECK (manifest_sha256 ~ '^[0-9a-f]{64}$'),
  final_sha256 text NOT NULL CHECK (final_sha256 ~ '^[0-9a-f]{64}$'),
  payload_sha256 text NOT NULL CHECK (payload_sha256 ~ '^[0-9a-f]{64}$'),
  execution_state text NOT NULL
    CHECK (execution_state IN ('completed', 'interrupted')),
  reported_verdict text NOT NULL
    CHECK (reported_verdict IN (
      'passed', 'failed_threshold', 'failed_execution', 'incomplete'
    )),
  evidence_state text NOT NULL
    CHECK (evidence_state IN ('complete', 'incomplete')),
  started_at timestamptz,
  ended_at timestamptz,
  samples bigint NOT NULL CHECK (samples >= 0),
  imported_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  PRIMARY KEY (run_id, attempt),
  UNIQUE (run_id, attempt, project_id)
);

-- v2: replace the pre-release unnamed state checks and permit honest
-- pre-launch interruption timestamps. DROP/ADD is transactional.
ALTER TABLE quality.run_attempts ALTER COLUMN started_at DROP NOT NULL;
ALTER TABLE quality.run_attempts ALTER COLUMN ended_at DROP NOT NULL;
ALTER TABLE quality.run_attempts DROP CONSTRAINT IF EXISTS run_attempts_check;
ALTER TABLE quality.run_attempts DROP CONSTRAINT IF EXISTS run_attempts_check1;
ALTER TABLE quality.run_attempts DROP CONSTRAINT IF EXISTS run_attempts_check2;
ALTER TABLE quality.run_attempts DROP CONSTRAINT IF EXISTS run_attempts_check3;
ALTER TABLE quality.run_attempts DROP CONSTRAINT IF EXISTS run_attempts_check4;
ALTER TABLE quality.run_attempts DROP CONSTRAINT IF EXISTS run_attempts_check5;
ALTER TABLE quality.run_attempts
  DROP CONSTRAINT IF EXISTS run_attempts_timestamp_consistency;
ALTER TABLE quality.run_attempts
  DROP CONSTRAINT IF EXISTS run_attempts_evidence_consistency;
ALTER TABLE quality.run_attempts
  DROP CONSTRAINT IF EXISTS run_attempts_interrupted_consistency;
ALTER TABLE quality.run_attempts
  DROP CONSTRAINT IF EXISTS run_attempts_threshold_consistency;
ALTER TABLE quality.run_attempts
  DROP CONSTRAINT IF EXISTS run_attempts_incomplete_consistency;
ALTER TABLE quality.run_attempts ADD CONSTRAINT run_attempts_timestamp_consistency
  CHECK (
    (execution_state = 'completed'
      AND started_at IS NOT NULL
      AND ended_at IS NOT NULL
      AND ended_at >= started_at)
    OR (execution_state = 'interrupted'
      AND (
        (started_at IS NULL AND ended_at IS NULL)
        OR (started_at IS NOT NULL
          AND ended_at IS NOT NULL
          AND ended_at >= started_at)
      ))
  ) NOT VALID;
ALTER TABLE quality.run_attempts ADD CONSTRAINT run_attempts_evidence_consistency
  CHECK (
    evidence_state <> 'complete'
    OR (execution_state = 'completed' AND samples > 0)
  ) NOT VALID;
ALTER TABLE quality.run_attempts ADD CONSTRAINT run_attempts_interrupted_consistency
  CHECK (
    execution_state <> 'interrupted'
    OR (evidence_state = 'incomplete' AND reported_verdict = 'incomplete')
  ) NOT VALID;
ALTER TABLE quality.run_attempts ADD CONSTRAINT run_attempts_threshold_consistency
  CHECK (
    reported_verdict NOT IN ('passed', 'failed_threshold')
    OR evidence_state = 'complete'
  ) NOT VALID;
ALTER TABLE quality.run_attempts ADD CONSTRAINT run_attempts_incomplete_consistency
  CHECK (
    reported_verdict <> 'incomplete'
    OR evidence_state = 'incomplete'
  ) NOT VALID;
ALTER TABLE quality.run_attempts
  VALIDATE CONSTRAINT run_attempts_timestamp_consistency;
ALTER TABLE quality.run_attempts
  VALIDATE CONSTRAINT run_attempts_evidence_consistency;
ALTER TABLE quality.run_attempts
  VALIDATE CONSTRAINT run_attempts_interrupted_consistency;
ALTER TABLE quality.run_attempts
  VALIDATE CONSTRAINT run_attempts_threshold_consistency;
ALTER TABLE quality.run_attempts
  VALIDATE CONSTRAINT run_attempts_incomplete_consistency;

CREATE TABLE IF NOT EXISTS quality.artifacts (
  run_id uuid NOT NULL,
  attempt integer NOT NULL,
  project_id text NOT NULL,
  name text NOT NULL CHECK (length(name) BETWEEN 1 AND 255),
  sha256 text NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
  bytes bigint NOT NULL CHECK (bytes >= 0),
  object_ref text CHECK (object_ref IS NULL OR length(object_ref) <= 2048),
  PRIMARY KEY (run_id, attempt, name),
  FOREIGN KEY (run_id, attempt, project_id)
    REFERENCES quality.run_attempts(run_id, attempt, project_id)
);

CREATE TABLE IF NOT EXISTS quality.metric_summaries (
  run_id uuid NOT NULL,
  attempt integer NOT NULL,
  project_id text NOT NULL,
  name text NOT NULL CHECK (length(name) BETWEEN 1 AND 255),
  metric_type text NOT NULL CHECK (length(metric_type) BETWEEN 1 AND 64),
  contains text NOT NULL CHECK (length(contains) BETWEEN 1 AND 64),
  values jsonb NOT NULL CHECK (jsonb_typeof(values) = 'object'),
  thresholds jsonb NOT NULL CHECK (jsonb_typeof(thresholds) = 'object'),
  PRIMARY KEY (run_id, attempt, name),
  FOREIGN KEY (run_id, attempt, project_id)
    REFERENCES quality.run_attempts(run_id, attempt, project_id)
);

CREATE TABLE IF NOT EXISTS quality.verdict_events (
  decision_id uuid PRIMARY KEY,
  run_id uuid NOT NULL,
  attempt integer NOT NULL,
  project_id text NOT NULL,
  verdict text NOT NULL CHECK (verdict IN ('passed', 'failed', 'incomplete')),
  reason text NOT NULL CHECK (length(reason) BETWEEN 1 AND 2000),
  decided_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  decided_by name NOT NULL DEFAULT current_user,
  FOREIGN KEY (run_id, attempt, project_id)
    REFERENCES quality.run_attempts(run_id, attempt, project_id)
);

CREATE OR REPLACE FUNCTION quality.has_project_access(
  requested_project_id text,
  actor name,
  access_kind text
) RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = quality, pg_catalog
AS $function$
  SELECT COALESCE(
    pg_has_role(
      actor,
      CASE access_kind
        WHEN 'reader' THEN p.reader_role
        WHEN 'writer' THEN p.writer_role
        WHEN 'verdict' THEN p.verdict_role
      END,
      'member'
    ),
    false
  )
  FROM quality.projects AS p
  WHERE p.project_id = requested_project_id;
$function$;

CREATE OR REPLACE FUNCTION quality.claim_run_attempt(
  p_run_id uuid,
  p_attempt integer,
  p_project_id text,
  p_manifest_sha256 text,
  p_final_sha256 text,
  p_payload_sha256 text,
  p_execution_state text,
  p_reported_verdict text,
  p_evidence_state text,
  p_started_at timestamptz,
  p_ended_at timestamptz,
  p_samples bigint
) RETURNS text
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = quality, pg_catalog
AS $function$
DECLARE
  existing quality.run_attempts%ROWTYPE;
BEGIN
  INSERT INTO quality.run_attempts (
    run_id, attempt, project_id, manifest_sha256, final_sha256,
    payload_sha256, execution_state, reported_verdict, evidence_state,
    started_at, ended_at, samples
  ) VALUES (
    p_run_id, p_attempt, p_project_id, p_manifest_sha256, p_final_sha256,
    p_payload_sha256, p_execution_state, p_reported_verdict, p_evidence_state,
    p_started_at, p_ended_at, p_samples
  )
  ON CONFLICT (run_id, attempt) DO NOTHING;

  IF FOUND THEN
    RETURN 'inserted';
  END IF;

  SELECT * INTO existing
  FROM quality.run_attempts
  WHERE run_id = p_run_id AND attempt = p_attempt;

  IF NOT FOUND
    OR existing.project_id IS DISTINCT FROM p_project_id
    OR existing.manifest_sha256 IS DISTINCT FROM p_manifest_sha256
    OR existing.final_sha256 IS DISTINCT FROM p_final_sha256
    OR existing.payload_sha256 IS DISTINCT FROM p_payload_sha256
    OR existing.execution_state IS DISTINCT FROM p_execution_state
    OR existing.reported_verdict IS DISTINCT FROM p_reported_verdict
    OR existing.evidence_state IS DISTINCT FROM p_evidence_state
    OR existing.started_at IS DISTINCT FROM p_started_at
    OR existing.ended_at IS DISTINCT FROM p_ended_at
    OR existing.samples IS DISTINCT FROM p_samples
  THEN
    RAISE EXCEPTION 'run attempt identity conflict';
  END IF;

  RETURN 'exact_replay';
END;
$function$;

DROP FUNCTION IF EXISTS quality.import_payload(jsonb);

CREATE OR REPLACE FUNCTION quality.import_payload(
  p_payload jsonb,
  p_unsigned_payload bytea
)
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = quality, pg_catalog
AS $function$
DECLARE
  expected_top text[] := ARRAY[
    'schema_version', 'identity', 'manifest_sha256', 'final_sha256',
    'payload_sha256', 'execution_state', 'reported_verdict', 'evidence_state',
    'ingestion_state', 'started_at', 'ended_at', 'samples', 'metrics', 'artifacts'
  ];
  expected_identity text[] := ARRAY['run_id', 'attempt', 'project_id'];
  expected_metric text[] := ARRAY[
    'name', 'type', 'contains', 'values', 'thresholds'
  ];
  expected_artifact text[] := ARRAY[
    'name', 'sha256', 'bytes', 'object_ref'
  ];
  identity jsonb;
  claim_state text;
  project_id text;
  run_id uuid;
  attempt integer;
BEGIN
  IF p_unsigned_payload IS NULL
    OR octet_length(p_unsigned_payload) = 0
    OR octet_length(p_unsigned_payload) > 1048576
  THEN
    RAISE EXCEPTION 'invalid quality import envelope';
  END IF;

  IF jsonb_typeof(p_payload) <> 'object'
    OR NOT (p_payload ?& expected_top)
    OR p_payload - expected_top <> '{}'::jsonb
    OR p_payload->>'schema_version' <> 'hyhome.quality-import/v1'
    OR p_payload->>'ingestion_state' <> 'pending'
    OR jsonb_typeof(p_payload->'identity') <> 'object'
    OR jsonb_typeof(p_payload->'metrics') <> 'array'
    OR jsonb_typeof(p_payload->'artifacts') <> 'array'
    OR convert_from(p_unsigned_payload, 'UTF8')::jsonb
      IS DISTINCT FROM p_payload - 'payload_sha256'
    OR encode(sha256(p_unsigned_payload), 'hex')
      IS DISTINCT FROM p_payload->>'payload_sha256'
  THEN
    RAISE EXCEPTION 'invalid quality import envelope';
  END IF;

  identity := p_payload->'identity';
  IF NOT (identity ?& expected_identity)
    OR identity - expected_identity <> '{}'::jsonb
    OR EXISTS (
      SELECT 1 FROM jsonb_array_elements(p_payload->'metrics') AS item
      WHERE jsonb_typeof(item) <> 'object'
        OR NOT (item ?& expected_metric)
        OR item - expected_metric <> '{}'::jsonb
    )
    OR EXISTS (
      SELECT 1 FROM jsonb_array_elements(p_payload->'artifacts') AS item
      WHERE jsonb_typeof(item) <> 'object'
        OR NOT (item ?& expected_artifact)
        OR item - expected_artifact <> '{}'::jsonb
    )
  THEN
    RAISE EXCEPTION 'invalid quality import envelope';
  END IF;

  run_id := (identity->>'run_id')::uuid;
  attempt := (identity->>'attempt')::integer;
  project_id := identity->>'project_id';
  IF NOT quality.has_project_access(project_id, session_user, 'writer') THEN
    RAISE EXCEPTION 'project writer authority required'
      USING ERRCODE = 'insufficient_privilege';
  END IF;

  claim_state := quality.claim_run_attempt(
    run_id,
    attempt,
    project_id,
    p_payload->>'manifest_sha256',
    p_payload->>'final_sha256',
    p_payload->>'payload_sha256',
    p_payload->>'execution_state',
    p_payload->>'reported_verdict',
    p_payload->>'evidence_state',
    (p_payload->>'started_at')::timestamptz,
    (p_payload->>'ended_at')::timestamptz,
    (p_payload->>'samples')::bigint
  );
  IF claim_state = 'exact_replay' THEN
    RETURN claim_state;
  END IF;

  INSERT INTO quality.artifacts (
    run_id, attempt, project_id, name, sha256, bytes, object_ref
  )
  SELECT
    run_id,
    attempt,
    project_id,
    item->>'name',
    item->>'sha256',
    (item->>'bytes')::bigint,
    item->>'object_ref'
  FROM jsonb_array_elements(p_payload->'artifacts') AS item;

  INSERT INTO quality.metric_summaries (
    run_id, attempt, project_id, name, metric_type, contains, values, thresholds
  )
  SELECT
    run_id,
    attempt,
    project_id,
    item->>'name',
    item->>'type',
    item->>'contains',
    item->'values',
    item->'thresholds'
  FROM jsonb_array_elements(p_payload->'metrics') AS item;

  RETURN claim_state;
END;
$function$;

REVOKE ALL ON FUNCTION quality.has_project_access(text, name, text) FROM PUBLIC;
REVOKE ALL ON FUNCTION quality.claim_run_attempt(
  uuid, integer, text, text, text, text, text, text, text,
  timestamptz, timestamptz, bigint
) FROM PUBLIC;
REVOKE ALL ON FUNCTION quality.import_payload(jsonb, bytea) FROM PUBLIC;

ALTER TABLE quality.run_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE quality.run_attempts FORCE ROW LEVEL SECURITY;
ALTER TABLE quality.artifacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE quality.artifacts FORCE ROW LEVEL SECURITY;
ALTER TABLE quality.metric_summaries ENABLE ROW LEVEL SECURITY;
ALTER TABLE quality.metric_summaries FORCE ROW LEVEL SECURITY;
ALTER TABLE quality.verdict_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE quality.verdict_events FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS run_attempts_select ON quality.run_attempts;
CREATE POLICY run_attempts_select ON quality.run_attempts FOR SELECT USING (
  current_user = 'perf_owner'::name
  OR quality.has_project_access(project_id, current_user, 'reader')
  OR quality.has_project_access(project_id, current_user, 'writer')
  OR quality.has_project_access(project_id, current_user, 'verdict')
);
DROP POLICY IF EXISTS run_attempts_insert ON quality.run_attempts;
CREATE POLICY run_attempts_insert ON quality.run_attempts FOR INSERT WITH CHECK (
  current_user = 'perf_owner'::name
  OR quality.has_project_access(project_id, current_user, 'writer')
);

DROP POLICY IF EXISTS artifacts_select ON quality.artifacts;
CREATE POLICY artifacts_select ON quality.artifacts FOR SELECT USING (
  current_user = 'perf_owner'::name
  OR quality.has_project_access(project_id, current_user, 'reader')
  OR quality.has_project_access(project_id, current_user, 'writer')
  OR quality.has_project_access(project_id, current_user, 'verdict')
);
DROP POLICY IF EXISTS artifacts_insert ON quality.artifacts;
CREATE POLICY artifacts_insert ON quality.artifacts FOR INSERT WITH CHECK (
  current_user = 'perf_owner'::name
  OR quality.has_project_access(project_id, current_user, 'writer')
);

DROP POLICY IF EXISTS metric_summaries_select ON quality.metric_summaries;
CREATE POLICY metric_summaries_select ON quality.metric_summaries FOR SELECT USING (
  current_user = 'perf_owner'::name
  OR quality.has_project_access(project_id, current_user, 'reader')
  OR quality.has_project_access(project_id, current_user, 'writer')
  OR quality.has_project_access(project_id, current_user, 'verdict')
);
DROP POLICY IF EXISTS metric_summaries_insert ON quality.metric_summaries;
CREATE POLICY metric_summaries_insert ON quality.metric_summaries FOR INSERT
WITH CHECK (
  current_user = 'perf_owner'::name
  OR quality.has_project_access(project_id, current_user, 'writer')
);

DROP POLICY IF EXISTS verdict_events_select ON quality.verdict_events;
CREATE POLICY verdict_events_select ON quality.verdict_events FOR SELECT USING (
  current_user = 'perf_owner'::name
  OR quality.has_project_access(project_id, current_user, 'reader')
  OR quality.has_project_access(project_id, current_user, 'writer')
  OR quality.has_project_access(project_id, current_user, 'verdict')
);
DROP POLICY IF EXISTS verdict_events_insert ON quality.verdict_events;
CREATE POLICY verdict_events_insert ON quality.verdict_events FOR INSERT
WITH CHECK (
  current_user = 'perf_owner'::name
  OR quality.has_project_access(project_id, current_user, 'verdict')
);

CREATE OR REPLACE VIEW quality.run_results
WITH (security_barrier = true, security_invoker = true)
AS
SELECT
  r.run_id,
  r.attempt,
  r.project_id,
  r.execution_state,
  r.reported_verdict,
  r.evidence_state,
  r.started_at,
  r.ended_at,
  r.samples,
  v.verdict AS official_verdict,
  v.decided_at AS verdict_decided_at
FROM quality.run_attempts AS r
LEFT JOIN LATERAL (
  SELECT e.verdict, e.decided_at
  FROM quality.verdict_events AS e
  WHERE e.run_id = r.run_id AND e.attempt = r.attempt
  ORDER BY e.decided_at DESC, e.decision_id DESC
  LIMIT 1
) AS v ON true;

REVOKE ALL ON ALL TABLES IN SCHEMA quality FROM PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE perf_owner IN SCHEMA quality
  REVOKE ALL ON TABLES FROM PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE perf_owner IN SCHEMA quality
  REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;

INSERT INTO quality.schema_migrations (version)
VALUES (1), (2)
ON CONFLICT (version) DO NOTHING;

COMMIT;
