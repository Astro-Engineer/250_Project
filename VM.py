#import necessary libraries
import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime
import math
import socket
#code to run on connect
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("iclee/light")
    client.message_callback_add("iclee/light", on_message_from_light)
    client.subscribe("iclee/sound")
    client.message_callback_add("iclee/sound", on_message_from_sound)
    client.subscribe("iclee/wrong")
    client.message_callback_add("iclee/wrong", on_message_from_wrong)
    
#code to run on message
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

#code to run on special message from light sensor
def on_message_from_light(client, userdata, message):
    data = json.loads(message.payload)
    xaxis = np.linspace(0, 4, len(data))
    #apply 20th degree polynomial regression
    #this is high to ensure we account for most if not all fluctuations in the data
    mymodel = np.poly1d(np.polyfit(xaxis, data, 20))
    plt.figure()
    #plot regression line
    plt.plot(xaxis, mymodel(xaxis), color='red')

    #plot scatter data
    plt.scatter(xaxis, data)
    #label graph
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Sample Light Strength")
    plt.savefig("light_graph")
    print("LIGHT COMPLETE")
    
#same as before but for sound data
def on_message_from_sound(client, userdata, message):
    data = json.loads(message.payload)
    xaxis = np.linspace(0, 4, len(data))
    mymodel = np.poly1d(np.polyfit(xaxis, data, 20))
    plt.figure()
    plt.plot(xaxis, mymodel(xaxis), color='red')

    plt.scatter(xaxis, data)

    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Sample Sound Strength")
    plt.savefig("sound_graph")
    print("SOUND COMPLETE")
        
#prints message if received topic is "wrong"
def on_message_from_wrong(client, userdata, message):
    print("Please enter either 'Light' or 'Sound'!")

if __name__ == '__main__':
    #client setup
    client = mqtt.Client()

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(host="192.168.27.5", port=1883, keepalive=60)

    client.loop_start()
    #sleep to wait before printing first statement
    time.sleep(1.5)
    
    while True:
        message = input("Enter what you would like measured? ")
        #publish the user input to the topic "input"
        client.publish("iclee/input", message)
        #allow data collection and graphs to be made before asking again
        time.sleep(5)
