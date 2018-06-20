
#Author:Daniel Lindberg

import time
import numpy as np
import argparse
import cv2
import sys
from select import select

#obtain the capture image
cap = cv2.VideoCapture(0)
#by default display canny
n = 'c'
#set the default timeout time to be 0
timeout=0
#always run until program is stopped
time_stamps = []
time_stamps.append(time.time())
while('q' not in n):
    #obtain the frames
    ret, frame = cap.read()
    time_stamps.append(time.time())
    #display in terminal to print canny or sobel
    print "\n Press C for canny, Press S for Sobel",
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        #read in the current line
        n= sys.stdin.readline()
        print n + "\n"
    else :
        print "no input. moving on..."
    #print the option in which it will do , s for sobel, c for canny
    print "n = "+ n + "\n"
    #if the input was c use the canny program
    if 'c' in n or 'C' in n:
        #if the input was c use the canny method on the read frame
        edit_frame = cv2.Canny(frame,100,200)
    elif 's' in n or 'S' in n:
        #if the input was s use the sobel method on the read frame
        edit_frame = cv2.Sobel(frame,cv2.CV_64F, 1, 1, ksize=3)
    else:
        continue
    #show the image wether it is canny or sobel
    cv2.imshow('Frame', edit_frame)
    #wait a hot second
    k= cv2.waitKey(1);
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()
#destroy the program if it is not running
diffs = []
i = 1;
#set the worst case as 0, as it will start out as smallest value
worst_case = 0
while i < len(time_stamps):
    #if the difference is greater than the worst case make it the worst case
    if (abs(time_stamps[i] - time_stamps[i-1]) > worst_case):
        worst_case = abs(time_stamps[i] - time_stamps[i-1])
        #append to the list the time difference
    diffs.append(abs(time_stamps[i] - time_stamps[i-1]))
    i=i+1
i=0
#gets the average difference of times (framerate)
average_framerate = sum(diffs)/len(diffs)
while i < len(diffs):
    #print the jitter of each frame
    print "Frame:"+ str(i) + " jitter:"+ str(diffs[i]-average_framerate)
    i=i+1
print "average framerate = " + str(average_framerate)
print "worst case = " + str(worst_case)
