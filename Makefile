#!make
include .env
export $(cat .env | xargs)

push:
	echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin; \
	docker push electricrainbow/pm-default-server-image:$(SERVER_VERSION); \
	docker push electricrainbow/pm-balancer-server-image:$(BALANCER_VERSION); \

build:
	docker-compose -f compose_build.yaml --env-file .env build

start: compose.yaml
	docker-compose -f compose.yaml --env-file .env up 

compose.yaml:
	python3 ./scripts/create_compose.py

stop:
	docker-compose -f compose.yaml --env-file .env down

test: compose.yaml
	python3 test_server.py

clean:
	./scripts/clean_script.sh

lint:
	flake8 balancer.py controller.py repository.py server.py service.py test_server.py utils.py ./scripts/create_compose.py

autopep:
	autopep8 -i balancer.py controller.py repository.py server.py service.py test_server.py utils.py ./scripts/create_compose.py

healthcheck:
	which docker > /dev/null && echo "Docker is installed" || >&2 echo "Docker is not installed"; \
	which flake8 > /dev/null && echo "Flake8 is installed" || >&2 echo "Flake8 is not installed"; \
	which docker-compose > /dev/null && echo "Docker-compose is installed" || >&2 echo "Docker-compose is not installed"; \
	which autopep8 > /dev/null && echo "Everything's ready" || >&2 echo "Autopep8 is not installed";


.PHONY: test build start stop healthcheck clean push
