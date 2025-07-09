DC = docker-compose

.PHONY: build up down logs help


ifeq ($(OS), Windows_NT)
    CLEAR_COMMAND = type nul > .env
else
    CLEAR_COMMAND = rm .env
endif


# --- Production Commands ---

build-prod:
	-$(CLEAR_COMMAND)
	echo MYSQL_PASSWORD=$(shell openssl rand -base64 32) >> .env
	$(DC) -f docker-compose-prod.yml build

up-prod:
	$(DC) -f docker-compose-prod.yml up -d

down-prod:
	$(DC) -f docker-compose-prod.yml down

logs-prod:
	$(DC) -f docker-compose-prod.yml logs -f


# --- Development Commands ---

build-dev:
	-$(CLEAR_COMMAND)
	echo MYSQL_PASSWORD=$(shell openssl rand -base64 32) >> .env
	$(DC) -f docker-compose-dev.yml build

up-dev:
	$(DC) -f docker-compose-dev.yml up

down-dev:
	$(DC) -f docker-compose-dev.yml down

logs-dev:
	$(DC) -f docker-compose-dev.yml logs -f


# --- Help ---

help:
	@echo "Available commands:"
	@echo " make build-prod - Build production containers"
	@echo " make up-prod    - Deploy production stack to Swarm"
	@echo " make down-prod  - Remove production stack"
	@echo " make logs-prod  - Show production logs"
	@echo ""
	@echo " make build-dev  - Build development containers"
	@echo " make up-dev     - Start development containers"
	@echo " make down-dev   - Stop and remove development containers"
	@echo " make logs-dev   - Show development logs"
	@echo ""
	@echo " make help       - Show this help message"

