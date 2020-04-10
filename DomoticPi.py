#!/usr/bin/env python3

DEVICE_NAME="LuzSalon"

import paho.mqtt.client as mqtt
import threading
import time
# This is the Publisher

status = False

client = mqtt.Client("RaspberryPI")
client.connect("localhost",1883,60)

def sendStatus():
	while True:
		print('Sending: ' + DEVICE_NAME + ' Status = ' + str(status))
		client.publish(DEVICE,status)
		time.sleep(1)


print ('Mqtt Client')

t = threading.Thread(target=sendStatus, name='sendStatus')

t.start()

client.loop_forever()

client.disconnect();
