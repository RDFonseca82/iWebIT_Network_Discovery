#!/bin/bash

echo "========================================"
echo " iWebIT Network Discovery - Installer"
echo "========================================"
echo ""

read -p "Enter IdCompany: " IDCOMPANY

if [ -z "$IDCOMPANY" ]; then
    echo "IdCompany is mandatory. Installation aborted."
    exit 1
fi

apt update
apt install -y arp-scan nmap git python3

INSTALL_PATH="/opt/iWebIT_Network_Discovery"

if [ -d "$INSTALL_PATH" ]; then
    echo "Directory already exists. Aborting."
    exit 1
fi

git clone https://github.com/TEU_USER/iWebIT_Network_Discovery.git "$INSTALL_PATH"

# Guardar IdCompany no config
sed -i "s/^IdCompany=.*/IdCompany=$IDCOMPANY/" \
    "$INSTALL_PATH/config/agent.conf"

chmod +x "$INSTALL_PATH/update.sh"

cp "$INSTALL_PATH/systemd/iwebit_network_discovery.service" /etc/systemd/system/
cp "$INSTALL_PATH/systemd/iwebit_network_discovery.timer" /etc/systemd/system/

systemctl daemon-reexec
systemctl enable iwebit_network_discovery.timer
systemctl start iwebit_network_discovery.timer

echo ""
echo "Installation completed successfully."
echo "IdCompany = $IDCOMPANY"
