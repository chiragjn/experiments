#!/bin/bash

SLEEP_FOR=0.1 gunicorn --bind 0.0.0.0:8081 \
  --worker-class uvicorn.workers.UvicornWorker \
  --keep-alive 5 \
  app:app

