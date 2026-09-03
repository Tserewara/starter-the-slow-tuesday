# The reports that slowed Tuesday

This repository is the Northstar Ledger reporting service used in the incident exercise. It includes a Python HTTP service, a PostgreSQL database seeded with report history, and a small load generator.

## Run it

You need Docker with Compose. Start the service and database with:

```sh
make up
```

The API is at `http://localhost:8081`. Check it with `curl http://localhost:8081/health`. `make test` runs the checks in a container, and `make down` removes the stack and its local database volume.

## Evidence commands

`make load` sends the filtered report traffic and prints p50 and p99 latency. `make explain` runs the same report predicate through `EXPLAIN (ANALYZE, BUFFERS)` inside PostgreSQL. `GET /version` exposes the build label that appears in the supplied deployment history.

The database is local training data. The service returns a count and latency field rather than the full report rows so the load output measures the query path instead of terminal bandwidth.
