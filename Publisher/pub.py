# python 3.6

import random
import time
import json
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

from paho.mqtt import client as mqtt_client


broker = '192.168.163.105' #broker.emqx.io
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'admin'
password = 'public'

#koneksi ke sensor
sensor = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1,
    xonxoff=0
)

master = modbus_rtu.RtuMaster(sensor)
master.set_timeout(2.0)
master.set_verbose(True)

dict_payload = dict()

def connect_mqtt():
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


def publish(client):
    #msg_count = 0
    while True:
        data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
        
        dict_payload["voltage"]= data[0] / 10.0
        dict_payload["current_A"] = (data[1] + (data[2] << 16)) / 1000.0 # [A]
        dict_payload["power_W"] = (data[3] + (data[4] << 16)) / 10.0 # [W]
        dict_payload["energy_Wh"] = data[5] + (data[6] << 16) # [Wh]
        dict_payload["frequency_Hz"] = data[7] / 10.0 # [Hz]
        dict_payload["power_factor"] = data[8] / 100.0
        dict_payload["alarm"] = data[9] # 0 = no alarm
        str_payload = json.dumps(dict_payload, indent=2)
        
        time.sleep(1)
        
        result = client.publish(topic, str_payload)
        status = result[0]
        if status == 0:
            print(f"Mengirim pesan {str_payload} ke {topic}")
        else:
            print(f"Gagal mengirim pesan ke {topic}")

try:
    master.close()
    if sensor.is_open:
        sensor.close()
except:
    pass

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
