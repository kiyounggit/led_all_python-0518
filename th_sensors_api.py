from urllib.request import urlopen
import json
import time
import RPi.GPIO as GPIO
import dht11
import threading

url_dht = 'http://192.168.0.194:3000/api/sensors/dht1'
url_led = "http://192.168.0.194:3000/api/sensors/led1"

eve = threading.Event()   # Event 객체 생성

class DhtThread(threading.Thread):
    def run(self):
        eve.set()
        print('Ready Thread:', self.getName())

        # read data using header pin 14
        instance = dht11.DHT11(pin = 15)

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



class LedThread(threading.Thread):
    def run(self):
        print(self.getName(), 'waiting..')
        eve.wait()

        print('Ready Thread:', self.getName())

        while True:
            fp = urlopen(url_led)  # u is a file like object
            data = fp.read() # bytearray
            mystr = data.decode("utf8")
            fp.close()
            #print(mystr)

            js = json.loads(mystr)
            print(js['switch'] )

            time.sleep(5)


if __name__ == "__main__":

    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.cleanup()

    threads = []

    dhtThread = DhtThread()
    ledThread = LedThread()
    dhtThread.start()
    ledThread.start()

    threads.append(dhtThread)
    threads.append(ledThread)

    for th in threads:
        th.join()

    print("Quiting...")