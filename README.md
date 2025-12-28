# iWebIT_Network_Discovery

Agente Linux para descoberta de dispositivos de rede usando ARP Scan + Nmap.

## Funcionalidades
- Redes definidas manualmente
- Descoberta IP / MAC / Vendor
- Resolução de hostname
- Detecção de SO (Nmap)
- Execução automática via systemd
- Auto-update via GitHub
- Logs e cache local

## Instalação
git clone https://github.com/RDFonseca82/iWebIT_Network_Discovery.git /opt/iWebIT_Network_Discovery
cd /opt/iWebIT_Network_Discovery
sudo ./install.sh

## Desinstalação
sudo systemctl stop iwebit_network_discovery.service
sudo systemctl disable iwebit_network_discovery.timer
sudo rm -rf /opt/iWebIT_Network_Discovery
sudo rm /etc/systemd/system/iwebit_network_discovery.service
sudo rm /etc/systemd/system/iwebit_network_discovery.timer
sudo systemctl daemon-reload
