import paho.mqtt.client as mqtt

import time

from datetime import datetime

import socket

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def on_connect(client, userdata, flags, rc):
    
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("iclee/ping")

    client.message_callback_add("iclee/ping", on_message_from_pong)

def on_message(client, userdata, msg):

    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_pong(client, userdata, message):
    value = mcp.read_adc(0)
    message = value
    
    print("Custom callback  - Int Message: "+str(message))
    
    client.publish("iclee/pong", f"{message}")

    print("Publishing number"+ str(message))


if __name__ == '__main__':

    client = mqtt.Client()

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(host="192.168.27.5", port=1883, keepalive=60)
    
    time.sleep(1)
    
    client.loop_forever()
