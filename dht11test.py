import RPi.GPIO as GPIO
import dht11
import time

import urllib.request as req
from urllib.request import urlopen
from urllib.parse import urlencode

url = "http://192.168.0.194:3000/api/sensors"

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin = 15)

while True:
	result = instance.read()

	if result.is_valid():
		temp = result.temperature
		humi = result.humidity
		
	    print("Temperature: %d C" % temp)
	    print("Humidity: %d %%" % humi)
	else:
	    print("Error: %d" % result.error_code)

	name = "DHT11 sensor"
	stype = "DHT11"
	switch = "on"

	params = urlencode({
		'title': name,
		'type': stype,
		'switch': switch,
		'temp' : temp,
		'humi' : humi
	})

	data = urlopen(url, params.encode('utf8')).read()

	time.sleep(3)


