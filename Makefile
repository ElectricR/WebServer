#!make
include .env
export $(cat .env | xargs)

push:
	docker push electricrainbow/pm-default-server-image:$(SERVER_VERSION)

build:
	docker-compose --env-file .env -f compose_build.yaml build

start:
	docker-compose --env-file .env -f compose.yaml up -d

stop:
	docker-compose --env-file .env -f compose.yaml down

clean:
	docker image rm electricrainbow/pm-default-server-image:$(SERVER_VERSION) mongo redis
	

healthcheck:
	which docker > /dev/null && echo "Docker is installed" || >&2 echo "Docker is not installed"
	which docker-compose > /dev/null && echo "Everything's ready" || >&2 echo "Docker-compose is not installed"


.PHONY: build start stop healthcheck clean push
