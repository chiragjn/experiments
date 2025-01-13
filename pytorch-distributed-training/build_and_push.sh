#!/bin/bash
set -ex

TAG=0.2.0
DOCKER_BUILDKIT=0 docker build \
    --platform linux/amd64 \
    -t docker.io/chiragjn/pytorch-distributed-training:$TAG \
    -t docker.io/chiragjn/pytorch-distributed-training:latest \
    --cache-from docker.io/chiragjn/pytorch-distributed-training:latest \
    .
docker push chiragjn/pytorch-distributed-training:$TAG
docker push chiragjn/pytorch-distributed-training:latest
