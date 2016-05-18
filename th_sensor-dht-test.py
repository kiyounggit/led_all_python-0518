import json, time
import RPi.GPIO as GPIO
import dht11
import threading
import urllib.request as req
from urllib.request import urlopen
from urllib.parse import urlencode


url_dht = 'http://localhost:3000/api/sensors/dht11/12345'

eve = threading.Event()   # Event 객체 생성

class DhtThread(threading.Thread):
  def run(self):
    eve.set()
    print('Ready Thread:', self.getName())

    instance = dht11.DHT11(pin = 10)

    while True:
      result = instance.read()

      if result.is_valid():
          temp = result.temperature
          humi = result.humidity
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

          # DHT POST
          data = urlopen(url_dht, params.encode('utf8')).read()

          print("Temperature: %d C" % temp)
          print("Humidity: %d %%" % humi)
      else:
          print("Error: %d" % result.error_code)

      time.sleep(3)


if __name__ == "__main__":

    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup()

    threads = []

    dhtThread = DhtThread()
    dhtThread.start()

    threads.append(dhtThread)

    for th in threads:
        th.join()

    print("Quiting...")