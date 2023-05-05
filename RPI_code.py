import paho.mqtt.client as mqtt

import time

from datetime import datetime

import socket

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)

def on_connect(client, userdata, flags, rc):
    
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("iclee/ping")

    client.message_callback_add("iclee/ping", on_message_from_pong)

def on_message(client, userdata, msg):

    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_pong(client, userdata, message):
    
    message = message.payload.decode()
    print("Message: "+message)
    
    if(message.lower() == "light"):
        value = mcp.read_adc(0)
        message = value
        client.publish("iclee/pong", f"{message}")
        print("pubbed1")
    elif(message.lower() == "sound"):
        value = mcp.read_adc(1)
        message = value
        client.publish("iclee/pong", f"{message}")
        print("pubbed2")
    else:
        message = 1000
        client.publish("iclee/pong", f"{message}")
        print("pubbed3")
    

    


if __name__ == '__main__':

    client = mqtt.Client()

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(host="192.168.27.5", port=1883, keepalive=60)
    
    time.sleep(1)
    
    client.loop_forever()
