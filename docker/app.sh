#!/bin/bash

cd ./app

alembic upgrade head

source .env && gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:9000