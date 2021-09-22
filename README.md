# Innonymous Api Server

NOTE: this repo is a part of project, see [full README](https://github.com/innonymous/compose) first


#### A fastapi RESTful api server, that provides all functionality.

![Build Status](https://github.com/innonymous/api-server/actions/workflows/dockerhub.yml/badge.svg)

Innonymous is a mobile-ready anonymous chat, powered by python and React.js

- Light
- Fully anonymous
- High performance12345678901234567890123456789012

## Quick start (You are needed Docker)
Example `.env` file:
```sh
API_DATABASE_URL=postgresql+asyncpg://username:password@host/innonymous
API_JWT_KEY=32 bytes in hex, can be generated as "openssl rand -hex 32"
```

## Start with:
```sh
docker run --env-file .env -p 8000:8000 smthngslv/innonymous-api-server:latest
```
