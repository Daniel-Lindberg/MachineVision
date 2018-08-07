#Author:Daniel Lindberg

import time
import cv2
import numpy as np
from skimage.morphology import skeletonize

#obtain the capture image
cap = cv2.VideoCapture(0)

#Used for the erode function
kernel = np.ones((3,3),np.uint8)

done=False

#get the start time
start_time = time.clock()

#iterator for number of frames 
i = 0

def bottomUpSkeleton(img):
    skeleton= np.zeros(img.shape,np.uint8)
    eroded=np.zeros(img.shape,np.uint8)
    temp=np.zeros(img.shape,np.uint8)
    _,thresh = cv2.threshold(img, 70,255,cv2.THRESH_BINARY)
    kernel=cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    iters=0
    while(True):
        cv2.erode(thresh,kernel,eroded)
        cv2.dilate(eroded,kernel,temp)
        cv2.subtract(thresh,temp,temp)
        cv2.bitwise_or(skeleton,temp,skeleton)
        thresh, eroded = eroded, thresh

        iters+=1
        if cv2.countNonZero(thresh) == 0:
            return(skeleton,iters)

#Do this loop for 100 second
while(time.clock()-start_time <= 100):
    #obtain the frames
    ret, frame = cap.read()
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    skeleton, iters = bottomUpSkeleton(frame)

    #write the frame to be made into a MPEG via ffmpeg
    path_name = str("Frame"+str("{0:0=4d}".format(i))+".png")
    cv2.imwrite(path_name,skeleton)
    i = i +1
    #wait a hot second
    k= cv2.waitKey(1);
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()
