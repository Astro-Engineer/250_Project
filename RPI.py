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

    client.subscribe("iclee/input")

    client.message_callback_add("iclee/input", on_message_from_input)

def on_message(client, userdata, msg):

    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def on_message_from_input(client, userdata, message):
    
    message = message.payload.decode()
    print("Message: "+message)
    values = []
    if(message.lower() == "light"):
      
        t_end = time.time() + 4
        while time.time() < t_end:
            values.append(mcp.read_adc(0))
            time.sleep(0.01)
        message = json.dumps(values)
            
        client.publish("iclee/light", message)
              
    elif(message.lower() == "sound"):
        t_end = time.time() + 4
        while time.time() < t_end:
            values.append(mcp.read_adc(1))
            time.sleep(0.01)
        message = json.dumps(values)
            
        client.publish("iclee/sound", message)
        
    else:
        GPIO.output(11, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(11, GPIO.LOW)
        time.sleep(0.5)
        message = ""
        client.publish("iclee/wrong", message)
    

    


if __name__ == '__main__':

    client = mqtt.Client()

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(host="192.168.27.5", port=1883, keepalive=60)
    
    time.sleep(1)
    
    client.loop_forever()
