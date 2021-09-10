#!/bin/sh

# Exit if there is an error.
set -e;

# Run migration.
./env/bin/alembic --config ./config/alembic.ini upgrade head;

# Start server.
./env/bin/gunicorn --config ./config/gunicorn.conf.py innonymous.api:app "$*";
