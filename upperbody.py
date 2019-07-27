import cv2
import pigpio
import time

#Setting up the PIO 
pi = pigpio.pi()
pi.set_mode(4, pigpio.OUTPUT)
pi.set_servo_pulsewidth(4, 1500)


# Create a CascadeClassifier Object
cascade = cv2.CascadeClassifier("haarcascade_upperbody.xml")

# Setting up the camera frame
width = 160
height = 120
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
	
if cap.isOpened():
	ret, frame = cap.read()
else:
	ret = False

current_angle = 90
center_thresh = 8
rate = 2

while ret:
	# Reading the image as gray scale image
	gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	 
	# Search the co-ordinates of the image
	upperbody = cascade.detectMultiScale(gray_img, scaleFactor = 1.05, minNeighbors=5)

	# Sorting the faces on basis of area
	upperbody = sorted(upperbody, key=lambda x:x[3]*x[2])
	
	if len(upperbody)>0:
		x,y,w,h = upperbody[-1]
		x_medium = int((x+x+w)//2)

		# Drawing the line on center of face
		cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)

		# Moving the servo
		if abs(x_medium - width//2)>center_thresh:
			if x_medium > width//2:
				current_angle += rate
			if x_medium < width//2:
				current_angle -=rate
			dc = (1+current_angle/180)
			pi.set_servo_pulsewidth(4, dc*1000)
			
	 
	cv2.imshow("Camera", frame)

	if cv2.waitKey(1) == 27: # exit on ESC
		break
	ret, frame = cap.read()
	
	# Flipping the frame
	frame = cv2.flip(frame, 0)



cv2.destroyAllWindows()
cap.release()