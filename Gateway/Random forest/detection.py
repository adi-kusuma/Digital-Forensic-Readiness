import scapy.all as sc
import pandas as pd
from sklearn.externals import joblib

# Load the trained Random Forest model
model = joblib.load('random_forest_model.pkl')

# Define the target IP address and port number to monitor
target_ip = '192.168.1.100'
target_port = 80

# Define the packet processing function
def process_packet(pkt):
    # Extract features from the packet
    pkt_features = [len(pkt), pkt[sc.IP].src, pkt[sc.IP].dst, pkt[sc.TCP].sport, pkt[sc.TCP].dport]

    # Convert the features to a pandas DataFrame
    data = pd.DataFrame([pkt_features], columns=['PacketSize', 'SrcIP', 'DstIP', 'SrcPort', 'DstPort'])

    # Encode categorical features such as IP addresses and port numbers
    data = pd.get_dummies(data, columns=['SrcIP', 'DstIP', 'SrcPort', 'DstPort'])

    # Use the trained model to predict if the packet is part of a DoS attack or not
    prediction = model.predict(data)

    if prediction[0] == 1:
        print('DoS attack detected from {}'.format(pkt[sc.IP].src))
    else:
        print('Normal traffic from {}'.format(pkt[sc.IP].src))

# Start sniffing network traffic and process each packet in real-time
sc.sniff(filter='tcp and host {}'.format(target_ip), prn=process_packet)
