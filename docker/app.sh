#!/bin/bash

cd /app/src

source ../.prod_env

if [ $DEBUG == 1 ]; then
      uvicorn main:app --host 0.0.0.0 --reload
else
      gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
fi