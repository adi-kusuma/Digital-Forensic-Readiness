import time
import datetime
from scapy.all import *
import logging
import pickle
import ipaddress
from logging.handlers import TimedRotatingFileHandler

# Load the saved random forest model
with open('rf_model.pkl', 'rb') as f:
    rf = pickle.load(f)

# Configure the logging module for packet data
logging.basicConfig(filename='packet_log.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Configure the logging module for predictions with timed rotating file handler
prediction_logger = logging.getLogger('prediction_logger')
prediction_logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('prediction_log.log', when='H', interval=1, backupCount=0)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
prediction_logger.addHandler(handler)

# Define the initial timestamp and attack log filename
current_hour = datetime.datetime.now().strftime("%Y-%m-%d_%H")
attack_log_file = f'ddos_attack_log_{current_hour}.log'

# Define a function to handle incoming packets
def handle_packet(packet):
    global current_hour, attack_log_file  # Declare current_hour and attack_log_file as global variables

    # Check if the packet has a TCP layer
    if TCP in packet:
        # Extract relevant packet data
        pkt_length = len(packet)
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport

        # Preprocess the data
        src_ip_int = int(ipaddress.IPv4Address(src_ip))
        dst_ip_int = int(ipaddress.IPv4Address(dst_ip))
        
        st = time.time()
        # Make a prediction using the random forest model
        prediction = rf.predict([[pkt_length, src_ip_int, dst_ip_int, src_port, dst_port]])

        # Log the packet data along with the predicted label
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        et = time.time()
        pt = (et - st) * 1000
        pkt_data = f"{timestamp},{pkt_length},{src_ip},{dst_ip},{src_port},{dst_port}"
        logging.info(pkt_data)

        # Write the prediction to the prediction log file
        prediction_data = f"{timestamp},{prediction[0]},{pt}"
        prediction_logger.info(prediction_data)

        # Check if the prediction indicates a DDoS attack
        if prediction == 1:
            print('Possible DDoS attack detected!')
            # Check if a new hour has started
            if timestamp[:13] != current_hour:
                # Update the current hour and create a new attack log file
                current_hour = timestamp[:13]
                attack_log_file = f'ddos_attack_log_{current_hour}.log'
            
            # Save the prediction log to the current attack log file
            with open(attack_log_file, 'a') as f:
                f.write(f'Prediction: {prediction_data}\n')
        else:
            print('Normal packet')

# Sniff packets and call the handle_packet function for each packet
sniff(prn=handle_packet)

