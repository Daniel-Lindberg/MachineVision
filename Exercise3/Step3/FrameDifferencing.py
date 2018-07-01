#Author: Daniel Lindberg

'''
use frame differencing for R,G & B to remove the bookshelf
background and to preserve the moving laser spot foreground. 
Re-encode the difference frames that result. How effective was
this at removing clutter?
'''
import cv2
import numpy

#take the video capture frame
cap = cv2.VideoCapture("../Dark-Room-Laser-Spot-with-Clutter.mpeg")
while not cap.isOpened():
	cap = cv2.VideoCapture("../Dark-Room-Laser-Spot-with-Clutter.mpeg")
	cv2.waitKey(1000)
	print "Wait for the header"

pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
#threshold value in which we are going to filter on the median filter
threshold = 250
while True:
    flag, frame = cap.read()
    if flag:
        # The frame is ready and already captured
        gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # apply the 3x3 median filter on the image
        processed_image = cv2.medianBlur(gray_scale, 3)
        #go through the grayscale image with median blur, if it hits a threshold for a value
        #then set it to 0 if it is not at that threshold. therefore removing clutter
        (thresh, im_bw) = cv2.threshold(processed_image, 245, threshold, 0)
        '''
        for (x,y), value in numpy.ndenumerate(processed_image):
        	if processed_image[x,y] > threshold:
        		pass
        	else:
        		processed_image[x,y] = 0.0
        '''
        #display image
        cv2.imshow('video', im_bw)
        pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        print str(pos_frame)+" frames"
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
        print "frame is not ready"
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)

    if cv2.waitKey(10) == 27:
        break
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break
'''
# read the image 
image = cv2.imread(image_path)
red_image = image.copy()
#set blue and green channels to 0
red_image[:, :, 0] = 0
red_image[:, :, 1] = 0
# display image
cv2.imshow('Median Filter Processing', red_image)
# save image to disk
cv2.imwrite('processed_image.png', red_image)
# pause the execution of the script until a key on the keyboard is pressed
cv2.waitKey(0)
'''