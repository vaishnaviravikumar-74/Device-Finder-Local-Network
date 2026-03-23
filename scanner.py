import scapy.all as scapy
import socket
import requests

def get_manufacturer(mac):
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        return "Unknown"
    except:
        return "Unknown"

def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        return "Unknown"

def scan_network(ip_range):
    # Send ARP request to all devices in the network
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    # Capture responses
    answered = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)[0]

    devices = []

    for element in answered:
        ip = element[1].psrc
        mac = element[1].hwsrc

        device = {
            "IP Address": ip,
            "MAC Address": mac,
            "Hostname": get_hostname(ip),
            "Manufacturer": get_manufacturer(mac)
        }
        devices.append(device)

    return devices