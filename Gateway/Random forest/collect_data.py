import numpy as np
import pandas as pd
import scapy.all as sc
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
# Capture network traffic data using Scapy
pkts = sc.sniff(count=5000)

# Preprocess the data and extract relevant features
features = []
labels = []

for pkt in pkts:
    # Extract features such as packet size, source/destination IP address, and port number
    pkt.show()
    pkt_features = [len(pkt), pkt[sc.IP].src, pkt[sc.IP].dst, pkt[sc.TCP].sport, pkt[sc.TCP].dport]
    
    # Determine if packet is part of a DoS attack or not
    if pkt_features[0] > 1000:  # if packet size is greater than 1500 bytes, consider it an attack
        labels.append(1)  # 1 represents attack
    else:
        labels.append(0)  # 0 represents normal traffic
    
    features.append(pkt_features)

# Convert the data to a pandas DataFrame
data = pd.DataFrame(features, columns=['PacketSize', 'SrcIP', 'DstIP', 'SrcPort', 'DstPort'])
data['Label'] = labels

# Encode categorical features such as IP addresses and port numbers
data = pd.get_dummies(data, columns=['SrcIP', 'DstIP', 'SrcPort', 'DstPort'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data.drop('Label', axis=1), data['Label'], test_size=0.2, random_state=42)

# Train the Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Test the model
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: {:.2f}%".format(accuracy * 100))

with open('dos_detection_model.pkl', 'wb') as f:
    pickle.dump(rf, f)
