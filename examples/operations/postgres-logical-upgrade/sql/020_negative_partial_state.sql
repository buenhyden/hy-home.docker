\set ON_ERROR_STOP on

CREATE TABLE rehearsal_partial_state_marker (
    id integer PRIMARY KEY
);

DO $$
BEGIN
    RAISE EXCEPTION 'intentional partial-state rehearsal failure';
END
$$;
