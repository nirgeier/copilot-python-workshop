#!/bin/bash

# Dynamically detect IMAGE_TAG based on OS using uname
os=$(uname -s)
case $os in
    Darwin)
        export IMAGE_TAG=macos
        ;;
    Linux)
        export IMAGE_TAG=linux
        ;;
    CYGWIN*|MINGW*|MSYS*)
        export IMAGE_TAG=win
        ;;
    *)
        export IMAGE_TAG=linux
        ;;
esac

docker compose build  --no-cache
docker compose up     --build     --force-recreate
docker compose push

docker  stop  copilot-python-workshop
docker  rm    copilot-python-workshop

docker  run                                                                   \
        --name copilot-python-workshop                                                            \
        -p 3000:3000                                                          \
        -p 4200:4200                                                          \
        -v ${PWD}/copilot-python-workshop:/app/src/copilot-python-workshop/   \
        nirgeier/copilot-python-workshop:$IMAGE_TAG

