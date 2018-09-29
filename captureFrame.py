import cv2
import serial
import numpy as np

class FaultyFrameException(Exception):
    pass

arduino = serial.Serial("/dev/ttyUSB0", 115200)

def selectColor(height, width, frame):
    return frame[height][width]


def calcLedlocations(frame_height, frame_width, numleds_l, numleds_t, numleds_r):
    led_locations = list()

    #left border
    for i in range(0, numleds_l):
        led_locations.append((int((i+0.5)*(float(frame_height)/numleds_l)), 0))

    #top border
    for i in range(0, numleds_t):
        led_locations.append((0, int((i+0.5)*(float(frame_height)/numleds_t))))

    #right border
    for i in range(0, numleds_l):
        led_locations.append((int((i+0.5)*(float(frame_height)/numleds_l)), frame_width-1))

    return led_locations

def byterize_led_colors(led_colors):
    byte_led_colors = list()
    for colors in led_colors:
        for color in colors:
            byte_led_colors.append(chr(color))
    return byte_led_colors


cap = cv2.VideoCapture(0)
frame_heigth = int(cap.get(4))
frame_width = int(cap.get(3))

led_locations = calcLedlocations(frame_heigth, frame_width, 20, 34, 20)
print(led_locations)

print("Frame height: {} width:{}".format(frame_width, frame_heigth))

ret, frame = cap.read()

colors = [[255,0,0],[0,0,255],[255,0,0],[0,0,255]]
print(colors)
print(byterize_led_colors(colors))
print(240)
print(frame[2][2])
print(type(frame[2][2]))
arduino.write(byterize_led_colors(colors))

def main_loop():
	while(True):
		# frame is a simple RGB frame[height][width][R][G][B]
		ret, frame = cap.read()
		if not ret:
			raise FaultyFrameException("The frame was not properly loaded")

		led_colors = list()
		print("hier",len(led_locations))
		for h, w in led_locations:
			led_colors.append(selectColor(h, w, frame))

		#led colors must be pushed to the arduino somehow
		#print(led_colors)
		#print(type(led_colors)))
		print("scherm")
		print(len(led_colors))

		arduino.write(byterize_led_colors(led_colors))
		

		# Display the resulting frame
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	# When everything done, release the capture
	cap.release()



#cv2.destroyAllWindows()
