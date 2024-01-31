from scapy.all import *
import logging
import time
import pickle
import ipaddress
from logging.handlers import TimedRotatingFileHandler

# Load the saved random forest model
with open('rf_model.pkl', 'rb') as f:
    rf = pickle.load(f)

# configure the logging module for packet data
logging.basicConfig(filename='packet_log.log', level=logging.INFO, format='%(asctime)s %(message)s')

# configure the logging module for predictions with timed rotating file handler
prediction_logger = logging.getLogger('prediction_logger')
prediction_logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('prediction_log.log', when='H', interval=1, backupCount=0)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
prediction_logger.addHandler(handler)

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
        
        st = time.time()
        # make a prediction using the random forest model
        prediction = rf.predict([[pkt_length, src_ip_int, dst_ip_int, src_port, dst_port]])

        # log the packet data along with the predicted label
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        et = time.time()
        pt = (et - st) * 1000
        pkt_data = f"{timestamp},{pkt_length},{src_ip},{dst_ip},{src_port},{dst_port}"
        logging.info(pkt_data)

        # write the prediction to the prediction log file
        prediction_data = f"{timestamp},{prediction[0]},{pt}"
        prediction_logger.info(prediction_data)

        # check if the prediction indicates a DDoS attack
        if prediction == 1:
            print('Possible DDoS attack detected!')
            # Save the prediction log to a separate file
            attack_timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
            attack_log_file = f'ddos_attack_log_{attack_timestamp}.log'
            with open(attack_log_file, 'w') as f:
                f.write(f'Attack timestamp: {timestamp}\n')
                f.write(f'Packet data: {pkt_data}\n')
                f.write(f'Prediction: {prediction_data}\n')
        else:
            print('Normal packet')

# sniff packets and call the handle_packet function for each packet
sniff(prn=handle_packet)

