import paho.mqtt.client as mqtt

import time

from datetime import datetime

import socket

def on_connect(client, userdata, flags, rc):
    
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("iclee/pong")

    client.message_callback_add("iclee/pong", on_message_from_pong)

def on_message(client, userdata, msg):

    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_pong(client, userdata, message):

    message = int(message.payload.decode()) + 1

    print("Custom callback  - Int Message: "+str(message))

    client.publish("iclee/ping", f"{message}")

    print("Publishing number " + str(message))

    time.sleep(4)    

if __name__ == '__main__':
    message = str(1)

    client = mqtt.Client()

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(host="192.168.139.5", port=1883, keepalive=60)

    

    client.loop_start()

    time.sleep(1)

    client.publish("iclee/ping", f"{message}")

    print("Publishing number")

    time.sleep(4)
    
    while True:
    	pass
