# Innonymous Api Server

#### A fastapi RESTful api server, that provides all functionality.

![Build Status](https://github.com/innonymous/api-server/actions/workflows/dockerhub.yml/badge.svg)

Innonymous is a mobile-ready anonymous chat, powered by python and React.js

- Light
- Fully anonymous
- High performance

## Quick start (You are needed Docker)

Example `.env` file:

```sh
API_AMQP_URL=amqp://guest:guest@localhost
API_DATABASE_URL=postgresql+asyncpg://username:password@host/innonymous
API_JWT_KEY=32 bytes in hex, can be generated as "openssl rand -hex 32"
```

Start with:

```sh
docker run --env-file .env -p 8000:8000 smthngslv/innonymous-api-server:latest
```
