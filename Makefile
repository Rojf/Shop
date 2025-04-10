.PHONY: up down shell local-up local-build local-down migrate

SERVICES = cart catalog orders payment
PORTS = 8000 8001 8002 8003
DOCKER_COMPOSE=docker compose
DOCKER_COMPOSE_FILE=deployment/docker-manifests/docker-compose.yml


define migrate
	export PYTHONPATH=$PYTHONPATH:src; \
	for service in $(SERVICES); do \
		echo "\033[1;34mChecking migrations for $$service service\033[0m"; \
		if ! poetry run python src/$$service/manage.py migrate --check; then \
			echo "\033[1;33mMigrations are pending for $$service, applying...\033[0m"; \
			poetry run python src/$$service/manage.py migrate; \
		else \
			echo "\033[1;32m$$service migrations are already up-to-date.\033[0m"; \
		fi \
	done
endef


up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d


down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down


shell:
	docker exec -it $(SERVICE)_service /bin/sh


local-build:
	poetry install
	@$(call migrate)


local-down:
	@echo "Stopping all servers on the specified ports..."

	@for port in $(PORTS); do \
		ps aux | grep "[p]ython.*runserver.*$$port" | awk '{print $$2}' | xargs kill; \
		echo "The process on port [$$port] has been stopped."; \
	done

	@(ps aux | grep "[c]elery.*-A.*celery_app.*worker.*--loglevel=INFO" | awk '{print $$2}' | xargs kill)


local-up:
	@echo "Running local servers and Celery worker."
	@echo "These ports are used in backend services: $$ports !!!"

	@i=0; \
	export PYTHONPATH=$PYTHONPATH:src; \
	for service in $(SERVICES); do \
		port=$$(echo $(PORTS) | cut -d ' ' -f $$((i+1))); \
		echo "Running $$service service on port $$port"; \
		nohup poetry run python src/$$service/manage.py runserver $$port & \
		i=$$((i+1)); \
	done

	@export DJANGO_SETTINGS_MODULE=src.notification.settings; \
	nohup poetry run celery -A src.notification.celery_app worker --loglevel=INFO &
