import time

import serial
import numpy as np

num_leds = 5

arduino = serial.Serial("/dev/ttyUSB0", 115200)

def concat_led_colors(led_colors):
    return np.append([], led_colors)

print("sleep")
time.sleep(4)
print("send")

def send_colors(colors):
    concat_colors = concat_led_colors(colors)
    byte_colors = concat_colors.astype(np.uint8)
    print(byte_colors)
    arduino.write(byte_colors)
    arduino.flush()

def turn_off_leds():
    turned_off = [0,0,0]
    colors = []
    for i in range(0, num_leds):
        colors.append(turned_off)
    send_colors(colors)

for j in range(0,256):
    i = 255 - j
    print(i)
    colors = [[1, 1, 1],[0,0,i],[i,i,i],[i,i,i], [20,20,20]]
    send_colors(colors)
    time.sleep(0.01)
turn_off_leds()

