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
    for element in data:
        print(element)
    xaxis = np.linspace(0, 4, 80)

    plt.scatter(xaxis, data)

    plt.xlabel("X-Label")
    plt.ylabel("Y-Label")
    plt.title("Title")
    plt.savefig("Sample Two")
    print("TWO COMPLETE")
    
def on_message_from_sound(client, userdata, message):

    data = json.loads(message.payload)
    for element in data:
        print(element)


    xaxis = np.linspace(0, 4, len(data))
    
    degree = 2
    coefficients = [0] * (degree+1)
    n = len(xaxis)
    for i in range(degree+1):
        for j in range(n):
            coefficients[i] += data[j] * math.pow(x[j], i)
    for i in range(degree-1, -1, -1):
        for j in range(degree, i, -1):
            coefficients[i] -= coefficients[j] * math.pow(x[0], j-i)
        coefficients[i] /= math.pow(x[0], i)
        
# plot the data and regression line

    plt.plot(xaxis, [sum([coefficients[i] * math.pow(j, i) for i in range(degree+1)]) for j in xaxis])
    

# plot the data and regression line
    plt.scatter(xaxis, data)
    plt.plot(xaxis, p(xaxis))
    plt.xlabel("X-Label")
    plt.ylabel("Y-Label")
    plt.title("Title")
    plt.show()
    plt.savefig("Sample Two")
    print("TWO COMPLETE")
        
def on_message_from_wrong(client, userdata, message):
    print("Please enter either 'Light', 'Sound'!")

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
