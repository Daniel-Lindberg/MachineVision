#Author: Daniel Lindberg

'''
Code to take the video .mpeg file and convert it into a bunch of .pgm files
'''
import cv2
import numpy

#take the video capture frame
cap = cv2.VideoCapture("../Dark-Room-Laser-Spot.mpeg")
while not cap.isOpened():
	cap = cv2.VideoCapture("../Dark-Room-Laser-Spot.mpeg")
	cv2.waitKey(1000)
	print "Wait for the header"

pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
i=0
while True:
    flag, frame = cap.read()
    if flag:
        path_name = str("Frame"+str("{0:0=4d}".format(i))+".pgm")
        cv2.imwrite( path_name, frame)
        i=i+1
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