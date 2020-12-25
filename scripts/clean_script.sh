#!/bin/bash
docker rm -v $(docker ps -a -q)
docker rmi $(docker images -a | grep -oP '^(<none>).+\K\w{12}')
docker rmi $(docker images -a | grep -oP '^(electricrainbow).+\K\w{12}')
rm compose.yaml
