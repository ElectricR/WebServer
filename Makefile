
push:
	docker push electricrainbow/pm-default-server-image:v3.0.0

build:
	docker-compose -f compose_build.yaml build

start:
	docker-compose -f compose.yaml up -d

stop:
	docker-compose -f compose.yaml down

clean:
	docker image rm electricrainbow/pm-default-server-image:v3.0.0 mongo redis
	

healthcheck:
	which docker > /dev/null && echo "Docker is installed" || >&2 echo "Docker is not installed"
	which docker-compose > /dev/null && echo "Everything's ready" || >&2 echo "Docker-compose is not installed"


.PHONY: build start stop healthcheck clean push
