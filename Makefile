.PHONY: up down test load explain

export COMPOSE_PROJECT_NAME=slow_tuesday

up:
	docker compose up -d --build db api

down:
	docker compose down -v --remove-orphans

test:
	docker compose run --rm --build test

load:
	docker compose run --rm --build loadgen

explain:
	docker compose exec db psql -U reports -d reports -c "EXPLAIN (ANALYZE, BUFFERS) SELECT id, report_type, created_at, total_cents FROM reports WHERE report_type = 'reconciliation' AND created_at >= now() - interval '7 days';"
