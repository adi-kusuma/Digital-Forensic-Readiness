# python3.6

import random
import json
import requests
import modbus_tk.defines as cst

from modbus_tk import modbus_rtu
from paho.mqtt import client as mqtt_client


#broker = '172.20.10.10'
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'admin'
password = 'kaito1412'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, str_payload):
        print(f"Menerima pesan {str_payload.payload.decode()} dari {str_payload.topic}")
        data = {str_payload.payload.decode()}
        json_str = json.dumps(list(data))
        res = requests.post('http://127.0.0.1:5000/arraymqtt', json=json_str)
        returned_data = res.json()
        print(returned_data)
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
