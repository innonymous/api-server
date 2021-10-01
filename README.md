# Innonymous Api Server

> NOTE: this repo is a part of project, see [full README](https://github.com/innonymous/compose) first


#### A fastapi RESTful api server, that provides all functionality.

![Build Status](https://github.com/innonymous/api-server/actions/workflows/dockerhub.yml/badge.svg)

Innonymous server is a fast and easy backend for chating, powered by python FastAPI

- Light
- Fully anonymous
- High performance

## Architecture brief view

Server backend is very easy, understandable and fast:

<p align="center">
<img src="images/arch_back.png"/>
</p>


## Quick start

1. Configure `.env` file:

```sh
API_AMQP_URL=amqp://guest:guest@localhost
API_DATABASE_URL=postgresql+asyncpg://username:password@host/innonymous
API_JWT_KEY=32 bytes in hex, can be generated as "openssl rand -hex 32"
```

2. Start backend using docker

```sh
docker run --env-file .env -p 8000:8000 smthngslv/innonymous-api-server:latest
```
