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

#Do this loop for 100 second
while(time.clock()-start_time <= 100):
    #obtain the frames
    ret, frame = cap.read()

    skeleton = skeletonize(frame)

    #write the frame to be made into a MPEG via ffmpeg
    path_name = str("Frame"+str("{0:0=4d}".format(i))+".png")
    cv2.imshow(skeleton)
    i = i +1
    #wait a hot second
    k= cv2.waitKey(1);
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()
