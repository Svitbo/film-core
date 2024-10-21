.ONESHELL: /usr/bin/bash

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
		--build \
		-d

core-apply-prod:
	docker compose -f compose.d/compose.yml \
		--env-file .env \
		up \
		--build \
		-d

core-destroy-dev:
	docker compose -f compose.d/compose.yml \
		-f compose.d/compose-dev.yml \
		--env-file .env \
		down \
		--volumes \
		--remove-orphans

core-destroy-prod:
	docker compose -f compose.d/compose.yml \
		--env-file .env \
		down \
		--remove-orphans
