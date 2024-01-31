from scapy.all import *
import logging
from datetime import datetime
import time
# configure the logging module
logging.basicConfig(filename='coba.log', level=logging.INFO, format='%(asctime)s %(message)s')

# define the attack threshold
attack_threshold = 1000

# define a function to handle incoming packets
def handle_packet(packet):
    # check if the packet has a TCP layer
    if TCP in packet:
        # extract relevant packet data and log it along with the label
        pkt_length = len(packet)
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        label = '1'
       
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pkt_data = f"{timestamp},{pkt_length},{src_ip},{dst_ip},{src_port},{dst_port},{label}"
        logging.info(pkt_data)

# sniff packets and call the handle_packet function for each packet
sniff(prn=handle_packet)

