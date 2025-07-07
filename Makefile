DC = docker-compose

.PHONY: build up down logs stop restart prune ps help

build:
	$(DC) build

up:
	$(DC) up -d

down:
	$(DC) down

logs:
	$(DC) logs -f

stop:
	$(DC) stop

restart:
	$(DC) restart

prune:
	docker system prune -f

ps:
	$(DC) ps

help:
	@echo "Available commands:"
	@echo "  make build    — build containers"
	@echo "  make up       — start containers in background"
	@echo "  make down     — stop and remove containers"
	@echo "  make logs     — show container logs"
	@echo "  make stop     — stop containers"
	@echo "  make restart  — restart containers"
	@echo "  make prune    — clean up unused docker resources"
	@echo "  make ps       — list containers"
	@echo "  make help     — this help message"
