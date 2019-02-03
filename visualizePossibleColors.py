import cv2
import numpy as np

import calibrateColor
import settings


def update_result_color_frame_name(ignore):
    print("update")
    r_factor = cv2.getTrackbarPos(r_name, result_color_frame_name) / 100.0
    g_factor = cv2.getTrackbarPos(g_name, result_color_frame_name) / 100.0
    b_factor = cv2.getTrackbarPos(b_name, result_color_frame_name) / 100.0
    result_color_rgb = [int(a * b) for a, b in zip(selected_color, [r_factor, g_factor, b_factor])]

    calibrateColor.show_one_color_in_frame(result_color_frame_name, result_color_rgb)


def select_color_callback(event, x, y, flags, param):
    global buttonDown
    if event == cv2.EVENT_LBUTTONDOWN:
        print("down")
        buttonDown = True
    if event == cv2.EVENT_LBUTTONUP:
        print("up")
        buttonDown = False
    if event == cv2.EVENT_MOUSEMOVE:
        if buttonDown:
            b, g, r = image[y][x]
            global selected_color
            selected_color = [r, g, b]
            calibrateColor.show_one_color_in_frame(selected_color_frame_name, selected_color)
            update_result_color_frame_name(None)


buttonDown = False

color_block_width = 10
color_block_height = 40

hue_num_buckets = settings.HUE_NUM_BUCKETS
saturation_num_buckets = settings.SATURATION_NUM_BUCKETS
value_num_buckets = settings.VALUE_NUM_BUCKETS

hue_bucket_size = int(180 / hue_num_buckets)
saturation_bucket_size = int(256 / saturation_num_buckets)
value_bucket_size = int(256 / value_num_buckets)

frame_name = "All colors"
cv2.namedWindow(frame_name)
image = np.empty((saturation_num_buckets*color_block_height, hue_num_buckets*value_num_buckets*color_block_width, 3), dtype=np.uint8)

v_index = 40

selected_color_frame_name = "Selected color"
cv2.namedWindow(selected_color_frame_name)
selected_color = [0,0,50]
calibrateColor.show_one_color_in_frame(selected_color_frame_name, selected_color)
cv2.setMouseCallback(frame_name, select_color_callback)

result_color_frame_name = "Result color"
cv2.namedWindow(result_color_frame_name)
selected_color = [0,0,50]
calibrateColor.show_one_color_in_frame(selected_color_frame_name, selected_color)

r_name = "R scale percent"
g_name = "G scale percent"
b_name = "B scale percent"

cv2.createTrackbar(r_name, result_color_frame_name, 100, 100, update_result_color_frame_name)
cv2.createTrackbar(g_name, result_color_frame_name, 100, 100, update_result_color_frame_name)
cv2.createTrackbar(b_name, result_color_frame_name, 100, 100, update_result_color_frame_name)

for h_index in range(hue_num_buckets):
    for s_index in range(saturation_num_buckets):
        for v_index in range(value_num_buckets):
            r, g, b = calibrateColor.hsv_index_to_rgb(h_index, s_index, v_index, hue_bucket_size, saturation_bucket_size, value_bucket_size)

            for i in range(color_block_height):
                for j in range(color_block_width):
                    x = (v_index * hue_num_buckets + h_index) * color_block_width + j
                    y = s_index * color_block_height + i
                    image[y][x] = [b, g, r]

cv2.imshow(frame_name, image)

# Connect with arduino
#arduino = calibrateColor.connect_Arduino()

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Send colors to arduino
    # colors = [result_color_rgb, result_color_rgb, result_color_rgb, result_color_rgb, result_color_rgb]
    # send_colors(arduino, colors)

cv2.destroyAllWindows()