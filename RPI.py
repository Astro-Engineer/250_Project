#adding necessary libraries
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import socket
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO

#setup for the mcp chip
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#setup for the LED
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)

#action to take when connecting to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("iclee/input")
    client.message_callback_add("iclee/input", on_message_from_input)

#action to take when a message is received
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

    #special action to take when message is from the "input" topic
def on_message_from_input(client, userdata, message):
    #read the string
    message = message.payload.decode()
    values = []
    #check what the string is and act accordingly
    if(message.lower() == "light"):
        #timer for 4 seconds
        t_end = time.time() + 4
        while time.time() < t_end:
            values.append(mcp.read_adc(0))
            #read value then add a small delay
            time.sleep(0.01)
        #store array as json
        message = json.dumps(values)
        #publish
        client.publish("iclee/light", message)
    #same as above for "sound" topic
    elif(message.lower() == "sound"):
        t_end = time.time() + 4
        while time.time() < t_end:
            values.append(mcp.read_adc(1))
            time.sleep(0.01)
        message = json.dumps(values)
            
        client.publish("iclee/sound", message)
    #if something else
    else:
        #set LED high for 3 seconds
        GPIO.output(11, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(11, GPIO.LOW)
        time.sleep(0.5)
        #dummy message
        message = ""
        #send to topic "wrong"
        client.publish("iclee/wrong", message)
    
if __name__ == '__main__':
    #setup client
    client = mqtt.Client()

    client.on_connect = on_connect

    client.on_message = on_message

    client.connect(host="192.168.27.5", port=1883, keepalive=60)
    
    time.sleep(1)
    #make sure it keeps running
    client.loop_forever()
