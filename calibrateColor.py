import math
import time

import settings
import cv2
import serial
import numpy as np
import matplotlib.pyplot as plt

class FaultyFrameException(Exception):
    pass


def concat_led_colors(led_colors):
    return np.append([], led_colors)


def send_colors(arduino, colors):
    concat_colors = concat_led_colors(colors)
    byte_colors = concat_colors.astype(np.uint8)
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


def show_one_color_in_frame(frame_name, color):
    r, g, b = color
    bgr_color = np.array([b, g, r], dtype=np.uint8)
    bgr_color_frame = np.tile(bgr_color, (240, 320, 1))
    # print(np.repeat(color, 20))
    cv2.imshow(frame_name, bgr_color_frame)

"""
def checkIndex(value, min, max):
    return min <= value < max


Maybe to be added later
def spread_hist(hist):
    print("hist is {} bij {} bij {}".format(len(hist), len(hist[0]), len(hist[0][0])))
    spread_hist = hist.copy()
    for i in range(len(hist)):
        for j in range(len(hist[0])):
            for k in range(len(hist[0][0])):
                for x, y in [(1,1), (1,-1), (-1, 1), (-1,-1)]:
                    if checkIndex(x)
"""


def hsv_index_to_rgb(h_index, s_index, v_index, hue_bucket_size, saturation_bucket_size, value_bucket_size):
    h = h_index*hue_bucket_size + int(hue_bucket_size / 2)
    s = s_index*saturation_bucket_size + int(saturation_bucket_size / 2)
    v = v_index*value_bucket_size + int(value_bucket_size / 2)

    hsv = np.uint8([[[h, s, v]]])
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)[0][0]
    return rgb


#WARNING input is BGR output is RGB
def find_dominant_color(sub_frame_bgr):
    hue_num_buckets = settings.HUE_NUM_BUCKETS
    saturation_num_buckets = settings.SATURATION_NUM_BUCKETS
    value_num_buckets = settings.VALUE_NUM_BUCKETS

    hue_bucket_size = int(180/hue_num_buckets)
    saturation_bucket_size = int(256/saturation_num_buckets)
    value_bucket_size = int(256 / value_num_buckets)

    sub_frame_hsv = cv2.cvtColor(sub_frame_bgr, cv2.COLOR_BGR2HSV)
    hist_hsv = cv2.calcHist([sub_frame_hsv], [0, 1, 2], None, [hue_num_buckets, saturation_num_buckets, value_num_buckets], [0, 180, 0, 256, 0, 256])
    #spread_hist_hsv = spread_hist(hist_hsv)        MAYBE TO BE ADDED LATER
    index = hist_hsv.argmax()

    #print(hist_hsv.max())

    h_index = math.floor(index/(saturation_num_buckets*value_num_buckets))
    s_index = math.floor((index-(h_index*saturation_num_buckets*value_num_buckets))/value_num_buckets)
    v_index = index-(h_index*saturation_num_buckets*value_num_buckets)-(s_index*value_num_buckets)

    return hsv_index_to_rgb(h_index, s_index, v_index, hue_bucket_size, saturation_bucket_size, value_bucket_size)



def nothing(x):
    pass


def main():
    num_leds = 5
    # UNCOMMENT
    # arduino = connect_Arduino()

    cap = cv2.VideoCapture(0)  # 0 for webcam, 2 for usb video
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800) Try with capture card
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    frame_heigth = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    print("Frame height: {} width:{}".format(frame_width, frame_heigth))
    corrected_color_frame_name = "corrected_color"
    r_name = "R scale percent"
    g_name = "G scale percent"
    b_name = "B scale percent"
    cv2.namedWindow(corrected_color_frame_name)
    cv2.createTrackbar(r_name, corrected_color_frame_name, 100, 100, nothing)
    cv2.createTrackbar(g_name, corrected_color_frame_name, 100, 100, nothing)
    cv2.createTrackbar(b_name, corrected_color_frame_name, 100, 100, nothing)

    while (True):
        # frame is a simple RGB frame[height][width][R][G][B]
        ret, frame_bgr = cap.read()
        if not ret:
            raise FaultyFrameException("The frame was not properly loaded")

        cv2.imshow("frame", frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # BGR to RGB
        # frameRGB = cv2.cvtColor(frameBRR, cv2.COLOR_BGR2RGB)

        sub_frame_bgr = frame_bgr[int(frame_heigth / 2) - 10:int(frame_heigth / 2) + 10,
                        int(frame_width / 2) - 10:int(frame_width / 2) + 10]
        cv2.imshow('sub image', sub_frame_bgr)

        dominant_color_rgb = find_dominant_color(sub_frame_bgr)

        show_one_color_in_frame("dominant_color", dominant_color_rgb)

        r_factor = cv2.getTrackbarPos(r_name, corrected_color_frame_name) / 100.0
        g_factor = cv2.getTrackbarPos(g_name, corrected_color_frame_name) / 100.0
        b_factor = cv2.getTrackbarPos(b_name, corrected_color_frame_name) / 100.0
        corrected_color_rgb = [int(a * b) for a, b in zip(dominant_color_rgb, [r_factor, g_factor, b_factor])]

        show_one_color_in_frame(corrected_color_frame_name, corrected_color_rgb)
        # create trackbars for color change

        # colors = [color, color, color, color, color]
        # UNCOMMENT
        # send_colors(arduino, colors)

    # When everything done, release the capture
    cap.release()
    # arduino.close()


if __name__ == "__main__":
    main()
