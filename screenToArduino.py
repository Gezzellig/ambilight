import time

import cv2
import serial
import numpy as np

class FaultyFrameException(Exception):
    pass

def select_average_color(frame, topleft, bottemright):
    tl_x, tl_y = topleft
    br_x, br_y = bottemright
    for y in range(tl_y, br_y):
        for x in range(tl_x, br_x):
            break



#arduino = serial.Serial("/dev/ttyUSB0", 115200)

cap = cv2.VideoCapture(0)
frame_heigth = int(cap.get(4))
frame_width = int(cap.get(3))

print("Frame height: {} width:{}".format(frame_width, frame_heigth))

print("initial sleep")
#time.sleep(4)
print("LETS GO!")


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

    r_color = np.floor_divide(color, [1,1,2])
    b8_color = r_color.astype(np.uint8)
    print(b8_color.dtype)
    print("{} then {}".format(color, b8_color))
    out_color = b8_color
    print(out_color)
    #arduino.write(out_color)
    #arduino.write(out_color)
    #arduino.write(out_color)
    #arduino.write(out_color)


# When everything done, release the capture
cap.release()

