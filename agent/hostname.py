import socket

def resolve(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None
