#!/usr/bin/env bash

echo "Input number to choice action"
echo "1: build"
echo "2: run bot"
echo "3: deploy docker dev contain"
echo "4: deploy docker prod contain"

read action

if [[ "$action" == "1" ]]; then
    /bin/bash ./script/build-image.sh
elif [[ "$action" == "2" ]]; then
    python3 ./bot.py
elif [[ "$action" == "3" ]]; then
    cd docker
    docker compose -p bot_dev --profile dev up -d
elif [[ "$action" == "4" ]]; then
    cd docker
    docker compose -p bot --profile prod up -d
fi
