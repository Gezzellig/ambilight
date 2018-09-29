import time

import serial
import numpy as np

arduino = serial.Serial("/dev/ttyUSB0", 115200)

def byterize_led_colors(led_colors):
    return np.append([], led_colors)
print("sleep")
time.sleep(4)
for i in range(0,500):
    print(i)
    colors = [[170,0,255],[0,0,i],[i,0,0],[i,i,i]]
    nparray = byterize_led_colors(colors)
    bytearray = nparray.astype(np.uint8)
    arduino.write(bytearray)
    arduino.flush()
    time.sleep(0.01)

