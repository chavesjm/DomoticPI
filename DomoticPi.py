#!/usr/bin/env python3

SERVERMQTT="192.168.0.103"
DEVICE_NAME="LuzSalonID"
RELAIS_1_GPIO = 2

import paho.mqtt.client as mqtt
import threading
import time
import queue
import RPi.GPIO as GPIO

def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(DEVICE_NAME)

def on_message(client, userdata, msg):
    new_value = msg.payload.decode()
    current_state = GPIO.input(RELAIS_1_GPIO)

    print("on_Message: new_value = " +  new_value)
    if current_state == GPIO.LOW:
        print("on_Message: current_state = LOW")
    else:
        print("on_Message: current_state = HIGH")

    if new_value == '0' and current_state == 1:
        print("Changing to LOW")
        GPIO.output(RELAIS_1_GPIO,GPIO.LOW)
    elif new_value == '1' and current_state == 0:
        print("Changing to HIGH")
        GPIO.output(RELAIS_1_GPIO,GPIO.HIGH)

def sendStatus():
	
	while True:
            state = GPIO.input(RELAIS_1_GPIO)
            print('Sending: ' + DEVICE_NAME + ' Status = ' + str(state))
            client.publish(DEVICE_NAME,state)
            time.sleep(1)

print ('Mqtt Client')

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # on

client = mqtt.Client("RaspberryPI")
client.connect(SERVERMQTT,1883,60)

client.on_connect = on_connect
client.on_message = on_message

t = threading.Thread(name = "SendStatus", target=sendStatus)
t.start()

client.loop_forever()

