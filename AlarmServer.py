#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, struct, json
import paho.mqtt.client as mqtt
import yaml
import logging
from time import sleep
from socket import *
from datetime import *

port = "15002"
server = socket(AF_INET, SOCK_STREAM)
server.bind(("0.0.0.0", int(port)))
# server.settimeout(0.5)
server.listen(1)
logging.basicConfig(level=logging.INFO)

def on_connect(client, userdata, flags, rc):
    logging.debug("Connected with result code "+str(rc))

def on_publish(client,userdata,result):
    logging.info("Data published")
    pass
    
with open('config.yaml', 'r') as file:
    settings = yaml.load(file, Loader=yaml.FullLoader)

mqtt_address = settings['MQTT_ADDRESS']
mqtt_port = settings['MQTT_PORT']
mqtt_username = settings['MQTT_USERNAME']
mqtt_password = settings['MQTT_PASSWORD']

client = mqtt.Client("cameras_alarmserver") 
client.on_connect = on_connect
client.on_publish = on_publish
client.username_pw_set(username=mqtt_username,password=mqtt_password)
logging.info("Connecting...")
client.connect(mqtt_address, mqtt_port)
client.loop_start()

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
        
        jdata = json.loads(data.decode('utf-8'))

        device_name = jdata['SerialID']
        mqtt_topic = 'cameras/' + device_name

        client.publish(mqtt_topic,json.dumps(jdata))  

    except (KeyboardInterrupt, SystemExit):
        break

client.loop_stop()
server.close()
sys.exit(1)
