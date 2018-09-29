import time

import cv2
import serial
import numpy as np

arduino = serial.Serial("/dev/ttyUSB0", 115200)

def byterize_led_colors(led_colors):
	return np.append([], led_colors)


colors = [[5,0,0],[0,0,5],[5,0,0],[0,0,5],[20,20,20]]
colors2 = [[5,5,0],[0,5,0],[0,5,0],[0,5,5],[40,20,20]]

print(colors)
nparray = byterize_led_colors(colors)
print(nparray)
print(nparray.dtype)
bytearray = nparray.astype(np.uint8)
print(bytearray)
print(bytearray.itemsize)

nparray2 = byterize_led_colors(colors2)
bytearray2 = nparray2.astype(np.uint8)

while True:
	print("sleep")
	time.sleep(4)
	print("send")
	arduino.write(bytearray)
	arduino.flush()
	print("sleep2")
	time.sleep(4)
	print("send2")
	arduino.write(bytearray2)
	arduino.flush()
