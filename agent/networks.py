import ipaddress

def load_networks(path):
    networks = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                networks.append(str(ipaddress.ip_network(line, strict=False)))
            except ValueError:
                pass

    return networks
