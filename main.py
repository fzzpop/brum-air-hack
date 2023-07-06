"""Script to connect Pi to WiFi and intermittently send data to sensor.community API.
"""
from time import sleep
import network
import socket
import machine
from pms5003 import PMS5003
import urequests

WIFI_SSID = "<your_ssid>"
WIFI_PASSWORD = "<your_password>"
SENSOR_NAME = "<your_sensor_name>"

pms5003 = PMS5003(
    uart=machine.UART(0, tx=machine.Pin(0), rx=machine.Pin(1), baudrate=9600),
    pin_enable=machine.Pin(3),
    pin_reset=machine.Pin(2),
    mode="active",
)


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    print(wlan.ifconfig())


def send_sensor_data():
    data = pms5003.read()
    pm2 = data.pm_ug_per_m3(2.5)
    pm1 = data.pm_ug_per_m3(10)

    endpoint = "https://api.sensor.community/v1/push-sensor-data/"
    headers = {"X-Pin": "1", "X-Sensor": SENSOR_NAME}
    body = {
        "software_version": "custom",
        "sensordatavalues": [
            {"value_type": "P1", "value": pm1},
            {"value_type": "P2", "value": pm2},
        ],
    }
    response = urequests.post(endpoint, json=body, headers=headers)
    print(data)
    print(response.content)


if __name__ == "__main__":
    connect_to_wifi()
    while True:
        send_sensor_data()
        sleep(145)
