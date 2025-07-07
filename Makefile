DC = docker-compose

.PHONY: build up down logs stop restart prune ps help

build-dev:
	$(DC) --profile development build

up-dev:
	$(DC) --profile development up -d

down-dev:
	$(DC) --profile development down

logs-dev:
	$(DC) --profile development logs -f


build-prod:
	$(DC) --profile production build

up-prod:
	$(DC) --profile production up -d

down-prod:
	$(DC) --profile production down

logs-prod:
	$(DC) --profile production logs -f

help:
	@echo "Available commands:"
	@echo "  make build-dev     — build containers (development profile)"
	@echo "  make up-dev        — start containers in background (development profile)"
	@echo "  make down-dev      — stop and remove containers (development profile)"
	@echo "  make logs-dev      — show container logs (development profile)"
	@echo "  make build-prod    — build containers (production profile)"
	@echo "  make up-prod       — start containers in background (production profile)"
	@echo "  make down-prod     — stop and remove containers (production profile)"
	@echo "  make logs-prod     — show container logs (production profile)"
	@echo "  make help          — this help message"
