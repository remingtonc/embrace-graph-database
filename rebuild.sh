#!/usr/bin/env sh
docker-compose down && docker-compose build && docker-compose up -d
