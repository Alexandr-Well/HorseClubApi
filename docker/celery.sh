#!/bin/bash

if [[ "${1}" == "worker" ]]; then
  celery --app=src.celery.tasks:celery worker -l info
elif [[ "${1}" == "flower" ]]; then
  celery --app=src.celery.tasks:celery flower
fi
