import time

import cv2
import serial
import numpy as np

class FaultyFrameException(Exception):
    pass


def concat_led_colors(led_colors):
    return np.append([], led_colors)


def send_colors(arduino, colors):
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


def connect_Arduino():
    arduino = serial.Serial("/dev/ttyUSB0", 115200)
    print("sleep")
    time.sleep(4)
    print("Should be connected!")
    return arduino


num_leds = 5
arduino = connect_Arduino()

cap = cv2.VideoCapture(0)
frame_heigth = int(cap.get(4))
frame_width = int(cap.get(3))

print("Frame height: {} width:{}".format(frame_width, frame_heigth))


def show_one_color_in_frame(color):
    r, g, b = color
    bgr_color = np.array([b, g, r], dtype=np.uint8)
    bgr_color_frame = np.tile(bgr_color, (240, 320, 1))
    # print(np.repeat(color, 20))
    cv2.imshow('result color', bgr_color_frame)


while (True):
    # frame is a simple RGB frame[height][width][R][G][B]
    ret, frame = cap.read()
    if not ret:
        raise FaultyFrameException("The frame was not properly loaded")

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    color = frame[10][10]
    show_one_color_in_frame(color)

    colors = [color, color, color, color, color]
    send_colors(arduino, colors)


# When everything done, release the capture
cap.release()
arduino.close()

