from scapy.all import *
import logging
import time
import pickle
import ipaddress
import time
# Load the saved random forest model
with open('rf_model.pkl', 'rb') as f:
    rf = pickle.load(f)

# configure the logging module for packet data
logging.basicConfig(filename='packet_log.log', level=logging.INFO, format='%(asctime)s %(message)s')

# configure the logging module for predictions
logging.basicConfig(filename='prediction_log.log', level=logging.INFO, format='%(asctime)s %(message)s')

# define a function to handle incoming packets
def handle_packet(packet):
    # check if the packet has a TCP layer
    if TCP in packet:
        # extract relevant packet data
        pkt_length = len(packet)
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport

        # preprocess the data
        src_ip_int = int(ipaddress.IPv4Address(src_ip))
        dst_ip_int = int(ipaddress.IPv4Address(dst_ip))
        
        st=time.time()
        # make a prediction using the random forest model
        prediction = rf.predict([[pkt_length, src_ip_int, dst_ip_int, src_port, dst_port]])

        # log the packet data along with the predicted label
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        et=time.time()
        pt=(et-st)*1000
        pkt_data = f"{timestamp},{pkt_length},{src_ip},{dst_ip},{src_port},{dst_port}"
        logging.info(pkt_data)

        # write the prediction to the prediction log file
        prediction_data = f"{timestamp},{prediction[0]},{pt}"
        logging.info(prediction_data)

        # check if the prediction indicates a DDoS attack
        if prediction == 1:
            print('Possible DDoS attack detected!')
        else:
	        print('Normal packet')
            
# sniff packets and call the handle_packet function for each packet
sniff(prn=handle_packet)
