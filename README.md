# The reports that slowed Tuesday

This is Northstar Ledger's reporting service, set up for the incident: a small Python HTTP service, a PostgreSQL database seeded with report history, and a load generator.

## Run it

You need Docker with Compose. Start the service and the database with:

```sh
make up
```

The API listens on `http://localhost:8081`, and `curl http://localhost:8081/health` tells you it's up. `make test` runs the checks in a container. `make down` removes the stack along with its local database volume.

## Evidence commands

`make load` sends the filtered report traffic and prints one summary line with the request count, how many succeeded, and p50 and p99 latency. `make explain` runs the same report query through `EXPLAIN (ANALYZE, BUFFERS)` inside PostgreSQL. `GET /version` returns the build label of the running service, and `deploys/` holds the diff of each deploy under that label, including this morning's.

The data is local training data. The service answers with a row count and a latency field instead of the full report rows, so `make load` measures the query and not your terminal.
