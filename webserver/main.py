from machine import Pin, UART
import time
import ujson
import sys

button_left = Pin(16, Pin.IN, Pin.PULL_DOWN)
button_right = Pin(15, Pin.IN, Pin.PULL_DOWN)
led = Pin("LED", Pin.OUT)
tx_pin = Pin(12)
rx_pin = Pin(13)

sys.stdout.write("booted\n")

button_left_pressed = False
button_right_pressed = False


def send_data(data):
    json_data = ujson.dumps(data)
    sys.stdout.write(json_data + "\n")

while True:
    if button_left.value() and not button_left_pressed:
        data = {"Session_status": "Start"}
        send_data(data)
        led.value(True)
        button_left_pressed = True
    elif not button_left.value():
        button_left_pressed = False

    if button_right.value() and not button_right_pressed:
        data = {"Session_status": "Stop"}
        send_data(data)
        led.value(False)
        button_right_pressed = True
    elif not button_right.value():
        button_right_pressed = False

    # Add a small delay to avoid unnecessary CPU usage
    time.sleep(0.1)