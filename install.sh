#!/bin/bash

apt update
apt install -y arp-scan nmap git python3

INSTALL_PATH="/opt/iWebIT_Network_Discovery"

git clone https://github.com/TEU_USER/iWebIT_Network_Discovery.git "$INSTALL_PATH"

chmod +x "$INSTALL_PATH/update.sh"

cp "$INSTALL_PATH/systemd/iwebit_network_discovery.service" /etc/systemd/system/
cp "$INSTALL_PATH/systemd/iwebit_network_discovery.timer" /etc/systemd/system/

systemctl daemon-reexec
systemctl enable iwebit_network_discovery.timer
systemctl start iwebit_network_discovery.timer
