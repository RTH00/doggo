#! /bin/bash

ENV_FILE="${1}"

if [ -z "${ENV_FILE}" ]; then
    echo "Usage: ${0} [env file]"
    exit 1
fi

set -e

echo "Sourcing env"
. "${ENV_FILE}"
cd doggo
echo "Migrating DB"
python3 manage.py migrate
echo "Collecting statics"
python3 manage.py collectstatic --no-input

echo "Starting gunicorn"
gunicorn  -b 0.0.0.0:8000 --workers=4 doggo.wsgi
