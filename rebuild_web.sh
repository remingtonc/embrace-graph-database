#!/usr/bin/env sh
docker-compose build web && docker-compose up --no-deps -d web
