from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle
import ipaddress
import numpy as np

df = pd.read_csv('coba.log', header=None, names=['timestamp', 'length', 'src_ip', 'dst_ip', 'src_port', 'dst_port', 'label'])

df['label'] = df['label'].fillna(0).astype(int)
df.dropna(subset=['label'], inplace=True)
df['label'] = df['label'].astype(int) # convert label to integer
df = df.drop('timestamp', axis=1)
df['src_ip'] = df['src_ip'].fillna('0.0.0.0') # replace missing values with a default value
df['src_ip'] = df['src_ip'].apply(lambda x: int(ipaddress.IPv4Address(x))) # convert source IP address to integer
df['dst_ip'] = df['dst_ip'].fillna('0.0.0.0') # replace missing values with a default value
df['dst_ip'] = df['dst_ip'].apply(lambda x: int(ipaddress.IPv4Address(x))) # convert destination IP address to integer

print('kosong :',df.isna().sum())
print('gg:',df.isin([np.inf, -np.inf]).sum())
df.dropna(inplace=True)

X = df.drop('label', axis=1) # input features
y = df['label'] # target variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)


#save the model
with open('model_2024.pkl', 'wb') as f:
    pickle.dump(rf, f)
y_pred = rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

