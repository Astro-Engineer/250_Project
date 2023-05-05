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

    message = int(message.payload.decode())

    print("Data Received: "+str(message))

if __name__ == '__main__':

    client = mqtt.Client()

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(host="192.168.27.5", port=1883, keepalive=60)

    

    client.loop_start()
    
    message = input("Enter what you would like measured? ")
    

    client.publish("iclee/ping", message)

    print("Publishing string: " + message)

    
    while True:
    	pass
