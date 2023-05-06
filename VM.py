import paho.mqtt.client as mqtt

import time

import matplotlib.pyplot as plt

import numpy as np

import json

from datetime import datetime

import math

import socket

def on_connect(client, userdata, flags, rc):
    
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("iclee/light")

    client.message_callback_add("iclee/light", on_message_from_light)
    
    client.subscribe("iclee/sound")

    client.message_callback_add("iclee/sound", on_message_from_sound)
    
    client.subscribe("iclee/wrong")
    
    client.message_callback_add("iclee/wrong", on_message_from_wrong)

def on_message(client, userdata, msg):

    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_light(client, userdata, message):

    data = json.loads(message.payload)

    xaxis = np.linspace(0, 4, len(data))
    
    mymodel = np.poly1d(np.polyfit(xaxis, data, 20))

    plt.plot(xaxis, mymodel(xaxis), color='red')

        
    

# plot the data and regression line
    plt.scatter(xaxis, data)

    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Sample Light Strength")
    plt.savefig("light_graph")
    print("LIGHT COMPLETE")
    
def on_message_from_sound(client, userdata, message):

    data = json.loads(message.payload)

    xaxis = np.linspace(0, 4, len(data))
    
    mymodel = np.poly1d(np.polyfit(xaxis, data, 20))

    plt.plot(xaxis, mymodel(xaxis), color='red')


# plot the data and regression line
    plt.scatter(xaxis, data)

    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Sample Sound Strength")
    plt.savefig("sound_graph")
    print("SOUND COMPLETE")
        
def on_message_from_wrong(client, userdata, message):
    print("Please enter either 'Light' or 'Sound'!")

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

        time.sleep(5)
