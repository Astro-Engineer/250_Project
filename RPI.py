import paho.mqtt.client as mqtt

import time

import json

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
    values = []
    if(message.lower() == "light"):
      
        t_end = time.time() + 2
        while time.time() < t_end:
            values.append(mcp.read_adc(0))
            time.sleep(0.05)
        message = json.dumps(values)
            
        client.publish("iclee/pong", message)
        print("pubbed1    " + str(len(values)))
              
    elif(message.lower() == "sound"):
        value = mcp.read_adc(1)
        message = value
        client.publish("iclee/pong", f"{message}")
        print("pubbed2")
    else:
        GPIO.output(11, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(11, GPIO.LOW)
        time.sleep(0.2)
    

    


if __name__ == '__main__':

    client = mqtt.Client()

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(host="192.168.27.5", port=1883, keepalive=60)
    
    time.sleep(1)
    
    client.loop_forever()
