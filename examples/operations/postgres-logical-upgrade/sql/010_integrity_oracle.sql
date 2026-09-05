\set ON_ERROR_STOP on

SELECT json_build_object(
    'schema_version', (
        SELECT version
        FROM rehearsal_schema_version
    ),
    'server_version_num', current_setting('server_version_num')::integer,
    'table_count', (
        SELECT count(*)
        FROM pg_class
        WHERE relnamespace = 'public'::regnamespace
          AND relkind = 'r'
    ),
    'account_count', (
        SELECT count(*)
        FROM accounts
    ),
    'order_count', (
        SELECT count(*)
        FROM orders
    ),
    'balance_sum', (
        SELECT sum(balance)
        FROM accounts
    ),
    'order_amount_sum', (
        SELECT sum(amount)
        FROM orders
    ),
    'account_digest', (
        SELECT md5(string_agg(
            id::text || '|' || code || '|' || balance::text,
            E'\n' ORDER BY id
        ))
        FROM accounts
    ),
    'order_digest', (
        SELECT md5(string_agg(
            id::text || '|' || account_id::text || '|' || amount::text || '|' || state,
            E'\n' ORDER BY id
        ))
        FROM orders
    ),
    'foreign_key_orphan_count', (
        SELECT count(*)
        FROM orders AS child
        LEFT JOIN accounts AS parent ON parent.id = child.account_id
        WHERE parent.id IS NULL
    ),
    'constraint_count', (
        SELECT count(*)
        FROM pg_constraint
        WHERE conrelid IN (
            'rehearsal_schema_version'::regclass,
            'accounts'::regclass,
            'orders'::regclass
        )
          AND contype IN ('p', 'u', 'f', 'c')
    )
);
