import paho.mqtt.client as mqtt

import time

import matplotlib.pyplot as plt
import numpy as np
import json

from datetime import datetime

import socket

def on_connect(client, userdata, flags, rc):
    
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("iclee/data")

    client.message_callback_add("iclee/data", on_message_from_data)
    
    client.subscribe("iclee/wrong")
    
    client.message_callback_add("iclee/wrong", on_message_from_wrong)

def on_message(client, userdata, msg):

    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_data(client, userdata, message):

    data = json.loads(message.payload)
    for element in data:
        print(element)
    xaxis = np.linspace(0, 4, 80)

    plt.plot(xaxis, data)
    plt.xlabel("X-Label")
    plt.ylabel("Y-Label")
    plt.title("Title")
    plt.savefig("Sample Two")
    print("TWO COMPLETE")
        
def on_message_from_wrong(client, userdata, message):
    print("Please enter either 'Light', 'Sound', or 'Distance'!")

if __name__ == '__main__':

    client = mqtt.Client()

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(host="192.168.27.5", port=1883, keepalive=60)

    

    client.loop_start()

    time.sleep(1.5)
    while True:
        message = input("Enter what you would like measured? ")
        

        client.publish("iclee/input", message)

        print("Publishing string: " + message)
        time.sleep(5)
