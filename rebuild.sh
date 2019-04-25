#!/usr/bin/env sh
./stop.sh
docker-compose build
./start.sh
