#Author:Daniel Lindberg

import time
import cv2
import numpy as np

#obtain the capture image
#cap = cv2.VideoCapture(0)

#Used for the erode function
kernel = np.ones((3,3),np.uint8)

done=False

#get the start time
start_time = time.clock()

#iterator for number of frames 
i = 0

#Do this loop for 100 second
while(True):
    #obtain the frames
    frame=cv2.imread('Frame0012.png')

    #encode in grayscale
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    size=np.size(frame)
    skel=np.zeros(frame.shape,np.uint8)

    #apply the threshold
    ret, frame=cv2.threshold(frame, 70,255,cv2.THRESH_BINARY)

    #Get the negative of the image
    frame = 255-frame
    
    #apply the median blur on replace blurr value of 1
    frame = cv2.medianBlur(frame, 1)

    #Do the skeleton processing loop
    """
    This section of code was adapted from the following post, which was
    based in turn on the Wikipedia description of a morphological skeleton
    http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/
    """
    element=cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    counter = 0
    while (counter <=100):
        eroded = cv2.erode(frame, element)
        temp = cv2.dilate(eroded, element)
        temp=cv2.subtract(frame, temp)
        skel=cv2.bitwise_or(skel,temp)
        img=eroded.copy()

        counter=counter+1
        zeros= size - cv2.countNonZero(frame)
        if zeros==size:
            done=True

    #write the frame to be made into a MPEG via ffmpeg
    path_name = str("Skeleton"+str("{0:0=4d}".format(i))+".png")
    cv2.imwrite( path_name, frame)
    i = i +1
    #wait a hot second
    k= cv2.waitKey(1);
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()
