import network
import socket
from time import sleep
import machine
from pms5003 import PMS5003
import urequests

ssid = '<your_ssid>'
password = '<your_password>'

pms5003 = PMS5003(
    uart=machine.UART(0, tx=machine.Pin(0), rx=machine.Pin(1), baudrate=9600),
    pin_enable=machine.Pin(3),
    pin_reset=machine.Pin(2),
    mode="active"
)

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())

def send():
    data = pms5003.read()
    pm2 = data.pm_ug_per_m3(2.5)
    pm1 = data.pm_ug_per_m3(10)
    
    endpoint = 'https://api.sensor.community/v1/push-sensor-data/'
    headers = {
        'X-Pin': '1',
        'X-Sensor': '<your_sensor_name>'
    }
    body = {
      "software_version": "custom", 
      "sensordatavalues": [
            {"value_type":"P1","value": pm1 },
            {"value_type":"P2","value": pm2 }
        ]
    }  
    r = urequests.post(
        endpoint,
        json=body,
        headers=headers
    )
    print(data)
    print(r.content)
        
    sleep(145)

if __name__  == "__main__":
    connect()
    while True:
        send()
