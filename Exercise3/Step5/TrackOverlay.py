#Author: Daniel Lindberg

'''
Use the Dark Room Laser Spot video you converted to a series
of graymap frames (using G band) and write a threshold function
based on your analysis of the characteristics of the edges of
this spot in the G band - raster each frame to determine the 
X- bar, Y-bar object COM based on X row maximum extents and 
Y column maximum extents and your threshold detector. Use the
Median Filter and/or Sharpen PSF if you want toenhance the 
image prior to threshold detection of the X and Y edges. 
Mark the COM (Center of Mass) and track it in each frame with
cross-hairs (at saturation level of 255 - should appear as 
white lines) so that the re-encoded video has tracking overlay.
'''
import cv2
import numpy
import imutils

#take the video capture frame
cap = cv2.VideoCapture("../Dark-Room-Laser-Spot.mpeg")
while not cap.isOpened():
	cap = cv2.VideoCapture("../Dark-Room-Laser-Spot.mpeg")
	cv2.waitKey(1000)
	print "Wait for the header"

pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
#threshold value in which we are going to filter on the median filter
threshold = 150
while True:
    flag, frame = cap.read()
    if flag:
        # The frame is ready and already captured
        #convert the image to grayscale
        gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #Filter the image for a threshold. Go through every pixel if it hits a threshold for a value
        #then set it to 0 if it is not at that threshold. therefore removing clutter
        (thresh, im_bw) = cv2.threshold(gray_scale, 0, threshold, 0)
        #Finds the contours of the object and puts the contours in the contours variable 
        im2, contours, hierarchy= cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #assuming you find a contour
        if len(contours) != 0:
            #find the largest contour object
            maximum_contour = max(contours, key = cv2.contourArea)
            #get the values associated with that contour with the moments command
            M = cv2.moments(maximum_contour)
            #Check to see that the value is not 0 , so you can divide
            if M["m00"] != 0:
                #get the Center values of the contour
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                #if the contour has the moments value set to 0, set the center to be the top left of the screen
                cX, cY = 0, 0
            #Draw the crosshairs that are yellow, 10 below and above the center respectively
            cv2.line(frame, (cX-10, cY), (cX+10, cY), (0,255,255), 5)
            cv2.line(frame, (cX, cY-10), (cX, cY+10), (0,255,255), 5)
        #display image
        cv2.imshow('video', frame)
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