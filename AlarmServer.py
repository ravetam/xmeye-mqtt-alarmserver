#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, struct, json
import paho.mqtt.client as mqtt
import yaml
from time import sleep
from socket import *
from datetime import *

port = "15002"
server = socket(AF_INET, SOCK_STREAM)
server.bind(("0.0.0.0", int(port)))
# server.settimeout(0.5)
server.listen(1)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

with open('config.yaml', 'r') as file:
    settings = yaml.load(file, Loader=yaml.FullLoader)

mqtt_address = settings['MQTT_ADDRESS']
mqtt_port = settings['MQTT_PORT']
mqtt_username = settings['MQTT_USERNAME']
mqtt_password = settings['MQTT_PASSWORD']

client = mqtt.Client("cameras") 
client.on_connect = on_connect
client.username_pw_set(username=mqtt_username,password=mqtt_password)
print("Connecting...")
client.connect(mqtt_address, mqtt_port)

def GetIP(s):
    return inet_ntoa(struct.pack("<I", int(s, 16)))


while True:
    try:
        conn, addr = server.accept()
        head, version, session, sequence_number, msgid, len_data = struct.unpack(
            "BB2xII2xHI", conn.recv(20)
        )
        sleep(0.1)  # Just for recive whole packet
        data = conn.recv(len_data)
        conn.close()
        reply = json.loads(data, encoding="utf8")
        print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]>>>"))
        print(head, version, session, sequence_number, msgid, len_data)
        print(json.dumps(reply, indent=4, sort_keys=True))
        print("<<<")

        client.publish("cameras",json.dumps(reply))  

    except (KeyboardInterrupt, SystemExit):
        break

server.close()
sys.exit(1)
