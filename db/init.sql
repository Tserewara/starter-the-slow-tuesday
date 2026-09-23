CREATE TABLE reports (
    id bigint PRIMARY KEY,
    report_type text NOT NULL,
    created_at timestamptz NOT NULL,
    total_cents integer NOT NULL
);

INSERT INTO reports (id, report_type, created_at, total_cents)
SELECT n,
       CASE WHEN n % 300 = 0 THEN 'reconciliation' ELSE 'daily' END,
       now() - ((n % 29) || ' days')::interval,
       1000 + (n % 50000)
FROM generate_series(1, 5000000) AS n;

ANALYZE reports;
