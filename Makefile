SERVICE =
DOCKER_COMPOSE=docker compose
DOCKER_COMPOSE_FILE=deployment/docker-manifests/docker-compose.yml


up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

shell:
	docker exec -it $(SERVICE) /bin/sh
