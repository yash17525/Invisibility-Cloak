import cv2
import numpy as np
import time

print("""

Harry :  Hey !! Would you like to try my invisibility cloak ??

         Its awesome !!

        
         Prepare to get invisible .....................
    """)

"""
We will replace the current frame pixels corresponding to the cloth with the background
pixels to generate the effect of an invisibility cloak. For this we need to store the frame of a
static background.
"""
cap = cv2.VideoCapture(0)
time.sleep(3)
background=0


for i in range(30):
	ret,background = cap.read()    
background = np.flip(background,axis=1)

"""
cap.read() method enables us to capture latest frame(stored in variable background) with
the camera and it also returns a Boolean (True/False stored in ret). If frame is read
correctly, it will be True. So you can check end of the video by checking this return value.
"""

"""
The image captured is a bit dark compared to when multiple frames are captured. Hence capturing
multiple images of static background with a for loop results in better image.
"""

while(cap.isOpened()):

	"""
	So the idea is that we will use a red colour cloth as out invisibility cloak. We will first
	determine the region covered by the cloth (determine pixels corresponding to red colour).
	To detect red colour we use the HSV colour space.
	"""
	ret, img = cap.read()
	
	# Flipping the image 
	img = np.flip(img,axis=1)
	
	# Converting image to HSV color space.
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	value = (35, 35)
	
	blurred = cv2.GaussianBlur(hsv, value,0)
	
	# Defining lower range for red color detection.
	lower_red = np.array([0,120,70]) # hue(color component) , saturation(amount of gray color), value (brightness)
	upper_red = np.array([10,255,255])
	mask1 = cv2.inRange(hsv,lower_red,upper_red)
	
	# Defining upper range for red color detection
	lower_red = np.array([170,120,70])
	upper_red = np.array([180,255,255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)
	
	# Addition of the two masks to generate the final mask.
	mask = mask1+mask2
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
	
	# Replacing pixels corresponding to cloak with the background pixels.
	"""
	access all the pixels which have value of 255 in
	the final mask (The pixels corresponding to the detected red colour), and we replace the pixel
	values with the pixel values of respective coordinates in the background frame
	"""

	img[np.where(mask==255)] = background[np.where(mask==255)]
	cv2.imshow('Display',img)
	k = cv2.waitKey(10)
	if k == 27:
		break

