from machine import Pin, ADC
from time import sleep
import dht
import sys
from umqtt.simple import MQTTClient
import ujson
import machine
from time import sleep
import network
#from wifinetwork.wifi import WifiConnect
import gc
import ubinascii
import esp

moist = ADC(0)
moistd = Pin(4, Pin.IN)
led = Pin(2, Pin.OUT)
sensor = dht.DHT11(Pin(5))
SERVER = '192.168.80.1'
CLIENT_ID = "ESP8622_DHT11_Sensor01"
UUID = esp.flash_id()
TOPIC = b'temp_humidity'
idesp = ubinascii.hexlify(machine.unique_id()).decode('utf-8')

class WifiConnect:
    def __init__():
        connected = False
        
    def connect():
        sleep(3)
        
        #import network
        ssid      = "PlantHealth"
        password  =  "Sm0keyThisIsn0tVietnamThisIsB0wlingThereAreRules."
     
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect('PlantHealth', 'Sm0keyThisIsn0tVietnamThisIsB0wlingThereAreRules.')
            while not sta_if.isconnected():
                pass
        if sta_if.isconnected():
            print("connection successfull")
            return sta_if  

    def disconnect():
        #import network
        sta_if = network.WLAN(network.STA_IF)
        sta_if.disconnect()
        sta_if.active(False)
        #return self.connected




def deep_sleep(msecs):
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after X milliseconds (waking the device)
    rtc.alarm(rtc.ALARM0, msecs)

    # put the device to sleep
    #machine.deepsleep()
    esp.deepsleep(msecs)
  
# Will return a integer
def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


print(esp.flash_id())


while True:
    print('Im awake !')
    #Connect to wifi
    wlan = WifiConnect.connect()
    sleep(10)
    if wlan is None:
        print("Could not initialize the network connection.")    
    else:
        sleep(10)
        try:
            #MQTT client def
            client = MQTTClient(CLIENT_ID, SERVER)
            client.connect()
            if gc.mem_free() < 102000:
                gc.collect()
            #blink LED
            led.value(1)
            sleep(2)
            led.value(0)
            sleep(2)

            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            moist_value = moist.read()
            payload = {}
            payload["room-temperature"]=temp
            #payload["room_temperature_unit"] = "Celsius"
            #degreesdict['clientID'] = CLIENT_ID
            payload["room_pourcent_humidity_air"]=hum
            #payload["room_humidity_air_unit"] = "%"

            #if moistd.value() == 1:
            # moisture = "LOW"
            #else :
            #moisture = "HIGH"
             
            moisturepourcent =  convert(moist_value, 0, 1023, 100, 0)
            payload["moisture_pourcent"]=moisturepourcent
            payload["status_moisture"] = moistd.value()
            payload["UUID"] = UUID
            #print(idesp)
            #payload['id'] = idesp
            #client.ping()
            to_publish = ujson.dumps(payload)
            client.publish('stats/', to_publish)
            print(payload)
            sleep(3)
            print('Im going to sleep')
            #         #sleep for 10 seconds (10000 milliseconds) => 1000 = 1 sec => 1800 000
            #client.disconnect()
            #WifiConnect.disconnect()
            #sleep(10)
            deep_sleep(6000000)
        except OSError as e:
            print('Failed to read sensor')
            print(e)
