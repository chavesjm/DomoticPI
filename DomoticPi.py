#!/usr/bin/env python3

DEVICE_NAME="LuzSalonID"

import paho.mqtt.client as mqtt
import threading
import time
import queue
import RPi.GPIO as gpio

# This is the Publisher

global status

def setStatus(new_status):
	print("New Status = " + str(new_status))
	status = new_status
	print("Status is now = " + str(status))
	

def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(DEVICE_NAME)

def on_message(client, userdata, msg):
	new_value = msg.payload.decode()
	setStatus(new_value)
	print('Receive Status = ' + str(new_value))

def sendStatus(q):
	
	while True:
		localStatus = q.get()
		print('Sending: ' + DEVICE_NAME + ' Status = ' + str(localStatus))
		client.publish(DEVICE_NAME,localStatus)
		time.sleep(1)
		q.task_done()
		print("Fin true")

print ('Mqtt Client')

status = 0

q = queue.Queue(maxsize = 1)
q.put(status)
 
client = mqtt.Client("RaspberryPI")
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

t = threading.Thread(name = "SendStatus", target=sendStatus, args=(q, ))
t.start()
q.join()

client.loop_forever()

