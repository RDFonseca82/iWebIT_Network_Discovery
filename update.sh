#!/bin/bash

BASE="/opt/iWebIT_Network_Discovery"
cd "$BASE" || exit 1

git fetch origin

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    systemctl stop iwebit_network_discovery.service
    git pull origin main
    systemctl start iwebit_network_discovery.service
fi
