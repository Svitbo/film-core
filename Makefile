.ONESHELL: /usr/bin/bash
.PHONY: core*

# Dependency building targets

venv:
	python3 -m venv venv
	. venv/bin/activate
	pip3 install -r requirements.txt

# Docker Compose targets

core-apply-dev:
	docker compose -f compose.d/compose.yml \
		-f compose.d/compose-dev.yml \
		--env-file .env \
		up \
		-t 3 \
		--build \
		-d

core-apply-prod:
	docker compose -f compose.d/compose.yml \
		--env-file .env \
		up \
		-t 3 \
		--build \
		-d

core-destroy-dev:
	docker compose -f compose.d/compose.yml \
		-f compose.d/compose-dev.yml \
		--env-file .env \
		down \
		-t 3 \
		--volumes

core-destroy-prod:
	docker compose -f compose.d/compose.yml \
		--env-file .env \
		down \
		-t 3

core-backend-logs:
	docker compose -f compose.d/compose.yml \
		-f compose.d/compose-dev.yml \
		logs -f \
		backend
