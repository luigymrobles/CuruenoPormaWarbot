#!make
include .env
SHELL := /bin/bash

TAIL_LOGS = 50

dev: complete-build sh

complete-build: build up

build:
	docker buildx build --platform linux/amd64 \
						--output type=docker \
						-t ${DOCKER_CONTAINER_NAME}_image .
	docker tag ${DOCKER_CONTAINER_NAME}_image ${REGISTRY}:${REGISTRY_PORT}/${DOCKER_CONTAINER_NAME}_image

up:
	docker compose up --force-recreate -d

down:
	docker compose down

sh:
	docker exec -it ${DOCKER_CONTAINER_NAME} bash

logs:
	docker logs --tail ${TAIL_LOGS} -f ${DOCKER_CONTAINER_NAME}

start-registry:
	docker run -d -p ${REGISTRY_PORT}:5000 --restart=always --name "${REGISTRY_NAME}" registry:2