#!make
include .env
export $(cat .env | xargs)

push:
	echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin; \
	docker push electricrainbow/pm-default-server-image:$(SERVER_VERSION); \
	docker push electricrainbow/pm-balancer-server-image:$(BALANCER_VERSION); \

build:
	docker-compose -f compose_build.yaml --env-file .env build

start:
	docker-compose -f compose.yaml --env-file .env up 

stop:
	docker-compose -f compose.yaml --env-file .env down

test:
	python3 test_server.py

clean:
	./clean_script.sh
	

healthcheck:
	which docker > /dev/null && echo "Docker is installed" || >&2 echo "Docker is not installed"
	which docker-compose > /dev/null && echo "Everything's ready" || >&2 echo "Docker-compose is not installed"


.PHONY: build start stop healthcheck clean push
