docker-up:
	@docker compose -f ./.infra/docker/docker-compose.yaml --env-file ./.env up -d --build

docker-down:
	@docker compose -f ./.infra/docker/docker-compose.yaml --env-file ./.env down --remove-orphans --volumes

docker-db-up:
	@docker compose -f ./.infra/docker/docker-compose.yaml --env-file ./.env up -d db

docker-db-down:
	@docker compose -f ./.infra/docker/docker-compose.yaml --env-file ./.env down db

docker-pg-up:
	@docker compose -f ./.infra/docker/docker-compose.yaml --env-file ./.env up -d pg

docker-pg-down:
	@docker compose -f ./.infra/docker/docker-compose.yaml --env-file ./.env down pg

migration-create:
	@cd ./.infra/migracao && poetry run alembic revision --autogenerate -m $(name)

migration-create-new:
	@cd ./.infra/migracao && poetry run alembic revision -m $(name) 

migration-upgrade:
	@cd ./.infra/migracao && poetry run alembic upgrade head

migration-downgrade:
	@cd ./.infra/migracao && poetry run alembic downgrade -1

migration-history:
	@cd ./.infra/migracao && poetry run alembic history

run-tests:
	@pytest