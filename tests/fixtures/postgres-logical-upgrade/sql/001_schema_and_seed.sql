\set ON_ERROR_STOP on

CREATE TABLE rehearsal_schema_version (
    version integer PRIMARY KEY
);

INSERT INTO rehearsal_schema_version (version) VALUES (1);

CREATE TABLE accounts (
    id bigint PRIMARY KEY,
    code text UNIQUE NOT NULL,
    balance numeric NOT NULL CHECK (balance >= 0)
);

INSERT INTO accounts (id, code, balance) VALUES
    (1, 'acct-alpha', 100.00),
    (2, 'acct-beta', 250.50),
    (3, 'acct-gamma', 49.50);

CREATE TABLE orders (
    id bigint PRIMARY KEY,
    account_id bigint NOT NULL REFERENCES accounts(id),
    amount numeric NOT NULL CHECK (amount > 0),
    state text NOT NULL CHECK (state IN ('open', 'paid'))
);

INSERT INTO orders (id, account_id, amount, state) VALUES
    (1, 1, 20.00, 'open'),
    (2, 1, 30.50, 'paid'),
    (3, 2, 100.00, 'paid'),
    (4, 3, 1.25, 'open');
